import pandas as pd
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api"

def parse_item_name(market_hash_name: str):
    """Parse item name to get components"""
    parts = market_hash_name.split('|')
    if len(parts) == 2:
        weapon_type = parts[0].strip()
        rest = parts[1].strip()
        
        if '(' in rest:
            skin_name = rest[:rest.rfind('(')].strip()
            wear = rest[rest.rfind('(')+1:rest.rfind(')')].strip()
        else:
            skin_name = rest
            wear = "Not Applicable"
            
        return {
            "market_hash_name": market_hash_name,
            "weapon_type": weapon_type,
            "skin_name": skin_name,
            "wear": wear,
            "item_type": "knife" if "★" in weapon_type else "weapon"
        }
    return None

def test_with_csv_data():
    """Test backend with real CS2 skin data"""
    print("\n=== Testing with CSV Data ===")
    
    csv_path = Path(__file__).parent.parent.parent.parent / "data" / "purchase.csv"
    df = pd.read_csv(csv_path)
    
    successful_items = 0
    failed_items = 0
    
    for _, row in df.iterrows():
        item_data = parse_item_name(row['name'])
        if item_data:
            try:
                print(f"\nAdding item: {item_data['market_hash_name']}")
                response = requests.post(f"{BASE_URL}/items", json=item_data)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    successful_items += 1
                    print("Successfully added!")
                else:
                    failed_items += 1
                    print(f"Failed: {response.text}")
            except Exception as e:
                failed_items += 1
                print(f"Error: {e}")
    
    print(f"\nResults:")
    print(f"Successfully added items: {successful_items}")
    print(f"Failed items: {failed_items}")
    
    print("\n=== Verifying Database Content ===")
    try:
        response = requests.get(f"{BASE_URL}/items")
        if response.status_code == 200:
            items = response.json()
            print(f"Total items in database: {len(items)}")
            print("\nSample items:")
            for item in items[:5]:
                print(json.dumps(item, indent=2))
        else:
            print(f"Failed to verify database content: {response.text}")
    except Exception as e:
        print(f"Error verifying database: {e}")

if __name__ == "__main__":
    print("=== Running Full Backend Test with CSV Data ===")
    test_with_csv_data()