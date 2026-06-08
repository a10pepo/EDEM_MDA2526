import logging
import os
import psycopg2
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

RDS_HOST = os.environ['RDS_HOST']
RDS_PORT = os.environ['RDS_PORT']
RDS_USER = os.environ['RDS_USER']
RDS_PASSWORD = os.environ['RDS_PASSWORD']
RDS_DB = os.environ['RDS_DB'] 

def connect_to_postgres_rds() -> psycopg2.extensions.connection:
    conn = psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )
    return conn

def create_wellhub_table(conn: psycopg2.extensions.connection) -> None:
    """Create the wellhub_trainings table if it doesn't exist."""
    conn.autocommit = True
    cur = conn.cursor()
    
    # Table creation query
    query = """
    CREATE TABLE IF NOT EXISTS wellhub_trainings (
        id SERIAL PRIMARY KEY,
        fecha TIMESTAMP WITH TIME ZONE,
        tipo_registro VARCHAR(50),     -- Booking / Checkin
        estado VARCHAR(50),            -- Completed / Cancelled / No-show / ...
        gimnasio VARCHAR(150),         -- Partner gym name
        tipo_clase VARCHAR(100),       -- Class type (e.g., Yoga, Crossfit, etc.)
        precio_individual NUMERIC(5,2) -- Price per session (calculated based on the original price in Glue)
    );
    """
    cur.execute(query)
    cur.close()

if __name__ == "__main__":
    try:
        logging.info("Connecting to RDS (PostgreSQL)...")
        conn = connect_to_postgres_rds()
        
        # 1. Create the database if it doesn't exist
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if the database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname='wellhub_db';")
        exists = cur.fetchone()
        
        if not exists:
            logging.info("🏗️ Creating the 'wellhub_db' database...")
            cur.execute("CREATE DATABASE wellhub_db;")
            logging.info("✅ Database 'wellhub_db' created.")
        else:
            logging.info("ℹ️ The database 'wellhub_db' already exists.")
            
        cur.close()
        conn.close()
        
        # 2. Now we connect directly to the new database to create the table
        logging.info("🔗 Connecting to the new 'wellhub_db' database...")
        conn = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database="wellhub_db" 
        )
        
        logging.info("🏗️ Creating table 'wellhub_trainings'...")
        create_wellhub_table(conn)
        logging.info("✅ Table ready to receive data.")
        
        conn.close()
        logging.info("🔒 Connection closed cleanly.")
        
    except Exception as e:
        logging.error(f"❌ An error occurred: {e}")