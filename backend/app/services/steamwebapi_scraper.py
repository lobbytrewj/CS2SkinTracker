import requests
import logging
from typing import Dict, List, Optional


logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class SteamWebAPIScraper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.steamwebapi.com/steam/api"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "CS2-Skin-Tracker/1.0",
            "Accept": "application/json"
        })

    def get_item_history(self, market_hash_name: str, origin: str = "steamwebapi",
                         type_param: str = "sell", interval: int = 30,
                         start_date: Optional[str] = None, end_date: Optional[str] = None) -> \
    Optional[Dict]:
        """
        Get price history for an item using the correct /history endpoint
        """
        endpoint = f"{self.base_url}/history"
        params = {
            "key": self.api_key,
            "market_hash_name": market_hash_name,
            "origin": origin,  # 'steamwebapi' or 'markets' for real market data
            "type": type_param,  # 'sell', 'offer', 'median'
            "interval": interval  # Default: 30
        }

        if start_date:
            params["start_date"] = start_date  # Format: YYYY-MM-DD
        if end_date:
            params["end_date"] = end_date  # Format: YYYY-MM-DD

        try:
            print(f"Making request to: {endpoint}")
            print(f"With params: {params}")

            response = self.session.get(endpoint, params = params)
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text[:500]}...")

            if response.status_code == 200:
                data = response.json()
                return data
            elif response.status_code == 404:
                logger.warning(f"Item not found: {market_hash_name}")
            elif response.status_code == 429:
                logger.error("Rate limit exceeded. Slow down requests or upgrade plan.")
            else:
                logger.error(f"Unexpected status code: {response.status_code}")

        except Exception as e:
            logger.error(f"Error fetching item history {market_hash_name}: {e}")
        return None

    def get_item_real_market_history(self, market_hash_name: str, type_param: str = "sell",
                                     interval: int = 30) -> Optional[Dict]:
        """
        Get real market price history (slower but more detailed)
        """
        return self.get_item_history(
            market_hash_name = market_hash_name,
            origin = "markets",  # Use real market data
            type_param = type_param,
            interval = interval
        )

# Test script
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("STEAMWEBAPI_KEY")
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")

    if not api_key:
        print("ERROR: No API key found. Make sure STEAMWEBAPI_KEY is in your .env file")
        exit(1)

    scraper = SteamWebAPIScraper(api_key = api_key)

    # Test item history with common CS2 items
    print("\n=== Testing Item History ===")

    # Try different item names
    test_items = [
        "AK-47 | Redline (Field-Tested)",
        "AWP | Dragon Lore (Factory New)",
    ]

    for item_name in test_items:
        print(f"\n--- Testing: {item_name} ---")
        history = scraper.get_item_history(item_name)
        if history:
            print(f"Success! Got history data: {type(history)}")
            if isinstance(history, dict):
                print(f"Keys in response: {list(history.keys())}")
        else:
            print("No data returned")