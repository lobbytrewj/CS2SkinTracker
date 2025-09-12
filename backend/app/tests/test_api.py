import sys
import os
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("Testing API Endpoints...")
    
    endpoints = {
        "root": "http://localhost:8000/",
        "items": f"{BASE_URL}/items"
    }
    
    for name, url in endpoints.items():
        try:
            response = requests.get(url)
            print(f"\n{name.upper()} Endpoint ({url}):")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"❌ Error testing {name}: {e}")

if __name__ == "__main__":
    test_api()