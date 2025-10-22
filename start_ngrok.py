#!/usr/bin/env python3
"""
Script simplificado para iniciar ngrok
"""

import subprocess
import time
import requests
import sys

def start_ngrok():
    """Inicia ngrok para el puerto 8080"""
    print("Iniciando ngrok para puerto 8080...")
    
    try:
        # Iniciar ngrok
        process = subprocess.Popen(['ngrok', 'http', '8080', '--log=stdout'])
        
        # Esperar a que ngrok se inicie
        time.sleep(5)
        
        # Obtener URL pública
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            tunnels = response.json()
            
            if tunnels['tunnels']:
                public_url = tunnels['tunnels'][0]['public_url']
                print(f"Tunel creado: {public_url}")
                print(f"Agrega esta URL a los dominios permitidos en D-ID Studio")
                print(f"Luego usa esta URL en lugar de localhost")
                return public_url, process
            else:
                print("No se pudo obtener la URL del tunel")
                return None, process
                
        except Exception as e:
            print(f"No se pudo obtener URL automaticamente: {e}")
            print("Ve a http://localhost:4040 para ver la URL del tunel")
            return None, process
            
    except FileNotFoundError:
        print("ngrok no esta instalado")
        print("Instala ngrok desde: https://ngrok.com/download")
        return None, None

def main():
    print("NGROK TUNNEL SETUP")
    print("=" * 30)
    
    public_url, ngrok_process = start_ngrok()
    
    if public_url:
        print("\n" + "=" * 50)
        print("TUNEL CONFIGURADO EXITOSAMENTE")
        print("=" * 50)
        print(f"URL Publica: {public_url}")
        print(f"URL Local: http://localhost:8080")
        print("\nPROXIMOS PASOS:")
        print("1. Agrega la URL publica a los dominios permitidos en D-ID Studio")
        print("2. Usa la URL publica en lugar de localhost")
        print("3. Presiona Ctrl+C para detener")
        
        try:
            # Mantener el proceso activo
            ngrok_process.wait()
        except KeyboardInterrupt:
            print("\nDeteniendo tunel...")
            ngrok_process.terminate()
            print("Tunel detenido")
    else:
        print("No se pudo crear el tunel")

if __name__ == "__main__":
    main()
