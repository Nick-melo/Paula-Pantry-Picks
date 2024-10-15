import streamlit as st
import requests
import os
from bs4 import BeautifulSoup
import html


API_URL = "https://api.spoonacular.com/recipes/findByIngredients"
API_KEY = "922d4c3e263640b89cb90fe65b826b9c"

def main():
    st.title("Paula's Pantry Picks")

    # Inicializar o estado
    if "recipes" not in st.session_state:
        st.session_state.recipes = []
    if "selected_recipe_id" not in st.session_state:
        st.session_state.selected_recipe_id = None
    if "selected_recipe_details" not in st.session_state:
        st.session_state.selected_recipe_details = {}

    ingredients = st.text_input("Enter ingredients (separated by commas):")

    if st.button("Find Recipes"):
        if ingredients:
            ingredients_list = [ingredient.strip().lower() for ingredient in ingredients.split(',')]
            st.session_state.recipes = find_recipes(ingredients_list)
            st.session_state.selected_recipe_id = None  # Resetar a receita selecionada
            st.session_state.selected_recipe_details = {}  # Resetar detalhes da receita

    # Mostrar a lista de receitas se houver alguma
    if st.session_state.recipes:
        st.subheader("Recipes you can make with the available ingredients:")
        recipe_options = [f"{recipe['title']} (ID: {recipe['id']})" for recipe in st.session_state.recipes]
        selected_option = st.selectbox("Select a recipe to view details:", recipe_options, key="recipe_selector")

        if selected_option:
            recipe_id = int(selected_option.split("ID: ")[1].strip(')'))
            if recipe_id != st.session_state.selected_recipe_id:
                st.session_state.selected_recipe_id = recipe_id
                st.session_state.selected_recipe_details = get_recipe_details(recipe_id)

    # Exibir detalhes da receita se uma for selecionada
    if st.session_state.selected_recipe_id and st.session_state.selected_recipe_details:
        recipe_details = st.session_state.selected_recipe_details
        display_recipe_details(recipe_details)
    else:
        st.write("Select a recipe to view details.")

def display_recipe_details(recipe_details):
    st.subheader(f"Details for {recipe_details['title']}:")
    # Exibir imagem da receita, se disponível
    st.image(recipe_details.get('image', ''), caption=recipe_details['title'], use_column_width=True)
    st.write(f"Ready in {recipe_details['readyInMinutes']} minutes.")
    st.write(f"Servings: {recipe_details['servings']}")

    st.write("Ingredients:")
    for ingredient in recipe_details['extendedIngredients']:
        st.write(f"- {ingredient['original']}")

    st.write("\nInstructions:")
    instructions = recipe_details.get('instructions', '')
    if instructions:
        formatted_instructions = remove_html_tags(instructions)
        st.write(formatted_instructions)
    else:
        st.write("No instructions provided.")

    

def remove_html_tags(text):
    # Remove HTML tags from the provided text.
    return html.unescape(BeautifulSoup(text, "html.parser").text)

def find_recipes(ingredients):
    params = {
        'ingredients': ','.join(ingredients),
        'number': 5,
        'ranking': 1,
        'ignorePantry': True,
        'apiKey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching recipes from API. Status code: {response.status_code}")
        return []

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {'apiKey': API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching recipe details. Status code: {response.status_code}")
        return {}

if __name__ == "__main__":
    main()
