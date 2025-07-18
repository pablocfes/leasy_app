# Leasy - Sistema de Gestión de Contratos y Facturación


Leasy es un sistema web construido con Django 5.2 para la gestión de clientes, vehículos, contratos y facturas, con capacidades de carga de archivos Excel/CSV y generación de reportes.

## Características principales

* ✅ Autenticación de usuarios por email
* 🚗 Gestión de clientes, vehículos y contratos
* 📄 Generación automática de facturas (invoices)
* 📊 Dashboard con listado paginado y buscador
* 📤 Carga masiva de datos mediante archivos Excel/CSV
* 📥 Generación de reportes personalizados en Excel
* 💻 Interfaz responsive con Bootstrap 5+

## Requerimientos técnicos

* Python 3.10+
* Django 5.2
* Bootstrap 5+
* PostgreSQL (recomendado) o SQLite
* Librerías adicionales (ver `requirements.txt`)

## Instalación

1. **Clonar el repositorio** :
   **bash**

```
   git clone https://github.com/pablocfes/leasy_app.git
   cd leasy
```

2. **Crear y activar entorno virtual** (recomendado):
   **bash**

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias** :
   **bash**

```
   pip install -r requirements.txt
```

4. **Configurar base de datos** :

* Crear una base de datos PostgreSQL o usar SQLite
* Configurar las variables de conexión en `settings.py`

5. **Migraciones y superusuario** :
   **bash**

```
   python manage.py migrate
   python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo** :
   **bash**

```
   python manage.py runserver
```

7. **Acceder al sistema** :
   **text**

```
   http://localhost:8000/
```

## Estructura del proyecto

**text**

```
leasy/
├── core/               # App principal
├── clientes/           # Gestión de clientes
├── contratos/          # Gestión de contratos
├── vehiculos/               # Gestión de vehículos
├── invoices/           # Gestión de facturas
├── reportes/            # Generación de reportes
├── static/             # Archivos estáticos
├── templates/          # Plantillas HTML
├── manage.py
└── requirements.txt
```

## Uso del sistema

1. **Autenticación** :

* Iniciar sesión con email y contraseña
* Usuarios no autenticados son redirigidos al login

2. **Dashboard** :

* Listado paginado de contratos (20 por página)
* Buscador por nombre, apellido, documento o vehículo

3. **Carga de archivos** :

* Subir archivos Excel/CSV con datos
* Validación de columnas requeridas

4. **Reportes** :

* Seleccionar columnas para el reporte
* Generar y descargar reporte en Excel

## Optimizaciones implementadas

* Uso de `select_related` y `prefetch_related` para optimizar queries
* Paginación para manejo de grandes volúmenes de datos
* Class-Based Views para mejor organización del código
* Separación de lógica de negocio de las vistas

## Licencia

Este proyecto está bajo licencia MIT. Ver el archivo LICENSE para más detalles.
