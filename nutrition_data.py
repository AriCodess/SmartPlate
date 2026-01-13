import pandas as pd
import os

# Robust file path handling
# This finds the 'data' folder relative to THIS script file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'Indian_Food_Nutrition_Processed.csv')

# Load the database once when the module is imported
try:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        # Clean numeric columns (convert text errors to 0)
        cols_to_clean = ['Calories (kcal)', 'Protein (g)', 'Carbohydrates (g)', 'Fats (g)']
        for col in cols_to_clean:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        print("✅ Nutrition Database Loaded Successfully!")
    else:
        df = None
        print(f"⚠️ Error: CSV file not found at {CSV_PATH}")
except Exception as e:
    df = None
    print(f"⚠️ Error reading CSV: {e}")

def get_nutrition_info(yolo_class_name):
    """
    Input: 'pizza' (from YOLO)
    Output: Dictionary with data for 'Cheese pizza' (from CSV)
    """
    if df is None:
        return None

    # Case-insensitive search: Find any dish name containing the YOLO tag
    # e.g., 'rice' matches 'Lemon rice', 'Curd rice', etc.
    matches = df[df['Dish Name'].str.contains(yolo_class_name, case=False, na=False)]
    
    if not matches.empty:
        # Strategy: Return the FIRST match found.
        # (You can improve this later to return the most common variant)
        row = matches.iloc[0]
        
        return {
            "name": row['Dish Name'],  # Real name from CSV
            "cal": int(row['Calories (kcal)']),
            "prot": float(row['Protein (g)']),
            "carb": float(row['Carbohydrates (g)']),
            "fat": float(row['Fats (g)'])
        }
    
    return None