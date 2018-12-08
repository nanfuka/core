from flask import jsonify, make_response, request
from .models import User, use
import flask.views
from app.helper import validate_data, validate_data_length
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, jwt_required

# use = []
class UserRegistration(flask.views.MethodView):

    def get(self):
        """
             This method returns all users created
        """
        if not use:
            return make_response(jsonify({"message": "No Registered users"}), 200)
        return make_response(jsonify({"users": use}), 200)

    def post(self):
        parser = request.get_json()
        user_name = parser.get('user_name')
        email = parser.get('email')
        password = parser.get('password')
        user_id = len(use)+1
        uses = User(user_id, user_name, email, password)
        for u in use:
            if user_name == u['user_name'] or email == u['email']:
                return make_response(jsonify({'message': 'username or email in use already'}), 400)
            if password == u['password']:
                return make_response(jsonify({'message': 'password in use already, please choose another password.'}), 400)
        user = uses.get_dictionary()

        if validate_data(user_name):
            return make_response(jsonify({'message': 'user_name field is required'}), 400)
        if validate_data(email):
            return make_response(jsonify({'message': 'Please add your user email'}), 400)
        if validate_data(password):
            return make_response(jsonify({'message': 'Please add your user password'}), 400)

        if validate_data_length(user_name):
            return make_response(jsonify({'message': 'username is to short'}), 400)
        if validate_data_length(password):
            return make_response(jsonify({'message': 'password is too short'}), 400)
        uses.create_user()
        response = {"message":"you have successfully added a new user"}
        response = {'user':user }
        return jsonify(response)

class UserLogin(flask.views.MethodView):
    def post(self):
        parser = request.get_json()
        user_name = parser.get('user_name')
        password = parser.get('password')

        if validate_data(user_name) and validate_data(password):
            return make_response(jsonify({'message': 'please enter both the username and password'}), 400)



        for one_user in use:
            if password == one_user['password'] and user_name == one_user["user_name"]:
                access_token = create_access_token(identity={"user_name": user_name})
                return make_response(jsonify({
                    "message": "You have successfully logged in", "access token": access_token}), 200)

        return make_response(jsonify({"message": "No such username and password"}), 200)
    @jwt_required
    def get(self):
        """ 
            This method returns all users
            of the id given to it from the list of available orders
        """
        if use:
            return make_response(jsonify({"users": use}), 200)
        return make_response(jsonify({"message": "parcel not found in our database please check the id and try again"}),
                             404)
    # @staticmethod
    # def UserRegistration.use_avai(user_name):
    #     for users in use:
    #         if users == use['user_name']:
    #             return users
    #         return None


# @app.route('/api/v1/parcels', methods=['POST'])
# def send_parcel():
#     """function to create a new parcel. A user is expected to enter all
#      their credentials in their valid format
#     """

#     data = request.get_json(force=True)

#     user_id = data.get('user_id')

#     email = data.get('email')

#     status = data.get('status')

#     item_to_be_shipped = data.get('item_to_be_shipped')

#     weight = data.get('weight')

#     name_of_reciever = data.get('name_of_reciever')

#     destination = data.get('destination')

#     item_origin = data.get('item_origin')

#     parcel = {'order_id': len(order_list)+1,

#               'user_id': user_id,

#               'email': email,

#               'status': status,

#               'item_to_be_shipped': item_to_be_shipped,

#               'weight': weight,

#               'name_of_reciever': name_of_reciever,

#               'item_origin': item_origin,

#               'destination': destination



#               }

#     if user_id is None:

#         return jsonify({"message": "Enter your user_id please"}), 400

#     if email is None:

#         return jsonify({"message": "Enter your email please"}), 400
#     if item_to_be_shipped is None:

#         return jsonify(
#             {"message": "Enter your item_to_be_shipped please"}), 400

#     if weight is None:

#         return jsonify({"message": "Enter your weight please"}), 400

#     if name_of_reciever is None:

#         return jsonify({"message": "Enter your name_of_reciever please"}), 400

#     if item_origin is None:

#         return jsonify({"message": "Enter your item_origin please"}), 400

#     if destination is None:

#         return jsonify({"message": "Enter your destination please"}), 400

#     if isinstance(user_id, str) or user_id == " ":

#         return jsonify({"message": "The input should be a number"}), 400

#     if isinstance(status, int) or status == " ":

#         return jsonify({"message": "The input should be a string"}), 400

#     if isinstance(item_to_be_shipped, int) or item_to_be_shipped == " ":

#         return jsonify({"message": "The input should be a string"}), 400

#     if isinstance(weight, str) or weight == " ":

#         return jsonify({"message": "The input should be a number"}), 400

#     if isinstance(name_of_reciever, int) or name_of_reciever == " ":

#         return jsonify({"message": "The input should be a string"}), 400

#     if isinstance(item_origin, int) or item_origin == " ":

#         return jsonify({"message": "The input should be a string"}), 400

#     if isinstance(destination, int) or user_id == " ":

#         return jsonify({"message": "The input should be a string"}), 400

#     special_characters = ['$', '#', '@', '!', '*']

#     if any(char in special_characters for char in data['username']):
#         return {'message': 'username cannot have special characters'}, 400

#     if any(char in special_characters
#            for char in (data['item_to_be_shipped'])):
#         return {'message':
#                 'item_to_be_shipped cannot have special characters'}, 400

#     if any(char in special_characters for char in (data['destination'])):
#         return {'message': 'destination cannot have special characters'}, 400

#     if any(char in special_characters for char in (data['item_origin'])):
#         return {'message': 'item_origin cannot have special characters'}, 400

#     if any(char in special_characters for char in (data['name_of_reciever'])):
#         return {'message':
#                 'name_of_reciever cannot have special characters'}, 400

#     if email is None:

#         return jsonify({"message": "Invalid email"}), 400

#     if item_to_be_shipped is None:

#         return jsonify(
#             {"message": "Enter your item_to_be_shipped please"}), 400

#     if isinstance(item_to_be_shipped, int):

#         return jsonify({"message": "The input should be string"}), 400

#     if weight is None:

#         return jsonify({"message": "Enter the parcel weight please"}), 400

#     if isinstance(weight, str):

#         return jsonify({"message": "The input should be a number"}), 400

#     if item_origin is None:

#         return jsonify({"message": "Enter your item_origin please"}), 400

#     if isinstance(weight, str):

#         return jsonify({"message": "The input should be a number"}), 400

#     if destination is None:

#         return jsonify({"message": "Enter your destination please"}), 400

#     if isinstance(destination, int):

#         return jsonify({"message": "The input should be a string"}), 400

#     if name_of_reciever is None:

#         return jsonify({"message": "Enter your name_of_reciever please"}), 400

#     if isinstance(name_of_reciever, int):

#         return jsonify({"message": "The input should be a string"}), 400

#     if data['item_to_be_shipped'].isspace() or \
#             (' ' in data['item_to_be_shipped']):

#         return jsonify({"message": "item to be shipped cannot be blank"}), 400

#     if data['name_of_reciever'].isspace()\
#             or (' ' in data['name_of_reciever']):

#         return jsonify({"message": "name of reciever cannot be blank"}), 400

#     if data['destination'].isspace() or (' ' in data['destination']):

#         return jsonify({"message": "destination cannot be blank"}), 400

#     if data['item_origin'].isspace() or (' ' in data['item_origin']):

#         return jsonify({"message": "item origin cannot be blank"}), 400

#     order_list.append(parcel)

#     return jsonify({"parcel_order was successfully created": parcel}), 201

#         # new_user.create_user()
#         # return make_response(jsonify({"message": "You have successfully registered"}), 201)


# # class UserLogin(flask.views.MethodView):
# #     def post(self):
# #         parser = request.get_json()
# #         user_name = parser.get('user_name')
# #         password = parser.get('password')

# #         if validate_data(user_name):
#             return make_response(jsonify({'message': 'user_name field is required'}), 400)

#         if validate_data(password):
#             return make_response(jsonify({'message': 'Please add your user password'}), 400)

#         for existing_user in users_data:
#             if user_name != existing_user['user_name']:
#                 if password != existing_user['password']:
#                     return make_response(jsonify({"message": "username and password dont match"}), 400)
#             if password == existing_user['password'] and user_name == existing_user["user_name"]:
#                 user_id = User.get_user_id(user_name)
#                 access_token = create_access_token(identity={"user_id": user_id, "user_name": user_name})
#                 return make_response(jsonify({
#                     "message": "You have successfully logged in this is you're", "access token": access_token}), 200)

#         return make_response(jsonify({"message": "incorrect username and password"}), 200)