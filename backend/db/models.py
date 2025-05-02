"""SQLAlchemy models for the ecommerce database."""
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    """Product model representing items in the ecommerce store."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    
    def to_dict(self):
        """Convert model instance to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "url": f"/products/{self.id}"
        }
