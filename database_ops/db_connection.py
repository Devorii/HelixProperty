from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOSTNAME')}/{os.getenv('DATABASE')}"
# Set up connection pool
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,  # Maximum number of connections to keep in the pool
    max_overflow=20,  # Number of connections allowed beyond pool_size
    pool_timeout=30,  # Timeout in seconds before giving up on getting a connection
    pool_pre_ping=True,  # Automatically ping the database to check for stale connections
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    '''Creating db session'''
    db=SessionLocal()
    try: 
        yield db
    finally:
        db.close()