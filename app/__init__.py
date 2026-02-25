

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.config import get_config
from app.models import db
from app.models.db import init_db


def create_app(config_name: str = None) -> Flask:
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration based on environment
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize database with SQLAlchemy
    db.init_app(app)
    
    # Initialize JWT Manager for Flask-JWT-Extended
    jwt = JWTManager(app)

    # Initialize Swagger documentation
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "DSPL Asset Pulse API",
            "description": "Production-ready API for asset management and employee dashboard system with JWT authentication and RBAC",
            "version": "1.0.0",
            "contact": {
                "name": "DSPL Asset Pulse Team"
            }
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"Bearer": []}]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    
    
    # Enable CORS for frontend access with explicit configuration
    print(f"[CORS] Allowed Origins: {config.CORS_ORIGINS}")
    CORS(app, 
         resources={r"/api/*": {
             "origins": config.CORS_ORIGINS,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type"],
             "supports_credentials": True,
             "max_age": 3600
         }}
    )
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register API blueprints
    register_blueprints(app)
    
    # Initialize database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_blueprints(app: Flask) -> None:

    # Import blueprints here to avoid circular imports
    from app.routes.auth import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.asset import asset_bp
    from app.routes.conference_room_routes import conference_room_bp
    from app.routes.booking_routes import booking_bp
    
    # Register blueprints with URL prefix
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(asset_bp, url_prefix="/api/v1/assets")
    app.register_blueprint(conference_room_bp, url_prefix="/api/v1/conference-rooms")
    app.register_blueprint(booking_bp, url_prefix="/api/v1/bookings")


def register_error_handlers(app: Flask) -> None:
    
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal server error"}, 500
    
    @app.errorhandler(400)
    def bad_request(e):
        return {"error": "Bad request"}, 400
