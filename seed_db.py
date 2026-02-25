

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.models import db, User, UserRole


def seed_users():
    """Add demo users to the database"""
    app = create_app()
    
    with app.app_context():
        # Check if users already exist
        if User.query.first():
            print("✓ Database already has users. Skipping seed.")
            return
        
        demo_users = [
            {
                "email": "employee@company.com",
                "password": "password123",
                "name": "John Employee",
                "role": UserRole.EMPLOYEE,
            },
            {
                "email": "hr@company.com",
                "password": "password123",
                "name": "Sarah HR Manager",
                "role": UserRole.HR,
            },
            {
                "email": "admin@company.com",
                "password": "password123",
                "name": "Admin User",
                "role": UserRole.ADMIN,
            },
        ]
        
        # Create users
        for user_data in demo_users:
            user = User(
                email=user_data["email"],
                password=user_data["password"],
                name=user_data["name"],
                role=user_data["role"],
            )
            db.session.add(user)
            print(f"✓ Created user: {user_data['email']} ({user_data['role'].value})")
        
        db.session.commit()
        print("\n Demo users created successfully!")
        print("\nDemo Credentials:")
        print("=" * 50)
        for user_data in demo_users:
            print(f"Email: {user_data['email']}")
            print(f"Password: {user_data['password']}")
            print(f"Role: {user_data['role'].value}")
            print("-" * 50)

if __name__ == "__main__":
    seed_users()