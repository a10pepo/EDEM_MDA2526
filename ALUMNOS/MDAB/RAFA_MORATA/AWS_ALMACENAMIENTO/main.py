"""Punto de entrada (CLI) del pipeline end2end de almacenamiento en AWS.

Uso:
    python main.py postgres    # crea el modelo y carga datos en RDS
    python main.py redshift    # EL de RDS a Redshift
    python main.py lakehouse   # EL al lakehouse Iceberg/S3/Glue
    python main.py all         # ejecuta los tres pasos en orden
"""
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="End2End AWS Almacenamiento (aviación)."
    )
    parser.add_argument(
        "step",
        choices=["postgres", "redshift", "lakehouse", "all"],
        help="paso del pipeline a ejecutar",
    )
    args = parser.parse_args()

    # Importes perezosos: ejecutar 'postgres' no requiere pyiceberg instalado.
    if args.step in ("postgres", "all"):
        from pipeline import postgres_load
        postgres_load.run()

    if args.step in ("redshift", "all"):
        from pipeline import redshift_el
        redshift_el.run()

    if args.step in ("lakehouse", "all"):
        from pipeline import lakehouse_el
        lakehouse_el.run()


if __name__ == "__main__":
    main()
