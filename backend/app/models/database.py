from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from sqlalchemy import Index

load_dotenv()

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    market_hash_name = Column(String, unique=True, nullable=False)
    item_type = Column(String, nullable=False)  # rifle, knife, etc.
    weapon_type = Column(String, nullable=False)  # AK-47, M4A4, etc.
    skin_name = Column(String, nullable=False)   # Redline, Asiimov, etc.
    wear = Column(String)                        # Factory New, Field-Tested, etc.
    #steam_price = Column(Float, nullable=True)
    buff_price = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

class PriceHistory(Base):
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey('items.item_id', ondelete='CASCADE'))
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=True)
    source = Column(String, nullable=False)  # 'steam' or 'buff'
    timestamp = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_price_history_item_id', 'item_id'),
        Index('idx_price_history_timestamp', 'timestamp'),
        Index('idx_price_history_source', 'source')
    )

def init_database():
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'cs2skins'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    db_url = f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}"
    
    engine = create_engine(db_url)
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    return engine

if __name__ == "__main__":
    init_database()