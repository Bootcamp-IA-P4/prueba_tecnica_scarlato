@echo off
REM 🚀 Script de Configuración Rápida - Recetas Gourmet (Windows)
REM Este script automatiza la configuración inicial del proyecto

echo 🍽️ Configurando Recetas Gourmet...
echo ==================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado. Por favor instálalo primero.
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Verificar si pip está instalado
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip no está instalado. Por favor instálalo primero.
    pause
    exit /b 1
)

echo ✅ pip encontrado

REM Crear entorno virtual
echo.
echo 🔧 Creando entorno virtual...
if not exist "venv" (
    python -m venv venv
    echo ✅ Entorno virtual creado
) else (
    echo ⚠️ Entorno virtual ya existe
)

REM Activar entorno virtual
echo.
echo 🔌 Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✅ Entorno virtual activado

REM Actualizar pip
echo.
echo ⬆️ Actualizando pip...
pip install --upgrade pip
echo ✅ pip actualizado

REM Instalar dependencias
echo.
echo 📦 Instalando dependencias...
pip install -r requirements.txt
echo ✅ Dependencias instaladas

REM Configurar archivo .env
echo.
echo ⚙️ Configurando variables de entorno...
if not exist ".env" (
    copy .env.example .env
    echo ✅ Archivo .env creado desde .env.example
    echo ⚠️ ¡IMPORTANTE! Edita el archivo .env con tus datos reales
) else (
    echo ⚠️ Archivo .env ya existe
)

REM Crear base de datos (SQLite por defecto)
echo.
echo 🗄️ Configurando base de datos...
python manage.py migrate
echo ✅ Migraciones aplicadas

REM Crear superusuario
echo.
set /p create_superuser=👤 ¿Deseas crear un superusuario? (y/n): 
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
    echo ✅ Superusuario creado
)

REM Recopilar archivos estáticos
echo.
echo 📄 Recopilando archivos estáticos...
python manage.py collectstatic --noinput
echo ✅ Archivos estáticos recopilados

REM Ejecutar tests
echo.
set /p run_tests=🧪 ¿Deseas ejecutar los tests? (y/n): 
if /i "%run_tests%"=="y" (
    python manage.py test
    echo ✅ Tests completados
)

REM Instrucciones finales
echo.
echo 🎉 ¡Configuración completada!
echo ==========================
echo.
echo 📋 Próximos pasos:
echo 1. Edita el archivo .env con tus configuraciones
echo 2. Ejecuta: python manage.py runserver
echo 3. Abre http://127.0.0.1:8000 en tu navegador
echo 4. Accede al admin en http://127.0.0.1:8000/admin/
echo.
echo 📚 Comandos útiles:
echo • Activar entorno: venv\Scripts\activate.bat
echo • Instalar paquete: pip install nombre-paquete
echo • Hacer migraciones: python manage.py makemigrations
echo • Aplicar migraciones: python manage.py migrate
echo • Ejecutar tests: python manage.py test
echo • Crear superusuario: python manage.py createsuperuser
echo.
echo 🔗 Enlaces útiles:
echo • Documentación: README.md
echo • Contribuir: CONTRIBUTING.md
echo • Seguridad: SECURITY.md
echo.
echo ✅ ¡Disfruta desarrollando con Recetas Gourmet! 🍽️
pause
