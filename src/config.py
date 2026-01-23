# Application configuration - Enterprise Grade

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///loan_manager.db')
    DATABASE_DIR = os.getenv('DATABASE_DIR', 'data')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', None)
    
    # Payment Processing
    MAX_TRANSACTION_AMOUNT = float(os.getenv('MAX_TRANSACTION_AMOUNT', 100000))
    MAX_DAILY_TRANSACTIONS = int(os.getenv('MAX_DAILY_TRANSACTIONS', 10))
    DAILY_TRANSACTION_LIMIT = float(os.getenv('DAILY_TRANSACTION_LIMIT', 500000))
    
    # API
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    
    # Logging
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # USA Specific (as strings to preserve leading zeros)
    USA_MIN_ROUTING = '010000000'
    USA_MAX_ROUTING = '121000248'
    
    # Canada Specific
    CANADA_TRANSIT_LENGTH = 5
    CANADA_INSTITUTION_LENGTH = 3
    
    # Fraud Detection
    FRAUD_CHECK_ENABLED = os.getenv('FRAUD_CHECK_ENABLED', 'true').lower() == 'true'
    FRAUD_ALERT_THRESHOLD = float(os.getenv('FRAUD_ALERT_THRESHOLD', 10000))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENVIRONMENT = 'development'


class ProductionConfig(Config):
    """Production configuration"""
    ENVIRONMENT = 'production'
    TESTING = False
    
    # Ensure critical env vars are set
    @classmethod
    def validate(cls):
        if cls.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("SECRET_KEY must be set in production")
        if cls.ENCRYPTION_KEY is None:
            raise ValueError("ENCRYPTION_KEY must be set in production")


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    ENVIRONMENT = 'testing'
    DATABASE_DIR = 'test_data'
    MAX_TRANSACTION_AMOUNT = 50000


def get_config():
    """Get configuration based on environment"""
    environment = os.getenv('ENVIRONMENT', 'development').lower()
    
    if environment == 'production':
        ProductionConfig.validate()
        return ProductionConfig()
    elif environment == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()
