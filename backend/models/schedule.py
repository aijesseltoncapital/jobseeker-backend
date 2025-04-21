from datetime import datetime
from app import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time = db.Column(db.String(5), nullable=False)  # Format: "09:00"
    end_time = db.Column(db.String(5), nullable=False)  # Format: "17:00"
    availability = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define unique constraint to avoid duplicate schedules for the same day
    __table_args__ = (db.UniqueConstraint('user_id', 'day_of_week', name='user_day_schedule_unique'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'availability': self.availability
        }