import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_system():
    """Test the entire backend system"""
    print("\n=== Testing Full Backend System ===")
    
    print("\n=== Testing Item Addition ===")
    test_items = [
        {
            "market_hash_name": "AK-47 | Redline (Field-Tested)",
            "item_type": "rifle",
            "weapon_type": "AK-47",
            "skin_name": "Redline",
            "wear": "Field-Tested"
        },
        {
            "market_hash_name": "AWP | Asiimov (Field-Tested)",
            "item_type": "sniper",
            "weapon_type": "AWP",
            "skin_name": "Asiimov",
            "wear": "Field-Tested"
        }
    ]

    for item in test_items:
        print(f"\nAdding item: {item['market_hash_name']}")
        response = requests.post(f"{BASE_URL}/items", json=item)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

    print("\n=== Verifying Added Items ===")
    response = requests.get(f"{BASE_URL}/items")
    print(f"Status: {response.status_code}")
    items = response.json()
    print(f"Total items in database: {len(items)}")
    print("Items:")
    print(json.dumps(items, indent=2))

if __name__ == "__main__":
    print("=== Running Full API Tests with Data ===")
    test_system()