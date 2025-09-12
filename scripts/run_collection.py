import asyncio
import schedule
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.app.services.price_collector import PriceCollector

async def run_collection():
    collector = PriceCollector()
    await collector.collect_and_store_prices()

def schedule_collection():
    asyncio.run(run_collection())

if __name__ == "__main__":
    # Run collection every hour
    schedule.every().hour.do(schedule_collection)
    
    while True:
        schedule.run_pending()
        time.sleep(60)