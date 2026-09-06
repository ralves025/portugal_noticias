# Decisões, pendências e riscos

Data-base: 05/09/2026. As decisões abaixo orientam a implementação posterior. Temas e frequência desejada foram informados pelo usuário; os demais detalhes continuam propostas salvo indicação explícita.

## Registro de decisões

| ID | Proposta | Motivo | Reavaliar quando |
| --- | --- | --- | --- |
| D01 | Hub de referências com leitura na origem | Escopo pequeno e vínculo claro com o veículo | Houver acordo para conteúdo adicional |
| D02 | RSS como primeira integração | Evita dependência inicial de scraping e APIs pagas | Fontes suficientes não forem viáveis |
| D03 | Next.js full stack | Uma base para interface e endpoints | Requisitos de hospedagem exigirem outra solução |
| D04 | PostgreSQL gerenciado no Supabase | Dados persistentes entre execuções serverless | Custos ou operação justificarem alternativa |
| D05 | Sem conta; favoritos locais | Reduz esforço e tratamento de dados pessoais | Sincronização ou acesso privado forem necessários |
| D06 | Uma coleta diária no MVP, horário-alvo 9h em Europe/Lisbon | Decisão do usuário para simplificar a primeira versão | Validar cobertura no P0 e operação do scheduler |
| D07 | Sem IA no MVP | A utilidade inicial não depende de geração de texto | Usuário solicitar resumo com rastreabilidade |
| D08 | Retenção de 30 dias | Limita armazenamento e mantém busca recente | Favoritos ou histórico exigirem outro prazo |

## Pendências sem bloqueio da documentação

| Questão | Premissa para avançar | Momento de resolução |
| --- | --- | --- |
| Temas e abrangência | Confirmados: atualidade nacional portuguesa, política portuguesa, desporto português e cultura | Refletir nos filtros e validar cobertura no P0 |
| Variante de português | pt-PT na interface | Antes da revisão de textos |
| Horário e fuso | Confirmados: uma vez ao dia, 9h de Portugal continental (Europe/Lisbon); janela técnica Hobby de início até 9h59 | Validar ajuste sazonal antes de configurar scheduler |
| Orçamento | Buscar franquias gratuitas, sem contratar plano | Antes de provisionar/publicar |
| Fontes favoritas | RTP como primeira candidata técnica; avaliar outras | P0 |
| Acesso público ou privado | Leitura sem login proposta; não incluir dados pessoais | Antes de hospedar |
| Sincronização entre dispositivos | Fora do MVP | Após avaliar o piloto |
| Nome e domínio | Notícias PT provisório; domínio próprio opcional | Publicação |

## Riscos e respostas

- Feed removido ou instável: adaptador isolado, estado por fonte, último resultado preservado e troca de candidata.
- Permissões incertas: integração pendente até registrar condições; omitir descrições por padrão.
- Cobertura concentrada em um veículo: identificar piloto e buscar fontes independentes antes de chamar o conjunto de panorama plural.
- Coleta uma vez ao dia pode perder itens que saem rapidamente do feed: medir janela de cobertura no P0; não prometer arquivo completo; rever periodicidade se necessário.
- Atraso do cron: exibir hora real; aviso após a janela matinal e a duração máxima de execução sem verificação bem-sucedida.
- Quotas, pausas ou alteração de preços: rever documentação do provedor antes de contratar e registrar configuração real.
- Categorias inconsistentes: mapear por fonte, manter Outros e não classificar por IA silenciosamente.
- Links quebrados ou com assinatura: manter atribuição e não prometer acesso integral.
- Favoritos apagados pelo navegador: explicar armazenamento local e oferecer sincronização somente em evolução futura.

## Evoluções possíveis após o piloto

Maior frequência; seleção de fontes favoritas; fontes regionais; exportar/importar favoritos; sincronização com login; instalação como PWA; conteúdo de serviços públicos e cidadania em área separada; resumo diário com links e revisão de qualidade, se solicitado. Cada evolução requer atualizar escopo e critérios de aceite.

## Estado desta entrega

P0 em execução: scripts e testes de diagnóstico criados; primeira amostra local realizada em 06/09/2026. Workflow integrado por PR; primeira execução manual do Actions validada e três manhãs agendadas. Ver [relatório P0](p0/README.md). Aplicação, banco e deploy do webapp não implementados. Aprovação pública das fontes e comparação das manhãs continuam pendentes.
