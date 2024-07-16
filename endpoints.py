#!/usr/bin/env python3
"""Restful api."""

"""Import necessary modules"""
from flask import Flask, request, jsonify, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
from jwtfunc import generate_token, token_required
from db_operations import *


"""Creating an instance of a flask class."""
app = Flask(__name__)
"""Enable CORS for all routes"""
CORS(app)

"""Configuration for file uploads"""
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}


"""Route handler for the root URL."""
@app.route('/')
def index():
    """
    Endpoint for the root url.

    Returns:
        JSON: A welcome message.

    """
    return jsonify({'message': 'Welcome to JobKonnect.'})


"""Define routes for user operations."""

"""Routes for user registration."""
@app.route('/api/user/register', methods=['POST'], strict_slashes=False)
def register():
    """
    Endpoint for the user registration.

    Returns:
        JSON: Success or error message.

    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

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
    contact_info= data.get('contact_infor', None)

    """Validate required fields"""     
    if not username or not password or not email or not role or not phone_number:
        """Missing required fields during registration."""
        return jsonify({'error': 'Missing required fields'}), 400

    """Validate required fields based on role."""
    if role == 'job_seeker' and (not first_name or not last_name):
        return jsonify({'error': 'First name and last name are required for job seekers'}), 400
    elif role == 'employer' and (not company_name or not website):
        return jsonify({'error': 'Company name and website are required for employers'}), 400

    try:
        """Call register_user function to add user to database."""
        register_user(username, password, email, role, phone_number, address,
                      first_name=first_name, last_name=last_name,
                      company_name=company_name, website=website, contact_info=contact_info)
    
        return jsonify({'message': 'User registered successfully'}), 201

    except ValueError as ve:
        return jsonify({'error': f'Registration failed: {str(ve)}'}), 400

    except IntegrityError as e:
        if "Duplicate entry" in str(e):
            error_message = "Sorry, the username is already taken. Please choose a different username."
        else:
            error_message = "An error occurred during user registration. Please try again later."

    except SQLAlchemyError as se:
        return jsonify({'error': f'Failed to register user: {str(se)}'}), 500


"""Route for user login"""
@app.route('/api/user/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Endpoint for the user login.

    Returns:
        JSON: User details and authentication token.

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
            'user': user.to_dict(),
            'token': token,
            'token_expiration': expiration
        })
    return jsonify({'error': 'Invalid email or password'}), 401


"""Route to get user by ID"""
@app.route('/api/user/<int:id>', methods=['GET'], strict_slashes=False)
def get_user_route(id):
    """
    Endpoint logic to get user by id.

    Args:
        id(int): The ID of the user to retrieve.

    Returns:
        JSON: User details or error message if the user is not found.

    """
    user = get_user_by_id(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict())


"""Route to get all users"""
@app.route('/api/users', methods=['GET'], strict_slashes=False)
def get_all_users_route():
    """
    Endpoint to retrieve all users.

    Returns:
        JSON: A list of all users.

    """
    users = get_all_users()
    return jsonify(users)


"""Define routes for Job operations."""


"""Route to create a new job listings"""
@app.route('/api/jobs', methods=['POST'])
def create_new_job():
    """
    Endpoint to create a new job listing.

    Returns:
        JSON: Newly created job details or error message.

    """
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


"""Route to retrieve all job listings"""
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """
    Endpoint to retrieve all job listings

    Returns:
        JSON: A list of all job listings.

    """
    jobs_list = get_all_jobs()
    if jobs_list is not None:
        return jsonify(jobs_list), 200
    else:
        return jsonify({'error': 'Failed to retrieve jobs'}), 500


"""Route to retrieve job details by ID."""
@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Endpoint to retrieve job details by ID.

    Args:
        job_id(int): The ID of the job to retrieve.

    Returns:
        JSON: Job details or error message if job not found.

    """
    job_details = get_job_by_id(job_id)
    if job_details:
        return jsonify(job_details), 200
    else:
        return jsonify({'error': f'Job with ID {job_id} not found'}), 404


"""Route to reyrieve jobs by employer ID."""
@app.route('/api/jobs/employer/<int:employer_id>', methods=['GET'], strict_slashes=False)
def get_jobs_by_employer(employer_id):
    """
    Endpoint to retrieve all jobs posted by a specific employer.

    Args:
        employer_id (int): The ID of the employer.

    Returns:
        JSON: A JSON response with a list of jobs, or an error message if failed.
    """
    try:
        jobs = get_jobs_by_employer_id(employer_id)
        if jobs is None:
            return jsonify({'error': f'Error retrieving jobs for employer {employer_id}'}), 500
        return jsonify(jobs), 200
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


"""Route to update job listing by ID."""
@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job_by_id(job_id):
    """
    Endpoint to update job listing by ID.

    Args:
        job_id(int): The ID of the job to update.

    Returns:
        JSON: Updated job details or error message if update failed.

    """
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


"""Route to delete job listings by ID."""
@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job_by_id(job_id):
    """
    Endpoint to delete job listing by ID.

    Args:
        job_id(int): The ID of the job to delete.

    Returns:
        JSON: Success message or error message if deletion failed.

    """
    success = delete_job(job_id)
    if success:
        return jsonify({'message': 'Job listing deleted successfully'}), 200
    else:
        return jsonify({'error': f'Failed to delete job with ID {job_id}'}), 500

"""Define routes for Application operations."""


"""Route to apply to a job."""
@app.route('/api/jobs/<int:id>/apply', methods=['POST'])
@token_required
def apply_to_job(current_user, id):
    """
    Endpoint to apply to a job.

    Args:
        current_user (dict): The authenticated user's information.
        id (int): The ID of the job to apply to.

    Returns:
        JSON: Application details or the error message if application failed.
    """
    
    if current_user['role'] != 'job_seeker':
        return jsonify({"error": "Only job_seeker can apply for jobs"}), 403

    job = get_job_by_id(id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    
    data = request.form
    files = request.files

    application_data = {
        "job_id": id,
        "user_id": current_user['id'],
        "years_of_experience": data.get('years_of_experience'),
        "status": data.get('status', 'submitted'),
        "employer_id": job.get('employer_id'),
        "name": data.get('name'),
        "school_name": data.get('school_name'),
        "portfolio": data.get('portfolio'),
        "skills": data.get('skills')
    }

    file_resume = files.get('resume')
    file_cover_letter = files.get('cover_letter')

    if not file_resume or not file_cover_letter:
        return jsonify({"error": "Resume and cover letter are required"}), 400

    filename_resume = secure_filename(file_resume.filename)
    filename_cover_letter = secure_filename(file_cover_letter.filename)

    file_resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_resume))
    file_cover_letter.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_cover_letter))

    """Generate URLs for the uploaded files"""
    application_data['resume'] = url_for('uploaded_file', filename=filename_resume, _external=True)
    application_data['cover_letter'] = url_for('uploaded_file', filename=filename_cover_letter, _external=True)

    try:
        application = create_application(application_data)
        return jsonify(application.to_dict()), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400


"""Route to uploaded_file."""
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    Serve a file from the upload directory.

    :param filename: The name of the file to be served.
    :return: The file located in the UPLOAD_FOLDER with the specified filename.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


"""Route to get all applications for the current user."""
@app.route('/api/applications', methods=['GET'])
@token_required
def get_applications_endpoint(current_user):
    """
    Endpoint to retrieve applications based on user role.

    Args:
        current_user (dict): The authenticated user's information.

    Returns:
        JSON: A list of applications or an error message if retrieval failed.
    """
    if current_user['role'] == 'employer':
        applications = get_applications(current_user['id'], 'employer')
    else:
        applications = get_applications(current_user['id'], 'job_seeker')

    application_dicts = [app.to_dict() for app in applications]
    return jsonify(application_dicts)


""" Route to get a specific application by ID."""
@app.route('/api/application/<int:id>', methods=['GET'])
@token_required
def get_application_by_id_endpoint(current_user, id):
    """
    Endpoint to retrieve a specific application by ID.
    
    Args:
        current_user (dict): The authenticated user's information.
        id (int): The ID of the application to retrieve.

    Returns:
        JSON: Application details or an error message if application not found or un authorized.
    """
    application = get_application_by_id(id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
    
    if current_user['role'] == 'employer' and application.employer_id != current_user['id']:
        return jsonify({"error": "Unauthorized access to this application"}), 403
    
    if current_user['role'] == 'job_seeker' and application.user_id != current_user['id']:
        return jsonify({"error": "Unauthorized access to this application"}), 403

    return jsonify(application.to_dict())


"""Route to update the status of a specific application by ID."""
@app.route('/api/application/<int:id>', methods=['PUT'])
@token_required
def update_application_status_endpoint(current_user, id):
    """
    Endpoint to update the status of a specific application by ID.

    Args:
        current_user (dict): The authenticated user's information.
        id (int): The ID of the application to update.

    Returns:
        JSON: Updated application details or an error message if update failed or application not found.
    """
    if current_user['role'] != 'employer':
        return jsonify({"error": "Only employers can update applications"}), 403

    data = request.get_json()
    application_dict = update_application_status(id, data)
    return jsonify(application_dict) if application_dict else jsonify({"error": "Application not found"}), 404


"""Route to delete a specific application by ID."""
@app.route('/api/application/<int:id>', methods=['DELETE'])
@token_required
def delete_application_endpoint(current_user, id):
    """
    Endpoint to delete a specific application by ID.

    Args:
        current_user (dict): The authenticated user's information.
        id (int): The ID of teh application to delete.

    Returns:
        JSON: Success message or an error message if deleteion failed or application not found.
    """
    if current_user['role'] != 'employer':
        return jsonify({"error": "Only employers can delete applications"}), 403

    success = delete_application(id)
    return jsonify({"message": "Application deleted"}) if success else jsonify({"error": "Application not found"}), 202

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
