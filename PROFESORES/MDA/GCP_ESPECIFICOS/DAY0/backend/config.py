import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:pass.@db:5432/tienda_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
