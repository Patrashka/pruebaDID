"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Puerto
    PORT = int(os.getenv('PORT', 5000))
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # D-ID
    DID_CLIENT_KEY = os.getenv('DID_CLIENT_KEY', 'Z29vZ2xlLW9hdXRoMnwxMTU1ODgzNDk4MjgyOTQ5MzYwNzM6SHFkdzdaU0gtMklRZ29Nb2Rvb0JS')
    DID_AGENT_ID = os.getenv('DID_AGENT_ID', 'v2_agt_gRs4QB2l')
    
    # Directorios
    REPORTES_DIR = 'reportes'
    TEMPLATES_DIR = 'templates'
    STATIC_DIR = 'static'
    
    # Configuración de reportes
    MAX_REPORTES_HISTORIAL = int(os.getenv('MAX_REPORTES_HISTORIAL', 10))
    
    # Configuración de IA
    MAX_TOKENS_RESPUESTA = int(os.getenv('MAX_TOKENS_RESPUESTA', 500))
    MAX_TOKENS_REPORTE = int(os.getenv('MAX_TOKENS_REPORTE', 400))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    
    @staticmethod
    def validate():
        """Valida que las configuraciones críticas estén presentes"""
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY no está configurada. Por favor, crea un archivo .env con tu API key.")
        
        # Crear directorio de reportes si no existe
        if not os.path.exists(Config.REPORTES_DIR):
            os.makedirs(Config.REPORTES_DIR)
            print(f"✓ Directorio '{Config.REPORTES_DIR}' creado")

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configuración para testing"""
    DEBUG = True
    TESTING = True
    OPENAI_API_KEY = 'test-key'

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtiene la configuración según el entorno"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])

