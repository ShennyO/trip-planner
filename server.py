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
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planner_development
app.bcrypt_rounds = 12
api = Api(app)




## Write Resources here
class User(Resource):
    def patch(self):
        #patch request is basically getting the document with a get request
        #and then updating the value
        users_collection = app.db.users
        name_result = request.json
        searched_name = request.args['name']
        searched_obj = users_collection.find_one({'name': searched_name})
        if searched_obj is None:
            not_found_msg = {'error': 'Name not found'}
            json_not_found = json.dumps(not_found_msg)
            return (json_not_found, 400, None)
        users_collection.update_one({'name': searched_name}, { "$set" : {'name': name_result['name']} })
        # json_searched_obj = JSONEncoder().encode(searched_obj)
        return (searched_obj, 200, None)

    def post(self):

      new_user = request.json
      print ("the new user object is: " + str(new_user))

      users_collection = app.db.users

    #   pdb.set_trace()
      if ('username' in new_user and 'password' in new_user and 'email' in new_user and 'id' in new_user):
          print ("the post request worked")
          result = users_collection.insert_one(new_user)
          print ("the result is: " + str(result))
          user_object = users_collection.find_one({"_id": ObjectId(result.inserted_id)})
          return (user_object, 200, None)

      error_dict = {'error': 'Missing Parameters'}
    #   json_error_obj = json.dumps(error_dict)

      return (error_dict, 400, None)


	  #querying for the object we just inserted into the database


    def get(self):
      #getting the collection
      users_collection = app.db.users
      #getting the user's username from url parameters
      if 'email' in request.args:
          user_email = request.args['email']
        #   user_email = request.args.get('email')
        #   user_id = request.args.get('id')
        #   user_password = request.args.get('password')
          #querying our database for that specific username
          result = users_collection.find_one({'email': user_email})
          if result is None:
             pdb.set_trace()
             not_found_msg = {'error': 'user not found'}
             json_not_found = json.dumps(not_found_msg)
             return (json_not_found, 400, None)
        #   response_json = JSONEncoder().encode(result)
          return (result, 200, None)

      invalid_parameters_msg = {'error': 'invalid search request'}
      json_invalid_msg = json.dumps(invalid_parameters_msg)
      return (json_invalid_msg, 400, None)






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
