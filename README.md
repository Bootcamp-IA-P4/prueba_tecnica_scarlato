# 🍽️ Recetas Gourmet - Aplicación Web Premium

Una aplicación web premium para gestionar una colección personal de recetas favoritas, desarrollada con Django y diseñada con una interfaz moderna y marketinera inspirada en sitios como gastronomistas.com.

## 🚀 Características

### Funcionalidades Principales
- **CRUD completo de recetas** con validaciones avanzadas
- **Sistema de categorías y etiquetas** para organizar recetas
- **Búsqueda avanzada y filtros** por múltiples criterios
- **Sistema de favoritos** para usuarios autenticados
- **Valoraciones y comentarios** en cada receta
- **Paginación inteligente** para mejor rendimiento
- **API REST completa** con Django REST Framework
- **Panel de administración personalizado**

### Diseño y UX
- **Diseño responsive** que funciona en todos los dispositivos
- **Interfaz premium** inspirada en sitios como gastronomistas.com
- **Animaciones CSS** y transiciones suaves
- **Experiencia de usuario optimizada** con AJAX
- **Notificaciones interactivas** para mejor feedback
- **Carga de imágenes** para recetas con vista previa

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 5.0** - Framework web principal
- **Django REST Framework** - API REST
- **Pillow** - Procesamiento de imágenes
- **django-filter** - Filtros avanzados
- **python-decouple** - Gestión de variables de entorno

### Frontend
- **HTML5** semántico y accesible
- **CSS3** con Grid y Flexbox
- **JavaScript ES6+** vanilla
- **Font Awesome** para iconografía
- **Google Fonts** para tipografía premium

### Testing y Calidad
- **Django Test Framework** - Tests unitarios
- **Coverage** - Cobertura de código
- **Factory Boy** - Factories para tests
- **Pytest-Django** - Runner de tests mejorado

---

## � **GUÍA COMPLETA DE INSTALACIÓN PASO A PASO**

### ⚠️ **ANTES DE COMENZAR - REQUISITOS PREVIOS**

Esta guía está diseñada para usuarios sin experiencia en sistemas. Sigue cada paso exactamente como se indica.

#### 🔧 **PASO 0: Instalar Requisitos del Sistema**

**Para Windows:**

1. **Instalar Python 3.9 o superior**
   - Ve a [python.org](https://www.python.org/downloads/)
   - Descarga Python 3.9+ para Windows
   - ⚠️ **IMPORTANTE**: Durante la instalación, marca la casilla "Add Python to PATH"
   - Instala con configuración por defecto

2. **Verificar instalación de Python**
   - Presiona `Win + R`, escribe `cmd` y presiona Enter
   - Escribe: `python --version`
   - Deberías ver algo como: `Python 3.9.x` o superior
   - Si no funciona, reinicia tu computadora e intenta de nuevo

3. **Instalar MySQL (Base de Datos)**
   - Ve a [mysql.com](https://dev.mysql.com/downloads/installer/)
   - Descarga "MySQL Installer for Windows"
   - Ejecuta el instalador y selecciona "Custom"
   - Instala: "MySQL Server" y "MySQL Workbench"
   - ⚠️ **IMPORTANTE**: Anota la contraseña del usuario root que elijas
   - Puedes usar una contraseña simple como `password123` para este proyecto

4. **Crear la Base de Datos**
   - Abre MySQL Workbench
   - Conéctate al servidor local (localhost)
   - Crea una nueva base de datos llamada `recetas_db`:
     ```sql
     CREATE DATABASE recetas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     ```

---

### 📁 **PASO 1: OBTENER EL CÓDIGO**

1. **Descargar el proyecto**
   - Si tienes Git instalado:
     ```bash
     git clone <url-del-repositorio>
     cd "prueba tecnica"
     ```
   - Si NO tienes Git:
     - Descarga el ZIP del proyecto
     - Extrae el archivo ZIP
     - Navega a la carpeta extraída

2. **Abrir PowerShell en la carpeta del proyecto**
   - Mantén presionado `Shift` y haz clic derecho en la carpeta del proyecto
   - Selecciona "Abrir ventana de PowerShell aquí"
   - O presiona `Win + R`, escribe `powershell`, navega a la carpeta:
     ```powershell
     cd "C:\Users\admin\Desktop\prueba tecnica\prueba tecnica"
     ```

---

### 🐍 **PASO 2: CONFIGURAR ENTORNO VIRTUAL DE PYTHON**

Un entorno virtual es como una "caja separada" donde instalaremos las dependencias del proyecto sin afectar tu sistema.

1. **Crear el entorno virtual**
   ```powershell
   python -m venv venv
   ```
   - Esto creará una carpeta `venv` en tu proyecto

2. **Activar el entorno virtual**
   ```powershell
   venv\Scripts\activate
   ```
   - ⚠️ **IMPORTANTE**: Deberías ver `(venv)` al inicio de tu línea de comandos
   - Si no lo ves, el entorno no está activado

3. **Verificar que el entorno esté activo**
   ```powershell
   where python
   ```
   - Debería mostrar una ruta que incluya `venv\Scripts\python.exe`

---

### 📦 **PASO 3: INSTALAR DEPENDENCIAS**

Con el entorno virtual activado (recuerda que debe mostrar `(venv)`):

1. **Actualizar pip (instalador de paquetes)**
   ```powershell
   python -m pip install --upgrade pip
   ```

2. **Instalar todas las dependencias del proyecto**
   ```powershell
   pip install -r requirements.txt
   ```
   - Esto puede tardar varios minutos
   - Verás mucho texto en pantalla, es normal

3. **Verificar instalación**
   ```powershell
   pip list
   ```
   - Deberías ver una lista de paquetes instalados incluyendo Django

---

### ⚙️ **PASO 4: CONFIGURAR VARIABLES DE ENTORNO**

1. **Crear el archivo de configuración**
   - En la carpeta raíz del proyecto (donde está `manage.py`)
   - Crea un archivo llamado `.env` (con el punto al inicio)
   - Puedes usar el Bloc de notas: `notepad .env`

2. **Agregar la configuración**
   Copia y pega exactamente esto en el archivo `.env`:
   ```env
   SECRET_KEY=django-insecure-tu-clave-secreta-super-larga-y-segura-123456789
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Configuración de MySQL
   DB_NAME=recetas_db
   DB_USER=root
   DB_PASSWORD=password123
   DB_HOST=localhost
   DB_PORT=3306
   ```
   - ⚠️ **IMPORTANTE**: Cambia `password123` por la contraseña que elegiste para MySQL
   - Guarda el archivo

---

### 🗄️ **PASO 5: CONFIGURAR LA BASE DE DATOS**

Con el entorno virtual activado y MySQL corriendo:

1. **Verificar conexión a MySQL**
   ```powershell
   python -c "import MySQLdb; print('MySQL conectado correctamente')"
   ```
   - Si hay error, verifica que MySQL esté corriendo y las credenciales sean correctas

2. **Crear las tablas de la base de datos**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
   - Esto creará todas las tablas necesarias en tu base de datos

3. **Verificar que las migraciones funcionaron**
   ```powershell
   python manage.py showmigrations
   ```
   - Deberías ver una lista de migraciones con [X] (aplicadas)

---

### 👑 **PASO 6: CREAR USUARIO ADMINISTRADOR**

Para acceder al panel de administración:

1. **Crear superusuario**
   ```powershell
   python manage.py createsuperuser
   ```
   - Te pedirá:
     - **Username**: elige un nombre (ej: `admin`)
     - **Email**: tu email (puede ser ficticio)
     - **Password**: una contraseña segura
   - ⚠️ **IMPORTANTE**: Anota estos datos, los necesitarás para acceder al admin

---

### 🚀 **PASO 7: EJECUTAR LA APLICACIÓN**

1. **Iniciar el servidor de desarrollo**
   ```powershell
   python manage.py runserver
   ```
   - Verás un mensaje como: `Starting development server at http://127.0.0.1:8000/`

2. **Abrir la aplicación en tu navegador**
   - Ve a: `http://localhost:8000` o `http://127.0.0.1:8000`
   - ¡Deberías ver la aplicación funcionando!

3. **Acceder al panel de administración**
   - Ve a: `http://localhost:8000/admin/`
   - Usa las credenciales que creaste en el paso 6
   - Desde aquí puedes crear recetas, categorías, etc.

---

### 🎉 **¡FELICITACIONES! LA APLICACIÓN ESTÁ FUNCIONANDO**

#### 🔍 **URLs Principales**
- **Página principal**: `http://localhost:8000/`
- **Panel de administración**: `http://localhost:8000/admin/`
- **API REST**: `http://localhost:8000/api/`
- **Documentación API**: `http://localhost:8000/api/docs/`

#### 🛑 **Para detener el servidor**
- En PowerShell, presiona `Ctrl + C`

#### 🔄 **Para volver a iniciar (días posteriores)**
1. Abrir PowerShell en la carpeta del proyecto
2. Activar entorno virtual: `venv\Scripts\activate`
3. Iniciar servidor: `python manage.py runserver`

---

### 📝 **PASO 8: CREAR CONTENIDO DE EJEMPLO**

Para tener datos de prueba:

1. **Crear categorías desde el admin**
   - Ve a `http://localhost:8000/admin/`
   - Clic en "Categorías" → "Agregar"
   - Crea categorías como: "Postres", "Platos Principales", "Aperitivos", etc.

2. **Crear etiquetas**
   - En el admin, clic en "Tags" → "Agregar"
   - Crea etiquetas como: "Rápido", "Vegetariano", "Sin Gluten", etc.

3. **Crear recetas**
   - En el admin, clic en "Recetas" → "Agregar"
   - Llena todos los campos
   - Sube una imagen (opcional)

---

### 🧪 **PASO 9: EJECUTAR PRUEBAS (OPCIONAL)**

Para verificar que todo funciona correctamente:

1. **Ejecutar todas las pruebas**
   ```powershell
   python manage.py test
   ```

2. **Ejecutar pruebas con cobertura**
   ```powershell
   coverage run --source='.' manage.py test
   coverage report
   ```

---

### 🚨 **SOLUCIÓN DE PROBLEMAS COMUNES**

#### **Error: "Python no se reconoce como comando"**
- Solución: Reinstala Python y asegúrate de marcar "Add Python to PATH"

#### **Error: "No module named 'MySQLdb'"**
- Solución: Verifica que MySQL esté instalado y corriendo
- Instala el cliente: `pip install mysqlclient`

#### **Error: "Access denied for user 'root'"**
- Solución: Verifica la contraseña en el archivo `.env`
- Asegúrate de que MySQL esté corriendo

#### **Error: "Port 8000 is already in use"**
- Solución: Otro proceso está usando el puerto
- Usa otro puerto: `python manage.py runserver 8001`

#### **Error: "No such file or directory: '.env'"**
- Solución: Crea el archivo `.env` en la carpeta raíz del proyecto

#### **El entorno virtual no se activa**
- Solución: Asegúrate de estar en la carpeta correcta
- Usa la ruta completa: `C:\ruta\a\tu\proyecto\venv\Scripts\activate`

#### **Error: "Permission denied"**
- Solución: Ejecuta PowerShell como administrador
- Clic derecho en PowerShell → "Ejecutar como administrador"

---

### 📞 **¿NECESITAS AYUDA?**

Si tienes problemas:

1. **Verifica que hayas seguido todos los pasos**
2. **Revisa los mensajes de error completos**
3. **Asegúrate de que el entorno virtual esté activo**
4. **Verifica que MySQL esté corriendo**

#### **Comandos útiles para diagnosticar:**
```powershell
# Verificar Python
python --version

# Verificar entorno virtual
where python

# Verificar instalación de Django
python -c "import django; print(django.get_version())"

# Verificar conexión a base de datos
python manage.py dbshell
```

---

## 💡 **CONSEJOS PARA PRINCIPIANTES**

### 🔧 **Herramientas Recomendadas**
- **Editor de código**: Visual Studio Code (gratuito)
- **Cliente MySQL**: MySQL Workbench (incluido con MySQL)
- **Navegador**: Chrome o Firefox para desarrollo

### 📚 **Recursos de Aprendizaje**
- **Django**: [djangoproject.com](https://docs.djangoproject.com/)
- **Python**: [python.org](https://www.python.org/about/gettingstarted/)
- **MySQL**: [mysql.com/learn](https://dev.mysql.com/doc/)

### 🎯 **Próximos Pasos**
1. Explora la interfaz de administración
2. Crea algunas recetas de prueba
3. Prueba la búsqueda y filtros
4. Experimenta con la API REST

---

## 📦 **INSTALACIÓN RÁPIDA (PARA USUARIOS AVANZADOS)**

Si ya tienes experiencia con Python y Django:

```bash
# Clonar y configurar
git clone <url-del-repositorio>
cd "prueba tecnica"

# Entorno virtual y dependencias
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Configurar .env (ver ejemplo arriba)
# Configurar MySQL y crear base de datos 'recetas_db'

# Migraciones y superusuario
python manage.py migrate
python manage.py createsuperuser

# Ejecutar
python manage.py runserver
```

## 🎯 **GUÍA DE USO DE LA APLICACIÓN**

### 👤 **Para Usuarios Finales**

#### **Navegación Principal**
1. **Página de Inicio** (`http://localhost:8000/`)
   - Muestra las recetas más populares
   - Banner de bienvenida con estadísticas
   - Acceso rápido a categorías principales

2. **Explorar Recetas**
   - **Ver todas**: Botón "Ver todas las recetas"
   - **Por categoría**: Filtros en el sidebar
   - **Búsqueda**: Barra de búsqueda en la parte superior

3. **Buscar Recetas**
   - **Búsqueda por texto**: Escribe ingredientes o nombres
   - **Filtros avanzados**:
     - Categoría (Postres, Platos principales, etc.)
     - Dificultad (Fácil, Media, Difícil)
     - Tiempo de preparación
     - Número de porciones
   - **Ordenamiento**: Por fecha, popularidad, tiempo, etc.

4. **Ver Detalles de Receta**
   - Clic en cualquier receta para ver:
     - Ingredientes completos
     - Pasos detallados
     - Información nutricional
     - Valoraciones de otros usuarios
     - Comentarios

5. **Sistema de Favoritos** (Requiere registro)
   - Clic en el corazón ❤️ para guardar recetas
   - Accede a tus favoritos desde el menú usuario

#### **Registro y Autenticación**
1. **Crear cuenta**
   - Clic en "Registrarse"
   - Completa el formulario
   - Confirma tu email (si está configurado)

2. **Iniciar sesión**
   - Clic en "Iniciar Sesión"
   - Usa tu usuario y contraseña

3. **Perfil de usuario**
   - Gestiona tus recetas favoritas
   - Ve tu historial de valoraciones
   - Actualiza tu información personal

#### **Interacción con Recetas**
1. **Valorar recetas**
   - Deja una puntuación de 1-5 estrellas
   - Escribe comentarios opcionales

2. **Compartir recetas**
   - Botones de compartir en redes sociales
   - Copia el enlace directo

---

### 👨‍💼 **Para Administradores**

#### **Acceso al Panel de Administración**
1. **Iniciar sesión como admin**
   - Ve a `http://localhost:8000/admin/`
   - Usa las credenciales de superusuario creadas anteriormente

2. **Dashboard principal**
   - Resumen de estadísticas
   - Acceso rápido a todas las secciones
   - Filtros y búsquedas avanzadas

#### **Gestión de Contenido**

1. **Crear Recetas**
   - Clic en "Recetas" → "Agregar receta"
   - **Campos obligatorios**:
     - Título
     - Descripción
     - Ingredientes (uno por línea)
     - Pasos (numerados automáticamente)
     - Categoría
     - Dificultad
     - Tiempo de preparación
     - Porciones
   - **Campos opcionales**:
     - Imagen
     - URL de video
     - Etiquetas
     - Notas adicionales

2. **Gestionar Categorías**
   - Clic en "Categorías" → "Agregar categoría"
   - Nombre y descripción
   - Imagen representativa (opcional)

3. **Gestionar Etiquetas**
   - Clic en "Tags" → "Agregar tag"
   - Útil para clasificación cruzada: "Vegetariano", "Sin Gluten", etc.

4. **Moderar Valoraciones**
   - Revisar comentarios de usuarios
   - Eliminar contenido inapropiado
   - Responder a comentarios

#### **Funciones Avanzadas del Admin**
1. **Filtros inteligentes**
   - Filtra por fecha de creación
   - Por popularidad (número de valoraciones)
   - Por usuario autor
   - Por estado (publicado/borrador)

2. **Acciones masivas**
   - Seleccionar múltiples recetas
   - Cambiar estado en lote
   - Exportar datos

3. **Búsqueda avanzada**
   - Buscar por cualquier campo
   - Búsqueda en ingredientes
   - Búsqueda por etiquetas

---

### 🔌 **API REST - Documentación**

La aplicación incluye una API REST completa para integración con otras aplicaciones.

#### **Endpoints Principales**

**Base URL**: `http://localhost:8000/api/`

#### **Recetas**
```http
GET /api/recetas/
```
- Lista todas las recetas
- Parámetros de filtrado:
  - `?categoria=ID` - Filtrar por categoría
  - `?dificultad=facil` - Filtrar por dificultad
  - `?search=texto` - Búsqueda en título/ingredientes
  - `?ordering=fecha_creacion` - Ordenar resultados
  - `?page=1` - Paginación

```http
POST /api/recetas/
```
- Crear nueva receta (requiere autenticación)
- Body (JSON):
```json
{
  "titulo": "Mi Receta",
  "descripcion": "Descripción de la receta",
  "ingredientes": "Ingredient 1\nIngredient 2",
  "pasos": "Paso 1\nPaso 2",
  "categoria": 1,
  "dificultad": "facil",
  "tiempo_preparacion": 30,
  "porciones": 4
}
```

```http
GET /api/recetas/{id}/
```
- Obtener receta específica

```http
PUT /api/recetas/{id}/
```
- Actualizar receta (solo el autor o admin)

```http
DELETE /api/recetas/{id}/
```
- Eliminar receta (solo el autor o admin)

#### **Categorías**
```http
GET /api/categorias/
POST /api/categorias/
GET /api/categorias/{id}/
PUT /api/categorias/{id}/
DELETE /api/categorias/{id}/
```

#### **Etiquetas**
```http
GET /api/tags/
POST /api/tags/
GET /api/tags/{id}/
PUT /api/tags/{id}/
DELETE /api/tags/{id}/
```

#### **Autenticación de API**
La API utiliza autenticación por tokens:

1. **Obtener token**
```http
POST /api/auth/login/
{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

2. **Usar token en requests**
```http
Authorization: Token tu_token_aqui
```

#### **Ejemplos de Uso con curl**

```bash
# Listar recetas
curl -X GET http://localhost:8000/api/recetas/

# Crear receta (autenticado)
curl -X POST http://localhost:8000/api/recetas/ \
  -H "Authorization: Token tu_token" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Pasta Carbonara",
    "descripcion": "Receta italiana clásica",
    "ingredientes": "Pasta\nHuevos\nPanceta\nQueso",
    "pasos": "Cocinar pasta\nMezclar ingredientes",
    "categoria": 1,
    "dificultad": "media",
    "tiempo_preparacion": 20,
    "porciones": 2
  }'

# Buscar recetas
curl -X GET "http://localhost:8000/api/recetas/?search=pasta"

# Filtrar por categoría
curl -X GET "http://localhost:8000/api/recetas/?categoria=1"
```

---

### 🧪 **TESTING - Guía Completa**

#### **Ejecutar Tests**

1. **Todos los tests**
   ```powershell
   python manage.py test
   ```

2. **Tests específicos**
   ```powershell
   # Solo tests de modelos
   python manage.py test recetas.tests.test_models
   
   # Solo tests de vistas
   python manage.py test recetas.tests.test_views
   
   # Solo tests de API
   python manage.py test recetas.tests.test_api
   ```

3. **Tests con mayor verbosidad**
   ```powershell
   python manage.py test --verbosity=2
   ```

#### **Coverage (Cobertura de Código)**

1. **Ejecutar tests con coverage**
   ```powershell
   coverage run --source='.' manage.py test
   ```

2. **Ver reporte en consola**
   ```powershell
   coverage report
   ```

3. **Generar reporte HTML**
   ```powershell
   coverage html
   ```
   - Abre `htmlcov/index.html` en tu navegador

#### **Tests Incluidos**

**Tests de Modelos (`test_models.py`)**
- Creación y validación de recetas
- Relaciones entre modelos
- Métodos personalizados
- Validaciones de campos

**Tests de Vistas (`test_views.py`)**
- Vistas de lista y detalle
- Formularios de creación/edición
- Autenticación y permisos
- Respuestas AJAX

**Tests de API (`test_api.py`)**
- Endpoints de la API REST
- Autenticación por tokens
- Serialización de datos
- Filtros y paginación

---

## 📁 Estructura del Proyecto

```
prueba-tecnica/
├── recetas_project/          # Configuración del proyecto
│   ├── settings.py          # Configuración principal
│   ├── urls.py              # URLs del proyecto
│   └── wsgi.py              # WSGI configuration
├── recetas/                 # Aplicación principal
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas de la aplicación
│   ├── forms.py             # Formularios
│   ├── filters.py           # Filtros de búsqueda
│   ├── serializers.py       # Serializers para API
│   ├── api_views.py         # Vistas de la API
│   ├── admin.py             # Configuración del admin
│   ├── urls.py              # URLs de la app
│   ├── api_urls.py          # URLs de la API
│   ├── templates/           # Templates HTML
│   └── tests/               # Tests unitarios
├── static/                  # Archivos estáticos
│   ├── css/                 # Estilos CSS
│   ├── js/                  # JavaScript
│   └── img/                 # Imágenes
├── media/                   # Archivos subidos
├── templates/               # Templates base
├── requirements.txt         # Dependencias
├── .env                     # Variables de entorno
└── README.md               # Documentación
```

## 🎨 Diseño y Arquitectura

### Patrones Utilizados
- **MVT (Model-View-Template)** - Arquitectura de Django
- **Repository Pattern** - Para consultas complejas
- **Factory Pattern** - Para creación de objetos en tests
- **Decorator Pattern** - Para permisos y autenticación

### Decisiones Técnicas

1. **Class-Based Views**: Para mayor reutilización y mantenibilidad
2. **Django REST Framework**: Para API robusta y bien documentada
3. **AJAX**: Para mejor experiencia de usuario sin recargas
4. **CSS Grid/Flexbox**: Para layouts modernos y responsivos
5. **Vanilla JavaScript**: Para evitar dependencias innecesarias

### Optimizaciones
- **Paginación**: Para mejorar rendimiento con muchas recetas
- **Lazy Loading**: Para imágenes y contenido dinámico
- **Caching**: Headers y queries optimizadas
- **Compresión**: CSS y JS minificados en producción

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
# Base
SECRET_KEY=clave-secreta-super-larga
DEBUG=False
ALLOWED_HOSTS=mi-dominio.com,www.mi-dominio.com

# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost/recetas_db

# Media y Static
MEDIA_URL=/media/
STATIC_URL=/static/
MEDIA_ROOT=/path/to/media/
STATIC_ROOT=/path/to/static/

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

### Deployment
Para producción, considera:
- Usar PostgreSQL en lugar de SQLite
- Configurar un servidor web (Nginx + Gunicorn)
- Activar HTTPS
- Configurar backup automático
- Usar CDN para archivos estáticos

## 🤝 Contribución

Este proyecto fue desarrollado como prueba técnica. Si quieres contribuir:

1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es una prueba técnica y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como prueba técnica para demostrar habilidades en:
- Desarrollo full-stack con Django
- Diseño de APIs REST
- Frontend moderno y responsive
- Testing y calidad de código
- Documentación técnica

---

**¡Gracias por revisar este proyecto!** 🚀

Para cualquier pregunta o comentario, no dudes en contactarme.

---

## 🔐 **GUÍA COMPLETA PARA SUBIR A GITHUB**

### 🚨 **IMPORTANTE: SEGURIDAD ANTES DE SUBIR**

**⚠️ NUNCA subas información sensible a GitHub**. Sigue estos pasos obligatorios:

#### **1. Proteger Datos Sensibles**

1. **Verificar que .env NO esté en Git**
   ```powershell
   git status
   ```
   - Si ves `.env` en la lista, **DETENTE**
   - Ejecuta: `git reset HEAD .env` y `git rm --cached .env`

2. **Verificar .gitignore**
   - Asegúrate de que el archivo `.gitignore` existe
   - Debe contener al menos:
   ```gitignore
   # Variables de entorno
   .env
   .env.local
   .env.production
   
   # Base de datos
   *.sqlite3
   *.db
   
   # Python
   __pycache__/
   *.pyc
   *.pyo
   
   # Entornos virtuales
   venv/
   .venv/
   env/
   
   # Media files
   media/
   
   # IDE
   .vscode/
   .idea/
   
   # Sistema
   .DS_Store
   Thumbs.db
   ```

3. **Usar .env.example en su lugar**
   - Crea un archivo `.env.example` con datos falsos:
   ```env
   # ARCHIVO DE EJEMPLO - NO CONTIENE DATOS REALES
   SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # MySQL Database Configuration
   DB_ENGINE=django.db.backends.mysql
   DB_NAME=nombre_de_tu_base_de_datos
   DB_USER=tu_usuario_mysql
   DB_PASSWORD=tu_contraseña_mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

#### **2. Verificar Proyecto con Script Automático**

Ejecuta el script de verificación:

**Windows:**
```powershell
.\check-github-ready.bat
```

**Linux/Mac:**
```bash
chmod +x check-github-ready.sh
./check-github-ready.sh
```

#### **3. Pasos para Subir a GitHub**

1. **Inicializar Git (si no lo has hecho)**
   ```powershell
   git init
   ```

2. **Configurar Git (primera vez)**
   ```powershell
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu-email@ejemplo.com"
   ```

3. **Agregar archivos al staging**
   ```powershell
   git add .
   ```

4. **Verificar qué se va a subir**
   ```powershell
   git status
   ```
   - **IMPORTANTE**: Verifica que NO aparezca `.env`

5. **Hacer commit inicial**
   ```powershell
   git commit -m "Initial commit: Aplicación de recetas Django completa"
   ```

6. **Crear repositorio en GitHub**
   - Ve a [github.com](https://github.com)
   - Clic en "New repository"
   - Nombre: `recetas-gourmet` (o el que prefieras)
   - Descripción: "Aplicación web premium para gestión de recetas"
   - Selecciona "Public" o "Private"
   - **NO** marques "Add a README file" (ya tienes uno)
   - Clic en "Create repository"

7. **Conectar con GitHub**
   ```powershell
   git remote add origin https://github.com/tu-usuario/recetas-gourmet.git
   git branch -M main
   git push -u origin main
   ```

---

### 🔧 **CONFIGURACIÓN AVANZADA DE GITHUB**

#### **1. Configurar GitHub Pages (Opcional)**
Para documentación online:
1. Ve a Settings → Pages
2. Selecciona "Deploy from a branch"
3. Branch: `main`, folder: `/docs`

#### **2. Configurar Actions (CI/CD)**
El proyecto incluye configuración de GitHub Actions:
- **Pruebas automáticas** en cada push
- **Verificación de código** con linting
- **Análisis de seguridad** con Bandit
- **Build de Docker** automático

#### **3. Configurar Dependabot**
Para actualizaciones automáticas de seguridad:
1. Ve a Settings → Security & analysis
2. Activa "Dependabot alerts"
3. Activa "Dependabot security updates"

#### **4. Configurar Branch Protection**
Para proteger la rama principal:
1. Ve a Settings → Branches
2. Add rule para `main`
3. Marca:
   - "Require pull request reviews"
   - "Require status checks"
   - "Require branches to be up to date"

---

### 🛠️ **HERRAMIENTAS INCLUIDAS**

#### **1. Scripts de Configuración**
- `setup.bat` / `setup.sh` - Configuración rápida
- `check-github-ready.bat` / `check-github-ready.sh` - Verificación pre-GitHub

#### **2. Docker (Opcional)**
Si quieres usar Docker:
```powershell
# Construir imagen
docker build -t recetas-gourmet .

# Ejecutar con Docker Compose
docker-compose up -d
```

#### **3. Configuración de Desarrollo**
- `.editorconfig` - Estilo de código consistente
- `.flake8` - Configuración de linting
- `pyproject.toml` - Configuración de herramientas Python

#### **4. GitHub Templates**
- `.github/ISSUE_TEMPLATE/` - Templates para issues
- `.github/PULL_REQUEST_TEMPLATE.md` - Template para PRs
- `.github/workflows/` - GitHub Actions

---

### 📚 **ARCHIVOS DE DOCUMENTACIÓN**

El proyecto incluye documentación profesional:

- **README.md** - Guía principal (este archivo)
- **CONTRIBUTING.md** - Guía para contribuir
- **SECURITY.md** - Política de seguridad
- **CHANGELOG.md** - Historial de cambios
- **LICENSE** - Licencia MIT

---

### 🔐 **MEJORES PRÁCTICAS DE SEGURIDAD**

#### **1. Nunca subas estos archivos:**
- `.env` - Variables de entorno reales
- `*.sqlite3` - Bases de datos con datos reales
- `*.log` - Logs que pueden contener información sensible
- `media/` - Archivos subidos por usuarios (pueden ser privados)

#### **2. Siempre incluye:**
- `.env.example` - Ejemplo de configuración
- `.gitignore` - Lista de archivos a ignorar
- `requirements.txt` - Dependencias exactas
- `README.md` - Documentación clara

#### **3. Configuración de producción:**
```env
# Producción
DEBUG=False
SECRET_KEY=clave-super-segura-generada-aleatoriamente
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

---

### 🎯 **DESPUÉS DE SUBIR A GITHUB**

#### **1. Configurar Colaboradores**
- Ve a Settings → Manage access
- Invita colaboradores si trabajas en equipo

#### **2. Configurar Webhooks (Opcional)**
Para despliegue automático:
- Settings → Webhooks
- Añade URL de tu servidor

#### **3. Configurar Issues y Projects**
- Activa Issues para reportes de bugs
- Usa Projects para organizar tareas

#### **4. Añadir Badges al README**
```markdown
[![Build Status](https://github.com/tu-usuario/recetas-gourmet/workflows/CI/badge.svg)](https://github.com/tu-usuario/recetas-gourmet/actions)
[![Coverage](https://codecov.io/gh/tu-usuario/recetas-gourmet/branch/main/graph/badge.svg)](https://codecov.io/gh/tu-usuario/recetas-gourmet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

---

### 🚀 **DESPLIEGUE EN PRODUCCIÓN**

#### **Opciones de Hosting:**
1. **Heroku** - Fácil para principiantes
2. **DigitalOcean** - VPS con más control
3. **AWS** - Escalable para proyectos grandes
4. **PythonAnywhere** - Especializado en Python

#### **Configuración básica para producción:**
```python
# settings.py adicional para producción
import os

# Seguridad
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Archivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

---

### 📋 **CHECKLIST FINAL**

Antes de subir a GitHub, verifica:

- [ ] `.env` NO está en Git
- [ ] `.env.example` existe con datos falsos
- [ ] `.gitignore` está configurado correctamente
- [ ] `requirements.txt` está actualizado
- [ ] Tests pasan correctamente
- [ ] README.md está completo
- [ ] No hay credenciales hardcodeadas en el código
- [ ] Archivos de documentación están presentes
- [ ] SECRET_KEY es diferente en producción

**¡Listo para subir a GitHub! 🚀**

---

## 📞 **SOPORTE Y COMUNIDAD**

### 🤝 **Contribuir al Proyecto**
- Fork el repositorio
- Crea una rama para tu feature
- Envía un Pull Request
- Revisa el archivo `CONTRIBUTING.md`

### 🐛 **Reportar Bugs**
- Usa los templates de GitHub Issues
- Incluye pasos para reproducir
- Proporciona información del entorno

### 💡 **Solicitar Funcionalidades**
- Abre un issue con el template correspondiente
- Describe el caso de uso
- Propone una solución

### 📚 **Documentación Adicional**
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [GitHub Docs](https://docs.github.com/)

---

## 📄 **LICENCIA**

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.

---

## 🎉 **CRÉDITOS**

- **Django** - Framework web
- **Django REST Framework** - API REST
- **Bootstrap** - Framework CSS
- **Font Awesome** - Iconos
- **Unsplash** - Imágenes de ejemplo

---

**¡Gracias por usar Recetas Gourmet! 🍽️✨**

Para cualquier duda o sugerencia, no dudes en crear un issue en GitHub.

---

*Proyecto desarrollado con ❤️ usando Django y las mejores prácticas de desarrollo web.*
