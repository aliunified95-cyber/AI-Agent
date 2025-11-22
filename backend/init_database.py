"""
Initialize database tables
Run this script to create all tables in the database
"""
from app.database import engine, Base
from app.models.db_models import Order, AgentSession, ConversationMessage
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    """Create all tables"""
    from app.database import engine, USE_DATABASE
    
    if not USE_DATABASE:
        print("ERROR: DATABASE_URL not configured in .env file")
        print("\nTo set up database:")
        print("1. Get your connection string from Supabase dashboard")
        print("2. Run: python reset_database_url.py")
        print("3. Then run this script again")
        exit(1)
    
    if not engine:
        print("ERROR: Could not create database engine")
        print("Please check your DATABASE_URL in .env file")
        exit(1)
    
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("SUCCESS: Database tables created successfully!")
    except Exception as e:
        print(f"ERROR: Could not create database tables: {e}")
        print("\nPossible issues:")
        print("1. Check your internet connection")
        print("2. Verify the Supabase hostname is correct")
        print("3. Make sure your Supabase project is active")
        print("4. Check if your IP is whitelisted in Supabase")
        exit(1)

if __name__ == "__main__":
    init_db()

