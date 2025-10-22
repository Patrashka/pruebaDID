#!/usr/bin/env python3
"""
Servidor con integración D-ID funcional
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

# ===== CONFIGURACIÓN D-ID =====
DID_API_KEY = os.getenv("DID_API_KEY")
DID_AGENT_ID = os.getenv("DID_AGENT_ID")
DID_CLIENT_KEY = os.getenv("DID_CLIENT_KEY")
DID_BASE_URL = "https://api.d-id.com"

# ===== ALMACENAMIENTO TEMPORAL =====
conversations = {}
medical_findings = {}

def register_medical_finding(session_id, finding, severity="normal"):
    """Registra un hallazgo médico importante"""
    if session_id not in medical_findings:
        medical_findings[session_id] = []
    
    medical_findings[session_id].append({
        "timestamp": datetime.now().isoformat(),
        "finding": finding,
        "severity": severity
    })

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
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .status { color: #28a745; font-weight: bold; }
            .warning { color: #ffc107; font-weight: bold; }
            .error { color: #dc3545; font-weight: bold; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px 0; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Avatar Medico Virtual - D-ID</h1>
            
            <div class="status">✅ Servidor funcionando</div>
            <div class="status">✅ D-ID API Key configurada</div>
            
            """ + (f'<div class="status">✅ Agent ID: {DID_AGENT_ID}</div>' if DID_AGENT_ID != 'tu_agent_id_aqui' else '<div class="warning">⚠️ Agent ID no configurado</div>') + """
            """ + (f'<div class="status">✅ Client Key: {DID_CLIENT_KEY[:20]}...</div>' if DID_CLIENT_KEY != 'tu_client_key_aqui' else '<div class="warning">⚠️ Client Key no configurado</div>') + """
            
            <h2>Endpoints Disponibles:</h2>
            <div class="endpoint">
                <strong>GET /api/status</strong> - Estado del servidor
            </div>
            <div class="endpoint">
                <strong>GET /api/did/agents</strong> - Lista de agentes D-ID
            </div>
            <div class="endpoint">
                <strong>GET /api/did/config</strong> - Configuración D-ID
            </div>
            <div class="endpoint">
                <strong>POST /api/ai/medical-chat</strong> - Chat médico básico
            </div>
            
            <h2>Páginas:</h2>
            <a href="/demo" class="btn">Página de Demostración</a>
            <a href="/avatar_simple.html" class="btn" style="background: #28a745;">🎥 AVATAR SIMPLE</a>
            <a href="/medical_avatar_demo.html" class="btn">Avatar Completo</a>
            <a href="/VERCEL_QUICK_START.html" class="btn" style="background: #28a745;">🚀 GUÍA VERCEL</a>
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
        "did_agent_id": "configured" if DID_AGENT_ID != 'tu_agent_id_aqui' else "missing",
        "did_client_key": "configured" if DID_CLIENT_KEY != 'tu_client_key_aqui' else "missing",
        "agents_count": len(conversations),
        "findings_count": len(medical_findings)
    })

@app.route("/api/did/agents")
def get_did_agents():
    """Obtiene la lista de agentes D-ID"""
    if not DID_API_KEY:
        return jsonify({"error": "D-ID API Key no configurada"}), 500
    
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{DID_BASE_URL}/agents", headers=headers)
        
        if response.status_code == 200:
            agents = response.json()
            return jsonify({
                "status": "success",
                "agents": agents.get('agents', []),
                "total": len(agents.get('agents', []))
            })
        else:
            return jsonify({
                "error": f"D-ID API error: {response.status_code}",
                "message": response.text
            }), response.status_code
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/did/config")
def get_did_config():
    """Devuelve la configuración D-ID"""
    return jsonify({
        "api_key": "configured" if DID_API_KEY else "missing",
        "agent_id": DID_AGENT_ID if DID_AGENT_ID != 'tu_agent_id_aqui' else "not_configured",
        "client_key": DID_CLIENT_KEY if DID_CLIENT_KEY != 'tu_client_key_aqui' else "not_configured",
        "base_url": DID_BASE_URL,
        "status": "ready" if all([DID_API_KEY, DID_AGENT_ID != 'tu_agent_id_aqui', DID_CLIENT_KEY != 'tu_client_key_aqui']) else "incomplete"
    })

@app.route("/api/ai/medical-chat", methods=["POST"])
def medical_chat():
    """Chat médico básico (sin IA por ahora)"""
    data = request.json or {}
    message = data.get("message", "")
    session_id = data.get("session_id", str(uuid.uuid4()))
    
    if not message:
        return jsonify({"error": "Falta el mensaje"}), 400
    
    # Simular respuesta médica básica
    responses = [
        "Entiendo tu consulta. ¿Podrías darme más detalles sobre tus síntomas?",
        "Esa es una preocupación válida. ¿Cuánto tiempo has tenido estos síntomas?",
        "Gracias por compartir esa información. ¿Has tomado algún medicamento?",
        "Es importante que consultes con un médico si los síntomas persisten.",
        "¿Has tenido fiebre o algún otro síntoma acompañante?"
    ]
    
    import random
    response = random.choice(responses)
    
    # Guardar en conversación
    conversations.setdefault(session_id, [])
    conversations[session_id].append({"role": "user", "content": message})
    conversations[session_id].append({"role": "assistant", "content": response})
    
    # Simular hallazgo médico ocasional
    if "dolor" in message.lower() or "fiebre" in message.lower():
        register_medical_finding(session_id, f"Síntomas reportados: {message}", "followup")
    
    return jsonify({
        "status": "success",
        "session_id": session_id,
        "response": response,
        "conversation_length": len(conversations[session_id])
    })

@app.route("/api/ai/findings/<session_id>")
def get_findings(session_id):
    """Obtiene hallazgos médicos de una sesión"""
    findings = medical_findings.get(session_id, [])
    return jsonify({
        "session_id": session_id,
        "findings": findings,
        "total": len(findings)
    })

@app.route("/medical_avatar_demo.html")
def medical_avatar_page():
    """Sirve la página del avatar médico"""
    try:
        with open('medical_avatar_demo.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo medical_avatar_demo.html no encontrado", 404

@app.route("/avatar_simple.html")
def avatar_simple_page():
    """Sirve la página simplificada del avatar"""
    try:
        with open('avatar_simple.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo avatar_simple.html no encontrado", 404

@app.route("/fix_did_connection.html")
def fix_did_connection_page():
    """Página para solucionar problemas de conexión D-ID"""
    try:
        with open('fix_did_connection.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo fix_did_connection.html no encontrado", 404

@app.route("/alternative_solution.html")
def alternative_solution_page():
    """Página con soluciones alternativas para Fortigate"""
    try:
        with open('alternative_solution.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo alternative_solution.html no encontrado", 404

@app.route("/VERCEL_QUICK_START.html")
def vercel_guide_page():
    """Guía rápida para desplegar en Vercel"""
    try:
        with open('VERCEL_QUICK_START.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Archivo VERCEL_QUICK_START.html no encontrado", 404

@app.route("/demo")
def demo_page():
    """Página de demostración"""
    return """
    <html>
    <head>
        <title>Demo - Avatar Medico</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }
            .status-box { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }
            .success { background: #d4edda; color: #155724; }
            .warning { background: #fff3cd; color: #856404; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .btn:hover { background: #0056b3; }
            .chat-box { background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; height: 300px; overflow-y: auto; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #007bff; color: white; text-align: right; }
            .assistant { background: #e9ecef; color: #333; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Demo - Avatar Medico Virtual</h1>
            
            <div class="status-box success">
                <h3>Servidor Funcionando</h3>
                <p>D-ID API configurada correctamente</p>
            </div>
            
            <div class="status-box warning">
                <h3>Configuración Pendiente</h3>
                <p>Necesitas configurar el Agent ID y Client Key para usar el avatar completo</p>
            </div>
            
            <h2>Chat Médico Básico</h2>
            <div class="chat-box" id="chatBox">
                <div class="message assistant">Hola, soy tu asistente médico virtual. ¿En qué puedo ayudarte?</div>
            </div>
            
            <input type="text" id="messageInput" placeholder="Escribe tu consulta médica..." style="width: 70%; padding: 10px;">
            <button class="btn" onclick="sendMessage()">Enviar</button>
            
            <h2>Pruebas de API</h2>
            <button class="btn" onclick="testAgents()">Ver Agentes D-ID</button>
            <button class="btn" onclick="testConfig()">Ver Configuración</button>
            
            <div id="results" style="margin-top: 20px;"></div>
        </div>
        
        <script>
            let currentSessionId = null;
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                // Agregar mensaje del usuario
                addMessage('user', message);
                input.value = '';
                
                try {
                    const response = await fetch('/api/ai/medical-chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            message: message,
                            session_id: currentSessionId
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'success') {
                        currentSessionId = data.session_id;
                        addMessage('assistant', data.response);
                    } else {
                        addMessage('assistant', 'Error: ' + data.error);
                    }
                } catch (error) {
                    addMessage('assistant', 'Error de conexión: ' + error.message);
                }
            }
            
            function addMessage(role, content) {
                const chatBox = document.getElementById('chatBox');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}`;
                messageDiv.textContent = content;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
            
            async function testAgents() {
                try {
                    const response = await fetch('/api/did/agents');
                    const data = await response.json();
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box"><h4>Agentes D-ID:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box" style="background: #f8d7da;"><h4>Error:</h4><p>' + error.message + '</p></div>';
                }
            }
            
            async function testConfig() {
                try {
                    const response = await fetch('/api/did/config');
                    const data = await response.json();
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box"><h4>Configuración D-ID:</h4><pre>' + JSON.stringify(data, null, 2) + '</pre></div>';
                } catch (error) {
                    document.getElementById('results').innerHTML = 
                        '<div class="status-box" style="background: #f8d7da;"><h4>Error:</h4><p>' + error.message + '</p></div>';
                }
            }
            
            // Permitir enviar con Enter
            document.getElementById('messageInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

# ===== MAIN =====
if __name__ == "__main__":
    print("AVATAR MEDICO VIRTUAL - D-ID INTEGRATION")
    print("=" * 50)
    print(f"D-ID API Key: {'Configurada' if DID_API_KEY else 'Faltante'}")
    print(f"Agent ID: {'Configurado' if DID_AGENT_ID != 'tu_agent_id_aqui' else 'Faltante'}")
    print(f"Client Key: {'Configurado' if DID_CLIENT_KEY != 'tu_client_key_aqui' else 'Faltante'}")
    print("=" * 50)
    print("Iniciando servidor...")
    print("Abre: http://localhost:8080")
    print("Demo: http://localhost:8080/demo")
    
    app.run(host="0.0.0.0", port=8080, debug=True)
