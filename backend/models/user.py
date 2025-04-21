from datetime import datetime
from app import db, bcrypt

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    linkedin_id = db.Column(db.String(100), nullable=True)
    google_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Profile fields
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    resume_url = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Settings
    notification_preferences = db.Column(db.JSON, default={})
    privacy_settings = db.Column(db.JSON, default={})
    
    # Relationships
    saved_jobs = db.relationship('SavedJob', backref='user', lazy=True)
    applications = db.relationship('JobApplication', backref='user', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    credentials = db.relationship('Credential', backref='user', lazy=True)
    payments = db.relationship('Payment', backref='user', lazy=True)
    rewards = db.relationship('Reward', backref='user', lazy=True)
    schedules = db.relationship('Schedule', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email
        }
    
    def get_full_profile(self):
        """Extended user data for profile endpoint"""
        return {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'email': self.email,
            'bio': self.bio,
            'skills': self.skills.split(',') if self.skills else [],
            'resume_url': self.resume_url,
            'profile_image': self.profile_image,
            'created_at': self.created_at.isoformat()
        }
