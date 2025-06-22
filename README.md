#  Fitness Studio Booking App

This is a simple web application built with **Flask** that allows users to:

- Sign up and log in
- View available fitness classes
- Book a class (without double booking)
- View their bookings

The app uses **SQLite** as its database and supports session-based login.

---

##  Features

-  **User Authentication**: Signup and login system with password hashing
-  **Class Management**: View upcoming classes with details
-  **Booking System**: Book a slot in available classes
-  **No Overbooking**: Prevents users from booking the same class twice
-  **Modular Structure**: Easy to understand and extend
-  **Unit Tests**: Basic tests included using `pytest`

---

##  Technologies Used

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Bootstrap (for styling)
- python-dotenv

---

##  Setup Instructions

Please read the entire README before starting
### 1. Clone the repository

```bash
git clone https://github.com/SarthakBhat22/Flask-Booking-App.git
cd Flask-Booking-App
```

### 2. Create a virtual environment and activate it
```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your secret key by adding a .env file in the root folder
```bash
# Add this to the .env file
SECRET_KEY="your_super_secret_key_here"
```

### 5. Run the app
```bash
python app.py
```

##  Test Instructions

#### ❗ Please run the tests before running the app, as the tests will run and clear the db to make sure everything is working.
```bash
pytest tests/
# Make sure to run this before running the app
```
## About the code
- The code will automatically add some data to the db. More classes can added using the seed_classes.py file.
- Please not that this app uses session based authentication, so do use the UI.
- If you wish to use curl commands, it would look something like this:
  
### 1. Signup

```bash
  curl -X POST http://localhost:5000/signup \
  -d "name=John Doe" \
  -d "email=john@example.com" \
  -d "password=test123" \
  -c cookies.txt

```

### 2. Login
```bash
  curl -X POST http://localhost:5000/login \
  -d "email=john@example.com" \
  -d "password=test123" \
  -c cookies.txt

```

### 3. View Available Classes 
```bash
curl http://localhost:5000/classes
```

### 4. Book a Class
```bash
curl -X POST http://localhost:5000/book \
  -d "class_id=1" \
  -d "client_name=John Doe" \
  -d "client_email=john@example.com" \
  -b cookies.txt
```

### 5. View Bookings
```bash
curl "http://localhost:5000/bookings?email=john@example.com"
```
- Please not that on MacOS it will be 127.0.0.1:5000 instead of localhost:5000
