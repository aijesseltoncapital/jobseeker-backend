from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_, and_
from flask_socketio import emit, join_room
from datetime import datetime

# Define the Blueprint for messages
messages_bp = Blueprint('messages', __name__)

# Example route for sending a message
@messages_bp.route('/send', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    data = request.get_json()
    recipient_id = data.get('recipient_id')
    content = data.get('content')

    if not recipient_id or not content:
        return jsonify({'error': 'Recipient ID and content are required'}), 400

    # Emit the message to the recipient's room
    room = f"user_{recipient_id}"
    emit('new_message', {'sender_id': user_id, 'content': content, 'timestamp': datetime.utcnow().isoformat()}, room=room)

    return jsonify({'status': 'Message sent successfully'}), 200

# Example route for joining a room
@messages_bp.route('/join', methods=['POST'])
@jwt_required()
def join_chat_room():
    user_id = get_jwt_identity()
    room = f"user_{user_id}"
    join_room(room)
    return jsonify({'status': f'Joined room {room} successfully'}), 200