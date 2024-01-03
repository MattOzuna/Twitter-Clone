"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
with app.app_context():
    db.create_all()


class UserModelTestCase(TestCase):
    """Test views for User."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            user1 = User.signup(
                email="fake_user1@test.com",
                username="fake_user1",
                password="HASHED_PASSWORD1",
                image_url=None
            )

            user2 = User.signup(
                email="fake_user2@test.com",
                username="fake_user2",
                password="HASHED_PASSWORD2",
                image_url=None
            )

            db.session.add_all([user1, user2])
            db.session.commit()

            self.user1_id = user1.id
            self.user2_id = user2.id

            self.client = app.test_client()
            

    def test_user_model(self):
        """Does basic model work?"""
        with app.app_context():
            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

        
            db.session.add(u)
            db.session.commit()

            # User should have no messages & no followers
            self.assertEqual(len(u.messages), 0)
            self.assertEqual(len(u.followers), 0)


    def test_user_repr(self):
        '''does the repr work'''
        with app.app_context():            
            user = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )
            user.id = 22222

            db.session.add(user)
            db.session.commit()

            self.assertEqual(user.__repr__(), "<User #22222: testuser, test@test.com>")
    
    
    def test_user1_follows_user2(self):
        '''does followe through relationship work'''
        with app.app_context(): 
            user1 = User.query.filter_by(id=self.user1_id).one()
            user2 = User.query.filter_by(id=self.user2_id).one()
                       
            user1.following.append(user2)

            db.session.commit()

            self.assertEqual(user2.followers[0].id, user1.id)
            self.assertEqual(user1.following[0].id, user2.id)
    

    def test_user1_is_following(self):
        '''Does is_following work'''

        with app.app_context(): 
            user1 = User.query.filter_by(id=self.user1_id).one()
            user2 = User.query.filter_by(id=self.user2_id).one()
                       
            user1.following.append(user2)

            db.session.commit()

            self.assertTrue(user1.is_following(user2))
            self.assertFalse(user2.is_following(user1))


    def test_user1_is_followed(self):
        '''Does is_followed_by work'''
        with app.app_context(): 
            user1 = User.query.filter_by(id=self.user1_id).one()
            user2 = User.query.filter_by(id=self.user2_id).one()
                       
            user1.following.append(user2)

            db.session.commit()

            self.assertFalse(user1.is_followed_by(user2))
            self.assertTrue(user2.is_followed_by(user1))


    def test_user_signup(self):
        '''Does signup classmethod work'''
        with app.app_context():            
            user = User.signup(
                email="test@test.com",
                username="fake_user",
                password="HASHED_PASSWORD",
                image_url=None
            )

            db.session.commit()

            user_id = user.id

            user = User.query.filter_by(id=user_id).one()

            self.assertEqual(user.username, "fake_user")
            self.assertEqual(user.email, "test@test.com")
            self.assertNotEqual(user.password, "HASHED_PASSWORD")
    

    def test_user_signup_username_taken(self):
        '''
            Does unique username constraint work.
            Username fake_user1 matches user named in setup method.
        ''' 
        with app.app_context():
                       
            user = User.signup(
                email="test@test.com",
                username="fake_user1",
                password="HASHED_PASSWORD",
                image_url=None
            )

            with self.assertRaises(exc.IntegrityError) as context:
                db.session.commit()


    def test_user_athenticate(self):
        '''Does authenitacte class method work'''
        with app.app_context():
            user2 = User.authenticate('fake_user2', 'HASHED_PASSWORD2')
            self.assertEqual(user2.id, self.user2_id)


    def test_user_athenticate_password_invalid(self):
        '''Does authenitacte class method work with wrong password'''
        with app.app_context():
            self.assertFalse(User.authenticate('fake_user2', 'WRONG_PASSWORD'))


    def test_user_athenticate_username_invalid(self):
        '''Does authenitacte class method work with wrong username'''
        with app.app_context():
            self.assertFalse(User.authenticate('fake_user1', 'HASHED_PASSWORD2'))













    