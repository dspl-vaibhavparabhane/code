

import os
from datetime import timedelta


class Config:
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-JWT-Extended Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_ALGORITHM = "HS256"
    JWT_DECODE_LEEWAY = 10  # Allow 10 seconds leeway for token validation
    
    # CORS
    CORS_ORIGINS = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")]


class DevelopmentConfig(Config):
    
    DEBUG = True
    TESTING = False
    
    # Use SQLite by default for quick testing (no setup needed)
    # To use PostgreSQL instead, set USE_POSTGRES=true in your .env
    USE_POSTGRES = os.getenv("USE_POSTGRES", "false").lower() == "true"
    
    if USE_POSTGRES:
        # PostgreSQL database URL
        SQLALCHEMY_DATABASE_URI = (
            f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
            f"{os.getenv('DB_PASSWORD', 'postgres')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '5432')}/"
            f"{os.getenv('DB_NAME', 'dspl_asset_pulse_dev')}"
        )
    else:
        # SQLite for quick testing (default)
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            "sqlite:///dspl_asset_pulse.db"
        )


class ProductionConfig(Config):
    
    DEBUG = False
    TESTING = False
    
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME')}"
    )
    
    # Production-specific settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Must be set in production


class TestingConfig(Config):
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}


def get_config(env: str = None) -> Config:

    if env is None:
        env = os.getenv("FLASK_ENV", "development")
    
    return config.get(env, config["default"])
