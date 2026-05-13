from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv, find_dotenv
import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Optional

load_dotenv(find_dotenv())


def get_secret(secret_name: Optional[str] = None, region_name: str = "us-east-1") -> dict:
    if not secret_name:
        raise ValueError("AWS secret name is required when USE_AWS_SECRETS is set to true.")

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    secret_string = get_secret_value_response.get("SecretString")
    if not secret_string:
        raise ValueError(f"Secret {secret_name} did not contain a SecretString")

    return json.loads(secret_string)


def load_database_url() -> str:
    database_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URL")
    if database_url:
        return database_url

    if os.getenv("USE_AWS_SECRETS", "").lower() == "true":
        secret_name = os.getenv("AWS_SECRET_NAME") or os.getenv("AWS_SSM_USERNAME")
        region_name = os.getenv("AWS_SECRET_REGION", "us-east-1")
        secret_values = get_secret(secret_name, region_name)

        username = secret_values.get("USERNAME")
        password = secret_values.get("PASSWORD")
        hostname = secret_values.get("HOSTNAME")
        database = secret_values.get("DATABASE")
    else:
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        hostname = os.getenv("HOSTNAME")
        database = os.getenv("DATABASE")

    if not all([username, password, hostname, database]):
        raise ValueError(
            "Database configuration is incomplete."
            " Set DATABASE_URL or USERNAME/PASSWORD/HOSTNAME/DATABASE in environment,"
            " or set USE_AWS_SECRETS=true with AWS_SECRET_NAME pointing to Secrets Manager."
        )

    return f"mysql+pymysql://{username}:{password}@{hostname}/{database}"



SQLALCHEMY_DATABASE_URL = load_database_url()
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

Base=declarative_base()