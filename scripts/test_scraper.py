import os
from backend.app.services.steamwebapi_scraper import SteamWebAPIScraper
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("STEAMWEBAPI_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")

if not api_key:
    print("ERROR: No API key found. Make sure STEAMWEBAPI_KEY is in your .env file")
    exit(1)

scraper = SteamWebAPIScraper(api_key=api_key)

# Test the old method calls with CORRECT market hash names
print("=== Testing with Original Method Names ===")

# Use the correct full market hash name instead of just "Redline"
item = scraper.get_item("AK-47 | Redline (Field-Tested)")
print("AK-47 Redline:", item)

# Test other conditions
item_mw = scraper.get_item("AK-47 | Redline (Minimal Wear)")
print("AK-47 Redline MW:", item_mw)

# Test popular items (will return empty as expected)
popular = scraper.get_popular_items(limit=5)
print("Popular items:", popular)

# Test inventory history (will return empty as expected)
history = scraper.get_inventory_history("76561198000000000")
print("Inventory history:", history)

print("\n=== Testing New Method Names ===")

# Test with proper CS2 item names (market hash names)
item_history = scraper.get_item_history("AK-47 | Redline (Field-Tested)")
print("AK-47 Redline History:", item_history)

# Test different conditions
item_bs = scraper.get_item_history("AK-47 | Redline (Battle-Scarred)")
print("AK-47 Redline BS:", item_bs)

# Test connection
print("\n=== Testing Connection ===")
connection_test = scraper.test_connection()
print("Connection Test:", connection_test)