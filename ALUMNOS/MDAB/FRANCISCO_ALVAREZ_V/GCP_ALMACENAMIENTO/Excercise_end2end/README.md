# End-to-End GCP Data Pipeline Exercise

E-commerce data pipeline on GCP: orders generation → Pub/Sub → PostgreSQL → BigQuery → dbt → Metabase.

## Architecture

```text
orders-app (VM)
  ├── Generates synthetic orders via ChatGPT API
  ├── Writes to Cloud SQL (PostgreSQL) — customers, products, orders, order_products
  └── Publishes to Pub/Sub: order-events

delivery-app (VM)
  ├── Consumes order-events-sub
  └── Publishes delivery status (processing → delivering → delivered) to delivery-events

Pub/Sub BigQuery Subscription
  └── delivery-events → BigQuery delivery.raw_events_delivery

EL Pipeline (local)
  └── PostgreSQL → BigQuery orders.{customers,products,orders,order_products} (every 60s)

dbt (analytical_layer)
  ├── delivery/mart/expanded_delivery_events — view over raw delivery events
  └── analytics/orders_per_customer, top_5_product_expenses — aggregation tables

Metabase (Docker)
  └── Visualization layer on BigQuery
```

## Prerequisites

- GCP project with billing enabled
- `gcloud` CLI authenticated
- Terraform >= 1.0
- Python 3.9+
- Docker + Docker Compose
- dbt-bigquery

## Infrastructure Setup

### Option A — Terraform (recommended)

```sh
cd terraform
# Edit variables.tf — set service_account_email
terraform init
terraform plan
terraform apply
```

Provisions: 2 Compute VMs (orders-app, delivery-app), Cloud SQL PostgreSQL, Pub/Sub topics (order-events, delivery-events) and subscription.

Teardown:
```sh
terraform destroy
```

### Option B — Manual (gcloud)

#### Pub/Sub topics

```sh
gcloud pubsub topics create order-events
gcloud pubsub topics create delivery-events
```

#### Compute instances (replace placeholders)

```sh
gcloud compute instances create orders-app \
  --zone=europe-west1-b \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --subnet=projects/<PROJECT_ID>/regions/europe-west1/subnetworks/default \
  --machine-type=e2-micro \
  --source-machine-image=projects/<PROJECT_ID>/global/machineImages/<IMAGE_NAME> \
  --boot-disk-size=10GB

gcloud compute instances create delivery-app \
  --zone=europe-west1-b \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --subnet=projects/<PROJECT_ID>/regions/europe-west1/subnetworks/default \
  --machine-type=e2-micro \
  --source-machine-image=projects/<PROJECT_ID>/global/machineImages/<IMAGE_NAME> \
  --boot-disk-size=10GB
```

#### Cloud SQL

```sh
gcloud sql instances create edem-postgres \
  --database-version=POSTGRES_16 \
  --tier=db-f1-micro \
  --edition=ENTERPRISE \
  --region=europe-west1 \
  --availability-type=zonal \
  --storage-size=10 \
  --no-deletion-protection \
  --authorized-networks=0.0.0.0/0 \
  --root-password=Edem2526#

gcloud sql users create postgres --instance=edem-postgres --password=EDEM2526
gcloud sql databases create ecommerce --instance=edem-postgres
```

## BigQuery Setup

### Orders dataset

```sql
CREATE TABLE IF NOT EXISTS `orders.customers` (id INT64, customer_name STRING, email STRING);
CREATE TABLE IF NOT EXISTS `orders.products` (id INT64, product_name STRING, price FLOAT64);
CREATE TABLE IF NOT EXISTS `orders.orders` (id INT64, customer_id INT64, created_at TIMESTAMP, total_price FLOAT64);
CREATE TABLE IF NOT EXISTS `orders.order_products` (order_id INT64, product_id INT64, quantity INT64, price FLOAT64);
```

### Delivery dataset

```sql
CREATE TABLE IF NOT EXISTS `delivery.raw_events_delivery` (
    subscription_name STRING,
    message_id STRING,
    publish_time TIMESTAMP,
    data JSON,
    attributes JSON
)
PARTITION BY DATE(publish_time)
CLUSTER BY subscription_name, message_id
OPTIONS (labels=[('source','bq_subs')]);
```

Then create a BigQuery subscription on the `delivery-events` topic pointing to `delivery.raw_events_delivery` (type: Write to BigQuery, write metadata, no schema). Grant the subscription SA `roles/bigquery.dataEditor` if prompted.

## Running the Apps

SSH into each VM, then:

```sh
gcloud compute ssh <instance-name> --zone=europe-west1-b
cd EDEM2526 && git pull
cd gcp_datawarehouse/excercise_end2end
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### orders-app

```sh
nohup bash -c 'HOST_IP=<CLOUD_SQL_IP> PROJECT_ID=<PROJECT_ID> python -m orders_app.orders_to_db.main' > output.log 2>&1 &
tail -f output.log
```

### delivery-app

```sh
nohup bash -c 'PROJECT_ID=<PROJECT_ID> python -m delivery_app.main' > output.log 2>&1 &
tail -f output.log
```

## EL Pipeline (PostgreSQL → BigQuery)

Run locally. Syncs every 60 seconds.

```sh
# Linux/Mac
POSTGRES_IP=<IP> GCP_PROJECT=<PROJECT_ID> python -m analytical_layer.el_orders.main

# Windows CMD
set POSTGRES_IP=<IP> && set GCP_PROJECT=<PROJECT_ID> && python -m analytical_layer.el_orders.main

# Windows PowerShell
$env:POSTGRES_IP="<IP>"; $env:GCP_PROJECT="<PROJECT_ID>"; python -m analytical_layer.el_orders.main
```

Requires application-default credentials:
```sh
gcloud auth application-default login
```

## dbt Analytical Layer

```sh
pip install dbt-bigquery
dbt init edem_project        # run inside analytical_layer/dbt_template/
```

Copy template files from `analytical_layer/dbt_template/edem_project/` into your project, then:

```sh
dbt run --select expanded_delivery_events   # delivery view
dbt run --select analytics                  # aggregation tables
```

## Metabase (Visualization)

```sh
cd analytical_layer
docker-compose up -d
```

Open [http://localhost:3000](http://localhost:3000). Connect to BigQuery using your GCP project credentials.

## Project Structure

```text
.
├── orders_app/
│   ├── chatgpt_orders/orders_handler.py   # synthetic order generation
│   └── orders_to_db/main.py               # writes to PostgreSQL + publishes to order-events
├── delivery_app/
│   └── main.py                            # consumes order-events, publishes delivery status
├── utils/
│   ├── events_manager.py                  # Pub/Sub publisher/subscriber wrapper
│   └── db_manager_utils.py                # PostgreSQL + BigQuery connection manager
├── analytical_layer/
│   ├── el_orders/main.py                  # EL: PostgreSQL → BigQuery sync
│   ├── dbt_template/edem_project/         # dbt models and macros
│   └── docker-compose.yml                 # Metabase
├── terraform/                             # IaC for GCP resources
└── requirements.txt
```

## Environment Variables

| Variable | Used by | Description |
| --- | --- | --- |
| `HOST_IP` | orders-app | Cloud SQL public IP |
| `PROJECT_ID` | orders-app, delivery-app | GCP project ID |
| `POSTGRES_IP` | EL pipeline | Cloud SQL public IP |
| `GCP_PROJECT` | EL pipeline | GCP project ID |
