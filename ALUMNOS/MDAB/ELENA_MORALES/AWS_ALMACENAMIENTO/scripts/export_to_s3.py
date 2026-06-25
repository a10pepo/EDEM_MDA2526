"""Exportación sencilla de tablas a CSV para subir a S3.

Este módulo deja preparada una base mínima para el entregable de AWS:
- leer datos desde la base relacional
- convertirlos a CSV
- prepararlos para subir a S3
"""

import csv
import io
import os
import sys
from pathlib import Path
from typing import Iterable

from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from app.database import SessionLocal
except ImportError:  # Compatibilidad si se ejecuta como script desde la carpeta scripts
    from database import SessionLocal


def rows_to_csv_bytes(rows: Iterable[dict]) -> bytes:
    """Convierte una lista de filas a bytes CSV."""
    rows = list(rows)
    output = io.StringIO()
    fieldnames = list(rows[0].keys()) if rows else []
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def export_table_to_csv(table_name: str, output_path: str | None = None) -> bytes:
    """Exporta una tabla a CSV usando SQLAlchemy.

    Si output_path se proporciona, también guarda el fichero localmente.
    """
    db = SessionLocal()
    try:
        query = text(f"SELECT * FROM {table_name}")
        rows = [dict(row._mapping) for row in db.execute(query)]
    finally:
        db.close()

    csv_bytes = rows_to_csv_bytes(rows)

    if output_path:
        with open(output_path, "wb") as fh:
            fh.write(csv_bytes)

    return csv_bytes


def export_all_tables(output_dir: str = "exports") -> dict[str, bytes]:
    """Exporta las tablas principales del proyecto a CSV."""
    os.makedirs(output_dir, exist_ok=True)
    tables = ["products", "customers", "orders", "order_customers"]
    exported = {}
    for table in tables:
        path = os.path.join(output_dir, f"{table}.csv")
        exported[table] = export_table_to_csv(table, output_path=path)
    return exported


def upload_directory_to_s3(local_dir: str, bucket_name: str, prefix: str = "", client=None) -> list[dict]:
    """Sube todos los ficheros de un directorio a un bucket S3."""
    if not bucket_name:
        raise ValueError("bucket_name es obligatorio")

    if client is None:
        try:
            import boto3
        except ImportError as exc:  # pragma: no cover - depende del entorno
            raise RuntimeError("boto3 es necesario para subir ficheros a S3") from exc

        client = boto3.client("s3", region_name=os.getenv("AWS_DEFAULT_REGION"))

    uploaded = []
    for root, _, files in os.walk(local_dir):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_dir)
            key = f"{prefix.rstrip('/')}/{relative_path}" if prefix else relative_path
            client.upload_file(local_path, bucket_name, key)
            uploaded.append({"local_path": local_path, "bucket": bucket_name, "key": key})
    return uploaded


def upload_exports_to_s3(bucket_name: str | None = None, prefix: str | None = None, local_dir: str = "exports", client=None) -> list[dict]:
    """Sube la carpeta de exportaciones a S3 usando variables de entorno por defecto."""
    bucket_name = bucket_name or os.getenv("S3_BUCKET_NAME")
    prefix = prefix or os.getenv("S3_PREFIX", "exports")
    if not bucket_name:
        raise ValueError("S3_BUCKET_NAME es obligatorio o pasa bucket_name")
    return upload_directory_to_s3(local_dir, bucket_name, prefix=prefix, client=client)


if __name__ == "__main__":
    export_all_tables()
    print("Archivos CSV generados en la carpeta exports/")
    try:
        upload_exports_to_s3()
        print("Archivos subidos a S3.")
    except Exception as exc:
        print(f"No se pudo subir a S3: {exc}")
