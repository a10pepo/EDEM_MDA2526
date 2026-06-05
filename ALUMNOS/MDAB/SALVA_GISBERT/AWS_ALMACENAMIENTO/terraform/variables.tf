variable "aws_region" {
  description = "AWS region where RDS PostgreSQL will be created."
  type        = string
  default     = "eu-west-1"
}

variable "allowed_cidr" {
  description = "Public CIDR allowed to connect to PostgreSQL, for example 80.20.10.5/32."
  type        = string
}

variable "manage_networking" {
  description = "Create or look up VPC networking resources. Disable this for restricted AWS accounts without EC2 permissions."
  type        = bool
  default     = false
}

variable "vpc_id" {
  description = "Optional VPC id. If omitted and networking is managed, Terraform tries to use the default VPC."
  type        = string
  default     = null
}

variable "subnet_ids" {
  description = "Optional subnet ids for a DB subnet group."
  type        = list(string)
  default     = []
}

variable "security_group_ids" {
  description = "Optional existing security group ids for RDS. If omitted and networking is managed, Terraform creates one."
  type        = list(string)
  default     = []
}

variable "create_db_subnet_group" {
  description = "Create a DB subnet group from subnet_ids or default VPC subnets."
  type        = bool
  default     = false
}

variable "db_identifier" {
  description = "RDS instance identifier."
  type        = string
  default     = "football-callup-manager"
}

variable "db_name" {
  description = "PostgreSQL database name."
  type        = string
  default     = "football_callup_manager"
}

variable "db_username" {
  description = "PostgreSQL username."
  type        = string
  default     = "footballadmin"
}

variable "db_password" {
  description = "PostgreSQL password."
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance size."
  type        = string
  default     = "db.t3.micro"
}

variable "engine_version" {
  description = "PostgreSQL engine version. Leave null to let AWS choose a supported default."
  type        = string
  default     = null
}

variable "allocated_storage" {
  description = "Allocated storage in GB."
  type        = number
  default     = 20
}

variable "publicly_accessible" {
  description = "Whether the RDS instance is publicly reachable."
  type        = bool
  default     = true
}
