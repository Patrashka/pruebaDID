# 🏥 Asistente Médico Virtual con D-ID Avatar

Aplicación web con avatar médico interactivo usando D-ID, inteligencia artificial (Google Gemini), reconocimiento de voz y generación automática de reportes.

## 🚀 Características

- 🤖 **Avatar Médico Interactivo** (D-ID Agent)
- 🧠 **IA Google Gemini** para respuestas médicas
- 🎤 **Speech-to-Text** en español
- 📋 **Reportes automáticos** descargables
- 📜 **Historial de consultas**
- 💻 **Interfaz moderna** y responsive

## ⚡ Inicio Rápido

### 1. Clonar e Instalar

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/pruebaDID.git
cd pruebaDID

# Crear entorno virtual e instalar dependencias
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configurar API Key

1. Obtén tu API key de Google Gemini: https://makersuite.google.com/app/apikey
2. Crea archivo `.env` en la raíz:

```env
GOOGLE_API_KEY=tu_api_key_aqui
GEMINI_MODEL=gemini-pro
FLASK_ENV=development
PORT=5000
```

### 3. Ejecutar

```bash
# Windows
run.bat

# Linux/Mac o manual
python app.py
```

Abre tu navegador en: `http://localhost:5000`

## 🌐 Deploy en Vercel (Recomendado)

**¿Por qué Vercel?** HTTPS automático (requerido para D-ID y reconocimiento de voz)

### Pasos:

1. **Push a GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **En Vercel:**
   - Ve a https://vercel.com
   - Importa tu repositorio de GitHub
   - Configura variables de entorno:
     - `GOOGLE_API_KEY` = tu_api_key
     - `FLASK_ENV` = production
     - `GEMINI_MODEL` = gemini-pro
   - Click "Deploy"

3. **¡Listo!** Tu app estará en `https://tu-proyecto.vercel.app` con HTTPS automático

**Guía detallada:** Ver [DEPLOYMENT_VERCEL.md](DEPLOYMENT_VERCEL.md)

## 📖 Uso

### Consulta por Texto
1. Escribe tu síntoma o consulta médica
2. Click en "Enviar Consulta"
3. El avatar responderá visualmente

### Consulta por Voz
1. Click en el botón de micrófono 🎤
2. Habla claramente (requiere HTTPS en producción)
3. El texto se transcribirá automáticamente
4. Click "Enviar"

### Ver Reportes
- Click en "Ver Reporte Detallado" después de cada consulta
- Descarga el reporte en formato texto
- Revisa el historial en el sidebar lateral

## 🛠️ Tecnologías

- **Backend:** Python, Flask
- **IA:** Google Gemini Pro
- **Avatar:** D-ID Agent SDK
- **Frontend:** HTML5, CSS3, JavaScript (Web Speech API)
- **Deployment:** Vercel

## 📁 Estructura del Proyecto

```
pruebaDID/
├── app.py                 # Backend Flask
├── config.py              # Configuración
├── templates/             # HTML
│   └── index.html
├── static/                # CSS y JS
│   ├── styles.css
│   └── app.js
├── reportes/              # Reportes generados
├── vercel.json            # Config Vercel
├── requirements.txt       # Dependencias
└── .env                   # Variables (crear manualmente)
```

## 🔧 Scripts Disponibles

### Windows:
- `setup_venv.bat` - Configurar entorno automáticamente
- `run.bat` - Ejecutar la aplicación

### Todos:
- `python app.py` - Iniciar servidor

## 🐛 Solución de Problemas

### Error: "GOOGLE_API_KEY not found"
- Verifica que el archivo `.env` existe
- Verifica que la API key es correcta

### El avatar no carga
- Verifica tu conexión a internet
- En producción, asegúrate de usar HTTPS (Vercel lo provee)

### El reconocimiento de voz no funciona
- Requiere HTTPS (usa Vercel para deployment)
- Usa Chrome o Edge
- Permite acceso al micrófono

### Error al hacer consultas
- Verifica que tu API key de Google Gemini es válida
- Verifica que tienes crédito disponible en Google AI Studio

## ⚠️ Importante

Este sistema es **solo para fines informativos y educativos**. No proporciona diagnósticos médicos reales ni debe usarse como sustituto de la atención médica profesional. Siempre consulta con un profesional de la salud calificado.

## 📝 Licencia

MIT License - Ver [LICENSE](LICENSE)

## 🔗 Enlaces Útiles

- [Google AI Studio](https://makersuite.google.com/app/apikey) - Obtener API key
- [Vercel](https://vercel.com) - Deploy gratuito con HTTPS
- [D-ID Documentation](https://docs.d-id.com/) - Info sobre el avatar
- [Deployment Guide](DEPLOYMENT_VERCEL.md) - Guía detallada de Vercel

---

**¿Preguntas?** Revisa [DEPLOYMENT_VERCEL.md](DEPLOYMENT_VERCEL.md) para más detalles.

**¡Desarrollado para ayudar con consultas médicas preliminares! 🏥✨**
