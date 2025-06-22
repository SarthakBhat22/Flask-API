"""
Unit Tests for Fitness Studio Booking Application.

This test suite validates core user flows:
- User signup
- User login
- Preventing duplicate bookings

It uses an in-memory SQLite database for isolation and speed.
"""

import unittest
from app import app, db, FitnessClass, User
from werkzeug.security import generate_password_hash
from datetime import datetime

class FitnessAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            # Add test class
            test_class = FitnessClass(
                name="Test Yoga",
                datetime=datetime(2025, 7, 1, 10, 0),
                instructor="Test",
                available_slots=3
            )
            db.session.add(test_class)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        response = self.client.post("/signup", data={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }, follow_redirects=True)
        self.assertIn(b"Welcome, Test User", response.data)

    def test_login(self):
        with app.app_context():
            user = User(name="Login User", email="login@example.com",
                        password=generate_password_hash("password123"))
            db.session.add(user)
            db.session.commit()

        response = self.client.post("/login", data={
            "email": "login@example.com",
            "password": "password123"
        }, follow_redirects=True)
        self.assertIn(b"Welcome, Login User", response.data)

    def test_duplicate_booking(self):
        # Signup user
        self.client.post("/signup", data={
            "name": "Booker",
            "email": "booker@example.com",
            "password": "testpass"
        }, follow_redirects=True)

        # First booking
        res1 = self.client.post("/book", data={
            "class_id": 1,
            "client_name": "Booker",
            "client_email": "booker@example.com"
        }, follow_redirects=True)
        self.assertIn(b"Bookings for", res1.data)

        # Duplicate booking
        res2 = self.client.post("/book", data={
            "class_id": 1,
            "client_name": "Booker",
            "client_email": "booker@example.com"
        }, follow_redirects=True)
        self.assertIn(b"already booked", res2.data.lower())


if __name__ == "__main__":
    unittest.main()
