"""Database connection utility for the backend.

This module configures SQLAlchemy to connect to a PostgreSQL database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get DB URL from environment or use SQLite as fallback for development
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/mcp_poc"
)

# For SQLite fallback during development/testing
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # PostgreSQL connection
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory that will create new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """Dependency for database session injection.

    This function creates a new database session for each request
    and closes it when the request is done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database with tables and sample data.
    
    This will create all tables defined in the models and
    add sample products if the database is empty.
    """
    from . import models, crud
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Add sample data if not exists
    db = SessionLocal()
    try:
        # Check if we already have products
        products = db.query(models.Product).all()
        if not products:
            # Add sample products
            crud.create_product(db, "Awesome Gadget", "Does cool stuff.", 99.99)
            crud.create_product(db, "Super Widget", "Makes life easier.", 49.50)
            print("Added sample products to database")
    finally:
        db.close()
