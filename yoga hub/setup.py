#!/usr/bin/env python3
"""
Setup script for Sangam Yoga Club Flask Application
"""

import os
import sys
from datetime import datetime, date, time
from app import app, db, User, Event

def create_sample_data():
    """Create sample data for development"""
    
    print("Creating sample data...")
    
    # Create sample admin user
    admin_user = User(
        email='admin@nitdelhi.ac.in',
        name='Admin User',
        role='admin'
    )
    
    # Create sample professor
    prof_user = User(
        email='prof.rajesh@nitdelhi.ac.in',
        name='Prof. Rajesh Kumar',
        role='professor'
    )
    
    # Create sample student
    student_user = User(
        email='student1@nitdelhi.ac.in',
        name='Priya Verma',
        role='student'
    )
    
    db.session.add_all([admin_user, prof_user, student_user])
    
    # Create sample events
    events = [
        Event(
            title='Morning Flow Session',
            description='Start your day with energizing yoga poses and breathing exercises.',
            date=date(2025, 11, 15),
            time=time(7, 0),
            location='Campus Yoga Hall',
            instructor='Dr. Priya Sharma',
            max_participants=25,
            category='class'
        ),
        Event(
            title='Stress Relief Workshop',
            description='Learn techniques to manage academic stress through yoga and meditation.',
            date=date(2025, 11, 20),
            time=time(17, 0),
            location='Meditation Room',
            instructor='Prof. Raj Kumar',
            max_participants=30,
            category='workshop'
        ),
        Event(
            title='Power Yoga Challenge',
            description='Intense yoga session for building strength and endurance.',
            date=date(2025, 11, 25),
            time=time(18, 0),
            location='Sports Complex',
            instructor='Instructor Amit',
            max_participants=20,
            category='class'
        ),
        Event(
            title='Mindfulness Meditation',
            description='Guided meditation session for mental clarity and peace.',
            date=date(2025, 12, 1),
            time=time(8, 30),
            location='Meditation Room',
            instructor='Dr. Meera Patel',
            max_participants=35,
            category='class'
        ),
        Event(
            title='Yoga for Beginners',
            description='Perfect for those new to yoga. Learn basic poses and breathing techniques.',
            date=date(2025, 12, 5),
            time=time(16, 0),
            location='Campus Yoga Hall',
            instructor='Ms. Anjali Singh',
            max_participants=40,
            category='workshop'
        )
    ]
    
    db.session.add_all(events)
    
    try:
        db.session.commit()
        print("✅ Sample data created successfully!")
        print(f"✅ Created {len(events)} sample events")
        print("✅ Created sample users (admin, professor, student)")
        print("\n📝 Login with any of these test emails:")
        print("   - admin@nitdelhi.ac.in (Admin)")
        print("   - prof.rajesh@nitdelhi.ac.in (Professor)")
        print("   - student1@nitdelhi.ac.in (Student)")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating sample data: {e}")

def setup_database():
    """Initialize the database"""
    print("Setting up database...")
    
    try:
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if we have any users
        user_count = User.query.count()
        if user_count == 0:
            create_sample_data()
        else:
            print(f"📊 Database already has {user_count} users")
            
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("🕉️  Setting up Sangam Yoga Club Application")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Creating from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from .env.example")
            print("🔧 Please edit .env file with your Google OAuth credentials")
        else:
            print("❌ No .env.example file found")
    
    # Setup database
    with app.app_context():
        setup_database()
    
    print("\n🚀 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Google OAuth credentials")
    print("2. Get credentials from: https://console.developers.google.com/")
    print("3. Run the application with: python app.py")
    print("4. Visit: http://localhost:5000")
    print("\n💡 For Google OAuth setup:")
    print("   - Authorized redirect URIs: http://localhost:5000/auth/google/callback")
    print("   - Authorized JavaScript origins: http://localhost:5000")

if __name__ == '__main__':
    main()