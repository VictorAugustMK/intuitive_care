
import subprocess

from flask import Flask, jsonify
from flask_cors import CORS
import web_scraper.main as crawler

app = Flask(__name__)
CORS(app)

@app.route('/api/mensagem', methods=['GET'])
def mensagem():
    return jsonify({"mensagem": "Olá, esta é uma mensagem da API Python!"})

@app.route('/api/sobre', methods=['GET'])
def sobre():
    return jsonify({"sobre": "Esta é a página sobre do backend!"})

@app.route('/api/download', methods=['GET'])
def download():
    try:
        download_crawler = crawler
        resultado = subprocess.run(['python', download_crawler], capture_output=True, text=True)

        if resultado.returncode == 0:
            return jsonify({"status": "Sucesso", "output": resultado.stdout})
        else:
            return jsonify({"status": "Erro", "output": resultado.stderr})

    except Exception as e:
        return jsonify({"status": "Erro", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)