from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class OrderItem(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(255), ForeignKey("orders.order_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    size = Column(String(50), nullable=False)
    color = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="order_items") 
    product = relationship("Product", back_populates="order_items")
