import os
from unittest import TestCase
from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

with app.app_context():
    db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            User.query.delete()
            Message.query.delete()
            Follows.query.delete()
            

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )
            db.session.add(u)
            db.session.commit()

            self.id = u.id
    
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
