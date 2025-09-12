from fastapi import APIRouter, HTTPException
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from datetime import datetime, timezone

load_dotenv()

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

db_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'cs2skins'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')
}

class ItemCreate(BaseModel):
    market_hash_name: str
    item_type: str
    weapon_type: str
    skin_name: str
    wear: str

@router.post("/")
async def create_item(item: ItemCreate):
    """Create a new item"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT item_id FROM items 
            WHERE market_hash_name = %s
        """, (item.market_hash_name,))
        
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Item already exists")
        
        cur.execute("""
            INSERT INTO items 
            (market_hash_name, item_type, weapon_type, skin_name, wear, created_at)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING *
        """, (
            item.market_hash_name,
            item.item_type,
            item.weapon_type,
            item.skin_name,
            item.wear
        ))
        
        new_item = cur.fetchone()
        conn.commit()
        return new_item
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()

@router.get("/")
async def get_items():
    """Get all items from database"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM items 
            ORDER BY created_at DESC
        """)
        
        items = cur.fetchall()
        return items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()