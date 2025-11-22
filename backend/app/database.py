from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Make database optional - app can run without it
USE_DATABASE = DATABASE_URL is not None and DATABASE_URL != ""

if USE_DATABASE:
    try:
        # Create engine (don't test connection yet)
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Verify connections before using
            pool_size=10,
            max_overflow=20,
            connect_args={"connect_timeout": 5}  # 5 second timeout
        )
        # Try a simple connection test
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✓ Database connection configured and tested")
        except Exception as conn_error:
            print(f"⚠ Warning: Database connection test failed: {conn_error}")
            print("⚠ Application will run without database persistence")
            print("⚠ You can fix the connection later and restart the app")
            USE_DATABASE = False
            engine = None
    except Exception as e:
        print(f"⚠ Warning: Could not configure database connection: {e}")
        print("⚠ Application will run without database persistence")
        USE_DATABASE = False
        engine = None
else:
    print("ℹ Info: DATABASE_URL not set. Application will run without database persistence.")
    engine = None

# Create session factory
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    if not SessionLocal:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

