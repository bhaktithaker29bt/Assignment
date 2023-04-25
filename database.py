"""Database config file"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = "sqlite:///./addresses.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Function to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()