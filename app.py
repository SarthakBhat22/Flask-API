from flask import Flask, request, render_template, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app and configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studio.db'  # Local SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SECRET_KEY", "default-dev-key")  # Secure session
db = SQLAlchemy(app)

# ------------------------- Models -------------------------

class FitnessClass(db.Model):
    """
    Model for fitness classes offered in the studio.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    instructor = db.Column(db.String(50), nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)


class Booking(db.Model):
    """
    Model to track user bookings for classes.
    """
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('fitness_class.id'), nullable=False)
    client_name = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    fitness_class = db.relationship("FitnessClass", backref="bookings")


class User(db.Model):
    """
    Model for registered users (clients or instructors).
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_instructor = db.Column(db.Boolean, default=False)

# ------------------------- Routes -------------------------

@app.route("/")
def home():
    """
    Landing page for the fitness studio.
    """
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handles user registration.
    """
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # Prevent duplicate email registration
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("signup"))

        # Create new user
        hashed = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()

        # Login user after signup
        session["user_email"] = user.email
        session["user_name"] = user.name
        flash(f"Signup successful! Welcome, {user.name}.", "success")
        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))

        session["user_email"] = user.email
        session["user_name"] = user.name
        flash(f"Login successful! Welcome back, {user.name}.", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Logs out the user by clearing the session.
    """
    session.clear()
    return redirect(url_for("home"))


@app.route("/classes")
def show_classes():
    """Displays all upcoming fitness classes."""
    classes = FitnessClass.query.filter(FitnessClass.datetime >= datetime.now()).all()
    return render_template("classes.html", classes=classes)

@app.route("/book", methods=["GET", "POST"])
def book():
    """
    Allows users to book a class.
    """
    if request.method == "POST":
        class_id = request.form["class_id"]
        name = session.get("user_name") or request.form["client_name"]
        email = session.get("user_email") or request.form["client_email"]

        fitness_class = FitnessClass.query.get(class_id)
        if not fitness_class or fitness_class.available_slots <= 0:
            flash("Booking failed: class not available or sold out.", "danger")
            return redirect(url_for("book"))

        # Prevent duplicate booking for same class
        existing = Booking.query.filter_by(
            class_id=class_id,
            client_email=email
        ).first()

        if existing:
            flash("You've already booked this class.", "warning")
            return redirect(url_for("book"))

        # Proceed with booking
        booking = Booking(class_id=class_id, client_name=name, client_email=email)
        fitness_class.available_slots -= 1
        db.session.add(booking)
        db.session.commit()
        flash("Booking successful!", "success")
        return redirect(url_for("show_bookings", email=email))

    available_classes = FitnessClass.query.filter(FitnessClass.available_slots > 0).all()
    return render_template("book.html", classes=available_classes)


@app.route("/bookings")
def show_bookings():
    """
    Displays the bookings for the logged-in user or queried email.
    """
    email = session.get("user_email") or request.args.get("email")
    bookings = []

    if email:
        bookings = Booking.query.filter_by(client_email=email).all()

    return render_template("bookings.html", bookings=bookings, email=email)

# ------------------------- Run App -------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Seed data if empty
        if not FitnessClass.query.first():
            classes = [
                FitnessClass(name="Yoga", datetime=datetime(2025, 6, 23, 10), instructor="Alice", available_slots=5),
                FitnessClass(name="Zumba", datetime=datetime(2025, 6, 24, 11), instructor="Bob", available_slots=8),
                FitnessClass(name="HIIT", datetime=datetime(2025, 6, 25, 12), instructor="Charlie", available_slots=6),
            ]
            db.session.add_all(classes)
            db.session.commit()

    app.run(debug=True)
