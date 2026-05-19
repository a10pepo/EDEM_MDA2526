# Proyecto End-to-End: Martha Segura

* **Pub/Sub Topics:** Creación de `order-events` y `delivery-events`.
![Tópicos de Pub/Sub](00-topics.png)

* **Compute Engine:** Instancias `orders-app` y `delivery-app` operativas.
![Instancias VM](01-instances.png)

Configuración de la base de datos operacional PostgreSQL en Cloud SQL.
![Cloud SQL Instance](02-database.png)

* **Orders App:** Insertando registros en Cloud SQL y publicando en Pub/Sub.
![Logs de Envío](03-sending.png)

* **Delivery App:** Consumiendo eventos de `order-events`.
![Logs de Consumo](04-consuming.png)

## Transformación de Datos con dbt (Capa Analítica)
![Configuración dbt](05-dbt.png)[alt text](<05- dbt-bigquery.png>)

## Visualización y BI
Despliegue de Metabase mediante Docker y conexión con el Data Warehouse (BigQuery) utilizando una Service Account de GCP.
![Conexión Metabase](06-metabase.png)

## Dasboard final
![alt text](07-visualizacion.png)