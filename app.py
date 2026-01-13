import streamlit as st
from ultralytics import YOLO
from PIL import Image
import pandas as pd
# Import our custom logic module
from nutrition_data import get_nutrition_info

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="SmartPlate AI",
    page_icon="🍛",
    layout="centered"
)

# --- HEADER ---
st.title("🍛 SmartPlate: Indian Food AI")
st.markdown("Use Computer Vision to detect food and retrieve nutrition info from a **custom Indian dataset**.")
st.divider()

# --- MODEL LOADING ---
@st.cache_resource
def load_model():
    # Downloads 'best.pt' on first run
    return YOLO('best.pt')

try:
    model = load_model()
except Exception as e:
    st.error(f"Failed to load AI Model: {e}")

# --- MAIN INTERFACE ---
uploaded_file = st.file_uploader("📸 Upload a food image (jpg, png)...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 1. Show Original Image
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Meal", use_container_width=True)
    
    if st.button("🔍 Analyze Nutrition"):
        with st.spinner("Identifying food items..."):
            # 2. Run AI Inference
            results = model(image)
            
            # 3. Process Results
            detected_items = []
            total_cal = 0
            
            for result in results:
                for box in result.boxes:
                    # Get class name from YOLO (e.g., 'pizza', 'apple')
                    class_id = int(box.cls[0])
                    yolo_name = model.names[class_id]

                    # --- DEBUGGING STEP 1: Print to Terminal ---
                    # Look at your terminal to see exactly what the model sees!
                    print(f"DEBUG: Model detected class_id={class_id}, name='{yolo_name}'")
                    
                    # --- ROBUST MATCHING STEP 2: Try variations ---
                    # Try original name first
                    info = get_nutrition_info(yolo_name)
                    
                    # If not found, try Title Case (e.g., 'cake' -> 'Cake')
                    if not info:
                        print(f"DEBUG: '{yolo_name}' not found. Trying '{yolo_name.title()}'...")
                        info = get_nutrition_info(yolo_name.title())

                    # If still not found, try Lower Case (e.g., 'Cake' -> 'cake')
                    if not info:
                        print(f"DEBUG: '{yolo_name.title()}' not found. Trying '{yolo_name.lower()}'...")
                        info = get_nutrition_info(yolo_name.lower())
                    
                    if info:
                        detected_items.append({
                            "Detected Object": yolo_name.title(),
                            "Matched Dish (CSV)": info['name'],
                            "Calories": info['cal'],
                            "Protein (g)": info['prot'],
                            "Carbs (g)": info['carb'],
                            "Fats (g)": info['fat']
                        })
                        total_cal += info['cal']
                    else:
                        print(f"DEBUG: Failed to find match for '{yolo_name}' in CSV after all attempts.")
            
            # 4. Display Results
            if detected_items:
                # Success Message
                st.success(f"Found {len(detected_items)} items with nutritional data!")
                
                # Big Metrics Display
                col1, col2 = st.columns(2)
                col1.metric("Total Calories", f"{total_cal} kcal")
                col2.metric("Items Identified", len(detected_items))
                
                # Data Table
                st.subheader("📝 Detailed Breakdown")
                df_results = pd.DataFrame(detected_items)
                st.table(df_results)
                
                # Annotated Image (Optional visual)
                res_plotted = results[0].plot()
                st.image(res_plotted[:, :, ::-1], caption="AI Vision Output", use_container_width=True)
                
            else:
                st.warning("⚠️ Objects detected, but no matching Indian dish found in the CSV.")
                st.info("Check your terminal for the 'DEBUG' messages to see exactly why the match failed!")