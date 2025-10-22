import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===== CONFIGURACIÓN D-ID =====
DID_API_KEY = os.environ.get("DID_API_KEY", "")
DID_AGENT_ID = os.environ.get("DID_AGENT_ID", "")
DID_CLIENT_KEY = os.environ.get("DID_CLIENT_KEY", "")
DID_BASE_URL = "https://api.d-id.com"

# ===== ENDPOINTS =====

@app.route("/")
@app.route("/api")
def home():
    """Página de inicio"""
    return jsonify({
        "status": "running",
        "message": "Avatar Medico Virtual - D-ID API",
        "did_api_key": "configured" if DID_API_KEY else "missing",
        "did_agent_id": "configured" if DID_AGENT_ID else "missing",
        "did_client_key": "configured" if DID_CLIENT_KEY else "missing",
        "endpoints": [
            "/api/status",
            "/api/did/config"
        ]
    })

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

# Test endpoint
@app.route("/api/test")
def test():
    return jsonify({"message": "Test successful!", "status": "ok"})

# Para Vercel
@app.route("/<path:path>")
def catch_all(path):
    return jsonify({
        "error": "Not Found",
        "path": f"/{path}",
        "available_endpoints": ["/", "/api/status", "/api/did/config", "/api/test"]
    }), 404
