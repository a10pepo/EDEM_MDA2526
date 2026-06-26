.PHONY: install install-dev run test setup-local setup-aws seed clean \
        docker-build docker-up docker-down docker-setup docker-seed docker-run docker-test docker-logs \
        api api-docker frontend frontend-docker dev

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

run:
	python main.py

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

setup-local:
	@echo "Starting DynamoDB Local via Docker..."
	docker compose up -d dynamodb
	@echo "Waiting for DynamoDB Local to be healthy..."
	docker compose run --rm --entrypoint "" app python aws/setup_tables.py

setup-aws:
	python aws/setup_tables.py

seed:
	docker compose run --rm --entrypoint "" app python aws/seed_data.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete

# ── Docker targets ────────────────────────────────────────────────────────────

docker-build:
	docker compose build

docker-up:
	docker compose up -d dynamodb
	@echo "Waiting for DynamoDB Local to be healthy..."
	docker compose run --rm --entrypoint "" app python aws/setup_tables.py

docker-down:
	docker compose down -v

docker-setup:
	docker compose run --rm --entrypoint "" app python aws/setup_tables.py

docker-seed:
	docker compose run --rm --entrypoint "" app python aws/seed_data.py

docker-test:
	docker compose run --rm --entrypoint "" app python -m pytest tests/ -v

docker-logs:
	docker compose logs -f dynamodb

# Run any CLI command: make docker-run CMD="product list"
docker-run:
	docker compose run --rm -it app python main.py $(CMD)

# ── API targets ───────────────────────────────────────────────────────────────

api:
	USE_LOCAL_DYNAMODB=true python api.py

api-docker:
	docker compose up dynamodb api

# ── Frontend targets ──────────────────────────────────────────────────────────

frontend:
	cd frontend && npm install && npm run dev

frontend-docker:
	docker compose up dynamodb api frontend

# Start everything locally (API + frontend) without Docker
dev:
	@echo "Starting API in background..."
	USE_LOCAL_DYNAMODB=true python api.py &
	@echo "Starting frontend..."
	cd frontend && npm run dev
