output "orders_app_ip" {
  description = "Public IP of the orders-app instance"
  value       = google_compute_instance.orders_app.network_interface[0].access_config[0].nat_ip
}

output "delivery_app_ip" {
  description = "Public IP of the delivery-app instance"
  value       = google_compute_instance.delivery_app.network_interface[0].access_config[0].nat_ip
}

resource "local_file" "ansible_vars" {
  filename = "${path.module}/../ansible/vars/db_config.yml"
  content  = <<-EOT
---
db_host: "${google_sql_database_instance.operational_db_instance.public_ip_address}"
db_user: "${var.user_op_db}"
db_password: "${var.password_op_db}"
db_name: "ecommerce"
EOT
}

resource "local_file" "ansible_inventory" {
  filename = "${path.module}/../ansible/inventory"
  content  = <<-EOT
[gcp_orders_app]
orders-app-server ansible_host=${google_compute_instance.orders_app.network_interface[0].access_config[0].nat_ip}

[gcp_delivery_app]
delivery-app-server ansible_host=${google_compute_instance.delivery_app.network_interface[0].access_config[0].nat_ip}

[gcp_all_apps:children]
gcp_orders_app
gcp_delivery_app

[gcp_all_apps:vars]
ansible_user=debian
ansible_port=22
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
ansible_become=true
ansible_become_method=sudo
EOT

  depends_on = [
    google_compute_instance.orders_app,
    google_compute_instance.delivery_app
  ]
}

resource "local_file" "ansible_env_vars" {
  filename = "${path.module}/../ansible/vars/env_vars.yml"
  content  = <<-EOT
---
PASSWORD_SQL: "${var.password_op_db}"
USER_SQL: "${var.user_op_db}"
GCS_BUCKET_NAME: "${google_storage_bucket.data_lake.name}"
HOST_IP: "${google_sql_database_instance.operational_db_instance.public_ip_address}"
PROJECT_ID: "${var.project_id}"
EOT

  depends_on = [
    google_storage_bucket.data_lake,
    google_sql_database_instance.operational_db_instance
  ]
}


