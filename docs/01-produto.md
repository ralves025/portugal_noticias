# Produto e escopo

## Objetivo

Facilitar um hábito de leitura de 5 a 10 minutos sobre Portugal. Prioridades confirmadas pelo usuário: temas gerais nacionais portugueses, política portuguesa, desporto português e cultura. Economia e sociedade entram como parte da atualidade nacional. A dupla cidadania inspira uma evolução futura sobre serviços e vida em Portugal, sem transformar o MVP em consultoria de cidadania.

## Premissas de planejamento

- Uso pessoal, principalmente em celular, também em computador.
- Interface em português de Portugal; linguagem simples e títulos originais.
- Leitura pública sem conta; preferências armazenadas apenas no navegador.
- Preferência confirmada: duas atualizações diárias, por volta das 9h e 14h, se viáveis. Confirmar fuso de referência e tolerância de atraso antes de configurar. Baixo custo continua como proposta, sem orçamento confirmado.
- O hub agrega referências; a leitura integral ocorre no site do veículo.

## Funcionalidades do MVP

| ID | Requisito | Aceite principal |
| --- | --- | --- |
| F01 | Lista cronológica de notícias | Cada item tem título, veículo, link e data quando disponível |
| F02 | Filtrar por tema, fonte e período | Filtros combináveis; limpar restaura a listagem |
| F03 | Buscar palavras no título | Busca sem distinção de maiúsculas ou acentos sobre dados armazenados |
| F04 | Guardar para ler depois | Persistência local após recarregar; botão para remover |
| F05 | Exibir atualização e falhas | Distingue horário de coleta e publicação; informa dados desatualizados |
| F06 | Página de fontes | Lista veículos ativos, links e estado da última coleta |
| F07 | Carregar mais resultados | Paginação determinística, sem repetição na mesma consulta |

Temas iniciais: País, Política, Economia, Sociedade, Cultura, Desporto, Mundo e Outros. Na ausência de classificação confiável, usar Outros. O padrão da página inicial exclui Mundo, com opção de inclusão: um veículo português também publica notícias internacionais.

Períodos: últimas 24 horas (padrão), 7 dias e 30 dias. Isso representa uma janela móvel, não o dia civil em Lisboa. Mostrar também hora/data em Europe/Lisbon, identificada como hora de Portugal continental. Opção de fuso local em preferências.

## Fora do MVP

Login, sincronização, aplicativo nativo, notificações, newsletters, comentários, rede social, traduções, rankings por IA, resumos automáticos, reprodução integral, imagens de veículos e mecanismo de pagamento. Favoritos não garantem disponibilidade eterna do link externo.

## Critérios de sucesso propostos

- Rafael consegue consultar o panorama recente e abrir uma matéria em até três interações.
- A indisponibilidade de uma fonte não derruba a página nem remove notícias anteriores.
- Uma semana de uso permite avaliar utilidade, variedade e frequência antes de expandir.
- Meta de três veículos independentes ativos, condicionada à viabilidade de acesso; uma fonte permite apenas um piloto identificado como tal.

Não instalar analytics no MVP. A avaliação inicial pode ser feita por observação manual e feedback do usuário.
