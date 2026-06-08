import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DBConfig:
    host: str
    db: str
    user: str
    password: str
    port: int


def load_rds_config() -> DBConfig:
    """Read RDS (Postgres) connection settings from environment variables."""
    return DBConfig(
        host=os.getenv("RDS_HOST", ""),
        db=os.getenv("RDS_DB", ""),
        user=os.getenv("RDS_USER", ""),
        password=os.getenv("RDS_PASSWORD", ""),
        port=int(os.getenv("RDS_PORT", "5432")),
    )


def load_redshift_config() -> DBConfig:
    """Read Redshift connection settings from environment variables."""
    return DBConfig(
        host=os.getenv("REDSHIFT_HOST", ""),
        db=os.getenv("REDSHIFT_DB", ""),
        user=os.getenv("REDSHIFT_USER", ""),
        password=os.getenv("REDSHIFT_PASSWORD", ""),
        port=int(os.getenv("REDSHIFT_PORT", "5439")),
    )


CSV_PATH = "raw_data/workout_data.csv"
