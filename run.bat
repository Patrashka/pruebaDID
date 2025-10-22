@echo off
echo ============================================
echo  Iniciando Asistente Médico Virtual D-ID
echo ============================================
echo.

REM Verificar si existe el entorno virtual
if not exist venv (
    echo ERROR: No se encontró el entorno virtual.
    echo Por favor, ejecuta setup_venv.bat primero.
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar si existe .env
if not exist .env (
    echo.
    echo ADVERTENCIA: No se encontró el archivo .env
    echo Por favor, crea un archivo .env con tu OPENAI_API_KEY
    echo.
    echo Ejemplo:
    echo OPENAI_API_KEY=tu_api_key_aqui
    echo FLASK_ENV=development
    echo PORT=5000
    echo.
    pause
)

echo Iniciando servidor Flask...
echo.
echo La aplicación estará disponible en: http://localhost:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python app.py

