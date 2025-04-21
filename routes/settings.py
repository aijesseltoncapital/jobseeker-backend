from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from models.user import User

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/account/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    data = request.get_json()
    password = data.get('password')
    confirmation = data.get('confirmation')
    
    # Validate request
    if not password or not confirmation:
        return {"status": "error", "message": "Password and confirmation are required"}, 400
    
    if confirmation != "DELETE":
        return {"status": "error", "message": "Confirmation must be 'DELETE'"}, 400
    
    # Verify password
    if not user.check_password(password):
        return {"status": "error", "message": "Incorrect password"}, 400
    
    # Delete user account
    db.session.delete(user)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Account deleted successfully"
    }

@settings_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notification_preferences():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    # Default preferences if not set
    preferences = user.notification_preferences or {
        "email_notifications": True,
        "push_notifications": True,
        "sms_notifications": True,
        "job_alerts": True,
        "message_notifications": True,
        "application_updates": True
    }
    
    return {
        "status": "success",
        "preferences": preferences
    }

@settings_bp.route('/notifications', methods=['PUT'])
@jwt_required()
def update_notification_preferences():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    data = request.get_json()
    
    # Validate preferences
    required_prefs = [
        "email_notifications", "push_notifications", "sms_notifications", 
        "job_alerts", "message_notifications", "application_updates"
    ]
    
    for pref in required_prefs:
        if pref not in data:
            return {"status": "error", "message": f"Missing preference: {pref}"}, 400
        if not isinstance(data[pref], bool):
            return {"status": "error", "message": f"Preference {pref} must be a boolean"}, 400
    
    # Update preferences
    user.notification_preferences = data
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Notification preferences updated",
        "preferences": user.notification_preferences
    }

@settings_bp.route('/privacy', methods=['GET'])
@jwt_required()
def get_privacy_settings():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    # Default settings if not set
    settings = user.privacy_settings or {
        "profile_visibility": "public",
        "resume_visibility": "connections",
        "contact_info_visibility": "connections",
        "job_application_visibility": "private"
    }
    
    return {
        "status": "success",
        "settings": settings
    }

@settings_bp.route('/privacy', methods=['PUT'])
@jwt_required()
def update_privacy_settings():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {"status": "error", "message": "User not found"}, 404
    
    data = request.get_json()
    
    # Validate settings
    required_settings = [
        "profile_visibility", "resume_visibility", 
        "contact_info_visibility", "job_application_visibility"
    ]
    
    valid_visibilities = ["public", "connections", "private"]
    
    for setting in required_settings:
        if setting not in data:
            return {"status": "error", "message": f"Missing setting: {setting}"}, 400
        if data[setting] not in valid_visibilities:
            return {"status": "error", "message": f"Invalid visibility for {setting}. Must be one of: {', '.join(valid_visibilities)}"}, 400
    
    # Update settings
    user.privacy_settings = data
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Privacy settings updated",
        "settings": user.privacy_settings
    }