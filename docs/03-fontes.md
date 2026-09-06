# Fontes de notícias

Pesquisa documental realizada em 05/09/2026. Disponibilidade de RSS não equivale a autorização irrestrita de republicação. O projeto usará somente campos compatíveis com as condições verificadas de cada fonte.

## Inventário inicial

| Veículo | Evidência / ponto de partida | Estado |
| --- | --- | --- |
| RTP Notícias | [Página oficial RSS](https://www.rtp.pt/noticias/rss/feeds), que informa o endpoint https://www.rtp.pt/noticias/rss | Três feeds testados localmente em 06/09; observação temporal e aprovação pública pendentes (ver relatório P0) |
| Público | [Site oficial](https://www.publico.pt/) | Página de descoberta retornou HTTP 403 localmente em 06/09; endpoint atual e condições pendentes |
| Observador | [Site oficial](https://observador.pt/); tentativa de abrir https://observador.pt/feed/ retornou erro na ferramenta de pesquisa | Feed confirmado no HTML oficial e testado localmente em 06/09; janela observada de 9,74h; uso público pendente |
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

## Sugestões para avaliar com o usuário

Prioridades informadas: atualidade nacional portuguesa, política portuguesa, desporto português e cultura. Proposta de conjunto inicial: RTP + Público + A Bola; Observador como opção adicional para comparar coberturas. Não representa escolha final do usuário nem aprovação técnica das integrações.

| Veículo | Papel sugerido | Referência editorial |
| --- | --- | --- |
| RTP | Base generalista, com canais de País, Cultura e Desporto | [RSS oficial](https://www.rtp.pt/noticias/rss/feeds) |
| Público | Complementar política e cultura, incluindo Ípsilon | [Ficha técnica e editorias](https://www.publico.pt/nos/ficha-tecnica) |
| A Bola | Cobertura especializada de desporto; conferir variedade além de futebol | [Apresentação do veículo](https://www.abola.pt/sobre) |
| Observador | Outra redação para comparar a cobertura da atualidade | [Estatuto editorial](https://observador.pt/estatuto-editorial/) |

Referências consultadas em 06/09/2026. A Bola passa a ser candidata; feed, condições de agregação e acesso às matérias continuam pendentes. As sugestões dizem respeito à cobertura editorial; não asseguram RSS disponível ou leitura integral gratuita.

## P0 em linguagem simples

P0 é um teste de viabilidade das fontes: descobrir de quais veículos o hub consegue receber referências de notícias automaticamente, com regularidade e nas condições apropriadas. A escolha de um veículo e sua integração são decisões distintas.

RSS é uma lista que o próprio site disponibiliza para programas, normalmente com título, link e data das notícias. O teste verifica se essa lista existe, funciona e atende aos temas escolhidos.

Exemplo com a RTP (passos futuros, não resultados já obtidos):

1. Usar a página oficial para localizar as listas de País, Cultura e Desporto.
2. Ler uma pequena amostra e verificar se há títulos, links válidos, datas e temas aproveitáveis.
3. Conferir as condições publicadas e quais campos poderão ser exibidos no hub.
4. Repetir a leitura em momentos diferentes, incluindo manhã, tarde e após o intervalo noturno, para ver se chegam novas notícias e quanto histórico permanece no feed.
5. Registrar a conclusão: utilizável, utilizável com limitações ou pendente/inviável, com evidências.

O resultado será uma tabela por veículo, com temas cobertos, situação técnica, limitações de conteúdo e recomendação de inclusão. Uma fonte pode ter boa cobertura jornalística e não oferecer uma integração adequada ao MVP.

Proposta de verificação temporal: amostras distribuídas por 24–48 horas, registradas quando efetivamente realizadas; esse período é uma janela de observação, não uma promessa de disponibilidade. Validar especialmente o intervalo entre duas manhãs consecutivas, pois a decisão do MVP é uma coleta diária às 9h de Portugal continental. Verificar se os feeds conservam cobertura suficiente durante esse intervalo, inclusive fins de semana. A hipótese de que a manhã oferece um panorama útil deve ser avaliada por fonte; não pressupor um horário comum de publicação. Não ativar automações de observação apenas por esta descrição do plano.

O usuário não precisa programar, fornecer senhas de jornais ou escolher todos os veículos previamente. Um agente executa a investigação em tarefa própria e apresenta os resultados para decidir quais fontes entram. A primeira amostra local da P0 foi executada em 06/09/2026. Consulte [resultados e observação na nuvem](p0/README.md); a etapa temporal e a aprovação de uso público continuam pendentes.
