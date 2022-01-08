from server import app
import unittest
import os
from model import db, connect_to_db


# Drop and re-create the test database.
os.system("dropdb Time2un")
os.system("createdb Time2Run")


# Unittesting so I can test individual code units
class Time2RunTests(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""
    def setUp(self):
        """Code to run before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "run"
        self.client = app.test_client()

        # Connect to test database
        connect_to_db(app)
        db.drop_all()
        db.create_all()


        def test_homepage(self):
            """Is the homepage reachable"""

        result = self.client.get("/")
        self.assertIn(b"homepage reached", result.data)


        ###############################################################################
        #                           LOGIN ROUTE TESTS                                 #
        ###############################################################################

        
    def test_login_route_correct(self):
        """tests that the login route is working correctly with correct login information"""
        result = self.client.post("/user_login",
        data={"email":"test1@hello.com", "password":"Hellotest1"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200) # status code 200: Asserting request was successful and 
                                                  # the server responded with the data requested
        self.assertIn(b"Welcome Back test_user1!", result.data)



    def test_login_route_incorrect(self):
        """tests that the login route is working correctly with an incorrect password"""
        result = self.client.post("/user_login",
        data={"email":"test1@hello.com", "password":"222222"}, follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Login details for test_user1 is incorrect. Try again!", result.data)
    


    def tearDown(self):
        """Run at end of every test."""

        db.session.close()
        db.drop_all()



if __name__ == '__main__':
    unittest.main()