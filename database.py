import sqlite3

# Path to the database file
DB_PATH = "database.db"

def init_db():
    """Initializes the database and creates the 'plants' table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            plant_id TEXT,
            date TEXT,
            image_path TEXT,              -- initial plantation image path
            growth_image_path TEXT,       -- latest growth image path
            feedback TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_plant(user_id, plant_id, date, image_path):
    """Inserts a new plant record."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO plants (user_id, plant_id, date, image_path)
        VALUES (?, ?, ?, ?)
    """, (user_id, plant_id, date, image_path))
    conn.commit()
    conn.close()

def get_all_plants():
    """Returns all plant records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, plant_id, date, image_path, growth_image_path, feedback
        FROM plants
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def get_plant(user_id, plant_id):
    """Returns a specific plant record by user_id and plant_id."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM plants
        WHERE user_id = ? AND plant_id = ?
    """, (user_id, plant_id))
    data = cursor.fetchone()
    conn.close()
    return data

def update_growth_image(user_id, plant_id, growth_image_path, feedback):
    """Updates the growth image and feedback for a plant."""
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
    """Updates the initial plantation image path for a plant."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE plants
        SET image_path = ?
        WHERE user_id = ? AND plant_id = ?
    """, (initial_image_path, user_id, plant_id))
    conn.commit()
    conn.close()

