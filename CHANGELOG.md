# Changelog

Histórico das alterações relevantes do Notícias PT, em ordem da mais recente para a mais antiga. Este arquivo registra trabalho realizado; funcionalidades planejadas ficam no [plano de execução](docs/06-execucao.md).

## Como manter

- Atualizar este arquivo na mesma alteração que modifica o projeto.
- Registrar mudanças ainda não incluídas em uma entrega datada em **Não lançado**.
- Agrupar entradas conforme necessário em **Adicionado**, **Alterado**, **Corrigido**, **Removido** e **Segurança**; omitir grupos vazios.
- Descrever o resultado e seu impacto, sem reproduzir a lista completa de commits. Incluir links de commits ou pull requests quando úteis.
- Ao fechar uma entrega, mover suas entradas para uma seção com data `AAAA-MM-DD` e título descritivo; manter **Não lançado** no topo.
- Usar número de versão somente quando houver uma versão efetivamente definida. Uma entrega de documentação não representa uma versão funcional da aplicação.

## Não lançado

### Adicionado

- Especificação de montagem dos ambientes local, CI, previews, homologação e produção; matriz de configuração, segredos, migrações, verificações, entrega por SHA e recuperação.
- Modelo de registro de entrega e referências nos documentos de arquitetura, stack e execução. Nenhum ambiente do webapp provisionado nesta alteração.

- Primeira coleta na nuvem executada com sucesso em 06/09/2026; artifact verificado e métricas preservadas. Relatório automático ampliado com avaliação por feed.
- P0: probe de feeds oficiais, nove testes automatizados, relatório técnico local e workflow de observação limitada a 6–8/09/2026 no GitHub Actions, com artifacts por sete dias e encerramento automático.
- Descoberta oficial de RSS de A Bola e Observador; registro de HTTP 403 do Público e das pendências de uso público. A observação temporal permanece em andamento.

### Alterado

- Em 2026-09-06, frequência do MVP simplificada para uma coleta diária, com horário-alvo de 9h em Europe/Lisbon; substitui a preferência anterior por duas coletas. Documentadas janela de execução e necessidade de ajuste sazonal do cron UTC.

- Preferências registradas: atualidade nacional portuguesa, política, desporto e cultura; duas atualizações desejadas, às 9h e 14h, com fuso e tolerância pendentes.
- Corrigida a interpretação dos limites de agendamento da Vercel; dois crons diários separados ficam como possibilidade a validar.
- Incluídas sugestões de veículos e explicação prática da validação de fontes (P0), ainda não executada.

### Preparação anterior

- Branch `develop` criada a partir de `main` para os desenvolvimentos do projeto.
- Fluxo documentado de branches de tarefa para `develop`, seguido de pull request de `develop` para `main` após validação.
- Changelog com histórico inicial e convenções para acompanhar as próximas implementações.
- Link para este histórico no README e orientação de atualização para agentes.

## 2026-09-05 — Planejamento inicial

### Adicionado

- Documentação do produto, escopo do MVP, pré-requisitos e stack proposta.
- Inventário inicial de fontes e protocolo de validação de feeds.
- Propostas de arquitetura, contratos de dados, experiência de uso e critérios de aceite.
- Plano de execução, registro de decisões, riscos e pendências.
- Orientações para agentes continuarem o projeto.
- Identificação do repositório GitHub e orientações de versionamento.

### Alterado

- README inicial ampliado para servir como índice da documentação, preservando a descrição original do projeto.
- Pasta local conectada ao repositório, com documentação enviada à branch `main` e histórico inicial preservado.

Referência: [commit do planejamento inicial](https://github.com/ralves025/portugal_noticias/commit/1e7448cbc446cd060e87ee5afb947145a5b4d3d4).

Esta entrega contém apenas documentação; aplicação, banco de dados, coleta automatizada e hospedagem ainda não foram implementados.
