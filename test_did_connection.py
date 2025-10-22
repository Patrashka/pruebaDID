#!/usr/bin/env python3
"""
Script para probar la conexión con D-ID y obtener información del agente
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración D-ID
DID_API_KEY = os.getenv("DID_API_KEY")
DID_BASE_URL = "https://api.d-id.com"

def test_did_connection():
    """Prueba la conexión con D-ID API"""
    print("Probando conexión con D-ID API...")
    
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Probar endpoint de agentes
        response = requests.get(f"{DID_BASE_URL}/agents", headers=headers)
        
        if response.status_code == 200:
            agents = response.json()
            print("Conexión exitosa con D-ID!")
            print(f"Agentes encontrados: {len(agents.get('agents', []))}")
            
            if agents.get('agents'):
                print("\nAgentes disponibles:")
                for i, agent in enumerate(agents['agents']):
                    print(f"  {i+1}. ID: {agent.get('id')}")
                    print(f"     Nombre: {agent.get('name', 'Sin nombre')}")
                    print(f"     Estado: {agent.get('status', 'Desconocido')}")
                    print()
            else:
                print("No hay agentes creados. Necesitas crear uno en D-ID Studio.")
                print("Ve a: https://studio.d-id.com")
                
        else:
            print(f"Error en la conexión: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"Error al conectar con D-ID: {e}")

def get_agent_details(agent_id):
    """Obtiene detalles de un agente específico"""
    headers = {
        "Authorization": f"Basic {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{DID_BASE_URL}/agents/{agent_id}", headers=headers)
        
        if response.status_code == 200:
            agent = response.json()
            print(f"\nDetalles del agente {agent_id}:")
            print(f"  Nombre: {agent.get('name')}")
            print(f"  Estado: {agent.get('status')}")
            print(f"  Presenter: {agent.get('presenter', {}).get('id')}")
            print(f"  Voice: {agent.get('voice', {}).get('id')}")
            return agent
        else:
            print(f"Error obteniendo agente: {response.status_code}")
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    return None

def main():
    print("D-ID CONNECTION TESTER")
    print("=" * 40)
    
    if not DID_API_KEY:
        print("Error: No se encontró DID_API_KEY en el archivo .env")
        return
    
    print(f"API Key configurada: {DID_API_KEY[:20]}...")
    
    # Probar conexión
    test_did_connection()
    
    # Si hay agentes, mostrar opción de obtener detalles
    print("\n" + "=" * 40)
    print("Para obtener el Client Key:")
    print("1. Ve a D-ID Studio: https://studio.d-id.com")
    print("2. Selecciona tu agente")
    print("3. Ve a la sección 'Embed' o 'Integration'")
    print("4. Copia el 'data-client-key' y 'data-agent-id'")
    print("5. Actualiza el archivo .env con esos valores")

if __name__ == "__main__":
    main()
