output "delivery_app_public_ip" {
  value       = google_compute_instance_from_machine_image.delivery_app.network_interface.0.access_config.0.nat_ip
  description = "The public IP address of the delivery app VM"
}

output "delivery_app_zone" {
  value = google_compute_instance_from_machine_image.delivery_app.zone
}

output "orders_app_public_ip" {
  value       = google_compute_instance_from_machine_image.orders_app.network_interface.0.access_config.0.nat_ip
  description = "The public IP address of the orders app VM"
}

output "orders_app_zone" {
  value = google_compute_instance_from_machine_image.orders_app.zone
}

output "postgres_public_ip" {
  value       = google_sql_database_instance.postgres_instance.ip_address.0.ip_address
  description = "The public IP address of the SQL instance"
}

output "gcs_bucket_name" {
  value       = google_storage_bucket.data_lake.name
  description = "The name of the GCS data lake bucket"
}

output "gcs_bucket_url" {
  value       = "gs://${google_storage_bucket.data_lake.name}"
  description = "The GCS bucket URL for data lake"
}
