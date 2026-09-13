<<<<<<< HEAD
# Company Review Platform

A Flask-based web app where employees can leave company reviews and job seekers can read them to make informed career decisions.

## Overview

This project allows:
- Employees to register with their current company and job role
- Employees to write, edit, and delete reviews
- Job seekers to browse company ratings and reviews
- Users to add previous-company proof documents and review those companies later
- Admins to approve previous-company submissions

## Tech Stack

- Python 3
- Flask
- MongoDB
- HTML, CSS, JavaScript

## Project Structure

- `app.py` — Flask app and routes
- `database.py` — MongoDB access layer
- `config.py` — app configuration
- `templates/` — HTML pages
- `static/` — CSS, JS, uploads
- `requirements.txt` — Python dependencies

## Prerequisites

- Python 3.9+
- MongoDB running locally on `mongodb://localhost:27017`
- A terminal or command prompt

## Setup

1. Open a terminal in the project folder.
2. Create and activate a virtual environment:

   Windows:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start MongoDB locally.
   - If `mongod` is installed, run:
   ```bash
   mongod
   ```
   - Or use your existing MongoDB instance and set `MONGODB_URI` as needed in `config.py` or your environment.

5. Start the app:
   ```bash
   python app.py
   ```

6. Open:
   ```text
   http://127.0.0.1:5000
   ```

## Main Features

### Employee features
- Register as an employee
- Submit reviews for current and previous companies
- Add proof documents for previous employers
- Edit and remove personal reviews
- View personal dashboard

### Job seeker features
- Browse company data
- Search and filter reviews by role and rating
- Read detailed company feedback

### Admin features
- View pending previous-company approvals
- Approve submitted documents
- Allow employees to review approved companies

## Default Login Flow

- Register a user from the app UI
- For employee accounts, provide a company and job role
- After login, the app redirects to the relevant dashboard

## Notes

- The app stores files in `static/uploads/`
- The default database name is `review_platform`
- If MongoDB is not running, the app will not start correctly

## Run script

On Windows you can also use:
```powershell
run.bat
```


### Reviews Collection
```json
{
    "_id": ObjectId,
    "user_id": ObjectId,
    "company_id": ObjectId,
    "job_role": String,
    "rating": Integer (1-5),
    "title": String,
    "feedback": String,
    "pros": String,
    "cons": String,
    "is_previous": Boolean,
    "created_at": DateTime,
    "updated_at": DateTime
}
```

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check the connection string in `database.py`
- Verify the database name is correct

### Port Already in Use
- Flask runs on port 5000 by default
- Change port in `app.py`: `app.run(port=5001)`

### File Upload Issues
- Check that `/static/uploads` directory exists
- Verify file size is under 16MB
- Ensure file type is allowed

## Future Enhancements

- Email verification for users
- Company admin dashboard
- Review moderation system
- Advanced analytics and statistics
- Mobile app version
- Salary data integration
- Interview experience sharing

## License

This project is for educational purposes.

## Support

For issues or questions, please contact the development team.

---

**Happy reviewing! Help job seekers make better career decisions.** 🚀
=======
# Company-Review-Platform 
>>>>>>> ac843bc30914e406497862620f65afd7d18fe3f2
