# 🚀 Guía de Deployment en Vercel

Esta guía te ayudará a desplegar tu Asistente Médico Virtual en Vercel con HTTPS automático.

---

## 📋 Prerrequisitos

- ✅ Cuenta de GitHub
- ✅ Cuenta de Vercel (https://vercel.com)
- ✅ API Key de Google Gemini
- ✅ Proyecto funcionando localmente

---

## 🔧 PASO 1: Preparar el Repositorio en GitHub

### 1.1 Crear Repositorio (Si no existe)

```bash
# Inicializar Git en tu proyecto
git init

# Añadir todos los archivos
git add .

# Hacer commit inicial
git commit -m "Initial commit: Asistente Médico D-ID con Google Gemini"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 1.2 Verificar que .gitignore está correcto

Asegúrate de que estos archivos NO se suban a GitHub:
```
venv/
.env
__pycache__/
reportes/*.json
*.log
```

El archivo `.gitignore` ya está configurado correctamente.

---

## 🌐 PASO 2: Configurar Vercel

### 2.1 Crear Proyecto en Vercel

1. Ve a https://vercel.com y haz login
2. Click en **"Add New Project"**
3. Selecciona **"Import Git Repository"**
4. Autoriza a Vercel para acceder a tu GitHub
5. Selecciona tu repositorio `pruebaDID`
6. Click en **"Import"**

### 2.2 Configurar Variables de Entorno

En la página de configuración del proyecto:

1. Ve a **"Environment Variables"**
2. Añade las siguientes variables:

```
GOOGLE_API_KEY = tu_google_api_key_aqui
FLASK_ENV = production
GEMINI_MODEL = gemini-pro
DID_CLIENT_KEY = Z29vZ2xlLW9hdXRoMnwxMTU1ODgzNDk4MjgyOTQ5MzYwNzM6SHFkdzdaU0gtMklRZ29Nb2Rvb0JS
DID_AGENT_ID = v2_agt_gRs4QB2l
```

**IMPORTANTE**: 
- Marca todas como disponibles para todos los entornos
- NO compartas tu GOOGLE_API_KEY públicamente

### 2.3 Configuración del Build

Vercel detectará automáticamente que es un proyecto Python.

Si necesitas configurar manualmente:
- **Framework Preset**: Other
- **Build Command**: (dejar vacío)
- **Output Directory**: (dejar vacío)
- **Install Command**: `pip install -r requirements.txt`

### 2.4 Deploy

1. Click en **"Deploy"**
2. Espera a que termine el build (2-3 minutos)
3. ¡Listo! Tu app estará disponible en `https://tu-proyecto.vercel.app`

---

## ✅ PASO 3: Verificar el Deployment

### 3.1 Probar la Aplicación

1. Abre tu URL de Vercel: `https://tu-proyecto.vercel.app`
2. Verifica que el avatar D-ID carga correctamente
3. Haz una consulta de prueba por texto
4. Prueba el reconocimiento de voz (requiere HTTPS ✅)
5. Verifica que se genera el reporte

### 3.2 Revisar Logs

Si hay errores:
1. Ve al Dashboard de Vercel
2. Selecciona tu proyecto
3. Click en **"Deployments"**
4. Click en el deployment más reciente
5. Ve a **"Logs"** para ver errores

---

## 🔄 PASO 4: Configurar Deploy Automático

### 4.1 Deploy en cada Push

Vercel ya está configurado para hacer deploy automático:

```bash
# Hacer cambios en tu código local
git add .
git commit -m "Descripción de cambios"
git push origin main

# Vercel detectará el push y hará deploy automáticamente
```

### 4.2 Deploy en Ramas Específicas

Por defecto, Vercel hace deploy de:
- `main` → Producción
- Otras ramas → Preview deployments

Puedes configurar esto en:
**Settings → Git → Production Branch**

---

## 🎯 PASO 5: Dominio Personalizado (Opcional)

### 5.1 Usar tu Propio Dominio

1. Ve a **Settings → Domains**
2. Click en **"Add Domain"**
3. Ingresa tu dominio (ej: `asistente-medico.com`)
4. Sigue las instrucciones para configurar DNS
5. Vercel proveerá SSL/HTTPS automáticamente

---

## 🔒 Seguridad en Producción

### Variables de Entorno

✅ **Nunca** hagas commit de `.env`
✅ Usa las variables de entorno de Vercel
✅ Regenera tu API key si se expone

### HTTPS

✅ Vercel provee HTTPS automáticamente
✅ D-ID requiere HTTPS para funcionar
✅ El reconocimiento de voz requiere HTTPS

### CORS

El proyecto ya tiene CORS configurado en `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

---

## 🐛 Solución de Problemas

### Error: "GOOGLE_API_KEY not found"

**Solución:**
1. Ve a Vercel Dashboard → Tu Proyecto → Settings → Environment Variables
2. Verifica que `GOOGLE_API_KEY` está configurada
3. Redeploy el proyecto

### Error: "Module not found"

**Solución:**
1. Verifica que `requirements.txt` está correcto
2. Asegúrate de que `vercel.json` está en la raíz
3. Revisa los logs de build en Vercel

### El avatar D-ID no carga

**Solución:**
1. Verifica que las credenciales D-ID están en las variables de entorno
2. Abre la consola del navegador (F12) para ver errores
3. Verifica que estás usando HTTPS (Vercel lo provee automáticamente)

### Reconocimiento de voz no funciona

**Solución:**
1. Verifica que estás usando HTTPS (✅ con Vercel)
2. Usa Chrome o Edge
3. Permite acceso al micrófono

### Error 500 al hacer consultas

**Solución:**
1. Revisa los logs en Vercel
2. Verifica que tu API key de Google Gemini es válida
3. Verifica que tienes crédito/cuota disponible en Google AI Studio

---

## 📊 Monitoreo y Analytics

### Ver Estadísticas

Vercel provee analytics automáticamente:
1. Dashboard → Tu Proyecto → Analytics
2. Verás:
   - Visitas
   - Performance
   - Errores
   - Geografía de usuarios

### Logs en Tiempo Real

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Ver logs en tiempo real
vercel logs
```

---

## 🔄 Workflow de Desarrollo Recomendado

### Desarrollo Local → GitHub → Vercel

```bash
# 1. Hacer cambios localmente
# Editar código...

# 2. Probar localmente
python app.py
# Abrir http://localhost:5000

# 3. Commit y push
git add .
git commit -m "Mejorar sistema de reportes"
git push origin main

# 4. Vercel detecta el push y hace deploy automático
# Esperar 2-3 minutos

# 5. Verificar en producción
# Abrir https://tu-proyecto.vercel.app
```

### Usar Ramas para Testing

```bash
# Crear rama de feature
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commit
git add .
git commit -m "Add nueva funcionalidad"
git push origin feature/nueva-funcionalidad

# Vercel creará un preview deployment
# URL: https://tu-proyecto-git-feature-nueva-funcionalidad.vercel.app

# Si funciona bien, hacer merge a main
git checkout main
git merge feature/nueva-funcionalidad
git push origin main
```

---

## 🎉 Checklist de Deployment

- [ ] Repositorio en GitHub creado y pusheado
- [ ] Cuenta de Vercel creada
- [ ] Proyecto importado en Vercel
- [ ] Variables de entorno configuradas en Vercel
- [ ] Primer deployment exitoso
- [ ] URL de producción funciona
- [ ] Avatar D-ID carga correctamente
- [ ] Consultas por texto funcionan
- [ ] Reconocimiento de voz funciona (HTTPS ✅)
- [ ] Reportes se generan correctamente
- [ ] Deploy automático configurado
- [ ] (Opcional) Dominio personalizado configurado

---

## 📞 URLs Importantes

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Documentación Vercel**: https://vercel.com/docs
- **Google AI Studio**: https://makersuite.google.com/app/apikey
- **D-ID Documentation**: https://docs.d-id.com/

---

## 💡 Tips Pro

### 1. Usar Preview Deployments

Cada push a una rama crea un preview deployment.
Úsalos para testing antes de merge a `main`.

### 2. Environment Variables por Entorno

Puedes tener diferentes valores para:
- Production
- Preview
- Development

### 3. Redeploy Rápido

Si necesitas redeploy sin cambios:
```bash
vercel --prod
```

### 4. Rollback a Version Anterior

En Vercel Dashboard:
1. Deployments → Seleccionar deployment anterior
2. Click en "..." → "Promote to Production"

### 5. Configurar Notificaciones

Settings → Notifications → Configurar alertas por email/Slack

---

## 🎊 ¡Felicidades!

Tu Asistente Médico Virtual ahora está en producción con:

- ✅ HTTPS automático
- ✅ Deploy automático desde GitHub
- ✅ Avatar D-ID funcionando
- ✅ Google Gemini integrado
- ✅ Reconocimiento de voz habilitado
- ✅ URL pública accesible desde cualquier lugar

---

**¿Preguntas?** Consulta la documentación de Vercel o revisa los logs en el dashboard.

**¡Tu aplicación está lista para el mundo! 🌍✨**

