from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

db_params = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

class ItemCreate(BaseModel):
    market_hash_name: str
    item_type: str
    weapon_type: str
    skin_name: str
    wear: str

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)

@router.post("/")
async def add_item(item: dict):
    """Add a new item to the database"""
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
            (market_hash_name, type, weapon_type, skin_name, wear)
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
            SELECT 
                item_id,
                market_hash_name,
                item_type,
                weapon_type,
                skin_name,
                wear,
                steam_price,
                buff_price,
                volume,
                created_at
            FROM items 
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

@router.get("/{item_id}/history")
async def get_price_history(
    item_id: str,
    days: Optional[int] = Query(7, description="Number of days of history to fetch"),
    source: Optional[str] = Query(None, description="Filter by source (steam/buff)")
):
    """Get price history for a specific item"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT 
                ph.price,
                ph.volume,
                ph.source,
                ph.timestamp,
                i.market_hash_name
            FROM price_history ph
            JOIN items i ON ph.item_id = i.id
            WHERE ph.item_id = %s
            AND ph.timestamp >= %s
        """
        
        params = [item_id, datetime.now() - timedelta(days=days)]
        
        if source:
            query += " AND ph.source = %s"
            params.append(source)
            
        query += " ORDER BY ph.timestamp DESC"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return results
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching price history: {str(e)}")

@router.get("/analysis/{item_id}")
async def get_price_analysis(item_id: str):
    """Get price analysis for an item"""
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            WITH price_stats AS (
                SELECT 
                    AVG(price) as avg_price,
                    MIN(price) as min_price,
                    MAX(price) as max_price,
                    source
                FROM price_history
                WHERE item_id = %s
                AND timestamp >= NOW() - INTERVAL '7 days'
                GROUP BY source
            )
            SELECT 
                source,
                ROUND(avg_price::numeric, 2) as average_price,
                min_price,
                max_price
            FROM price_stats
        """, (item_id,))
        
        analysis = cur.fetchall()
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()