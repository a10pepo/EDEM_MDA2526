resource "google_compute_instance_from_machine_image" "delivery_app" {
  name           = "delivery-app"
  provider       = google-beta
  zone           = var.zone
  source_machine_image  = "projects/inspiring-bonus-481514-j4/global/machineImages/imagenorders"
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


resource "google_storage_bucket" "bucketprin" {
  name          = "bucketedemcloudpgesparter"
  location      = "europe-southwest1"
  force_destroy = false
}

resource "google_compute_instance_from_machine_image" "orders_app" {
  name           = "orders-app"
  provider       = google-beta
  zone           = var.zone
  source_machine_image  = "projects/inspiring-bonus-481514-j4/global/machineImages/imagenorders"
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

resource "google_sql_database_instance" "operational_db_instance" {
    name = var.instance_db_name
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
      ssl_mode     = "ALLOW_UNENCRYPTED_AND_ENCRYPTED"
      authorized_networks {
        name  = "public-access"
        value = local.my_ip_cidr
      }
        }
    }
    lifecycle {
        prevent_destroy = false
    }
}

resource "google_sql_database" "ecommerce" {
    name = "ecommerce"
    instance = var.instance_db_name
}

resource "google_pubsub_topic" "order_events" {
  name = "order-events"
}

resource "google_pubsub_subscription" "order_events_sub" {
  name  = "${google_pubsub_topic.order_events.name}-sub"
  topic = google_pubsub_topic.order_events.name
}

resource "google_pubsub_topic" "delivery_events" {
  name = "delivery-events"
}

resource "google_pubsub_subscription" "delivery_events_sub" {
  name  = "${google_pubsub_topic.delivery_events.name}-sub"
  topic = google_pubsub_topic.delivery_events.name
}

resource "google_sql_user" "user_op_db" {
    name = var.user
    instance = var.instance_db_name
    password = var.password
}

output "delivery_events_topic_name" {
  value = google_pubsub_topic.delivery_events.name
}

resource "null_resource" "init_db_schema_direct" {
  provisioner "local-exec" {
    command = <<EOT
      if ! command -v psql >/dev/null 2>&1; then
        echo "psql no está instalado. Instalando..."
        if [[ "$OSTYPE" == "darwin"* ]]; then
          brew install postgresql
        else
          sudo apt-get update && sudo apt-get install -y postgresql-client
        fi
      fi
      PGPASSWORD="${var.password}" psql --host="${var.publicipdb}" --username="${var.user}" --dbname=ecommerce --port=5432 -f ${path.module}/schema.sql
    EOT
    environment = {
      PGPASSWORD = var.password
    }
  }
}

