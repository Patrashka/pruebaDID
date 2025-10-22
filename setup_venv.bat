@echo off
echo ============================================
echo  Configuración de Entorno Virtual - Asistente Médico D-ID
echo ============================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

echo [1/5] Verificando Python...
python --version
echo.

REM Crear entorno virtual
echo [2/5] Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe. ¿Deseas recrearlo? (S/N)
    set /p recrear=
    if /i "%recrear%"=="S" (
        echo Eliminando entorno virtual anterior...
        rmdir /s /q venv
        python -m venv venv
        echo Entorno virtual recreado.
    ) else (
        echo Usando entorno virtual existente.
    )
) else (
    python -m venv venv
    echo Entorno virtual creado.
)
echo.

REM Activar entorno virtual
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

REM Actualizar pip
echo [4/5] Actualizando pip...
python -m pip install --upgrade pip
echo.

REM Instalar dependencias
echo [5/5] Instalando dependencias...
pip install -r requirements.txt
echo.

echo ============================================
echo  Configuración completada exitosamente!
echo ============================================
echo.
echo Próximos pasos:
echo 1. Crea un archivo .env con tu OPENAI_API_KEY
echo 2. Ejecuta: run.bat
echo.
echo Para activar el entorno virtual manualmente:
echo    venv\Scripts\activate
echo.
pause

