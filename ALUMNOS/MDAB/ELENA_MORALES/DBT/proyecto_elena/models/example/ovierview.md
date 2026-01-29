{% docs __overview__ %}

# ⚽ Proyecto de Análisis de Fútbol Internacional

### Resumen
Este proyecto de dbt procesa datos históricos de partidos de fútbol internacional (desde 1872 hasta 2024) para responder preguntas clave sobre el rendimiento de selecciones y jugadores.

### 🗂️ Estructura del Proyecto

El proyecto transforma los datos crudos en tablas listas para el análisis:

* **Staging**: Limpieza básica de datos, estandarización de fechas y traducción de columnas al inglés.
* **Marts**: Tablas de negocio agregadas para responder preguntas específicas.

### 📊 Modelos Principales

1. **top_scorers**: Ranking de los máximos goleadores de la historia. Permite analizar quiénes han marcado más goles y cuántos de ellos fueron de penalti.
2. **team_stats**: Visión 360º de cada selección nacional. Incluye victorias totales (local y visitante) y goles a favor.

### 📚 Fuente de Datos
Los datos provienen del dataset público de Kaggle "International football results from 1872 to 2024".

{% enddocs %}