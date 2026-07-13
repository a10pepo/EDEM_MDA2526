# Design Spec: AWS Delivery Fleet Management System MVP

**Date:** 2026-06-06  
**Status:** Approved

---

## 1. Overview

MVP de sistema de gestión de flota de reparto desplegado en AWS (eu-north-1) usando Terraform + K3s (single-node Kubernetes) en EC2. El sistema incluye un simulador en tiempo real que mueve vehículos en el mapa.

---

## 2. Stack Tecnológico

| Capa | Tecnología |
|------|-----------|
| IaC | Terraform |
| Compute | EC2 t3.small + K3s |
| Base de datos | RDS PostgreSQL t4g.micro |
| Backend | Python 3.11 + FastAPI + SQLAlchemy |
| Frontend | HTML/JS + Leaflet.js + Nginx |
| Simulador | Python loop (Kubernetes Deployment) |
| Orquestación | K3s (kubectl) |
| Región AWS | eu-north-1 (Estocolmo) |

---

## 3. Infraestructura Terraform

### Red
- VPC: `10.0.0.0/16`
- Subnet pública: `10.0.1.0/24` (eu-north-1a) — EC2
- Subnet privada A: `10.0.2.0/24` (eu-north-1a) — RDS (AZ primaria)
- Subnet privada B: `10.0.3.0/24` (eu-north-1b) — RDS (AZ secundaria, requerida por aws_db_subnet_group)

### Security Groups
- `sg_ec2`: ingress 22, 80, 443 desde 0.0.0.0/0; egress all
- `sg_rds`: ingress 5432 solo desde `sg_ec2`

### EC2
- AMI: Ubuntu Server 22.04 LTS (HVM, eu-north-1)
- Tipo: t3.small
- User data: instala Docker + K3s

### RDS
- Engine: PostgreSQL 15
- Tipo: db.t4g.micro
- Multi-AZ: false (single-AZ, en eu-north-1a)
- publicly_accessible: false
- DB subnet group: subnet privada A + B

### Credenciales
- Gestionadas via `terraform.tfvars` (no se sube al repo)
- Variables: `db_username`, `db_password`, `db_name`, `key_pair_name`

### Outputs
- `ec2_public_ip`
- `rds_endpoint`

---

## 4. Base de Datos

### Tablas
- `conductores`: id, dni (UNIQUE), nombre, telefono
- `vehiculos`: id, matricula (UNIQUE), modelo, capacidad_carga_kg, fecha_itv, estado
- `rutas`: id, vehiculo_id, conductor_id, origen_lat/lng, destino_lat/lng, actual_lat/lng, estado
- `pedidos`: id, ruta_id, peso_kg, descripcion

### Inicialización
FastAPI gestiona todo vía SQLAlchemy `lifespan`:
1. `Base.metadata.create_all()` al arrancar — crea tablas si no existen
2. Detecta si la DB está vacía (COUNT conductores == 0) e inserta seed data
3. Sin `schema.sql` externo; sin paso de inicialización en `deploy.sh`

### Seed Data
- 5 conductores con datos reales de ejemplo
- 5 vehículos: 2 con `fecha_itv` en < 30 días (alerta ITV visible)
- 3 rutas `en_ruta` con coordenadas en ciudades españolas
- 2 rutas `pendiente`
- Pedidos para 2 rutas que superen 90% capacidad (alerta sobrecarga visible)

---

## 5. Backend API (FastAPI)

### Estructura
```
backend/
  app/
    main.py          # FastAPI app, lifespan, CORS
    database.py      # SQLAlchemy engine + session
    models.py        # ORM models (conductores, vehiculos, rutas, pedidos)
    seed.py          # seed data logic
    routers/
      conductores.py
      vehiculos.py
      rutas.py
      alerts.py
      tracking.py
  Dockerfile
  requirements.txt
```

### Endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/conductores` | Listar / crear conductores |
| GET/PUT/DELETE | `/api/conductores/{id}` | Leer / actualizar / borrar |
| GET/POST | `/api/vehiculos` | Listar / crear vehículos |
| GET/PUT/DELETE | `/api/vehiculos/{id}` | Leer / actualizar / borrar |
| GET/POST | `/api/rutas` | Listar / crear rutas |
| GET/PUT/DELETE | `/api/rutas/{id}` | Leer / actualizar / borrar |
| GET | `/api/routes/active` | Posiciones actuales (para mapa) |
| GET | `/api/alerts` | Alertas ITV + sobrecarga activas |
| GET | `/api/health` | Healthcheck K8s liveness probe |

### Alertas
- **ITV:** `fecha_itv - CURRENT_DATE < 30 días` y estado != 'taller'
- **Sobrecarga:** `SUM(pedidos.peso_kg) / vehiculos.capacidad_carga_kg > 0.9`

---

## 6. Simulador (Kubernetes Deployment)

### Lógica (simulate.py)
```
Cada 5 segundos:
  Para cada ruta con estado = 'en_ruta':
    actual_lat += (destino_lat - actual_lat) * 0.01
    actual_lng += (destino_lng - actual_lng) * 0.01
    Si distancia_restante < 0.01°:
      estado = 'completada'
      Crear nueva ruta igual pero con origen/destino intercambiados → estado 'en_ruta'
```

El loop continuo garantiza que el mapa nunca quede vacío.

### Estructura
```
simulator/
  simulate.py
  Dockerfile
  requirements.txt
```

---

## 7. Kubernetes Manifests (k8s/)

| Fichero | Descripción |
|---------|-------------|
| `backend-deployment.yaml` | Deployment backend, 1 réplica, env vars DB |
| `backend-service.yaml` | ClusterIP :8000 |
| `frontend-deployment.yaml` | Deployment frontend Nginx, 1 réplica |
| `frontend-service.yaml` | NodePort :80 |
| `simulator-deployment.yaml` | Deployment simulador, 1 réplica, env vars DB |
| `nginx-configmap.yaml` | Proxy `/api/` → backend service |

### Inyección de variables de entorno
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Inyectadas en `backend-deployment.yaml` vía placeholder `REPLACE_*`
- El `deploy.sh` usa `sed` para sustituir los placeholders antes del `kubectl apply`

---

## 8. Frontend

### Layout (2 secciones)
1. **Admin Panel** (tab izquierdo):
   - Formularios HTML para crear conductores, vehículos, rutas
   - Tablas para ver y eliminar registros existentes
   - Panel de alertas activas (ITV + sobrecarga) con badge rojo

2. **Live Tracking Map** (tab derecho):
   - Mapa Leaflet.js con tiles de OpenStreetMap (sin API key)
   - Polling a `/api/routes/active` cada 3 segundos
   - Marcador custom por vehículo en `actual_lat/lng`
   - Polyline origen → actual → destino
   - Badge contador de alertas activas visible en todo momento

---

## 9. deploy.sh (ajustes al script existente)

El script existente cubre fases 1-4 correctamente. Ajustes:
- **Eliminar Fase de schema.sql** — FastAPI lo gestiona solo al arrancar
- **Fase 3 ampliada:** construir y transferir también la imagen del `simulator`
- **Espera de K3s:** añadir `sleep` o poll hasta que K3s esté listo antes del `kubectl apply`
- **Fase 4:** incluir `simulator-deployment.yaml` en el `kubectl apply`

---

## 10. Ficheros a Crear

```
AWS_ALMACENAMIENTO/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── seed.py
│   │   └── routers/
│   │       ├── conductores.py
│   │       ├── vehiculos.py
│   │       ├── rutas.py
│   │       ├── alerts.py
│   │       └── tracking.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── Dockerfile
├── simulator/
│   ├── simulate.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── simulator-deployment.yaml
│   └── nginx-configmap.yaml
├── deploy.sh  (actualizar existente)
└── docs/superpowers/specs/2026-06-06-delivery-fleet-design.md
```
