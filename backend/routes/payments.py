from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from backend.models.payment import Payment

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/history', methods=['GET'])
@jwt_required()
def get_payment_history():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Get total count
    total = Payment.query.filter_by(user_id=user_id).count()
    
    # Get payments with pagination
    payments = Payment.query.filter_by(user_id=user_id)\
        .order_by(Payment.created_at.desc())\
        .offset((page - 1) * limit)\
        .limit(limit)\
        .all()
    
    return {
        "status": "success",
        "total": total,
        "page": page,
        "limit": limit,
        "payments": [payment.to_dict() for payment in payments]
    }

@payments_bp.route('/process', methods=['POST'])
@jwt_required()
def process_payment():
    """
    Process a payment for premium features
    
    In a real application, this would integrate with a payment processor
    like Stripe, PayPal, etc.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    payment_type = data.get('payment_type')
    amount = data.get('amount')
    currency = data.get('currency', 'USD')
    
    if not payment_type or not amount:
        return {"status": "error", "message": "Payment type and amount are required"}, 400
    
    # Create payment record (in pending state)
    payment = Payment(
        user_id=user_id,
        amount=amount,
        currency=currency,
        payment_type=payment_type,
        status='pending',
        description=data.get('description', f'{payment_type.title()} payment')
    )
    
    db.session.add(payment)
    db.session.commit()
    
    # In a real application, this would redirect to a payment processor
    # For demo purposes, we'll just simulate a successful payment
    payment.status = 'completed'
    payment.transaction_id = f"tx_{payment.id}_{user_id}"
    payment.provider = "Stripe"  # Example provider
    
    db.session.commit()
    
    return {
        "status": "success",
        "message": "Payment processed successfully",
        "payment": payment.to_dict()
    }

@payments_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_payment_details(id):
    user_id = get_jwt_identity()
    
    # Find payment and ensure it belongs to user
    payment = Payment.query.filter_by(id=id, user_id=user_id).first()
    
    if not payment:
        return {"status": "error", "message": "Payment not found"}, 404
    
    return {
        "status": "success",
        "payment": payment.to_dict()
    }