FROM python:3.11-slim

RUN pip install --no-cache-dir dbt-core dbt-duckdb

WORKDIR /app
COPY car_sales_dbt /app

CMD ["bash", "-c", "dbt seed --profiles-dir . && dbt run --profiles-dir . && dbt test --profiles-dir . && dbt docs generate --profiles-dir . && tail -f /dev/null"]
