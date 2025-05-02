"""CRUD operations for the database."""
from sqlalchemy.orm import Session

from . import models


def get_product(db: Session, product_id: int):
    """Get a product by ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """Get all products with pagination."""
    return db.query(models.Product).offset(skip).limit(limit).all()


def search_products(db: Session, name_query: str):
    """Search for products by name."""
    return db.query(models.Product).filter(
        models.Product.name.ilike(f"%{name_query}%")
    ).first()


def create_product(db: Session, name: str, description: str, price: float):
    """Create a new product."""
    db_product = models.Product(
        name=name,
        description=description,
        price=price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
