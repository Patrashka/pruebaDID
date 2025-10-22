#!/usr/bin/env python3
"""
Script para configurar un túnel local que simule un dominio permitido para D-ID
Esto resuelve el problema de localhost con D-ID API
"""

import subprocess
import sys
import time
import requests
import json
from urllib.parse import urlparse

def install_ngrok():
    """Instala ngrok si no está disponible"""
    try:
        subprocess.run(['ngrok', 'version'], check=True, capture_output=True)
        print("✅ ngrok ya está instalado")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Instalando ngrok...")
        try:
            # Para Windows
            if sys.platform == "win32":
                subprocess.run(['winget', 'install', 'ngrok.ngrok'], check=True)
            # Para macOS
            elif sys.platform == "darwin":
                subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], check=True)
            # Para Linux
            else:
                subprocess.run(['curl', '-s', 'https://ngrok-agent.s3.amazonaws.com/ngrok.asc', '|', 'sudo', 'tee', '/etc/apt/trusted.gpg.d/ngrok.asc', '>', '/dev/null'], shell=True)
                subprocess.run(['echo', '"deb https://ngrok-agent.s3.amazonaws.com buster main"', '|', 'sudo', 'tee', '/etc/apt/sources.list.d/ngrok.list'], shell=True)
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', 'ngrok'], check=True)
            
            print("✅ ngrok instalado correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando ngrok: {e}")
            print("📝 Instala ngrok manualmente desde: https://ngrok.com/download")
            return False

def start_ngrok_tunnel(port=8080):
    """Inicia un túnel ngrok para el puerto especificado"""
    try:
        print(f"🚀 Iniciando túnel ngrok para puerto {port}...")
        
        # Iniciar ngrok en background
        process = subprocess.Popen(
            ['ngrok', 'http', str(port), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Esperar a que ngrok se inicie
        time.sleep(3)
        
        # Obtener la URL del túnel
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            tunnels = response.json()
            
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ Túnel creado: {public_url}")
                return public_url, process
            else:
                print("❌ No se pudo obtener la URL del túnel")
                return None, process
                
        except requests.RequestException:
            print("❌ No se pudo conectar a la API de ngrok")
            return None, process
            
    except Exception as e:
        print(f"❌ Error iniciando túnel: {e}")
        return None, None

def update_did_domains(public_url, api_key):
    """Actualiza los dominios permitidos en D-ID (esto requeriría API de D-ID)"""
    print(f"📝 IMPORTANTE: Agrega este dominio a tu configuración de D-ID:")
    print(f"   {public_url}")
    print(f"   Ve a D-ID Studio > Tu Agente > Configuración > Dominios Permitidos")
    print(f"   Agrega: {public_url}")

def create_local_proxy_config(public_url):
    """Crea un archivo de configuración para el proxy local"""
    config = {
        "public_url": public_url,
        "local_port": 8080,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "instructions": [
            "1. Agrega la URL pública a los dominios permitidos en D-ID Studio",
            "2. Usa esta URL en lugar de localhost en tu aplicación",
            "3. El túnel redirigirá automáticamente a tu servidor local"
        ]
    }
    
    with open('tunnel_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("📄 Configuración guardada en tunnel_config.json")

def main():
    print("🔧 Configurando túnel local para D-ID...")
    print("=" * 50)
    
    # Verificar/instalar ngrok
    if not install_ngrok():
        return
    
    # Obtener puerto del servidor
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("❌ Puerto inválido, usando 8080")
    
    # Iniciar túnel
    public_url, ngrok_process = start_ngrok_tunnel(port)
    
    if public_url:
        print("\n" + "=" * 50)
        print("🎉 TÚNEL CONFIGURADO EXITOSAMENTE")
        print("=" * 50)
        print(f"URL Pública: {public_url}")
        print(f"URL Local: http://localhost:{port}")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Agrega la URL pública a los dominios permitidos en D-ID Studio")
        print("2. Actualiza tu archivo .env con las credenciales de D-ID")
        print("3. Inicia tu servidor Flask: python server_combined.py")
        print("4. Abre medical_avatar_demo.html en tu navegador")
        print("5. Usa la URL pública en lugar de localhost")
        
        # Crear configuración
        create_local_proxy_config(public_url)
        
        print(f"\n🔄 Túnel activo. Presiona Ctrl+C para detener.")
        
        try:
            # Mantener el proceso activo
            ngrok_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo túnel...")
            ngrok_process.terminate()
            print("✅ Túnel detenido")
    else:
        print("❌ No se pudo crear el túnel")

if __name__ == "__main__":
    main()
