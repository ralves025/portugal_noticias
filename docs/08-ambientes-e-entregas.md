# Ambientes e entregas

Data: 06/09/2026. Status: especificação para montagem futura. Nenhum ambiente do webapp foi provisionado por esta entrega. O GitHub Actions da P0 já existe e é independente deste plano.

Este documento define a proposta de montagem, configuração e entrega. Complementa [pré-requisitos](02-pre-requisitos-stack.md), [arquitetura](04-arquitetura.md) e [plano de execução](06-execucao.md). O fluxo Git `develop` → PR → `main` foi definido pelo usuário; escolhas de infraestrutura abaixo são recomendações a validar na implementação e nas cotas das contas.

## 1. Topologia proposta

| Ambiente | Origem do código | Execução e dados | Coleta |
| --- | --- | --- | --- |
| Local | develop ou branch de tarefa | Next.js local; fixtures por padrão; Supabase local quando necessário | Desligada por padrão; teste pontual explícito |
| CI | SHA do PR ou commit verificado | Runner temporário; fixtures e banco descartável para testes de migração | Sem feeds reais nos testes determinísticos |
| Prévia de tarefa | Branch criada de develop | Deploy Preview opcional; fixtures; sem banco compartilhado | Desligada |
| Homologação | SHA selecionado de develop | Deploy Preview da Vercel; projeto Supabase exclusivo de homologação | Manual e protegida; somente fontes aptas ao uso desse ambiente |
| Produção | SHA revisado integrado na main | Deploy Production; projeto Supabase exclusivo de produção | Diária, horário-alvo 9h Europe/Lisbon, após liberação |
| P0 temporária | Workflow já integrado na main | Runner do Actions; métricas e artifacts; sem banco do app | Janela própria documentada no relatório P0 |

Homologação é o ambiente para testar a aplicação integrada antes de disponibilizá-la para uso diário. Uma prévia de tarefa serve para avaliar uma mudança isolada. Não compartilham a mesma política de acesso a dados.

Proposta mínima: um projeto Vercel para o app, usando seus ambientes Preview e Production; dois projetos Supabase independentes quando a integração remota for necessária. Não depender de ambientes personalizados ou branches gerenciadas de banco no MVP. Se as cotas não comportarem os projetos, manter testes locais e fixtures até resolver o orçamento; não usar produção como banco de teste.

A Vercel distingue Preview e Production, inclusive na configuração de variáveis. O conceito de homologação adotado aqui utiliza Preview; não é um novo ambiente pago presumido. Referências: [ambientes Vercel](https://vercel.com/docs/deployments/environments) e [variáveis por ambiente](https://vercel.com/docs/environment-variables/manage-across-environments).

## 2. Inventário a preencher durante a montagem

| Item | Valor/status atual | Responsabilidade proposta |
| --- | --- | --- |
| Repositório | ralves025/portugal_noticias; branches develop e main | Rafael |
| Projeto Vercel / organização | Não provisionado | Rafael ou agente autorizado |
| URL estável da homologação | Não definida; domínio próprio dispensável | Executor da montagem |
| URL de produção | Não definida; domínio próprio opcional | Rafael |
| Supabase homologação / project ref / região | Não provisionado | Executor da montagem |
| Supabase produção / project ref / região | Não provisionado | Executor da montagem |
| Responsável pelas entregas e reversão | Rafael; agentes podem executar tarefas autorizadas | Rafael |
| Limite mensal de gasto | Não definido; buscar franquias existentes | Rafael antes de contratar |
| Método de acesso à homologação | Definir antes de usar conteúdo restrito; fixtures podem ser públicas | Executor da montagem |
| Responsável pelo ajuste sazonal do cron | Rafael ou agente designado; ainda não operacional | Antes de ativar coleta |

Registrar IDs não secretos, região, URLs, cotas verificadas e data de verificação. Valores de tokens e senhas não entram neste inventário. Escolher regiões compatíveis para aplicação e banco depois de conferir disponibilidade e latência; não presumir uma região contratada.

## 3. Sequência de montagem

### Etapa A — base local e CI (P1)

1. Fixar Node LTS, npm e versões compatíveis; versionar lockfile e convenção de versão do runtime.
2. Criar scripts de instalação, execução, lint, tipos, testes e build. Documentar os comandos efetivos no README quando existirem; eles ainda não estão implementados.
3. Criar .env.example com placeholders e modos descritos abaixo; confirmar arquivos locais de configuração ignorados pelo Git.
4. Rodar interface com fixtures claramente fictícias, sem credenciais e sem rede para fontes.
5. Criar CI de aplicação separado do workflow P0. Testar instalações reproduzíveis e build com fixtures.
6. Ao iniciar migrações, usar Supabase local com Docker, ou banco descartável equivalente para CI. Não redefinir/resetar um banco remoto compartilhado durante testes.

Aceite: outro agente consegue preparar o ambiente pelos comandos registrados; testes determinísticos não precisam de segredos e a aplicação informa quando usa fixtures.

### Etapa B — homologação integrada (P2–P4)

1. Conferir cotas e criar apenas o projeto Supabase de homologação quando necessário.
2. Aplicar migrações versionadas e seeds sintéticos; registrar o project ref e a última migração.
3. Criar o projeto Vercel sem habilitar uma segunda rota automática de deploy por Git. Nesta proposta o pipeline do Actions será o único executor das entregas.
4. Configurar as variáveis Preview de develop para homologação. Prévias de outras branches ficam em modo fixtures e não recebem credenciais de banco.
5. Configurar o ambiente GitHub `homologacao`, permitindo entregas somente da develop, com credenciais específicas de implantação e migração.
6. Executar entrega controlada do SHA escolhido: validações, build para o destino, migrações compatíveis e deploy Preview; registrar URL e resultado dos testes de fumaça.
7. Validar filtros, favoritos, fontes indisponíveis, banco correto e ingestão manual protegida. Sem fonte aprovada para esse uso, usar seeds sintéticos; não interpretar sucesso técnico P0 como liberação pública.

Aceite: homologação isolada de produção, sem coleta agendada; URL e SHA rastreáveis; alterações no banco não afetam outros ambientes.

### Etapa C — produção (P5–P6)

1. Resolver acesso público/restrito e permissões de uso das fontes; definir URL, cotas e responsáveis.
2. Criar o projeto Supabase de produção separado e o ambiente GitHub `producao`, restrito à main.
3. Configurar exclusivamente variáveis Production; aplicar o schema, sem seeds fictícios.
4. Verificar backup/exportação e restauração compatíveis com o plano antes de alterações com dados existentes.
5. Publicar pelo processo de entrega abaixo; iniciar com ingestão desativada.
6. Após verificar ambiente, schema e fonte apta, ativar ingestão, executar coleta inicial protegida e conferir os dados.
7. Ativar apenas o agendamento definitivo escolhido; verificar primeira execução real e seu horário, sem usar a coleta P0 como substituto.

Aceite: produção aponta somente para seu banco; nenhum conteúdo fictício; segredos ausentes no navegador; fluxo principal funcional e procedimento de reversão registrado.

## 4. Variáveis, modos e segredos

As variáveis novas são contratos propostos para P1/P2. Nenhuma foi cadastrada em serviços nesta entrega.

| Variável | Finalidade | Local / tarefa | Homologação | Produção |
| --- | --- | --- | --- | --- |
| APP_ENV | Validação explícita do ambiente no servidor | local / preview | homologacao | producao |
| DATA_MODE | Escolher fixtures ou banco | fixtures; database só em integração local | database | database obrigatório |
| INGESTION_ENABLED | Habilitar serviço de coleta | false por padrão | false; ativação manual controlada | false inicialmente; true após liberação |
| SUPABASE_URL | Endpoint do banco | Local se usado; ausente em preview de tarefa | Projeto homologação | Projeto produção |
| SUPABASE_SERVICE_ROLE_KEY | Acesso exclusivo do backend | Somente banco local quando usado | Chave homologação | Chave produção |
| CRON_SECRET | Autorizar endpoint de coleta | Segredo local para teste | Segredo exclusivo | Segredo exclusivo |
| APP_BASE_URL | URL canônica | URL local/da prévia | URL homologação | URL produção |

Regras de implementação: produção rejeita DATA_MODE=fixtures; fixtures não instanciam clientes de banco; flags e credenciais nunca recebem prefixo público. Ausência de configuração necessária causa erro claro, sem fallback silencioso para outro banco. Validar o project ref esperado no pipeline e na inicialização quando houver banco. INGESTION_ENABLED=false bloqueia coleta mesmo com segredo correto; true não cria agendamento por si só.

A chave service-role possui acesso amplo: fica apenas no backend, nunca em fixtures, browser, logs ou artifacts. Não usar essa chave para migrações de schema: o executor de migração recebe sua credencial específica, limitada ao projeto-alvo.

Segredos do runtime ficam na Vercel, separados por escopo. Segredos de entrega ficam nos respectivos GitHub Environments: autenticação da Vercel e da CLI/banco Supabase escolhida. IDs de projeto são configuração, não substituem autenticação. Evitar duplicar chaves de runtime no GitHub; se o build precisar de configuração, carregá-la pelo mecanismo oficial do ambiente e não arquivar arquivos .env ou .vercel. Referência: [vercel pull](https://vercel.com/docs/cli/pull).

Prévias de tarefas externas e CI de pull requests não recebem secrets. Não executar código de PR não revisado em job com credenciais de entrega. Usar permissões mínimas do GITHUB_TOKEN por job e Actions fixadas por SHA, como na P0.

Favoritos em localStorage são separados por origem: dados de uma URL de preview não migram automaticamente para homologação ou produção. Não oferecer migração implícita desses favoritos.

## 5. Fluxo Git e entrega

Fluxo de código: branch de tarefa → PR para develop → homologação → PR develop para main → entrega de produção. O usuário também permite trabalho direto na develop; main sempre recebe por PR. Correções urgentes seguem o mesmo percurso com escopo pequeno.

No MVP, propõe-se disparo manual de entrega por workflow_dispatch, com SHA explícito. Merge é integração de código; não publica automaticamente o app. Assim a implantação não compete com migrações executadas em paralelo. Não habilitar simultaneamente deploy automático da integração Git da Vercel. Se a estratégia mudar, registrar uma nova decisão e manter um único caminho de publicação.

| Pipeline futuro | Quando | Pode receber credenciais? | Resultado |
| --- | --- | --- | --- |
| ci-app | PR e alterações relevantes em develop/main | Não; banco de CI descartável | Verificações do código e schema |
| preview-tarefa | Pedido explícito para SHA revisado | Só credencial de deploy em etapa confiável; sem banco | Prévia opcional com fixtures |
| entregar-homologacao | Disparo na develop, SHA informado | Ambiente homologacao | Migração e deploy Preview |
| entregar-producao | Disparo na main, SHA informado | Ambiente producao | Migração e deploy Production |

Os nomes são planejados, não workflows já existentes. Configurar proteções de branches e environments ao implementá-los: PR obrigatório na main, verificações aprovadas, bloqueio de force push e restrição da branch de origem da entrega. Registrar se há revisor disponível; não exigir uma segunda pessoa fictícia em projeto individual. Uma tarefa de publicação já autorizada não exige uma nova aprovação conversacional; regras reais do GitHub continuam aplicáveis. Recursos de proteção dependem da conta/plano e devem ser conferidos. Referência: [GitHub Environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).

### Ordem de uma entrega

1. Selecionar o SHA atual da branch correta e conferir que é o commit revisado, com checks aprovados. Se a branch avançar antes do início, interromper e escolher conscientemente o SHA; não trocar por latest durante a execução.
2. Obter configuração do destino e validar IDs do projeto Vercel e banco. Construir/testar com dependências fixadas, sem consultar feeds no build.
3. Serializar entregas por ambiente: uma execução por vez, sem cancelar migração em andamento. Bloquear caminho de migração fora desse controle.
4. Comparar histórico de migrações; aplicar somente as pendentes, compatíveis com a versão atualmente publicada. Em caso de falha, parar antes de publicar.
5. Publicar exatamente o código selecionado no destino correspondente e capturar ID/URL do deploy. Build de Preview não deve ser promovido cegamente com variáveis de homologação; reconstruir para Production com o mesmo código revisado e configuração própria.
6. Verificar a versão entregue, consulta ao banco correto e fluxos de leitura; registrar resultados e liberar a URL de uso.
7. Atualizar o [registro da entrega](modelos/registro-entrega.md) e o CHANGELOG com resultado real. Registrar também falhas e eventual reversão.

Após merge develop→main, um merge commit pode mudar o SHA. Conferir diferenças, repetir CI no SHA da main e usar esse SHA para produção; não alegar que é literalmente o mesmo commit da homologação. Sincronizar develop com o merge antes do próximo ciclo.

A CLI da Vercel permite deploy de projetos e saída com URL; a configuração dos comandos efetivos será fixada/testada na implementação. Referência: [vercel deploy](https://vercel.com/docs/cli/deploy).

## 6. Migrações e dados

Versionar migrações SQL em supabase/migrations e nunca reescrever uma migração aplicada em ambiente compartilhado. Testar tanto banco vazio quanto atualização desde o schema da última entrega. Configurações RLS, índices e permissões fazem parte das migrações; não depender de alterações manuais esquecidas no painel.

Usar mudanças aditivas primeiro: adicionar coluna/tabela compatível, publicar código que a utiliza e remover a estrutura antiga apenas em entrega posterior, após abandonar a necessidade de rollback. Migrações não transacionais ou backfills longos exigem plano específico e checkpoint. Não rodar migrações no build da Vercel ou em requisições públicas.

Seeds são sintéticos e idempotentes em desenvolvimento/homologação; nunca copiar dados pessoais, chaves ou o banco inteiro de produção para previews. Catalogar fontes separadamente da ativação: criar a configuração não autoriza coletar nem publicar.

A Supabase documenta migrações versionadas e projetos separados de staging/produção. Esta proposta usa esses conceitos sem adotar automaticamente todos os passos do exemplo oficial. Referências: [gerenciamento de ambientes](https://supabase.com/docs/guides/deployment/managing-environments) e [migrações](https://supabase.com/docs/guides/deployment/database-migrations).

## 7. Verificações exigidas por tipo de alteração

| Alteração | Evidência mínima |
| --- | --- |
| Apenas Markdown | Links locais, consistência e diff; não executar coleta ou deploy |
| Interface/contratos | Lint, tipos, build e testes relevantes; revisão visual se layout mudou |
| Banco | Migração em banco vazio e desde versão anterior; permissões e RLS |
| Coleta | Fixtures de falhas/deduplicação; verificação externa separada quando necessária |
| Entrega/configuração | IDs e ambiente-alvo, SHA, configuração válida e teste de fumaça após deploy |

Configurar um check agregador sempre presente para PRs, distinguindo verificações dispensadas por escopo de falhas. Não exigir um job que nunca dispara em mudanças de documentação e fica pendente para sempre. Durante a fase atual só existem os testes P0, não uma CI completa do app.

Teste de fumaça futuro: página inicial, API de leitura, filtro e link de origem; guardar/remover notícia em navegador; confirmar ausência de fixtures em produção e rejeição de coleta sem autorização. Não registrar valor de credenciais nos resultados. Metadados de versão podem expor apenas SHA e ambiente, sem segredos ou IDs internos desnecessários.

## 8. Falha, reversão e recuperação

Se a migração falhar, manter a versão do app publicada e interromper a entrega. Inspecionar o estado real do schema antes de repetir; não presumir que tudo foi revertido. Se a migração passar e o deploy falhar, manter mudanças aditivas compatíveis e corrigir/reexecutar a implantação.

Se a nova aplicação falhar, retornar ao deploy anterior apenas se compatível com o schema atual. Reverter código não reverte banco, configurações, cron nem segredos. Uma correção de configuração pode exigir novo build/deploy. Se houver risco de gravação incorreta, desativar ingestão e cancelar o disparo correspondente antes de recuperar.

Antes de migração com dados existentes, registrar último backup/exportação, local protegido, procedimento de restauração e evidência de teste em ambiente isolado. Disponibilidade e retenção de backup dependem do plano; não afirmar que recuperação está garantida sem verificar. Não usar reset remoto nem importação sobre produção como tentativa de correção improvisada.

Rafael é o responsável proposto por decidir retomada; o executor registra horário da falha, impacto, versão/schema anterior e atual e ação tomada no registro da entrega. A retomada exige nova verificação do fluxo principal e da coleta.

## 9. Relação com a P0 e próximos passos

A P0 coleta métricas em artifacts, não abastece banco de homologação/produção. Seu workflow temporário não vira automaticamente o scheduler do app. O atraso observado na primeira execução agendada é evidência sobre aquela execução do Actions, não uma medição da pontualidade da Vercel.

Podem avançar sem concluir P0: montagem local com fixtures, contratos, CI determinística e estrutura de migrações. Dependem dos resultados/decisões restantes: fontes ativas, campos exibidos, coleta real pública e frequência final operacional.

Próxima implementação: P1 cria base local e CI; P2 cria banco/ingestão; P4 integra homologação; P6 prepara produção. Esta entrega documenta o procedimento; não instala ferramentas, cria contas, cadastra segredos, altera proteções, configura novos workflows ou publica o app.
