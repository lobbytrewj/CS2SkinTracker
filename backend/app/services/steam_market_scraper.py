import requests
import json
import time
from typing import Dict, List, Optional


class SteamMarketPrices:
    def __init__(self, rate_limit_delay: float = 1.0, country: str = "US", currency: int = 1):
        self.price_url = "https://steamcommunity.com/market/priceoverview/"
        self.search_url = "https://steamcommunity.com/market/search/render/"
        self.rate_limit_delay = rate_limit_delay
        self.country = country
        self.currency = currency
        self.last_request_time = 0

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://steamcommunity.com/market/",
            "X-Requested-With": "XMLHttpRequest",
        })

    def _wait_for_rate_limit(self):
        if self.rate_limit_delay > 0:
            time_since_last = time.time() - self.last_request_time
            if time_since_last < self.rate_limit_delay:
                wait_time = self.rate_limit_delay - time_since_last
                print(f"Rate limiting: waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
        self.last_request_time = time.time()

    def get_item_price(self, market_hash_name: str, appid: int = 730) -> Optional[Dict]:
        """
        Get current price for an item using Steam's priceoverview endpoint

        Args:
            market_hash_name: Item name (e.g., "AK-47 | Redline (Field-Tested)")
            appid: Steam App ID (730 for CS2/CSGO, 440 for TF2, etc.)

        Returns:
            Dict with price data or None if failed
        """
        self._wait_for_rate_limit()

        params = {
            'country': self.country,
            'currency': self.currency,
            'appid': appid,
            'market_hash_name': market_hash_name
        }

        try:
            print(f"Fetching price for: {market_hash_name}")
            response = self.session.get(self.price_url, params = params)

            print(f"Status: {response.status_code}")
            print(f"URL: {response.url}")

            if response.status_code == 200:
                data = response.json()
                print(f"Response: {json.dumps(data, indent = 2)}")

                if data.get('success'):
                    return {
                        'item_name': market_hash_name,
                        'success': True,
                        'lowest_price': data.get('lowest_price'),
                        'volume': data.get('volume'),
                        'median_price': data.get('median_price'),
                        'raw_data': data
                    }
                else:
                    print(f"Steam returned success=false: {data}")
            else:
                print(f"HTTP Error {response.status_code}: {response.text[:500]}")

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print(f"Raw response: {response.text[:500]}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return None

    def get_multiple_prices(self, item_names: List[str], appid: int = 730) -> Dict[
        str, Optional[Dict]]:
        """Get prices for multiple items"""
        results = {}
        total = len(item_names)

        for i, item_name in enumerate(item_names, 1):
            print(f"\n--- Processing {i}/{total}: {item_name} ---")
            results[item_name] = self.get_item_price(item_name, appid)

        return results

    def test_different_formats(self):
        """Test different item name formats to see what works"""

        test_items = [
            ("AK-47 | Redline (Field-Tested)", 730),
            ("AK-47 | Redline (Minimal Wear)", 730),
            ("Operation Bravo Case", 730),
            ("Prisma Case", 730),
            ("StatTrak™ AK-47 | Redline (Field-Tested)", 730),
        ]

        print("=== Testing Different Item Name Formats ===")

        for item_name, appid in test_items:
            print(f"\n{'=' * 60}")
            print(f"Testing: {item_name} (AppID: {appid})")
            print('=' * 60)

            result = self.get_item_price(item_name, appid)

            if result and result.get('success'):
                print(f"✓ SUCCESS!")
                print(f"  Lowest Price: {result.get('lowest_price', 'N/A')}")
                print(f"  Volume: {result.get('volume', 'N/A')}")
                print(f"  Median Price: {result.get('median_price', 'N/A')}")
            else:
                print("✗ FAILED")


def test_manual_urls():
    """Test by manually constructing known working URLs"""

    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://steamcommunity.com/market/",
    })

    test_urls = [
        "https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=AK-47%20%7C%20Redline%20%28Field-Tested%29",
        "https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=Operation%20Bravo%20Case",
        "https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name=Mann%20Co.%20Supply%20Crate%20Key"
    ]

    print("\n" + "=" * 80)
    print("=== Testing Manual URLs ===")

    for url in test_urls:
        print(f"\nTesting URL: {url}")
        try:
            response = session.get(url)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Success: {data.get('success', False)}")
                    if data.get('success'):
                        print(f"Lowest: {data.get('lowest_price', 'N/A')}")
                        print(f"Volume: {data.get('volume', 'N/A')}")
                    else:
                        print(f"Error data: {data}")
                except:
                    print(f"Raw response: {response.text[:200]}")
            else:
                print(f"Error: {response.text[:200]}")

        except Exception as e:
            print(f"Failed: {e}")


if __name__ == "__main__":
    print("=== Steam Market Price Overview Test ===")

    scraper = SteamMarketPrices(
        rate_limit_delay = 1.5,
        country = "US",
        currency = 1
    )

    scraper.test_different_formats()

    test_manual_urls()