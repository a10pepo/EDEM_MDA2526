La idea al hacer el despliegue en AWS es que esté todo bajo la prueba gratuita y no me cobren nada.

# El proyecto es el backend de un E-commerce para una tienda de ropa.

Objetivo del negocio:
La aplicación debe gestionar el catálogo de ropa (con soporte para categorías, tallas y colores), el inventario, y el procesamiento de pedidos. Debe exponer una API REST limpia y escalable.

### Stack Técnico (Free-Tier friendly):

Lenguaje: Python.

Backend/API: FastAPI (con Pydantic para validación y SQLAlchemy o SQLModel para el ORM).

Base de Datos: PostgreSQL (diseño relacional para usuarios, productos, variantes y pedidos).

Almacenamiento de Medios: Amazon S3 (para guardar y servir las imágenes de los productos).

Infraestructura en AWS: Terraform (IaC) y Docker. Todo debería levantarse en AWS al hacer el terraform apply.
Arquitectura en AWS esperada (Totalmente administrada):
Base de Datos: Amazon RDS (PostgreSQL).
Almacenamiento: Amazon S3 (Bucket público/protegido para las imágenes del catálogo).

Tus tareas paso a paso:

### Planificación:
Confirma que entiendes la arquitectura. Propón el diseño del esquema de la base de datos relacional (tablas para Products, ProductVariants para tallas/colores, Orders, OrderItems) y la estructura de carpetas del proyecto. Espera mi 'ok'.

### Desarrollo Local:
Escribe el código en Python (los modelos de la base de datos, los endpoints de la API en FastAPI para consultar catálogo y crear pedidos) y un archivo docker-compose.yml para probar la API y Postgres en local.

Infraestructura (Terraform): Crea los archivos .tf necesarios para levantar de forma automatizada la VPC, el RDS de Postgres, el bucket de S3 y el servicio de contenedores en AWS.

### Instrucciones de despliegue:
Dame los comandos exactos para empaquetar la aplicación en Docker, subirla a AWS ECR y aplicar el plan de Terraform.

Empieza por el paso 1, mostrando la estructura de archivos propuesta y el diseño del modelo de datos para las prendas de ropa.
