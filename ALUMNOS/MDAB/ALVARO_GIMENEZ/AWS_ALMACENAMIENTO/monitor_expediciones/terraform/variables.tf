variable "aws_region" {
  description = "Región de AWS donde desplegar Aurora"
  type        = string
  default     = "eu-west-1"
}

variable "db_username" {
  description = "Usuario master de Aurora"
  type        = string
  default     = "almacen_user"
}

variable "db_password" {
  description = "Contraseña master de Aurora"
  type        = string
  sensitive   = true
}

variable "my_ip" {
  description = "Tu IP pública (sin /32). Obtenla con: curl ifconfig.me"
  type        = string
}
