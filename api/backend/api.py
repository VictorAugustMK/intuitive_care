import glob
import os
import psycopg2
import configparser

from flask import Flask, jsonify, request
from flask_cors import CORS
from web_scraper.main import Crawler

app = Flask(__name__)
CORS(app)

config = configparser.ConfigParser()
config.read("C:\\repo\\intuitive_care\\.config")

if 'DATABASE' not in config:
    raise Exception("A seção [DATABASE] não foi encontrada no arquivo de configuração.")

DATABASE = config['DATABASE']

DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"
print("Configuração carregada com sucesso!")


def get_db_connection():
    conn = psycopg2.connect(
        host=DATABASE['host'],
        database=DATABASE['database'],
        user=DATABASE['user'],
        password=DATABASE['password'],
        port=DATABASE['port']
    )
    return conn


@app.route('/operadoras', methods=['GET'])
def search_operator():
    search_term = request.args.to_dict()
    page = int(request.args.get('page', 1))
    limit = 15
    offset = (page - 1) * limit

    conn = get_db_connection()
    cursor = conn.cursor()

    where_clauses = []
    query_params = []

    for key, value in search_term.items():
        if key != "page" and key != "limit" and value:
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

    count_query = f"""
    SELECT COUNT(*) FROM operator_plans.report_cadop
    WHERE {where_sql};
    """
    cursor.execute(count_query, query_params)
    total_count = cursor.fetchone()[0]
    total_pages = (total_count + limit - 1) // limit

    cursor.close()
    conn.close()

    operadortors_list = []
    for operadora in operadoras:
        operadortors_list.append({
            'razao_social': operadora[0],
            'nome_fantasia': operadora[1],
            'registro_ans': operadora[2],
            'cnpj': operadora[3],
            'representante': operadora[4]
        })

    return jsonify({'operadoras': operadortors_list, 'totalCount': total_count, 'totalPages': total_pages})


@app.route('/setup-db', methods=['POST'])
def setup_db():
    querys_path = DATABASE['querys']

    sql_files = glob.glob(os.path.join(querys_path, "**", "*.sql"), recursive=True)

    if not sql_files:
        return jsonify({"error": "Nenhum arquivo SQL encontrado!"}), 400

    print(f"Arquivos encontrados: {sql_files}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for sql_file in sql_files:
            with open(sql_file, 'r', encoding='utf-8') as file:
                sql_script = file.read()
                print(f"Executando: {sql_file}")
                cursor.execute(sql_script)

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Banco de dados configurado com sucesso!"})

    except Exception as e:
        print(f"Erro ao configurar o banco de dados: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download_files', methods=['POST'])
def download_files():
    try:
        resultado = Crawler()
        return jsonify({"message": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
