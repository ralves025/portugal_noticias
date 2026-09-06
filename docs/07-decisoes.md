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
| D06 | Duas atualizações desejadas, aproximadamente 9h e 14h | Preferência expressa pelo usuário | Definir fuso, tolerância e validar scheduler |
| D07 | Sem IA no MVP | A utilidade inicial não depende de geração de texto | Usuário solicitar resumo com rastreabilidade |
| D08 | Retenção de 30 dias | Limita armazenamento e mantém busca recente | Favoritos ou histórico exigirem outro prazo |

## Pendências sem bloqueio da documentação

| Questão | Premissa para avançar | Momento de resolução |
| --- | --- | --- |
| Temas e abrangência | Confirmados: atualidade nacional portuguesa, política portuguesa, desporto português e cultura | Refletir nos filtros e validar cobertura no P0 |
| Variante de português | pt-PT na interface | Antes da revisão de textos |
| Horários e fuso | Duas atualizações desejadas: 9h e 14h; fuso e tolerância pendentes | Antes de configurar scheduler |
| Orçamento | Buscar franquias gratuitas, sem contratar plano | Antes de provisionar/publicar |
| Fontes favoritas | RTP como primeira candidata técnica; avaliar outras | P0 |
| Acesso público ou privado | Leitura sem login proposta; não incluir dados pessoais | Antes de hospedar |
| Sincronização entre dispositivos | Fora do MVP | Após avaliar o piloto |
| Nome e domínio | Notícias PT provisório; domínio próprio opcional | Publicação |

## Riscos e respostas

- Feed removido ou instável: adaptador isolado, estado por fonte, último resultado preservado e troca de candidata.
- Permissões incertas: integração pendente até registrar condições; omitir descrições por padrão.
- Cobertura concentrada em um veículo: identificar piloto e buscar fontes independentes antes de chamar o conjunto de panorama plural.
- Coleta duas vezes ao dia pode perder itens que saem rapidamente do feed: medir janela de cobertura no P0; não prometer arquivo completo; rever periodicidade se necessário.
- Atraso do cron: exibir hora real; aviso quando a janela esperada terminar sem verificação bem-sucedida; tolerância ainda a definir.
- Quotas, pausas ou alteração de preços: rever documentação do provedor antes de contratar e registrar configuração real.
- Categorias inconsistentes: mapear por fonte, manter Outros e não classificar por IA silenciosamente.
- Links quebrados ou com assinatura: manter atribuição e não prometer acesso integral.
- Favoritos apagados pelo navegador: explicar armazenamento local e oferecer sincronização somente em evolução futura.

## Evoluções possíveis após o piloto

Maior frequência; seleção de fontes favoritas; fontes regionais; exportar/importar favoritos; sincronização com login; instalação como PWA; conteúdo de serviços públicos e cidadania em área separada; resumo diário com links e revisão de qualidade, se solicitado. Cada evolução requer atualizar escopo e critérios de aceite.

## Estado desta entrega

Documentação criada. Nenhum código da aplicação, teste operacional de RSS, banco, conta, agendamento ou deploy foi executado. Pesquisa confirmou a documentação RSS da RTP e restrições do scheduler proposto; os demais veículos continuam candidatos. A próxima tarefa recomendada é P0, seguida da fundação com fixtures.
