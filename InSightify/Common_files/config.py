import os

class config:
    # Example PostgreSQL URL:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        "postgresql://aaki:1234@192.168.1.35:5490/NewInSightify"
    )
    DATABASE_SCHEMA = os.getenv(
        'DATABASE_SCHEMA',"in_use"
    )
    # SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')