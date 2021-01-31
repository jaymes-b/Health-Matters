import spoonacular as sp
import requests
import json
#fe3c1ea44a3f49f2ab8015238b8605a4
#265470c9b6f04a0d9535d385763d7f19
api = sp.API("265470c9b6f04a0d9535d385763d7f19")
#Almost used f4a8409201dd4d3ca6d687796881bfe8

# url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
# headers = {
#     'x-rapidapi-key': "04971e3383msh7cce6ecca39b48fp1b23bbjsnd0e81a4583f9",
#     'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
#     }

# response = requests.request("GET", url, headers=headers, params=querystring)


class Recipe:
  def __init__(self, ingredients = "", foodname = "", recipe_amount = 1):
    # Know we would call it multiple times, so we make a class attribute (because we'd pass it in response = '')
    self.ingredients = dict()
    self.ingredients["ingredients"] = ingredients #ingre should be a string. Example "apples,flour,sugar"
    self.ingredients["ignorePantry"] = "false" #this makes it so that the api call does NOT ignore flour/salt/water
    self.ingredients["number"] = recipe_amount #amount of recips to output is defauled to 2
    self.food_name = foodname # can be anything, example "cheeseburger with mushrooms"


  def GetRequest_Ingredients(self): #takes ingredients as input and  returns a potential recipe
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
    headers = {
        'x-rapidapi-key': "f4c99ab3d5msh07bfa430aafa7bep149cddjsn2d17db76303d",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=self.ingredients)
    data_json = response.json() #returns the response data as a json file
    return data_json


  def GetRequest_Text(self): #this method searches spoontacular based on a food name. Ex: pizza, will return ingredients for pizza
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/detect"
    text = "text=" #first part of the payload
    query = "%20".join(self.food_name.split()) #second part of the payload 
    #payload = "text=cheeseburger%20with%20mushrooms" each space is turned into %20
    payload = text + query
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'x-rapidapi-key': "f4c99ab3d5msh07bfa430aafa7bep149cddjsn2d17db76303d",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    data_json = response.json()
    return data_json

# IN CASE WE NEED IT AGAIN (GITHUB GUY'S FOOD RECIPES DIDN'T EXIST)
# def get_analyzed_instructions(self, rec_id):
#   first_part = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
#   recipe_id = str(rec_id)
#   url = first_part + recipe_id + "/analyzedInstructions"
#   querystring = {"stepBreakdown":"true"}
#   headers = {
#       'x-rapidapi-key': "56e969b87cmshb98d477764b7a01p1fdb05jsn81b29370139c",
#       'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
#       }
#   response = requests.request("GET", url, headers=headers, params=querystring)
#   return response.json()
  


  def process_recipe_ID_summary(self, json_file): #this method processes the data into a more usable format. extracts useful data from the json file
    recipe_dict = dict()
    for i in range(self.ingredients['number']):
      try:
          recipe_id = json_file[i]['id']
          recipe_summary = api.summarize_recipe(recipe_id).json()     # needed .json() lol
          recipe_instructions = api.get_analyzed_recipe_instructions(recipe_id, stepBreakdown= True).json()
          recipe_dict[recipe_id] = (recipe_summary, recipe_instructions)
      except:
        print("No Recipes Found!")
      
    return recipe_dict


  def return_results(self, recipe_dict):
    for recipe_id in recipe_dict.keys():
      summary = recipe_dict[recipe_id][0]['summary']
      title = recipe_dict[recipe_id][0]['title']
      try:
        yield title, summary
      except IndexError:
        print("error")
        return None
  
        
#dictionary id: {(summary,title), instructions}
#steps is a list of dictionaries.
  def display_instructions(self, recipe_dict):
    output = ""
    for recipe_id in recipe_dict.keys():
      instructions = recipe_dict[recipe_id][1][0] #steps
      output += instructions['name'] + "\n"
      steps = instructions['steps']
      for index in range(len(steps)): #each step[index] is a dictionary
        currrent_step = steps[index]['step']
        output += f"Step #{index + 1}: " + currrent_step + "\n"
    return "<br>Step".join(output.split("Step"))



  #gets the json file for display_ingredients
  def get_recipe_ingredients_id(self, id):
    first_part = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
    extension = "/ingredientWidget.json"
    url = first_part + str(id) + extension
    headers = {
      'x-rapidapi-key': "f4c99ab3d5msh07bfa430aafa7bep149cddjsn2d17db76303d",
      'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
      }
    return requests.request("GET", url, headers=headers).json()



#parses through big json file to display quantity of ingredients
  def display_ingredients(self, recipe_dict): #display_ingredients gets the data from getRecipeIngredientsByID
    output = "Ingredients Needed:\n"
    id = list(recipe_dict.keys())[0]
    data_json = self.get_recipe_ingredients_id(id)
    for ingredients, list_of_ingredients in data_json.items():
      for ingredients_dict in list_of_ingredients:
        tempStr = ""
        for amount_image_name, value in ingredients_dict.items():
          if amount_image_name == 'amount': #enter the metric from here
            tempStr += str(value['metric']['value']) + ' '
            tempStr += str(value['metric']['unit']) +' '
          elif amount_image_name == 'name':
            tempStr += str(value) + ' '  #adds name of ingredient.
        output += str(tempStr) + '\n'
    return output

        


def getImage(self, json_file): #takes data from GetRequestIngredients and inserts them into a recipeList
  return json_file[0]['image']

  

# def displayRecipe(self, id): #displays the recipe of 1 item
#   return api.get_analyzed_recipe_instructions(id)