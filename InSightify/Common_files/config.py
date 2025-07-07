import os

class config:
    # Example PostgreSQL URL:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        "postgresql://lakshyadityabhatnagar:Lab1234@localhost:5432/NewInSightify"
    )
    DATABASE_SCHEMA = os.getenv(
        'DATABASE_SCHEMA',"in_use"
    )
    # SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
    # LM_STUDIO_URL="http://192.168.1.17:1234/v1/chat/completions"
    MODEL_NAME = "google/gemma-3-12b"