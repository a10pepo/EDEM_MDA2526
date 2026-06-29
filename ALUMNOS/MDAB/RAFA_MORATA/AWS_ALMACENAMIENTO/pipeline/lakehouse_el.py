"""EL: extrae de PostgreSQL (RDS) y escribe en un data lakehouse.

Tecnología: Apache Iceberg como formato de tabla, Amazon S3 como
almacenamiento y AWS Glue Data Catalog como catálogo de metadatos.
Se usa `overwrite` para que el proceso sea idempotente (re-ejecutable).
"""
import pyarrow as pa
from pyiceberg.catalog import load_catalog

from . import config, db

# Esquemas Iceberg/PyArrow (equivalentes al modelo transaccional)
SCHEMAS = {
    "airplanes": pa.schema([
        ("plate_number", pa.string()),
        ("type", pa.string()),
        ("last_maintenance_date", pa.date32()),
        ("next_maintenance_date", pa.date32()),
        ("capacity", pa.int32()),
        ("owner_id", pa.string()),
        ("owner_name", pa.string()),
        ("hangar_id", pa.string()),
        ("fuel_capacity", pa.int32()),
    ]),
    "passengers": pa.schema([
        ("passenger_id", pa.string()),
        ("name", pa.string()),
        ("national_id", pa.string()),
        ("date_of_birth", pa.date32()),
    ]),
    "flights": pa.schema([
        ("flight_id", pa.string()),
        ("plate_number", pa.string()),
        ("arrival_time", pa.timestamp("us")),
        ("departure_time", pa.timestamp("us")),
        ("fuel_consumption", pa.int32()),
        ("occupied_seats", pa.int32()),
        ("origin", pa.string()),
        ("destination", pa.string()),
    ]),
    "flight_passengers": pa.schema([
        ("flight_id", pa.string()),
        ("passenger_id", pa.string()),
        ("status", pa.string()),
    ]),
}


def _catalog():
    """Catálogo Iceberg respaldado por AWS Glue (credenciales vía boto3)."""
    return load_catalog(
        "glue",
        **{
            "type": "glue",
            "warehouse": config.ICEBERG_WAREHOUSE,
            # Claves específicas de PyIceberg para pasar la región a los
            # clientes de Glue (catálogo) y S3 (PyArrowFileIO).
            "glue.region": config.AWS_REGION,
            "s3.region": config.AWS_REGION,
        },
    )


def run():
    catalog = _catalog()
    source = db.connect_postgres()
    try:
        try:
            catalog.create_namespace(config.GLUE_DATABASE)
        except Exception:
            pass  # el namespace (base de datos Glue) ya existe

        for table, schema in SCHEMAS.items():
            rows = db.fetch_dicts(source, table)
            arrow_table = pa.Table.from_pylist(rows, schema=schema)

            identifier = f"{config.GLUE_DATABASE}.{table}"
            if not catalog.table_exists(identifier):
                catalog.create_table(identifier, schema=schema)

            iceberg_table = catalog.load_table(identifier)
            iceberg_table.overwrite(arrow_table)
            print(
                f"[lakehouse] {table}: {arrow_table.num_rows} filas "
                f"en Iceberg/Glue/S3 ({identifier})."
            )
    finally:
        source.close()


if __name__ == "__main__":
    run()
