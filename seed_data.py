from database import insert_plant
from datetime import datetime

# Sample plant records with Google Drive direct URLs for initial images
plants = [
    ("user_001", "plant_001", "https://drive.google.com/uc?export=view&id=1z7nou0SIt7hko7PbRRkHIT4eryKXRu40"),
    ("user_002", "plant_002", "https://drive.google.com/uc?export=view&id=199HlMC8HjGnjYcNBPFYokY_pR71tWOGA"),
    ("user_003", "plant_003", "https://drive.google.com/uc?export=view&id=1vnCBI3rsXZSr6Fq7i3Uu8lBxyGDxZYbL"),
]

for user_id, plant_id, image_path in plants:
    insert_plant(user_id, plant_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), image_path)

print("✅ Sample plant records inserted successfully.")


