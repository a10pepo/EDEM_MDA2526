variable "region" {
  default = "eu-west-1"
}

variable "db_password" {
  description = "Master password for the RDS instance"
  type        = string
  sensitive   = true
  default     = "Aerodrome2025!"
}
