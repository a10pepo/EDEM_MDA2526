# Guía de despliegue — E-commerce Ropa (AWS, coste ≈ 0)

Arquitectura: **EC2 t3.micro** (capa gratuita) ejecutando la API FastAPI + Postgres
con docker-compose. Imágenes en **S3 privado** (URLs prefirmadas). Imagen de la
API en **ECR**. Todo se levanta con **Terraform**.

> 💸 **Recordatorio de coste:** `t3.micro`, 20 GB de disco, S3 (<5 GB) y ECR
> (<500 MB) están en la **capa gratuita durante 12 meses**. Para que sea 0 € de
> verdad: no añadas RDS ni NAT Gateway, y destruye el entorno cuando no lo uses
> (`terraform destroy`). Restringe `ssh_cidr` a tu IP.

---

## 0. Requisitos previos

- Cuenta de AWS + **AWS CLI** configurado: `aws configure` (access key, secret, región `eu-west-1`).
- **Docker** y **Terraform** instalados.
- (Opcional) un **EC2 Key Pair** si quieres SSH a la instancia.

Comprueba la identidad:
```bash
aws sts get-caller-identity
```

---

## 1. Probar en local (opcional pero recomendado)

```bash
# Levanta API + Postgres
docker compose up --build
# API en http://localhost:8000  ·  Docs en http://localhost:8000/docs

# En otra terminal, ejecuta los tests:
python -m pip install -r requirements-dev.txt
python -m pytest
```

---

## 2. Desplegar TODO con un solo `terraform apply`

Terraform construye la imagen, la sube a ECR y crea la infraestructura en el
orden correcto (ECR → build/push → VPC/S3/IAM/EC2). El recurso
[`null_resource.docker_build_push`](infra/build.tf) ejecuta `docker build` +
`docker push` automáticamente, por eso necesitas **Docker y AWS CLI** en esta
máquina.

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # edita ssh_cidr / key_pair_name

terraform init
terraform apply        # responde "yes"
```

Eso es todo. Terraform mostrará al final:

```
api_public_ip = "x.x.x.x"
api_url       = "http://x.x.x.x"
s3_bucket_name = "ecommerce-ropa-media-xxxxxxxx"
ecr_repository_url = "...."
```

El EC2 tarda **1–3 minutos** en instalar Docker, descargar la imagen y arrancar.

---

## 3. Verificar

```bash
curl http://$(terraform output -raw api_public_ip)/health
# {"status":"ok"}

# Documentación interactiva:
#   http://<api_public_ip>/docs
```

Prueba rápida del catálogo:
```bash
API=http://$(terraform output -raw api_public_ip)
curl -X POST $API/categories -H "Content-Type: application/json" \
  -d '{"name":"Hombre","slug":"hombre"}'
curl -X POST $API/products -H "Content-Type: application/json" \
  -d '{"name":"Camiseta","slug":"camiseta","base_price":"19.99"}'
```

---

## 4. Actualizar la app (re-despliegue)

Al cambiar el código de `app/`, Terraform detecta el cambio (hash de fuentes) y
reconstruye + sube la nueva imagen solo. Como la instancia EC2 ya existe y no se
recrea sola, fuérzala a recargar la imagen nueva:

```bash
cd infra
terraform apply -replace=aws_instance.api
```

---

## 5. Apagar todo (para no gastar)

```bash
cd infra
terraform destroy
```

Esto elimina EC2, VPC, S3 (con `force`), ECR e IAM. **Coste tras destruir: 0 €.**

---

## Notas de seguridad y coste

- El bucket S3 es **privado**; las imágenes se sirven con URLs prefirmadas que
  caducan (`S3_PRESIGN_EXPIRATION`, 1 h por defecto).
- La API usa el **IAM Instance Role** del EC2: **no hay claves AWS en el código**.
- Postgres corre dentro del EC2 sin puerto público; los datos viven en un volumen
  Docker. Para producción real conviene migrar a RDS y/o configurar backups.
- Vigila siempre el **AWS Billing Dashboard** y activa un **presupuesto de 1 USD**
  con alerta por email para enterarte si algo se sale de la capa gratuita.
