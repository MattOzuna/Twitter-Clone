import os
from unittest import TestCase
from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

with app.app_context():
    db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            User.query.delete()
            Message.query.delete()
            Follows.query.delete()
            

            user = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )


            db.session.add(user)
            db.session.commit()

            self.id = user.id
    
    # def tearDown(self):
    #     return super().tearDown()
    
    def test_message_model(self):
        """Does basic model work?"""
        with app.app_context():
            new_message = Message(
                text="Big Test",
                user_id=self.id
            )

        
            db.session.add(new_message)
            db.session.commit()
            
            self.assertEqual(new_message.user.id, self.id)
        
            msg = Message.query.filter_by(id=new_message.id).one()

        self.assertEqual(msg.text, "Big Test")
        

    def test_message_likes(self):
        with app.app_context():
            message1 = Message(
                text="Test warble",
                user_id=self.id
            )

            message2 = Message(
                text="hopefully this works",
                user_id=self.id 
            )

            user = User.signup("user2", "user2@email.com", "password", None)
            

            db.session.add_all([message1, message2, user])
            db.session.commit()

            user_id = user.id

            user.likes.append(message1)

            db.session.commit()

            likes = Likes.query.filter_by(user_id = user_id).all()

            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].message_id, message1.id)
