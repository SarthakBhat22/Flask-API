from app import db, FitnessClass, app
from datetime import datetime

with app.app_context():
    new_classes = [
            FitnessClass(name="Yoga", datetime=datetime(2025, 6, 29, 10), instructor="Alice", available_slots=5),
            FitnessClass(name="Zumba", datetime=datetime(2025, 6, 30, 11), instructor="Bob", available_slots=8),
            FitnessClass(name="HIIT", datetime=datetime(2025, 7, 1, 12), instructor="Charlie", available_slots=6),
        ]
    db.session.add_all(new_classes)
    db.session.commit()
    print("Classes added.")
