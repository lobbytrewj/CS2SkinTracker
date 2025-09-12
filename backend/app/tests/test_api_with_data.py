import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_add_items():
    """Test adding items to the database"""
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
    
    added_items = []
    for item in test_items:
        try:
            print(f"\nAdding item: {item['market_hash_name']}")
            response = requests.post(f"{BASE_URL}/items", json=item)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                added_item = response.json()
                added_items.append(added_item)
                print("Added successfully:", json.dumps(added_item, indent=2))
            else:
                print("Error:", response.text)
                
        except Exception as e:
            print(f"Error: {e}")
    
    return added_items

def test_get_items():
    """Test getting all items"""
    print("\n=== Testing Get Items ===")
    try:
        response = requests.get(f"{BASE_URL}/items")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            items = response.json()
            print(f"Total items: {len(items)}")
            print("First item:", json.dumps(items[0], indent=2) if items else "No items")
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=== Running API Tests ===")
    
    added_items = test_add_items()
    
    test_get_items()