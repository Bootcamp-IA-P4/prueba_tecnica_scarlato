# 🤝 Contribuciones

¡Gracias por tu interés en contribuir al proyecto Recetas Gourmet! Este documento te guiará sobre cómo colaborar de manera efectiva.

## 📋 Cómo Contribuir

### 1. Fork del Proyecto
```bash
# 1. Haz un fork del repositorio en GitHub
# 2. Clona tu fork
git clone https://github.com/tu-usuario/recetas-gourmet.git
cd recetas-gourmet
```

### 2. Configuración del Entorno
```bash
# Crea un entorno virtual
python -m venv venv

# Activa el entorno (Windows)
venv\Scripts\activate

# Activa el entorno (macOS/Linux)
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt
```

### 3. Configuración de la Base de Datos
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Edita .env con tus datos reales
# Ejecuta las migraciones
python manage.py migrate

# Crea un superusuario
python manage.py createsuperuser
```

### 4. Flujo de Trabajo
```bash
# Crea una rama para tu feature
git checkout -b feature/nueva-funcionalidad

# Realiza tus cambios
# Ejecuta los tests
python manage.py test

# Commit y push
git add .
git commit -m "feat: descripción de la nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

### 5. Pull Request
- Abre un Pull Request describiendo tus cambios
- Asegúrate de que los tests pasen
- Incluye capturas de pantalla si es necesario

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python manage.py test

# Tests específicos
python manage.py test recetas.tests.test_models

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

### Coverage Esperado
- Mantén la cobertura de código por encima del 80%
- Escribe tests para nuevas funcionalidades
- Actualiza tests existentes si es necesario

## 🎨 Estándares de Código

### Python
- Sigue PEP 8
- Usa type hints cuando sea posible
- Documenta funciones complejas
- Mantén líneas de máximo 100 caracteres

### Django
- Sigue las convenciones de Django
- Usa Class-Based Views cuando sea apropiado
- Implementa validaciones en formularios
- Usa el ORM de Django para consultas

### Frontend
- Usa CSS Grid y Flexbox
- Mantén el código JavaScript vanilla
- Asegúrate de que sea responsive
- Prueba en diferentes navegadores

## 📝 Tipos de Contribuciones

### 🐛 Bug Fixes
- Reporta bugs usando issues
- Incluye pasos para reproducir
- Proporciona información del entorno

### ✨ Nuevas Funcionalidades
- Discute la funcionalidad en un issue primero
- Mantén el scope pequeño y manejable
- Documenta la nueva funcionalidad

### 📚 Documentación
- Mejora el README
- Añade docstrings
- Actualiza comentarios de código

### 🎨 Mejoras de UI/UX
- Mantén el diseño coherente
- Prueba en dispositivos móviles
- Considera la accesibilidad

## 🚀 Despliegue

### Preparación para Producción
```bash
# Configura variables de entorno
DEBUG=False
SECRET_KEY=clave-super-segura
DATABASE_URL=tu-base-de-datos-produccion

# Ejecuta collectstatic
python manage.py collectstatic

# Ejecuta las migraciones en producción
python manage.py migrate
```

## 📞 Contacto

Si tienes preguntas o necesitas ayuda:
- Abre un issue en GitHub
- Revisa la documentación existente
- Contacta al mantenedor principal

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la misma licencia del proyecto.

---

¡Gracias por hacer que Recetas Gourmet sea aún mejor! 🍽️✨
