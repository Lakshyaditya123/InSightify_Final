from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from InSightify.Common_files.config import config


class InsightifyDB:
    def __init__(self):
        self.config=config
        self.engine = create_engine(config.DATABASE_URL, echo=True)

    def get_engine(self):
        return self.engine

    def get_session(self):
        session = sessionmaker(bind=self.engine, reflect=True)
        return session()
    @staticmethod
    def get_metadata():
        return MetaData(schema=config.DATABASE_SCHEMA)
