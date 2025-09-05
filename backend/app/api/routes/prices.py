from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import os

router = APIRouter(
    prefix="/prices",
    tags=["prices"]
)

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
            JOIN items i ON i.item_id = ph.item_id
            WHERE ph.item_id = %s
            AND ph.timestamp >= %s
        """
        params = [item_id, datetime.utcnow() - timedelta(days=days)]
        
        if source:
            query += " AND ph.source = %s"
            params.append(source)
            
        query += " ORDER BY ph.timestamp DESC"
        
        cur.execute(query, params)
        history = cur.fetchall()
        
        if not history:
            raise HTTPException(status_code=404, detail="No price history found")
            
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            cur.close()
            conn.close()

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