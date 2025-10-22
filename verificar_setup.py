#!/usr/bin/env python3
"""
Script de verificación para el sistema de Consulta Médica Virtual
Verifica que todas las dependencias y configuraciones estén correctas
"""

import os
import sys
import importlib
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_status(item, status, details=""):
    """Imprime el estado de un elemento"""
    status_icon = "[OK]" if status else "[ERROR]"
    print(f"{status_icon} {item}")
    if details:
        print(f"   {details}")

def check_file_exists(filepath, description):
    """Verifica si un archivo existe"""
    exists = Path(filepath).exists()
    print_status(description, exists, filepath if exists else f"Archivo no encontrado: {filepath}")
    return exists

def check_python_packages():
    """Verifica que los paquetes de Python estén instalados"""
    print_header("VERIFICACIÓN DE PAQUETES PYTHON")
    
    required_packages = [
        'flask',
        'flask_cors', 
        'google.generativeai',
        'python_dotenv',
        'requests',
        'whisper',
        'gtts',
        'PIL'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            if package == 'google.generativeai':
                import google.generativeai as genai
            elif package == 'flask_cors':
                import flask_cors
            elif package == 'python_dotenv':
                import dotenv
            elif package == 'PIL':
                from PIL import Image
            else:
                importlib.import_module(package)
            print_status(f"Paquete {package}", True)
        except ImportError:
            print_status(f"Paquete {package}", False, "No instalado")
            all_installed = False
    
    return all_installed

def check_environment_variables():
    """Verifica las variables de entorno"""
    print_header("VERIFICACIÓN DE VARIABLES DE ENTORNO")
    
    # Cargar variables del archivo .env si existe
    env_file = Path('.env')
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print_status("Archivo .env", True, "Variables cargadas")
    else:
        print_status("Archivo .env", False, "Crea el archivo .env desde env_template.txt")
    
    # Verificar variables críticas
    google_key = os.getenv('GOOGLE_GEMINI_API_KEY')
    print_status("GOOGLE_GEMINI_API_KEY", bool(google_key), 
                f"Configurada: {google_key[:8]}..." if google_key else "No configurada")
    
    flask_env = os.getenv('FLASK_ENV', 'development')
    print_status("FLASK_ENV", True, f"Valor: {flask_env}")
    
    return bool(google_key)

def check_project_structure():
    """Verifica la estructura del proyecto"""
    print_header("VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
    
    required_files = [
        ('server_combined.py', 'Servidor principal Flask'),
        ('requirements.txt', 'Dependencias de Python'),
        ('vercel.json', 'Configuración de Vercel'),
        ('wsgi.py', 'Entry point para Vercel'),
        ('runtime.txt', 'Versión de Python para Vercel'),
        ('README.md', 'Documentación del proyecto'),
        ('env_template.txt', 'Plantilla de variables de entorno')
    ]
    
    required_dirs = [
        ('templates/', 'Plantillas HTML'),
        ('static/', 'Archivos estáticos (CSS, JS)')
    ]
    
    all_files_ok = True
    
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_files_ok = False
    
    for dirpath, description in required_dirs:
        if not check_file_exists(dirpath, description):
            all_files_ok = False
    
    return all_files_ok

def check_did_configuration():
    """Verifica la configuración de D-ID"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN D-ID")
    
    # Verificar que las credenciales estén en el HTML
    html_file = Path('templates/index.html')
    if html_file.exists():
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_client_key = 'Z29vZ2xlLW9hdXRoMnwxMTU1ODgzNDk4MjgyOTQ5MzYwNzM6SHFkdzdaU0gtMklRZ29Nb2Rvb0JS' in content
        has_agent_id = 'v2_agt_gRs4QB2l' in content
        has_script = 'agent.d-id.com' in content
        
        print_status("Client Key D-ID", has_client_key)
        print_status("Agent ID D-ID", has_agent_id)
        print_status("Script D-ID", has_script)
        
        return has_client_key and has_agent_id and has_script
    else:
        print_status("Archivo HTML", False, "templates/index.html no encontrado")
        return False

def test_gemini_connection():
    """Prueba la conexión con Google Gemini"""
    print_header("PRUEBA DE CONEXIÓN CON GEMINI")
    
    try:
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            print_status("Conexión Gemini", False, "API key no configurada")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Prueba simple
        response = model.generate_content("Di hola")
        if response.text:
            print_status("Conexión Gemini", True, f"Respuesta: {response.text[:50]}...")
            return True
        else:
            print_status("Conexión Gemini", False, "Sin respuesta del modelo")
            return False
            
    except Exception as e:
        print_status("Conexión Gemini", False, f"Error: {str(e)}")
        return False

def main():
    """Función principal de verificación"""
    print_header("VERIFICACIÓN DEL SISTEMA DE CONSULTA MÉDICA VIRTUAL")
    print("Este script verifica que todo esté configurado correctamente para el deployment")
    
    checks = [
        ("Paquetes Python", check_python_packages),
        ("Variables de Entorno", check_environment_variables),
        ("Estructura del Proyecto", check_project_structure),
        ("Configuración D-ID", check_did_configuration),
        ("Conexión Gemini", test_gemini_connection)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"[ERROR] Error en {check_name}: {e}")
            results.append((check_name, False))
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    all_passed = True
    for check_name, result in results:
        print_status(check_name, result)
        if not result:
            all_passed = False
    
    print(f"\n{'='*60}")
    if all_passed:
        print("[SUCCESS] ¡TODAS LAS VERIFICACIONES PASARON!")
        print("[OK] El sistema está listo para deployment en Vercel")
        print("\nPróximos pasos:")
        print("1. Haz commit y push de tus cambios a GitHub")
        print("2. Conecta tu repositorio con Vercel")
        print("3. Configura las variables de entorno en Vercel")
        print("4. Deploy!")
    else:
        print("[WARNING] ALGUNAS VERIFICACIONES FALLARON")
        print("[ERROR] Revisa los errores arriba antes de hacer deployment")
        print("\nPasos para corregir:")
        print("1. Instala las dependencias faltantes: pip install -r requirements.txt")
        print("2. Crea el archivo .env desde env_template.txt")
        print("3. Configura tu GOOGLE_GEMINI_API_KEY")
        print("4. Ejecuta este script nuevamente")
    
    print(f"{'='*60}\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
