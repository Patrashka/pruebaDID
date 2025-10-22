# 🤖 Avatar Médico Virtual con D-ID

Este proyecto integra la API de D-ID con un sistema de IA médica para crear un avatar virtual que puede conversar con pacientes y registrar hallazgos médicos importantes.

## 🚀 Características

- **Avatar Virtual**: Integración completa con D-ID para avatar médico
- **Speech-to-Text**: Conversión de audio a texto usando Whisper
- **IA Médica**: Procesamiento inteligente con Google Gemini
- **Registro de Hallazgos**: Sistema automático de detección y registro de hallazgos médicos importantes
- **Interfaz Web**: Página de demostración completa con controles de audio y chat
- **Solución Localhost**: Túnel ngrok para simular dominio permitido

## 📋 Prerrequisitos

1. **Python 3.8+**
2. **Cuenta de D-ID** con agente creado
3. **API Key de Google Gemini**
4. **ngrok** (se instala automáticamente)

## 🛠️ Instalación

### 1. Clonar e instalar dependencias

```bash
# Instalar dependencias de Python
pip install flask flask-cors python-dotenv google-generativeai openai-whisper gtts requests

# O usar requirements.txt si existe
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crea un archivo `.env` basado en `env_example.txt`:

```bash
# Google Gemini API
GOOGLE_GEMINI_API_KEY=tu_gemini_api_key_aqui

# D-ID Configuration
DID_API_KEY=tu_did_api_key_aqui
DID_AGENT_ID=tu_agent_id_aqui
DID_CLIENT_KEY=tu_client_key_aqui

# Server Configuration
PORT=8080
```

### 3. Configurar D-ID

1. Ve a [D-ID Studio](https://studio.d-id.com)
2. Crea un nuevo agente médico
3. Configura imagen, voz y personalidad
4. En la configuración del agente, agrega dominios permitidos (se configurará automáticamente)

## 🚀 Uso

### Opción 1: Configuración Automática (Recomendada)

```bash
# 1. Configurar túnel automáticamente
python setup_local_tunnel.py

# 2. En otra terminal, iniciar el servidor
python server_combined.py

# 3. Abrir medical_avatar_demo.html en el navegador
# 4. Usar la URL pública proporcionada por ngrok
```

### Opción 2: Configuración Manual

```bash
# 1. Iniciar servidor
python server_combined.py

# 2. Configurar túnel manualmente con ngrok
ngrok http 8080

# 3. Copiar la URL pública de ngrok
# 4. Agregar la URL a dominios permitidos en D-ID Studio
# 5. Abrir medical_avatar_demo.html
```

## 📱 Interfaz de Usuario

La página `medical_avatar_demo.html` incluye:

- **Sección del Avatar**: Video del avatar médico en tiempo real
- **Controles de Conexión**: Conectar/desconectar del avatar
- **Chat de Audio**: Subir archivos de audio para consultas
- **Panel de Hallazgos**: Registro automático de hallazgos médicos importantes
- **Configuración**: Campos para Client Key y Agent ID de D-ID

## 🔧 API Endpoints

### Endpoints Principales

- `POST /api/ai/did-medical-avatar` - Procesa audio y devuelve respuesta para avatar
- `GET /api/ai/medical-findings/<session_id>` - Obtiene hallazgos médicos
- `GET /api/ai/conversation/<session_id>` - Obtiene conversación completa
- `GET /api/did/config` - Devuelve configuración D-ID

### Flujo de Trabajo

1. **Usuario graba audio** con consulta médica
2. **Speech-to-Text** convierte audio a texto (Whisper)
3. **IA Médica** procesa consulta (Gemini)
4. **Análisis de Hallazgos** detecta casos importantes
5. **Avatar responde** con audio generado (D-ID)
6. **Registro automático** de hallazgos médicos

## 🏥 Sistema de Hallazgos Médicos

El sistema automáticamente:

- **Detecta síntomas graves** que requieren atención urgente
- **Identifica casos** que necesitan seguimiento médico
- **Registra timestamp** y severidad de cada hallazgo
- **Categoriza por urgencia**: Normal, Seguimiento, Urgente

### Tipos de Hallazgos

- 🟢 **NORMAL**: Consultas rutinarias sin hallazgos importantes
- 🟡 **SEGUIMIENTO**: Casos que requieren seguimiento médico
- 🔴 **URGENTE**: Síntomas que requieren atención médica inmediata

## 🔒 Seguridad y Dominios

### Problema de Localhost

D-ID requiere dominios permitidos para funcionar. La solución incluye:

1. **Túnel ngrok** que crea una URL pública
2. **Configuración automática** de dominios permitidos
3. **Proxy local** que redirige a tu servidor

### Configuración de Dominios

```bash
# El script automáticamente te dirá qué URL agregar
python setup_local_tunnel.py

# Ejemplo de URL generada:
# https://abc123.ngrok.io -> http://localhost:8080
```

## 🐛 Solución de Problemas

### Error: "Domain not allowed"

1. Verifica que agregaste la URL de ngrok a dominios permitidos en D-ID Studio
2. Asegúrate de usar la URL pública, no localhost
3. Reinicia el túnel si cambió la URL

### Error: "D-ID not configured"

1. Verifica que las variables de entorno estén configuradas
2. Confirma que el Client Key y Agent ID son correctos
3. Revisa que el agente esté activo en D-ID Studio

### Error: "Audio not processed"

1. Verifica que el archivo de audio sea compatible (WAV, MP3, etc.)
2. Asegúrate de que Whisper esté instalado correctamente
3. Revisa los logs del servidor para errores específicos

## 📊 Monitoreo y Logs

### Logs del Servidor

```bash
# El servidor muestra logs detallados
python server_combined.py

# Ejemplo de logs:
# 🧩 Inicializando modelo Gemini...
# ✅ Modelo Gemini listo para usar.
# 🔄 Procesando audio...
# 📋 Hallazgo registrado: URGENTE
```

### Archivos de Configuración

- `tunnel_config.json` - Configuración del túnel ngrok
- `.env` - Variables de entorno
- `medical_findings.json` - Hallazgos médicos (si se implementa persistencia)

## 🔮 Extensiones Futuras

- **Persistencia de datos** en base de datos
- **Múltiples avatares** médicos especializados
- **Integración con EHR** (Electronic Health Records)
- **Análisis de sentimientos** en consultas
- **Reportes automáticos** para médicos
- **API REST completa** para integración con otros sistemas

## 📞 Soporte

Para problemas específicos:

1. **D-ID**: [Documentación oficial](https://docs.d-id.com/reference/agents-sdk-overview)
2. **Google Gemini**: [Documentación de API](https://ai.google.dev/docs)
3. **Whisper**: [Documentación OpenAI](https://github.com/openai/whisper)

## 📄 Licencia

Este proyecto es para fines educativos y de demostración. Asegúrate de cumplir con los términos de servicio de todas las APIs utilizadas.
