# Assets Project

## Descrição

O projeto tem por objetivo realizar o cadastro de ativos e monitoramento dos mesmos em intervalos pré-configurados, de forma que o usuário receba notificações por e-mail caso o ativo cruze algum túnel de preço.

## Configuração do projeto

### Tecnologias

O backend foi desenvolvido usando Python 3.9.6, com o framework Django 4.2.20. 

O frontend foi implementado utilizando HTML, CSS, Javascript e Bootstrap. 

O banco de dados escolhido foi o PostgreSQL 13.3.

O monitoramento dos ativos foi realizado utilizando a API [brapi.dev](https://brapi.dev).

Para o monitoramento dos ativos em uma periodicidade de tempo pré-definida, foi utilizado o Celery, com o backend Redis.

Para o gerenciamento das dependências do projeto, foi escolhido o [pip-tools](https://pypi.org/project/pip-tools/).
### Instruções de execução

Crie, na raiz do projeto, um arquivo .env para armazenar suas variáveis de ambiente. Um arquivo de exemplo pode ser encontrado [aqui](.env_example).

Para a criação dos containers no Docker e execução do sistema, execute:
> make local-up

Após iniciar o projeto, é possível acessar a tela de login no seguinte link:
> http://localhost:8000/auth/login
