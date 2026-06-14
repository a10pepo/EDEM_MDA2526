# Construye la imagen Docker y la sube a ECR como parte de `terraform apply`.
# Se ejecuta DESPUÉS de crear el repositorio ECR y ANTES de crear el EC2
# (el EC2 declara depends_on sobre este recurso), de modo que la imagen ya
# existe cuando la instancia intenta descargarla al arrancar.
#
# Requiere Docker y AWS CLI en la máquina que ejecuta Terraform.
resource "null_resource" "docker_build_push" {
  # Solo reconstruye cuando cambian el Dockerfile, las dependencias o el código.
  triggers = {
    dockerfile   = filemd5("${path.module}/../Dockerfile")
    requirements = filemd5("${path.module}/../requirements.txt")
    image_uri    = local.image_uri
    source_hash = sha1(join("", [
      for f in fileset("${path.module}/../app", "**") :
      filemd5("${path.module}/../app/${f}")
    ]))
  }

  provisioner "local-exec" {
    # Un único comando encadenado: válido en cmd.exe (Windows), bash y zsh.
    command = join(" && ", [
      "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${local.ecr_registry}",
      "docker build --platform linux/amd64 -t ${local.image_uri} ${path.module}/..",
      "docker push ${local.image_uri}",
    ])
  }

  depends_on = [
    aws_ecr_repository.api,
    aws_ecr_lifecycle_policy.api,
  ]
}
