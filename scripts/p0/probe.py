"""Bounded feed feasibility probe. Stores metrics/hashes, never article text."""
import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import hashlib
from html.parser import HTMLParser
import ipaddress
import json
import os
from pathlib import Path
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
MAX_BYTES = 2 * 1024 * 1024
UA = 'PortugalNoticias-P0/0.1 (+https://github.com/ralves025/portugal_noticias)'
UTC = timezone.utc


def stamp(dt):
    return dt.astimezone(UTC).isoformat()


def canonical(url, base):
    p = urllib.parse.urlsplit(urllib.parse.urljoin(base, url))
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('invalid_url')
    query = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)
             if not k.lower().startswith('utm_') and k.lower() != 'fbclid']
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path,
                                   urllib.parse.urlencode(query), ''))


def validate_target(url, hosts):
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or p.hostname not in hosts or p.username or p.password or p.port not in (None, 443):
        raise ValueError('target_not_allowed')
    addresses = socket.getaddrinfo(p.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('non_public_target')


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, hosts, chain):
        self.hosts, self.chain = hosts, chain

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if len(self.chain) >= 3:
            raise ValueError('too_many_redirects')
        validate_target(newurl, self.hosts)
        self.chain.append({'status': code, 'url': newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, hosts, method='GET'):
    validate_target(url, hosts)
    chain = []
    opener = urllib.request.build_opener(Redirects(hosts, chain))
    req = urllib.request.Request(url, method=method, headers={
        'User-Agent': UA, 'Accept-Encoding': 'identity',
        'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/html;q=0.5'})
    start = time.monotonic()
    try:
        with opener.open(req, timeout=15) as r:
            meta = {'http_status': r.status, 'final_url': r.url,
                    'content_type': r.headers.get('Content-Type', ''),
                    'etag': r.headers.get('ETag'), 'last_modified': r.headers.get('Last-Modified'),
                    'redirects': chain}
            if r.headers.get('Content-Encoding', 'identity') not in ('identity', ''):
                raise ValueError('unsupported_compression')
            data = r.read(MAX_BYTES + 1) if method == 'GET' else b''
            if len(data) > MAX_BYTES:
                raise ValueError('response_too_large')
            meta.update(bytes=len(data), elapsed_ms=round((time.monotonic()-start)*1000))
            return data, meta
    except urllib.error.HTTPError as e:
        # No retry, no response body saved, no evasion of access controls.
        return b'', {'http_status': e.code, 'final_url': e.url, 'redirects': chain,
                     'retry_after': e.headers.get('Retry-After'),
                     'elapsed_ms': round((time.monotonic()-start)*1000)}


def localname(tag):
    return tag.rsplit('}', 1)[-1]


def field(node, names):
    for child in node:
        if localname(child.tag) in names:
            return ''.join(child.itertext()).strip()
    return ''


def parse_date(value):
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
    except (ValueError, TypeError, OverflowError):
        try:
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return None
    return dt.astimezone(UTC) if dt.tzinfo else None


def parse_feed(data, base, now):
    # Deliberately accept UTF-8 only; fail visibly on other encodings in this probe.
    text = data.decode('utf-8-sig')
    if '\x00' in text or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('unsafe_xml')
    root = ET.fromstring(text)
    if localname(root.tag) not in ('rss', 'feed', 'RDF'):
        raise ValueError('not_rss_or_atom')
    nodes = [n for n in root.iter() if localname(n.tag) in ('item', 'entry')]
    if len(nodes) > 1000:
        raise ValueError('too_many_items')
    items, urls, categories = [], [], Counter()
    invalid_titles = invalid_links = missing_dates = invalid_dates = future_dates = 0
    for n in nodes:
        title = field(n, {'title'})
        link = field(n, {'link'})
        if localname(n.tag) == 'entry':
            link = next((c.get('href', '') for c in n if localname(c.tag) == 'link'
                         and c.get('rel', 'alternate') == 'alternate'), '')
        invalid_titles += not bool(title)
        url = None
        try:
            if not link:
                raise ValueError('missing_link')
            url = canonical(link, base)
        except ValueError:
            invalid_links += 1
        raw_date = field(n, {'pubDate', 'published', 'date'})
        dt = parse_date(raw_date)
        missing_dates += not bool(raw_date)
        invalid_dates += bool(raw_date) and dt is None
        if dt and dt > now + timedelta(minutes=10):
            future_dates += 1
            dt = None
        for c in n:
            if localname(c.tag) == 'category':
                category = (c.get('term') or ''.join(c.itertext())).strip()
                if category:
                    categories[category[:120]] += 1
        identity = url or field(n, {'guid', 'id'})
        items.append({'id_hash': hashlib.sha256(identity.encode()).hexdigest() if identity else None,
                      'published_at': stamp(dt) if dt else None,
                      'title_present': bool(title), 'link_valid': bool(url),
                      'guid_present': bool(field(n, {'guid', 'id'}))})
        if url:
            urls.append(url)
    dates = [parse_date(i['published_at']) for i in items if i['published_at']]
    return {'format': localname(root.tag), 'item_count': len(nodes),
            'missing_titles': invalid_titles, 'invalid_links': invalid_links,
            'missing_dates': missing_dates, 'invalid_dates': invalid_dates,
            'future_dates': future_dates, 'duplicate_urls': len(urls)-len(set(urls)),
            'newest_published_at': stamp(max(dates)) if dates else None,
            'oldest_published_at': stamp(min(dates)) if dates else None,
            'span_hours': round((max(dates)-min(dates)).total_seconds()/3600, 2) if dates else None,
            'items_last_24h': sum(now-timedelta(hours=24) <= d <= now for d in dates),
            'categories': dict(categories), 'items': items}, list(dict.fromkeys(urls))[:2]


class FeedLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('type') in ('application/rss+xml', 'application/atom+xml'):
            self.links.append(a.get('href', ''))


def probe(entry, now, discovery=False):
    result = {k: v for k, v in entry.items() if k != 'hosts'}
    result['observed_at'] = stamp(now)
    result['publication_approved'] = False
    try:
        data, meta = fetch(entry['url'], entry['hosts'])
        result.update(meta)
        if meta['http_status'] != 200:
            result['status'] = 'http_error'
        elif discovery:
            parser = FeedLinks()
            parser.feed(data.decode('utf-8', 'replace'))
            result.update(status='discovery_only', discovered_feeds=parser.links)
        else:
            metrics, sample = parse_feed(data, meta['final_url'], now)
            result.update(metrics, status='ok' if metrics['item_count'] else 'empty_feed')
            checks = []
            for url in sample:
                # Verify reachability with HEAD only, without saving articles or URLs.
                check = {'id_hash': hashlib.sha256(url.encode()).hexdigest()}
                try:
                    _, head = fetch(url, entry['hosts'], method='HEAD')
                    check['http_status'] = head['http_status']
                except Exception as e:
                    check['error'] = type(e).__name__
                checks.append(check)
            result['sample_link_checks'] = checks
    except Exception as e:
        result.update(status='probe_error', error_type=type(e).__name__)
        if isinstance(e, ValueError):
            result['error_code'] = str(e)[:100]
    return result


def summary(report):
    rows = ['# P0 — amostra técnica', '', f"Coleta UTC: {report['observed_at']}",
            f"Ambiente: {report['environment']}; evento: {report['event']}", '',
            '| Fonte/feed | Estado | HTTP | Itens | Janela (h) |', '| --- | --- | --- | --- | --- |']
    for r in report['results']:
        rows.append(f"| {r['id']} | {r['status']} | {r.get('http_status', '-')} | {r.get('item_count', '-')} | {r.get('span_hours', '-')} |")
    rows += ['', 'Sucesso técnico não aprova publicação. HEAD 403/405 não prova link quebrado.',
             'A janela entre datas não demonstra que todas as notícias do intervalo estão presentes.',
             'Detalhes e identificadores hash estão em snapshot.json; textos e corpos não são armazenados.']
    return '\n'.join(rows) + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='p0-results')
    args = parser.parse_args()
    config = json.loads((ROOT/'scripts/p0/sources.json').read_text(encoding='utf-8-sig'))
    now = datetime.now(UTC)
    report = {'schema_version': 1, 'observed_at': stamp(now),
              'environment': 'github-actions' if os.getenv('GITHUB_ACTIONS') else 'local',
              'event': os.getenv('GITHUB_EVENT_NAME', 'local'),
              'run_id': os.getenv('GITHUB_RUN_ID'), 'commit': os.getenv('GITHUB_SHA'),
              'results': []}
    for entry in config['feeds']:
        report['results'].append(probe(entry, datetime.now(UTC)))
    for entry in config['discovery_pages']:
        report['results'].append(probe(entry, datetime.now(UTC), discovery=True))
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    (out/'snapshot.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    md = summary(report)
    (out/'summary.md').write_text(md, encoding='utf-8')
    print(md)
    # Source failures are findings, not an infrastructure exception. Artifacts must survive.
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
