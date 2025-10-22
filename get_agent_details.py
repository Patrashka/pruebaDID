#!/usr/bin/env python3
"""
Script para obtener detalles de agentes D-ID y configurar el sistema
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

DID_API_KEY = os.getenv("DID_API_KEY")
DID_BASE_URL = "https://api.d-id.com"

def get_agent_details():
    """Obtiene detalles de todos los agentes"""
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{DID_BASE_URL}/agents", headers=headers)
        
        if response.status_code == 200:
            agents = response.json()
            
            print("AGENTES D-ID DISPONIBLES:")
            print("=" * 50)
            
            for i, agent in enumerate(agents.get('agents', [])):
                print(f"\n{i+1}. AGENTE: {agent.get('id')}")
                print(f"   Nombre: {agent.get('name', 'Sin nombre')}")
                print(f"   Estado: {agent.get('status', 'Desconocido')}")
                print(f"   Chats: {agent.get('chats', 0)}")
                print(f"   Embed: {'Habilitado' if agent.get('embed') else 'Deshabilitado'}")
                print(f"   Creado: {agent.get('created_at', 'Desconocido')}")
                
                # Obtener detalles específicos del agente
                agent_id = agent.get('id')
                agent_details = get_single_agent_details(agent_id, headers)
                
                if agent_details:
                    print(f"   Presenter: {agent_details.get('presenter', {}).get('id', 'N/A')}")
                    print(f"   Voice: {agent_details.get('voice', {}).get('id', 'N/A')}")
                    print(f"   Knowledge: {len(agent_details.get('knowledge', []))} elementos")
            
            print("\n" + "=" * 50)
            print("PARA CONFIGURAR EL AVATAR:")
            print("1. Ve a D-ID Studio: https://studio.d-id.com")
            print("2. Selecciona uno de los agentes de arriba")
            print("3. Ve a la seccion 'Embed' o 'Integration'")
            print("4. Copia el 'data-client-key' y 'data-agent-id'")
            print("5. Actualiza el archivo .env con esos valores")
            
            return agents.get('agents', [])
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_single_agent_details(agent_id, headers):
    """Obtiene detalles de un agente específico"""
    try:
        response = requests.get(f"{DID_BASE_URL}/agents/{agent_id}", headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception as e:
        print(f"Error obteniendo detalles del agente {agent_id}: {e}")
        return None

def update_env_file(agent_id, client_key):
    """Actualiza el archivo .env con los nuevos valores"""
    env_content = f"""# Google Gemini API
GOOGLE_GEMINI_API_KEY=tu_gemini_api_key_aqui

# D-ID Configuration
DID_API_KEY={DID_API_KEY}
DID_AGENT_ID={agent_id}
DID_CLIENT_KEY={client_key}

# Server Configuration
PORT=8080
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\nArchivo .env actualizado con:")
    print(f"  Agent ID: {agent_id}")
    print(f"  Client Key: {client_key[:20]}...")

def main():
    print("D-ID AGENT CONFIGURATION HELPER")
    print("=" * 50)
    
    if not DID_API_KEY:
        print("Error: No se encontró DID_API_KEY en el archivo .env")
        return
    
    # Obtener agentes
    agents = get_agent_details()
    
    if agents:
        print(f"\nSe encontraron {len(agents)} agentes.")
        print("\nSi quieres usar uno específico, ejecuta:")
        print("python get_agent_details.py --agent-id <ID_DEL_AGENTE> --client-key <CLIENT_KEY>")
        
        # Si se pasan argumentos, actualizar configuración
        import sys
        if len(sys.argv) >= 5:
            if sys.argv[1] == "--agent-id" and sys.argv[3] == "--client-key":
                agent_id = sys.argv[2]
                client_key = sys.argv[4]
                update_env_file(agent_id, client_key)
                print("\n¡Configuración completada! Ahora puedes usar el avatar completo.")

if __name__ == "__main__":
    main()
