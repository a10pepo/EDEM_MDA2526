# Football Callup Manager

Proyecto MVP para gestionar las convocatorias de un equipo de futbol desde terminal.

La idea es sustituir una libreta tradicional por una base de datos sencilla donde el
club pueda registrar jugadores, partidos y convocatorias.

La base de datos del proyecto es **Amazon RDS PostgreSQL**.

## Tablas

El proyecto usa solo 3 tablas:

- `players`: jugadores del equipo, posicion, estado fisico y ultima revision medica.
- `matches`: partidos, rival, fecha, estadio y maximo de convocados.
- `callups`: relacion entre jugadores y partidos, con dorsal y estado de convocatoria.

La DDL completa esta en `schema.sql` y esta preparada para PostgreSQL.

## Requisitos

- Python 3.10 o superior.
- Una base de datos Amazon RDS PostgreSQL.
- Dependencias de Python:

```bash
pip install -r requirements.txt
```

## Crear RDS PostgreSQL

Puedes crear la base de datos con Terraform usando la carpeta `terraform/`.

1. Copia el fichero de ejemplo:

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

2. Edita `terraform.tfvars`:

```hcl
allowed_cidr = "TU_IP_PUBLICA/32"
db_password  = "UnaPasswordSegura123!"
```

`allowed_cidr` debe ser tu IP publica con `/32`. Por ejemplo:

```hcl
allowed_cidr = "80.20.10.5/32"
```

3. Crea RDS:

Antes de ejecutar Terraform, asegurate de tener credenciales AWS configuradas,
por ejemplo con `aws configure` o variables de entorno.

Tu usuario AWS necesita permisos para crear RDS. Para una demo, lo mas simple es
asignar la policy administrada:

```text
AmazonRDSFullAccess
```

Si no puedes modificar permisos, pide al admin/profesor que la asigne al usuario
que usas en `aws configure`. Tambien hay una policy de ejemplo mas acotada en
`terraform/rds-iam-policy.example.json`.

```bash
terraform init
terraform apply
```

Terraform mostrara un output llamado `git_bash_env` con las variables que debes
copiar en tu terminal.

Cuando termines de probar, puedes borrar RDS para evitar costes:

```bash
terraform destroy
```

> Nota: RDS puede generar coste. El proyecto usa `db.t3.micro` y 20 GB para el MVP.

### Variables de conexion

Necesitas estos datos de tu instancia RDS:

- Endpoint o host.
- Puerto, normalmente `5432`.
- Nombre de la base de datos.
- Usuario y password.
- Acceso de red permitido desde tu IP, EC2, Cloud9 o el entorno donde ejecutes Python.

En Git Bash:

```bash
export RDS_HOST="tu-endpoint-rds.amazonaws.com"
export RDS_PORT="5432"
export RDS_DATABASE="football_callup_manager"
export RDS_USER="footballadmin"
export RDS_PASSWORD="tu_password"
export RDS_SSLMODE="require"
```

Tambien se aceptan las variables antiguas `DB_HOST`, `DB_PORT`, `DB_NAME`,
`DB_USER` y `DB_PASSWORD`, pero para RDS es mas claro usar `RDS_*`.

## Generar datos aleatorios

```bash
python seed_data.py
```

Opciones utiles:

```bash
python seed_data.py --players 30 --matches 8 --seed 42
```

El script recrea las tablas usando `schema.sql` e inserta datos aleatorios en RDS.

Si quieres insertar nuevos datos sin recrear las tablas:

```bash
python seed_data.py --skip-schema
```

## Usar la aplicacion

Ver jugadores:

```bash
python app.py players
```

Ver partidos:

```bash
python app.py matches
```

Ver convocatoria de un partido:

```bash
python app.py callups 1
```

Ver alertas:

```bash
python app.py alerts
```

## API para el frontend

El frontend React no se conecta directamente a la base de datos. Usa una API HTTP
intermedia para leer la informacion de Amazon RDS PostgreSQL.

Arrancar la API:

```bash
uvicorn api:app --reload
```

Endpoints principales:

- `GET /api/players`
- `GET /api/matches`
- `GET /api/callups`
- `GET /api/alerts`

## Frontend React

El frontend esta en la carpeta `frontend/`.

Instalar dependencias:

```bash
cd frontend
npm install
```

Arrancar en desarrollo:

```bash
npm run dev
```

Abrir:

```text
http://127.0.0.1:5173
```

Si la API no esta arrancada o RDS no esta configurado, el frontend muestra datos
de demo para poder ensenar el MVP igualmente.

## Reglas de negocio del MVP

- Alerta si un partido tiene menos de 11 jugadores confirmados.
- Alerta si una convocatoria tiene mas del 10% de plazas libres.
- Alerta si un jugador lleva mas de 365 dias sin revision medica.

## Siguiente sprint

Ideas posibles para evolucionar el producto:

- Crear una API REST con FastAPI.
- Dockerizar la aplicacion.
- Desplegar la aplicacion en AWS EC2, ECS o Lambda.
- Anadir una interfaz web sencilla.
- Registrar goles, tarjetas y estadisticas por jugador.
