import os
import mimetypes
import requests
import google.generativeai as genai
from dotenv import load_dotenv

# Load Gemini API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def fetch_image_bytes(path):
    """Fetch image bytes and MIME type whether path is URL or local."""
    if path.startswith("http"):
        response = requests.get(path)
        response.raise_for_status()
        mime_type = mimetypes.guess_type(path)[0] or "image/jpeg"
        return response.content, mime_type
    else:
        with open(path, "rb") as f:
            data = f.read()
        mime_type = mimetypes.guess_type(path)[0] or "image/jpeg"
        return data, mime_type

def analyze_growth(initial_image_path, latest_image_path):
    try:
        # Fetch both image blobs
        initial_bytes, mime_type_1 = fetch_image_bytes(initial_image_path)
        latest_bytes, mime_type_2 = fetch_image_bytes(latest_image_path)

        initial_blob = {
            "mime_type": mime_type_1,
            "data": initial_bytes
        }

        latest_blob = {
            "mime_type": mime_type_2,
            "data": latest_bytes
        }

        # Prompt for analysis
        prompt = (
            "You are an expert botanist monitoring plant growth over time. Compare the plant in the first image (initial stage) "
            "with the second image (after about 30 days). Analyze visible signs of growth including height, number and size of leaves, "
            "leaf color, stem strength, and overall health.\n\n"
            "Also, identify the plant species if possible. Track growth progress and estimate the improvement percentage if visually evident.\n\n"
            "List what the plant may need for optimal growth — water, nutrients, light, space, soil quality, or pest management.\n\n"
            "Provide a short summary of the plant's development over time and then give 3–5 specific recommendations for improving its growth over the next 3 months."
        )

        # Send to Gemini
        response = model.generate_content([
            prompt,
            {"text": "Initial image of the plant:"},
            initial_blob,
            {"text": "Latest image of the plant (after growth):"},
            latest_blob
        ])

        return response.text

    except Exception as e:
        return f"Error analyzing images: {e}"
