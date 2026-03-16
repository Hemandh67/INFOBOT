import os
import django
import datetime
from pymongo import MongoClient

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infobot.settings')
django.setup()

from django.contrib.auth.models import User
from django.conf import settings

def create_data():
    print("Creating dummy data...")
    
    # 1. Create admin user in SQLite
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created (password: admin123).")
    else:
        print("Superuser 'admin' already exists.")
    
    # 2. Create notices in MongoDB
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    notices_collection = db['notices']
    
    # Check if notices exist
    if notices_collection.count_documents({}) > 0:
        print("Notices already exist in MongoDB. Skipping creation.")
        return

    notices = [
        {
            'title': 'Semester Exam Schedule',
            'description': 'The end semester exams will begin from 20th May. Time table is attached on the notice board.',
            'category': 'Exam',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        },
        {
            'title': 'Campus Recruitment: TechCorp',
            'description': 'TechCorp will be visiting our campus on 25th May for recruitment. Eligible branches: CS, IT. CGPA > 7.5 required.',
            'category': 'Placement',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        },
        {
            'title': 'Annual Cultural Fest "Sanskriti"',
            'description': 'Our annual fest "Sanskriti" is scheduled for 10th June. Auditions for dance and music will start next week in the auditorium.',
            'category': 'Event',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        },
        {
            'title': 'Library Holiday',
            'description': 'The library will remain closed tomorrow due to maintenance work.',
            'category': 'General',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        },
        {
            'title': 'Python Workshop',
            'description': 'A 2-day workshop on Python programming will be held this weekend. Register at the CS department before Friday.',
            'category': 'Event',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        },
        {
            'title': 'Mid-Term Results Declared',
            'description': 'The mid-term results for 3rd year students have been declared. Check the student portal.',
            'category': 'Exam',
            'posted_by': 'admin',
            'date_posted': datetime.datetime.now()
        }
    ]
    
    notices_collection.insert_many(notices)
    print(f"Created {len(notices)} dummy notices in MongoDB.")

    print("Dummy data creation complete!")

if __name__ == '__main__':
    create_data()
