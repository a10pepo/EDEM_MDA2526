import os


def load_psycopg():
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as error:
        raise RuntimeError(
            "Missing dependency: psycopg. Install it with: pip install -r requirements.txt"
        ) from error

    return psycopg, dict_row


def get_env(names, default=None, required=True):
    for name in names:
        value = os.getenv(name)
        if value:
            return value

    if required:
        readable_names = " or ".join(names)
        raise RuntimeError(f"Missing required environment variable: {readable_names}")

    return default


def connect():
    psycopg, dict_row = load_psycopg()
    return psycopg.connect(
        host=get_env(("RDS_HOST", "DB_HOST")),
        port=int(get_env(("RDS_PORT", "DB_PORT"), default="5432", required=False)),
        dbname=get_env(("RDS_DATABASE", "DB_NAME")),
        user=get_env(("RDS_USER", "DB_USER")),
        password=get_env(("RDS_PASSWORD", "DB_PASSWORD")),
        sslmode=get_env(("RDS_SSLMODE", "DB_SSLMODE"), default="require", required=False),
        row_factory=dict_row,
    )


def fetch_all_dicts(cursor):
    return cursor.fetchall()


def fetch_one_dict(cursor):
    return cursor.fetchone()


def query_all(connection, sql, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params or ())
        return fetch_all_dicts(cursor)
    finally:
        cursor.close()


def query_one(connection, sql, params=None):
    cursor = connection.cursor()
    try:
        cursor.execute(sql, params or ())
        return fetch_one_dict(cursor)
    finally:
        cursor.close()


def execute_many(connection, sql, rows):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, rows)
    finally:
        cursor.close()
