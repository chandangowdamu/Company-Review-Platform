# Testing Guide - Company Review Platform

This document provides detailed instructions for testing all features of the Review Platform.

## Pre-Testing Setup

### 1. Start the Application
```bash
# Activate virtual environment
# Windows
venv\Scripts\activate

# Execute the run script or directly run:
python app.py
```

### 2. Load Sample Data (Optional)
```bash
python add_sample_data.py
```

This will populate the database with:
- 4 sample employees
- 2 sample job seekers
- 8 sample companies
- 6 sample reviews

### 3. Access the Application
Open browser and navigate to: `http://127.0.0.1:5000`

---

## Test Cases

### A. AUTHENTICATION TESTING

#### Test Case A1: Employee Registration
**Steps:**
1. Click "Register" button
2. Select "Employee" toggle
3. Fill in form:
   - Name: Test Employee
   - Email: testemployee@test.com
   - Password: TestPass123
   - Company: Google
   - Job Role: Software Developer (SDE)
4. Click "Create Account"

**Expected Result:** 
- Account created successfully
- Redirected to employee dashboard
- Message: "Account created successfully! Redirecting..."

#### Test Case A2: Job Seeker Registration
**Steps:**
1. Click "Register" button
2. Select "Job Seeker" toggle (default)
3. Fill in form:
   - Name: Test Seeker
   - Email: testseeker@test.com
   - Password: SeekPass123
4. Click "Create Account"

**Expected Result:**
- Account created successfully
- Redirected to job seeker dashboard
- Message: "Account created successfully! Redirecting..."

#### Test Case A3: Duplicate Email Registration
**Steps:**
1. Try to register with an email that already exists
2. Attempt to create account

**Expected Result:**
- Error message: "Email already registered"
- Form is not submitted

#### Test Case A4: Validation Errors
**Steps:**
1. Try registering with:
   - Empty name field
   - Invalid email format
   - Password less than 6 characters
   - Employee without company/role

**Expected Result:**
- Appropriate error messages displayed
- Form not submitted
- User data preserved

#### Test Case A5: Employee Login
**Steps:**
1. Go to login page
2. Enter:
   - Email: testemployee@test.com
   - Password: TestPass123
3. Click "Login"

**Expected Result:**
- Login successful
- Redirected to employee dashboard
- Welcome message shows employee name

#### Test Case A6: Job Seeker Login
**Steps:**
1. Go to login page
2. Enter:
   - Email: testseeker@test.com
   - Password: SeekPass123
3. Click "Login"

**Expected Result:**
- Login successful
- Redirected to job seeker dashboard
- Welcome message shows seeker name

#### Test Case A7: Invalid Credentials
**Steps:**
1. Go to login page
2. Enter:
   - Email: wrong@email.com
   - Password: wrongpass
3. Click "Login"

**Expected Result:**
- Error message: "Invalid email or password"
- Not logged in
- Redirected back to login page

---

### B. EMPLOYEE DASHBOARD TESTING

#### Test Case B1: Dashboard Display
**Prerequisites:** Logged in as employee

**Steps:**
1. Navigate to employee dashboard
2. Verify dashboard elements

**Expected Result:**
- Dashboard header visible
- Stats cards showing:
  - Number of reviews
  - Current company
  - Current role
- "Write a Review" section visible
- "My Reviews" section visible

#### Test Case B2: Submit Current Company Review
**Prerequisites:** Logged in as employee

**Steps:**
1. In "Write a Review" section, "Current Company" tab is active
2. Company and role are auto-filled
3. Fill review form:
   - Select 5-star rating
   - Title: "Great workplace"
   - Feedback: Detailed multi-line feedback
   - Pros: "Good culture"
   - Cons: "Long hours"
4. Click "Submit Review"

**Expected Result:**
- Success message: "Review submitted successfully!"
- Page reloads
- New review appears in "My Reviews" section
- Review shows correct details

#### Test Case B3: Submit Current Company Review - Missing Fields
**Steps:**
1. Leave feedback field empty
2. Try to submit

**Expected Result:**
- Error message: "All fields required"
- Form not submitted

#### Test Case B4: Submit Invalid Rating
**Steps:**
1. Try to submit without selecting rating

**Expected Result:**
- HTML5 validation prevents submission
- Rating field is highlighted

#### Test Case B5: Add Previous Company with Document
**Steps:**
1. Click "Previous Company" tab
2. Fill form:
   - Company Name: Microsoft
   - Job Role: Product Manager
   - Upload file: Select a PDF/JPG file
3. Click "Add Previous Company"

**Expected Result:**
- Success message: "Previous company added! You can now write reviews..."
- File is uploaded to `/static/uploads/`
- Can now write reviews for this company

#### Test Case B6: Add Previous Company - Missing Document
**Steps:**
1. Click "Previous Company" tab
2. Fill company name and role
3. Don't select file
4. Click "Add Previous Company"

**Expected Result:**
- Error message: "Document required for previous company"
- Form not submitted

#### Test Case B7: Invalid File Type Upload
**Steps:**
1. Click "Previous Company" tab
2. Try to upload .exe or .zip file
3. Click "Add Previous Company"

**Expected Result:**
- Error message: "Invalid file type"
- Only specific types allowed (PDF, DOC, JPG, etc.)

#### Test Case B8: Edit Review
**Steps:**
1. Find a review in "My Reviews" section
2. Click "Edit" button
3. Modify details (title, rating, feedback)
4. Click "Update"

**Expected Result:**
- Review is updated
- Updated timestamp reflects change
- Changes visible in review card

#### Test Case B9: Delete Review
**Steps:**
1. Find a review in "My Reviews" section
2. Click "Delete" button
3. Confirm deletion in dialog

**Expected Result:**
- Review is deleted
- Success message displayed
- Review no longer appears in "My Reviews"
- Database record is removed

#### Test Case B10: Delete Review - Confirmation
**Steps:**
1. Click "Delete" on a review
2. Cancel the confirmation dialog

**Expected Result:**
- Review is NOT deleted
- Dialog closes
- Review still visible

---

### C. JOB SEEKER DASHBOARD TESTING

#### Test Case C1: Dashboard Display
**Prerequisites:** Logged in as job seeker

**Steps:**
1. Navigate to job seeker dashboard
2. Verify page elements

**Expected Result:**
- Hero section with search bar visible
- Filter section with:
  - Job Role dropdown
  - Minimum Rating dropdown
  - Reset Filters button
- "Browse Companies" section with company cards
- "Latest Reviews" section with review cards

#### Test Case C2: Search Companies
**Steps:**
1. Type "Google" in search bar
2. Click "Search"

**Expected Result:**
- Shows only companies matching "Google"
- Company cards display:
  - Company name
  - Number of reviews
  - Average rating
- Can click to view details

#### Test Case C3: Search - No Results
**Steps:**
1. Search for non-existent company: "ZZZCompany123"
2. Click "Search"

**Expected Result:**
- Message: "No companies found"
- Company grid is empty

#### Test Case C4: View Company Details
**Steps:**
1. Click on any company card
2. Modal opens showing company details

**Expected Result:**
- Modal displays:
  - Company name
  - Average rating
  - Total reviews count
  - Ratings by role
  - List of reviews
- Can read full reviews from modal
- Modal has close button

#### Test Case C5: Filter by Job Role
**Steps:**
1. Select "Software Developer (SDE)" from role dropdown
2. Filter applies automatically

**Expected Result:**
- Reviews filtered to show only SDE reviews
- Reviews from other roles hidden
- Review count may decrease

#### Test Case C6: Filter by Minimum Rating
**Steps:**
1. Select "⭐⭐⭐⭐ and above" minimum rating
2. Filter applies

**Expected Result:**
- Shows only reviews with 4 or 5 stars
- Reviews below threshold hidden
- Search bar updates

#### Test Case C7: Combine Filters
**Steps:**
1. Select Job Role: "HR"
2. Select Min Rating: "⭐⭐⭐ and above"
3. Both filters apply

**Expected Result:**
- Shows only HR reviews with 3+ stars
- Other reviews hidden
- Clear filtering logic works

#### Test Case C8: Reset Filters
**Steps:**
1. Apply some filters
2. Click "Reset Filters"

**Expected Result:**
- All filters cleared
- Shows all reviews again
- Dropdowns reset to default

#### Test Case C9: Read Full Review
**Steps:**
1. In review card, click "Read Full Review"
2. View modal opens

**Expected Result:**
- Full review displayed with:
  - Title
  - Company name
  - Rating
  - Full feedback text
  - Pros and Cons (if available)
  - Author info (generic - doesn't show employee name)
  - Date

#### Test Case C10: Cannot Edit as Job Seeker
**Steps:**
1. Logged in as job seeker
2. Try to find "Edit" or "Delete" buttons on reviews

**Expected Result:**
- No edit/delete buttons visible
- Only "Read Full Review" button available
- Read-only access confirmed

---

### D. ROLE-BASED ACCESS TESTING

#### Test Case D1: Job Seeker Cannot Access Employee Features
**Steps:**
1. Logged in as job seeker
2. Try to manually navigate to `/employee-dashboard`
3. Or try to access review creation API

**Expected Result:**
- Redirect to `/user-dashboard`
- Cannot access employee features
- Access denied for API endpoints

#### Test Case D2: Employee Cannot Access as Job Seeker
**Steps:**
1. Logged in as employee
2. Try to navigate to `/user-dashboard`

**Expected Result:**
- Redirect to `/employee-dashboard`
- Cannot switch to seeker view

#### Test Case D3: Unauthenticated Access
**Steps:**
1. Not logged in
2. Try to access `/employee-dashboard` or `/user-dashboard` directly

**Expected Result:**
- Redirect to login page
- Cannot access protected pages

---

### E. RESPONSIVE DESIGN TESTING

#### Test Case E1: Desktop View (1920px+)
**Steps:**
1. Open browser to full 1920px width
2. Navigate dashboard

**Expected Result:**
- Multi-column layouts display correctly
- Company cards in 3-4 columns
- All elements properly spaced
- Navigation bar displays horizontally

#### Test Case E2: Tablet View (768px-1024px)
**Steps:**
1. Resize browser to 850px width
2. Test navigation and forms

**Expected Result:**
- Single/dual column layouts
- Company cards in 2 columns
- Navigation adapts for smaller screen
- Forms remain usable

#### Test Case E3: Mobile View (320px-480px)
**Steps:**
1. Resize browser to 400px width
2. Test all functionality

**Expected Result:**
- Single column layout
- Company cards full width
- Vertical navigation
- Forms stack properly
- Touch-friendly button sizes
- All features functional

#### Test Case E4: Mobile Navigation
**Steps:**
1. On mobile (400px), click hamburger menu
2. Test navigation links

**Expected Result:**
- Navigation menu toggles
- Links are easily clickable
- Menu closes on selection

---

### F. DATA VALIDATION TESTING

#### Test Case F1: Long Text Input
**Steps:**
1. Enter very long feedback (10000+ characters)
2. Submit review

**Expected Result:**
- Either truncated or accepted
- No database errors
- Form handles gracefully

#### Test Case F2: Special Characters
**Steps:**
1. Enter special characters in review: `<script>alert('xss')</script>`
2. Submit

**Expected Result:**
- Text escaped/sanitized
- No XSS vulnerability
- Text displays as literal string

#### Test Case F3: SQL/Injection Attempts
**Steps:**
1. Try MongoDB injection in search: `{$ne: null}`
2. Enter in company search

**Expected Result:**
- Injection prevented
- Literal text searched
- No security breach

---

### G. DATABASE TESTING

#### Test Case G1: Data Persistence
**Steps:**
1. Create a review as employee
2. Close browser completely
3. Reopen and login
4. Check if review still exists

**Expected Result:**
- Review persists in database
- Data is NOT lost on page refresh
- Database queries work correctly

#### Test Case G2: Multiple User Sessions
**Steps:**
1. Open app in 2 browser windows
2. Login as different users
3. Create reviews in both
4. Check both accounts

**Expected Result:**
- Each session is independent
- Reviews appear only for correct user
- No data mixing between sessions

#### Test Case G3: Concurrent Operations
**Steps:**
1. Submit review in Window 1
2. Search companies in Window 2 simultaneously
3. Check both operations complete

**Expected Result:**
- Both operations succeed
- No conflicts
- Database handles concurrency

---

### H. LOGOUT AND SESSION TESTING

#### Test Case H1: Logout Functionality
**Steps:**
1. Logged in as any user
2. Click "Logout"

**Expected Result:**
- Session cleared
- Redirected to login page
- User cannot access dashboards

#### Test Case H2: Session Expiry
**Steps:**
1. Login
2. Close browser
3. Manually clear cookies
4. Try accessing dashboard

**Expected Result:**
- Redirect to login page
- Session is invalid
- Must login again

#### Test Case H3: Back Button After Logout
**Steps:**
1. Login to account
2. Logout
3. Click browser back button

**Expected Result:**
- Cannot access previous protected page
- Must login again
- Session doesn't resurrect

---

### I. ERROR HANDLING TESTING

#### Test Case I1: Database Connection Error
**Steps:**
1. Stop MongoDB service
2. Try to perform database operation
3. Check error handling

**Expected Result:**
- Error message displays
- Application doesn't crash
- Graceful error page shown

#### Test Case I2: Invalid Form Submission
**Steps:**
1. Open browser console
2. Modify form to submit invalid data
3. Submit

**Expected Result:**
- Server validation catches error
- Error message returned
- Form not processed

#### Test Case I3: File Upload Error
**Steps:**
1. Try to upload file exceeding 16MB
2. Or non-permitted file type

**Expected Result:**
- Error message: "File too large" or "Invalid type"
- File not uploaded
- System handles gracefully

---

### J. VISUAL AND UX TESTING

#### Test Case J1: Loading States
**Steps:**
1. Submit a form
2. Observe loading state

**Expected Result:**
- Button shows loading animation
- Button is disabled during submission
- Prevents double submission

#### Test Case J2: Error Messages
**Steps:**
1. Trigger various errors
2. Check message visibility

**Expected Result:**
- Error message is red/noticeable
- Auto-hides after 5 seconds
- Clear, actionable messages

#### Test Case J3: Success Messages
**Steps:**
1. Complete successful actions
2. Observe success messages

**Expected Result:**
- Success message is green
- Message is clear and confirms action
- Auto-hides after 5 seconds

#### Test Case J4: Form Reset
**Steps:**
1. Fill form with data
2. Click form's reset button or successful submission

**Expected Result:**
- Form fields cleared
- Ready for new input
- No stale data

---

## Test Data Checklist

- ✅ Multiple users created
- ✅ Reviews from different roles
- ✅ Various rating levels (1-5)
- ✅ Long and short feedback texts
- ✅ Reviews from previous companies
- ✅ Multiple companies in database
- ✅ Search covers various scenarios
- ✅ Filter combinations tested

## Performance Testing

### Load Test
```
Scenario: 100 job seekers viewing reviews simultaneously
Expected: Page loads in < 2 seconds
Expected: No database timeouts
```

### Search Performance
```
Scenario: Search across 1000+ reviews
Expected: Results return in < 1 second
Expected: Indexes being used effectively
```

---

## Sign-Off

After completing all tests, complete this checklist:

- [ ] Authentication works (login/register)
- [ ] Employee can create reviews
- [ ] Employee can edit/delete reviews
- [ ] Employee can add previous companies
- [ ] Job seeker can search companies
- [ ] Job seeker can filter reviews
- [ ] Job seeker has read-only access
- [ ] Role-based access works
- [ ] Responsive design works (3 breakpoints)
- [ ] Data persists in database
- [ ] Error handling works
- [ ] Messages display correctly
- [ ] No console errors
- [ ] No security vulnerabilities found

## Test Result Summary

| Component | Status | Notes |
|-----------|--------|-------|
| Registration | PASS/FAIL | |
| Login | PASS/FAIL | |
| Employee Dashboard | PASS/FAIL | |
| Review Creation | PASS/FAIL | |
| Job Seeker Dashboard | PASS/FAIL | |
| Search & Filter | PASS/FAIL | |
| Role Access | PASS/FAIL | |
| Responsive Design | PASS/FAIL | |
| Database | PASS/FAIL | |
| Security | PASS/FAIL | |

---

## Reporting Issues

When reporting bugs:
1. Document steps to reproduce
2. Include browser/OS information
3. Attach screenshots if applicable
4. Check browser console for errors
5. Include any error messages
6. State expected vs actual behavior

---

**Test Environment:** Windows 10/11 or Linux or macOS
**Browser:** Chrome, Firefox, Safari (latest versions)
**Database:** MongoDB 5.0+
**Python:** 3.7+

Happy Testing! 🧪
