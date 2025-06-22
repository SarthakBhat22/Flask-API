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

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Flask-API.git
cd Flask-API
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
SECRET_KEY=your_super_secret_key_here
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
