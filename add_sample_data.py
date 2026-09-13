# Script to populate database with sample data for testing
# Run this script once to add test data to your database

from database import Database
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def add_sample_data():
    """Add sample data to the database"""
    
    db = Database()
    
    print("Clearing existing data...")
    db.db.users.delete_many({})
    db.db.companies.delete_many({})
    db.db.reviews.delete_many({})
    
    print("Adding sample companies...")
    companies = [
        {"name": "Google", "created_at": datetime.now()},
        {"name": "Microsoft", "created_at": datetime.now()},
        {"name": "Amazon", "created_at": datetime.now()},
        {"name": "Meta", "created_at": datetime.now()},
        {"name": "Apple", "created_at": datetime.now()},
        {"name": "Tesla", "created_at": datetime.now()},
        {"name": "Netflix", "created_at": datetime.now()},
        {"name": "Uber", "created_at": datetime.now()},
    ]
    company_ids = {}
    for company in companies:
        result = db.create_company(company)
        company_ids[company["name"]] = str(result)
    
    print("Adding sample employees...")
    employees = [
        {
            "email": "john.doe@email.com",
            "password": generate_password_hash("password123"),
            "name": "John Doe",
            "user_type": "employee",
            "company": "Google",
            "job_role": "Software Developer (SDE)",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "email": "jane.smith@email.com",
            "password": generate_password_hash("password123"),
            "name": "Jane Smith",
            "user_type": "employee",
            "company": "Microsoft",
            "job_role": "Product Manager",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "email": "bob.wilson@email.com",
            "password": generate_password_hash("password123"),
            "name": "Bob Wilson",
            "user_type": "employee",
            "company": "Amazon",
            "job_role": "Manager",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "email": "alice.johnson@email.com",
            "password": generate_password_hash("password123"),
            "name": "Alice Johnson",
            "user_type": "employee",
            "company": "Meta",
            "job_role": "Data Scientist",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
    ]
    
    employee_ids = []
    for employee in employees:
        employee_id = db.create_user(employee)
        employee_ids.append(str(employee_id))
    
    print("Adding sample job seekers...")
    job_seekers = [
        {
            "email": "seeker1@email.com",
            "password": generate_password_hash("password123"),
            "name": "Raj Kumar",
            "user_type": "jobseeker",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "email": "seeker2@email.com",
            "password": generate_password_hash("password123"),
            "name": "Priya Sharma",
            "user_type": "jobseeker",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
    ]
    
    for seeker in job_seekers:
        db.create_user(seeker)
    
    print("Adding sample reviews...")
    reviews_data = [
        # Google reviews
        {
            "user_id": employee_ids[0],
            "company_id": company_ids["Google"],
            "job_role": "Software Developer (SDE)",
            "rating": 5,
            "title": "Excellent company culture and innovation",
            "feedback": "Working at Google has been an amazing experience. The company values innovation and provides great tools. The work-life balance is good and the compensation is competitive.",
            "pros": "Great culture, learning opportunities, good salary",
            "cons": "Very competitive, high workload at times",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=30),
            "updated_at": datetime.now() - timedelta(days=30)
        },
        # Microsoft reviews
        {
            "user_id": employee_ids[1],
            "company_id": company_ids["Microsoft"],
            "job_role": "Product Manager",
            "rating": 4,
            "title": "Great career growth opportunities",
            "feedback": "Microsoft provides excellent opportunities for career growth. The teams are collaborative and the products are impactful. The work environment is professional and supportive.",
            "pros": "Career growth, good benefits, supportive teams",
            "cons": "Can be bureaucratic at times",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=25),
            "updated_at": datetime.now() - timedelta(days=25)
        },
        # Amazon reviews
        {
            "user_id": employee_ids[2],
            "company_id": company_ids["Amazon"],
            "job_role": "Manager",
            "rating": 4,
            "title": "Fast-paced and results-oriented",
            "feedback": "Amazon is a very results-oriented company. The pace is fast and demanding, but you learn a lot. Leadership principles are emphasized throughout the organization.",
            "pros": "Fast learning, clear metrics, leadership principles",
            "cons": "High pressure, long hours",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=20),
            "updated_at": datetime.now() - timedelta(days=20)
        },
        # Meta reviews
        {
            "user_id": employee_ids[3],
            "company_id": company_ids["Meta"],
            "job_role": "Data Scientist",
            "rating": 5,
            "title": "Cutting-edge technology and talented team",
            "feedback": "Working with Big Data and ML at Meta is incredible. The team consists of top talents and the infrastructure is world-class. You get to work on projects that impact billions.",
            "pros": "Talented team, cutting-edge tech, good compensation",
            "cons": "Very competitive culture",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=15),
            "updated_at": datetime.now() - timedelta(days=15)
        },
        # Additional reviews for variety
        {
            "user_id": employee_ids[0],
            "company_id": company_ids["Amazon"],
            "job_role": "Software Developer (SDE)",
            "rating": 3,
            "title": "Good opportunity but demanding",
            "feedback": "Amazon is a good company for learning and career growth. However, the work-life balance can be challenging. The interview process is rigorous and expectations are very high.",
            "pros": "Learning, career growth, strong brand",
            "cons": "Work-life balance, high pressure",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=10),
            "updated_at": datetime.now() - timedelta(days=10)
        },
        {
            "user_id": employee_ids[1],
            "company_id": company_ids["Google"],
            "job_role": "Product Manager",
            "rating": 4,
            "title": "Great place to launch your career",
            "feedback": "Google offers excellent opportunities for product managers. The interview process is challenging but fair. Once you're in, you get access to great mentors and opportunities to lead impactful projects.",
            "pros": "Mentorship, impact, learning opportunities",
            "cons": "Competitive environment",
            "is_previous": False,
            "created_at": datetime.now() - timedelta(days=5),
            "updated_at": datetime.now() - timedelta(days=5)
        },
    ]
    
    for review in reviews_data:
        db.create_review(review)
    
    print("\n✅ Sample data added successfully!")
    print("\nYou can now login with these accounts:")
    print("\nEmployees:")
    for i, employee in enumerate(employees):
        print(f"  {i+1}. Email: {employee['email']}")
        print(f"     Password: password123")
    print("\nJob Seekers:")
    for i, seeker in enumerate(job_seekers):
        print(f"  {i+1}. Email: {seeker['email']}")
        print(f"     Password: password123")
    print("\n💡 Tip: Use these accounts to test the platform features")

if __name__ == "__main__":
    try:
        add_sample_data()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure MongoDB is running!")
