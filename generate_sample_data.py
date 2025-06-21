import os
import sqlite3
from datetime import datetime

# Paths
UPLOAD_DIR = r"C:\Users\Yash Bhosale\OneDrive\Desktop\Tree Plant growth tracking\seed_data"

DB_FILE = "database.db"

# Sample records
sample_data = [
    {"user_id": "user_001", "plant_id": "plant_001", "image": "plant1.jpeg"},
    {"user_id": "user_002", "plant_id": "plant_002", "image": "plant2.jpeg"},
    {"user_id": "user_003", "plant_id": "plant_003", "image": "plant3.jpeg"},
]

# Create DB connection
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ✅ Step 1: Create table with all required fields
cursor.execute("""
    CREATE TABLE IF NOT EXISTS plants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        plant_id TEXT,
        image_path TEXT,
        growth_image_path TEXT,
        feedback TEXT,
        date TEXT
    )
""")

# ✅ Step 2: Insert dummy records
for record in sample_data:
    src_path = os.path.join(UPLOAD_DIR, record["image"])
    if not os.path.exists(src_path):
        print(f"❌ Image not found: {record['image']}")
        continue

    cursor.execute("""
        INSERT INTO plants (user_id, plant_id, image_path, growth_image_path, feedback, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        record["user_id"],
        record["plant_id"],
        src_path,
        None,
        None,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

conn.commit()
conn.close()
print("✅ Sample data inserted successfully.")


