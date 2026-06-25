output "rds_endpoint" {
  value = aws_db_instance.aerodrome.endpoint
}

output "database_url" {
  value     = "postgresql://aerodrome:${var.db_password}@${aws_db_instance.aerodrome.endpoint}/aerodrome"
  sensitive = true
}
