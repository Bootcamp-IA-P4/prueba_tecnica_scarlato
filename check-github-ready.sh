#!/bin/bash

# 🔍 Script de Verificación Pre-GitHub
# Verifica que el proyecto esté listo para subir a GitHub

echo "🔍 Verificando proyecto antes de subir a GitHub..."
echo "================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Contadores
passed=0
failed=0
warnings=0

# Función para mostrar resultados
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
    ((passed++))
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
    ((failed++))
}

check_warn() {
    echo -e "${YELLOW}⚠️ $1${NC}"
    ((warnings++))
}

echo ""
echo "📋 Verificando archivos de seguridad..."
echo "======================================="

# Verificar que .env no esté en git
if git ls-files | grep -q "^\.env$"; then
    check_fail ".env está siendo trackeado por Git - ¡PELIGRO!"
    echo "   → Ejecuta: git rm --cached .env"
    echo "   → Agrega .env al .gitignore"
else
    check_pass ".env no está en el repositorio Git"
fi

# Verificar que .env.example exista
if [ -f ".env.example" ]; then
    check_pass ".env.example existe"
else
    check_fail ".env.example no existe"
    echo "   → Crea un archivo .env.example sin datos sensibles"
fi

# Verificar que .gitignore exista
if [ -f ".gitignore" ]; then
    check_pass ".gitignore existe"
    
    # Verificar contenido importante en .gitignore
    if grep -q "\.env" .gitignore; then
        check_pass ".env está en .gitignore"
    else
        check_fail ".env no está en .gitignore"
    fi
    
    if grep -q "__pycache__" .gitignore; then
        check_pass "__pycache__ está en .gitignore"
    else
        check_warn "__pycache__ no está en .gitignore"
    fi
else
    check_fail ".gitignore no existe"
fi

echo ""
echo "📄 Verificando archivos de documentación..."
echo "==========================================="

# Verificar README
if [ -f "README.md" ]; then
    check_pass "README.md existe"
    
    # Verificar contenido básico del README
    if grep -q "# " README.md; then
        check_pass "README.md tiene título"
    else
        check_warn "README.md no tiene título principal"
    fi
else
    check_fail "README.md no existe"
fi

# Verificar otros archivos de documentación
if [ -f "CONTRIBUTING.md" ]; then
    check_pass "CONTRIBUTING.md existe"
else
    check_warn "CONTRIBUTING.md no existe (recomendado)"
fi

if [ -f "LICENSE" ]; then
    check_pass "LICENSE existe"
else
    check_warn "LICENSE no existe (recomendado)"
fi

if [ -f "CHANGELOG.md" ]; then
    check_pass "CHANGELOG.md existe"
else
    check_warn "CHANGELOG.md no existe (recomendado)"
fi

echo ""
echo "🐍 Verificando archivos de Python..."
echo "===================================="

# Verificar requirements.txt
if [ -f "requirements.txt" ]; then
    check_pass "requirements.txt existe"
    
    # Verificar que no esté vacío
    if [ -s "requirements.txt" ]; then
        check_pass "requirements.txt no está vacío"
    else
        check_fail "requirements.txt está vacío"
    fi
else
    check_fail "requirements.txt no existe"
fi

# Verificar manage.py
if [ -f "manage.py" ]; then
    check_pass "manage.py existe"
else
    check_fail "manage.py no existe"
fi

echo ""
echo "🔐 Verificando seguridad..."
echo "=========================="

# Verificar que no haya archivos con datos sensibles
dangerous_files=("*.sqlite3" "*.db" "*.log" "*.tmp" "*.bak")
for pattern in "${dangerous_files[@]}"; do
    if find . -name "$pattern" -not -path "./venv/*" -not -path "./.venv/*" | grep -q .; then
        check_warn "Archivos $pattern encontrados - considera añadirlos al .gitignore"
    fi
done

# Verificar archivos de configuración
if [ -f ".env" ]; then
    if grep -q "SECRET_KEY.*=" .env; then
        if grep -q "SECRET_KEY=django-insecure" .env; then
            check_warn "SECRET_KEY parece ser de desarrollo - cámbiala en producción"
        else
            check_pass "SECRET_KEY está configurada"
        fi
    else
        check_fail "SECRET_KEY no encontrada en .env"
    fi
fi

echo ""
echo "🧪 Verificando tests..."
echo "======================"

# Verificar que existan archivos de test
if find . -name "test_*.py" -o -name "*_test.py" -o -name "tests.py" | grep -q .; then
    check_pass "Archivos de test encontrados"
    
    # Ejecutar tests si es posible
    if [ -f "manage.py" ]; then
        echo "🔄 Ejecutando tests..."
        if python manage.py test --verbosity=0 > /dev/null 2>&1; then
            check_pass "Tests ejecutados correctamente"
        else
            check_fail "Tests fallaron"
            echo "   → Ejecuta: python manage.py test"
        fi
    fi
else
    check_warn "No se encontraron archivos de test"
fi

echo ""
echo "📊 Resumen de la verificación..."
echo "==============================="
echo -e "${GREEN}✅ Verificaciones pasadas: $passed${NC}"
echo -e "${YELLOW}⚠️ Advertencias: $warnings${NC}"
echo -e "${RED}❌ Verificaciones fallidas: $failed${NC}"

echo ""
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡Proyecto listo para subir a GitHub!${NC}"
    echo ""
    echo "📋 Próximos pasos:"
    echo "1. git add ."
    echo "2. git commit -m 'Initial commit: Aplicación de recetas Django'"
    echo "3. git push origin main"
    echo ""
    echo "🔗 No olvides:"
    echo "• Configurar el repositorio como público o privado según tus necesidades"
    echo "• Añadir colaboradores si es necesario"
    echo "• Configurar GitHub Pages si quieres documentación online"
    echo "• Revisar las configuraciones de seguridad del repositorio"
else
    echo -e "${RED}⚠️ Hay problemas que debes resolver antes de subir a GitHub${NC}"
    echo ""
    echo "🔧 Corrige los errores marcados con ❌ y ejecuta este script nuevamente"
fi

echo ""
echo "📚 Recursos útiles:"
echo "• https://docs.github.com/es/repositories/creating-and-managing-repositories"
echo "• https://docs.github.com/es/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility"
echo "• https://gitignore.io/ - Generador de archivos .gitignore"
