# AWS_Almacenamiento

Este repositorio contiene una API FastAPI preparada para el entregable de AWS con una arquitectura simple y clara:

- base de datos relacional para la capa transaccional,
- exportación de datos a CSV,
- preparación para S3 y para un flujo de lakehouse con Glue/Iceberg,
- y despliegue en EC2.

## Estructura del proyecto

- app/: lógica principal de la aplicación
  - api.py: endpoints FastAPI
  - database.py: conexión a la base de datos
  - models.py: modelos SQLAlchemy
  - schemas.py: validación con Pydantic
  - seed_data.py: datos iniciales
  - seed_db.py: carga de datos inicial
- scripts/: utilidades para AWS
  - export_to_s3.py: exporta tablas a CSV y prepara la subida a S3
  - glue_iceberg_setup.py: configuración base para Glue/Iceberg
- tests/: pruebas básicas del flujo de exportación
- exports/: archivos CSV generados localmente

## Ejecutar la API localmente

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.api:app --host 127.0.0.1 --port 8000
```

## Exportar datos

```bash
python scripts/export_to_s3.py
```

## Arquitectura propuesta para el entregable

- RDS: base de datos transaccional
- S3: almacenamiento de exportaciones
- Glue + Iceberg: capa lakehouse/analítica
- EC2: despliegue de la API

## Estado del proyecto

La app ya está funcionando localmente y los scripts de exportación están verificados.
