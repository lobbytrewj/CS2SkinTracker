import asyncio
import logging
from datetime import datetime
#from .steam_market_scraper import SteamMarketPrices
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
        #self.steam_scraper = SteamMarketPrices()
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
        conn = None
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor(cursor_factory=RealDictCursor)
            
            cur.execute("BEGIN")

            cur.execute("SELECT item_id, market_hash_name FROM items")
            items = cur.fetchall()
            
            for item in items:
                try:
                    '''steam_price = self.steam_scraper.get_item_price(item['market_hash_name'])
                    if steam_price:
                        cur.execute("""
                            INSERT INTO price_history (item_id, price, volume, source, timestamp)
                            VALUES (%s, %s, %s, 'steam', CURRENT_TIMESTAMP)
                        """, (item['item_id'], steam_price['lowest_price'], steam_price.get('volume')))
                    '''
                    buff_price = await self.buff_parser.get_item_price(item['market_hash_name'])
                    if buff_price:
                        cur.execute("""
                            INSERT INTO price_history (item_id, price, source, timestamp)
                            VALUES (%s, %s, 'buff', CURRENT_TIMESTAMP)
                        """, (item['item_id'], buff_price))
                    
                    cur.execute("""
                        UPDATE items 
                        SET steam_price = %s, 
                            buff_price = %s,
                            volume = %s
                        WHERE item_id = %s
                    """, (
                        #steam_price['lowest_price'] if steam_price else None,
                        buff_price if buff_price else None,
                        #steam_price.get('volume') if steam_price else None,
                        item['item_id']
                    ))
                    
                    logger.info(f"Collected prices for {item['market_hash_name']}")
                    
                except Exception as e:
                    logger.error(f"Error collecting prices for {item['market_hash_name']}: {e}")
                    continue
            
            cur.execute("COMMIT")
            logger.info(f"Successfully collected prices for {len(items)} items")
            
        except Exception as e:
            if conn:
                cur.execute("ROLLBACK")
            logger.error(f"Error in price collection: {e}")
            raise
        finally:
            if conn:
                cur.close()
                conn.close()

    async def collect_steam_prices(self, items):
        """Collect prices from Steam Market"""
        for item in items:
            try:
                price_data = await self.steam_scraper.get_item_price(item['market_hash_name'])
                if price_data:
                    logger.info(f"Steam price for {item['market_hash_name']}: {price_data}")
                    yield {
                        'item_id': item['item_id'],
                        'price': price_data['lowest_price'],
                        'volume': price_data.get('volume'),
                        'source': 'steam'
                    }
            except Exception as e:
                logger.error(f"Error getting Steam price for {item['market_hash_name']}: {e}")
                continue

    async def collect_buff_prices(self, items):
        """Collect prices from Buff"""
        for item in items:
            try:
                price = await self.buff_parser.get_item_price(item['market_hash_name'])
                if price:
                    logger.info(f"Buff price for {item['market_hash_name']}: {price}")
                    yield {
                        'item_id': item['item_id'],
                        'price': price,
                        'source': 'buff'
                    }
            except Exception as e:
                logger.error(f"Error getting Buff price for {item['market_hash_name']}: {e}")
                continue