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

dam = DataAccessModel()
dam.parseUserData(dam.getUserInfo("user1"))
