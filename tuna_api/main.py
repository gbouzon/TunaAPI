#imports
from fastapi import FastAPI
from dotenv import find_dotenv, dotenv_values
import requests
import json

app = FastAPI()
config = dotenv_values(find_dotenv())
food_apikey = config.get("FOOD_APIKEY")
search_url = "https://api.spoonacular.com/recipes/complexSearch"
info_url = "https://api.spoonacular.com/recipes/" # + id + "/information"


##write a function that takes in a query and returns recipe ids in a list -> 5 max, if 0, return "no recipes"
# write a function that takes the list of recipe ids and calls the info_url for each id and returns list of 
# ingredients and instructions
# get intolerances from database and pass as a strings separated by commas

def search_recipes(query, intolerances):
    querystring = {
        "apiKey": food_apikey, "query": query, "instructionsRequired": "true", "number": "5",
        "intolerances": intolerances
    }
    response = requests.request("GET", search_url, params=querystring)

    ids = []
    for item in response.json()["results"]:
        ids.append(item["id"])

    return ids    

def get_recipe_info(ids):
    fields_to_include = [
        'id',
        'title',
        'readyInMinutes',
        'instructions',
        'image',
    ]
    result = []
    for id in ids:
        querystring = {"apiKey": food_apikey}
        response = requests.request("GET", info_url + str(id) + "/information", params=querystring)
        original_values = [ingredient['original'] for ingredient in response.json().get('extendedIngredients', [])]
        extracted_data = {field: response.json()[field] for field in fields_to_include}
        extracted_data['ingredients'] = original_values
        result.append(extracted_data)
    return result


print(get_recipe_info(search_recipes("chicken", ["dairyFree", "glutenFree"])))
# define endpoints
# @app.get("/")
# def root():
#     return {"message": recomment_recipe_api_call("chicken")}




