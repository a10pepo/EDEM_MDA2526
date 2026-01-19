# DELIVERY APP VM

resource "google_compute_instance" "delivery_app" {

  boot_disk {
    auto_delete = true
    device_name = "delivery-app"

    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20260114"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src           = "vm_add-tf"
    goog-ops-agent-policy = "v2-x86-template-1-4-0"
  }

  machine_type = "e2-micro"

  metadata = {
    enable-osconfig = "TRUE"
  }

  name = "delivery-app"

  network_interface {
    access_config {

    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = var.subnetwork
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only", 
      "https://www.googleapis.com/auth/logging.write", 
      "https://www.googleapis.com/auth/monitoring.write", 
      "https://www.googleapis.com/auth/service.management.readonly", 
      "https://www.googleapis.com/auth/servicecontrol", 
      "https://www.googleapis.com/auth/trace.append",
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
      ]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = "europe-west1-d"

  depends_on = [
    google_sql_database_instance.postgres_instance,
    google_pubsub_topic.order_events,
    google_pubsub_topic.delivery_events
  ]

}


# ORDERS APP VM
resource "google_compute_instance" "orders_app" {


  boot_disk {
    auto_delete = true
    device_name = "orders-app"

    initialize_params {
      image = "projects/debian-cloud/global/images/debian-12-bookworm-v20260114"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    goog-ec-src           = "vm_add-tf"
    goog-ops-agent-policy = "v2-x86-template-1-4-0"
  }

  machine_type = "e2-micro"

  metadata = {
    enable-osconfig = "TRUE"
  }

  name = "orders-app"

  network_interface {
    access_config {

    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = var.subnetwork
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only", 
      "https://www.googleapis.com/auth/logging.write", 
      "https://www.googleapis.com/auth/monitoring.write", 
      "https://www.googleapis.com/auth/service.management.readonly", 
      "https://www.googleapis.com/auth/servicecontrol", 
      "https://www.googleapis.com/auth/trace.append",
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
      ]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["http-server", "https-server"]
  zone = "europe-west1-d"

  depends_on = [
    google_sql_database_instance.postgres_instance,
    google_pubsub_topic.order_events,
    google_pubsub_topic.delivery_events
  ]
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
  name             = "cloud-sql-cabesa-edem"
  region           = var.region
  database_version = "POSTGRES_15"
  settings {
    tier            = "db-f1-micro"
    availability_type = "ZONAL"
    disk_size       = 100 # GB

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
