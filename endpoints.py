#!/usr/bin/env python3
"""Restful api."""

from flask import Flask, jsonify, request
from flask_cors import CORS
from jwtfunc import generate_token, token_required
from db_operations import *


"""Creating an instance of a flask class."""
app = Flask(__name__)
CORS(app)


"""Route handler for the root URL."""
@app.route('/')
def index():
    """
    Endpoint for the root url.
    """
    return jsonify({'message': 'Welcome to JobKonnect.'})

"""Define routes for user operations."""


@app.route('/api/user/register', methods=['POST'], strict_slashes=False)
def register():
    """
    Endpoint for the user registration.
    """
    """Extract data from JSON request."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    phone_number = data.get('phone_number')
    address = data.get('address')
    first_name = data.get('first_name', None)
    last_name = data.get('last_name', None)
    company_name = data.get('company_name', None)
    website = data.get('website', None)
    contact_infor= data.get('contact_infor', None)

    """Validate required fields based on role."""
    if role == 'job_seeker' and (not first_name or not last_name):
        return jsonify({'error': 'First name and last name are required for job seekers'}), 400
    elif role == 'employer' and (not company_name or not website):
        return jsonify({'error': 'Company name and website are required for employers'}), 400

    try:
        """Call register_user function to add user to database."""
        register_user(username, password, email, role, phone_number, address,
                      first_name=first_name, last_name=last_name,
                      company_name=company_name, website=website, contact_infor=contact_infor)

        return jsonify({'message': 'User registered successfully'}), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except SQLAlchemyError as se:
        return jsonify({'error': f'Failed to register user: {str(se)}'}), 500
    

@app.route('/api/user/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Endpoint for the user login.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email')
    password = data.get('password')

    """Validate input."""
    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    """Query the user from the database."""
    user = login_user(email, password)
    if user:
        token, expiration = generate_token(user.id, user.username, user.role)
        print(f"Token: {token}, Expiration: {expiration}")
        return jsonify({
            'user_id': user.id,
            'token': token,
            'role': user.role,
            'token_expiration': expiration
        })
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/user/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_route(id):
    """Implement logic to get user by id."""
    user = get_user_by_id(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())

#@app.route('/api/user/<int:user_id>/application', methods=['GET'])
#@token_required
#def get_user_application(current_user, user_id):
#   """Retrieve a specific job application associated with a given."""
#    if current_user['id'] != user_id:
#        """Check if the current user is authorized to access this endpoint."""
#        return jsonify({'error': 'Unauthorized access'}), 403

#    """Retrieve the application for the given user_id."""
#    application = get_application_by_user_id(user_id)
#    if application:
#        """If application found, return it with status code 200."""
#        return jsonify(application), 200
#    else:
#        """If no application found, return an error message with status code 404."""
#        return jsonify({'error': 'No application found'}), 404

"""Define routes for Job operations."""


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Delete job listing by ID."""
    jobs_list = get_all_jobs()
    if jobs_list is not None:
        return jsonify(jobs_list), 200
    else:
        return jsonify({'error': 'Failed to retrieve jobs'}), 500


@app.route('/api/jobs', methods=['POST'])
def create_new_job():
    """Create a new job listing."""
    data = request.get_json()
    job_id = create_job(data)
    if job_id is not None:
        return jsonify({'message': 'Job listing created successfully', 'job_id': job_id}), 201
    else:
        return jsonify({'error': 'Failed to create job listing'}), 500


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Retrieve job details by ID."""
    job_details = get_job_by_id(job_id)
    if job_details:
        return jsonify(job_details), 200
    else:
        return jsonify({'error': f'Job with ID {job_id} not found'}), 404


@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job_by_id(job_id):
    """Update job listing by ID."""
    data = request.get_json()
    success = update_job(job_id, data)
    if success:
        return jsonify({'message': 'Job listing updated successfully'}), 200
    else:
        return jsonify({'error': f'Failed to update job with ID {job_id}'}), 500


@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job_by_id(job_id):
    """Delete job listing by ID."""
    success = delete_job(job_id)
    if success:
        return jsonify({'message': 'Job listing deleted successfully'}), 200
    else:
        return jsonify({'error': f'Failed to delete job with ID {job_id}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
