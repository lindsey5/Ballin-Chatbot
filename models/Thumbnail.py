from sqlalchemy import Column, Integer, String, ForeignKey
from config.db import Base

class Thumbnail(Base):
    __tablename__ = 'thumbnails'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True, nullable=False)
    thumbnailUrl = Column(String(255), nullable=False)
    thumbnailPublicId = Column(String(255), nullable=False)
