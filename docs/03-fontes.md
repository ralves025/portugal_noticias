# Fontes de notícias

Pesquisa documental realizada em 05/09/2026. Disponibilidade de RSS não equivale a autorização irrestrita de republicação. O projeto usará somente campos compatíveis com as condições verificadas de cada fonte.

## Inventário inicial

| Veículo | Evidência / ponto de partida | Estado |
| --- | --- | --- |
| RTP Notícias | [Página oficial RSS](https://www.rtp.pt/noticias/rss/feeds), que informa o endpoint https://www.rtp.pt/noticias/rss | RSS documentado; XML e condições de uso ainda precisam ser testados/revisados |
| Público | [Site oficial](https://www.publico.pt/) | Candidato; endpoint atual e condições não confirmados |
| Observador | [Site oficial](https://observador.pt/); tentativa de abrir https://observador.pt/feed/ retornou erro na ferramenta de pesquisa | Candidato; erro não comprova ausência de feed |
| Renascença | [Site oficial](https://rr.sapo.pt/) | Candidato para ampliar diversidade; integração não verificada |
| SIC Notícias | [Site oficial](https://sicnoticias.pt/) | Candidato; integração não verificada |

Os links dos candidatos são pontos de investigação, não endpoints aprovados. A página da RTP enumera Últimas, País, Mundo, Desporto, Economia, Cultura, Vídeos e Áudios; começar pelo conteúdo textual. Não presumir que exista um feed específico para cada tema interno do produto.

## Protocolo de validação — pacote P0

1. Localizar feed ou API por página oficial ou metadados do veículo; não adivinhar URLs e marcar como confirmadas.
2. Registrar URL final, redirecionamentos, status HTTP, tipo e tamanho da resposta, data e executor da verificação.
3. Testar parsing e inspecionar amostra: título, link, GUID, data, categorias e eventual descrição.
4. Verificar condições publicadas para agregação, atribuição, cache e trechos; registrar URL e conclusão limitada à evidência encontrada. Se ambíguas, manter a integração pendente ou usar apenas um link ao veículo.
5. Registrar mapeamento de categorias e particularidades, incluindo itens sem data e links relativos.
6. Repetir a coleta em outro momento para verificar atualização e duplicatas. Um feed estático não prova cobertura diária.
7. Ativar somente após passar pela validação técnica e definir os campos permitidos. Se uma fonte falhar, avançar com outra candidata.

## Registro a preencher por fonte

| Campo | Valor inicial |
| --- | --- |
| ID / nome / site | A preencher |
| Feed e hosts permitidos | A preencher após descoberta |
| Evidência oficial e termos | URLs + data + observações |
| Estado | pending / active / disabled |
| Campos exibíveis | Título, URL e atribuição; confirmar por fonte |
| Descrição permitida | Não, até revisão específica |
| Categorias e mapeamento | A preencher |
| Resultado de parsing / atualização | Não testado |
| Restrições e periodicidade | A preencher |

## Política de conteúdo proposta

- Preservar título, autoria quando disponível e nome do veículo; abrir a URL original.
- Excluir corpo integral e imagens. Descrição curta é opcional e só entra se permitida; limite visual proposto de 240 caracteres não substitui permissão.
- Converter eventual descrição permitida em texto simples; não renderizar HTML externo.
- Não contornar assinatura, login ou bloqueio; não assumir acesso gratuito a todos os links.
- Não apagar matérias de veículos distintos por tratarem do mesmo acontecimento. Deduplicar somente a mesma publicação conforme arquitetura.
- Não apresentar diversidade de veículos como garantia automática de neutralidade ou veracidade.
