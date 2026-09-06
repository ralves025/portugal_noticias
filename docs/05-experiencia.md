# Experiência de uso

## Direção visual

Interface de leitura tranquila, responsiva e sem poluição visual. Fundo claro, texto de alto contraste e uma cor de destaque discreta. Tipografia de sistema para reduzir carregamento. Evitar copiar a identidade visual de jornais ou usar símbolos que sugiram vínculo oficial com o Estado português.

## Telas

| Rota | Conteúdo |
| --- | --- |
| / | Notícias recentes, pesquisa, filtros e atualização |
| /guardadas | Favoritos deste navegador, com opção de remover |
| /fontes | Veículos ativos e disponibilidade resumida |
| /preferencias | Fuso, período padrão e limpeza dos dados locais |

Na tela inicial: nome provisório Notícias PT, indicação de última verificação, filtros, lista de notícias e botão Carregar mais. Em celular, filtros recolhíveis com indicação dos ativos; em desktop, faixa horizontal. Filtros ficam na URL para preservar navegação e compartilhamento.

## Cartão de notícia

Ordem: tema e veículo; título clicável; data/hora; descrição quando permitida; Guardar e Ler na fonte. Sem imagem no MVP. Data relativa deve permitir consultar a data absoluta. Se published_at faltar, escrever “Data de publicação não informada” e informar a primeira coleta separadamente.

Ler na fonte abre nova aba com indicação acessível e rel="noopener noreferrer". Não prometer que o conteúdo será gratuito. Guardar confirma a ação sem interromper a leitura; o botão passa a Remover das guardadas.

## Estados obrigatórios

- Carregamento: estrutura leve sem deslocar a página.
- Nenhum resultado: explicar filtros e oferecer limpar ou ampliar período.
- Primeiro acesso sem coleta: explicar que ainda não há notícias disponíveis.
- Falha parcial: conservar lista e informar fontes temporariamente indisponíveis.
- Dados antigos: aviso com horário real da última verificação bem-sucedida.
- Falha total da API: mensagem e Tentar novamente; não confundir com lista vazia.
- Favoritos vazios: instrução curta para guardar uma notícia.
- Armazenamento local bloqueado/cheio: informar que preferências não serão mantidas; continuar leitura.

Atualizar a página apenas consulta o banco; não dispara coleta externa. Não usar botão “Atualizar notícias” que prometa busca em tempo real na modalidade diária.

## Preferências e favoritos

Guardar snapshot mínimo com id, título, URL, veículo e data; não salvar corpo de matéria. Versionar o formato do localStorage e tratar JSON corrompido sem derrubar a aplicação. Sem sincronização ou garantia após limpeza do navegador. Preferências locais aplicam-se apenas quando não houver filtros explícitos na URL. Ler localStorage após montagem para evitar divergências de hidratação.

## Acessibilidade e qualidade

Usar landmarks, cabeçalhos hierárquicos, rótulos de campos, foco visível e navegação completa por teclado. Não comunicar estado apenas por cor. Alvos de toque confortáveis e contraste verificável. Testar a 360 px e 1280 px, além de zoom de 200%. A lista deve permanecer utilizável sem rolagem horizontal. Datas devem considerar Europe/Lisbon com horário de verão, sem offset fixo.
