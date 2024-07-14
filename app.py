import streamlit as st
import spoonacular as sp
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Meal Finder", page_icon="🍴")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://4kwallpapers.com/images/wallpapers/ios-13-stock-ipados-dark-green-black-background-amoled-ipad-2560x1440-794.jpg");
        background-attachment: fixed;
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Meal Finder")

def get_recipes(ingredients, diet):
    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        st.error("API key not found. Please set the SPOONACULAR_API_KEY environment variable.")
        return {}

    api = sp.API(api_key)
    try:
        response = api.search_recipes_complex(query=ingredients, diet=diet, number=10, addRecipeInformation=True)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            st.error(f"Error: {response.status_code} - {data.get('message', 'Something went wrong.')}")
            return {}
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return {}

def main():
    ingredients = st.text_input("Enter comma-separated ingredients (e.g. chicken, rice, broccoli): ")
    diet = st.selectbox("Dietary restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Ketogenic"])

    if st.button("Find Recipes"):
        if ingredients:
            with st.spinner("Fetching recipes..."):
                response = get_recipes(ingredients, diet)
                results = response.get("results", [])
                if not results:
                    st.write("No recipes found.")
                else:
                    df = pd.DataFrame(results)
                    df = df[["title", "readyInMinutes", "servings", "sourceUrl"]]
                    st.write(df)
        else:
            st.write("Enter at least one ingredient")

if __name__ == "__main__":
    main()
