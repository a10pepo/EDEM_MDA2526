output "ecr_repository_url" {
  description = "URL del repositorio ECR (para docker push)."
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_registry" {
  description = "Host del registro ECR (para docker login)."
  value       = split("/", aws_ecr_repository.api.repository_url)[0]
}

output "api_public_ip" {
  description = "IP pública del EC2. La API responde en http://<ip>/"
  value       = aws_instance.api.public_ip
}

output "api_url" {
  description = "URL base de la API."
  value       = "http://${aws_instance.api.public_ip}"
}

output "s3_bucket_name" {
  description = "Nombre del bucket de medios."
  value       = aws_s3_bucket.media.bucket
}
