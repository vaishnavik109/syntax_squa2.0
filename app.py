from flask import Flask, render_template, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Spoonacular API details
API_KEY = "b572a27b102f44ad809092b2da246181"
INGREDIENTS_URL = "https://api.spoonacular.com/recipes/findByIngredients"
RECIPE_DETAILS_URL = "https://api.spoonacular.com/recipes/{id}/information"

def get_recipe_details(recipe_id):
    response = requests.get(RECIPE_DETAILS_URL.format(id=recipe_id), params={"apiKey": API_KEY})
    return response.json() if response.status_code == 200 else None

def search_recipes_from_api(ingredients, cuisine):
    query = ",".join(ingredients)

    # Include the selected cuisine in the API request (if provided)
    params = {
        "ingredients": query,
        "number": 5,
        "apiKey": API_KEY
    }
    if cuisine:
        params["cuisine"] = cuisine

    response = requests.get(INGREDIENTS_URL, params=params)

    if response.status_code == 200:
        recipes = response.json()
        detailed_recipes = []

        for recipe in recipes:
            details = get_recipe_details(recipe["id"])
            if details:
                detailed_recipes.append({
                    "name": details["title"],
                    "ingredients": ", ".join([i["name"] for i in details["extendedIngredients"]]),
                    "instructions": details["instructions"] or "No instructions available."
                })

        return detailed_recipes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    ingredients = [ing.strip().lower() for ing in data.get('ingredients', [])]
    cuisine = data.get('cuisine', '').lower()

    # Get recipes from the Spoonacular API with optional cuisine filtering
    recipes = search_recipes_from_api(ingredients, cuisine)

    if recipes:
        return jsonify(recipes)
    else:
        return jsonify({"message": "No matching recipes found."})

if __name__ == "__main__":
    app.run(debug=True)
