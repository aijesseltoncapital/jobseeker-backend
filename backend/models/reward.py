from datetime import datetime
from app import db

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)  # profile_complete, apply, login, etc.
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'points': self.points,
            'action': self.action,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }