# Arquitetura e contratos

Proposta técnica, ainda não implementada.

## Fluxo

1. Scheduler chama endpoint protegido no Next.js, em runtime Node.js.
2. Serviço de ingestão busca somente feeds ativos do catálogo permitido.
3. Adaptador interpreta XML, valida e normaliza itens.
4. PostgreSQL persiste notícias por upsert e registra o resultado de cada fonte.
5. Interface consulta os dados persistidos por uma API somente de leitura.
6. Favoritos e preferências ficam no localStorage do navegador.

A página não aguarda os veículos externos. Uma falha na coleta mantém o último conjunto válido. Não usar memória de uma função serverless ou disco local como armazenamento permanente.

## Estrutura futura sugerida

- src/app/: páginas, layout e endpoints.
- src/components/: lista, filtros, cartão, avisos e favoritos.
- src/lib/ingestion/: fetch controlado, adaptadores e normalização.
- src/lib/db/: repositórios e cliente exclusivo do servidor.
- src/lib/contracts/: esquemas Zod e tipos públicos.
- src/lib/preferences/: persistência local versionada.
- supabase/migrations/: tabelas, índices e políticas SQL.
- tests/fixtures/: feeds fictícios e respostas inválidas.
- docs/: documentação existente, atualizada junto às decisões.

## Modelo de dados

| Entidade | Campos principais | Restrições |
| --- | --- | --- |
| sources | id, name, site_url, status, terms_url, reviewed_at, excerpt_allowed | id estável; ativação explícita |
| feeds | id, source_id, feed_url, allowed_hosts, category_mapping, etag, last_modified, last_success_at, last_error_at | URL única; pertence a uma fonte |
| articles | id, source_id, canonical_url, url_hash, title, excerpt, author, category, published_at, first_seen_at, updated_at | UNIQUE(source_id, url_hash); datas em UTC |
| feed_items | feed_id, external_id, article_id | UNIQUE(feed_id, external_id); external_id pode usar hash da URL quando GUID faltar |
| ingestion_runs | id, started_at, finished_at, status, inserted_count, updated_count, failed_count | status running/success/partial/failed |
| ingestion_results | run_id, feed_id, status, http_status, item_count, error_code | erro resumido sem credenciais nem corpo remoto |

published_at é nullable; nunca substituir uma publicação desconhecida pela hora de coleta. Ordenar por COALESCE(published_at, first_seen_at) DESC, id DESC; indicar visualmente data desconhecida. Datas inválidas ou mais de 10 minutos no futuro são tratadas como desconhecidas e registradas para inspeção.

Para deduplicar, resolver links relativos usando a URL do feed, aceitar apenas HTTP/HTTPS, remover fragmentos e parâmetros conhecidos de rastreamento (utm_*, fbclid). Preservar outros parâmetros, path e trailing slash: podem identificar conteúdos distintos. O hash é calculado sobre a URL normalizada. GUID serve para detectar alterações de uma publicação no mesmo feed. Se GUID e URL apontarem para registros distintos, registrar conflito e não mesclar silenciosamente. Não deduplicar entre veículos nem por título parecido.

## API pública proposta

GET /api/articles com q (até 100 caracteres), source, category, period=24h|7d|30d, cursor e limit (padrão 20, máximo 50). Os filtros são combinados por AND; períodos usam a data efetiva de ordenação. Busca em título sem distinção de acentos ou caixa, usando consulta parametrizada e normalização PostgreSQL adequada. Category ausente exclui Mundo; category=all inclui todos. Validar enumerações e limitar consultas.

Resposta: items, nextCursor, dataAsOf, stale e partialFailure. Cada item contém id, title, url, source {id, name}, category, publishedAt (nullable), firstSeenAt e excerpt (nullable). Cursor opaco deve carregar a chave de ordenação e um limite temporal de snapshot; mudança de filtro inicia nova paginação. Tratar o cursor como entrada não confiável.

GET /api/sources retorna apenas catálogo público e estado resumido; não expõe segredos, erros internos ou URLs administrativas.

GET /api/cron/ingest exige Authorization: Bearer CRON_SECRET, por compatibilidade com o scheduler proposto. Não cachear a resposta. Implementar exclusão mútua com lease no banco e expiração para evitar execuções simultâneas; liberar ao concluir. Esse endpoint não aparece na interface. A função de ingestão pode ser chamada diretamente por comando local autenticado na fase de desenvolvimento.

## Resiliência e limites iniciais

- Timeout por feed: 10 segundos; tamanho máximo descomprimido: 2 MB; até 100 itens por feed e duas requisições simultâneas. Valores propostos, calibrar no P0.
- Limitar duração total abaixo do teto da hospedagem escolhida. Adiar feeds restantes quando acabar o orçamento, registrando coleta parcial.
- Usar ETag/Last-Modified quando disponíveis. HTTP 304 conta como verificação bem-sucedida; não significa publicação nova.
- Respeitar Retry-After em 429; não fazer loops de retry. Falhas serão tentadas novamente na próxima execução.
- Falha de um item não invalida itens válidos; falha de um feed não reverte outros feeds.
- Com duas atualizações desejadas (9h e 14h), avaliar atraso pela última janela agendada já encerrada, por fonte. O limiar anterior de 30 horas fica substituído por essa regra; duração da janela depende da tolerância e do scheduler ainda a definir. O intervalo noturno normal não deve gerar alerta. Se nunca houve sucesso, informar ausência de coleta. Sinalizar no conjunto quando alguma fonte ativa perdeu a janela esperada.
- Guardar artigos por 30 dias e logs por 14 dias, com limpeza idempotente. Favoritos locais mantêm título/link e podem sobreviver à limpeza do servidor.

## Segurança e privacidade

Feeds e seus títulos são dados não confiáveis. Não renderizar HTML externo. Restringir hosts e validar também cada redirecionamento; bloquear destinos privados, loopback e metadados de nuvem, inclusive após resolução DNS. Não oferecer endpoint para buscar uma URL arbitrária enviada pelo usuário. Limitar expansão de XML e usar parser com dependências revisadas.

Banco acessível apenas pelo backend, com RLS habilitada e sem permissões de leitura/escrita para papéis públicos por padrão. Chave service-role contorna RLS: mantê-la exclusivamente no servidor e expor somente DTOs públicos. Proteger cron por segredo, limitar requisições públicas e nunca registrar tokens.

Favoritos locais são dados do navegador, não um mecanismo de privacidade do hub público. Se acesso restrito for necessário, decidir autenticação antes de hospedar. Não incluir analytics ou dados de cidadania. Prever limpar todos os dados locais pela interface.
