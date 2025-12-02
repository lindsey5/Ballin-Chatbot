from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class OrderAddress(Base):
    __tablename__ = "orderaddresses"

    order_id = Column(String(100), ForeignKey("orders.order_id"), primary_key=True, nullable=False)
    fullname = Column(String(200), nullable=False)
    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200), nullable=False)
    admin_area_1 = Column(String(200), nullable=False)
    admin_area_2 = Column(String(200), nullable=False)
    postal_code = Column(String(200), nullable=False)
    phone = Column(String(11), nullable=False)

    # relationship back to Order
    order = relationship("Order", back_populates="order_address")
