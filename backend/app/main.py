from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv
from typing import List, Dict, Optional
from psycopg2.extras import RealDictCursor
import statistics
import os
from app.api.routes import items, prices
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

db_params = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'cs2skins'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT', '5432')
}

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(items.router, prefix="/api")
app.include_router(prices.router, prefix="/api")

@app.get("/skin/{item_id}")
async def skin_detail(request: Request, item_id: int):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT * FROM items WHERE item_id = %s
        """, (item_id,))
        item = cur.fetchone()
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        cur.execute("""
            SELECT price, timestamp::date as date
            FROM price_history
            WHERE item_id = %s
            AND timestamp >= NOW() - INTERVAL '7 days'
            ORDER BY timestamp ASC
        """, (item_id,))
        history = cur.fetchall()
        
        price_history = {
            "dates": [h['date'].strftime('%Y-%m-%d') for h in history],
            "prices": [float(h['price']) for h in history]
        }
        
        prices = [float(h['price']) for h in history]
        stats = {
            "avg_price": statistics.mean(prices) if prices else None,
            "max_price": max(prices) if prices else None,
            "min_price": min(prices) if prices else None
        }
        
        return templates.TemplateResponse("skin_details.html", {
            "request": request,
            "item": item,
            "price_history": price_history,
            "stats": stats
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
@app.get("/")
@app.get("/skins")
async def list_skins(
    request: Request,
    weapon_type: Optional[str] = None,
    wear: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "name",
    order: Optional[str] = "asc"
):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT DISTINCT weapon_type FROM items ORDER BY weapon_type")
        weapon_types = [row['weapon_type'] for row in cur.fetchall()]
        
        cur.execute("SELECT DISTINCT wear FROM items WHERE wear IS NOT NULL ORDER BY wear")
        wears = [row['wear'] for row in cur.fetchall()]
        
        query = """
            SELECT i.*, 
                   COALESCE(ph.price, i.buff_price) as current_price,
                   ph.timestamp as price_updated
            FROM items i
            LEFT JOIN (
                SELECT DISTINCT ON (item_id) item_id, price, timestamp
                FROM price_history
                ORDER BY item_id, timestamp DESC
            ) ph ON i.item_id = ph.item_id
            WHERE 1=1
        """
        params = []
        
        if weapon_type:
            query += " AND i.weapon_type = %s"
            params.append(weapon_type)
        
        if wear:
            query += " AND i.wear = %s"
            params.append(wear)
        
        if min_price:
            query += " AND COALESCE(ph.price, i.buff_price) >= %s"
            params.append(min_price)
        
        if max_price:
            query += " AND COALESCE(ph.price, i.buff_price) <= %s"
            params.append(max_price)
        
        sort_column = {
            "name": "i.market_hash_name",
            "price": "current_price",
            "type": "i.weapon_type",
            "wear": "i.wear"
        }.get(sort_by, "i.market_hash_name")
        
        query += f" ORDER BY {sort_column} {'DESC' if order == 'desc' else 'ASC'}"
        
        cur.execute(query, params)
        items = cur.fetchall()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total_items,
                AVG(COALESCE(ph.price, i.buff_price)) as avg_price,
                MIN(COALESCE(ph.price, i.buff_price)) as min_price,
                MAX(COALESCE(ph.price, i.buff_price)) as max_price
            FROM items i
            LEFT JOIN (
                SELECT DISTINCT ON (item_id) item_id, price
                FROM price_history
                ORDER BY item_id, timestamp DESC
            ) ph ON i.item_id = ph.item_id
        """)
        stats = cur.fetchone()
        
        return templates.TemplateResponse("skins.html", {
            "request": request,
            "items": items,
            "weapon_types": weapon_types,
            "wears": wears,
            "stats": stats,
            "filters": {
                "weapon_type": weapon_type,
                "wear": wear,
                "min_price": min_price,
                "max_price": max_price,
                "sort_by": sort_by,
                "order": order
            }
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.get("/analytics")
async def analytics(request: Request):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                COUNT(DISTINCT i.item_id) as total_items,
                COUNT(DISTINCT ph.id) as total_price_points,
                COALESCE(AVG(NULLIF(ph.price, 0)), 0) as overall_avg_price
            FROM items i
            LEFT JOIN price_history ph ON i.item_id = ph.item_id
        """)
        market_stats = cur.fetchone()
        
        cur.execute("""
            SELECT 
                i.market_hash_name,
                COALESCE(AVG(NULLIF(ph.price, 0)), 0) as avg_price,
                COALESCE(MIN(NULLIF(ph.price, 0)), 0) as min_price,
                COALESCE(MAX(NULLIF(ph.price, 0)), 0) as max_price,
                COUNT(DISTINCT ph.id) as data_points
            FROM items i
            LEFT JOIN price_history ph ON i.item_id = ph.item_id
            WHERE ph.timestamp >= NOW() - INTERVAL '30 days'
            GROUP BY i.market_hash_name
            HAVING COUNT(ph.id) > 0
            ORDER BY avg_price DESC
            LIMIT 10
        """)
        top_items = cur.fetchall() or []

        cur.execute("""
            WITH daily_prices AS (
                SELECT 
                    item_id,
                    DATE(timestamp) as date,
                    AVG(NULLIF(price, 0)) as avg_daily_price
                FROM price_history
                WHERE timestamp >= NOW() - INTERVAL '30 days'
                GROUP BY item_id, DATE(timestamp)
            ),
            price_changes AS (
                SELECT 
                    i.market_hash_name,
                    COALESCE(
                        (
                            MAX(CASE WHEN date = DATE(NOW()) THEN avg_daily_price END) -
                            MIN(CASE WHEN date = DATE(NOW() - INTERVAL '7 days') THEN avg_daily_price END)
                        ) / NULLIF(MIN(CASE WHEN date = DATE(NOW() - INTERVAL '7 days') THEN avg_daily_price END), 0) * 100,
                        0
                    ) as price_change
                FROM daily_prices dp
                JOIN items i ON dp.item_id = i.item_id
                GROUP BY i.market_hash_name
                HAVING COUNT(dp.avg_daily_price) > 0
            )
            SELECT 
                market_hash_name,
                CASE 
                    WHEN price_change::text = 'NaN' OR price_change::text = 'infinity' 
                    THEN 0 
                    ELSE price_change 
                END as price_change
            FROM price_changes
            WHERE price_change IS NOT NULL
            ORDER BY ABS(price_change) DESC
            LIMIT 5
        """)
        trending_items = cur.fetchall() or []

        if not market_stats:
            market_stats = {
                'total_items': 0,
                'total_price_points': 0,
                'overall_avg_price': 0
            }
        
        return templates.TemplateResponse("analytics.html", {
            "request": request,
            "top_items": top_items,
            "market_stats": market_stats,
            "trending_items": trending_items
        })
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating analytics. Please try again later."
        )
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()