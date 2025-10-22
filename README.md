# 🏥 Consulta Médica Virtual con D-ID Avatar

Sistema de consultas médicas virtuales que integra un avatar de D-ID con inteligencia artificial (Google Gemini) para proporcionar asistencia médica interactiva.

## 🚀 Características

- **Avatar D-ID**: Avatar virtual que habla y responde a consultas médicas
- **IA Médica**: Integración con Google Gemini para respuestas médicas inteligentes
- **Speech-to-Text**: Reconocimiento de voz para consultas por audio
- **Text-to-Speech**: Respuestas en audio del avatar
- **Reportes Médicos**: Generación automática de resúmenes de consultas
- **Interfaz Moderna**: Diseño responsive y profesional
- **Múltiples APIs**: Sistema modular con diferentes endpoints médicos

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **IA**: Google Gemini API
- **Avatar**: D-ID Studio API
- **Audio**: Whisper (STT), gTTS (TTS)
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Vercel

## 📋 Requisitos Previos

1. **Cuenta de Google Cloud** con API de Gemini habilitada
2. **Cuenta de D-ID** con avatar configurado
3. **Git** instalado
4. **Cuenta de Vercel** para deployment

## ⚙️ Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd pruebaDID
```

### 2. Configurar Variables de Entorno

Copia el archivo de plantilla y configura tus API keys:

```bash
cp env_template.txt .env
```

Edita el archivo `.env` con tus credenciales:

```env
# Google Gemini API
GOOGLE_GEMINI_API_KEY=tu_api_key_de_google_aqui

# Configuración del servidor
PORT=8080
FLASK_ENV=production

# D-ID Configuration (ya configuradas)
DID_CLIENT_KEY=Z29vZ2xlLW9hdXRoMnwxMTU1ODgzNDk4MjgyOTQ5MzYwNzM6SHFkdzdaU0gtMklRZ29Nb2Rvb0JS
DID_AGENT_ID=v2_agt_gRs4QB2l
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar D-ID

1. Ve a [D-ID Studio](https://studio.d-id.com/)
2. Asegúrate de que tu avatar esté configurado
3. Verifica que el dominio de Vercel esté en "Allowed Origins"

## 🚀 Deployment en Vercel

### 1. Conectar con GitHub

1. Ve a [Vercel](https://vercel.com/)
2. Conecta tu cuenta de GitHub
3. Importa tu repositorio

### 2. Configurar Variables de Entorno en Vercel

En el dashboard de Vercel, ve a Settings > Environment Variables y agrega:

- `GOOGLE_GEMINI_API_KEY`: Tu API key de Google Gemini
- `FLASK_ENV`: `production`

### 3. Deploy

Vercel detectará automáticamente la configuración y desplegará la aplicación.

## 📱 Uso del Sistema

### Interfaz Principal

1. **Avatar D-ID**: Se carga automáticamente en la sección izquierda
2. **Chat**: Interfaz de conversación en la sección derecha
3. **Reporte Médico**: Resumen automático de la consulta

### Funcionalidades

- **Consulta por Texto**: Escribe tu consulta médica
- **Consulta por Voz**: Usa el botón de micrófono para grabar
- **Respuesta del Avatar**: El avatar D-ID responde con voz y texto
- **Reporte Automático**: Se genera un resumen médico de la consulta

## 🔧 APIs Disponibles

El sistema incluye múltiples endpoints médicos:

### Consultas Básicas
- `POST /api/ai/patient` - Consulta para pacientes
- `POST /api/ai/doctor` - Consulta para doctores

### Audio y Voz
- `POST /api/ai/speech-to-text` - Convertir audio a texto
- `POST /api/ai/text-to-speech` - Convertir texto a audio
- `POST /api/ai/voice-session` - Flujo completo de voz

### Análisis de Archivos
- `POST /api/ai/file/analyze_json` - Analizar archivos médicos
- `POST /api/ai/file/analyze_xml` - Analizar archivos (XML)

### Interacciones Avanzadas
- `POST /api/ai/interaction` - Conversación con memoria
- `POST /api/ai/conclusion` - Resumen final de consulta

## 🎯 Flujo de Trabajo

1. **Usuario inicia consulta** (texto o voz)
2. **Sistema procesa input** (STT si es audio)
3. **IA genera respuesta** (Google Gemini)
4. **Avatar responde** (D-ID + TTS)
5. **Reporte se actualiza** (resumen médico)

## 🔒 Seguridad y Privacidad

- **HTTPS obligatorio** para D-ID
- **Variables de entorno** para API keys
- **Validación de input** en frontend y backend
- **Advertencias médicas** incluidas en la interfaz

## 🐛 Solución de Problemas

### Avatar D-ID no carga
- Verifica que el dominio esté en "Allowed Origins" en D-ID
- Confirma que las credenciales sean correctas
- Revisa la consola del navegador para errores

### Error en consultas IA
- Verifica que `GOOGLE_GEMINI_API_KEY` esté configurada
- Confirma que la API key sea válida
- Revisa los logs de Vercel

### Problemas de audio
- Verifica permisos de micrófono en el navegador
- Confirma que el navegador soporte Web Speech API
- Revisa la consola para errores de audio

## 📊 Monitoreo

- **Logs de Vercel**: Revisa el dashboard para errores
- **Consola del navegador**: Para errores de frontend
- **Network tab**: Para problemas de API

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## ⚠️ Disclaimer Médico

**IMPORTANTE**: Este sistema es solo para orientación médica y no sustituye una consulta médica profesional. Siempre consulta con un médico calificado para diagnósticos y tratamientos.

## 📞 Soporte

Para soporte técnico o preguntas sobre el sistema, contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ usando D-ID Avatar y Google Gemini AI**
