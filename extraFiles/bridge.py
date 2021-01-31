from flask import Flask, render_template, request
from Recipe import Recipe 
import requests

# Creating Flask App object
app = Flask(__name__,
           static_url_path='',
           static_folder='html')
           
# Each method in the Flask App is tied to a url, which is written using '@app.route()'
@app.route('/')
def root():
    # Default an HTML page (HOME PAGE)
    return app.send_static_file('index.html')

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/findByIngredients"
headers = {
    'x-rapidapi-key': "f4c99ab3d5msh07bfa430aafa7bep149cddjsn2d17db76303d",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

@app.route("/")
def search_page():
  pass #setup search here.
  
#@app.route("/recipe.html")

@app.route('/search',  methods = ["POST", "GET"])
def s():
  if request.method == 'POST':
    query = request.form['query']
    new_recipe = Recipe(ingredients = query)
    json_data = new_recipe.GetRequest_Ingredients()
    recipe_dict = new_recipe.process_recipe_ID_summary(json_data)
    recipes = new_recipe.return_results(recipe_dict)
    return render_template('search.html', results = recipes) #the recipes we want to display

if __name__== '__main__':
  app.run(host='0.0.0.0', port='8000')
  #app.run(debug=True)