import os

class config:
    # Example PostgreSQL URL:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        "postgresql://lakshyadityabhatnagar:Lab1234@localhost:5432/New_InSightify"
    )
    DATABASE_SCHEMA = os.getenv(
        'DATABASE_SCHEMA',"in_use"
    )
    # SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')