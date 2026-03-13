"""
Module: database
Purpose: Handles database connection and session management using SQLAlchemy.
Author: Your Name
Created: 2023-10-27
Notes: Configures the SQLAlchemy engine and sessionmaker.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

# Create a SQLAlchemy engine
engine = create_engine(Config.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session.
    Yields a session that is automatically closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all tables defined in models.
    """
    # Import all models here to ensure they are registered with Base
    import models.cession_result
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
