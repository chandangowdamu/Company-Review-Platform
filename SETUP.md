# Complete Setup Guide - Company and College Review Platform

## Prerequisites
Before you start, make sure you have the following installed:
- **Python 3.7+** - [Download here](https://www.python.org/downloads/)
- **MongoDB** - [Download here](https://www.mongodb.com/try/download/community)
- **Git** (optional) - [Download here](https://git-scm.com/)

## Step-by-Step Installation

### Step 1: Extract the Project
```bash
# Extract the project folder to your desired location
# Or if cloned from git:
cd ABBS\ Main\ 1111
```

### Step 2: Verify Python Installation
```bash
python --version
# Output should be Python 3.7 or higher
```

### Step 3: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

After activation, you should see `(venv)` at the beginning of your terminal prompt.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- pymongo (MongoDB driver)
- werkzeug (security utilities)

### Step 5: Set Up MongoDB

#### Option A: Local MongoDB (Recommended for Development)
1. **Download MongoDB Community Edition**
   - Go to https://www.mongodb.com/try/download/community
   - Select your operating system
   - Download and install

2. **Start MongoDB**
   - **Windows**: 
     ```bash
     # Run MongoDB service (if installed with setup wizard)
     # Or start mongod.exe from installation directory
     MongoDB_Installation_Path\bin\mongod.exe
     ```
   
   - **macOS** (with Homebrew):
     ```bash
     brew services start mongodb/brew/mongodb-community
     ```
   
   - **Linux**:
     ```bash
     sudo service mongod start
     ```

#### Option B: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a cluster
4. Get connection string
5. Update `database.py`:
   ```python
   self.client = MongoClient('your_atlas_connection_string')
   ```

### Step 6: Verify MongoDB Connection
```bash
# Try connecting to MongoDB
mongosh  # or 'mongo' for older versions
# or
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/')"
```

### Step 7: Run the Application

```bash
# Make sure you're in the project directory and venv is activated
python app.py
```

You should see output like:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 8: Access the Application
Open your web browser and go to: **http://127.0.0.1:5000**

## Feature Walkthrough

### Test Employee Features
1. Go to **Register**
2. Select **Employee**
3. Fill in details:
   - Name: John Doe
   - Email: john@example.com
   - Password: password123
   - Company: Google
   - Job Role: Software Developer (SDE)
4. Click **Create Account**
5. You're now on the Employee Dashboard

### Write Your First Review
1. Fill in the review form with:
   - Rating: 5 stars
   - Title: Great company to work for
   - Feedback: Detailed experience...
   - Pros: Good work culture
   - Cons: Long working hours
2. Click **Submit Review**

### Add a Previous Company
1. Go to **Previous Company** tab
2. Enter company name and role
3. Upload a document (any PDF, JPG, etc.)
4. Now you can write reviews for that company too

### Test Job Seeker Features
1. **Logout** from employee account
2. Go to **Register** again
3. Select **Job Seeker**
4. Fill in basic details and create account
5. You can now:
   - Search for companies
   - Read reviews
   - Filter by role and rating
   - Cannot create/edit reviews

## Common Issues & Solutions

### Issue: "Connection refused" MongoDB error
**Solution:**
- Ensure MongoDB is running
- Check if port 27017 is being used by another service
- Verify MongoDB installation

### Issue: Port 5000 already in use
**Solution:**
```bash
# Change port in app.py
app.run(debug=True, host='127.0.0.1', port=5001)
# Then access at http://127.0.0.1:5001
```

### Issue: Module not found errors
**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt
```

### Issue: Database not created
**Solution:**
- MongoDB automatically creates databases on first use
- Just run the app and it will create the necessary collections

### Issue: Can't upload files
**Solution:**
- Ensure `static/uploads` directory exists
- Change file permissions if needed
- Check file size limit (16MB max)

## File Organization

```
ABBS Main 1111/
├── app.py                          # Main application file
├── database.py                     # Database operations
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                        # Main documentation
├── SETUP.md                         # This setup guide
├── templates/                      # HTML files
│   ├── login.html
│   ├── register.html
│   ├── employee_dashboard.html
│   ├── user_dashboard.html
│   ├── 404.html
│   └── 500.html
└── static/                         # Static files
    ├── css/
    │   ├── auth.css               # Login/Register styles
    │   └── style.css              # Dashboard styles
    ├── js/                        # JavaScript (expandable)
    └── uploads/                   # File storage directory
```

## Development Tips

### Enable Debug Mode
The app runs in debug mode by default. This means:
- Automatic reload on code changes
- Detailed error messages
- Interactive debugger

### Check Database
```bash
# Open MongoDB shell
mongosh

# List databases
show dbs

# Use review_platform database
use review_platform

# List collections
show collections

# View users
db.users.find()

# View reviews
db.reviews.find()

# View companies
db.companies.find()
```

### Test API Endpoints
You can test API endpoints using:
- **Postman** - [Download here](https://www.postman.com/)
- **curl** command line:
  ```bash
  curl http://127.0.0.1:5000/api/companies
  ```

## Database Backup

### Backup MongoDB Data
```bash
mongodump --out /path/to/backup/
```

### Restore MongoDB Data
```bash
mongorestore /path/to/backup/
```

## Deployment (Optional)

To deploy to production:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Use MongoDB Atlas instead of local MongoDB
3. Set `FLASK_ENV=production`
4. Use a reverse proxy (Nginx, Apache)
5. Enable HTTPS with SSL certificates

## Environment Variables (Optional)

Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Then modify `database.py` to use these variables:
```python
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self, uri=os.getenv('MONGODB_URI')):
        # ... rest of code
```

## Performance Optimization

The application includes:
- Database indexing for faster queries
- CSS minification ready
- Efficient database queries
- Session-based caching

## Security Checklist

- ✅ Password hashing implemented
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ File upload validation
- ✅ Input validation on all forms
- ✅ SQL injection prevention (using MongoDB)

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Guide](https://pymongo.readthedocs.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/security/)

## Getting Help

1. Check the README.md for general information
2. Review error messages carefully
3. Check browser console (F12) for JavaScript errors
4. Check Flask terminal output for backend errors
5. Verify MongoDB is running and accessible

## Next Steps

After setup:
1. Test employee and job seeker flows
2. Create sample data
3. Customize styling if needed
4. Add more job roles from database
5. Implement additional features as needed

---

Happy coding! 🚀

For issues or questions, refer to the README.md or troubleshooting section above.
