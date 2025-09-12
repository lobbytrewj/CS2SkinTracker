import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.buff_parser import BuffParser
from app.models.database import init_database

def test_database():
    print("1. Testing Database Connection...")
    parser = BuffParser()
    conn = parser.connect_db()
    if conn:
        print("✅ Database connection successful!")
        conn.close()
    else:
        print("❌ Database connection failed!")

    print("\n2. Initializing Database Schema...")
    try:
        init_database()
        print("✅ Database schema initialized!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")

if __name__ == "__main__":
    test_database()