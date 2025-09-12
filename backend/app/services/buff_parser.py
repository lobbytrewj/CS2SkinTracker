import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

class BuffParser:
    def __init__(self):
        self.db_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'cs2skins'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        self.base_url = "https://buff.163.com/api/market/goods"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def connect_db(self):
        """Establish database connection"""
        try:
            conn = psycopg2.connect(**self.db_params)
            conn.autocommit = True  # Add this line
            return conn
        except psycopg2.Error as e:
            print(f"Database connection failed: {e}")
            return None

    async def get_item_price(self, item_name: str) -> Optional[float]:
        """Get current price for a specific item"""
        try:
            params = {
                'game': 'csgo',
                'page_num': 1,
                'search': item_name
            }
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data['code'] == 'OK' and data['data']['items']:
                return float(data['data']['items'][0]['sell_min_price'])
            return None
        except requests.RequestException as e:
            print(f"Error fetching price for {item_name}: {e}")
            return None

    async def get_items(self, limit: int = 100) -> List[Dict]:
        """Get all items from database"""
        conn = self.connect_db()
        if not conn:
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT * FROM items 
                ORDER BY created_at DESC 
                LIMIT %s
            """, (limit,))
            items = cur.fetchall()
            return items
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    async def get_item(self, item_id: str) -> Optional[Dict]:
        """Get specific item details"""
        conn = self.connect_db()
        if not conn:
            return None
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT * FROM items 
                WHERE item_id = %s
            """, (item_id,))
            item = cur.fetchone()
            return item
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn:
                conn.close()

    async def get_price_history(self, item_id: str) -> List[Dict]:
        """Get price history for an item"""
        conn = self.connect_db()
        if not conn:
            return []
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT * FROM price_history 
                WHERE item_id = %s 
                ORDER BY timestamp DESC
            """, (item_id,))
            history = cur.fetchall()
            return history
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []
        finally:
            if conn:
                conn.close()

    async def update_prices(self):
        """Update prices for all items in database"""
        conn = self.connect_db()
        if not conn:
            return
        
        try:
            cur = conn.cursor()
            # Get all items
            cur.execute("SELECT item_id, market_hash_name FROM items")
            items = cur.fetchall()
            
            for item_id, market_hash_name in items:
                price = await self.get_item_price(market_hash_name)
                if price:
                    cur.execute("""
                        UPDATE items 
                        SET buff_price = %s 
                        WHERE item_id = %s
                    """, (price, item_id))
                    
                    cur.execute("""
                        INSERT INTO price_history (item_id, price, source) 
                        VALUES (%s, %s, 'buff')
                    """, (item_id, price))
                    
                    conn.commit()
                
                time.sleep(1)
                
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()

    async def add_item(self, market_hash_name: str, item_type: str) -> Optional[Dict]:
        """Add a new item to track"""
        conn = self.connect_db()
        if not conn:
            return None
        
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM items WHERE market_hash_name = %s", (market_hash_name,))
            if cur.fetchone():
                return None
                
            price = await self.get_item_price(market_hash_name)
            
            cur.execute("""
                INSERT INTO items (market_hash_name, type, buff_price) 
                VALUES (%s, %s, %s)
                RETURNING *
            """, (market_hash_name, item_type, price))
            
            new_item = cur.fetchone()
            
            if price:
                cur.execute("""
                    INSERT INTO price_history (item_id, price, source) 
                    VALUES (%s, %s, 'buff')
                """, (new_item['item_id'], price))
            
            conn.commit()
            return new_item
            
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()