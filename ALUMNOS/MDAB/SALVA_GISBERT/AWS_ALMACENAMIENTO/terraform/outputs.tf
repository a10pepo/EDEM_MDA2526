output "rds_host" {
  description = "RDS PostgreSQL endpoint host."
  value       = aws_db_instance.football.address
}

output "rds_port" {
  description = "RDS PostgreSQL port."
  value       = aws_db_instance.football.port
}

output "rds_database" {
  description = "PostgreSQL database name."
  value       = aws_db_instance.football.db_name
}

output "rds_user" {
  description = "PostgreSQL username."
  value       = aws_db_instance.football.username
}

output "git_bash_env" {
  description = "Git Bash commands to configure local connection variables."
  value       = <<EOT
export RDS_HOST="${aws_db_instance.football.address}"
export RDS_PORT="${aws_db_instance.football.port}"
export RDS_DATABASE="${aws_db_instance.football.db_name}"
export RDS_USER="${aws_db_instance.football.username}"
export RDS_PASSWORD="<same password from terraform.tfvars>"
export RDS_SSLMODE="require"
EOT
}

output "powershell_env" {
  description = "PowerShell commands to configure local connection variables."
  value       = <<EOT
$env:RDS_HOST="${aws_db_instance.football.address}"
$env:RDS_PORT="${aws_db_instance.football.port}"
$env:RDS_DATABASE="${aws_db_instance.football.db_name}"
$env:RDS_USER="${aws_db_instance.football.username}"
$env:RDS_PASSWORD="<same password from terraform.tfvars>"
$env:RDS_SSLMODE="require"
EOT
}
