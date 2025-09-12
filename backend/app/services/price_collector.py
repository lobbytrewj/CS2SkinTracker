import asyncio
import logging
from datetime import datetime
from .steam_market_scraper import SteamMarketPrices
from .buff_parser import BuffParser
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceCollector:
    def __init__(self):
        self.steam_scraper = SteamMarketPrices()
        self.buff_parser = BuffParser()
        self.db_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT')
        }

    async def collect_and_store_prices(self):
        """Collect prices from both Steam and Buff"""
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all items from database
            cur.execute("SELECT item_id, market_hash_name FROM items")
            items = cur.fetchall()
            
            for item in items:
                # Get Steam price
                steam_price = await self.steam_scraper.get_item_price(item['market_hash_name'])
                if steam_price:
                    cur.execute("""
                        INSERT INTO price_history (item_id, price, volume, source)
                        VALUES (%s, %s, %s, 'steam')
                    """, (item['item_id'], steam_price['lowest_price'], steam_price.get('volume')))
                
                # Get Buff price
                buff_price = await self.buff_parser.get_item_price(item['market_hash_name'])
                if buff_price:
                    cur.execute("""
                        INSERT INTO price_history (item_id, price, source)
                        VALUES (%s, %s, 'buff')
                    """, (item['item_id'], buff_price))
                
                await asyncio.sleep(1)  # Rate limiting
                
            conn.commit()
            logger.info(f"Successfully collected prices for {len(items)} items")
            
        except Exception as e:
            logger.error(f"Error collecting prices: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()

if __name__ == "__main__":
    collector = PriceCollector()
    asyncio.run(collector.collect_and_store_prices())