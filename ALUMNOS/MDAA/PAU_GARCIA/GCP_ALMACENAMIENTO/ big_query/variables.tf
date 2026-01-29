variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default = "inspiring-bonus-481514-j4"
}

variable "delivery_events_topic_name" {
  description = "Nombre del topic Pub/Sub delivery_events"
  type        = string
}

variable "service_account_email" {
  type = string
}