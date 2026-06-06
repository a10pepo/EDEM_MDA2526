output "aurora_endpoint" {
  description = "Endpoint writer del cluster Aurora (úsalo como DB_HOST)"
  value       = aws_rds_cluster.aurora.endpoint
}

output "aurora_port" {
  description = "Puerto de Aurora PostgreSQL"
  value       = aws_rds_cluster.aurora.port
}

output "aurora_db_name" {
  description = "Nombre de la base de datos"
  value       = aws_rds_cluster.aurora.database_name
}

output "env_file_content" {
  description = "Contenido listo para copiar en tu fichero .env"
  value       = <<-EOT
    DB_HOST=${aws_rds_cluster.aurora.endpoint}
    DB_NAME=${aws_rds_cluster.aurora.database_name}
    DB_USER=${var.db_username}
    DB_PASS=<tu_password>
  EOT
}

output "init_sql_command" {
  description = "Comando para inicializar el esquema en Aurora (requiere psql instalado)"
  value       = "psql -h ${aws_rds_cluster.aurora.endpoint} -U ${var.db_username} -d ${aws_rds_cluster.aurora.database_name} -f ../db/init.sql"
}
