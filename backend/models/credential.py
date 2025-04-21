from datetime import datetime
from app import db

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    credential_type = db.Column(db.String(50), nullable=True)  # certificate, degree, license
    issuer = db.Column(db.String(100), nullable=True)
    issue_date = db.Column(db.DateTime, nullable=True)
    expiry_date = db.Column(db.DateTime, nullable=True)
    file_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'credential_type': self.credential_type,
            'issuer': self.issuer,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'file_url': self.file_url,
            'created_at': self.created_at.isoformat()
        }