"""Collect previous Actions artifacts, compare hashes and stop the bounded study."""
import argparse
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
import zipfile
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[2]
REPO='ralves025/portugal_noticias'
WORKFLOW='p0-fontes.yml'

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None


def api(path, method='GET'):
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+path,method=method,
        headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],
                 'Accept':'application/vnd.github+json','User-Agent':'PortugalNoticias-P0'})
    opener=urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req,timeout=30) as r:
            body=r.read(5*1024*1024)
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        if e.code==302:
            # Never forward the GitHub token to the signed artifact URL.
            url=e.headers['Location']
            if not url.startswith('https://'): raise ValueError('insecure_redirect')
            with urllib.request.urlopen(url,timeout=30) as r:
                data=r.read(5*1024*1024+1)
                if len(data)>5*1024*1024: raise ValueError('artifact_too_large')
                return data
        raise


def previous():
    artifacts=api('actions/artifacts?per_page=100')['artifacts']
    snapshots=[]
    for a in artifacts:
        if not a['name'].startswith('p0-snapshot-') or a['expired']: continue
        if str(a.get('workflow_run',{}).get('id'))==os.getenv('GITHUB_RUN_ID'): continue
        data=api('actions/artifacts/'+str(a['id'])+'/zip')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            info=archive.getinfo('snapshot.json')
            if info.file_size>3*1024*1024: raise ValueError('snapshot_too_large')
            snapshots.append(json.loads(archive.read(info)))
        if len(snapshots)>=12: break
    return snapshots


def timeline(snapshots):
    ordered=sorted(snapshots,key=lambda s:s['observed_at'])
    scheduled={}
    for s in ordered:
        when=datetime.fromisoformat(s['observed_at']).astimezone(ZoneInfo('Europe/Lisbon'))
        if s['event']=='schedule' and 9<=when.hour<12:
            scheduled[when.date().isoformat()]=s
    lines=['# P0 — comparação temporal','',f'Amostras disponíveis: {len(ordered)}.',
           f'Manhãs distintas observadas por agendamento (09h–12h): {len(scheduled)}.',
           'A janela de três horas identifica atrasos; não garante pontualidade às 9h.', '',
           '| Coleta UTC | Feed | Estado | Itens | Novos hashes vs amostra anterior válida |',
           '| --- | --- | --- | --- | --- |']
    prev={}
    for s in ordered:
        for r in s['results']:
            ids={i['id_hash'] for i in r.get('items',[]) if i.get('id_hash')}
            added=len(ids-prev[r['id']]) if r['id'] in prev and r['status']=='ok' else '-'
            lines.append(f"| {s['observed_at']} | {r['id']} | {r['status']} | {r.get('item_count','-')} | {added} |")
            if r['status']=='ok': prev[r['id']]=ids
    lines+=['','## Situação da observação','',
            'Três manhãs registradas; interpretar os resultados por fonte.' if len(scheduled)>=3
            else 'Observação ainda insuficiente para concluir três manhãs; não declarar P0 concluída.',
            '', 'Novos hashes indicam alterações na lista, não necessariamente notícias publicadas desde a última coleta.',
            'Falhas e feeds vazios não são apagados. O relatório técnico não concede direitos de publicação.']
    lines += ['', '## Resultado técnico por feed nas manhãs agendadas', '',
              '| Feed | Manhãs com leitura válida | Menor janela observada (h) | Avaliação |',
              '| --- | --- | --- | --- |']
    ids = sorted({r['id'] for s in ordered for r in s['results']})
    for feed_id in ids:
        rows = [r for s in scheduled.values() for r in s['results'] if r['id'] == feed_id]
        valid = [r for r in rows if r['status'] == 'ok']
        spans = [r['span_hours'] for r in valid if r.get('span_hours') is not None]
        if len(rows) < 3:
            verdict = 'Observação incompleta'
        elif len(valid) < 3:
            verdict = 'Falhas ou descoberta pendente; não aprovar integração'
        elif spans and min(spans) < 24:
            verdict = 'Leitura consistente; cobertura diária possivelmente parcial'
        else:
            verdict = 'Leitura consistente na amostra; cobertura integral não comprovada'
        lines.append(f"| {feed_id} | {len(valid)}/{len(rows)} | {min(spans) if spans else '-'} | {verdict} |")
    lines += ['', 'Uso público continua pendente conforme docs/p0/README.md. Nenhuma fonte foi ativada.',
              'As amostras matinais devem ter datas consecutivas; inspecionar a cronologia antes da conclusão final.']
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['gate','compare','disable']); args=p.parse_args()
    cfg=json.loads((ROOT/'scripts/p0/sources.json').read_text(encoding='utf-8-sig'))
    now=datetime.now(timezone.utc).astimezone(ZoneInfo(cfg['timezone']))
    today=now.date().isoformat()
    if args.command=='gate':
        run=cfg['observation_start']<=today<=cfg['observation_end']
        finish=today>cfg['observation_end'] or (today==cfg['observation_end'] and now.hour>=9)
        with open(os.environ['GITHUB_OUTPUT'],'a') as f:
            f.write(f"run={str(run).lower()}\nfinish={str(finish).lower()}\n")
    elif args.command=='disable':
        api('actions/workflows/'+WORKFLOW+'/disable',method='PUT')
        print('Agendamento P0 desativado ao final da janela de observação.')
    else:
        out=ROOT/'p0-results'
        current=json.loads((out/'snapshot.json').read_text())
        snapshots=previous()+[current]
        md=timeline(snapshots)
        (out/'comparison.md').write_text(md,encoding='utf-8')
        if os.getenv('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f: f.write(md)
        print(md)

if __name__=='__main__': main()
