# P0 — execução e resultados

Estado: primeira amostra local concluída; configuração da nuvem em validação. A P0 completa depende das manhãs agendadas e da análise de uso público. Data: 06/09/2026.

## Escopo autorizado

Testar RTP (País, Desporto, Cultura), A Bola e Observador; investigar o acesso e descoberta do Público. Não implementar o webapp, ativar fontes em produção ou publicar matérias. A autorização do usuário para executar a P0 inclui configurar Actions, validar, integrar por pull request e observar as próximas manhãs.

## Primeira amostra local

Coleta iniciada em 06/09/2026 às 03:20 UTC (04:20 em Portugal continental). Esta amostra não conta como uma das três manhãs às 9h.

| Feed | HTTP | Itens | Intervalo entre publicação mais antiga e mais recente | Últimas 24h |
| --- | --- | --- | --- | --- |
| RTP País | 200 | 50 | 56,18 h | 13 |
| RTP Desporto | 200 | 50 | 32,74 h | 25 |
| RTP Cultura | 200 | 50 | 262,32 h | 1 |
| A Bola | 200 | 325 | 47,58 h | 158 |
| Observador | 200 | 51 | 9,74 h | 51 |
| Público (página de descoberta) | 403 | — | — | — |

Nos cinco feeds: títulos, URLs e datas presentes; nenhuma URL repetida dentro do mesmo feed e nenhuma data futura rejeitada. Dois links por feed responderam HTTP 200 via HEAD. Isso comprova resposta da amostra de links, não leitura integral gratuita nem disponibilidade de todos os artigos.

A janela entre datas não comprova cobertura completa. Observador mostrou uma janela inferior a 24h; será necessário aceitar cobertura parcial ou procurar feeds temáticos oficiais, se existirem. A Bola apresentou 325 itens, portanto o limite proposto de 100 itens do futuro coletor exige revisão para não truncar a cobertura diária. O probe admite até 1.000 itens e 2 MB apenas para medir esse comportamento.

## Categorias e adequação aos temas

- RTP País: vieram categorias País e Cultura; a categoria de cada item deve prevalecer sobre o nome do feed. Política não apareceu como categoria separada nessa amostra, portanto não classificar todo País como Política.
- RTP Desporto: inclui Futebol Nacional, clubes portugueses, modalidades e Futebol Internacional. O feed não é exclusivamente português; o filtro geográfico precisa de regra própria.
- RTP Cultura: categoria Cultura em todos os 50 itens; apenas um publicado nas últimas 24h. Uma lista diária curta não significa falha da fonte.
- A Bola: sem categorias no RSS observado. Atribuir Desporto é possível pelo catálogo; separar âmbito nacional e internacional permanece pendente sem depender de scraping de matérias.
- Observador: múltiplas etiquetas por item, incluindo Política, Sociedade, Desporto, Cultura, Mundo e Opinião. Mapeamento proposto: categoria explícita do tema; distinguir Opinião antes de apresentar como notícia factual. Não inferir tema só pelo primeiro rótulo.

## Condições de uso e decisão de publicação

Estas são observações documentais, não uma autorização concedida pelo projeto. Acesso técnico e permissão de exibição têm estados separados. Todos os feeds permanecem com publication_approved=false.

| Veículo | Evidência oficial | Conclusão limitada à evidência |
| --- | --- | --- |
| RTP | [RSS](https://www.rtp.pt/noticias/rss/feeds) e [termos, §§4 e 7.2](https://media.rtp.pt/rgpd/termos-e-condicoes/) | A página orienta uso em leitores RSS. Os termos admitem uso pessoal com atribuição, mas restringem outros usos e links de plataformas externas. Não considerar automaticamente autorizado um hub público com links profundos; esclarecer essa condição antes da ativação pública. |
| A Bola | [Termos, §§1–2](https://www.abola.pt/termos-e-condicoes) | O texto contempla uso informativo com atribuição e também ressalva autorização para propriedade intelectual. Manter aprovação pública pendente até resolver o alcance aplicável ao hub. |
| Observador | [Termos, §1](https://observador.pt/termos-e-condicoes/) | O texto limita uso sem consentimento aos fins privados permitidos. Integração pública continua pendente. |
| Público | [Site oficial](https://www.publico.pt/) | Acesso automatizado devolveu 403. Endpoint atual e condições ainda não confirmados; não contornar o bloqueio. |

Leitura realizada em 06/09/2026; a página do Observador disponível na pesquisa pode refletir cache, exigindo reconferência antes de ativação. Não foram enviados pedidos de autorização aos veículos.

## Operação da observação na nuvem

Workflow: `.github/workflows/p0-fontes.yml`. Repositório público com Actions habilitado; runner padrão Ubuntu. Código Python 3.11 sem dependências de terceiros. Actions oficiais fixadas por SHA. Sem secrets de jornais ou banco; token temporário do GitHub para ler artifacts e, apenas no job final, desativar o próprio workflow.

- Primeira execução manual após integração revisada na main.
- Coletas agendadas para 9h Europe/Lisbon em 6, 7 e 8 de setembro de 2026. O dia 9 é apenas uma oportunidade adicional de encerramento caso o job final anterior não rode.
- Limite de datas no script impede coleta fora de 06–08/09/2026, inclusive em anos futuros.
- Ao terminar a janela, o job de encerramento desativa o workflow. Uma falha nessa etapa deve aparecer como falha da execução; o limite de datas continua impedindo novas consultas aos veículos.
- O GitHub pode atrasar ou não entregar um disparo. Registrar a hora efetiva; contar como manhã observada apenas execuções schedule entre 09h e 12h locais em datas distintas. Amostras ausentes não são inventadas ou substituídas silenciosamente por execução manual.
- Cada artifact `p0-snapshot-...` fica disponível por 7 dias e contém snapshot.json, summary.md e comparison.md. O relatório compara hashes com amostras anteriores, preservando falhas. Não salva títulos, descrições, matérias ou URLs individuais em claro.
- O resumo da execução mostra a comparação. Ao final, baixar o artifact mais recente e consolidar o resultado em documento via develop → PR → main. Não marcar a P0 aprovada apenas porque o workflow terminou sem erro.

Referências: [agendamento do Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onschedule), [custos](https://docs.github.com/en/billing/concepts/product-billing/github-actions). Retenção curta limita armazenamento; não foi contratado plano nem alterado orçamento da conta.

## Reproduzir e validar

`python -m unittest discover -s tests/p0 -v` executa testes com dados fictícios, sem rede.

`python scripts/p0/probe.py` executa uma amostra real e grava em p0-results/ (ignorado pelo Git). Windows precisa de Python 3.11; cloud.py usa a base de fusos do runner Ubuntu. Arquivos temporários locais e credenciais não são versionados.

Validação realizada: nove testes passaram localmente, cobrindo RSS/Atom, campos ausentes, datas futuras, XML malformado/perigoso, deduplicação, destinos bloqueados, erros HTTP e comparação temporal. Ainda verificar testes e primeira coleta no Actions.

Limites do probe: UTF-8 apenas; destinos restritos ao catálogo com validação DNS e redirecionamentos, mas sem conexão com IP fixado após DNS. É uma ferramenta de diagnóstico para catálogo controlado, não um endpoint público nem o coletor de produção. Condicionais ETag/304 são registradas mas ainda não exercitadas; a observação baixa a lista completa para permitir comparação independente entre execuções.
