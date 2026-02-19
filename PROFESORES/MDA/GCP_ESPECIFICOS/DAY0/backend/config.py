import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://admin-user:password-super-secreto-123@34.14.31.92:5432/mi-base-de-datos'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
