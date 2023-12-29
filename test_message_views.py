"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

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


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()
            Message.query.delete()


            testuser = User.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        image_url=None)
            
            db.session.commit()
            self.id = testuser.id
            

    def tearDown(self):
        with app.app_context():
            User.query.delete()
            Message.query.delete()
            db.session.commit()


    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        
        with app.test_client() as c:
            
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            
            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            # self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.location, f'/users/{self.id}')

            msg = Message.query.filter_by(user_id=self.id).one()

            self.assertEqual(msg.text, "Hello")

    
    def test_get_message(self):
        with app.test_client() as client:

            with app.app_context():
                new_message = Message(text = "Big Test",
                                    user_id = f"{self.id}")
                db.session.add(new_message)
                db.session.commit()
                msg_id = new_message.id

        
            response = client.get(f'/messages/{msg_id}')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<p class="single-message">Big Test</p>', html)


    def test_delete_message(self):
        with app.test_client() as client:

            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.id

            with app.app_context():
                new_message = Message(text = "Delete Test",
                                    user_id = f"{self.id}")
                db.session.add(new_message)
                db.session.commit()

                msg_id = new_message.id

            response = client.post(f'/messages/{msg_id}/delete')
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, f'/users/{self.id}')

            msg = Message.query.all()
        
            self.assertEqual(len(msg), 0)






