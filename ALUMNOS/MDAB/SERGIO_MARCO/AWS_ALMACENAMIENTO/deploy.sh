#!/bin/bash
set -e  # Detiene el script si falla algún comando

APP_NAME="delivery-fleet"
SSH_KEY_PATH="~/.ssh/id_rsa_aws" # Cambia esto por la ruta a tu clave PEM/RSA de AWS

echo ""
echo "========================================"
echo "  AWS Delivery Fleet MVP "
echo "  Pipeline Deployment    "
echo "========================================"
echo ""

# =============================================================================
# CONFIGURACIÓN DEL PERFIL DE AWS
# =============================================================================

# Validar que AWS CLI está instalado y configurado
if ! command -v aws &> /dev/null; then
    echo "❌ Error: AWS CLI no está instalado."
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)

echo "Cuenta AWS : $ACCOUNT_ID"
echo "Región     : $REGION"
echo ""
read -p "¿Continuar con el despliegue en esta cuenta y región? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
  echo "Despliegue cancelado."
  exit 1
fi

# =============================================================================
# FASE 1 — Infraestructura base (Terraform)
# =============================================================================
echo ""
echo ">>> FASE 1: Desplegando infraestructura en AWS (VPC, RDS, EC2)..."
cd terraform

terraform init -upgrade

echo "-> Validando código Terraform..."
if ! terraform validate; then
    echo "❌ ERROR: Fallo en la validación de Terraform."
    exit 1
fi

terraform apply -auto-approve

# Extraer variables de salida de Terraform necesarias para los siguientes pasos
EC2_PUBLIC_IP=$(terraform output -raw ec2_public_ip)
RDS_ENDPOINT=$(terraform output -raw rds_endpoint)

cd ..
echo "✅ Fase 1 completada. Infraestructura lista."
echo "🌐 IP Pública de EC2: $EC2_PUBLIC_IP"
echo "🗄️ Endpoint de RDS: $RDS_ENDPOINT"

# Leer credenciales de la BD desde terraform.tfvars para inyectarlas en los manifiestos
DB_USER=$(grep 'db_username' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')
DB_PASSWORD=$(grep 'db_password' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')
DB_NAME=$(grep 'db_name' terraform/terraform.tfvars | sed 's/.*= *"\(.*\)"/\1/')
DB_PORT=5432

# =============================================================================
# FASE 2 — Compilación de imágenes Docker locales
# =============================================================================
echo ""
echo ">>> FASE 2: Compilando imágenes Docker de Backend, Frontend y Simulator..."

docker build --platform linux/amd64 -t $APP_NAME-backend:latest ./backend
docker build --platform linux/amd64 -t $APP_NAME-frontend:latest ./frontend
docker build --platform linux/amd64 -t $APP_NAME-simulator:latest ./simulator

echo "-> Empaquetando imágenes para transferencia (tar)..."
docker save -o backend.tar $APP_NAME-backend:latest
docker save -o frontend.tar $APP_NAME-frontend:latest
docker save -o simulator.tar $APP_NAME-simulator:latest

echo "✅ Fase 2 completada. Imágenes compiladas y empaquetadas."

# =============================================================================
# FASE 3 — Transferencia e importación en K3s (EC2)
# =============================================================================
echo ""
echo ">>> FASE 3: Transfiriendo imágenes al servidor EC2 y cargando en K3s..."

# Espera robusta: primero a que SSH responda, luego a que K3s esté Ready.
# El user-data de la EC2 instala Docker + K3s y puede tardar 2-3 min.
SSH_OPTS="-i $SSH_KEY_PATH -o StrictHostKeyChecking=no -o ConnectTimeout=5"

echo "⏳ Esperando a que la EC2 acepte conexiones SSH..."
for i in $(seq 1 30); do
  if ssh $SSH_OPTS ubuntu@$EC2_PUBLIC_IP "echo ok" >/dev/null 2>&1; then
    echo "   ✅ SSH disponible."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "❌ ERROR: SSH no respondió tras varios intentos."; exit 1
  fi
  echo "   Intento $i/30: SSH aún no listo, reintentando en 10s..."
  sleep 10
done

echo "⏳ Esperando a que K3s esté operativo (puede tardar 2-3 min)..."
for i in $(seq 1 30); do
  if ssh $SSH_OPTS ubuntu@$EC2_PUBLIC_IP "sudo k3s kubectl get nodes 2>/dev/null | grep -q ' Ready'"; then
    echo "   ✅ K3s operativo."
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "❌ ERROR: K3s no llegó a estado Ready tras varios intentos."; exit 1
  fi
  echo "   Intento $i/30: K3s aún instalándose, reintentando en 10s..."
  sleep 10
done

# Subir los archivos tar por SCP
scp -i $SSH_KEY_PATH -o StrictHostKeyChecking=no backend.tar frontend.tar simulator.tar ubuntu@$EC2_PUBLIC_IP:~

# Importar las imágenes en el containerd de K3s
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ubuntu@$EC2_PUBLIC_IP << EOF
    echo "-> Importando imágenes en K3s..."
    sudo k3s ctr images import backend.tar
    sudo k3s ctr images import frontend.tar
    sudo k3s ctr images import simulator.tar
    rm backend.tar frontend.tar simulator.tar
EOF

# Limpiar archivos locales
rm backend.tar frontend.tar simulator.tar

echo "✅ Fase 3 completada. Imágenes disponibles en el clúster K3s."

# =============================================================================
# FASE 4 — Despliegue en Kubernetes
# =============================================================================
echo ""
echo ">>> FASE 4: Aplicando manifiestos de Kubernetes..."

# Copiar la carpeta k8s al servidor
scp -i $SSH_KEY_PATH -o StrictHostKeyChecking=no -r ./k8s ubuntu@$EC2_PUBLIC_IP:~/k8s

# Aplicar los manifiestos en el clúster remoto
ssh -i $SSH_KEY_PATH -o StrictHostKeyChecking=no ubuntu@$EC2_PUBLIC_IP << EOF
    echo "-> Inyectando credenciales de la BD en los manifiestos..."
    # El backend y el simulator necesitan los mismos datos de conexión a RDS
    for f in ~/k8s/backend-deployment.yaml ~/k8s/simulator-deployment.yaml; do
      sed -i "s|REPLACE_DB_HOST|$RDS_ENDPOINT|g"     "\$f"
      sed -i "s|REPLACE_DB_PORT|$DB_PORT|g"          "\$f"
      sed -i "s|REPLACE_DB_NAME|$DB_NAME|g"          "\$f"
      sed -i "s|REPLACE_DB_USER|$DB_USER|g"          "\$f"
      sed -i "s|REPLACE_DB_PASSWORD|$DB_PASSWORD|g"  "\$f"
    done

    echo "-> Desplegando pods y servicios..."
    sudo kubectl apply -f ~/k8s/
EOF

echo "✅ Fase 4 completada."

# =============================================================================
# DESPLIEGUE FINALIZADO
# =============================================================================
echo ""
echo "🚀 ¡DESPLIEGUE FINALIZADO CON ÉXITO! 🚀"
echo "Puedes acceder a tu aplicación de Gestión de Flota en:"
echo "👉 http://$EC2_PUBLIC_IP"
echo ""

# =============================================================================
# FASE 5 — Teardown opcional (destruir toda la infraestructura)
# =============================================================================
echo "========================================"
echo "  LIMPIEZA DE RECURSOS (DESTROY)        "
echo "========================================"
echo "⚠️  Mientras la infraestructura siga levantada, AWS sigue cobrando"
echo "    (EC2 t3.small + RDS t4g.micro se facturan por hora)."
echo ""
read -p "¿Destruir TODA la infraestructura ahora con 'terraform destroy'? (yes/no): " DESTROY_CONFIRM

if [ "$DESTROY_CONFIRM" = "yes" ]; then
  echo ""
  echo ">>> Destruyendo infraestructura en AWS..."
  cd terraform
  terraform destroy -auto-approve
  cd ..
  echo ""
  echo "✅ Infraestructura destruida. La cuenta queda sin recursos facturables."
else
  echo ""
  echo "ℹ️  Infraestructura CONSERVADA y en funcionamiento."
  echo "   App disponible en: http://$EC2_PUBLIC_IP"
  echo "   Recuerda destruirla cuando termines para no acumular coste:"
  echo "      cd terraform && terraform destroy -auto-approve"
fi
echo ""