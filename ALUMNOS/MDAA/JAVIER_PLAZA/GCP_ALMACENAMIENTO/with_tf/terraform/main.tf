resource "google_compute_instance" "orders_app" {
  name = "orders-app"
  machine_type = "e2-micro"
  zone = var.zone
  allow_stopping_for_update = true
  network_interface {
    subnetwork = var.subnetwork
    access_config {
      
    }
  }
  tags = ["http-server", "https-server", "ssh"]
  service_account {
    email = var.service_account_email
    scopes = [
        "https://www.googleapis.com/auth/pubsub",
        "https://www.googleapis.com/auth/sqlservice.admin",
        "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  boot_disk {
    initialize_params {
      image = "debian-11-bullseye-v20241210"
    }
  }
  metadata = {
    enable-oslogin = false
    ssh-keys = "debian:${file(pathexpand("~/.ssh/id_rsa.pub"))}"
  }
}

resource "google_compute_instance" "delivery_app" {
  name = "delivery-app"
  machine_type = "e2-micro"
  zone = var.zone
  allow_stopping_for_update = true
  network_interface {
    subnetwork = var.subnetwork
    access_config {
      
    }
  }
  tags = ["http-server", "https-server", "ssh"]
  service_account {
    email = var.service_account_email
    scopes = [
        "https://www.googleapis.com/auth/pubsub",
        "https://www.googleapis.com/auth/sqlservice.admin",
        "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
  boot_disk {
    initialize_params {
      image = "debian-11-bullseye-v20241210"
    }
  }
  metadata = {
    enable-oslogin = false
    ssh-keys       = "debian:${file(pathexpand("~/.ssh/id_rsa.pub"))}"
  }
}

resource "google_compute_firewall" "allow_ssh" {
  name = "allow-ssh"
  network = var.network
  allow {
    protocol = "tcp"
    ports = ["22"]
  }
  source_ranges = [local.my_ip_cidr]
  target_tags = ["ssh"]
}

resource "google_pubsub_topic" "order_events" {
  name = "orders-events"
}

resource "google_pubsub_subscription" "order_events_sub" {
  name = "${google_pubsub_topic.order_events.name}-sub"
  topic = google_pubsub_topic.order_events.name
}

resource "google_pubsub_topic" "delivery_events" {
  name = "delivery-events"
}

resource "google_pubsub_subscription" "delivery_events_sub" {
  name = "${google_pubsub_topic.delivery_events.name}-sub"
  topic = google_pubsub_topic.delivery_events.name
}

resource "google_pubsub_topic" "delivery_events_dead_letter" {
  name = "delivery-events-dead-letter"
}

resource "google_pubsub_subscription" "delivery_events_dead_letter_sub" {
  name = "${google_pubsub_topic.delivery_events_dead_letter.name}-sub"
  topic = google_pubsub_topic.delivery_events_dead_letter.name
}

resource "google_sql_database_instance" "operational_db_instance" {
  name = "operational-db-instance"
  database_version = "POSTGRES_17"
  region = var.region
  deletion_protection = true
  settings {
    edition = "ENTERPRISE"
    tier = "db-f1-micro"
    availability_type = "ZONAL"
    disk_size = 100
    ip_configuration {
      ipv4_enabled = true
      ssl_mode = "ALLOW_UNENCRYPTED_AND_ENCRYPTED"
      authorized_networks {
        name = "public-access"
        value = local.my_ip_cidr
      }
      authorized_networks {
        name  = "delivery-app-external-ip"
        value = google_compute_instance.delivery_app.network_interface[0].access_config[0].nat_ip
      }
      authorized_networks {
        name  = "orders-app-external-ip"
        value = google_compute_instance.orders_app.network_interface[0].access_config[0].nat_ip
      }
    }
  }
  lifecycle {
    prevent_destroy = false
  }
}

resource "google_sql_database" "ecommerce" {
  name = "ecommerce"
  instance = google_sql_database_instance.operational_db_instance.name
}

resource "google_sql_user" "user_op_db" {
  name = var.user_op_db
  instance = google_sql_database_instance.operational_db_instance.name
  password = var.password_op_db
}

resource "google_bigquery_dataset" "orders_bronze" {
    dataset_id = "orders_bronze"
    location = var.region
    project = var.project_id 
}

resource "google_bigquery_dataset" "delivery_bronze" {
    dataset_id = "delivery_bronze"
    location = var.region 
    project = var.project_id
}

resource "google_bigquery_table" "customers_orders_bronze" {
    dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
    table_id = "customers"
    schema = <<EOF
    [
        {
        "name": "id",
        "type": "INT64"
        },
        {
        "name": "customer_name",
        "type": "STRING"
        },
        {
        "name": "email",
        "type": "STRING"
        }
    ]
    EOF
}

resource "google_bigquery_table" "products_orders_bronze" {
    dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
    table_id = "products"
    schema = <<EOF
    [
        {
        "name": "id",
        "type": "INT64"
        },
        {
        "name": "product_name",
        "type": "STRING"
        },
        {
        "name": "price",
        "type": "FLOAT64"
        }
    ]
    EOF
}

resource "google_bigquery_table" "orders_orders_bronze" {
    dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
    table_id = "orders"
    schema = <<EOF
    [
        {
        "name": "id",
        "type": "INT64"
        },
        {
        "name": "customer_id",
        "type": "INT64"
        },
        {
        "name": "created_at",
        "type": "TIMESTAMP"
        },
        {
        "name": "total_price",
        "type": "FLOAT64"
        }
    ]
    EOF
}

resource "google_bigquery_table" "order_products_orders_bronze" {
    dataset_id = google_bigquery_dataset.orders_bronze.dataset_id
    table_id = "order_products"
    schema = <<EOF
    [
        {
        "name": "order_id",
        "type": "INT64"
        },
        {
        "name": "product_id",
        "type": "INT64"
        },
        {
        "name": "quantity",
        "type": "INT64"
        },
        {
        "name": "price",
        "type": "FLOAT64"
        }
    ]
    EOF
}

resource "google_bigquery_table" "raw_events_delivery_bronze" {
    dataset_id = google_bigquery_dataset.delivery_bronze.dataset_id
    table_id = "raw_events_delivery"
    schema = <<EOF
    [
        {
        "name": "subscription_name",
        "type": "STRING"
        },
        {
        "name": "message_id",
        "type": "STRING"
        },
        {
        "name": "publish_time",
        "type": "TIMESTAMP"
        },
        {
        "name": "data",
        "type": "JSON"
        },
        {
        "name": "attributes",
        "type": "JSON"
        }
    ]
    EOF
    time_partitioning {
        type = "DAY"
        field = "publish_time"
    }
    clustering = [
        "subscription_name",
        "message_id"
    ]
    labels = {
        source = "bq_subs"
    }
}

resource "google_bigquery_dataset_iam_member" "pubsub_bigquery_permission" {
  dataset_id = google_bigquery_dataset.delivery_bronze.dataset_id
  role = "roles/bigquery.dataEditor"
  member = "serviceAccount:service-${var.project_number}@gcp-sa-pubsub.iam.gserviceaccount.com"

  depends_on = [google_bigquery_dataset.delivery_bronze]
}

resource "google_pubsub_subscription" "delivery_events_bq_sub" {
  depends_on = [
      google_bigquery_table.raw_events_delivery_bronze,
      google_pubsub_topic.delivery_events,
      google_pubsub_subscription.delivery_events_dead_letter_sub
  ]

  name = "delivery-events-bq-sub"
  topic = google_pubsub_topic.delivery_events.name

  bigquery_config {
      table = "${var.project_id}:${google_bigquery_dataset.delivery_bronze.dataset_id}.raw_events_delivery"
      use_table_schema = false
      write_metadata = true
  }

  dead_letter_policy {
      dead_letter_topic = google_pubsub_topic.delivery_events_dead_letter.id
      max_delivery_attempts = 5
  }
}

resource "google_storage_bucket" "data_lake" {
  name = "e2e-gcp-storage-${var.project_id}"
  location = var.region
  force_destroy = true
}

resource "google_project_iam_member" "permissions_sa" {
  for_each = toset(var.roles_permissions)
  project = var.project_id
  role = each.value
  member  = "serviceAccount:${var.project_number}-compute@developer.gserviceaccount.com"
}

