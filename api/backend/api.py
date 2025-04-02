from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import configparser

app = Flask(__name__)
CORS(app)

# Carregar as configurações do banco
config = configparser.ConfigParser()
config.read("C:\\repo\\intuitive_care\\.config")

# Verificar se a seção [DATABASE] existe no arquivo de configuração
if 'DATABASE' not in config:
    raise Exception("A seção [DATABASE] não foi encontrada no arquivo de configuração.")

DATABASE = config['DATABASE']

# Formatar a URI do banco de dados
DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"
print("Configuração carregada com sucesso!")

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host=DATABASE['host'],
        database=DATABASE['database'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        port=DATABASE['port']
    )
    return conn

# Rota para buscar operadoras
@app.route('/operadoras', methods=['GET'])
@app.route('/operadoras', methods=['GET'])
def search_operadoras():
    search_term = request.args.get('search', '')  # Pega o parâmetro de busca
    page = int(request.args.get('page', 1))  # Pega a página atual, default é 1
    per_page = 15  # Número de resultados por página
    offset = (page - 1) * per_page  # Cálculo do offset para a consulta SQL

    conn = get_db_connection()
    cursor = conn.cursor()

    # Query para pegar os dados da tabela com LIMIT e OFFSET
    query = f"""
    SELECT razao_social AS "Razão Social",
           nome_fantasia AS "Nome Fantasia",
           registro_ans AS "Registro ANS",
           cnpj AS "CNPJ",
           representante AS "Representante"
    FROM operator_plans.report_cadop
    WHERE razao_social ILIKE %s OR nome_fantasia ILIKE %s
    LIMIT %s OFFSET %s;
    """
    cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%', per_page, offset))

    operadoras = cursor.fetchall()

    # Calcular o número total de páginas
    cursor.execute(f"SELECT COUNT(*) FROM operator_plans.report_cadop WHERE razao_social ILIKE %s OR nome_fantasia ILIKE %s;", ('%' + search_term + '%', '%' + search_term + '%'))
    total_results = cursor.fetchone()[0]
    total_pages = (total_results // per_page) + (1 if total_results % per_page > 0 else 0)

    cursor.close()
    conn.close()

    # Formatando os dados para enviar como JSON
    operadoras_list = []
    for operadora in operadoras:
        operadoras_list.append({
            'razao_social': operadora[0],
            'nome_fantasia': operadora[1],
            'registro_ans': operadora[2],
            'cnpj': operadora[3],
            'representante': operadora[4]
        })

    return jsonify({
        'operadoras': operadoras_list,
        'total_pages': total_pages
    })


if __name__ == '__main__':
    app.run(debug=True)
