#!/usr/bin/env python3
"""Restful api."""

from flask import Flask, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from jwtfunc import generate_token, token_required
from db_operations import *


"""Creating an instance of a flask class."""
app = Flask(__name__)
CORS(app)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
        job_details = get_job_by_id(job_id)
        if job_details:
            """Fetch job details after creation."""
            return jsonify(job_details), 201
        else:
            return jsonify({'error': f'Job with ID {job_id} not found after creation'}), 404
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
        job_details = get_job_by_id(job_id)
        """Fetch updated job details."""
        if job_details:
            return jsonify(job_details), 200
        else:
            return jsonify({'error': f'Job with ID {job_id} not found after update'}), 404
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

@app.route('/api/jobs/<int:id>/apply', methods=['POST'])
@token_required
def apply_to_job(current_user, id):
    if current_user['role'] != 'job_seeker':
        return jsonify({"error": "Only job_seeker can apply for jobs"}), 403

    job = Job.query.get(id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    data = request.form
    files = request.files

    application_data = {
        "id": data.get('id'),
        "job_id": id,
        "employer_id": job.employer_id,
        "user_id": current_user['id'],
        "name": data.get('name'),
        "skills": data.get('skills'),
        "years_of_experience": data.get('years_of_experience'),
        "email": data.get('email'),
        "status": data.get('status', 'under_review'),  # Default status to 'under_review'
    }

    file_resume = files.get('resume')
    file_cover_letter = files.get('cover_letter')

    if not file_resume or not file_cover_letter:
        return jsonify({"error": "Resume and cover letter are required"}), 400

    filename_resume = secure_filename(file_resume.filename)
    filename_cover_letter = secure_filename(file_cover_letter.filename)

    file_resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_resume))
    file_cover_letter.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_cover_letter))

    # Generate URLs for the uploaded files
    application_data['resume'] = url_for('uploaded_file', filename=filename_resume, _external=True)
    application_data['cover_letter'] = url_for('uploaded_file', filename=filename_cover_letter, _external=True)

    application = create_application(application_data)
    return jsonify(application.to_dict()), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/api/applications', methods=['GET'])
@token_required
def get_applications_endpoint(current_user):
    if current_user['role'] == 'employer':
        applications = get_applications(current_user['id'], 'employer')
    else:
        applications = get_applications(current_user['id'], 'job_seeker')

    application_dicts = [app.to_dict() for app in applications]
    return jsonify(application_dicts)

@app.route('/api/application/<int:id>', methods=['GET'])
@token_required
def get_application_by_id_endpoint(current_user, id):
    application = get_application_by_id(id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
    
    if current_user['role'] == 'employer' and application.employer_id != current_user['id']:
        return jsonify({"error": "Unauthorized access to this application"}), 403
    
    if current_user['role'] == 'job_seeker' and application.user_id != current_user['id']:
        return jsonify({"error": "Unauthorized access to this application"}), 403

    return jsonify(application.to_dict())


@app.route('/api/application/<int:id>', methods=['PUT'])
@token_required
def update_application_status_endpoint(current_user, id):
    if current_user['role'] != 'employer':
        return jsonify({"error": "Only employers can update applications"}), 403

    data = request.json
    application = update_application_status(id, data)
    return jsonify(application.to_dict()) if application else jsonify({"error": "Application not found"}), 404

@app.route('/api/application/<int:id>', methods=['DELETE'])
@token_required
def delete_application_endpoint(current_user, id):
    if current_user['role'] != 'employer':
        return jsonify({"error": "Only employers can delete applications"}), 403

    success = delete_application(id)
    return jsonify({"message": "Application deleted"}) if success else jsonify({"error": "Application not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
