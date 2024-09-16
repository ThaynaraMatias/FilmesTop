FilmesTop é uma aplicação web para gerenciar filmes e aluguéis. Os usuários podem se cadastrar, adicionar filmes, listar filmes por gênero e alugar filmes. Estão disponíveis
as seguintes funcionalidades:
1. Autenticação de Usuário: Permite que usuários façam login e gerenciem suas sessões.
2. Gerenciamento de Filmes: Permite a adição de novos filmes e exibição dos filmes disponíveis.
3. Aluguel de Filmes: Permite o aluguel dos filmes disponíveis.
4. Avaliação de Filmes: Permite a avaliação dos filmes que o usuário já alugou.
5. Listagem de Aluguéis: Exibi todos os aluguéis realizados por um usuário.

Orientações para Executar o Projeto
1. Clone o Repositório:
  git clone <url-do-repositorio>
  cd nome-do-repositorio

2. Configure um Ambiente Virtual
  python -m venv venv
  source venv/bin/activate  # Para Unix/macOS
  venv\Scripts\activate     # Para Windows

3. Instale as Dependências
   pip install -r requirements.txt

Configuração do Banco de Dados:
1. No shell do Python, execute os seguintes comandos para criar o banco de dados e as tabelas:
  from filmestop import db
  db.create_all()
  exit()

Executando a Aplicação:
1. No terminal, execute o comando para iniciar a aplicação:
   flask run

