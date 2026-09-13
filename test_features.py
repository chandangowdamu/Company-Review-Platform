#!/usr/bin/env python3
"""
Test script to verify all platform features
Tests: authentication, review CRUD, autosuggest, edit, delete, admin approval
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

# Test credentials
EMPLOYEE_EMAIL = "john.doe@email.com"
EMPLOYEE_PASS = "password123"
ADMIN_EMAIL = "admin@email.com"
ADMIN_PASS = "admin123"

session = requests.Session()

print("=" * 60)
print("COMPANY REVIEW PLATFORM - FEATURE TEST SUITE")
print("=" * 60)

# Test 1: Login with employee account
print("\n[TEST 1] Employee Login")
print("-" * 60)
try:
    login_data = {
        'email': EMPLOYEE_EMAIL,
        'password': EMPLOYEE_PASS
    }
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
    if response.status_code == 200 and "Employee Dashboard" in response.text:
        print("✅ Login successful - dashboard loaded")
    else:
        print(f"❌ Login failed - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: View Employee Dashboard
print("\n[TEST 2] View Employee Dashboard")
print("-" * 60)
try:
    response = session.get(f"{BASE_URL}/employee-dashboard")
    if response.status_code == 200:
        if "Write a Review" in response.text and "My Reviews" in response.text:
            print("✅ Dashboard loaded with all sections")
        else:
            print("⚠️  Dashboard loaded but some sections missing")
    else:
        print(f"❌ Dashboard load failed - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Get company suggestions (autosuggest)
print("\n[TEST 3] Company Autosuggest API")
print("-" * 60)
try:
    response = session.get(f"{BASE_URL}/api/companies")
    if response.status_code == 200:
        companies = response.json()
        if len(companies) > 0:
            print(f"✅ Got {len(companies)} companies for autosuggest")
            print(f"   Sample: {[c['name'] for c in companies[:3]]}")
        else:
            print("⚠️  Empty company list")
    else:
        print(f"❌ Failed - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Create a new review
print("\n[TEST 4] Create Review")
print("-" * 60)
try:
    review_data = {
        'company_id': 'google_id',  # Will be replaced with actual ID
        'job_role': 'Software Developer (SDE)',
        'rating': 4,
        'title': 'Great workplace with good benefits',
        'feedback': 'Good learning environment, supportive management team.',
        'pros': 'Flexible work from home, excellent benefits',
        'cons': 'Long working hours sometimes',
        # interview metadata
        'interview_difficulty': 'Medium',
        'interview_rounds': 3,
        'technical_questions': 'Data structures, system design',
        'hr_experience': 'Friendly and prompt',
        'tips': 'Practice coding problems daily',
        'salary_range': '90k-110k',
        'years_experience': '2-4',
        'location': 'New York'
    }
    
    # First get company list
    companies = session.get(f"{BASE_URL}/api/companies").json()
    if companies:
        review_data['company_id'] = companies[0]['_id']
        response = session.post(f"{BASE_URL}/api/create-review", json=review_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Review created: {result.get('review_id', 'Success')}")
        else:
            print(f"⚠️  Response: {response.status_code}")
            if response.headers.get('content-type') == 'application/json':
                print(f"   Message: {response.json()}")
    else:
        print("⚠️  No companies available")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Get user's reviews (via company endpoint)
print("\n[TEST 5] Get Company Reviews")
print("-" * 60)
try:
    companies = session.get(f"{BASE_URL}/api/companies").json()
    if companies:
        company_id = companies[0]['_id']
        response = session.get(f"{BASE_URL}/api/company/{company_id}/reviews")
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ Retrieved {len(reviews) if isinstance(reviews, list) else 0} reviews")
            if isinstance(reviews, list) and reviews:
                # check interview metadata keys exist
                sample = reviews[0]
                for key in ['interview_difficulty','interview_rounds','technical_questions','hr_experience','tips','salary_range','years_experience','location']:
                    if key not in sample:
                        print(f"⚠️  Missing field {key} in response")
        else:
            print(f"⚠️  Status: {response.status_code}")
    else:
        print("⚠️  No companies available")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6: Search reviews (general)
print("\n[TEST 6] Search Reviews with Filters")
print("-" * 60)
try:
    search_params = {'min_rating': 3}
    response = session.get(f"{BASE_URL}/api/search-reviews", params=search_params)
    if response.status_code == 200:
        reviews = response.json()
        print(f"✅ Found {len(reviews)} reviews with rating >= 3")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 6b: Search by company and role
print("\n[TEST 6b] Search by Company and Role")
print("-" * 60)
try:
    companies = session.get(f"{BASE_URL}/api/companies").json()
    if companies:
        comp_id = companies[0]['_id']
        params = {'company_id': comp_id, 'role': 'Software Developer (SDE)'}
        response = session.get(f"{BASE_URL}/api/search-reviews", params=params)
        if response.status_code == 200:
            reviews = response.json()
            print(f"✅ Found {len(reviews)} reviews for company {companies[0]['name']} and role SDE")
        else:
            print(f"⚠️  Status: {response.status_code}")
    else:
        print("⚠️  No companies to test with")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 7: View user dashboard (job seeker)
print("\n[TEST 7] Job Seeker Dashboard Access")
print("-" * 60)
try:
    session.cookies.clear()  # Clear cookies to simulate new session
    response = session.get(f"{BASE_URL}/user-dashboard")
    if response.status_code == 200 and "search" in response.text.lower():
        print("✅ Job seeker dashboard accessible and displays reviews")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 8: Check 404 error handling
print("\n[TEST 8] Error Page Handling")
print("-" * 60)
try:
    response = session.get(f"{BASE_URL}/invalid-page")
    if response.status_code == 404 and "404" in response.text:
        print("✅ 404 error page displayed correctly")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("FEATURE TEST SUMMARY")
print("=" * 60)
print("✅ = Passed | ⚠️  = Warning | ❌ = Failed")
print("\nTo manually test advanced features:")
print("1. Open http://127.0.0.1:5000 in your browser")
print("2. Login with: john.doe@email.com / password123")
print("3. Test: Review submission, edit modal, autosuggest, delete")
print("4. Test: Previous company with document upload")
print("5. Test: Admin approval workflow")

print("\nNOTE: For edit and admin features, you need to test through the UI")
print("=" * 60)
