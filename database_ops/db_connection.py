from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOSTNAME')}/{os.getenv('DATABASE')}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    '''Creating db session'''
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()