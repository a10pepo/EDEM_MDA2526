# F1 Data Platform — End-to-End AWS Project

A cloud data engineering project built on the 2024 Formula 1 season. Covers the full stack: relational database (RDS), data lakehouse (S3 + Glue + Athena), REST API (FastAPI) and a React frontend.

## Architecture

```
src/initial_info.py   →   RDS PostgreSQL   →   S3 (Parquet)
     (seed data)           (OLTP layer)         Glue Catalog
                                ↓                    ↓
                           FastAPI /api          Athena queries
                                ↓
                         React frontend
```

## Project structure

```
end2end/
├── src/
│   ├── initial_info.py   # seed data — teams, drivers, races, results
│   ├── load_rds.py       # insert data into RDS (idempotent)
│   ├── load_glue.py      # RDS → Parquet on S3 → Glue Catalog
│   ├── pipeline.py       # runs load_rds + load_glue in one command
│   ├── api.py            # FastAPI — GET /teams /drivers /races /results
│   └── check_rds.py      # debug script to query RDS directly
├── db/
│   └── init.sql          # DDL — run once to create tables in RDS
├── tests/                # 26 pytest tests
├── frontend/             # React + Vite
├── .env.example          # copy to .env and fill in your values
└── requirements.txt
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your RDS endpoint and AWS credentials
```

### 3. Create tables in RDS (once)

```bash
psql -h $PGHOST -U $PGUSER -d $PGDATABASE -f db/init.sql
```

### 4. Run the full pipeline

```bash
python src/pipeline.py
```

This loads seed data into RDS and syncs everything to the Glue Data Lakehouse (Parquet on S3) in a single command.

## Adding new races

1. Append a new race dict to `races` in `src/initial_info.py`
2. Run `python src/pipeline.py` again

RDS only inserts new rows (`ON CONFLICT DO NOTHING`). Glue does a full-refresh from RDS, so the lakehouse stays in sync automatically.

## Running the API

```bash
uvicorn src.api:app --reload
```

Endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/teams` | All 10 constructor teams |
| GET | `/drivers` | All 20 drivers with their team |
| GET | `/races` | Races ordered by season and round |
| GET | `/results` | Race results with driver and race info |

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

Opens at `http://localhost:5173`.

## Running tests

```bash
pytest tests/ -v
```

Tests are fully offline — no RDS or AWS connection needed.
