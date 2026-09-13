from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import json
from functools import wraps
from bson.objectid import ObjectId
from database import Database
import secrets

app = Flask(__name__)
# load configuration from config.py based on FLASK_ENV
from config import get_config
app.config.from_object(get_config())

# secret key may come from env or config
app.secret_key = app.config.get('SECRET_KEY') or secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = app.config.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024)
app.config['UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER', 'static/uploads')
ALLOWED_EXTENSIONS = app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'})

db = Database(app.config.get('MONGODB_URI'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = db.get_user(session['user_id'])
        if user['user_type'] != 'employee':
            return jsonify({'error': 'Only employees can access this'}), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = db.get_user(session['user_id'])
        if user['user_type'] != 'admin':
            return jsonify({'error': 'Admin only'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        user = db.get_user(session['user_id'])
        if user['user_type'] == 'employee':
            return redirect(url_for('employee_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        user_type = data.get('user_type', 'jobseeker').strip()
        company = data.get('company', '').strip()
        job_role = data.get('job_role', '').strip()
        
        if not all([email, password, name]):
            return jsonify({'error': 'Please fill all required fields'}), 400
        
        if db.user_exists(email):
            return jsonify({'error': 'Email already registered'}), 400
        
        if user_type == 'employee':
            if not company or not job_role:
                return jsonify({'error': 'Employees must provide company and job role'}), 400
        
        user_data = {
            'email': email,
            'password': generate_password_hash(password),
            'name': name,
            'user_type': user_type,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        if user_type == 'employee':
            user_data['company'] = company
            user_data['job_role'] = job_role
            user_data['verified'] = False
            user_data['previous_companies'] = []
        
        user_id = db.create_user(user_data)
        # Ensure the company exists in companies collection so employees can review it
        if user_type == 'employee' and company:
            try:
                db.get_or_create_company(company)
            except Exception:
                # non-fatal: continue even if company creation fails
                pass
        
        if request.is_json:
            return jsonify({'success': True, 'user_id': str(user_id)}), 201
        
        session['user_id'] = str(user_id)
        if user_type == 'employee':
            return redirect(url_for('employee_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = db.get_user_by_email(email)
        
        if not user or not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        session['user_id'] = str(user['_id'])
        session['user_type'] = user['user_type']
        session['name'] = user['name']
        
        if request.is_json:
            return jsonify({
                'success': True,
                'user_type': user['user_type'],
                'redirect': url_for('employee_dashboard') if user['user_type'] == 'employee' else url_for('user_dashboard')
            }), 200
        
        if user['user_type'] == 'employee':
            return redirect(url_for('employee_dashboard'))
        return redirect(url_for('user_dashboard'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/employee-dashboard')
@login_required
def employee_dashboard():
    user = db.get_user(session['user_id'])
    if user['user_type'] != 'employee':
        return redirect(url_for('user_dashboard'))
    
    reviews = db.get_user_reviews(session['user_id'])
    companies = db.get_all_companies()
    
    return render_template('employee_dashboard.html', 
                         user=user, 
                         reviews=reviews,
                         total_reviews=len(reviews),
                         companies=companies)

@app.route('/user-dashboard')
@login_required
def user_dashboard():
    user = db.get_user(session['user_id'])
    if user['user_type'] != 'jobseeker':
        return redirect(url_for('employee_dashboard'))
    
    companies = db.get_all_companies()
    reviews = db.get_all_reviews()
    
    return render_template('user_dashboard.html',
                         user=user,
                         companies=companies,
                         reviews=reviews)

@app.route('/api/companies', methods=['GET', 'POST'])
def manage_companies():
    if request.method == 'GET':
        search = request.args.get('search', '').strip()
        role_filter = request.args.get('role', '').strip()
        companies = db.get_all_companies()
        
        if search:
            companies = [c for c in companies if search.lower() in c['name'].lower()]
        
        companies_list = []
        for company in companies:
            reviews = db.get_company_reviews(str(company['_id']))
            # apply role filter on the backend if provided
            if role_filter:
                reviews = [r for r in reviews if r.get('job_role', '').lower() == role_filter.lower()]
            avg_rating = sum(r['rating'] for r in reviews) / len(reviews) if reviews else 0
            companies_list.append({
                '_id': str(company['_id']),
                'name': company['name'],
                'average_rating': round(avg_rating, 2),
                'review_count': len(reviews)
            })
        
        return jsonify(companies_list), 200
    
    return jsonify({'error': 'Method not allowed'}), 405

@app.route('/api/add-company', methods=['POST'])
@employee_required
def add_company():
    data = request.get_json()
    company_name = data.get('company_name', '').strip()
    
    if not company_name:
        return jsonify({'error': 'Company name required'}), 400
    
    if db.company_exists(company_name):
        return jsonify({'success': True, 'message': 'Company already exists'}), 200
    
    company_id = db.create_company({
        'name': company_name,
        'created_at': datetime.now()
    })
    
    return jsonify({'success': True, 'company_id': str(company_id)}), 201

@app.route('/api/company/<company_id>')
def get_company_details(company_id):
    try:
        company = db.get_company(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404
        
        reviews = db.get_company_reviews(company_id)
        ratings_by_role = {}
        
        for review in reviews:
            role = review.get('job_role', 'Unknown')
            if role not in ratings_by_role:
                ratings_by_role[role] = []
            ratings_by_role[role].append(review['rating'])
        
        role_ratings = {}
        for role, ratings in ratings_by_role.items():
            role_ratings[role] = {
                'average': round(sum(ratings) / len(ratings), 2),
                'count': len(ratings)
            }
        
        return jsonify({
            'name': company['name'],
            'reviews': len(reviews),
            'average_rating': round(sum(r['rating'] for r in reviews) / len(reviews), 2) if reviews else 0,
            'role_ratings': role_ratings
        }), 200
    
    except:
        return jsonify({'error': 'Invalid company ID'}), 400

@app.route('/api/company/<company_id>/reviews')
def get_company_reviews_api(company_id):
    try:
        reviews = db.get_company_reviews(company_id)
        reviews_list = []
        
        for review in reviews:
            user = db.get_user(review['user_id'])
            reviews_list.append({
                'id': str(review['_id']),
                'author': user['name'],
                'job_role': review['job_role'],
                'how_got': review.get('how_got', ''),
                'rating': review['rating'],
                'title': review['title'],
                'feedback': review['feedback'],
                'created_at': review['created_at'].strftime('%Y-%m-%d'),
                'pros': review.get('pros', ''),
                'cons': review.get('cons', ''),
                'interview_difficulty': review.get('interview_difficulty', ''),
                'interview_rounds': review.get('interview_rounds', ''),
                'technical_questions': review.get('technical_questions', ''),
                'hr_experience': review.get('hr_experience', ''),
                'tips': review.get('tips', ''),
                'salary_range': review.get('salary_range', ''),
                'years_experience': review.get('years_experience', ''),
                'location': review.get('location', '')
            })
        
        return jsonify(reviews_list), 200
    
    except:
        return jsonify({'error': 'Invalid company ID'}), 400

@app.route('/api/create-review', methods=['POST'])
@employee_required
def create_review():
    user_id = session.get('user_id')
    user = db.get_user(user_id)
    
    data = request.get_json()
    
    company_id = data.get('company_id', '').strip()
    try:
        rating = int(data.get('rating', 0))
    except Exception:
        rating = 0
    title = data.get('title', '').strip()
    feedback = data.get('feedback', '').strip()
    pros = data.get('pros', '').strip()
    cons = data.get('cons', '').strip()
    job_role = data.get('job_role', '').strip()
    how_got = data.get('how_got', '').strip()
    # interview related optional fields
    interview_difficulty = data.get('interview_difficulty', '').strip()
    interview_rounds = data.get('interview_rounds', '').strip()
    technical_questions = data.get('technical_questions', '').strip()
    hr_experience = data.get('hr_experience', '').strip()
    tips = data.get('tips', '').strip()
    salary_range = data.get('salary_range', '').strip()
    years_experience = data.get('years_experience', '').strip()
    location = data.get('location', '').strip()
    is_previous = data.get('is_previous', False)
    
    # Require how_got as part of review metadata linking
    if not all([company_id, rating, title, feedback, job_role, how_got]):
        return jsonify({'error': 'All fields required (including how you got the job)'}), 400
    
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    
    if not db.company_exists_by_id(company_id):
        return jsonify({'error': 'Company not found'}), 404
    # No ownership/approval checks: allow employees to submit reviews
    # for any company (previous or current) without admin verification.
    
    review_data = {
        'user_id': user_id,
        'company_id': company_id,
        'job_role': job_role,
        'how_got': how_got,
        'rating': rating,
        'title': title,
        'feedback': feedback,
        'pros': pros,
        'cons': cons,
        'is_previous': is_previous,
        # store interview details even if empty so fields exist
        'interview_difficulty': interview_difficulty,
        'interview_rounds': interview_rounds,
        'technical_questions': technical_questions,
        'hr_experience': hr_experience,
        'tips': tips,
        'salary_range': salary_range,
        'years_experience': years_experience,
        'location': location,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }
    
    review_id = db.create_review(review_data)
    
    return jsonify({'success': True, 'review_id': str(review_id)}), 201

@app.route('/api/update-review/<review_id>', methods=['PUT'])
@employee_required
def update_review(review_id):
    user_id = session.get('user_id')
    
    review = db.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    if review['user_id'] != user_id:
        return jsonify({'error': 'You can only edit your own reviews'}), 403
    
    data = request.get_json()
    
    update_data = {
        'updated_at': datetime.now()
    }
    
    if 'rating' in data:
        update_data['rating'] = int(data['rating'])
    if 'title' in data:
        update_data['title'] = data['title'].strip()
    if 'feedback' in data:
        update_data['feedback'] = data['feedback'].strip()
    if 'pros' in data:
        update_data['pros'] = data['pros'].strip()
    if 'cons' in data:
        update_data['cons'] = data['cons'].strip()
    if 'how_got' in data:
        update_data['how_got'] = data['how_got'].strip()
    # interview-related fields can also be updated
    if 'interview_difficulty' in data:
        update_data['interview_difficulty'] = data['interview_difficulty'].strip()
    if 'interview_rounds' in data:
        update_data['interview_rounds'] = data['interview_rounds'].strip()
    if 'technical_questions' in data:
        update_data['technical_questions'] = data['technical_questions'].strip()
    if 'hr_experience' in data:
        update_data['hr_experience'] = data['hr_experience'].strip()
    if 'tips' in data:
        update_data['tips'] = data['tips'].strip()
    if 'salary_range' in data:
        update_data['salary_range'] = data['salary_range'].strip()
    if 'years_experience' in data:
        update_data['years_experience'] = data['years_experience'].strip()
    if 'location' in data:
        update_data['location'] = data['location'].strip()
    
    db.update_review(review_id, update_data)
    
    return jsonify({'success': True}), 200

@app.route('/api/delete-review/<review_id>', methods=['DELETE'])
@employee_required
def delete_review(review_id):
    user_id = session.get('user_id')
    
    review = db.get_review(review_id)
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    
    if review['user_id'] != user_id:
        return jsonify({'error': 'You can only delete your own reviews'}), 403
    
    db.delete_review(review_id)
    
    return jsonify({'success': True}), 200

@app.route('/api/add-previous-company', methods=['POST'])
@employee_required
def add_previous_company():
    user_id = session.get('user_id')
    # Use form data (multipart/form-data) because this endpoint expects a file upload
    company_name = request.form.get('company_name', '').strip()
    job_role = request.form.get('job_role', '').strip()
    
    if not company_name or not job_role:
        return jsonify({'error': 'Company name and job role required'}), 400
    
    # Check if file uploaded
    if 'document' not in request.files:
        return jsonify({'error': 'Document required for previous company'}), 400

    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    filename = secure_filename(f"{user_id}_{datetime.now().timestamp()}_{file.filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({'error': 'Failed to save document'}), 500

    company_id = db.get_or_create_company(company_name)

    db.add_previous_company(user_id, str(company_id), company_name, job_role, filename)

    return jsonify({'success': True, 'company_id': str(company_id)}), 201


# --- Admin routes ----------------------------------------------------------
@app.route('/admin/pending-previous')
@admin_required
def view_pending_previous():
    pending = db.get_pending_previous_companies()
    return jsonify(pending), 200

@app.route('/admin')
@admin_required
def admin_dashboard():
    return render_template('admin.html')

@app.route('/admin/approve-previous/<user_id>/<company_id>', methods=['POST'])
@admin_required
def approve_previous(user_id, company_id):
    result = db.approve_previous_company(user_id, company_id)
    if result and getattr(result, 'modified_count', 0) > 0:
        return jsonify({'success': True}), 200
    return jsonify({'error': 'Approval failed or already approved'}), 400

@app.route('/api/search-reviews', methods=['GET'])
def search_reviews():
    company_id = request.args.get('company_id', '').strip()
    job_role = request.args.get('role', '').strip()
    min_rating = int(request.args.get('min_rating', 1))
    
    reviews = db.get_all_reviews()
    
    if company_id:
        reviews = [r for r in reviews if r['company_id'] == company_id]
    
    if job_role:
        reviews = [r for r in reviews if r['job_role'].lower() == job_role.lower()]
    
    if min_rating > 1:
        reviews = [r for r in reviews if r['rating'] >= min_rating]
    
    reviews_list = []
    for review in reviews:
        user = db.get_user(review['user_id'])
        company = db.get_company(review['company_id'])
        
        reviews_list.append({
            'id': str(review['_id']),
            'company': company['name'],
            'author': user['name'],
            'job_role': review['job_role'],
            'how_got': review.get('how_got', ''),
            'rating': review['rating'],
            'title': review['title'],
            'feedback': review['feedback'],
            'pros': review.get('pros', ''),
            'cons': review.get('cons', ''),
            'created_at': review['created_at'].strftime('%Y-%m-%d'),
            'interview_difficulty': review.get('interview_difficulty', ''),
            'interview_rounds': review.get('interview_rounds', ''),
            'technical_questions': review.get('technical_questions', ''),
            'hr_experience': review.get('hr_experience', ''),
            'tips': review.get('tips', ''),
            'salary_range': review.get('salary_range', ''),
            'years_experience': review.get('years_experience', ''),
            'location': review.get('location', '')
        })
    
    return jsonify(reviews_list), 200

@app.route('/api/user/<user_id>')
def get_user_profile(user_id):
    user = db.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    if user['user_type'] == 'employee':
        reviews = db.get_user_reviews(user_id)
        return jsonify({
            'name': user['name'],
            'email': user['email'],
            'job_role': user.get('job_role', ''),
            'company': user.get('company', ''),
            'review_count': len(reviews),
            'user_type': 'employee'
        }), 200
    
    return jsonify({
        'name': user['name'],
        'email': user['email'],
        'user_type': 'jobseeker'
    }), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(
        debug=app.config.get('DEBUG', False),
        host=app.config.get('APP_HOST', '127.0.0.1'),
        port=app.config.get('APP_PORT', 5000)
    )
