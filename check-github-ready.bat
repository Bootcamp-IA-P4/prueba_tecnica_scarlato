@echo off
REM 🔍 Script de Verificación Pre-GitHub (Windows)
REM Verifica que el proyecto esté listo para subir a GitHub

echo 🔍 Verificando proyecto antes de subir a GitHub...
echo ================================================

set /a passed=0
set /a failed=0
set /a warnings=0

echo.
echo 📋 Verificando archivos de seguridad...
echo =======================================

REM Verificar que .env no esté en git
git ls-files | findstr /r "^\.env$" >nul
if %errorlevel% equ 0 (
    echo ❌ .env está siendo trackeado por Git - ¡PELIGRO!
    echo    → Ejecuta: git rm --cached .env
    echo    → Agrega .env al .gitignore
    set /a failed+=1
) else (
    echo ✅ .env no está en el repositorio Git
    set /a passed+=1
)

REM Verificar que .env.example exista
if exist ".env.example" (
    echo ✅ .env.example existe
    set /a passed+=1
) else (
    echo ❌ .env.example no existe
    echo    → Crea un archivo .env.example sin datos sensibles
    set /a failed+=1
)

REM Verificar que .gitignore exista
if exist ".gitignore" (
    echo ✅ .gitignore existe
    set /a passed+=1
    
    REM Verificar contenido importante en .gitignore
    findstr /C:".env" .gitignore >nul
    if %errorlevel% equ 0 (
        echo ✅ .env está en .gitignore
        set /a passed+=1
    ) else (
        echo ❌ .env no está en .gitignore
        set /a failed+=1
    )
    
    findstr /C:"__pycache__" .gitignore >nul
    if %errorlevel% equ 0 (
        echo ✅ __pycache__ está en .gitignore
        set /a passed+=1
    ) else (
        echo ⚠️ __pycache__ no está en .gitignore
        set /a warnings+=1
    )
) else (
    echo ❌ .gitignore no existe
    set /a failed+=1
)

echo.
echo 📄 Verificando archivos de documentación...
echo ===========================================

REM Verificar README
if exist "README.md" (
    echo ✅ README.md existe
    set /a passed+=1
    
    REM Verificar contenido básico del README
    findstr /C:"# " README.md >nul
    if %errorlevel% equ 0 (
        echo ✅ README.md tiene título
        set /a passed+=1
    ) else (
        echo ⚠️ README.md no tiene título principal
        set /a warnings+=1
    )
) else (
    echo ❌ README.md no existe
    set /a failed+=1
)

REM Verificar otros archivos de documentación
if exist "CONTRIBUTING.md" (
    echo ✅ CONTRIBUTING.md existe
    set /a passed+=1
) else (
    echo ⚠️ CONTRIBUTING.md no existe (recomendado)
    set /a warnings+=1
)

if exist "LICENSE" (
    echo ✅ LICENSE existe
    set /a passed+=1
) else (
    echo ⚠️ LICENSE no existe (recomendado)
    set /a warnings+=1
)

if exist "CHANGELOG.md" (
    echo ✅ CHANGELOG.md existe
    set /a passed+=1
) else (
    echo ⚠️ CHANGELOG.md no existe (recomendado)
    set /a warnings+=1
)

echo.
echo 🐍 Verificando archivos de Python...
echo ====================================

REM Verificar requirements.txt
if exist "requirements.txt" (
    echo ✅ requirements.txt existe
    set /a passed+=1
    
    REM Verificar que no esté vacío
    for /f %%i in ('type requirements.txt 2^>nul ^| find /c /v ""') do set linecount=%%i
    if %linecount% gtr 0 (
        echo ✅ requirements.txt no está vacío
        set /a passed+=1
    ) else (
        echo ❌ requirements.txt está vacío
        set /a failed+=1
    )
) else (
    echo ❌ requirements.txt no existe
    set /a failed+=1
)

REM Verificar manage.py
if exist "manage.py" (
    echo ✅ manage.py existe
    set /a passed+=1
) else (
    echo ❌ manage.py no existe
    set /a failed+=1
)

echo.
echo 🔐 Verificando seguridad...
echo ==========================

REM Verificar archivos de configuración
if exist ".env" (
    findstr /C:"SECRET_KEY" .env >nul
    if %errorlevel% equ 0 (
        findstr /C:"SECRET_KEY=django-insecure" .env >nul
        if %errorlevel% equ 0 (
            echo ⚠️ SECRET_KEY parece ser de desarrollo - cámbiala en producción
            set /a warnings+=1
        ) else (
            echo ✅ SECRET_KEY está configurada
            set /a passed+=1
        )
    ) else (
        echo ❌ SECRET_KEY no encontrada en .env
        set /a failed+=1
    )
)

echo.
echo 🧪 Verificando tests...
echo ======================

REM Verificar que existan archivos de test
dir /s /b test_*.py *_test.py tests.py 2>nul | findstr /v /c:"" >nul
if %errorlevel% equ 0 (
    echo ✅ Archivos de test encontrados
    set /a passed+=1
    
    REM Ejecutar tests si es posible
    if exist "manage.py" (
        echo 🔄 Ejecutando tests...
        python manage.py test --verbosity=0 >nul 2>&1
        if %errorlevel% equ 0 (
            echo ✅ Tests ejecutados correctamente
            set /a passed+=1
        ) else (
            echo ❌ Tests fallaron
            echo    → Ejecuta: python manage.py test
            set /a failed+=1
        )
    )
) else (
    echo ⚠️ No se encontraron archivos de test
    set /a warnings+=1
)

echo.
echo 📊 Resumen de la verificación...
echo ===============================
echo ✅ Verificaciones pasadas: %passed%
echo ⚠️ Advertencias: %warnings%
echo ❌ Verificaciones fallidas: %failed%

echo.
if %failed% equ 0 (
    echo 🎉 ¡Proyecto listo para subir a GitHub!
    echo.
    echo 📋 Próximos pasos:
    echo 1. git add .
    echo 2. git commit -m "Initial commit: Aplicación de recetas Django"
    echo 3. git push origin main
    echo.
    echo 🔗 No olvides:
    echo • Configurar el repositorio como público o privado según tus necesidades
    echo • Añadir colaboradores si es necesario
    echo • Configurar GitHub Pages si quieres documentación online
    echo • Revisar las configuraciones de seguridad del repositorio
) else (
    echo ⚠️ Hay problemas que debes resolver antes de subir a GitHub
    echo.
    echo 🔧 Corrige los errores marcados con ❌ y ejecuta este script nuevamente
)

echo.
echo 📚 Recursos útiles:
echo • https://docs.github.com/es/repositories/creating-and-managing-repositories
echo • https://docs.github.com/es/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility
echo • https://gitignore.io/ - Generador de archivos .gitignore

pause
