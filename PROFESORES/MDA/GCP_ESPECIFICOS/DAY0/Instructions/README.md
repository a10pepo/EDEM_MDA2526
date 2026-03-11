# 🚀 Guía de Migración: De Docker Local a Google Cloud SQL

Este repositorio contiene la hoja de ruta para migrar una base de datos PostgreSQL desde un entorno de desarrollo local (Docker) hacia una infraestructura gestionada en **Google Cloud Platform (GCP)**.



---

## 📋 Requisitos Previos

* Cuenta de Google Cloud Platform con un proyecto activo.
* Terraform instalado.
* Google Cloud SDK (`gcloud`) configurado.
* Docker y Docker Compose funcionando en local.

---

## Paso 1: Aprovisionamiento de Infraestructura con Terraform

### 📝 Instrucción
Define la infraestructura necesaria en GCP. Debes crear una instancia de Cloud SQL y autorizar el acceso desde el exterior para poder realizar la migración y pruebas.

### ✅ Validación
1.  Ejecuta `terraform apply`.
2.  Al finalizar, verifica que obtienes la IP pública en el output.
3.  Conéctate desde un cliente local (**pgAdmin** o **DBeaver**) usando la IP, el usuario `admin` y la contraseña definida.

---

## Paso 2: Exportación de Datos Locales (Dump)

### 📝 Instrucción
Genera un archivo de respaldo (`backup.sql`) con los datos actuales de tu contenedor Docker local sin detener el servicio.

### ✅ Validación
Verifica que se ha creado un archivo `backup.sql` en tu directorio de trabajo y que, al abrirlo con un editor de texto, contiene sentencias SQL como `INSERT INTO` o `CREATE TABLE`.

---

## Paso 3: Preparación del Storage (GCS)

### 📝 Instrucción
Cloud SQL no permite importar archivos locales directamente. Necesitas subir el backup a un Bucket de Cloud Storage.

1.  Añade a tu Terraform un recurso `google_storage_bucket`.
2.  Sube el archivo `backup.sql` a ese bucket usando la CLI.

### ✅ Validación
Ve a la consola de GCP -> **Cloud Storage** y verifica que tu bucket existe y contiene el archivo `.sql`.

---

## Paso 4: Importación de Datos

### 📝 Instrucción
Importa los datos desde el Bucket de Storage hacia tu nueva instancia de Cloud SQL.

> **Nota:** La cuenta de servicio de la instancia de Cloud SQL debe tener permisos de lectura sobre el bucket. Para este laboratorio, usaremos tu usuario autenticado vía `gcloud` para orquestar la operación.

### ✅ Validación
Conéctate a la instancia de Cloud SQL (usando DBeaver o CLI) y ejecuta una consulta de prueba (ej. `SELECT count(*) FROM tabla;`).

---

## Paso 5: Reconfiguración de la Aplicación

### 📝 Instrucción
Modifica tu archivo `docker-compose.yaml` para que la aplicación apunte a la nube:

1.  Elimina o comenta la definición del servicio `db` local.
2.  Cambia las variables de entorno de tu servicio de aplicación (`DB_HOST`, `DB_USER`, etc.) para usar las credenciales de Cloud SQL.

### ✅ Validación
1.  Ejecuta `docker-compose up --build`.
2.  La aplicación debe iniciar sin errores de conexión ("Connection Refused").
3.  Navega por la aplicación y verifica que ves los datos antiguos.
