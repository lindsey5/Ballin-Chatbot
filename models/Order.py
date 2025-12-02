import enum
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from models.Customer import Customer
from config.db import Base

class OrderStatus(enum.Enum):
    Pending = "Pending"
    Confirmed = "Confirmed"
    Shipped = "Shipped"
    Delivered = "Delivered"
    Received = "Received"
    Cancelled = "Cancelled"
    Rejected = "Rejected"
    Failed = "Failed"

class PaymentMethod(enum.Enum):
    COD = "COD"
    GCASH = "GCASH"
    PAYMAYA = "PAYMAYA"

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String(255), primary_key=True, nullable=False)
    customer_id = Column(Integer, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.Pending)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    subtotal = Column(Float, nullable=False)
    shipping_fee = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    order_date = Column(DateTime, nullable=False)
    cancellation_reason = Column(String(255), nullable=True)

    # Relationships
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    order_address = relationship("OrderAddress", back_populates="order", uselist=False)
    customer = relationship("Customer", back_populates="order", uselist=False)
