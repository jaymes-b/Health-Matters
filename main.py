from flask import Flask, render_template, request
from Recipe import Recipe 
#import bridge
import requests
#Tyler API Key. 85% done #04971e3383msh7cce6ecca39b48fp1b23bbjsnd0e81a4583f9
#james' api key 6363361fe0mshb866e02351c6597p1a39f3jsna55a35395da5
# Creating Flask App object
#also tyler 56e969b87cmshb98d477764b7a01p1fdb05jsn81b29370139c
#tyler again 0bbf4a8464msh9d91d44fbbcd793p10cbe4jsn70bd46674321
#tyler for the 4th time 7ca717f64cmsh6b43430895c9462p10cee1jsnd71915833a12
#tyler 5th f4c99ab3d5msh07bfa430aafa7bep149cddjsn2d17db76303d
app = Flask(__name__,
           static_url_path='',
           static_folder='templates')
           
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

# @app.route('/')
# def search_page():
#   pass #setup search here.
  

@app.route('/search')
def s():
  #if request.method == 'GET':
  query = request.args.get('query')
  # query.split()
  # query = ','.join(query)
  query = str(query)
  new_recipe = Recipe(ingredients = query)
  #print(new_recipe)
  json_data = new_recipe.GetRequest_Ingredients()
  #print(json_data)
  recipe_dict = new_recipe.process_recipe_ID_summary(json_data)
  recipes = new_recipe.return_results(recipe_dict)
  instructions = new_recipe.display_instructions(recipe_dict)
  ingredients = new_recipe.display_ingredients(recipe_dict)
  print(instructions)
  return render_template('search.html', results = recipes, json_file = json_data, instructions = instructions, ingredients = ingredients) #the recipes we want to display

@app.route('/recipe')
def r():
  return ""


if __name__== '__main__':
  app.run(host='0.0.0.0', port='8000')
  #app.run(debug=True)


# if __name__ == "__main__":
#  app.run(host='0.0.0.0', 
  #  new_recipe = Recipe(ingredients= "apple,sugar,flour",foodname = "cheese burger")
  #  print(new_recipe.GetRequest_Ingredients())
#   # print(new_recipe.GetRequest_Ingredients())

#  
# 
# GetRequest_i_Text
  # ingredients = input("Please enter ingredients: ")
  # ingredients = re.split(' |, |',ingredients) #parse with regex for both , and space.
  # ingredientStr = ','.join(ingredients)
  # # new_recipe = Recipe(ingredients)
  # # ingredients takes in a string like "apple,orange,etc". not a split list.
  # api.search_recipes_by_ingredients(ingredients, 5, True, 1, True)