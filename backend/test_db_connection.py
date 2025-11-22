"""
Test database connection
"""
import os
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in .env file")
    exit(1)

print("Testing database connection...")
print(f"URL (masked): {DATABASE_URL.split('@')[0]}@***")

try:
    # Parse the URL
    parsed = urlparse(DATABASE_URL)
    
    print(f"\nParsed connection details:")
    print(f"  Host: {parsed.hostname}")
    print(f"  Port: {parsed.port}")
    print(f"  Database: {parsed.path[1:] if parsed.path else 'postgres'}")
    print(f"  User: {parsed.username}")
    
    # Try to connect
    print(f"\nAttempting to connect to {parsed.hostname}...")
    
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:] if parsed.path else 'postgres',
        user=parsed.username,
        password=parsed.password
    )
    
    print("SUCCESS: Connected to database!")
    
    # Test query
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    cur.close()
    conn.close()
    
    print("\nDatabase connection test PASSED!")
    
except psycopg2.OperationalError as e:
    print(f"\nERROR: Could not connect to database")
    print(f"Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Check your internet connection")
    print("2. Verify the Supabase database is running")
    print("3. Check if your IP is whitelisted in Supabase (if required)")
    print("4. Verify the hostname is correct")
    exit(1)
except Exception as e:
    print(f"\nERROR: {str(e)}")
    exit(1)

