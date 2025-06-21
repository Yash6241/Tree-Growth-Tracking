import os
import streamlit as st
from database import get_plant, update_growth_image, update_initial_image
from gemini_utils import analyze_growth

def is_url(path):
    return isinstance(path, str) and path.startswith("http")

UPLOAD_FOLDER = "data/uploaded"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

st.set_page_config(page_title="🌱 Plant Growth Tracker", layout="centered")
st.title("📸 Plant Growth Analysis App")

user_id = st.text_input("Enter your User ID:")
plant_id = st.text_input("Enter your Plant ID:")

if user_id and plant_id:
    plant_data = get_plant(user_id, plant_id)

    if plant_data:
        st.success("✅ Plant Found")

        initial_image_path = plant_data[4]  # image_path column index (0-based)

        if initial_image_path:
            st.markdown("### 🌱 Initial Plantation Photo")
            if is_url(initial_image_path):
                st.image(initial_image_path, caption="Initial Photo", use_container_width=True)
            elif os.path.exists(initial_image_path):
                st.image(initial_image_path, caption="Initial Photo", use_container_width=True)
            else:
                st.warning("⚠️ Initial image not found on the server.")
        else:
            st.warning("⚠️ Initial image not found on the server.")

        # Upload initial image if missing or file missing locally
        if not initial_image_path or (not is_url(initial_image_path) and not os.path.exists(initial_image_path)):
            st.markdown("### Please upload the Initial Plantation Photo:")
            initial_upload = st.file_uploader("Upload Initial Plantation Image", type=["jpg", "jpeg", "png", "webp"], key="initial")

            if initial_upload:
                ext = initial_upload.name.split(".")[-1]
                new_initial_path = os.path.join(UPLOAD_FOLDER, f"{plant_id}_initial.{ext}")

                with open(new_initial_path, "wb") as f:
                    f.write(initial_upload.read())

                st.success("✅ Initial plantation image uploaded successfully!")
                st.image(new_initial_path, caption="Uploaded Initial Photo", use_container_width=True)

                update_initial_image(user_id, plant_id, new_initial_path)
                initial_image_path = new_initial_path

        # Upload new growth image
        st.markdown("### 📤 Upload New Plant Image (After Growth)")
        uploaded_file = st.file_uploader("Choose a recent plant photo...", type=["jpg", "jpeg", "png", "webp"], key="latest")

        if uploaded_file and initial_image_path and (is_url(initial_image_path) or os.path.exists(initial_image_path)):
            ext = uploaded_file.name.split(".")[-1]
            new_img_path = os.path.join(UPLOAD_FOLDER, f"{plant_id}_latest.{ext}")

            with open(new_img_path, "wb") as f:
                f.write(uploaded_file.read())

            st.image(new_img_path, caption="Latest Uploaded", use_container_width=True)

            st.markdown("🔍 **Analyzing growth... Please wait...**")
            feedback = analyze_growth(initial_image_path, new_img_path)

            update_growth_image(user_id, plant_id, new_img_path, feedback)

            st.success("✅ Growth analyzed using Gemini AI")
            st.markdown("### 📋 Gemini Feedback:")
            st.info(feedback)

    else:
        st.error("❌ Plant not found for this User ID and Plant ID. Please check your input.")







