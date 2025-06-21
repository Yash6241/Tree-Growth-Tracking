import sqlite3

DB_PATH = "database.db"

def init_db():
    """Initialize DB and create plants table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            plant_id TEXT,
            date TEXT,
            image_path TEXT,            -- initial image URL or local path
            growth_image_path TEXT,     -- latest growth image URL or local path
            feedback TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_plant(user_id, plant_id, date, image_path):
    """Insert a new plant record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plants (user_id, plant_id, date, image_path)
        VALUES (?, ?, ?, ?)
    """, (user_id, plant_id, date, image_path))
    conn.commit()
    conn.close()

def get_plant(user_id, plant_id):
    """Get plant record by user and plant ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM plants WHERE user_id = ? AND plant_id = ?
    """, (user_id, plant_id))
    data = cursor.fetchone()
    conn.close()
    return data

def update_growth_image(user_id, plant_id, growth_image_path, feedback):
    """Update growth image path and feedback."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE plants
        SET growth_image_path = ?, feedback = ?
        WHERE user_id = ? AND plant_id = ?
    """, (growth_image_path, feedback, user_id, plant_id))
    conn.commit()
    conn.close()

def update_initial_image(user_id, plant_id, initial_image_path):
    """Update initial image path."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE plants
        SET image_path = ?
        WHERE user_id = ? AND plant_id = ?
    """, (initial_image_path, user_id, plant_id))
    conn.commit()
    conn.close()



