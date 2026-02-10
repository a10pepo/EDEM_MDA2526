import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:Edem2526.@34.65.201.193:5432/tienda_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
