import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nec-newgen-secret-key-2024'
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:Sathiya@localhost:2618/nec_newgen'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True
    }
    
    # Application Configuration
    APP_NAME = 'NEC NewGen'
    COLLEGE_NAME = 'National Engineering College'
    
    # Theme Configuration
    THEME_CONFIG = {
        'dark': {
            'primary': '#001f3f',
            'secondary': '#FFD700',
            'dark_blue': '#003366',
            'light_blue': '#00509E',
            'background': 'linear-gradient(135deg, #001f3f 0%, #003366 100%)',
            'text_color': 'white'
        },
        'light': {
            'primary': '#f8f9fa',
            'secondary': '#001f3f',
            'dark_blue': '#e9ecef',
            'light_blue': '#00509E',
            'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
            'text_color': '#333'
        }
    }
    
    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'static/uploads'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Security Configuration
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'