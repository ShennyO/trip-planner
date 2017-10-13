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
            username="Ouyeezyy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )


        response = self.app.get(
        '/users',
        query_string=dict(email="sunnyouyang.ehs@gmail.com")
        )


        self.assertEqual(response.status_code, 200)





    def testUserParam(self):

        response = self.app.post(
            '/users',
            data=json.dumps(dict(
            username="Shenny",
            password="testzzz"

            )), content_type = 'application/json'

        )


        print("IT WORKED")

        self.assertEqual(response.status_code, 400)

    def testPatch(self):


        #to do the Patch, I get the user with a get request with the user's email in the URL parameters
        #and then i'll change the parameters with the body of the request.
        #to test the patch, I want to see if the parameters I changed is equal
        #to the client's post request.

        changed_username="BlackOuyeezy"

        self.app.post(
            '/users',
            data=json.dumps(dict(
            username="BOuyeezy",
            password="test",
            email="sunnyouyangs.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )


        #the patch is going to take both a query string, for the request arguments and also take data thats from our body
        response = self.app.patch(
            '/users',
            query_string=dict(email="sunnyouyangs.ehs@gmail.com"),
            data=json.dumps(dict(
            username="BlackOuyeezy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_get(self):
        print("HEYO")
        self.app.post(
            '/users',
            data=json.dumps(dict(
            username="Ouyeezyy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )

        response = self.app.get(
        '/users',
        query_string=dict(email="sunnyouyangs.ehs@gmail.com")
        )

        self.assertEqual(response.status_code, 400)

    def test_nonexistent_patch(self):

        response = self.app.patch(
            '/users',
            query_string=dict(email="sunnyouyangs.ehs@gmail.com"),
            data=json.dumps(dict(
            username="BlackOuyeezy",
            password="test",
            email="sunnyouyang.ehs@gmail.com",
            id="51011123"
            )), content_type='application/json'
        )

        self.assertEqual(response.status_code, 401)








if __name__ == '__main__':
    unittest.main()
