# Tienda Universitaria - Aplicación Web con Docker

Esta es una aplicación web completa para una tienda de merchandising universitario, construida con una arquitectura frontend-backend y desplegada con Docker Compose.

## Arquitectura

La aplicación está compuesta por 6 contenedores:

1. **Frontend**: Aplicación web con HTML, CSS y JavaScript servida por Nginx (Puerto 8080)
2. **Backend**: API REST desarrollada en Flask (Puerto 5001)
3. **PostgreSQL**: Base de datos (Puerto 5432)
4. **pgAdmin**: Herramienta de administración de la base de datos (Puerto 5050)
5. **Data Generator**: Generador de datos históricos de pedidos (se ejecuta una vez al inicio)
6. **Grafana**: Dashboard de análisis y visualización de ventas (Puerto 3000)

## Requisitos Previos

- Docker
- Docker Compose

## Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
cd /ruta/del/proyecto
```

### 2. Levantar todos los servicios

```bash
docker-compose up -d
```

Este comando descargará las imágenes necesarias, construirá los contenedores y levantará todos los servicios.

### 3. Acceder a la aplicación

Una vez que todos los contenedores estén corriendo, puedes acceder a:

- **Tienda Web**: http://localhost:8080
- **API Backend**: http://localhost:5001
- **pgAdmin**: http://localhost:5050
- **Grafana**: http://localhost:3000

## Accesos y Credenciales

### Grafana (Dashboard de Análisis)
- **URL**: http://localhost:3000
- **Usuario**: admin
- **Contraseña**: admin
- El dashboard "Tienda Universitaria - Análisis de Ventas" se cargará automáticamente

### pgAdmin
- **URL**: http://localhost:5050
- **Email**: admin@admin.com
- **Password**: admin

#### Configurar conexión a PostgreSQL en pgAdmin:
1. Hacer clic en "Add New Server"
2. En la pestaña "General", dar un nombre (ej: "Tienda DB")
3. En la pestaña "Connection":
   - **Host**: db
   - **Port**: 5432
   - **Database**: tienda_db
   - **Username**: user
   - **Password**: password

### Base de Datos PostgreSQL
- **Host**: localhost (desde tu máquina) o "db" (desde otros contenedores)
- **Puerto**: 5432
- **Base de datos**: tienda_db
- **Usuario**: user
- **Contraseña**: password

## Funcionalidades de la Tienda

### Vista de Cliente
1. **Catálogo de Productos**: Ver todos los productos disponibles con imágenes, precios y stock
2. **Filtro por Categoría**: Filtrar productos por categoría (Ropa, Accesorios, Papelería)
3. **Carrito de Compras**:
   - Añadir productos al carrito
   - Modificar cantidades
   - Eliminar productos
   - Ver total del pedido
4. **Finalizar Compra**: Completar el pedido con datos del cliente

### Panel de Administración
Accede al panel haciendo clic en "Panel Admin" en la cabecera.

1. **Gestión de Productos**:
   - Crear nuevos productos
   - Editar productos existentes
   - Eliminar productos
   - Ver stock disponible

2. **Gestión de Pedidos**:
   - Ver todos los pedidos realizados
   - Ver detalles de cada pedido
   - Ver estado de los pedidos

## API Endpoints

### Productos
- `GET /api/productos` - Obtener todos los productos
- `GET /api/productos/<id>` - Obtener un producto específico
- `POST /api/productos` - Crear un nuevo producto
- `PUT /api/productos/<id>` - Actualizar un producto
- `DELETE /api/productos/<id>` - Eliminar un producto

### Pedidos
- `GET /api/pedidos` - Obtener todos los pedidos
- `GET /api/pedidos/<id>` - Obtener un pedido específico
- `POST /api/pedidos` - Crear un nuevo pedido
- `PUT /api/pedidos/<id>` - Actualizar estado de un pedido

### Utilidades
- `GET /health` - Verificar estado de la API
- `POST /api/init-data` - Inicializar datos de ejemplo

## Estructura del Proyecto

```
.
├── backend/
│   ├── app.py              # Aplicación Flask principal
│   ├── models.py           # Modelos de base de datos
│   ├── config.py           # Configuración
│   ├── requirements.txt    # Dependencias Python
│   └── Dockerfile          # Dockerfile del backend
├── frontend/
│   ├── index.html          # Página principal
│   ├── styles.css          # Estilos
│   ├── app.js              # Lógica JavaScript
│   ├── nginx.conf          # Configuración Nginx
│   └── Dockerfile          # Dockerfile del frontend
├── docker-compose.yml      # Orquestación de contenedores
└── README.md              # Este archivo
```

## Gestión de Contenedores

### Ver estado de los contenedores
```bash
docker-compose ps
```

### Ver logs de todos los servicios
```bash
docker-compose logs -f
```

### Ver logs de un servicio específico
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Detener todos los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes (base de datos)
```bash
docker-compose down -v
```

### Reconstruir los contenedores después de cambios
```bash
docker-compose up -d --build
```

## Datos Iniciales

La primera vez que accedas a la aplicación, se cargarán automáticamente 6 productos de ejemplo:
- Camiseta Universidad
- Sudadera
- Taza Universidad
- Bolígrafo
- Mochila
- Gorra

Si necesitas reinicializar los datos, puedes hacerlo desde el código o ejecutando:
```bash
curl -X POST http://localhost:5001/api/init-data
```

## Datos Históricos y Análisis

### Generador de Datos Históricos

El contenedor `data-generator` se ejecuta automáticamente al levantar la aplicación y genera:
- Entre 150 y 250 pedidos aleatorios
- Distribuidos en los últimos 90 días
- Con 30 clientes únicos
- Incluye pedidos completados, pendientes y cancelados
- Asigna productos aleatorios a cada pedido

El generador verifica que ya existan productos en la base de datos y solo se ejecuta si hay menos de 10 pedidos existentes.

### Dashboard de Grafana

Accede a Grafana en http://localhost:3000 (admin/admin) para visualizar:

**Métricas Principales:**
- Ventas totales en euros
- Total de pedidos
- Pedidos completados
- Pedidos pendientes

**Gráficos de Análisis:**
- Evolución de ventas por día
- Distribución de ventas por categoría (gráfico de pastel)
- Top 10 productos más vendidos
- Compras por usuario (top 15 clientes)
- Evolución de pedidos por estado

El dashboard se configura automáticamente al iniciar el contenedor de Grafana.

## Tecnologías Utilizadas

### Backend
- Python 3.11
- Flask 3.0
- Flask-SQLAlchemy
- Flask-CORS
- PostgreSQL 15
- psycopg2

### Frontend
- HTML5
- CSS3
- JavaScript (Vanilla)
- Nginx

### Infraestructura
- Docker
- Docker Compose
- pgAdmin 4
- Grafana (Dashboard y visualización)

## Solución de Problemas

### Los contenedores no se inician
1. Verifica que Docker esté corriendo
2. Verifica que los puertos no estén ocupados (8080, 5001, 3000, 5432, 5050)
3. Revisa los logs: `docker-compose logs`

### Error de conexión a la base de datos
1. Espera unos segundos después de iniciar los contenedores
2. Verifica que el contenedor de PostgreSQL esté corriendo: `docker-compose ps`
3. Revisa los logs del backend: `docker-compose logs backend`

### El frontend no carga los productos
1. Verifica que el backend esté corriendo: http://localhost:5001/health
2. Abre la consola del navegador (F12) y busca errores
3. Verifica que no haya problemas de CORS

### Cambios en el código no se reflejan
1. Reconstruye los contenedores: `docker-compose up -d --build`
2. Para el frontend, limpia la caché del navegador

## Mejoras Futuras

- Autenticación de usuarios
- Pasarela de pago real
- Sistema de valoraciones y comentarios
- Panel de estadísticas y reportes
- Notificaciones por email
- Implementación de búsqueda de productos
- Gestión de imágenes con upload

## Licencia

Este proyecto es un ejercicio educativo para uso académico.
