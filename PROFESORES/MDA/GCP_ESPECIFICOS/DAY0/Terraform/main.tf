# Generamos un sufijo aleatorio para que el nombre de la instancia sea único
resource "random_id" "db_name_suffix" {
  byte_length = 4
}

# --- Instancia de Cloud SQL ---
resource "google_sql_database_instance" "instance" {
  name             = "mi-instancia-sql-${random_id.db_name_suffix.hex}"
  database_version = "POSTGRES_15"
  region           = "europe-west1" 

  deletion_protection = false # CUIDADO: 'false' permite destruir la DB con terraform destroy. En prod ponlo en 'true'.

  settings {
    tier = "db-f1-micro" 
    ip_configuration {
      ipv4_enabled = true 
      
      authorized_networks {
        name  = "Mi IP Publica"
        # IMPORTANTE: Añade /32 al final de la IP que encontraste en Google
        value = "0.0.0.0/0" 
      }
    }
  }
}

# --- Base de Datos ---
resource "google_sql_database" "database" {
  name     = "mi-base-de-datos"
  instance = google_sql_database_instance.instance.name
}

# --- Usuario ---
resource "google_sql_user" "users" {
  name     = "admin-user"
  instance = google_sql_database_instance.instance.name
  password = "password-super-secreto-123" # En prod, usa Secret Manager o variables, no texto plano.
}
