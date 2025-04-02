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
def search_operadoras():
    search_term = request.args.to_dict()  # Pega todos os parâmetros da URL, incluindo filtros e paginação
    page = int(request.args.get('page', 1))  # Obtém o número da página
    limit = 15  # Número de resultados por página
    offset = (page - 1) * limit  # Cálculo do offset

    # Conectar ao banco
    conn = get_db_connection()
    cursor = conn.cursor()

    # Construir a consulta SQL com base nos filtros fornecidos
    where_clauses = []
    query_params = []

    for key, value in search_term.items():
        if key != "page" and key != "limit" and value:  # Exclui os parâmetros 'page' e 'limit' para o filtro
            where_clauses.append(f"{key} ILIKE %s")
            query_params.append(f"%{value}%")

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
    query = f"""
    SELECT razao_social, nome_fantasia, registro_ans, cnpj, representante
    FROM operator_plans.report_cadop
    WHERE {where_sql}
    LIMIT {limit} OFFSET {offset};
    """

    cursor.execute(query, query_params)
    operadoras = cursor.fetchall()

    # Obter o número total de resultados
    count_query = f"""
    SELECT COUNT(*) FROM operator_plans.report_cadop
    WHERE {where_sql};
    """
    cursor.execute(count_query, query_params)
    total_count = cursor.fetchone()[0]
    total_pages = (total_count + limit - 1) // limit

    cursor.close()
    conn.close()

    operadoras_list = []
    for operadora in operadoras:
        operadoras_list.append({
            'razao_social': operadora[0],
            'nome_fantasia': operadora[1],
            'registro_ans': operadora[2],
            'cnpj': operadora[3],
            'representante': operadora[4]
        })
    # Retorne o JSON com os resultados e a contagem total
    return jsonify({'operadoras': operadoras_list, 'totalCount': total_count, 'totalPages': total_pages})

if __name__ == '__main__':
    app.run(debug=True)
