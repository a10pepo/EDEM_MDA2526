import pandas as pd
import psycopg
import os

reemplazos = str.maketrans("áéíóúÁÉÍÓÚüÜ", "aeiouAEIOUuU")

def create_rae_table():
    try:
        # Get database connection
        url = os.getenv("DATABASE_URL")
        connection = psycopg.connect(url)
        cur = connection.cursor()

        # Create RAE table
        cur.execute("DROP TABLE IF EXISTS rae")
        cur.execute("""
        CREATE TABLE rae (
            palabra VARCHAR(100) PRIMARY KEY
        );""")
        print("table created")
        connection.commit()
        
        # Read CSV file - only first column
        df = pd.read_csv('palabras.csv', usecols=[0])
        
        # Insert words into RAE table, ignoring duplicates
        for index, row in df.iterrows():
            normalized_word = normalizar(row.iloc[0])
            query = """
            INSERT INTO rae (palabra) 
            VALUES (%s)
            ON CONFLICT (palabra) DO NOTHING;
            """
            cur.execute(query, (normalized_word,))
        
        connection.commit()
        print("RAE table created and populated successfully")
        
    except:
        print(f"Error")
        if 'connection' in locals():
            connection.rollback()
    finally:
        if 'connection' in locals():
            cur.close()
            connection.close()

def normalizar(s) :
    if s is None:
        return s
    return s.strip().lower().translate(reemplazos)

if __name__ == "__main__":
    create_rae_table()