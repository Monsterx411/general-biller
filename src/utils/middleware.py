import logging
import uuid
from flask import request, g
from datetime import datetime

logger = logging.getLogger(__name__)

class RequestLogger:
    """Log HTTP requests with unique IDs"""
    
    @staticmethod
    def setup(app):
        """Register logging before/after request handlers"""
        
        @app.before_request
        def before_request():
            g.request_id = str(uuid.uuid4())
            g.start_time = datetime.utcnow()
            logger.info(f"[{g.request_id}] {request.method} {request.path}")
        
        @app.after_request
        def after_request(response):
            if hasattr(g, "start_time"):
                elapsed = (datetime.utcnow() - g.start_time).total_seconds()
                logger.info(
                    f"[{g.request_id}] {request.method} {request.path} "
                    f"{response.status_code} ({elapsed:.3f}s)"
                )
            return response


class ErrorHandler:
    """Global error handler"""
    
    @staticmethod
    def setup(app):
        """Register error handlers"""
        
        @app.errorhandler(400)
        def bad_request(error):
            return {"error": "Bad request", "message": str(error)}, 400
        
        @app.errorhandler(401)
        def unauthorized(error):
            return {"error": "Unauthorized", "message": str(error)}, 401
        
        @app.errorhandler(404)
        def not_found(error):
            return {"error": "Not found", "message": str(error)}, 404
        
        @app.errorhandler(500)
        def internal_error(error):
            logger.exception("Internal server error")
            return {"error": "Internal server error", "message": "An error occurred"}, 500
