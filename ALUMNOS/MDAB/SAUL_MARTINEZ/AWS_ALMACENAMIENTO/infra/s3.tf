# Bucket PRIVADO para las imágenes del catálogo. No se sirve nada públicamente:
# la API genera URLs prefirmadas temporales para leer/subir objetos.

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "media" {
  bucket = "${var.project_name}-media-${random_id.bucket_suffix.hex}"
  tags   = { Name = "${var.project_name}-media" }
}

# Bloquea por completo cualquier acceso público.
resource "aws_s3_bucket_public_access_block" "media" {
  bucket                  = aws_s3_bucket.media.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "media" {
  bucket = aws_s3_bucket.media.id
  versioning_configuration {
    status = "Disabled"
  }
}

# CORS para permitir subidas directas (PUT) desde el navegador vía URL prefirmada.
resource "aws_s3_bucket_cors_configuration" "media" {
  bucket = aws_s3_bucket.media.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT"]
    allowed_origins = ["*"]
    max_age_seconds = 3000
  }
}
