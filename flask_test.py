from app import app
import unittest

class FlaskappTests(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Setup the test
        self.app.testing = True
