

from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance (will be initialized in app factory)
db = SQLAlchemy()


def init_db(app):
    """
    Initialize database with Flask app.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    # Create all tables
    with app.app_context():
        db.create_all()
