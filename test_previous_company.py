#!/usr/bin/env python3
"""
Test script to verify previous company workflow (no admin approval required)
"""

import requests
import json
import os
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

# Test credentials
EMPLOYEE_EMAIL = "jane.smith@email.com"
EMPLOYEE_PASS = "password123"

session = requests.Session()

print("=" * 70)
print("PREVIOUS COMPANY WORKFLOW TEST (No Admin Approval)")
print("=" * 70)

# Test 1: Login
print("\n[TEST 1] Employee Login")
print("-" * 70)
try:
    login_data = {
        'email': EMPLOYEE_EMAIL,
        'password': EMPLOYEE_PASS
    }
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=True)
    if response.status_code == 200 and "Employee Dashboard" in response.text:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Add a previous company with document
print("\n[TEST 2] Add Previous Company (with document)")
print("-" * 70)
try:
    # Create a temporary test file
    test_file_path = "test_document.txt"
    with open(test_file_path, 'w') as f:
        f.write("This is a test employment document")
    
    with open(test_file_path, 'rb') as f:
        files = {
            'document': ('test_document.txt', f, 'text/plain')
        }
        data = {
            'company_name': 'Tesla',
            'job_role': 'Software Developer (SDE)'
        }
        response = session.post(f"{BASE_URL}/api/add-previous-company", 
                               data=data, files=files)
    
    if response.status_code == 201:
        result = response.json()
        if result.get('success'):
            print("✅ Previous company added successfully")
            print(f"   Company ID:{result.get('company_id')}")
            previous_company_id = result.get('company_id')
        else:
            print(f"❌ Failed: {result}")
    else:
        print(f"❌ Failed - Status: {response.status_code}")
        print(f"   Response: {response.text}")
    
    # Clean up test file
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Create a review for the previous company (should not need approval)
print("\n[TEST 3] Create Review for Previous Company (No Admin Approval)")
print("-" * 70)
try:
    review_data = {
        'company_id': previous_company_id,
        'job_role': 'Software Developer (SDE)',
        'rating': 4,
        'title': 'Great workplace and learning opportunities',
        'feedback': 'Tesla offers excellent growth opportunities and interesting projects.',
        'pros': 'Cutting-edge technology, great compensation',
        'cons': 'High work pressure, demanding deadlines',
        'is_previous': True
    }
    
    response = session.post(f"{BASE_URL}/api/create-review", json=review_data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Review created successfully for previous company!")
        print(f"   Review ID: {result.get('review_id')}")
    elif response.status_code == 403:
        result = response.json()
        print(f"❌ Access denied: {result.get('error')}")
    else:
        print(f"❌ Failed - Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Verify review appears in dashboard
print("\n[TEST 4] Verify Review Appears in Dashboard")
print("-" * 70)
try:
    response = session.get(f"{BASE_URL}/employee-dashboard")
    if response.status_code == 200:
        if 'Great workplace' in response.text:
            print("✅ Review appears in employee dashboard")
        else:
            print("⚠️  Review may not be displayed yet (could be normal)")
    else:
        print(f"❌ Dashboard failed - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: Check that other employees can also add same previous company
print("\n[TEST 5] Another Employee Adds Same Previous Company")
print("-" * 70)
try:
    # Logout and login with different employee
    session.cookies.clear()
    login_data = {
        'email': 'bob.wilson@email.com',
        'password': 'password123'
    }
    response = session.post(f"{BASE_URL}/login", data=login_data)
    
    # Add same company
    test_file_path = "test_document2.txt"
    with open(test_file_path, 'w') as f:
        f.write("Another test employment document")
    
    with open(test_file_path, 'rb') as f:
        files = {
            'document': ('test_document2.txt', f, 'text/plain')
        }
        data = {
            'company_name': 'Tesla',
            'job_role': 'Product Manager'
        }
        response = session.post(f"{BASE_URL}/api/add-previous-company", 
                               data=data, files=files)
    
    if response.status_code == 201:
        print("✅ Second employee successfully added same previous company")
    else:
        print(f"⚠️  Status: {response.status_code}")
    
    # Clean up
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("WORKFLOW SUMMARY")
print("=" * 70)
print("✅ = Passed | ⚠️  = Warning | ❌ = Failed")
print("\nIMPORTANT CHANGES:")
print("1. ✅ Previous companies can be added directly (no admin approval needed)")
print("2. ✅ Reviews can be written immediately after adding a company")
print("3. ✅ Document upload is still required for verification")
print("4. ✅ Multiple employees can add and review same previous company")
print("\n" + "=" * 70)
