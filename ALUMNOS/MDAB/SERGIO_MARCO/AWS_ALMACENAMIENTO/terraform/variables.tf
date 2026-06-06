variable "region" {
  type        = string
  default     = "eu-north-1"
  description = "AWS region to deploy into"
}

variable "db_name" {
  type        = string
  default     = "fleetdb"
  description = "PostgreSQL database name"
}

variable "db_username" {
  type        = string
  description = "RDS master username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "RDS master password"
}

variable "key_pair_name" {
  type        = string
  description = "Name of the EC2 key pair for SSH access"
}

variable "ssh_allowed_cidr" {
  type        = string
  default     = "0.0.0.0/0"
  description = "CIDR block allowed to SSH into the EC2 instance"
}
