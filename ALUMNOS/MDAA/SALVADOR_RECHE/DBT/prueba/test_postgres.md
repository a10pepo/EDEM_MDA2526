# Guía de Pruebas de PostgreSQL

## Paso 1: Construir y levantar los contenedores

```bash
cd prueba
docker-compose build
docker-compose up -d
```

## Paso 2: Verificar que los contenedores estén corriendo

```bash
docker-compose ps
```

Deberías ver ambos contenedores (postgres y dbt) en estado "Up".

## Paso 3: Verificar que PostgreSQL esté funcionando

```bash
# Ver logs de PostgreSQL
docker-compose logs postgres

# Conectarse directamente a PostgreSQL
docker-compose exec postgres psql -U prueba_user -d prueba_db
```

Una vez dentro de PostgreSQL, puedes ejecutar:

```sql
-- Ver todas las tablas
\dt

-- Verificar que la tabla calidad_aire existe
SELECT * FROM calidad_aire LIMIT 5;

-- Ver la estructura de la tabla
\d calidad_aire

-- Salir de PostgreSQL
\q
```

## Paso 4: Probar la conexión desde DBT

```bash
# Verificar la configuración de DBT
docker-compose exec dbt dbt debug

# Esto debería mostrar que la conexión a PostgreSQL es exitosa
```

## Paso 5: Ejecutar un modelo de prueba

```bash
# Ejecutar el modelo de ejemplo
docker-compose exec dbt dbt run --models my_first_model

# Ver todos los modelos disponibles
docker-compose exec dbt dbt list
```

## Paso 6: Consultar la tabla calidad_aire desde DBT

Puedes crear un modelo simple para consultar la tabla:

```sql
-- models/staging/staging__calidad_aire.sql
SELECT * FROM public.calidad_aire LIMIT 10
```

Luego ejecutar:
```bash
docker-compose exec dbt dbt run --models staging__calidad_aire
```

## Comandos útiles

```bash
# Detener los contenedores
docker-compose stop

# Detener y eliminar los contenedores (pero mantener volúmenes)
docker-compose down

# Detener y eliminar TODO (incluyendo volúmenes - esto eliminará la base de datos)
docker-compose down -v

# Ver logs en tiempo real
docker-compose logs -f postgres
```

## Solución de problemas

Si hay errores:

1. **Verificar el archivo .env**: Asegúrate de que existe y tiene los valores correctos
2. **Ver logs**: `docker-compose logs postgres`
3. **Reiniciar**: `docker-compose restart`
4. **Reconstruir desde cero**: `docker-compose down -v && docker-compose up -d`

