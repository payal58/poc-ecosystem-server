import pandas as pd
from sqlalchemy import create_engine, text

# === 1️⃣ Configure your Neon connection string ===
# Example: postgresql://<user>:<password>@<host>/<dbname>?sslmode=require
DATABASE_URL= 'postgresql://neondb_owner:npg_YRHUiA6WMz0V@ep-wild-moon-a4062tuj-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

# === 2️⃣ Create database connection ===
engine = create_engine(DATABASE_URL)

# === 3️⃣ Create table (if not already created) ===
# create_table_query = """
# CREATE TABLE IF NOT EXISTS organizations (
#     id SERIAL PRIMARY KEY,
#     organization_name TEXT NOT NULL,
#     city VARCHAR(100),
#     address TEXT,
#     latitude DECIMAL(9,6),
#     longitude DECIMAL(9,6),
#     province_state VARCHAR(50),
#     sector_type VARCHAR(200),
#     services_offered TEXT,
#     website TEXT,
#     email_address TEXT,
#     phone_number VARCHAR(50),
#     contact_name TEXT,
#     notes TEXT,
#     created_at TIMESTAMP DEFAULT NOW()
# );
# """
# with engine.begin() as conn:
#     conn.execute(text(create_table_query))

# === 4️⃣ Load and clean CSV ===
df = pd.read_csv("data.csv")

# normalize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# ensure only valid columns go in
expected_cols = [
    "organization_name", "city", "address", "latitude", "longitude",
    "province_state", "sector_type", "services_offered", "website",
    "email_address", "phone_number", "contact_name", "notes"
]
df = df[[c for c in expected_cols if c in df.columns]]

# === 5️⃣ Upload to NeonDB ===
df.to_sql("organizations", engine, if_exists="append", index=False)

print(f"✅ Uploaded {len(df)} records to NeonDB successfully.")
