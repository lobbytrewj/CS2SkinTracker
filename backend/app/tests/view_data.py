import requests
import json
from tabulate import tabulate

def view_database_content():
    """View all items in the database in a formatted table"""
    try:
        response = requests.get("http://localhost:8000/api/items")
        if response.status_code == 200:
            items = response.json()
            
            if not items:
                print("No items found in database!")
                return
                
            table_data = []
            for item in items:
                table_data.append([
                    item['market_hash_name'],
                    item['item_type'],
                    item['weapon_type'],
                    item['skin_name'],
                    item['wear'],
                    item.get('buff_price', 'N/A'),
                    item.get('created_at', 'N/A')
                ])
            
            headers = ['Name', 'Type', 'Weapon', 'Skin', 'Wear', 'Buff Price', 'Created At']
            print("\n=== Current Database Contents ===")
            print(f"Total Items: {len(items)}")
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
            
        else:
            print(f"Error getting items: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error viewing database: {e}")

if __name__ == "__main__":
    view_database_content()