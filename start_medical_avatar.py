#!/usr/bin/env python3
"""
Script de inicio rápido para el Avatar Médico Virtual con D-ID
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = [
        'flask', 'flask_cors', 'python-dotenv', 
        'google-generativeai', 'openai-whisper', 'gtts', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Faltan dependencias:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Instalando dependencias...")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, check=True)
            print("✅ Dependencias instaladas correctamente")
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias")
            print("💡 Instala manualmente: pip install " + " ".join(missing_packages))
            return False
    
    return True

def check_env_file():
    """Verifica que el archivo .env esté configurado"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ Archivo .env no encontrado")
        print("📝 Creando archivo .env desde ejemplo...")
        
        try:
            with open('env_example.txt', 'r') as example:
                content = example.read()
            
            with open('.env', 'w') as env:
                env.write(content)
            
            print("✅ Archivo .env creado")
            print("⚠️  IMPORTANTE: Configura las variables en .env antes de continuar")
            return False
        except FileNotFoundError:
            print("❌ Archivo env_example.txt no encontrado")
            return False
    
    # Verificar que las variables estén configuradas
    with open('.env', 'r') as f:
        content = f.read()
    
    required_vars = ['GOOGLE_GEMINI_API_KEY', 'DID_API_KEY', 'DID_AGENT_ID', 'DID_CLIENT_KEY']
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=tu_" in content or f"{var}=" not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Variables no configuradas en .env:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Configura estas variables antes de continuar")
        return False
    
    return True

def start_server():
    """Inicia el servidor Flask"""
    print("🚀 Iniciando servidor Flask...")
    
    try:
        # Iniciar servidor en background
        process = subprocess.Popen([sys.executable, 'server_combined.py'])
        
        # Esperar a que el servidor se inicie
        time.sleep(3)
        
        print("✅ Servidor iniciado en http://localhost:8080")
        return process
        
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return None

def start_tunnel():
    """Inicia el túnel ngrok"""
    print("🌐 Configurando túnel ngrok...")
    
    try:
        # Verificar si ngrok está instalado
        subprocess.run(['ngrok', 'version'], check=True, capture_output=True)
        
        # Iniciar túnel
        tunnel_process = subprocess.Popen(['ngrok', 'http', '8080', '--log=stdout'])
        
        # Esperar a que ngrok se inicie
        time.sleep(5)
        
        # Obtener URL pública
        try:
            import requests
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            tunnels = response.json()
            
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"✅ Túnel creado: {public_url}")
                print(f"📝 Agrega esta URL a los dominios permitidos en D-ID Studio")
                return public_url, tunnel_process
            else:
                print("❌ No se pudo obtener la URL del túnel")
                return None, tunnel_process
                
        except Exception as e:
            print(f"⚠️  No se pudo obtener URL automáticamente: {e}")
            print("💡 Ve a http://localhost:4040 para ver la URL del túnel")
            return None, tunnel_process
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ngrok no está instalado")
        print("💡 Instala ngrok desde: https://ngrok.com/download")
        return None, None

def open_demo_page():
    """Abre la página de demostración"""
    demo_file = Path('medical_avatar_demo.html')
    
    if demo_file.exists():
        print("🌐 Abriendo página de demostración...")
        webbrowser.open(f'file://{demo_file.absolute()}')
        print("✅ Página abierta en el navegador")
    else:
        print("❌ Archivo medical_avatar_demo.html no encontrado")

def main():
    print("🤖 AVATAR MÉDICO VIRTUAL - INICIO RÁPIDO")
    print("=" * 50)
    
    # 1. Verificar dependencias
    print("1️⃣ Verificando dependencias...")
    if not check_dependencies():
        return
    
    # 2. Verificar configuración
    print("\n2️⃣ Verificando configuración...")
    if not check_env_file():
        print("\n⚠️  Configura el archivo .env y ejecuta este script nuevamente")
        return
    
    # 3. Iniciar servidor
    print("\n3️⃣ Iniciando servidor...")
    server_process = start_server()
    if not server_process:
        return
    
    # 4. Configurar túnel
    print("\n4️⃣ Configurando túnel...")
    public_url, tunnel_process = start_tunnel()
    
    # 5. Abrir página de demostración
    print("\n5️⃣ Abriendo página de demostración...")
    open_demo_page()
    
    # 6. Mostrar información final
    print("\n" + "=" * 50)
    print("🎉 SISTEMA INICIADO EXITOSAMENTE")
    print("=" * 50)
    print("📱 Página de demostración: medical_avatar_demo.html")
    print("🔧 Servidor: http://localhost:8080")
    if public_url:
        print(f"🌐 URL Pública: {public_url}")
        print("📝 IMPORTANTE: Agrega la URL pública a D-ID Studio")
    print("\n🔄 Presiona Ctrl+C para detener todos los servicios")
    
    try:
        # Mantener el script activo
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servicios...")
        
        if server_process:
            server_process.terminate()
            print("✅ Servidor detenido")
        
        if tunnel_process:
            tunnel_process.terminate()
            print("✅ Túnel detenido")
        
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main()
