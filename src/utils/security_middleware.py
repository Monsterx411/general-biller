"""
Enhanced security middleware for Flask
HTTPS enforcement, security headers, CSRF protection
"""

from flask import request, make_response
from functools import wraps
import secrets


class SecurityHeaders:
    """Add security headers to responses"""
    
    @staticmethod
    def setup(app):
        """Setup security headers middleware"""
        
        @app.after_request
        def add_security_headers(response):
            """Add security headers to all responses"""
            
            # Prevent clickjacking
            response.headers['X-Frame-Options'] = 'DENY'
            
            # Prevent MIME type sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            # Enable XSS protection
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            # Strict Transport Security (HTTPS only)
            # Only enable if running on HTTPS
            if request.is_secure:
                response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
            # Content Security Policy
            # Note: 'unsafe-inline' and 'unsafe-eval' are development-only
            # In production, use nonces or hashes for inline scripts
            if app.config.get('ENVIRONMENT') == 'production':
                response.headers['Content-Security-Policy'] = (
                    "default-src 'self'; "
                    "script-src 'self'; "
                    "style-src 'self'; "
                    "img-src 'self' data: https:; "
                    "font-src 'self'; "
                    "connect-src 'self'; "
                    "frame-ancestors 'none';"
                )
            else:
                # Development mode - allows inline scripts for debugging
                response.headers['Content-Security-Policy'] = (
                    "default-src 'self'; "
                    "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
                    "style-src 'self' 'unsafe-inline'; "
                    "img-src 'self' data: https:; "
                    "font-src 'self'; "
                    "connect-src 'self'; "
                    "frame-ancestors 'none';"
                )
            
            # Referrer Policy
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Permissions Policy
            response.headers['Permissions-Policy'] = (
                "geolocation=(), "
                "microphone=(), "
                "camera=()"
            )
            
            return response


class HTTPSRedirect:
    """Force HTTPS in production"""
    
    @staticmethod
    def setup(app):
        """Setup HTTPS redirect middleware"""
        
        @app.before_request
        def enforce_https():
            """Redirect HTTP to HTTPS in production"""
            # Only enforce in production
            if app.config.get('ENVIRONMENT') == 'production':
                if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
                    url = request.url.replace('http://', 'https://', 1)
                    return make_response(
                        {'error': 'HTTPS required', 'redirect_url': url},
                        301
                    )


class CSRFProtection:
    """
    CSRF protection middleware
    Note: For production, use Flask-WTF or similar library
    """
    
    def __init__(self):
        self.tokens = {}
    
    @staticmethod
    def generate_token():
        """Generate CSRF token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_token(token: str, session_token: str) -> bool:
        """Validate CSRF token"""
        import hmac
        if not token or not session_token:
            return False
        return hmac.compare_digest(token, session_token)


def require_https(f):
    """Decorator to require HTTPS for specific endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_secure and request.headers.get('X-Forwarded-Proto') != 'https':
            return make_response(
                {'error': 'HTTPS required for this endpoint'},
                403
            )
        return f(*args, **kwargs)
    return decorated_function


class IdempotencyHandler:
    """
    Handle idempotency keys to prevent duplicate payment processing
    """
    
    def __init__(self):
        self.processed_keys = {}  # In production, use Redis
    
    def check_idempotency(self, key: str) -> dict:
        """
        Check if idempotency key has been processed
        
        Returns:
            dict with 'processed' and optional 'result'
        """
        if key in self.processed_keys:
            return {
                'processed': True,
                'result': self.processed_keys[key]
            }
        return {'processed': False}
    
    def store_result(self, key: str, result: dict, ttl_seconds: int = 86400):
        """Store result for idempotency key"""
        # In production, use Redis with TTL
        self.processed_keys[key] = result


# Global idempotency handler
idempotency_handler = IdempotencyHandler()


def idempotent(f):
    """
    Decorator for idempotent endpoints (payments, etc.)
    Requires X-Idempotency-Key header
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        idempotency_key = request.headers.get('X-Idempotency-Key')
        
        if not idempotency_key:
            return make_response(
                {
                    'error': 'Idempotency key required',
                    'message': 'Include X-Idempotency-Key header for this operation'
                },
                400
            )
        
        # Check if already processed
        check = idempotency_handler.check_idempotency(idempotency_key)
        if check['processed']:
            return make_response(check['result'], 200)
        
        # Process request
        result = f(*args, **kwargs)
        
        # Store result
        if isinstance(result, tuple):
            response_data, status_code = result
        else:
            response_data, status_code = result, 200
        
        # Only store successful results
        if status_code == 200:
            idempotency_handler.store_result(idempotency_key, response_data)
        
        return result
    
    return decorated_function
