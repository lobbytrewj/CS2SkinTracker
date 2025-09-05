from fastapi import APIRouter, HTTPException
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import os

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

db_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'cs2skins'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')
}

@router.get("/")
async def get_items(limit: int = 100):
    """Get all items from database"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM items 
            ORDER BY created_at DESC 
            LIMIT %s
        """, (limit,))
        
        items = cur.fetchall()
        return items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()

@router.get("/{item_id}")
async def get_item(item_id: str):
    """Get specific item details"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM items 
            WHERE item_id = %s
        """, (item_id,))
        
        item = cur.fetchone()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
            
        return item
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()

@router.get("/type/{type}")
async def get_items_by_type(type: str):
    """Get items by type (sale/purchase)"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM items 
            WHERE type = %s 
            ORDER BY created_at DESC
        """, (type,))
        
        items = cur.fetchall()
        return items
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()