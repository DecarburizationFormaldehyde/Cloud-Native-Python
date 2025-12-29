from flask import request, json

from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Setup the test
        self.app.testing = True

    def test_users_status_code(self):
        # send HTTP GET request to the application
        result = self.app.get('api/v1/users')
        # assert the status code of the response
        self.assertEqual(result.status_code,200)

    def test_tweets_status_code(self):
        # send HTTP GET request to the application
        result = self.app.get('api/v2/tweets')
        # assert the status code of the response
        self.assertEqual(result.status_code,200)

    def test_info_status_code(self):
        # send HTTP GET request to the application
        result = self.app.get('api/V1/info')
        # assert the status code of the response
        self.assertEqual(result.status_code,200)

    def test_addusers_status_code(self):
        # send HTTP POST request to the application
        result = self.app.post('api/v1/users',
                               data={"username":"manish21", "email":"manishtest@gmail.com", "password": "test123"},
                               content_type='application/json')
        print(result)
         # assert the status code of the response
        self.assertEqual(result.status_code,201)

    def test_updusers_status_code(self):
        # send HTTP PUT request to the application
        result = self.app.put('api/v1/users/4',
                               data={"password":"testing1234"},
                               content_type='application/json')
        # assert the status code of the response
        self.assertEqual(result.status_code,200)

    def test_addtweets_status_code(self):
        # send HTTP POST request to the application
        result = self.app.post('api/v2/tweets',
                               data=json.dumps({"username":"mahesh@rocks",
                                     "body":"This is my first tweet#test"}),
                               content_type='application/json')
        # assert the status code of the response
        self.assertEqual(result.status_code,201)

    def test_delusers_status_code(self):
        # send HTTP DELETE request to the application
        result = self.app.delete('api/v1/users',
                                 data='{"username":"manish21"}',
                                 content_type='application/json')
        # assert the status code of the response
        self.assertEqual(result.status_code,200)
    