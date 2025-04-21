from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from app import db
from backend.models.reward import Reward
from backend.models.user import User

rewards_bp = Blueprint('rewards', __name__)

@rewards_bp.route('', methods=['GET'])
@jwt_required()
def get_rewards():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Get total points for this user
    total_points = db.session.query(func.sum(Reward.points))\
        .filter_by(user_id=user_id)\
        .scalar() or 0
    
    # Get total entries count
    total_entries = Reward.query.filter_by(user_id=user_id).count()
    
    # Get rewards with pagination
    rewards = Reward.query.filter_by(user_id=user_id)\
        .order_by(Reward.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    return {
        "status": "success",
        "total_points": total_points,
        "total_entries": total_entries,
        "page": page,
        "limit": limit,
        "rewards": [reward.to_dict() for reward in rewards]
    }

@rewards_bp.route('/add', methods=['POST'])
@jwt_required()
def add_reward():
    """
    Add reward points for an action
    
    This endpoint would typically be called internally by the system,
    not directly by clients.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    action = data.get('action')
    points = data.get('points')
    description = data.get('description')
    
    if not action or not points:
        return {"status": "error", "message": "Action and points are required"}, 400
    
    # Validate points is a positive number
    try:
        points = int(points)
        if points <= 0:
            raise ValueError
    except ValueError:
        return {"status": "error", "message": "Points must be a positive integer"}, 400
    
    # Create reward record
    reward = Reward(
        user_id=user_id,
        action=action,
        points=points,
        description=description
    )
    
    db.session.add(reward)
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Reward points added",
        "reward": reward.to_dict()
    }

@rewards_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get a leaderboard of users with the most points"""
    # This is a simplified implementation
    # In a real application, you might want to cache this result
    # or calculate it periodically to improve performance
    
    # Query for top 10 users by total points
    leaderboard = db.session.query(
        Reward.user_id,
        func.sum(Reward.points).label('total_points')
    ).group_by(Reward.user_id)\
    .order_by(func.sum(Reward.points).desc())\
    .limit(10)\
    .all()
    
    # Get user names (fixed version)
    result = []
    for user_id, total_points in leaderboard:
        user = User.query.get(user_id)
        result.append({
            "user_id": user_id,
            "name": user.name if user and user.name else f"User {user_id}",
            "total_points": total_points
        })
    
    return {
        "status": "success",
        "leaderboard": result
    }