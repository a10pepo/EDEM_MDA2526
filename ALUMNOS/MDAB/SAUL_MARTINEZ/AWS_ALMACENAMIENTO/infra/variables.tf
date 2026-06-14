variable "aws_region" {
  description = "Región de AWS (Irlanda por cercanía a España)."
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Prefijo para nombrar todos los recursos."
  type        = string
  default     = "ecommerce-ropa"
}

variable "instance_type" {
  description = "Tipo de EC2. t3.micro entra en la capa gratuita (750h/mes, 12 meses)."
  type        = string
  default     = "t3.micro"
}

variable "ssh_cidr" {
  description = "CIDR autorizado para SSH (puerto 22). Pon tu IP/32 por seguridad."
  type        = string
  default     = "0.0.0.0/0"
}

variable "key_pair_name" {
  description = "Nombre de un EC2 Key Pair EXISTENTE para SSH. Vacío = sin acceso SSH."
  type        = string
  default     = ""
}

variable "image_tag" {
  description = "Tag de la imagen Docker en ECR que desplegará el EC2."
  type        = string
  default     = "latest"
}
