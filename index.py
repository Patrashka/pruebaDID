import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# ===== CONFIGURACIÓN D-ID =====
DID_API_KEY = os.environ.get("DID_API_KEY", "")
DID_AGENT_ID = os.environ.get("DID_AGENT_ID", "")
DID_CLIENT_KEY = os.environ.get("DID_CLIENT_KEY", "")
DID_BASE_URL = "https://api.d-id.com"

# ===== ENDPOINTS =====

@app.route("/")
def home():
    """Página de inicio"""
    return """
    <html>
    <head>
        <title>Avatar Medico Virtual - D-ID</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 800px; margin: 0 auto; }
            .status { color: #28a745; font-weight: bold; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Avatar Medico Virtual - D-ID</h1>
            <p class="status">Servidor funcionando correctamente</p>
            <p>D-ID API Key: """ + ('Configurada' if DID_API_KEY else 'Faltante') + """</p>
            <p>Agent ID: """ + ('Configurado' if DID_AGENT_ID else 'Faltante') + """</p>
            <p>Client Key: """ + ('Configurado' if DID_CLIENT_KEY else 'Faltante') + """</p>
            <h2>Paginas:</h2>
            <a href="/avatar_simple.html" class="btn">Avatar Simple</a>
            <a href="/api/status" class="btn">Ver Status</a>
        </div>
    </body>
    </html>
    """

@app.route("/api/status")
def api_status():
    """Estado del servidor"""
    return jsonify({
        "status": "running",
        "did_api_key": "configured" if DID_API_KEY else "missing",
        "did_agent_id": "configured" if DID_AGENT_ID else "missing",
        "did_client_key": "configured" if DID_CLIENT_KEY else "missing"
    })

@app.route("/api/did/config")
def get_did_config():
    """Devuelve la configuración D-ID"""
    return jsonify({
        "api_key": "configured" if DID_API_KEY else "missing",
        "agent_id": DID_AGENT_ID if DID_AGENT_ID else "not_configured",
        "client_key": DID_CLIENT_KEY if DID_CLIENT_KEY else "not_configured",
        "base_url": DID_BASE_URL,
        "status": "ready" if all([DID_API_KEY, DID_AGENT_ID, DID_CLIENT_KEY]) else "incomplete"
    })

@app.route("/avatar_simple.html")
def avatar_simple():
    """Página del avatar simple"""
    try:
        import os
        file_path = os.path.join(os.path.dirname(__file__), '..', 'avatar_simple.html')
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}", 404

# Vercel necesita esta exportación
app.config['DEBUG'] = False
