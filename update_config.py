#!/usr/bin/env python3
"""
Script para actualizar la configuración con Agent ID y Client Key
"""

def update_config():
    print("ACTUALIZAR CONFIGURACION D-ID")
    print("=" * 40)
    print("Para obtener el Agent ID y Client Key:")
    print("1. Ve a https://studio.d-id.com")
    print("2. Selecciona uno de tus agentes")
    print("3. Busca la seccion 'Embed' o 'Integration'")
    print("4. Copia el 'data-agent-id' y 'data-client-key'")
    print()
    print("Luego ejecuta:")
    print("python get_agent_details.py --agent-id TU_AGENT_ID --client-key TU_CLIENT_KEY")
    print()
    print("O edita manualmente el archivo .env con:")
    print("DID_AGENT_ID=tu_agent_id_aqui")
    print("DID_CLIENT_KEY=tu_client_key_aqui")

if __name__ == "__main__":
    update_config()
