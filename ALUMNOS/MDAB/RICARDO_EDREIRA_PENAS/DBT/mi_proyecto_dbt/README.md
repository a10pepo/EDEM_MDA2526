# 🚀 SpaceX Launch Analytics
**Autor: Ricardo Edreira**

## Descripción

Proyecto DBT que analiza **205 lanzamientos históricos de SpaceX** (2006-2024) para responder preguntas de negocio sobre rendimiento de cohetes y plataformas.

## Fuente de Datos

**API pública de SpaceX v4** - https://api.spacexdata.com/v4/

| Datos | Cantidad |
|-------|----------|
| Lanzamientos | 205 |
| Cohetes | 4 (Falcon 1, Falcon 9, Falcon Heavy, Starship) |
| Plataformas | 6 (Florida, California, Marshall Islands) |

## Arquitectura (Medallion)

```
BRONZE (Seeds)          SILVER (Staging)         GOLD (Marts)
──────────────          ────────────────         ────────────
raw_launches     →      stg_launches      →      launches_summary
raw_rockets      →      stg_rockets       →      rocket_performance
raw_launchpads   →      stg_launchpads    →      launchpad_stats
```

## Modelos

### Staging (Limpieza)
| Modelo | Descripción |
|--------|-------------|
| `stg_launches` | Parseo de fechas, normalización de campos booleanos |
| `stg_rockets` | Conversión de tipos, limpieza de texto |
| `stg_launchpads` | Cálculo de coordenadas y tasas de éxito |

### Marts (Analíticos)
| Modelo | Pregunta que responde |
|--------|----------------------|
| `launches_summary` | ¿Cómo evolucionó la frecuencia de lanzamientos por año? |
| `rocket_performance` | ¿Cuál es la tasa de éxito de cada cohete? |
| `launchpad_stats` | ¿Qué plataforma tiene mejor rendimiento? |

## Comandos

```bash
dbt seed                    # Cargar datos CSV
dbt run                     # Ejecutar modelos
dbt test                    # Ejecutar tests (16 tests)
dbt docs generate --static  # Generar documentación
```

## Entrega

Subir el archivo: `target/static_index.html`
