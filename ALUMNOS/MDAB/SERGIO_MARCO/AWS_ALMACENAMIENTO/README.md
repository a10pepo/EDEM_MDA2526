# AWS Delivery Fleet Management System (MVP)

Sistema de gestión de flota de reparto desplegado en AWS con **Terraform + K3s**.
Backend FastAPI, frontend con Leaflet.js + OpenStreetMap, y un simulador que mueve
los vehículos en tiempo real. Todo se levanta con un único script: `deploy.sh`.

---

## Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│  AWS (eu-north-1)                                              │
│                                                                │
│  ┌────────────────────────┐      ┌─────────────────────────┐  │
│  │  EC2 t3.small (K3s)     │      │  RDS PostgreSQL         │  │
│  │  ┌──────┐ ┌──────────┐  │      │  db.t4g.micro           │  │
│  │  │backend│ │frontend  │  │◄────►│  (subnet privada)       │  │
│  │  └──────┘ │(nginx)   │  │ 5432 │                         │  │
│  │  ┌────────┐└──────────┘ │      └─────────────────────────┘  │
│  │  │simulator│            │                                   │
│  │  └────────┘   subnet pública                                │
│  └────────────────────────┘                                    │
└──────────────────────────────────────────────────────────────┘
        ▲ 80                          ▲ SSH/SCP (build + deploy)
        │                             │
     navegador                    tu portátil (deploy.sh)
```

- **Compute:** una EC2 `t3.small` con **K3s** (Kubernetes ligero), sin EKS para abaratar.
- **Base de datos:** RDS PostgreSQL `db.t4g.micro` en subred privada, accesible solo
  desde el Security Group de la EC2.
- **Backend:** API FastAPI en contenedor. Crea el esquema y siembra datos de prueba al
  arrancar (no hace falta `schema.sql` aparte).
- **Frontend:** SPA con Leaflet.js servida por Nginx; panel de administración + mapa en vivo.
- **Simulador:** actualiza las coordenadas de los vehículos `en_ruta` cada 5 s.

---

## ⚠️ ¿En qué cuenta de AWS se despliega?

**El `deploy.sh` NO contiene ninguna cuenta ni credencial hardcodeada.** La cuenta de
destino la determina **el perfil del AWS CLI configurado en tu máquina**. Al arrancar, el
script ejecuta:

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=$(aws configure get region)
```

…te muestra esa cuenta y región, y **pide confirmación** antes de crear nada:

```
Cuenta AWS : 649631967525
Región     : eu-north-1
¿Continuar con el despliegue en esta cuenta y región? (yes/no):
```

Por tanto, **se despliega en la cuenta dueña de las credenciales (Access Key) que tengas
activas** — ya sea por `aws configure`, por la variable `AWS_PROFILE`, o por las variables
`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`. Terraform usa exactamente el mismo proveedor
de credenciales. Verifica siempre la cuenta que muestra el banner antes de escribir `yes`.

> Nota sobre la región: el banner muestra la región del perfil, pero **los recursos de
> Terraform se crean en la región de `terraform/variables.tf` (`eu-north-1` por defecto)**.
> Para evitar confusiones, configura tu perfil también en `eu-north-1`.

---

## Requisitos previos

| Herramienta | Para qué |
|-------------|----------|
| **AWS CLI** configurado | Credenciales de la cuenta destino (`aws configure`) |
| **Terraform** ≥ 1.5 | Provisionar la infraestructura |
| **Docker** (Desktop en ejecución) | Compilar las imágenes del backend, frontend y simulador |
| **Cliente SSH/SCP** | Transferir imágenes y desplegar en K3s (incluido en Git Bash) |
| **Key pair de EC2** | Acceso SSH a la instancia (ver abajo) |

### Autenticarse en AWS CLI

```bash
aws configure
# AWS Access Key ID     : AKIA....
# AWS Secret Access Key : ....
# Default region name   : eu-north-1
# Default output format : json

aws sts get-caller-identity   # comprobar que devuelve tu cuenta
```

### Crear el key pair SSH

El nombre debe coincidir con `key_pair_name` en `terraform/terraform.tfvars`, y la clave
privada debe estar en la ruta `SSH_KEY_PATH` del `deploy.sh` (por defecto `~/.ssh/id_rsa_aws`):

```bash
aws ec2 create-key-pair --key-name fleet-key --region eu-north-1 \
    --query KeyMaterial --output text > ~/.ssh/id_rsa_aws
chmod 600 ~/.ssh/id_rsa_aws
```

### Configurar variables de Terraform

Copia la plantilla y rellena tus valores (este archivo **no se sube a git**):

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

```hcl
db_username   = "fleetadmin"
db_password   = "FleetDbEdem2026!"   # 8-128 chars, sin / @ " ni espacios
db_name       = "fleetdb"
key_pair_name = "fleet-key"          # debe existir en AWS (paso anterior)
```

---

## Despliegue

```bash
./deploy.sh
```

El script ejecuta 5 fases:

1. **Infraestructura (Terraform):** crea VPC, subredes, RDS y EC2. Extrae la IP pública
   y el endpoint de RDS de los outputs.
2. **Build Docker:** compila las imágenes `backend`, `frontend` y `simulator` y las
   empaqueta en `.tar`.
3. **Transferencia a K3s:** copia los `.tar` por SCP e importa las imágenes en containerd
   (`k3s ctr images import`). No se usa registro ECR para no incurrir en coste.
4. **Kubernetes:** copia los manifiestos, **inyecta las credenciales de la BD** (endpoint de
   RDS, usuario, contraseña…) y aplica todo con `kubectl apply`.
5. **Teardown opcional:** al terminar pregunta si quieres destruir la infraestructura.

Al finalizar imprime la URL de acceso:

```
👉 http://<IP_PUBLICA_EC2>
```

---

## Destruir la infraestructura (evitar costes)

> Mientras la EC2 y la RDS estén levantadas, **AWS factura por hora**. Destrúyelas al terminar.

El `deploy.sh` ofrece hacerlo al final (responde `yes` en la Fase 5). De forma manual:

```bash
cd terraform
terraform destroy -auto-approve
```

Todos los recursos están configurados para borrarse limpiamente
(`skip_final_snapshot = true` en RDS, sin Elastic IP ni Load Balancer de AWS, volumen raíz
con `delete_on_termination`). El key pair, al crearse fuera de Terraform, debes borrarlo
aparte si quieres dejar la cuenta 100 % limpia:

```bash
aws ec2 delete-key-pair --key-name fleet-key --region eu-north-1
```

---

## Estructura del proyecto

```
AWS_ALMACENAMIENTO/
├── terraform/          # IaC: VPC, subredes, SGs, EC2, RDS, outputs
├── backend/            # API FastAPI (CRUD, alertas, tracking) + tests
├── frontend/           # SPA Leaflet + Nginx
├── simulator/          # Movimiento de vehículos en tiempo real + tests
├── k8s/                # Manifiestos de Kubernetes (deployments + services)
├── deploy.sh           # Script maestro de despliegue (5 fases)
└── README.md
```

---

## Modelo de datos

- **conductores** — `id`, `dni`, `nombre`, `telefono`
- **vehiculos** — `id`, `matricula`, `modelo`, `capacidad_carga_kg`, `fecha_itv`, `estado`
- **rutas** — `id`, `vehiculo_id`, `conductor_id`, coordenadas origen/destino/actual, `estado`
- **pedidos** — `id`, `ruta_id`, `peso_kg`, `descripcion` (para la alerta de sobrecarga)

### Alertas (endpoint `/api/alerts`)

- **ITV:** vehículos cuya `fecha_itv` está a menos de 30 días.
- **Sobrecarga:** rutas cuyo peso supera el 90 % de la capacidad del vehículo.

---

## Seguridad

- **Nunca se commitean secretos.** El `.gitignore` excluye `*.tfvars`, `*.tfstate`,
  claves privadas (`id_rsa*`, `*.pem`, `*.key`) y archivos `.env`.
- Las credenciales de AWS viven solo en tu perfil local (`~/.aws/`), nunca en el repo.
- La RDS no es accesible públicamente; solo desde el Security Group de la EC2.

---

## Tests

```bash
cd backend   && python -m pytest tests/ -q   # 24 tests
cd simulator && python -m pytest tests/ -q   #  5 tests
```
