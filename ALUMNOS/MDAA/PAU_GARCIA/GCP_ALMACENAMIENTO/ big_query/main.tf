
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
  topic = var.delivery_events_topic_name

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
