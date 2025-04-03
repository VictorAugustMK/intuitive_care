📌 Projeto: Sistema de Consulta de Operadoras e Gastos

📖 Visão Geral

Este projeto é uma aplicação web para consulta e análise de dados de operadoras de planos de saúde. Ele permite a busca de operadoras, visualização de gastos anuais e trimestrais e a configuração automatizada do banco de dados.

Antes de iniciar, crie um banco de dados no PostgreSQL com o nome `` para garantir que a aplicação funcione corretamente.

Além disso, execute as rotas na sequência em que estão organizadas na página Home para evitar erros na utilização do sistema.

🛠 Tecnologias Utilizadas

Frontend

Vue.js

CSS para estilização

Backend

Python

Flask

PostgreSQL

psycopg2

Banco de Dados

PostgreSQL

PL/pgSQL para Stored Procedures

🚀 Instalação e Configuração

Clonando o Repositório

git clone https://github.com/VictorAugustMK/intuitive_care.git
cd intuitive_care

Configurando o Backend

Instale as dependências do Python:

pip install -r requirements.txt

Configure o arquivo .config com as credenciais do banco de dados e ajuste os diretórios conforme necessário.

Exemplo de diretórios recomendados no .config:

download_dir = C:\repo\intuitive_care\web_scraper\out
cookies_folder = C://repo//intuitive_care//web_scraper//chromedriver//cookies
accounting_folder = C:\repo\intuitive_care\accounting_intuitive_care\financial_statements
operator_plans_folder = C:\repo\intuitive_care\accounting_intuitive_care\operator_plans

Inicie a API Flask:

python app.py

Configurando o Frontend

Navegue até a pasta do frontend:

cd frontend

Instale as dependências:

npm install

Inicie o servidor Vue.js:

npm run dev

📌 Funcionalidades

📌 Página Inicial

Acesso à listagem de operadoras

Botão para configurar o banco de dados automaticamente

📌 Operadoras

Busca avançada por Razão Social, Nome Fantasia, Registro ANS, CNPJ e Representante

Paginação para exibir resultados em blocos de 15 itens

Botão "Buscar Todos"

📌 Gastos Anuais

Tabela com Empresa, Nome Fantasia, Registro ANS, Descrição, Ano e Gastos Anuais

Filtro por ano que mantém os valores disponíveis mesmo após buscas

📌 Gastos Trimestrais

Similar à tela de gastos anuais, mas focado nos gastos por trimestre

Paginação corrigida para evitar duplicação de resultados

📌 Rotas Disponíveis

Backend (Flask)

GET /operadoras - Consulta operadoras com filtros e paginação.

POST /setup-db - Executa scripts SQL para configuração do banco.

GET /gastos-trimestrais - Obtém dados dos gastos trimestrais.

GET /gastos-anuais - Obtém dados dos gastos anuais.

Frontend (Vue.js)

/ - Home Page

/operadoras - Tela de consulta de operadoras.

/gastos-trimestrais - Tela de consulta de gastos trimestrais.

/gastos-anuais - Tela de consulta de gastos anuais.

📌 Melhorias Futuras

Implementação de testes automatizados.

Melhoria na performance das consultas.

Melhor tratamento de erros.

📜 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.
