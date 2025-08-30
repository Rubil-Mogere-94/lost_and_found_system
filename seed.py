#!/usr/bin/env python3
"""
Seed the database with sample data
"""

from app.database import init_db, Session
from app.models import User, Item, Claim
from datetime import datetime, timedelta, timezone

def seed_database():
    # Initialize database
    init_db()
    
    session = Session()
    
    try:
        # Check if users already exist
        if session.query(User).count() > 0:
            print("Database already has data. Skipping seeding.")
            return
        
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@example.com",
            role="admin"
        )
        session.add(admin)
        
        # Create sample users
        users = [
            User(name="John Doe", email="john@example.com", role="finder"),
            User(name="Jane Smith", email="jane@example.com", role="finder"),
            User(name="Alice Johnson", email="alice@example.com", role="claimer"),
            User(name="Bob Williams", email="bob@example.com", role="claimer"),
        ]
        
        for user in users:
            session.add(user)
        
        session.commit()
        
        # Create sample items
        items = [
            Item(
                description="Black backpack with laptop stickers",
                location="Library, 2nd floor",
                finder_id=2,  # John Doe
                date_found=datetime.now(timezone.utc) - timedelta(days=3)
            ),
            Item(
                description="Silver keychain with car keys",
                location="Parking lot, section B",
                finder_id=3,  # Jane Smith
                date_found=datetime.now(timezone.utc) - timedelta(days=2)
            ),
            Item(
                description="Blue water bottle",
                location="Gym, locker room",
                finder_id=2,  # John Doe
                date_found=datetime.now(timezone.utc) - timedelta(days=1)
            ),
            Item(
                description="Wallet with credit cards",
                location="Cafeteria, table 5",
                finder_id=3,  # Jane Smith
                date_found=datetime.now(timezone.utc),
            )
        ]
        
        for item in items:
            session.add(item)
        
        session.commit()

        # Add a claim for one of the items
        claim = Claim(item_id=4, claimer_id=4, status="approved")
        session.add(claim)
        session.commit()

        print("Database seeded successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {str(e)}")
        raise
    finally:
        Session.remove()

if __name__ == '__main__':
    seed_database()
