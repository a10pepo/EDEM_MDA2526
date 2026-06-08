import pandas as pd
from dotenv import load_dotenv
import os

# .env credentials loading...
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connection URL for pandas
conexion_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

try:
    print("🔄 Connecting to the RDS database...")
    
    df = pd.read_sql("SELECT * FROM wellhub_trainings;", conexion_url)
    
    print("\n=======================================================")
    print(f"🎉 SUCCESSFUL CONNECTION! Number of rows found: {len(df)}")
    print("=======================================================\n")
    
    # Shows the columns and the first 10 rows of the dataframe
    print(df.head(10))
    
except Exception as e:
    print("\n❌ Error when connecting or reading the table:")
    print(e)