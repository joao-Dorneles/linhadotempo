from flask import Flask, render_template, send_from_directory, jsonify, request, Response
import os
import requests

app = Flask(__name__)

CARDAPIO_BASE_URL = "https://usercenterlt.onrender.com"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml', mimetype='application/xml')

@app.route("/proxy-search")
def proxy_search():
    termo = request.args.get('q', '') 
    target_url = f"{CARDAPIO_BASE_URL}/api/search?q={termo}"
    
    try:
        response = requests.get(target_url)
        proxy_response = Response(response.content)
        proxy_response.headers['Content-Type'] = response.headers.get('Content-Type', 'application/json')
        
        return proxy_response
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com o Domínio 2: {e}")
        return jsonify({"error": "Falha na comunicação com o servidor de Cardápio."}), 503

if __name__ == "__main__":
    app.run(debug=True)