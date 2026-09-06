# Notícias PT — projeto inicial

Status: P0 em execução; aplicação ainda não implementada. Atualizado em 06/09/2026.

Mini hub pessoal para acompanhar Portugal diariamente, pensado para Rafael, cidadão brasileiro e português. A proposta permite consultar notícias em poucos minutos e abrir as matérias nos veículos de origem.

## Repositório do projeto

Repositório definido pelo usuário: [ralves025/portugal_noticias](https://github.com/ralves025/portugal_noticias).

Este é o destino de versionamento da documentação e da futura aplicação. A pasta local está conectada ao remoto origin, e a branch principal verificada é main. O histórico preserva o commit inicial do GitHub.

Descrição original do repositório: “webapp para reunir uma seleção curada diária de notícias de Portugal”. No MVP, a seleção será feita por fontes e filtros, sem curadoria editorial manual diária prevista.

Fluxo definido para o projeto: desenvolver em `develop` antes de integrar à branch principal `main`. Para tarefas isoladas, criar branches a partir de `develop` e abrir pull requests para `develop`. Após validar o conjunto de alterações, abrir um pull request de `develop` para `main`. Preservar o histórico e as alterações locais ao sincronizar.

## Documentos e ordem de leitura

1. [Produto e escopo](docs/01-produto.md): público, funcionalidades e limites do MVP.
2. [Pré-requisitos e ferramentas](docs/02-pre-requisitos-stack.md): ambiente, bibliotecas, serviços e custos.
3. [Fontes de notícias](docs/03-fontes.md): evidências, candidatas e processo de validação.
4. [Arquitetura e dados](docs/04-arquitetura.md): coleta, armazenamento, contratos e segurança.
5. [Experiência de uso](docs/05-experiencia.md): telas, estados e regras de apresentação.
6. [Plano de execução](docs/06-execucao.md): pacotes de trabalho e critérios de aceite.
7. [Decisões e pendências](docs/07-decisoes.md): premissas, riscos e próximos passos.
8. [Ambientes e entregas](docs/08-ambientes-e-entregas.md): montagem local, homologação, produção, configuração e fluxo de publicação.
9. [Orientações para agentes](AGENTS.md): como continuar este projeto.
10. [Histórico de alterações](CHANGELOG.md): entregas realizadas e mudanças ainda não lançadas.

Modelo operacional: [registro de entrega](docs/modelos/registro-entrega.md).

## Proposta resumida

- Webapp responsivo, sem login no MVP, com notícias organizadas por data, tema e veículo.
- Next.js + React + TypeScript; PostgreSQL no Supabase; coleta RSS no servidor.
- Uma atualização diária no MVP, com horário-alvo de 9h de Portugal continental (Europe/Lisbon); considerar a janela de execução do scheduler.
- Favoritos e preferências locais, sem sincronização entre dispositivos.
- Sem reprodução de matérias completas, resumos gerados por IA ou coleta por scraping no MVP.

Temas, horário-alvo e fluxo Git foram definidos pelo usuário; a infraestrutura do webapp continua uma proposta. Scripts e workflow de diagnóstico da P0 já foram executados. Ambientes, banco e aplicação do hub ainda não foram montados; consultar o relatório P0 para resultados e limitações.

## Próxima ação recomendada

Acompanhar a [execução da P0 e seus resultados](docs/p0/README.md). Em seguida, criar a base da aplicação com dados fictícios claramente identificados. A primeira versão utilizável pode operar com uma fonte validada; a meta de diversidade é pelo menos três veículos independentes.
