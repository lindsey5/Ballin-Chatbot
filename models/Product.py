import enum
from config.db import Base
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

class ProductStatus(enum.Enum):
    Available = "Available"
    Deleted = "Deleted"

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    status = Column(Enum(ProductStatus), nullable=False, default=ProductStatus.Available)

    variants = relationship("Variant", backref="product")
    thumbnail = relationship("Thumbnail", uselist=False, backref="product")
    order_items = relationship("OrderItem", back_populates="product")