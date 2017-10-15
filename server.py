from flask import Flask, request, make_response
from flask_restful import Resource, Api
from pymongo import MongoClient
# from utils.mongo_json_encoder import JSONEncoder
from bson.objectid import ObjectId
import bcrypt
import json
import pdb

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
app.bcrypt_rounds = 12
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)

def validate_auth(email, password):
    user_collection = app.db.users
    user = user_collection.find_one({'email': email})

    if user is None:
        return False
    else:
        # check if the hash we generate based on auth matches stored hash
        encodedPassword = password.encode('utf-8')
        if bcrypt.hashpw(encodedPassword, user['password']) == user['password']:
            return True
        else:
            return False

def authenticated_request(func):
    def wrapper(*args, **kwargs):
        auth = request.authorization

        if not auth or not validate_auth(auth.username, auth.password):
            return ({'error': 'Basic Auth Required.'}, 401, None)

        return func(*args, **kwargs)

    return wrapper



## Write Resources here


class Trip(Resource):

    @authenticated_request
    def get(self):
        #now that I set up my trips collection in MongoDB, I can start working on the functions
        trips_collection = app.db.trips
        if 'email' in request.args:
            trip = request.args['email']
            result_trip = trips_collection.find_one({'email': trip})
            if result_trip is None:
                not_found_msg = {'error': 'user not found'}
                json_not_found = json.dumps(not_found_msg)
                return (json_not_found, 400, None)
            return (result_trip, 200, None)

        invalid_parameters_msg = {'error': 'invalid search request'}
        json_invalid_msg = json.dumps(invalid_parameters_msg)
        return (json_invalid_msg, 400, None)


    @authenticated_request
    def post(self):
        trips_collection = app.db.trips
        #I want them to have the email set, destination, and a start date
        #waypoints can be empty, completed set to false, end-date can be empty.
        trip = request.json
        if 'email' in trip and 'destination' in trip and 'start_date' in trip and 'end_date' in trip and 'waypoints' in trip and 'completed' in trip:

            if trip['waypoints'] is None:
                trip['waypoints'] = []


            result = trips_collection.insert_one(trip)

            trip_object = trips_collection.find_one({"_id": ObjectId(result.inserted_id)})
            return (trip_object, 200, None)

        error_dict = {'error': 'Missing Parameters'}


        return (error_dict, 400, None)


    @authenticated_request
    def patch(self):
        #get request to get the trip object, by the name and by the email
        trips_collection = app.db.trips
        if 'destination' in request.args and 'email' in request.args:
            selected_trip = trips_collection.find_one({'destination': request.args['destination'], 'email': request.args['email']})
            trip = request.json

            if 'destination' in trip:
                if trip['destination'] != None:
                    trips_collection.update_one({'email': request.args['email'], 'destination': request.args['destination']}, {'$set' : {'destination': trip['destination']}})
                    return ({"success": "You have successfully updated " + str(trips_collection.find_one({'destination': request.args['destination'], 'email': request.args['email']}))}, 200, None)


            if 'waypoints' in trip:
                if trip['waypoints'] != None:
                    trips_collection.update_one({'email': request.args['email'], 'destination': request.args['destination']}, {'$set': {'waypoints': trip['waypoints']}})
                    return ({"success": "You have successfully updated " + str(trips_collection.find_one({'destination': request.args['destination'], 'email': request.args['email']}))}, 200, None)



            if 'completed' in trip:
                if trip['completed'] != None:
                    trips_collection.update_one({'email': request.args['email'], 'destination': request.args['destination']}, {'$set': {'completed': trip['completed']}})
                    return ({"success": "You have successfully updated " + str(trips_collection.find_one({'destination': request.args['destination'], 'email': request.args['email']}))}, 200, None)



            error_dict = {'error': 'invalid patch request, missing body'}
            return (error_dict, 400, None)

        error_dict = {'error': 'Missing url parameters'}
        return (error_dict, 400, None)

    @authenticated_request
    def delete(self):
        trips_collection = app.db.trips
        if 'destination' in request.args and 'email' in request.args:

            selected_trip = trips_collection.find_one({'destination': request.args['destination'], 'email': request.args['email']})
            if selected_trip != None:
                result = trips_collection.delete_one({'destination': request.args['destination'], 'email': request.args['email']})
            return ('You just deleted your' + str(selected_trip) + ' trip', 200, None )



class User(Resource):

    def patch(self):
        #patch request is basically getting the document with a get request
        #and then updating the value

        users_collection = app.db.users
        name_result = request.json
        searched_email = request.args['email']
        searched_obj = users_collection.find_one({'email': searched_email})
        if searched_obj is None:
            not_found_msg = {'error': 'Name not found'}
            json_not_found = json.dumps(not_found_msg)
            return (json_not_found, 401, None)
        result = users_collection.update_one({'email': searched_email}, { "$set" : {'username': name_result['username']} })
        # json_searched_obj = JSONEncoder().encode(searched_obj)
        searched_obj.pop('password')
        return (searched_obj, 200, None)

    def post(self):

      new_user = request.json
      print ("the new user object is: " + str(new_user))

      users_collection = app.db.users


      if ('username' in new_user and 'password' in new_user and 'email' in new_user and 'id' in new_user):
          password = new_user['password']
          encodedPassword = password.encode('utf-8')

          hashed = bcrypt.hashpw(
          encodedPassword, bcrypt.gensalt(app.bcrypt_rounds)
          )
          new_user['password'] = encodedPassword

          #After inserting an obj into the database, it returns to us the object ID
          #So we use the id in our find_one function only after it has been posted
          #Regularly, how would we be able to find a user based off of it's id?
          result = users_collection.insert_one(new_user)
          print ("the result is: " + str(result))
          user_object = users_collection.find_one({"_id": ObjectId(result.inserted_id)})
          user_object.pop('password')
          return (user_object, 200, None)

      error_dict = {'error': 'Missing Parameters'}


      return (error_dict, 400, None)



    def get(self):
      #getting the collection
      users_collection = app.db.users

      #getting the user's username from url parameters
      if 'email' in request.args and 'password' in request.args:
          user_email = request.args['email']
          user_password = request.args['password']

          #result is the user_obj from our database
          result = users_collection.find_one({'email': user_email})
          if result is None:

             not_found_msg = {'error': 'user not found'}
             json_not_found = json.dumps(not_found_msg)
             return (json_not_found, 400, None)

          #The jsonPassword is the password that was entered in the parameter of this GET request.

          encodedPassword = user_password.encode('utf-8')

          if bcrypt.hashpw(encodedPassword, result['password']) == result['password']:
              result.pop('password')
              return (result, 200, None)

          else:
              error_dict = {'error': 'Invalid login information'}


              return (error_dict, 400, None)








      invalid_parameters_msg = {'error': 'invalid search request'}
      json_invalid_msg = json.dumps(invalid_parameters_msg)
      return (json_invalid_msg, 400, None)

    def delete(self):
        #in here we want to delete the user, but we only want to delete the user if we can delete the trips along with it
        users_collection = app.db.users
        trips_collection = app.db.trips
        #so we have to check if theres any trips associated with that user first, if there is, delete those trips, then delete the user

        if 'email' in request.args and 'destination' in request.args:
            #try to find any trips that has the user emailed inside
            selected_trip = trips_collection.find({'email': request.args['email']})
            #if there are none, then we can delete the user
            selected_user = users_collection.find_one({'email': request.args['email']})


            if selected_trip is None:
                users_collection.delete_one({'email': request.args['email']})
                success_msg = {'success': 'you just deleted ' + selected_user}
                json_success_msg = json.dumps(success_msg)
                return (json_success_msg, 200, None)

            trips_collection.delete({'email': request.args['email']})
            users_collection.delete_one({'email': request.args['email']})

            success_msg = {'success': 'you just deleted ' + selected_user}
            json_success_msg = json.dumps(success_msg)
            return (json_success_msg, 200, None)

        invalid_parameters_msg = {'error': 'invalid user search request'}
        json_invalid_msg = json.dumps(invalid_parameters_msg)
        return (json_invalid_msg, 400, None)



api.add_resource(Trip, '/trips')
api.add_resource(User, '/users')



@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(JSONEncoder().encode(data), code)
    resp.headers.extend(headers or {})
    return resp

if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request
    # related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)
