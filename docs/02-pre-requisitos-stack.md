# Pré-requisitos e ferramentas

## Ambiente futuro

- Git, editor e terminal PowerShell ou equivalente.
- Node.js em uma versão LTS ainda suportada e compatível com Next.js; fixar a versão exata na implementação. A documentação consultada informa mínimo 20.9, o que não implica recomendar essa versão antiga.
- npm como gerenciador único, com package-lock.json versionado.
- Navegadores atuais para desenvolvimento e verificação em celular.
- Conta Supabase e projeto de desenvolvimento ao integrar persistência; conta Vercel apenas na etapa de hospedagem. Repositório remoto recomendado para CI e histórico.
- Docker opcional para Supabase local; dispensável usando projeto remoto separado de produção.

Referência: [instalação do Next.js](https://nextjs.org/docs/app/getting-started/installation), consultada em 05/09/2026.

## Stack recomendada

| Tecnologia | Finalidade | Decisão |
| --- | --- | --- |
| Next.js, App Router + React | Interface e endpoints em um projeto | Adotar versão estável compatível na implementação |
| TypeScript | Contratos da aplicação e normalização | Modo strict |
| Tailwind CSS | Estilos responsivos | Evitar biblioteca visual adicional inicialmente |
| rss-parser | Interpretar RSS/Atom no servidor | Fazer fetch controlado e depois parseString |
| Zod | Validar parâmetros e dados normalizados | Validar todas as fronteiras externas |
| Supabase PostgreSQL | Persistência compartilhada das notícias | Migrações SQL versionadas |
| @supabase/supabase-js | Acesso ao banco pelo servidor | Credencial restrita ao backend |
| Vitest | Testes de normalização e ingestão | Fixtures locais determinísticas |
| Testing Library | Interações dos componentes | Cobrir filtros e favoritos |
| Playwright | Fluxos completos e responsividade | Testes sem depender de feeds reais |
| ESLint + TypeScript | Qualidade estática | Rodar separadamente do build |
| Vercel | Hospedar Next.js e disparar coleta | Proposta, ainda sem provisionamento |

Usar fetch e Intl nativos para HTTP e datas. Não introduzir ORM, Redis, fila, biblioteca de estado global ou serviço de IA sem necessidade demonstrada. Verificar manutenção, compatibilidade e alertas de segurança antes de fixar versões das bibliotecas.

Referências primárias: [rss-parser](https://github.com/rbren/rss-parser), [Supabase Database](https://supabase.com/docs/guides/database/overview). As demais bibliotecas são escolhas propostas, não um conjunto de versões já testado.

## Configuração prevista

O agente de implementação deverá criar .env.example apenas com placeholders:

| Variável | Local | Uso |
| --- | --- | --- |
| SUPABASE_URL | Servidor | Endereço do projeto |
| SUPABASE_SERVICE_ROLE_KEY | Segredo no servidor | Ingestão e consultas internas; nunca enviar ao cliente |
| CRON_SECRET | Segredo no servidor | Autorizar a chamada agendada |
| APP_BASE_URL | Servidor | URL canônica do ambiente |

Não é necessário fornecer credenciais para o protótipo com fixtures. Separar projetos ou ambientes de teste e produção. Não criar uma chave pública de banco se o navegador só consultar o backend.

## Hospedagem, frequência e custos

A preferência do usuário é receber duas atualizações por dia, por volta das 9h e 14h. Ainda é necessário confirmar se são horários de Brasília ou de Portugal continental e qual atraso é aceitável.

Correção da interpretação inicial: o plano Hobby da Vercel limita cada cron a uma execução diária, mas permite vários crons por projeto. A proposta a validar é usar dois agendamentos diários separados, compartilhando a mesma lógica de ingestão; não uma única expressão que rode duas vezes no dia. Isso não foi configurado nem testado. A documentação informa que uma execução marcada para uma hora pode ocorrer até o fim daquela hora, portanto não garante atualização pronta exatamente às 9h ou 14h. Fonte: [limites de cron da Vercel](https://vercel.com/docs/cron-jobs/usage-and-pricing), consultada em 05/09/2026.

Se a tolerância exigir maior precisão, avaliar outro scheduler ou plano compatível antes de contratar. A hospedagem da aplicação e o serviço que dispara a coleta podem ser escolhidos separadamente.

O cron da Vercel usa UTC. Converter os horários somente depois da confirmação do fuso. Se a referência for Europe/Lisbon, considerar as mudanças sazonais de horário; não fixar um offset anual. A interface continuará informando a hora real de atualização.

Objetivo de custo: começar dentro das franquias disponíveis, sem compromisso de custo zero. Conferir preços, quotas, pausa por inatividade, retenção e limites de execução na contratação. Custos potenciais: hospedagem, banco, domínio opcional e tráfego. Nenhuma assinatura paga está autorizada ou provisionada neste planejamento.
