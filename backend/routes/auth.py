from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app import db, bcrypt
from backend.models.user import User
from backend.services.auth_service import send_otp, verify_otp
from backend.services.social_service import verify_google_token, verify_linkedin_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')
    
    user = User.query.filter_by(phone_number=phone_number).first()
    
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return {
            "status": "success",
            "token": access_token,
            "user": user.to_dict()
        }
    
    return {"status": "error", "message": "Invalid credentials"}, 401

@auth_bp.route('/login/google', methods=['POST'])
def google_login():
    data = request.get_json()
    google_token = data.get('google_token')
    
    if not google_token:
        return {"status": "error", "message": "Missing token"}, 400
    
    user_info = verify_google_token(google_token)
    if not user_info:
        return {"status": "error", "message": "Invalid Google token"}, 401
    
    # Find or create user
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(
            name=user_info['name'],
            email=user_info['email'],
            google_id=user_info['sub']
        )
        db.session.add(user)
        db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return {
        "status": "success",
        "token": access_token,
        "user": user.to_dict()
    }

@auth_bp.route('/login/linkedin', methods=['POST'])
def linkedin_login():
    data = request.get_json()
    linkedin_token = data.get('linkedin_token')
    
    if not linkedin_token:
        return {"status": "error", "message": "Missing token"}, 400
    
    user_info = verify_linkedin_token(linkedin_token)
    if not user_info:
        return {"status": "error", "message": "Invalid LinkedIn token"}, 401
    
    # Find or create user
    user = User.query.filter_by(linkedin_id=user_info['id']).first()
    if not user:
        user = User(
            name=user_info['localizedFirstName'] + ' ' + user_info['localizedLastName'],
            linkedin_id=user_info['id']
        )
        db.session.add(user)
        db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return {
        "status": "success",
        "token": access_token,
        "user": user.to_dict()
    }

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    phone_number = data.get('phone_number')
    
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    # Send OTP to user's phone
    send_otp(phone_number)
    
    return {
        "status": "success",
        "message": "OTP sent to phone number"
    }

@auth_bp.route('/check-otp', methods=['POST'])
def check_otp():
    data = request.get_json()
    otp = data.get('otp')
    phone_number = data.get('phone_number')  # This is missing in the implementation
    
    if not phone_number:
        return {"status": "error", "message": "Phone number is required"}, 400
    
    # verify_otp needs both phone_number and otp parameters
    if verify_otp(phone_number, otp):
        return {
            "status": "success",
            "message": "OTP confirmed"
        }
    
    return {"status": "error", "message": "Invalid OTP"}, 400

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    phone_number = data.get('phone_number')
    new_password = data.get('new_password')
    
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    user.set_password(new_password)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Password reset successful"
    }

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    phone_number = data.get('phone_number')
    password = data.get('password')
    
    if User.query.filter_by(phone_number=phone_number).first():
        return {"status": "error", "message": "Phone number already registered"}, 400
    
    user = User(phone_number=phone_number)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    
    return {
        "status": "success",
        "token": access_token,
        "user": user.to_dict()
    }, 201

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT tokens are stateless, so we don't need to invalidate them server-side
    # Client should discard the token
    return {
        "status": "success",
        "message": "Logged out successfully"
    }
