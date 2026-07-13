output "ec2_public_ip" {
  value = aws_instance.app.public_ip
}

output "rds_endpoint" {
  description = "RDS hostname (without port) for backend env var DB_HOST"
  value       = aws_db_instance.postgres.address
}
