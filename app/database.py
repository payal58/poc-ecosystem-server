from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set. Please check your .env file.")

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    echo=False  # Set to True for SQL query logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

