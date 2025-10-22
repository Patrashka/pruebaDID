@echo off
echo ============================================
echo  Limpieza de archivos de Git
echo ============================================
echo.
echo Este script eliminará del repositorio Git:
echo - venv/
echo - .env
echo - __pycache__/
echo - reportes/*.json
echo - Otros archivos del .gitignore
echo.
echo NOTA: Los archivos NO se borrarán de tu PC,
echo       solo del repositorio de Git.
echo.
pause

echo.
echo Eliminando del cache de Git...
echo.

REM Eliminar venv del tracking
git rm -r --cached venv 2>nul
echo ✓ venv/

REM Eliminar .env del tracking
git rm --cached .env 2>nul
echo ✓ .env

REM Eliminar __pycache__ del tracking
git rm -r --cached __pycache__ 2>nul
echo ✓ __pycache__/

REM Eliminar reportes del tracking
git rm -r --cached reportes/*.json 2>nul
git rm -r --cached reportes/*.txt 2>nul
git rm -r --cached reportes/*.pdf 2>nul
echo ✓ reportes/

REM Eliminar logs del tracking
git rm --cached *.log 2>nul
echo ✓ logs

REM Aplicar .gitignore a todo el repo
git rm -r --cached . 2>nul
git add .

echo.
echo ============================================
echo  Archivos limpiados del cache de Git
echo ============================================
echo.
echo Ahora haz commit y push:
echo.
echo   git commit -m "Limpiar archivos ignorados"
echo   git push origin main
echo.
pause

