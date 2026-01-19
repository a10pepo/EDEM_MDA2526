# 🚀 SpaceX Launch Analytics
**Autor: Ricardo Edreira**

## Descripción

Proyecto DBT que analiza **205 lanzamientos históricos de SpaceX** (2006-2024) para responder preguntas de negocio.

## Fuente de Datos

**API pública de SpaceX v4** - https://api.spacexdata.com/v4/

| Datos | Cantidad |
|-------|----------|
| Lanzamientos | 205 |
| Cohetes | 4 (Falcon 1, Falcon 9, Falcon Heavy, Starship) |
| Plataformas | 6 (Florida, California, Marshall Islands) |

## Arquitectura

```
BRONZE (Seeds)          SILVER (Staging)         GOLD (Marts)
──────────────          ────────────────         ────────────
raw_launches     →      stg_launches      →      launches_summary
raw_rockets      →      stg_rockets       →      rocket_performance
raw_launchpads   →      stg_launchpads    →      launchpad_stats
```

## Modelos

### Staging
| Modelo | Descripción |
|--------|-------------|
| `stg_launches` | Parseo de fechas, normalización de booleanos |
| `stg_rockets` | Conversión de tipos numéricos |
| `stg_launchpads` | Cálculo de tasas de éxito |

### Marts
| Modelo | Pregunta que responde |
|--------|----------------------|
| `launches_summary` | ¿Cómo evolucionó la frecuencia por año? |
| `rocket_performance` | ¿Cuál es la tasa de éxito por cohete? |
| `launchpad_stats` | ¿Qué plataforma tiene mejor rendimiento? |

## Comandos

### 1. Ingesta de datos (opcional)
```bash
python scripts/download_spacex_data.py
```

### 2. Ejecutar DBT
```bash
dbt seed                    # Cargar datos
dbt run                     # Ejecutar modelos
dbt test                    # Ejecutar tests
dbt docs generate --static  # Generar documentación
```

## Entrega

Subir: `target/static_index.html`
