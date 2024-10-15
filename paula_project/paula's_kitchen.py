import requests
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, Listbox, Scrollbar, END

API_URL = "https://api.spoonacular.com/recipes/findByIngredients"
API_KEY = '922d4c3e263640b89cb90fe65b826b9c'

def main():
    root = tk.Tk()
    root.title("Recipe Finder")

    # Labels and Input Field
    tk.Label(root, text="Enter ingredients (separated by commas):").pack(pady=10)
    ingredients_entry = tk.Entry(root, width=50)
    ingredients_entry.pack(pady=10)

    # Search Button
    tk.Button(root, text="Find Recipes", command=lambda: find_recipes_gui(ingredients_entry, root)).pack(pady=10)

    root.mainloop()

def find_recipes_gui(ingredients_entry, root):
    ingredients = ingredients_entry.get().strip()
    if not ingredients:
        messagebox.showwarning("Input Error", "No ingredients provided.")
        return

    ingredients = [ingredient.strip().lower() for ingredient in ingredients.split(',')]
    recipes = find_recipes(ingredients)

    if recipes:
        # Create a new window to display the recipes
        recipe_window = tk.Toplevel(root)
        recipe_window.title("Recipes")

        tk.Label(recipe_window, text="Recipes you can make with the available ingredients:").pack(pady=10)

        listbox = Listbox(recipe_window, width=50, height=10)
        listbox.pack(pady=10)

        scrollbar = Scrollbar(recipe_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)

        for recipe in recipes:
            listbox.insert(END, f"{recipe['title']} (ID: {recipe['id']})")

        def on_select(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                recipe_id = recipes[index]['id']
                recipe_details = get_recipe_details(recipe_id)
                if recipe_details:
                    display_recipe_details_gui(recipe_details)

        listbox.bind('<<ListboxSelect>>', on_select)

    else:
        messagebox.showinfo("No Results", "No recipes found with the available ingredients.")

def display_recipe_details_gui(recipe_details):
    details_window = tk.Toplevel()
    details_window.title("Recipe Details")

    tk.Label(details_window, text=f"Details for {recipe_details['title']}:", font=('Arial', 14, 'bold')).pack(pady=10)
    tk.Label(details_window, text=f"Ready in {recipe_details['readyInMinutes']} minutes.").pack(pady=5)
    tk.Label(details_window, text=f"Servings: {recipe_details['servings']}").pack(pady=5)

    tk.Label(details_window, text="Ingredients:").pack(pady=5)
    for ingredient in recipe_details['extendedIngredients']:
        tk.Label(details_window, text=f"- {ingredient['original']}").pack(anchor="w")

    tk.Label(details_window, text="\nInstructions:").pack(pady=5)
    tk.Label(details_window, text=recipe_details['instructions'] if recipe_details['instructions'] else "No instructions provided.", wraplength=400).pack(pady=5)

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
        data = response.json()
        if isinstance(data, list):
            return data
        else:
            messagebox.showerror("API Error", "Unexpected data format received from API.")
            return []
    else:
        messagebox.showerror("API Error", f"Error fetching recipes from API. Status code: {response.status_code}")
        return []

def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    requirements = {'apiKey': API_KEY}
    response = requests.get(url, params=requirements)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("API Error", f"Error fetching recipe details. Status code: {response.status_code}")
        return {}

if __name__ == "__main__":
    main()
