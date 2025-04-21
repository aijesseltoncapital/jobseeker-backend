from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from flask_socketio import emit, join_room, leave_room

from app import db, socketio
from models.message import Message, Conversation
from models.user import User
from models.notification import Notification
from datetime import datetime

# Define the Blueprint for messages
messages_bp = Blueprint('messages', __name__)

@messages_bp.route('', methods=['GET'])
@jwt_required()
def get_message_list():
    user_id = get_jwt_identity()
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Find conversations where the user is either user1 or user2
    query = Conversation.query.filter(
        or_(
            Conversation.user1_id == user_id,
            Conversation.user2_id == user_id
        )
    )
    
    if keyword:
        # Search in conversation title or latest message
        query = query.filter(Conversation.title.ilike(f'%{keyword}%'))
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    conversations = query.order_by(Conversation.updated_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return {
        "status": "success",
        "total": total,
        "page": page,
        "limit": limit,
        "conversations": [conv.to_dict() for conv in conversations]
    }

@messages_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_message_detail(id):
    user_id = get_jwt_identity()
    
    # Find conversation and ensure user is a participant
    conversation = Conversation.query.filter_by(id=id).filter(
        or_(
            Conversation.user1_id == user_id,
            Conversation.user2_id == user_id
        )
    ).first()
    
    if not conversation:
        return {"status": "error", "message": "Conversation not found"}, 404
    
    # Get messages in this conversation
    messages = Message.query.filter_by(conversation_id=id).order_by(Message.created_at).all()
    
    # Mark unread messages as read
    unread_messages = Message.query.filter_by(
        conversation_id=id,
        receiver_id=user_id,
        read_at=None
    ).all()
    
    for msg in unread_messages:
        msg.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return {
        "status": "success",
        "conversation": conversation.to_dict(),
        "messages": [msg.to_dict() for msg in messages]
    }

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    # Authentication is handled by the decorator in app.py
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('join')
def handle_join(data):
    user_id = get_jwt_identity()
    
    # Create a room for the user to receive messages
    room = f"user_{user_id}"
    join_room(room)
    
    print(f"User {user_id} joined room {room}")
    
    # Also join any conversation rooms if specified
    if 'conversation_id' in data:
        conversation_room = f"conversation_{data['conversation_id']}"
        join_room(conversation_room)
        print(f"User {user_id} joined conversation room {conversation_room}")

@socketio.on('leave')
def handle_leave(data):
    user_id = get_jwt_identity()
    
    if 'conversation_id' in data:
        room = f"conversation_{data['conversation_id']}"
        leave_room(room)
        print(f"User {user_id} left room {room}")

@socketio.on('message')
def handle_message(data):
    user_id = get_jwt_identity()
    receiver_id = data.get('receiver_id')
    text = data.get('text')
    conversation_id = data.get('conversation_id')
    
    if not receiver_id or not text:
        return {"status": "error", "message": "Receiver ID and text are required"}
    
    # Find or create conversation
    if not conversation_id:
        # Check if conversation exists between these users
        conversation = Conversation.query.filter(
            or_(
                and_(Conversation.user1_id == user_id, Conversation.user2_id == receiver_id),
                and_(Conversation.user1_id == receiver_id, Conversation.user2_id == user_id)
            )
        ).first()
        
        if not conversation:
            # Create new conversation
            sender = User.query.get(user_id)
            receiver = User.query.get(receiver_id)
            
            if not receiver:
                return {"status": "error", "message": "Receiver not found"}
            
            title = f"Conversation with {receiver.name if receiver.name else 'User'}"
            conversation = Conversation(
                user1_id=user_id,
                user2_id=receiver_id,
                title=title
            )
            db.session.add(conversation)
            db.session.commit()
    else:
        conversation = Conversation.query.get(conversation_id)
        if not conversation:
            return {"status": "error", "message": "Conversation not found"}
        
        # Ensure user is part of this conversation
        if conversation.user1_id != user_id and conversation.user2_id != user_id:
            return {"status": "error", "message": "Not authorized to send message in this conversation"}
    
    # Create message
    message = Message(
        conversation_id=conversation.id,
        sender_id=user_id,
        receiver_id=receiver_id,
        text=text
    )
    db.session.add(message)
    
    # Update conversation timestamp
    conversation.updated_at = datetime.utcnow()
    
    # Create notification for recipient
    notification = Notification(
        user_id=receiver_id,
        title="New Message",
        message=f"You have received a new message",
        notification_type="message",
        related_id=conversation.id
    )
    db.session.add(notification)
    
    db.session.commit()
    
    # Emit to both the recipient's user room and the conversation room
    message_data = message.to_dict()
    
    # Send to recipient's personal room
    recipient_room = f"user_{receiver_id}"
    emit('new_message', message_data, room=recipient_room)
    
    # Send to conversation room
    conversation_room = f"conversation_{conversation.id}"
    emit('new_message', message_data, room=conversation_room)
    
    return {"status": "success", "message": message_data}