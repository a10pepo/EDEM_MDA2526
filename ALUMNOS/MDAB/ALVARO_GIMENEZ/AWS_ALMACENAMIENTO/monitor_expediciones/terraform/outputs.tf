output "db_endpoint" {
  description = "Endpoint de la instancia RDS (host:puerto)"
  value       = aws_db_instance.postgres.endpoint
}

output "db_address" {
  description = "Host de la instancia RDS (úsalo como DB_HOST)"
  value       = aws_db_instance.postgres.address
}

output "db_port" {
  description = "Puerto de PostgreSQL"
  value       = aws_db_instance.postgres.port
}

output "db_name" {
  description = "Nombre de la base de datos"
  value       = aws_db_instance.postgres.db_name
}

output "env_file_content" {
  description = "Contenido listo para copiar en tu fichero .env"
  value       = <<-EOT
    DB_HOST=${aws_db_instance.postgres.address}
    DB_NAME=${aws_db_instance.postgres.db_name}
    DB_USER=${var.db_username}
    DB_PASS=<tu_password>
  EOT
}

output "init_sql_command" {
  description = "Comando para inicializar el esquema en RDS (requiere psql instalado)"
  value       = "psql -h ${aws_db_instance.postgres.address} -U ${var.db_username} -d ${aws_db_instance.postgres.db_name} -f ../db/init.sql"
}
