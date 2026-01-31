"""
General Biller - Enterprise Bill Payment System
Flask API Application

Copyright (c) 2026 General Biller Contributors
Licensed under the MIT License - see LICENSE file for details
"""

from flask import Flask
from flask_cors import CORS
from src.config import get_config
from src.models.db import init_db
from src.utils.middleware import RequestLogger, ErrorHandler
from src.utils.security_middleware import SecurityHeaders, HTTPSRedirect
from .routes import api_bp
from .auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False

    # CORS configuration - restrict in production
    if config.ENVIRONMENT == 'production':
        CORS(app, origins=["https://yourdomain.com"])  # Configure allowed origins
    else:
        CORS(app)

    # Register security middleware
    SecurityHeaders.setup(app)
    if config.ENVIRONMENT == 'production':
        HTTPSRedirect.setup(app)

    # Register logging and error handlers
    RequestLogger.setup(app)
    ErrorHandler.setup(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(api_bp, url_prefix="/api")

    # Initialize database tables if needed
    try:
        init_db()
    except Exception as e:
        # Avoid crashing if DB not reachable; web can still run
        print(f"Database initialization warning: {e}")

    @app.get("/health")
    def health():
        return {"status": "ok", "environment": config.ENVIRONMENT}

    @app.get("/readiness")
    def readiness():
        """Check if all systems are ready"""
        try:
            init_db()
            return {"ready": True, "status": "all systems operational"}
        except Exception as e:
            return {"ready": False, "status": str(e)}, 503

    return app


# For gunicorn: app object
app = create_app()
