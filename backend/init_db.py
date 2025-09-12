from app.models.database import Base, init_database

def main():
    """Initialize database with proper schema"""
    print("Initializing database...")
    try:
        engine = init_database()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    main()