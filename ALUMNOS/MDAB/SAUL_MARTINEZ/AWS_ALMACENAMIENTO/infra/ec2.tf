# Instancia EC2 t3.micro (capa gratuita) que ejecuta la API + Postgres con
# docker-compose. La imagen se descarga de ECR al arrancar (user_data).

# AMI más reciente de Amazon Linux 2023 (vía SSM, siempre actualizada).
data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
}

# Contraseña de Postgres generada y guardada solo en el estado de Terraform.
resource "random_password" "postgres" {
  length  = 24
  special = false
}

locals {
  ecr_registry = split("/", aws_ecr_repository.api.repository_url)[0]
  image_uri    = "${aws_ecr_repository.api.repository_url}:${var.image_tag}"

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    image_uri         = local.image_uri
    ecr_registry      = local.ecr_registry
    aws_region        = var.aws_region
    s3_bucket_name    = aws_s3_bucket.media.bucket
    postgres_password = random_password.postgres.result
    compose_content   = file("${path.module}/../docker-compose.prod.yml")
  })
}

resource "aws_instance" "api" {
  ami                    = data.aws_ssm_parameter.al2023.value
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.api.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2.name
  key_name               = var.key_pair_name != "" ? var.key_pair_name : null
  user_data              = local.user_data

  # Volumen raíz dentro de la capa gratuita (30 GB gp3 incluidos).
  root_block_device {
    volume_size = 20
    volume_type = "gp3"
  }

  # No crear el EC2 hasta que la imagen esté en ECR (build.tf).
  depends_on = [null_resource.docker_build_push]

  tags = { Name = "${var.project_name}-api" }
}
