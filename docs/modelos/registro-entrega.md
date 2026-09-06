# Registro de entrega — modelo

Copiar para docs/entregas/AAAA-MM-DD-identificador.md ao realizar uma entrega. Este modelo não comprova que uma entrega ocorreu. Omitir credenciais e preencher somente fatos verificados.

## Identificação

| Campo | Valor |
| --- | --- |
| Data/hora e fuso | A preencher |
| Executor / responsável | A preencher |
| Ambiente | homologacao / producao |
| Objetivo e comportamento alterado | A preencher |
| PR e SHA entregue | A preencher |
| SHA testado em homologação e diferenças | A preencher |
| Execução do pipeline | Link |
| ID e URL do deploy | A preencher |
| Versão anterior / deploy para reversão | A preencher |
| Resultado | sucesso / falha / revertida |

## Configuração e banco

- Projeto-alvo conferido (IDs não secretos): a preencher.
- Última migração anterior e migrações aplicadas: a preencher ou não aplicável.
- Compatibilidade com a versão anterior: evidência ou limitação.
- Backup/exportação e restauração verificados: referência protegida e data; não colocar URLs de acesso temporário ou senhas.
- Mudanças de variáveis: nomes e finalidade, nunca valores secretos.
- Estado da ingestão e scheduler: antes/depois; horário real verificado ou pendente.

## Validação

| Verificação | Resultado e evidência |
| --- | --- |
| Checks do SHA entregue | A preencher |
| Migrações | A preencher ou não aplicável |
| Testes de fumaça | A preencher |
| Ambiente/dados corretos | A preencher |
| Limitações conhecidas | A preencher |

## Falhas e recuperação

Registrar impacto, horário, ações tomadas, estado do banco, deploy restaurado e verificações de retomada. Se não houve falha, indicar não aplicável.

## Encerramento

- CHANGELOG atualizado: referência.
- Branches sincronizadas após integração: resultado.
- Pendências com responsável: a preencher ou nenhuma.
- Próxima observação necessária: descrição e mecanismo realmente configurado; não prometer acompanhamento inexistente.
