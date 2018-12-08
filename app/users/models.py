"""
    Global variable users_data  holds  user data , initially its empty
"""

use = []

class User:
    def __init__(self, user_id, user_name, email, password):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """

        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password


    def get_dictionary(self):
        return{
            "user_id" :len(use)+1,
            "user_name" : self.user_name,
            "email" : self.email,
            "password" : self.password
    }

    def create_user(self):
        """
            This method receives an object of the
            class, creates and returns a dictionary from the object
        """
        user = {
            
            "user_id" :self.user_id,
            "user_name" : self.user_name,
            "email" : self.email,
            "password" : self.password
        }

        use.append(user)

        return user
    @staticmethod
    def get_user_id(user_name):
        for existing_user in use:
            if user_name == existing_user['user_name']:
                return existing_user['user_id']
        return {"message": "user doesn't exist"}
