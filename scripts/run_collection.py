import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import schedule
import time
from datetime import datetime
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from backend.app.services.price_collector import PriceCollector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('price_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def verify_collection():
    """Verify that prices were collected successfully"""
    try:
        load_dotenv()
        db_params = {
            'host': os.getenv('DB_HOST'),
            'database': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT')
        }
        
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT 
                i.market_hash_name,
                ph.price,
                ph.source,
                ph.timestamp
            FROM price_history ph
            JOIN items i ON ph.item_id = i.item_id
            WHERE ph.timestamp > NOW() - INTERVAL '1 hour'
            AND ph.source = 'buff'
            ORDER BY ph.timestamp DESC
            LIMIT 5
        """)
        
        recent_prices = cur.fetchall()
        if recent_prices:
            logger.info("Recent price collections:")
            for price in recent_prices:
                logger.info(f"{price['market_hash_name']}: {price['price']} ({price['source']}) at {price['timestamp']}")
        else:
            logger.warning("No recent price collections found!")
            
        return bool(recent_prices)
        
    except Exception as e:
        logger.error(f"Error verifying collection: {e}")
        return False
    finally:
        if conn:
            cur.close()
            conn.close()

async def run_scheduled_collection():
    """Run price collection and verify results"""
    try:
        start_time = time.time()
        logger.info(f"Starting scheduled collection at {datetime.now()}")
        
        collector = PriceCollector()
        await collector.collect_and_store_prices()
        
        if verify_collection():
            logger.info("✅ Price collection completed successfully!")
        else:
            logger.error("Price collection may have failed!")
            
        execution_time = time.time() - start_time
        logger.info(f"Collection completed in {execution_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error in collection: {e}")

def main():
    """Main function to run the collection schedule"""
    logger.info("Starting price collection service")
    
    asyncio.run(run_scheduled_collection())
    
    schedule.every().hour.at(":00").do(lambda: asyncio.run(run_scheduled_collection()))
    
    logger.info("Price collection scheduled for every hour")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()