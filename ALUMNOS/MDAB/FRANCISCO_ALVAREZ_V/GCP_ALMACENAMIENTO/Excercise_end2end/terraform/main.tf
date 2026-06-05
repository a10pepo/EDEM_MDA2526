# ──────────────────────────────────────────────
# ENABLE REQUIRED APIs
# ──────────────────────────────────────────────
resource "google_project_service" "compute" {
  service            = "compute.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "sql" {
  service            = "sqladmin.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "pubsub" {
  service            = "pubsub.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "bigquery" {
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

# ──────────────────────────────────────────────
# PUB/SUB
# ──────────────────────────────────────────────
resource "google_pubsub_topic" "order_events" {
  name       = "order-events"
  depends_on = [google_project_service.pubsub]
}

resource "google_pubsub_subscription" "order_events_sub" {
  name  = "order-events-sub"
  topic = google_pubsub_topic.order_events.name

  ack_deadline_seconds = 60
}

resource "google_pubsub_topic" "delivery_events" {
  name       = "delivery-events"
  depends_on = [google_project_service.pubsub]
}

# ──────────────────────────────────────────────
# CLOUD SQL (PostgreSQL)
# ──────────────────────────────────────────────
resource "google_sql_database_instance" "postgres_instance" {
  name             = "edem-postgres"
  region           = var.region
  database_version = "POSTGRES_15"

  settings {
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    disk_size         = 10

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "public-access"
        value = "0.0.0.0/0"
      }
    }
  }

  deletion_protection = false
  depends_on          = [google_project_service.sql]
}

resource "google_sql_user" "postgres_user" {
  name     = "postgres"
  instance = google_sql_database_instance.postgres_instance.name
  password = var.db_password
}

resource "google_sql_database" "ecommerce" {
  name     = "ecommerce"
  instance = google_sql_database_instance.postgres_instance.name
}

# ──────────────────────────────────────────────
# STARTUP SCRIPTS
# ──────────────────────────────────────────────
locals {
  orders_startup = <<-EOT
    #!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y python3 python3-pip python3-venv git

    # Wait for Cloud SQL to be reachable (up to 5 min)
    for i in $(seq 1 30); do
      pg_ip="${google_sql_database_instance.postgres_instance.public_ip_address}"
      python3 -c "import socket; s=socket.create_connection(('$pg_ip', 5432), 5)" 2>/dev/null && break
      sleep 10
    done

    # Clone or update repo
    if [ -n "${var.repo_url}" ]; then
      git clone ${var.repo_url} /app || (cd /app && git pull)
    fi

    cd /app
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    nohup bash -c "HOST_IP=${google_sql_database_instance.postgres_instance.public_ip_address} PROJECT_ID=${var.project_id} python -m orders_app.orders_to_db.main" > /var/log/orders-app.log 2>&1 &
  EOT

  delivery_startup = <<-EOT
    #!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y python3 python3-pip python3-venv git

    # Clone or update repo
    if [ -n "${var.repo_url}" ]; then
      git clone ${var.repo_url} /app || (cd /app && git pull)
    fi

    cd /app
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    nohup bash -c "PROJECT_ID=${var.project_id} python -m delivery_app.main" > /var/log/delivery-app.log 2>&1 &
  EOT
}

# ──────────────────────────────────────────────
# COMPUTE VMs
# ──────────────────────────────────────────────
resource "google_compute_instance" "orders_app" {
  name         = "orders-app"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  network_interface {
    subnetwork = var.subnetwork
    access_config {}
  }

  metadata = {
    startup-script = local.orders_startup
  }

  service_account {
    email = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/sqlservice.admin",
      "https://www.googleapis.com/auth/pubsub"
    ]
  }

  allow_stopping_for_update = true
  depends_on                = [google_project_service.compute, google_sql_database_instance.postgres_instance]
}

resource "google_compute_instance" "delivery_app" {
  name         = "delivery-app"
  machine_type = "e2-micro"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
      size  = 10
    }
  }

  network_interface {
    subnetwork = var.subnetwork
    access_config {}
  }

  metadata = {
    startup-script = local.delivery_startup
  }

  service_account {
    email = var.service_account_email
    scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/pubsub"
    ]
  }

  allow_stopping_for_update = true
  depends_on                = [google_project_service.compute]
}

# ──────────────────────────────────────────────
# OUTPUTS
# ──────────────────────────────────────────────
output "postgres_public_ip" {
  description = "Cloud SQL public IP — use for POSTGRES_IP env var"
  value       = google_sql_database_instance.postgres_instance.public_ip_address
}

output "orders_app_ip" {
  description = "orders-app VM external IP"
  value       = google_compute_instance.orders_app.network_interface[0].access_config[0].nat_ip
}

output "delivery_app_ip" {
  description = "delivery-app VM external IP"
  value       = google_compute_instance.delivery_app.network_interface[0].access_config[0].nat_ip
}
