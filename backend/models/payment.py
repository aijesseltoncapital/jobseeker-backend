from datetime import datetime
from app import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default="USD")
    payment_type = db.Column(db.String(50), nullable=False)  # subscription, premium_feature, etc.
    status = db.Column(db.String(20), nullable=False)  # completed, pending, failed, refunded
    transaction_id = db.Column(db.String(100), nullable=True)
    provider = db.Column(db.String(50), nullable=True)  # Stripe, PayPal, etc.
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'currency': self.currency,
            'payment_type': self.payment_type,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'provider': self.provider,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }