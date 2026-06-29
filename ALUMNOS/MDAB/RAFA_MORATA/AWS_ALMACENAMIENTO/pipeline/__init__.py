"""Pipeline end2end de almacenamiento en AWS para datos de aviación.

Pasos:
  - postgres_load : modela y carga los datos en PostgreSQL (RDS).
  - redshift_el   : EL de la BBDD transaccional a Redshift (analítica).
  - lakehouse_el  : EL al data lakehouse (Iceberg + S3 + Glue).
"""
