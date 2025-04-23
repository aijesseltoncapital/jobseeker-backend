from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from backend.config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
socketio = SocketIO()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Register blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.jobs import jobs_bp
    from backend.routes.messages import messages_bp
    from backend.routes.notifications import notifications_bp
    from backend.routes.profile import profile_bp
    from backend.routes.settings import settings_bp
    from backend.routes.payments import payments_bp
    from backend.routes.rewards import rewards_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(rewards_bp, url_prefix='/rewards')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"status": "error", "message": "Not found"}, 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return {"status": "error", "message": "Internal server error"}, 500
    
    return app

# Add this to ensure socket.io works with JWT
@socketio.on('connect')
def test_connect():
    auth = request.args.get('token')
    if auth:
        try:
            # Verify JWT token
            decoded_token = jwt.decode_token(auth)
            user_id = decoded_token['sub']
            return True
        except:
            return False
    return False

app = create_app()
if __name__ == "__main__":
    socketio.run(app, debug=True)
