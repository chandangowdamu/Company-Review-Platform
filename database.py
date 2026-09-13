from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

class Database:
    def __init__(self, uri='mongodb://localhost:27017/'):
        try:
            self.client = MongoClient(uri)
            self.db = self.client['review_platform']
            
            # Create collections if they don't exist
            if 'users' not in self.db.list_collection_names():
                self.db.create_collection('users')
            if 'companies' not in self.db.list_collection_names():
                self.db.create_collection('companies')
            if 'reviews' not in self.db.list_collection_names():
                self.db.create_collection('reviews')
            
            # Create indexes
            self.db.users.create_index('email', unique=True)
            self.db.companies.create_index('name', unique=True)
            self.db.reviews.create_index('company_id')
            self.db.reviews.create_index('user_id')
            
            print("Database connection successful")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise
    
    # User operations
    def create_user(self, user_data):
        result = self.db.users.insert_one(user_data)
        return result.inserted_id
    
    def get_user(self, user_id):
        try:
            return self.db.users.find_one({'_id': ObjectId(user_id)})
        except:
            return None
    
    def get_user_by_email(self, email):
        return self.db.users.find_one({'email': email})
    
    def user_exists(self, email):
        return self.db.users.find_one({'email': email}) is not None
    
    def update_user(self, user_id, update_data):
        return self.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
    
    def add_previous_company(self, user_id, company_id, company_name, job_role, document_path):
        # Add company directly without needing admin approval
        return self.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$push': {
                'previous_companies': {
                    'company_id': company_id,
                    'company_name': company_name,
                    'job_role': job_role,
                    'document': document_path,
                    'approved': True,
                    'added_at': datetime.now()
                }
            }}
        )

    def get_pending_previous_companies(self):
        # returns list of {user_id, company} entries pending approval
        pipeline = [
            {'$unwind': '$previous_companies'},
            {'$match': {'previous_companies.approved': False}},
            {'$project': {
                'user_id': '$_id',
                'user_name': '$name',
                'email': '$email',
                'company': '$previous_companies'
            }}
        ]
        return list(self.db.users.aggregate(pipeline))

    def approve_previous_company(self, user_id, company_id):
        return self.db.users.update_one(
            {'_id': ObjectId(user_id), 'previous_companies.company_id': company_id},
            {'$set': {'previous_companies.$.approved': True}}
        )
    
    # Company operations
    def create_company(self, company_data):
        result = self.db.companies.insert_one(company_data)
        return result.inserted_id
    
    def get_company(self, company_id):
        try:
            return self.db.companies.find_one({'_id': ObjectId(company_id)})
        except:
            return None
    
    def get_all_companies(self):
        return list(self.db.companies.find().sort('name', 1))
    
    def company_exists(self, company_name):
        return self.db.companies.find_one({'name': company_name}) is not None
    
    def company_exists_by_id(self, company_id):
        try:
            return self.db.companies.find_one({'_id': ObjectId(company_id)}) is not None
        except:
            return False
    
    def get_or_create_company(self, company_name):
        company = self.db.companies.find_one({'name': company_name})
        if company:
            return company['_id']
        else:
            return self.create_company({'name': company_name, 'created_at': datetime.now()})
    
    # Review operations
    def create_review(self, review_data):
        result = self.db.reviews.insert_one(review_data)
        return result.inserted_id
    
    def get_review(self, review_id):
        try:
            return self.db.reviews.find_one({'_id': ObjectId(review_id)})
        except:
            return None
    
    def get_all_reviews(self):
        return list(self.db.reviews.find().sort('created_at', -1))
    
    def get_company_reviews(self, company_id):
        try:
            return list(self.db.reviews.find(
                {'company_id': company_id}
            ).sort('created_at', -1))
        except:
            return []
    
    def get_user_reviews(self, user_id):
        return list(self.db.reviews.find({'user_id': user_id}).sort('created_at', -1))
    
    def update_review(self, review_id, update_data):
        try:
            return self.db.reviews.update_one(
                {'_id': ObjectId(review_id)},
                {'$set': update_data}
            )
        except:
            return None
    
    def delete_review(self, review_id):
        try:
            return self.db.reviews.delete_one({'_id': ObjectId(review_id)})
        except:
            return None
    
    def get_reviews_by_role(self, company_id, job_role):
        try:
            return list(self.db.reviews.find({
                'company_id': company_id,
                'job_role': job_role
            }).sort('created_at', -1))
        except:
            return []
    
    def close(self):
        self.client.close()
