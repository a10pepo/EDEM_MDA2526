# 🛍️ E-commerce Ropa — Backend API

Backend de un **e-commerce para una tienda de ropa**. Expone una API REST que
gestiona el **catálogo** (categorías, productos y variantes por talla/color), el
**inventario** y el **procesamiento de pedidos**. Las imágenes de los productos se
guardan en **Amazon S3** y se sirven mediante **URLs prefirmadas** temporales.

Toda la infraestructura se levanta en AWS con **un solo `terraform apply`**, y
está diseñada para caber en la **capa gratuita** (coste ≈ 0 €).

---

## ✨ ¿Qué hace la aplicación?

- **Catálogo de ropa** con categorías jerárquicas (p. ej. *Hombre → Camisetas*).
- **Variantes de producto** por combinación de **talla + color**, cada una con su
  propio **SKU**, **stock** y precio opcional.
- **Gestión de inventario**: al crear un pedido se valida y se descuenta el stock.
- **Pedidos**: se crean con varias líneas; el **precio se congela** en el momento
  de la compra (no cambia si luego se actualiza el catálogo).
- **Imágenes en S3**: el bucket es **privado**; la API genera URLs prefirmadas para
  subir (PUT) y para servir (GET) las imágenes de forma segura y temporal.
- Documentación interactiva automática en **`/docs`** (Swagger UI).

### Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET`  | `/health` | Comprobación de estado |
| `POST` | `/categories` · `GET /categories` · `GET /categories/{id}` | Categorías |
| `POST` | `/products` · `GET /products?category_id=` · `GET /products/{id}` | Productos (el detalle incluye variantes e imágenes con URL) |
| `POST` | `/products/{id}/variants` | Añadir variante (talla/color/sku/stock) |
| `POST` | `/products/{id}/images` | Registrar una imagen ya subida a S3 |
| `POST` | `/products/{id}/images/presign` | Obtener URL prefirmada para **subir** una imagen |
| `POST` | `/orders` · `GET /orders/{id}` | Crear y consultar pedidos |

---

## 🧰 Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Lenguaje | **Python 3.12** |
| API | **FastAPI** + **Pydantic** (validación) |
| ORM / Modelos | **SQLModel** (SQLAlchemy + Pydantic) |
| Base de datos | **PostgreSQL 16** |
| Almacenamiento de medios | **Amazon S3** (privado, URLs prefirmadas) vía **boto3** |
| Tests | **pytest** + **httpx** (TDD, 18 tests, ~97 % cobertura) |
| Contenedores | **Docker** + **docker-compose** |
| Infraestructura (IaC) | **Terraform** |
| Cómputo en AWS | **EC2 t3.micro** (capa gratuita) |
| Registro de imágenes | **Amazon ECR** |

### Nota sobre la arquitectura (decisión de coste)

- **EC2 `t3.micro`** (750 h/mes gratis durante 12 meses) ejecutando el contenedor
  de la API **y** PostgreSQL al lado mediante docker-compose.
- **VPC con una subred pública** (sin NAT Gateway). PostgreSQL **no se expone** a
  internet: corre en la red interna de Docker dentro del EC2.
- **S3 privado** con URLs prefirmadas y **ECR** para la imagen.

Resultado: misma funcionalidad, **coste ≈ 0 €** dentro de la capa gratuita.

---

## 🏗️ Arquitectura en AWS

```
                Internet
                   │
            ┌──────▼───────┐
            │ Internet GW  │
            └──────┬───────┘
   ┌───────────────▼─────────────────┐  VPC 10.0.0.0/16  (eu-west-1)
   │  Subred PÚBLICA  10.0.1.0/24     │
   │  ┌────────────────────────────┐ │      ┌──────────────┐
   │  │ EC2 t3.micro (IP pública)  │ │─────▶│  S3 privado  │  (IAM Role,
   │  │  docker-compose:           │ │ pre- │  imágenes    │   sin claves
   │  │   • FastAPI  :80           │ │firma │  catálogo    │   en el código)
   │  │   • PostgreSQL (interno)   │ │      └──────────────┘
   │  └────────────────────────────┘ │
   │   Security Group: 80 (API), 22 (SSH restringido)
   └─────────────────────────────────┘
```

---

## 📂 Estructura del proyecto

```
.
├── app/
│   ├── main.py              # Instancia FastAPI + routers
│   ├── core/config.py       # Configuración (variables de entorno)
│   ├── db/session.py        # Motor y sesión de BD
│   ├── models/              # Modelos SQLModel (tablas)
│   ├── schemas/             # DTOs de request/response (Pydantic)
│   ├── services/            # Lógica de negocio (pedidos, almacenamiento S3)
│   └── api/routes/          # Endpoints: health, categories, products, orders
├── tests/                   # Tests unitarios e integración (pytest)
├── infra/                   # Terraform: VPC, EC2, S3, IAM, ECR, build & push
├── Dockerfile               # Imagen de la API
├── docker-compose.yml       # Entorno LOCAL (API + Postgres)
├── docker-compose.prod.yml  # Entorno EC2 (imagen desde ECR)
├── requirements.txt         # Dependencias de la app
├── requirements-dev.txt     # Dependencias de test
├── DEPLOY.md                # Guía de despliegue detallada
└── ENUNCIADO.md             # Enunciado original
```

### Modelo de datos

```
users        categories(jerárquica)    products ──┐
                                                   ├─ product_variants (talla+color+sku+stock)
orders ─┐                                          └─ product_images   (s3_key)
        └─ order_items (variant_id, cantidad, precio_congelado)
```

---

## 💻 Probar en local (sin AWS)

Requisitos: **Docker**.

```bash
# Levanta la API + PostgreSQL
docker compose up --build
```

- API: <http://localhost:8000>
- Documentación interactiva: <http://localhost:8000/docs>

Ejecutar los tests:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest          # 18 tests
```

---

## ☁️ Desplegar en AWS (con tus propias credenciales)

> Esto crea recursos en **tu** cuenta de AWS. Dentro de la capa gratuita el coste
> es ~0 €, pero **revisa tu facturación** y ejecuta `terraform destroy` al acabar.

### Requisitos previos

1. **Cuenta de AWS** y **AWS CLI** instalado y configurado con tus credenciales:
   ```bash
   aws configure
   # AWS Access Key ID / Secret Access Key / región: eu-west-1
   ```
   Comprueba que funciona:
   ```bash
   aws sts get-caller-identity
   ```
2. **Docker** en marcha (Terraform lo usa para construir y subir la imagen).
3. **Terraform** ≥ 1.5.

### Despliegue (un solo comando)

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars   # (opcional) ajusta ssh_cidr / key_pair_name
terraform init
terraform apply        # escribe "yes" para confirmar
```

Terraform se encarga de **todo** en el orden correcto:

1. Crea el repositorio **ECR**.
2. **Construye** la imagen Docker y la **sube** a ECR (`docker build` + `push`).
3. Crea **VPC, S3, IAM** y la instancia **EC2**, que al arrancar descarga la imagen
   y levanta la API + PostgreSQL.

Al terminar muestra las salidas, incluida la URL pública:

```
api_url        = "http://x.x.x.x"
api_public_ip  = "x.x.x.x"
s3_bucket_name = "ecommerce-ropa-media-xxxxxxxx"
```

Espera **1–3 minutos** (arranque del EC2) y verifica:

```bash
curl http://<api_public_ip>/health      # {"status":"ok"}
# Documentación: http://<api_public_ip>/docs
```

### Apagar y borrar todo (coste 0)

```bash
cd infra
terraform destroy
```

Para más detalle (verificación, re-despliegue, notas de seguridad), ver
[DEPLOY.md](DEPLOY.md).

---

## 🔒 Notas de seguridad y coste

- **Sin claves de AWS en el código**: el EC2 usa un **IAM Instance Role** para
  acceder a S3 y ECR.
- **Bucket S3 privado**; las imágenes se sirven con URLs prefirmadas que caducan.
- Restringe el acceso SSH editando `ssh_cidr` en `terraform.tfvars` (pon tu IP/32).
- Recomendado: crea un **AWS Budget de 1 USD** con alerta por email.
- Todos los recursos (EC2 t3.micro, 20 GB disco, S3 < 5 GB, ECR < 500 MB) están en
  la **capa gratuita durante 12 meses**.

---

## ✅ Estado / calidad

- Desarrollado con **TDD**: **18 tests** (unitarios + integración), **~97 %** de
  cobertura.
- Infraestructura validada con `terraform validate`.
