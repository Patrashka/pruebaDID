#!/usr/bin/env python3
"""
Servidor de demostración simplificado para el Avatar Médico Virtual
Funciona sin necesidad de claves de API para pruebas básicas
"""

import os
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ===== CONFIGURACIÓN =====
PORT = int(os.getenv("PORT", 8080))

# ===== ENDPOINTS BÁSICOS =====

@app.route("/")
def home():
    """Página de inicio"""
    return """
    <html>
    <head>
        <title>🤖 Avatar Médico Virtual - Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { color: #28a745; font-weight: bold; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .demo-link { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Avatar Médico Virtual - Demo</h1>
            <p class="status">✅ Servidor funcionando correctamente</p>
            
            <h2>📋 Endpoints Disponibles:</h2>
            <div class="endpoint">
                <strong>GET /</strong> - Esta página de inicio
            </div>
            <div class="endpoint">
                <strong>GET /api/status</strong> - Estado del servidor
            </div>
            <div class="endpoint">
                <strong>GET /api/did/config</strong> - Configuración D-ID
            </div>
            <div class="endpoint">
                <strong>POST /api/ai/did-medical-avatar</strong> - Procesamiento médico con D-ID
            </div>
            
            <h2>🌐 Páginas de Demostración:</h2>
            <a href="/demo" class="demo-link">Ver Página de Demostración</a>
            
            <h2>⚙️ Configuración:</h2>
            <p>Para usar todas las funciones, configura las variables en el archivo <code>.env</code>:</p>
            <ul>
                <li>GOOGLE_GEMINI_API_KEY</li>
                <li>DID_API_KEY</li>
                <li>DID_AGENT_ID</li>
                <li>DID_CLIENT_KEY</li>
            </ul>
        </div>
    </body>
    </html>
    """

@app.route("/api/status")
def api_status():
    """Estado del servidor"""
    return jsonify({
        "status": "running",
        "message": "Servidor funcionando correctamente",
        "port": PORT,
        "features": {
            "flask": True,
            "cors": True,
            "dotenv": True
        }
    })

@app.route("/api/did/config")
def get_did_config():
    """Configuración D-ID (demo)"""
    return jsonify({
        "status": "demo",
        "message": "Modo demostración - configura las variables de entorno para usar D-ID",
        "required_vars": [
            "DID_API_KEY",
            "DID_AGENT_ID", 
            "DID_CLIENT_KEY"
        ],
        "demo_mode": True
    })

@app.route("/api/ai/did-medical-avatar", methods=["POST"])
def did_medical_avatar_demo():
    """Endpoint de demostración para procesamiento médico"""
    return jsonify({
        "status": "demo",
        "message": "Este es un endpoint de demostración",
        "note": "Configura las variables de entorno para usar la funcionalidad completa",
        "required_config": {
            "GOOGLE_GEMINI_API_KEY": "Para procesamiento de IA",
            "DID_API_KEY": "Para integración con avatar",
            "DID_AGENT_ID": "ID del agente D-ID",
            "DID_CLIENT_KEY": "Clave de cliente D-ID"
        }
    })

@app.route("/demo")
def demo_page():
    """Página de demostración simplificada"""
    return """
    <html>
    <head>
        <title>Demo - Avatar Médico Virtual</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
            .status-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .success { background: #d4edda; color: #155724; }
            .warning { background: #fff3cd; color: #856404; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Avatar Médico Virtual - Demo</h1>
            
            <div class="status-box success">
                <h3>✅ Servidor Funcionando</h3>
                <p>El servidor está ejecutándose correctamente en el puerto """ + str(PORT) + """</p>
            </div>
            
            <div class="status-box warning">
                <h3>⚠️ Configuración Pendiente</h3>
                <p>Para usar todas las funciones del avatar médico, necesitas configurar las variables de entorno en el archivo <code>.env</code></p>
            </div>
            
            <h2>🧪 Pruebas de API</h2>
            <button class="btn" onclick="testAPI()">Probar API Status</button>
            <button class="btn" onclick="testDIDConfig()">Probar Config D-ID</button>
            
            <div id="results" style="margin-top: 20px;"></div>
            
            <h2>📁 Archivos Disponibles</h2>
            <ul>
                <li><strong>medical_avatar_demo.html</strong> - Página completa con D-ID SDK</li>
                <li><strong>server_combined.py</strong> - Servidor completo con todas las funciones</li>
                <li><strong>setup_local_tunnel.py</strong> - Script para configurar túnel ngrok</li>
                <li><strong>start_medical_avatar.py</strong> - Script de inicio automático</li>
            </ul>
            
            <h2>🚀 Próximos Pasos</h2>
            <ol>
                <li>Configura las variables en <code>.env</code></li>
                <li>Ejecuta <code>python server_combined.py</code> para el servidor completo</li>
                <li>Abre <code>medical_avatar_demo.html</code> en tu navegador</li>
                <li>Configura el túnel ngrok para D-ID</li>
            </ol>
        </div>
        
        <script>
            async function testAPI() {
                try {
                    const response = await fetch('/api/status');
                    const data = await response.json();
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box success"><h4>API Status:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box" style="background: #f8d7da; color: #721c24;"><h4>Error:</h4><p>' + error.message + '</p></div>';
                }
            }
            
            async function testDIDConfig() {
                try {
                    const response = await fetch('/api/did/config');
                    const data = await response.json();
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box warning"><h4>D-ID Config:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box" style="background: #f8d7da; color: #721c24;"><h4>Error:</h4><p>' + error.message + '</p></div>';
                }
            }
        </script>
    </body>
    </html>
    """

# ===== MAIN =====
if __name__ == "__main__":
    print("AVATAR MEDICO VIRTUAL - SERVIDOR DEMO")
    print("=" * 50)
    print(f"Iniciando servidor en puerto {PORT}")
    print(f"Abre: http://localhost:{PORT}")
    print(f"Demo: http://localhost:{PORT}/demo")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=PORT, debug=True)
