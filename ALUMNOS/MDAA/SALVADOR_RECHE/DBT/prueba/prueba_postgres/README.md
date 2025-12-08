# Proyecto DBT con PostgreSQL

Este es un proyecto DBT configurado para trabajar con PostgreSQL.

## Configuración

### Requisitos previos

- Docker y Docker Compose instalados

### Inicio rápido

1. **Construir y levantar los servicios**:
   ```bash
   cd prueba
   docker-compose up -d
   ```

2. **Ejecutar comandos DBT**:
   ```bash
   docker-compose exec dbt dbt debug
   docker-compose exec dbt dbt run
   docker-compose exec dbt dbt test
   ```

3. **Ver logs de PostgreSQL**:
   ```bash
   docker-compose logs postgres
   ```

## Estructura del proyecto

- `models/` - Modelos SQL de DBT
- `macros/` - Macros reutilizables
- `snapshots/` - Snapshots para captura de cambios
- `tests/` - Tests personalizados
- `analyses/` - Análisis ad-hoc
- `seeds/` - Datos de semilla (CSV)

## Configuración de PostgreSQL

### Variables de entorno

El proyecto utiliza un archivo `.env` para gestionar las credenciales de PostgreSQL de forma segura. 

**Antes de iniciar por primera vez**, asegúrate de que existe el archivo `.env` en la carpeta `prueba/`. Puedes copiarlo desde el archivo de ejemplo:

```bash
cd prueba
cp .env.example .env
```

Luego, edita el archivo `.env` y ajusta las credenciales según tus necesidades:

- **POSTGRES_HOST**: postgres (nombre del servicio en docker-compose)
- **POSTGRES_PORT**: 5432
- **POSTGRES_DB**: prueba_db
- **POSTGRES_USER**: prueba_user
- **POSTGRES_PASSWORD**: prueba_password (cambia esto por una contraseña segura)
- **POSTGRES_SCHEMA**: public

**Importante**: El archivo `.env` está incluido en `.gitignore` y no se subirá al repositorio. Nunca compartas tus credenciales.

### Tabla de inicialización

Al levantar el contenedor de PostgreSQL por primera vez, se crea automáticamente la tabla `calidad_aire` en el esquema `public`. Esta tabla está lista para trabajar con datos de calidad del aire.

**Nota importante**: Si ya tienes un volumen de PostgreSQL existente, la tabla no se recreará. Para forzar la recreación, elimina el volumen con:
```bash
docker-compose down -v
docker-compose up -d
```

## Recursos

- [Documentación de dbt](https://docs.getdbt.com/docs/introduction)
- [Discourse de dbt](https://discourse.getdbt.com/)
- [Comunidad de Slack](https://community.getdbt.com/)

