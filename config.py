import os

class Config:
    """Base configuration for SR Technologies website."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sr_technologies_secure_production_key_2026'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False

# Active configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}