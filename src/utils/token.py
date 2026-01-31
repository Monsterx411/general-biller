import jwt
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

# Generate secure SECRET_KEY if not provided
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production-min-32-chars")

class TokenManager:
    """Manage JWT token generation and validation"""
    
    @staticmethod
    def generate_token(user_id, expires_in=86400):
        """Generate a JWT token valid for 24 hours by default"""
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "iat": now,
            "exp": now + timedelta(seconds=expires_in),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def verify_token(token):
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


def token_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401
        
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        payload = TokenManager.verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        request.user_id = payload.get("user_id")
        return f(*args, **kwargs)
    
    return decorated
