# 🚀 Guía para Desplegar en Vercel

## 📋 Pasos para Desplegar el Avatar Médico en Vercel

### 1. Preparar el Proyecto

Los archivos necesarios ya están creados:
- ✅ `vercel.json` - Configuración de Vercel
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `server_with_did.py` - Servidor principal
- ✅ `.env` - Variables de entorno (NO subir a GitHub)

### 2. Crear Cuenta en Vercel

1. **Ve a**: https://vercel.com
2. **Haz clic en "Sign Up"**
3. **Regístrate con GitHub** (recomendado) o email

### 3. Subir el Proyecto a GitHub

#### Opción A: Usar GitHub Desktop
1. Descarga GitHub Desktop: https://desktop.github.com
2. Crea un nuevo repositorio
3. Agrega los archivos del proyecto
4. Haz commit y push

#### Opción B: Usar Git desde terminal
```bash
# Inicializar repositorio
git init

# Crear .gitignore
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore

# Agregar archivos
git add .

# Hacer commit
git commit -m "Initial commit - Avatar Médico Virtual"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 4. Desplegar en Vercel

1. **Ve a Vercel**: https://vercel.com/dashboard
2. **Haz clic en "New Project"**
3. **Importa tu repositorio de GitHub**
4. **Configura las variables de entorno**:
   - Click en "Environment Variables"
   - Agrega las siguientes variables:
     ```
     DID_API_KEY=aW50ZWdyYWNpb24yNTlAZ21haWwuY29t:nbrNazwVQw3qIidcJv5p0
     DID_AGENT_ID=v2_agt_gRs4QB2l
     DID_CLIENT_KEY=Z29vZ2xlLW9hdXRoMnwxMTU1ODgzNDk4MjgyOTQ5MzYwNzM6SHFkdzdaU0gtMklRZ29Nb2Rvb0JS
     ```
5. **Haz clic en "Deploy"**

### 5. Obtener la URL de Vercel

Después del despliegue, Vercel te dará una URL como:
```
https://tu-proyecto.vercel.app
```

### 6. Configurar D-ID Studio

1. **Ve a**: https://studio.d-id.com
2. **Selecciona tu agente**: `v2_agt_gRs4QB2l`
3. **Ve a configuración/embed**
4. **Agrega a dominios permitidos**:
   ```
   https://tu-proyecto.vercel.app
   ```

### 7. Probar el Avatar

Una vez configurado:
1. **Ve a**: `https://tu-proyecto.vercel.app`
2. **Haz clic en "AVATAR SIMPLE"**
3. **Haz clic en "Conectar Avatar"**
4. **¡El avatar debería aparecer!**

## 🔧 Solución de Problemas

### Error: Build Failed
- Verifica que `requirements.txt` esté correcto
- Asegúrate de que `vercel.json` esté en la raíz del proyecto

### Error: 404 Not Found
- Verifica que `server_with_did.py` esté en la raíz
- Revisa la configuración en `vercel.json`

### Error: Variables de entorno no funcionan
- Ve a Vercel Dashboard > Tu Proyecto > Settings > Environment Variables
- Asegúrate de que todas las variables estén agregadas
- Redeploy el proyecto después de agregar variables

## 📱 URLs Disponibles

Después del despliegue, tendrás acceso a:
- `/` - Página principal
- `/avatar_simple.html` - Avatar simplificado
- `/medical_avatar_demo.html` - Avatar completo
- `/demo` - Demo básico
- `/api/did/config` - Configuración D-ID

## 🎯 Ventajas de Vercel

- ✅ **Gratis** para proyectos personales
- ✅ **HTTPS automático**
- ✅ **Despliegues automáticos** desde GitHub
- ✅ **Sin configuración de servidor**
- ✅ **Compatible con D-ID**

## 📝 Notas Importantes

1. **NO subas el archivo `.env` a GitHub** (está en .gitignore)
2. **Usa Environment Variables** en Vercel Dashboard
3. **Cada push a GitHub** redesplegará automáticamente
4. **URL personalizada**: Puedes agregar un dominio personalizado en Vercel

## 🆘 Ayuda Adicional

Si necesitas ayuda:
- **Documentación Vercel**: https://vercel.com/docs
- **Documentación D-ID**: https://docs.d-id.com
