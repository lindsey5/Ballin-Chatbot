from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.db import Base

class Variant(Base):
    __tablename__ = 'variants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    sku = Column(String(255), nullable=False, unique=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    size = Column(String(50), nullable=True)
    color = Column(String(50), nullable=False)
