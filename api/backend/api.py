import glob
import os
import psycopg2
import configparser

from flask import Flask, jsonify, request
from flask_cors import CORS
from web_scraper.main import WebScraper
from pdf_reader.pdf_to_csv import PdfToCSV

app = Flask(__name__)
CORS(app)

config = configparser.ConfigParser()
config.read("C:\\repo\\intuitive_care\\.config")

if 'DATABASE' not in config:
    raise Exception("A seção [DATABASE] não foi encontrada no arquivo de configuração.")

DATABASE = config['DATABASE']

DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"
print("Configuration loaded successfully!")


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

    try:

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
        operators = cursor.fetchall()

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
        for operator in operators:
            operadortors_list.append({
                'razao_social': operator[0],
                'nome_fantasia': operator[1],
                'registro_ans': operator[2],
                'cnpj': operator[3],
                'representante': operator[4]
            })

        return jsonify({'operators': operadortors_list, 'totalCount': total_count, 'totalPages': total_pages})

    except Exception as e:
        print(f"Error to search operators: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/setup_db', methods=['POST'])
def setup_db():
    querys_path = DATABASE['querys']

    sql_files = glob.glob(os.path.join(querys_path, "**", "*.sql"), recursive=True)

    if not sql_files:
        return jsonify({"error": "No SQL file found!!"}), 400

    print(f"Files found: {sql_files}")

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

        return jsonify({"message": "Database configured successfully!"})

    except Exception as e:
        print(f"Error configuring the database: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/download_files', methods=['POST'])
def download_files():
    try:
        result = WebScraper()
        if result is None:
            return jsonify({"error": "WebScraper did not return data."}), 500

        return jsonify({"message": "Finishing web scraping"})
    except Exception as e:
        print(f"Error downloading files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/pdf_csv', methods=['POST'])
def transformation_to_csv():

    try:

        result = PdfToCSV()

        if result is None:
            return jsonify({"error": "PdfToCSV did not return data."}), 500

        return jsonify({"message": "Finishing transformation"})

    except Exception as e:
        print(f"Error downloading files: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/gastos_anuais', methods=['GET'])
def get_gastos_anuais():

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        ano = request.args.get('ano')

        if ano:
            query = """
            SELECT * FROM financial_statements.mv_gastos_anuais
            WHERE "ANO" = %s;
            """
            cursor.execute(query, (ano,))
        else:
            query = "SELECT * FROM financial_statements.mv_gastos_anuais LIMIT 10;"
            cursor.execute(query)

        results = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]
        gastos_anuais = [dict(zip(colunas, linha)) for linha in results]

        cursor.close()
        conn.close()

        return jsonify({'gastos_anuais': gastos_anuais})

    except Exception as e:
        print(f"Error search annual expenses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/anos_gastos_anual', methods=['GET'])
def get_anos_disponiveis_anual():

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        query = 'SELECT DISTINCT "ANO" FROM financial_statements.mv_gastos_anuais ORDER BY "ANO" DESC;'
        cursor.execute(query)
        anos = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()


        return jsonify({"anos": anos})

    except Exception as e:
        print(f"Error search year annual expenses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/gastos_trimestrais', methods=['GET'])
def get_gastos_trimestrais():

    try:

        ano = request.args.get('ano')
        page = int(request.args.get('page', 1))
        limit = 15
        offset = (page - 1) * limit

        conn = get_db_connection()
        cursor = conn.cursor()

        where_clauses = []
        query_params = []

        if ano:
            where_clauses.append('"ANO" = %s')
            query_params.append(ano)

        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

        query = f"""
            SELECT "EMPRESA", "NOME FANTASIA", "REGISTRO ANS", "DESCRIÇÃO", "ANO", "GASTOS TRIMESTRAL FINAL"
            FROM financial_statements.mv_gastos_trimestrais
            WHERE {where_sql}
            LIMIT {limit} OFFSET {offset};
        """

        count_query = f"""
            SELECT COUNT(*) FROM financial_statements.mv_gastos_trimestrais
            WHERE {where_sql};
        """

        cursor.execute(query, query_params)
        results = cursor.fetchall()

        cursor.execute(count_query, query_params)
        total_count = cursor.fetchone()[0]
        total_pages = (total_count + limit - 1) // limit

        gastos_trimestrais = [
            {
                "empresa": row[0],
                "nome_fantasia": row[1],
                "registro_ans": row[2],
                "descricao": row[3],
                "ano": row[4],
                "gastos_trimestrais": row[5]
            }
            for row in results
        ]

        cursor.close()
        conn.close()

        return jsonify({
            "gastos_trimestrais": gastos_trimestrais,
            "totalCount": total_count,
            "totalPages": total_pages
        })

    except Exception as e:
        print(f"Error fetching quarterly expenses: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/anos_gastos_trimestrais', methods=['GET'])
def get_anos_disponiveis_trimestre():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = 'SELECT DISTINCT "ANO" FROM financial_statements.mv_gastos_trimestrais ORDER BY "ANO" DESC;'
        cursor.execute(query)
        anos = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify({"anos": anos})

    except Exception as e:
        print(f"Error search year annual expenses: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
