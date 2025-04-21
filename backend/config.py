import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-should-be-changed'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///jobseeker.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Redis for socket.io (optional)
    REDIS_URL = os.environ.get('REDIS_URL')
    
    # OAuth configurations
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    LINKEDIN_CLIENT_ID = os.environ.get('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.environ.get('LINKEDIN_CLIENT_SECRET')
    
    # Upload paths for different file types
    RESUME_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'resumes')
    CREDENTIAL_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'credentials')
    PROFILE_IMAGES_FOLDER = os.path.join(UPLOAD_FOLDER, 'profile_images')
