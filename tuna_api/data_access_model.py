import pyrebase
from dotenv import find_dotenv, dotenv_values

class DataAccessModel:

    def __init__(self):
        conf = dotenv_values(find_dotenv())
        config = {
            "apiKey": conf.get('FB_API'),
            "authDomain": conf.get('FB_AUTH_DOMAIN'),
            "databaseURL": conf.get('FB_DATABASE_URL'),
            "storageBucket": conf.get('FB_STORAGE_BUCKET'),
            "serviceAccount": conf.get('FB_SERVICE_ACCOUNT')
        }       
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()

    ## User Operations
    def formatUserJson(self, user):
        return {
            'UID': user['uid'],
            'Name': user['name'],
            'Email': user['email'],
            'Password_hash': user['password_hash'],
            'ProfileImage': user['pfp'],
            'Allergies': user['allergies'],
            'Preferences': user['preferences']
        }
    
    def userIsNull(self, uid):
        return self.db.child("Users").child(uid).get().val() == None
    
    def createUser(self, uid, name, email, password_hash, pfp, allergies, preferences):	
        user = {
            'uid': uid,
            'name': name,
            'email': email,
            'password_hash': password_hash,
            'pfp': pfp,
            'allergies': allergies,
            'preferences': preferences
        }
        if self.userIsNull(uid):
            self.db.child("Users").child(uid).set(self.formatUserJson(user))
        else:
            self.updateUser(uid, self.formatUserJson(user))

    def getUserInfo(self, uid):
        if self.userIsNull(uid) is False:
            return self.db.child("Users").child(uid).get().val()
        else:
            print("Invalid user. Please enter a valid user identification key.")

    def updateUser(self, uid, user_data):
        if self.userIsNull(uid) is False:
            self.db.child("Users").child(uid).update(user_data)
        else:
            print("Invalid user. Please enter a valid user identification key.")

    def deleteUser(self, uid):
        if self.userIsNull(uid) is False:
            self.db.child("Users").child(uid).remove()
        else:
            print("Invalid user. No user was deleted.")

    def parseUserData(self, userData):
        print("Name: " + userData['name'])
        print("Email: " + userData['email'])
        print("Allergies: " + str(userData['allergies']))
        print("Preferences: " + str(userData['preferences']))

    ## Favourite Recipe Operations
    def formatFavouriteRecipeJson(self, recipe):
        return {
            'id': recipe['id'],
            'uid': recipe['uid'],
            'title': recipe['title'],
            'prep_time': recipe['prep_time'],
            'ingredients': recipe['ingredients'],
            'instructions': recipe['instructions'],
            'picture_url': recipe['picture_url'],
        }
    
    def favouriteRecipeIsNull(self, uid):
        return self.db.child("Favourites").child().order_by_child("uid").equal_to(uid).get().val() == None

    def createFavouriteRecipe(self, id, uid, title, prep_time, ingredients, instructions, picture_url):
        recipe = {
            'id': id,
            'uid': uid,
            'title': title,
            'prep_time': prep_time,
            'ingredients': ingredients,
            'instructions': instructions,
            'picture_url': picture_url,
        }
        if self.favouriteRecipeIsNull(uid):
            self.db.child("Favourites").child().set(self.formatFavouriteRecipeJson(recipe))
        else:
            self.updateFavouriteRecipe(uid, self.formatFavouriteRecipeJson(recipe))

    def getFavouriteRecipeInfo(self, uid):
        if self.favouriteRecipeIsNull(uid) is False:
            return self.db.child("Favourites").child().order_by_child("uid").equal_to(uid).get().val()
        else:
            print("Invalid user. Please enter a valid user identification key.")
    
    def updateFavouriteRecipe(self, uid, recipe_data):
        if self.favouriteRecipeIsNull(uid) is False:
            self.db.child("Favourites").child().update(recipe_data)
        else:
            print("Invalid user. Please enter a valid user identification key.")

    def deleteFavouriteRecipe(self, uid):
        if self.favouriteRecipeIsNull(uid) is False:
            self.db.child("Favourites").child().remove()
        else:
            print("Invalid user. No user was deleted.")

    def parseFavouriteRecipeData(self, recipeData):
        print("Title: " + recipeData['title'])
        print("Prep Time: " + recipeData['prep_time'])
        print("Ingredients: " + str(recipeData['ingredients']))
        print("Instructions: " + str(recipeData['instructions']))
        print("Picture URL: " + recipeData['picture_url'])

    ## Shopping List Operations
        
    def formatShoppingListJson(self, shopping_list):
        return {
            'uid': shopping_list['uid'],
            'ingredients': shopping_list['ingredients'],
        }
    
    def shoppingListIsNull(self, uid):
        return self.db.child("ShoppingList").child().order_by_child("uid").equal_to(uid).get().val() == None
    
    def createShoppingList(self, uid, ingredients):
        shopping_list = {
            'uid': uid,
            'ingredients': ingredients,
        }
        if self.shoppingListIsNull(uid):
            self.db.child("ShoppingList").child().set(self.formatShoppingListJson(shopping_list))
        else:
            self.updateShoppingList(uid, self.formatShoppingListJson(shopping_list))

    def getShoppingListInfo(self, uid):
        if self.shoppingListIsNull(uid) is False:
            return self.db.child("ShoppingList").child().order_by_child("uid").equal_to(uid).get().val()
        else:
            print("Invalid user. Please enter a valid user identification key.")

    def updateShoppingList(self, uid, shopping_list_data):
        if self.shoppingListIsNull(uid) is False:
            self.db.child("ShoppingList").child().update(shopping_list_data)
        else:
            print("Invalid user. Please enter a valid user identification key.")

    def deleteShoppingList(self, uid):
        if self.shoppingListIsNull(uid) is False:
            self.db.child("ShoppingList").child().remove()
        else:
            print("Invalid user. No user was deleted.")

    def parseShoppingListData(self, shopping_list_data):
        print("Ingredients: " + str(shopping_list_data['ingredients']))
        
dam = DataAccessModel()
dam.parseUserData(dam.getUserInfo("user1"))
