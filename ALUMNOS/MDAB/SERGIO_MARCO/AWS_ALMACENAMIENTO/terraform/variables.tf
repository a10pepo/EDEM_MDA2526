variable "region"      { default = "eu-north-1" }
variable "db_name"     { default = "fleetdb" }
variable "db_username" {}
variable "db_password" { sensitive = true }
variable "key_pair_name" {}
