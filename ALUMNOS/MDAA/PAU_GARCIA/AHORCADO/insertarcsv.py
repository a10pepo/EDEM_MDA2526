import pandas as pd
import psycopg
import os

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
            query = """
            INSERT INTO rae (palabra) 
            VALUES (%s)
            ON CONFLICT (palabra) DO NOTHING;
            """
            cur.execute(query, (row.iloc[0],))
            print(row.iloc[0] + " introducida")
        
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

if __name__ == "__main__":
    create_rae_table()