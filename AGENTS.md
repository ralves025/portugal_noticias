# Orientações para agentes

## Contexto e escopo

Este repositório contém o planejamento de um mini hub pessoal de notícias de Portugal. Leia README.md e os documentos em docs/ antes de trabalhar. O pedido original autoriza apenas a documentação inicial; a implementação depende de uma tarefa posterior do usuário.

## Convenções para trabalhos futuros

- Preserve a simplicidade do MVP e registre mudanças de escopo em docs/07-decisoes.md.
- Use português na documentação e interface; preserve a redação original dos títulos.
- Não considere uma fonte ativa sem validar o endpoint e registrar condições de uso e campos permitidos.
- Não invente notícias, URLs de feeds, datas ou resultados de testes. Identifique fixtures como conteúdo fictício.
- Separe acesso externo, normalização e persistência. Leia os contratos de docs/04-arquitetura.md antes de alterá-los.
- Não exponha credenciais, não use prefixo público para chaves de servidor e não versione arquivos de segredos.
- Não faça scraping, contorne paywalls ou acrescente IA, autenticação e notificações ao MVP sem alteração explícita de escopo.
- Ao implementar, fixe versões compatíveis e mantenha o lockfile. Execute os testes relevantes de docs/06-execucao.md.
- Entregue um relato com arquivos alterados, validações realmente executadas e limitações. Não marque etapas futuras como concluídas.

## Divisão do trabalho

Os pacotes do plano podem ser atribuídos a agentes em tarefas futuras. A divisão não exige execução simultânea. Evite alterações concorrentes nos contratos, migrações e lockfile; combine interfaces antes de integrar.

## Repositório e fluxo Git

- Repositório definido pelo usuário: https://github.com/ralves025/portugal_noticias.
- Antes de configurar Git ou sincronizar, inspecione o estado local e remoto e confirme a branch principal existente; não presuma main ou master.
- Se já existir um remoto origin diferente, investigue antes de substituí-lo. Preserve arquivos locais e conteúdo remoto durante a integração inicial.
- Fluxo recomendado: uma branch por tarefa e pull request para a branch principal, com resumo e validações executadas.
- Não use force push nem descarte histórico ou alterações para resolver divergências. A indicação do repositório na documentação não significa que os arquivos já foram enviados.
