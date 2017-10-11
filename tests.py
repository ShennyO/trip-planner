import server
import unittest
import json
import bcrypt
import base64
from pymongo import MongoClient
import pdb


class TripPlannerTestCase(unittest.TestCase):
    def setUp(self):

      self.app = server.app.test_client()
      # Run app in testing mode to retrieve exceptions and stack traces
      server.app.config['TESTING'] = True

      mongo = MongoClient('localhost', 27017)
      global db

      # Reduce encryption workloads for tests
      server.app.bcrypt_rounds = 4

      db = mongo.trip_planner_test
      server.app.db = db

      db.drop_collection('users')
      db.drop_collection('trips')

    # User tests, fill with test methods
    def testCreateUser(self):

        self.app.post(
            '/users',
            data=json.dumps(dict(
            username="Ouyeezy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )


        response = self.app.get(
        '/users',
        query_string=dict(email="sunnyouyang.ehs@gmail.com")
        )


        response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)

    def testUserParam(self):

        response = self.app.post(
            '/users',
            data=json.dumps(dict(
            username="Shenny",
            password="test"

            )), content_type = 'application/json'

        )

        response_json = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)

    def testPatch(self):


        #to do the Patch, I get the user with a get request with the user's email in the URL parameters
        #and then i'll change the parameters with the body of the request.
        #to test the patch, I want to see if the parameters I changed is equal
        #to the client's post request.

        self.app.post(
            '/users',
            data=json.dumps(dict(
            username="Ouyeezy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )


        user_obj = self.app.get(
        '/users',
        query_string=dict(email="sunnyouyang.ehs@gmail.com")
        )

        self.app.patch








if __name__ == '__main__':
    unittest.main()
