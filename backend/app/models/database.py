from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    item_id = Column(String, ForeignKey("items.item_id"))
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer)
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)