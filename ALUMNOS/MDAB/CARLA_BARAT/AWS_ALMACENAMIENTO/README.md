# Zara Store Management System

**Sprint 1 — Terminal MVP**

Pedro is the manager of a Zara franchise. His father ran the store for 30 years keeping everything in paper notebooks: one for the product inventory, one for purchase tickets, one for customer records. Pedro wants to modernise the operation and be able to access the system from anywhere.

This is the Sprint 1 MVP: a Python CLI application backed by AWS DynamoDB.

---

## Domain

| Entity | Key field | Equivalent in notebooks |
|---|---|---|
| **Product** | SKU | Inventory notebook — name, size, color, stock, price, supplier |
| **Ticket** | ticket_id | Sales notebook — items purchased, cashier, customer, payment |
| **Customer** | customer_id | Customer notebook — name, email, membership level |

---

## Features

### Products
- List all products in inventory
- Register a new product (or update existing)
- View product details
- Check stock level vs restock threshold
- Update stock quantity after receiving goods

### Tickets
- List all purchase tickets
- Register a new ticket interactively (add items one by one)
- View ticket details with itemised breakdown
- Update ticket status (`pending` → `completed` → `returned`)

### Customers
- List all customers
- Register a customer
- View customer details and full purchase history
- Check purchase/return status of a customer

### Alerts (3 thresholds)
| Alert | Condition | Notebook equivalent |
|---|---|---|
| **Low Stock** | `stock_quantity <= restock_threshold` | Post-it on shelf when nearly empty |
| **High Discount** | ticket discount > 20% of gross amount | Manager approval required |
| **High Return Rate** | returned tickets > 10% of all tickets | Flag for store review |

---

## Project Structure

```
├── main.py                  # CLI entry point
├── src/
│   ├── models/              # Data classes (Product, Ticket, Customer)
│   ├── db/                  # DynamoDB client + table names
│   ├── services/            # Business logic (CRUD + alerts)
│   └── cli/                 # Typer command groups
├── aws/
│   ├── setup_tables.py      # Create DynamoDB tables
│   ├── seed_data.py         # Populate with demo data
│   └── cloudformation.yaml  # Full AWS infrastructure
└── tests/                   # pytest + moto (mocked DynamoDB)
```

---

## Local Setup (LocalStack)

```bash
# 1. Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# 2. Copy and edit env vars
cp .env.example .env

# 3. Start LocalStack (Docker required)
localstack start -d

# 4. Create tables and seed demo data
USE_LOCAL_DYNAMODB=true python aws/setup_tables.py
USE_LOCAL_DYNAMODB=true python aws/seed_data.py

# 5. Run the app
USE_LOCAL_DYNAMODB=true python main.py --help
```

---

## AWS Setup

```bash
# Deploy infrastructure with CloudFormation
aws cloudformation deploy \
  --template-file aws/cloudformation.yaml \
  --stack-name zara-management \
  --parameter-overrides KeyName=my-key \
  --capabilities CAPABILITY_NAMED_IAM

# SSH into the EC2 instance and run:
python3 main.py setup
python3 aws/seed_data.py
python3 main.py --help
```

---

## Usage Examples

```bash
# List all products
python main.py product list

# Register a product
python main.py product register

# Check stock level
python main.py product stock ZAR-SH-002

# Register a sale (interactive)
python main.py ticket register

# Mark ticket as returned
python main.py ticket status TKT-20260603-001 returned

# View customer history
python main.py customer get DNI-001

# Run all alerts
python main.py alerts check
```

---

## Tests

```bash
pytest tests/ -v
```

The test suite uses `moto` to mock DynamoDB — no real AWS credentials needed.

---

## Roadmap

| Sprint | Goal |
|---|---|
| **1 (current)** | Terminal MVP — CRUD + alerts via CLI, DynamoDB, AWS EC2 |
| 2 | Dockerize + docker-compose for local dev |
| 3 | REST API with FastAPI |
| 4 | CI/CD pipeline (GitHub Actions) |
| 5 | Web UI (React or simple Jinja2) |
| 6 | Kubernetes deployment (microk8s on EC2) |
