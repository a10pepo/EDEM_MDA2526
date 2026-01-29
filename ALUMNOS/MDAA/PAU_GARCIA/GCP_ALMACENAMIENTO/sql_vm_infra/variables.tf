variable "subnetwork" {
  description = "The subnetwork for the instances"
  type        = string
}

variable "service_account_email" {
  description = "Email of the service account to attach to the VMs"
  type        = string
}

variable "user" {
  type = string
}
variable "password" {
  type = string
}

data "http" "my_ip" {
  url = "https://api.ipify.org"
}

locals {
  my_ip_cidr = "${chomp(data.http.my_ip.response_body)}/32"
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default = "inspiring-bonus-481514-j4"
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "zone" {
  description = "The GCP zone"
  type        = string
  default     = "europe-west1-b"
}

variable "instance_db_name" {
  default = "edem-e2e-db"
}

variable "publicipdb" {
  type = string
}
