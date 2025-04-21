from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app import db
from backend.models.notification import Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_notification_list():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Get total notification count
    total = Notification.query.filter_by(user_id=user_id).count()
    
    # Get read notification count
    read_count = Notification.query.filter_by(user_id=user_id).filter(Notification.read_at != None).count()
    
    # Get notifications with pagination
    notifications = Notification.query.filter_by(user_id=user_id)\
        .order_by(Notification.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    return {
        "status": "success",
        "total": total,
        "page": page,
        "limit": limit,
        "read_count": read_count,
        "notifications": [notification.to_dict() for notification in notifications]
    }

@notifications_bp.route('/mark-read-all', methods=['POST'])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()
    
    # Find all unread notifications
    unread_notifications = Notification.query.filter_by(user_id=user_id, read_at=None).all()
    
    count = len(unread_notifications)
    
    # Mark all as read
    for notification in unread_notifications:
        notification.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return {
        "status": "success",
        "message": "All notifications marked as read",
        "count": count
    }

@notifications_bp.route('/<int:id>/read', methods=['POST'])
@jwt_required()
def mark_notification_read(id):
    user_id = get_jwt_identity()
    
    # Find notification and ensure it belongs to user
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    
    if not notification:
        return {"status": "error", "message": "Notification not found"}, 404
    
    notification.read_at = datetime.utcnow()
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Notification marked as read"
    }

@notifications_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_notification(id):
    user_id = get_jwt_identity()
    
    # Find notification and ensure it belongs to user
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()
    
    if not notification:
        return {"status": "error", "message": "Notification not found"}, 404
    
    db.session.delete(notification)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Notification deleted"
    }