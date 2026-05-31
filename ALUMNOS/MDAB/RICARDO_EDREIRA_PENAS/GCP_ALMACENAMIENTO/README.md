# Entregable End2End GCP Almacenamiento

Despliegue de una arquitectura end2end en Google Cloud Platform.

---

## 1. Orders App y Delivery App — Compute Engine

Despliegue de las dos aplicaciones como instancias de VM en Compute Engine (`delivery-app` y `orders-app`).

![Compute Engine](images/compute_engine.png)

---

## 2. Pub/Sub

Creacion de los topicos `delivery-events` y `order-events` con sus suscriptores.

![Pub/Sub](images/pubsub.png)

---

## 3. Cloud SQL

Instancia PostgreSQL 16 (`edem-postgres`) desplegada en Cloud SQL.

![Cloud SQL](images/cloud_sql.png)

---

## 4. BigQuery

Data Warehouse con los datasets de la capa analitica: `orders`, `orders_analytics`, `delivery`, `delivery_mart`, `orders_delivery_mart`.

![BigQuery](images/bigquery.png)

---

## 5. DBT

Ejecucion de `dbt run --full-refresh` con los 5 modelos completados correctamente.

![DBT](images/dbt.png)

---

## 6. Metabase

Dashboard desplegado en local con Docker Compose, conectado a BigQuery, mostrando pedidos por cliente y top 5 productos por gasto.

![Metabase](images/metabase.png)

---

## Autor

Ricardo Edreira Penas — EDEM MDA 2025/26
