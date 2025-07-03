#!/bin/bash

# 🚀 Script de Configuración Rápida - Recetas Gourmet
# Este script automatiza la configuración inicial del proyecto

echo "🍽️ Configurando Recetas Gourmet..."
echo "=================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar mensajes
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

print_status "Python 3 encontrado"

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 no está instalado. Por favor instálalo primero."
    exit 1
fi

print_status "pip3 encontrado"

# Crear entorno virtual
echo ""
echo "🔧 Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Entorno virtual creado"
else
    print_warning "Entorno virtual ya existe"
fi

# Activar entorno virtual
echo ""
echo "🔌 Activando entorno virtual..."
source venv/bin/activate
print_status "Entorno virtual activado"

# Actualizar pip
echo ""
echo "⬆️ Actualizando pip..."
pip install --upgrade pip
print_status "pip actualizado"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip install -r requirements.txt
print_status "Dependencias instaladas"

# Configurar archivo .env
echo ""
echo "⚙️ Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_status "Archivo .env creado desde .env.example"
    print_warning "¡IMPORTANTE! Edita el archivo .env con tus datos reales"
else
    print_warning "Archivo .env ya existe"
fi

# Crear base de datos (SQLite por defecto)
echo ""
echo "🗄️ Configurando base de datos..."
python manage.py migrate
print_status "Migraciones aplicadas"

# Crear superusuario
echo ""
echo "👤 ¿Deseas crear un superusuario? (y/n)"
read -p "> " create_superuser
if [[ $create_superuser == "y" || $create_superuser == "Y" ]]; then
    python manage.py createsuperuser
    print_status "Superusuario creado"
fi

# Recopilar archivos estáticos
echo ""
echo "📄 Recopilando archivos estáticos..."
python manage.py collectstatic --noinput
print_status "Archivos estáticos recopilados"

# Ejecutar tests
echo ""
echo "🧪 ¿Deseas ejecutar los tests? (y/n)"
read -p "> " run_tests
if [[ $run_tests == "y" || $run_tests == "Y" ]]; then
    python manage.py test
    print_status "Tests completados"
fi

# Instrucciones finales
echo ""
echo "🎉 ¡Configuración completada!"
echo "=========================="
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env con tus configuraciones"
echo "2. Ejecuta: python manage.py runserver"
echo "3. Abre http://127.0.0.1:8000 en tu navegador"
echo "4. Accede al admin en http://127.0.0.1:8000/admin/"
echo ""
echo "📚 Comandos útiles:"
echo "• Activar entorno: source venv/bin/activate"
echo "• Instalar paquete: pip install nombre-paquete"
echo "• Hacer migraciones: python manage.py makemigrations"
echo "• Aplicar migraciones: python manage.py migrate"
echo "• Ejecutar tests: python manage.py test"
echo "• Crear superusuario: python manage.py createsuperuser"
echo ""
echo "🔗 Enlaces útiles:"
echo "• Documentación: README.md"
echo "• Contribuir: CONTRIBUTING.md"
echo "• Seguridad: SECURITY.md"
echo ""
print_status "¡Disfruta desarrollando con Recetas Gourmet! 🍽️"
