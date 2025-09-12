from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker  # Updated import
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)  # Added autoincrement
    market_hash_name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    wear = Column(String)
    steam_price = Column(Float)
    buff_price = Column(Float)
    volume = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.item_id', ondelete='CASCADE'), nullable=False)  # Updated foreign key
    price = Column(Float, nullable=False)
    volume = Column(Integer)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_database():
    # Drop and recreate database
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'cs2skins'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    db_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    
    # Create engine and tables
    engine = create_engine(db_url)
    
    # Drop existing tables and create new ones
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    return engine

if __name__ == "__main__":
    init_database()