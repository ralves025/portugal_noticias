# Plano de execução para tarefas futuras

Status: P0 em execução desde 06/09/2026; primeira amostra local concluída e observação temporal agendada no Actions. P1–P6 não iniciados. Ver [relatório P0](p0/README.md).

## Pacotes e dependências

| Pacote | Responsabilidade sugerida | Entradas | Entregáveis e aceite |
| --- | --- | --- | --- |
| P0 — Fontes | Agente de pesquisa e integração | docs/03-fontes.md | Registro verificável de pelo menos uma fonte utilizável e avaliação das demais candidatas; não ativar fontes pendentes |
| P1 — Fundação | Agente de estrutura | Produto, stack, contratos | Next.js inicial, versões fixadas, lockfile, scripts, .env.example e fixtures identificadas; build e checagem de tipos passam |
| P2 — Banco e coleta | Agente de backend | P0 + P1 + arquitetura | Migrações, adaptadores, upsert, logs, endpoint protegido, lease e limpeza; testes de falha e idempotência passam |
| P3 — Interface | Agente de frontend | P1 + contratos + experiência | Telas e estados completos com fixtures; filtros, links e favoritos funcionam em celular e teclado |
| P4 — Integração | Agente integrador | P2 + P3 | API real conectada; filtros, paginação e estados de coleta preservam contrato; fixtures não aparecem em produção |
| P5 — Verificação | Agente de qualidade | P4 | Fluxos automatizados essenciais, revisão visual e relatório com limitações |
| P6 — Hospedagem piloto | Agente de entrega | P5 + ambiente de destino definido | Deploy, cron, primeira coleta e verificação no dia seguinte; documentar rollback e custos aplicáveis |

P0 e P1 não dependem entre si. P3 pode usar fixtures enquanto P2 é desenvolvido, desde que contratos estejam estabilizados. Essa divisão serve para atribuições futuras; nenhum agente adicional foi acionado nesta etapa.

## Cenários de validação

### Unidade e integração

- RSS válido e Atom válido; XML quebrado; título/link ausente; categoria desconhecida; data ausente/inválida/futura.
- URL relativa, parâmetro funcional preservado, tracking removido e link não HTTP rejeitado.
- Mesma URL em dois feeds do mesmo veículo gera um artigo; mesmo assunto em veículos diferentes permanece separado.
- GUID estável com título atualizado não cria duplicata; conflito entre GUID e URL não mescla registros silenciosamente.
- Repetir a coleta não aumenta o número de artigos existentes.
- HTTP 304 preserva artigos e atualiza verificação; 429, timeout e feed inválido não apagam dados.
- Cron sem segredo é rejeitado; duas execuções concorrentes não coletam simultaneamente.
- Destino privado e redirecionamento não permitido são bloqueados; payload excessivo é interrompido.
- Migrações aplicam em banco vazio; usuário público não consegue escrever ou ler diretamente tabelas protegidas.

### Fluxos completos

- Abrir página, combinar filtros, pesquisar com/sem acento, carregar mais e abrir veículo correto.
- Trocar filtros reinicia cursor; resultados mantêm ordenação estável.
- Guardar, recarregar e remover; limpar dados locais; armazenamento indisponível não bloqueia leitura.
- Simular falha parcial, dados antigos, lista vazia e falha da API.
- Conferir data perto da meia-noite e transição de horário de verão de Lisboa.
- Validar teclado, foco, zoom e layouts de celular/desktop.

Testes determinísticos usam fixtures locais. Smoke test real das fontes é separado e registra a data, pois disponibilidade externa pode mudar.

## Critério de pronto do MVP

Funcionalidades F01–F07 atendidas; pelo menos uma fonte operacional identificada como piloto se ainda não houver diversidade; nenhuma fonte não validada ativa; nenhuma credencial no cliente; fontes atribuídas; falhas tratadas; build, tipos, lint e testes relevantes aprovados. Registrar o que foi realmente executado, sem afirmar que ausência de erro na interface prova ingestão correta.

## Checklist operacional futuro

1. Definir acesso público ou restrito e confirmar condições/cotas dos serviços escolhidos.
2. Criar ambiente, aplicar migrações, cadastrar apenas fontes validadas e configurar segredos.
3. Executar primeira ingestão protegida e verificar artigos e logs.
4. Publicar preview e validar fluxos; promover ao ambiente de uso quando a tarefa de publicação estiver autorizada.
5. Configurar uma coleta diária com horário-alvo de 9h em Europe/Lisbon; validar a janela de execução, a conversão para UTC e o procedimento de ajuste sazonal antes de publicar. Conferir uma execução automática na manhã seguinte.
6. Documentar exportação/restauração do banco disponível no plano, retenção e procedimento para desativar uma fonte.
7. Para rollback, restaurar a versão anterior da aplicação compatível com o schema; não presumir reversão automática de migrações nem cron.

## Modelo de passagem entre agentes

Registrar: pacote e objetivo; arquivos alterados; contratos afetados; comandos/verificações executados e resultados; limitações conhecidas; decisões novas; próximo pacote liberado. Manter README e decisões consistentes com a implementação final.
