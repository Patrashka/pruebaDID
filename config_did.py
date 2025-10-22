#!/usr/bin/env python3
"""
Script para configurar D-ID con la API key proporcionada
"""

import os

# Tu API key de D-ID
DID_API_KEY = "aW50ZWdyYWNpb24yNTlAZ21haWwuY29t:nbrNazwVQw3qIidcJv5p0"

# Crear archivo .env con la configuración
env_content = f"""# Google Gemini API
GOOGLE_GEMINI_API_KEY=tu_gemini_api_key_aqui

# D-ID Configuration
DID_API_KEY={DID_API_KEY}
DID_AGENT_ID=tu_agent_id_aqui
DID_CLIENT_KEY=tu_client_key_aqui

# Server Configuration
PORT=8080
"""

# Escribir el archivo .env
with open('.env', 'w', encoding='utf-8') as f:
    f.write(env_content)

print("Archivo .env configurado con tu API key de D-ID")
print("Ahora necesitas:")
print("   1. Crear un agente en D-ID Studio")
print("   2. Obtener el Agent ID y Client Key")
print("   3. Configurar Google Gemini API Key")
print("   4. Actualizar el archivo .env con esos valores")
