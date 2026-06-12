#!/bin/bash
set -euxo pipefail

# --- Instalar Docker y el plugin compose en Amazon Linux 2023 ---
dnf update -y
dnf install -y docker
systemctl enable --now docker

mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/v2.32.1/docker-compose-linux-$(uname -m)" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# --- Preparar el directorio de la app ---
APP_DIR=/opt/app
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Archivo de entorno consumido por docker-compose.prod.yml
cat > .env <<EOF
IMAGE_URI=${image_uri}
AWS_REGION=${aws_region}
S3_BUCKET_NAME=${s3_bucket_name}
POSTGRES_PASSWORD=${postgres_password}
EOF

# docker-compose de producción (generado por Terraform)
cat > docker-compose.yml <<'EOF'
${compose_content}
EOF

# --- Autenticarse en ECR y arrancar ---
aws ecr get-login-password --region ${aws_region} \
  | docker login --username AWS --password-stdin ${ecr_registry}

docker compose pull
docker compose up -d
