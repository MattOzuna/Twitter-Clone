"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase
from models import db, connect_db, Message, User, Likes, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
with app.app_context():
    db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):

    def setUp(self):
        with app.app_context():

            db.drop_all()
            db.create_all()

            testuser1 = User.signup(username="Franky",
                                        email="test1@test.com",
                                        password="testuser",
                                        image_url=None)
            
            testuser2 = User.signup(username="Patrick",
                                        email="test2@test.com",
                                        password="testuser",
                                        image_url=None)
            testuser3 = User.signup(username="Marty",
                                        email="test3@test.com",
                                        password="testuser",
                                        image_url=None)
            
            db.session.commit()

            self.id1 = testuser1.id
            self.id2 = testuser2.id
            self.id3 = testuser3.id
    

    def test_list_users(self):
        '''Does the user index work'''
        with app.test_client() as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("@Franky", html)
            self.assertIn("@Patrick", html)


    def test_list_user_with_search_q(self):
        '''DOes the user index work with a search query'''
        with app.test_client() as client:
            response = client.get("/users?q=Patrick")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertNotIn("@Franky", html)
            self.assertIn("@Patrick", html)
    

    def test_user_show(self):
        '''Does route for a specific user work'''
        with app.test_client() as client:
            response = client.get(f"/users/{self.id1}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("@Franky", html)


    def test_user_show_following(self):
        '''
        Does the show followers route work
        '''
        with app.app_context(): 
            # setup Patrick following Franky
            user1 = User.query.filter_by(id=self.id1).one()
            user2 = User.query.filter_by(id=self.id2).one()
                    
            user2.following.append(user1)

            db.session.commit()

        with app.test_client() as client:
            # logged in as Patrick
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id2

            response = client.get(f'/users/{self.id2}/following')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("@Franky", html)
            self.assertNotIn("@Marty", html)

    
    def test_user_show_following_not_logged_in(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.id1}/following', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Access unauthorized", html)


    def test_user_show_followers(self):
        '''
        Does the show followers route work
        '''
        with app.app_context(): 
            # setup Patrick following Franky
            user1 = User.query.filter_by(id=self.id1).one()
            user2 = User.query.filter_by(id=self.id2).one()
                    
            user2.following.append(user1)

            db.session.commit()

        with app.test_client() as client:
            # logged in as Franky
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id1

            response = client.get(f'/users/{self.id1}/followers')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("@Patrick", html)
            self.assertNotIn("@Marty", html)
    

    def test_user_show_followers_not_logged_in(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.id1}/followers', follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Access unauthorized", html)



    



