"""
Rate limiting middleware for API protection
Prevents abuse and DoS attacks
"""

from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import threading


class RateLimiter:
    """
    In-memory rate limiter (use Redis in production)
    Implements sliding window rate limiting
    """
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_rate_limited(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if key has exceeded rate limit
        
        Args:
            key: Identifier (IP address, user ID, etc.)
            max_requests: Maximum requests allowed in window
            window_seconds: Time window in seconds
            
        Returns:
            True if rate limited, False otherwise
        """
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window_seconds)
        
        with self.lock:
            # Remove old requests outside the window
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff
            ]
            
            # Check if limit exceeded
            if len(self.requests[key]) >= max_requests:
                return True
            
            # Add current request
            self.requests[key].append(now)
            return False
    
    def get_remaining(self, key: str, max_requests: int, window_seconds: int) -> int:
        """Get remaining requests in current window"""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=window_seconds)
        
        with self.lock:
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff
            ]
            return max(0, max_requests - len(self.requests[key]))
    
    def reset(self, key: str = None):
        """Reset rate limit for key or all keys"""
        with self.lock:
            if key:
                self.requests[key] = []
            else:
                self.requests.clear()


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 100, window_seconds: int = 60, key_func=None):
    """
    Decorator for rate limiting endpoints
    
    Args:
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
        key_func: Function to generate rate limit key (default: IP address)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Determine rate limit key
            if key_func:
                key = key_func()
            else:
                # Default: use IP address
                key = request.remote_addr or "unknown"
            
            # Check rate limit
            if rate_limiter.is_rate_limited(key, max_requests, window_seconds):
                remaining = rate_limiter.get_remaining(key, max_requests, window_seconds)
                return jsonify({
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. Try again later.",
                    "retry_after": window_seconds
                }), 429
            
            # Add rate limit headers
            response = f(*args, **kwargs)
            if isinstance(response, tuple):
                response_obj, status_code = response[0], response[1] if len(response) > 1 else 200
            else:
                response_obj, status_code = response, 200
            
            remaining = rate_limiter.get_remaining(key, max_requests, window_seconds)
            
            # Add headers (if returning response object)
            if hasattr(response_obj, 'headers'):
                response_obj.headers['X-RateLimit-Limit'] = str(max_requests)
                response_obj.headers['X-RateLimit-Remaining'] = str(remaining)
                response_obj.headers['X-RateLimit-Reset'] = str(window_seconds)
            
            return response_obj, status_code if isinstance(response, tuple) else response_obj
        
        return decorated_function
    return decorator


def get_user_key():
    """Get rate limit key from authenticated user"""
    user_id = getattr(request, 'user_id', None)
    if user_id:
        return f"user:{user_id}"
    return request.remote_addr or "unknown"
