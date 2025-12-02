import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from config.db import Base

class CustomerStatus(enum.Enum):
    Active = "Active"
    Deactivated = "Deactivated"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, ForeignKey("orders.customer_id"), primary_key=True, autoincrement=True)
    firstname = Column(String(255), nullable=False, unique=True)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    status = Column(Enum(CustomerStatus), nullable=False, default=CustomerStatus.Active)
    order = relationship("Order", back_populates="customer")

