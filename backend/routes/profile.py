from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import bcrypt

from app import db
from backend.models.user import User
from backend.models.credential import Credential
from backend.models.schedule import Schedule

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    return {
        "status": "success",
        "user": user.get_full_profile()
    }

@profile_bp.route('/edit', methods=['PUT'])
@jwt_required()
def edit_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    data = request.get_json()
    
    # Update fields that are provided
    if 'name' in data:
        user.name = data['name']
    
    if 'bio' in data:
        user.bio = data['bio']
    
    if 'skills' in data:
        user.skills = data['skills']
    
    if 'email' in data and data['email'] != user.email:
        # Check if email is already in use
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return {"status": "error", "message": "Email already in use"}, 400
        
        user.email = data['email']
    
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "user": user.to_dict()
    }

@profile_bp.route('/resume', methods=['GET'])
@jwt_required()
def download_resume():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or not user.resume_url:
        return {"status": "error", "message": "Resume not found"}, 404
    
    # In a real application, this might be a URL to a cloud storage service
    # or a path to a local file
    resume_path = os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], user.resume_url)
    
    if not os.path.exists(resume_path):
        return {"status": "error", "message": "Resume file not found"}, 404
    
    return send_file(resume_path, as_attachment=True)

@profile_bp.route('/resume/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    if 'resume' not in request.files:
        return {"status": "error", "message": "No file part"}, 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return {"status": "error", "message": "No selected file"}, 400
    
    # Check file extension
    allowed_extensions = {'pdf', 'doc', 'docx'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return {"status": "error", "message": "File type not allowed"}, 400
    
    # Make sure upload directory exists
    os.makedirs(current_app.config['RESUME_UPLOAD_FOLDER'], exist_ok=True)
    
    # Save file with secure filename
    filename = secure_filename(f"{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
    file_path = os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Update user's resume URL
    user.resume_url = filename
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Resume uploaded successfully",
        "resume_url": filename
    }

@profile_bp.route('/credentials', methods=['POST'])
@jwt_required()
def upload_credential():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    if 'credential' not in request.files:
        return {"status": "error", "message": "No file part"}, 400
    
    file = request.files['credential']
    
    if file.filename == '':
        return {"status": "error", "message": "No selected file"}, 400
    
    # Get form data
    title = request.form.get('title')
    description = request.form.get('description')
    credential_type = request.form.get('credential_type')
    issuer = request.form.get('issuer')
    
    if not title:
        return {"status": "error", "message": "Title is required"}, 400
    
    # Check file extension
    allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return {"status": "error", "message": "File type not allowed"}, 400
    
    # Make sure upload directory exists
    os.makedirs(current_app.config['CREDENTIAL_UPLOAD_FOLDER'], exist_ok=True)
    
    # Save file with secure filename
    filename = secure_filename(f"{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
    file_path = os.path.join(current_app.config['CREDENTIAL_UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Create credential record
    credential = Credential(
        user_id=user_id,
        title=title,
        description=description,
        credential_type=credential_type,
        issuer=issuer,
        file_url=filename
    )
    
    db.session.add(credential)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Credential uploaded successfully",
        "credential": credential.to_dict()
    }

@profile_bp.route('/credentials', methods=['GET'])
@jwt_required()
def get_credentials():
    user_id = get_jwt_identity()
    
    credentials = Credential.query.filter_by(user_id=user_id).all()
    
    return {
        "status": "success",
        "credentials": [credential.to_dict() for credential in credentials]
    }

@profile_bp.route('/schedule', methods=['GET'])
@jwt_required()
def get_schedule():
    user_id = get_jwt_identity()
    
    schedules = Schedule.query.filter_by(user_id=user_id).all()
    
    return {
        "status": "success",
        "schedules": [schedule.to_dict() for schedule in schedules]
    }

@profile_bp.route('/schedule', methods=['POST'])
@jwt_required()
def update_schedule():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not isinstance(data, list):
        return {"status": "error", "message": "Schedule data must be an array"}, 400
    
    # Delete existing schedules
    Schedule.query.filter_by(user_id=user_id).delete()
    
    # Create new schedules
    for schedule_data in data:
        day_of_week = schedule_data.get('day_of_week')
        start_time = schedule_data.get('start_time')
        end_time = schedule_data.get('end_time')
        availability = schedule_data.get('availability', True)
        
        if day_of_week is None or start_time is None or end_time is None:
            return {"status": "error", "message": "Each schedule must have day_of_week, start_time, and end_time"}, 400
        
        schedule = Schedule(
            user_id=user_id,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            availability=availability
        )
        db.session.add(schedule)
    
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Schedule updated successfully"
    }

@profile_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return {"status": "error", "message": "Current password and new password are required"}, 400
    
    # Check current password
    if not user.check_password(current_password):
        return {"status": "error", "message": "Current password is incorrect"}, 400
    
    # Update password
    user.set_password(new_password)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Password changed successfully"
    }

@profile_bp.route('/profile-image', methods=['POST'])
@jwt_required()
def upload_profile_image():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    if 'image' not in request.files:
        return {"status": "error", "message": "No file part"}, 400
    
    file = request.files['image']
    
    if file.filename == '':
        return {"status": "error", "message": "No selected file"}, 400
    
    # Check file extension
    allowed_extensions = {'jpg', 'jpeg', 'png'}
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
        return {"status": "error", "message": "File type not allowed"}, 400
    
    # Make sure upload directory exists
    os.makedirs(current_app.config['PROFILE_IMAGES_FOLDER'], exist_ok=True)
    
    # Save file with secure filename
    filename = secure_filename(f"{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{file.filename}")
    file_path = os.path.join(current_app.config['PROFILE_IMAGES_FOLDER'], filename)
    file.save(file_path)
    
    # Update user's profile image
    user.profile_image = filename
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Profile image uploaded successfully",
        "profile_image": filename
    }