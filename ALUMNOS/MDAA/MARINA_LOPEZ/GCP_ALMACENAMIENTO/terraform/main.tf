# DELIVERY APP VM
resource "google_compute_instance_from_machine_image" "delivery_app" {
  name           = "delivery-app"
  provider       = google-beta
  zone           = var.zone
  source_machine_image  = "projects/${var.project_id}/global/machineImages/orders-app-img"
  machine_type   = "e2-micro"

  network_interface {
    subnetwork = var.subnetwork
    access_config {
        // Ephemeral IP
    }
  }

  service_account {
    email  = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
    ]
  }
  allow_stopping_for_update = true
}

# ORDERS APP VM
resource "google_compute_instance_from_machine_image" "orders_app" {
  name           = "orders-app"
  provider       = google-beta
  zone           = var.zone
  source_machine_image  = "projects/${var.project_id}/global/machineImages/orders-app-img"
  machine_type   = "e2-micro"

  network_interface {
    subnetwork = var.subnetwork
    access_config {
        // Ephemeral IP
    }
  }

  service_account {
    email  = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
    ]
  }

  allow_stopping_for_update = true
}

# order_events Pub/Sub topic and subscription
resource "google_pubsub_topic" "order_events" {
  name = "order-events"
}

resource "google_pubsub_subscription" "order_events_sub" {
  name  = "${google_pubsub_topic.order_events.name}-sub"
  topic = google_pubsub_topic.order_events.name
}

# delivery_events Pub/Sub topic
resource "google_pubsub_topic" "delivery_events" {
  name = "delivery-events"
}


# Postgres SQL instance
resource "google_sql_database_instance" "postgres_instance" {
  name             = "e2e"
  region           = var.region
  database_version = "POSTGRES_15"
  settings {
    tier            = "db-f1-micro"
    availability_type = "ZONAL"
    disk_size       = 100 # GB
    # deletion_protection = false

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "public-access"
        value = "0.0.0.0/0"
      }
    }
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "google_sql_user" "postgres_user" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres_instance.name
  password = "Edem2526."
}

resource "google_sql_database" "ecommerce" {
  name     = "ecommerce"
  instance = google_sql_database_instance.postgres_instance.name
}


# BigQuery Resources
resource "google_bigquery_dataset" "orders_bronze" {
  dataset_id  = "orders_bronze"
  project     = var.project_id
  location    = "europe-west1"
}

resource "google_bigquery_dataset" "delivery_bronze" {
  dataset_id  = "delivery_bronze"
  project     = var.project_id
  location    = "europe-west1"
}

resource "google_bigquery_table" "customers" {
  dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
  table_id   = "customers"

  schema = <<EOF
[
  {"name": "id", "type": "INT64"},
  {"name": "customer_name", "type": "STRING"},
  {"name": "email", "type": "STRING"}
]
EOF
}

resource "google_bigquery_table" "products" {
  dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
  table_id   = "products"

  schema = <<EOF
[
  {"name": "id", "type": "INT64"},
  {"name": "product_name", "type": "STRING"},
  {"name": "price", "type": "FLOAT64"}
]
EOF
}

resource "google_bigquery_table" "orders" {
  dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
  table_id   = "orders"

  schema = <<EOF
[
  {"name": "id", "type": "INT64"},
  {"name": "customer_id", "type": "INT64"},
  {"name": "created_at", "type": "TIMESTAMP"},
  {"name": "total_price", "type": "FLOAT64"}
]
EOF
}

resource "google_bigquery_table" "order_products" {
  dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
  table_id   = "order_products"

  schema = <<EOF
[
  {"name": "order_id", "type": "INT64"},
  {"name": "product_id", "type": "INT64"},
  {"name": "quantity", "type": "INT64"},
  {"name": "price", "type": "FLOAT64"}
]
EOF
}

resource "google_bigquery_table" "raw_events_delivery" {
  dataset_id = google_bigquery_dataset.delivery_bronze.dataset_id
  table_id   = "raw_events_delivery"

  schema = <<EOF
[
  {"name": "subscription_name", "type": "STRING"},
  {"name": "message_id", "type": "STRING"},
  {"name": "publish_time", "type": "TIMESTAMP"},
  {"name": "data", "type": "JSON"},
  {"name": "attributes", "type": "JSON"}
]
EOF

  time_partitioning {
    type = "DAY"
    field = "publish_time"
  }

  clustering = ["subscription_name", "message_id"]

  labels = {
    source = "bq_subs"
  }
}

# Pub/Sub Subscription to BigQuery
resource "google_pubsub_subscription" "delivery_events_bq_sub" {
  depends_on = [
    google_bigquery_table.raw_events_delivery,
    google_pubsub_topic.delivery_events_dead_letter,
    google_pubsub_subscription.delivery_events_dead_letter_sub
  ]

  name  = "delivery-events-bq-sub"
  topic = google_pubsub_topic.delivery_events.name

  bigquery_config {
    table               = "${var.project_id}:${google_bigquery_dataset.delivery_bronze.dataset_id}.raw_events_delivery"
    use_table_schema    = false
    write_metadata      = true
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.delivery_events_dead_letter.id
    max_delivery_attempts = 5
  }
}

# Dead Letter Topic and Subscription
resource "google_pubsub_topic" "delivery_events_dead_letter" {
  name = "delivery-events-dead-letter"
}

resource "google_pubsub_subscription" "delivery_events_dead_letter_sub" {
  name  = "delivery-events-dead-letter-sub"
  topic = google_pubsub_topic.delivery_events_dead_letter.name
}



# --- STOCK APP INFRASTRUCTURE ---

# Stock APP VM
resource "google_compute_instance_from_machine_image" "stock_app" {
  name           = "stock-app"
  provider       = google-beta
  zone           = var.zone
  source_machine_image  = "projects/${var.project_id}/global/machineImages/orders-app-img"
  machine_type   = "e2-micro"

  network_interface {
    subnetwork = var.subnetwork
    access_config {
        // Ephemeral IP
    }
  }

  service_account {
    email  = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
    ]
  }
  allow_stopping_for_update = true
}

# Pub/Sub topic and subscription

resource "google_pubsub_topic" "stock_alerts" {
  name = "stock-alerts"
}

# Suscripción para Leer Pedidos --> Conectamos la Stock App al topic de "order-events"

resource "google_pubsub_subscription" "stock_subscription" {
  name  = "stock-sub"                         
  topic = google_pubsub_topic.order_events.name 
}

# Suscripción para VER las alertas (Test)
resource "google_pubsub_subscription" "stock_alerts_sub_test" {
  name  = "stock-alerts-sub-test"
  topic = google_pubsub_topic.stock_alerts.name
}


# Crear dataset y la tabla vacía en BigQuery para recibir alertas
resource "google_bigquery_dataset" "stock_bronze" {
  dataset_id  = "stock_bronze"
  project     = var.project_id
  location    = "europe-west1"
}
resource "google_bigquery_table" "stock_alerts" {
  dataset_id = google_bigquery_dataset.stock_bronze.dataset_id
  table_id   = "stock_alerts"

  schema = <<EOF
[
  {"name": "subscription_name", "type": "STRING"},
  {"name": "message_id", "type": "STRING"},
  {"name": "publish_time", "type": "TIMESTAMP"},
  {"name": "data", "type": "JSON"}, 
  {"name": "attributes", "type": "JSON"}
]
EOF
}

# Pub/Sub Subscription to BigQuery
resource "google_pubsub_subscription" "stock_alerts_bq_sub" {
  depends_on = [
    google_bigquery_table.stock_alerts,
    google_pubsub_topic.stock_alerts_dead_letter,
    google_pubsub_subscription.stock_alerts_dead_letter_sub
  ]
  
  name  = "stock_alerts_bq_sub"
  topic = google_pubsub_topic.stock_alerts.name


  bigquery_config {
    table               = "${var.project_id}:${google_bigquery_dataset.stock_bronze.dataset_id}.stock_alerts"
    use_table_schema    = false
    write_metadata      = true
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.stock_alerts_dead_letter.id
    max_delivery_attempts = 5
  }
}

# Dead Letter Topic and Subscription
resource "google_pubsub_topic" "stock_alerts_dead_letter" {
  name = "stock_alerts-dead-letter"
}

resource "google_pubsub_subscription" "stock_alerts_dead_letter_sub" {
  name  = "stock_alerts-dead-letter-sub"
  topic = google_pubsub_topic.stock_alerts_dead_letter.name
}