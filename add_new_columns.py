"""
Script to add new columns to users table and create new feature tables
Run this if migrations are having issues
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url)

with engine.connect() as conn:
    # Start transaction
    trans = conn.begin()
    
    try:
        # Add new columns to users table (if they don't exist)
        print("Adding new columns to users table...")
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS business_stage VARCHAR,
            ADD COLUMN IF NOT EXISTS sector VARCHAR,
            ADD COLUMN IF NOT EXISTS bio TEXT,
            ADD COLUMN IF NOT EXISTS profile_image VARCHAR,
            ADD COLUMN IF NOT EXISTS language_preference VARCHAR DEFAULT 'en' NOT NULL;
        """))
        
        print("✓ Users table updated")
        
        # Note: The new tables will be created by SQLAlchemy's create_all() 
        # when the server starts, or you can run the migration manually later
        
        trans.commit()
        print("✓ All changes committed successfully!")
        
    except Exception as e:
        trans.rollback()
        print(f"✗ Error: {e}")
        raise

print("\nDone! You can now restart your backend server.")
print("The new tables will be created automatically by SQLAlchemy.")


