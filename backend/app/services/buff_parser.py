import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timezone
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
import asyncio
import logger

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

    async def get_item_price(self, market_hash_name: str) -> Optional[float]:
        """Get current price for a specific item"""
        try:
            await asyncio.sleep(1)

            if not market_hash_name or not isinstance(market_hash_name, str):
                logger.error(f"Invalid item name: {market_hash_name}")
                return None
            
            params = {
                'game': 'csgo',
                'page_num': 1,
                'search': market_hash_name
            }
            response = await self._make_request(self.base_url, params)
            if response and response.get('code') == 'OK':
                items = response.get('data', {}).get('items', [])
                if items:
                    price = items[0].get('sell_min_price')
                    if price is not None and float(price) > 0:
                        return float(price)
                    logger.warning(f"Invalid price for {market_hash_name}: {price}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting price for {market_hash_name}: {e}")
            return None

    async def get_item_details(self, market_hash_name: str) -> Optional[Dict]:
        """Get detailed information about an item"""
        try:
            await asyncio.sleep(1)
            
            if not market_hash_name or not isinstance(market_hash_name, str):
                logger.error(f"Invalid item name: {market_hash_name}")
                return None
                
            params = {
                'game': 'csgo',
                'page_num': 1,
                'search': market_hash_name
            }
            
            response = await self._make_request(self.base_url, params)
            if response and response.get('code') == 'OK':
                items = response.get('data', {}).get('items', [])
                if items:
                    item = items[0]
                    sell_min_price = item.get('sell_min_price')
                    steam_price = item.get('steam_price_cny')
                    
                    if sell_min_price is not None and steam_price is not None:
                        return {
                            'market_hash_name': item.get('market_hash_name'),
                            'sell_min_price': float(sell_min_price),
                            'sell_num': int(item.get('sell_num', 0)),
                            'steam_price': float(steam_price),
                            'buff_price': float(sell_min_price),
                            'updated_at': datetime.now(timezone.utc)
                        }
                    logger.warning(f"Invalid prices for {market_hash_name}: buff={sell_min_price}, steam={steam_price}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting details for {market_hash_name}: {e}")
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