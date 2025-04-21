from datetime import datetime
from app import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    job_type = db.Column(db.String(50), nullable=False)  # e.g., full-time, part-time, contract
    salary = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('JobApplication', backref='job', lazy=True)
    saved_by = db.relationship('SavedJob', backref='job', lazy=True)
    
    def to_dict(self, detailed=False):
        """Convert job object to dictionary"""
        result = {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'job_type': self.job_type,
            'salary': self.salary,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None
        }
        
        if detailed:
            result.update({
                'description': self.description,
                'requirements': self.requirements,
                'benefits': self.benefits,
                'expires_at': self.expires_at.isoformat() if self.expires_at else None,
                'application_count': len(self.applications)
            })
            
        return result

class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Define unique constraint to avoid saving the same job twice
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='user_job_unique'),)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='applied')  # applied, viewed, rejected, interviewed, offered, accepted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Define unique constraint to avoid applying to the same job twice
    __table_args__ = (db.UniqueConstraint('user_id', 'job_id', name='user_job_application_unique'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'company': self.job.company if self.job else None,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }