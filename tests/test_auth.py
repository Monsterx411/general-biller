"""
Authentication and Token Management Tests
"""

import pytest
import jwt
from datetime import datetime, timedelta
from src.utils.token import TokenManager, token_required, SECRET_KEY
from flask import Flask, jsonify
import json

@pytest.fixture
def app():
    """Create test Flask app"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    
    @app.route('/public')
    def public():
        return jsonify({"message": "public endpoint"})
    
    @app.route('/protected')
    @token_required
    def protected():
        return jsonify({"message": "protected endpoint"})
    
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

class TestTokenGeneration:
    """Test token generation functionality"""
    
    def test_generate_token_default_expiry(self):
        """Test token generation with default expiry (24 hours)"""
        user_id = "test-user-123"
        token = TokenManager.generate_token(user_id)
        
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        assert payload["user_id"] == user_id
        assert "iat" in payload
        assert "exp" in payload
    
    def test_generate_token_custom_expiry(self):
        """Test token generation with custom expiry time"""
        user_id = "test-user-456"
        expires_in = 3600  # 1 hour
        token = TokenManager.generate_token(user_id, expires_in=expires_in)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Verify expiry time is approximately 1 hour from now
        exp_time = datetime.fromtimestamp(payload["exp"])
        iat_time = datetime.fromtimestamp(payload["iat"])
        time_diff = (exp_time - iat_time).total_seconds()
        
        assert abs(time_diff - expires_in) < 2  # Allow 2 second tolerance
    
    def test_generate_token_different_users(self):
        """Test that different users get different tokens"""
        token1 = TokenManager.generate_token("user1")
        token2 = TokenManager.generate_token("user2")
        
        assert token1 != token2
        
        payload1 = jwt.decode(token1, SECRET_KEY, algorithms=["HS256"])
        payload2 = jwt.decode(token2, SECRET_KEY, algorithms=["HS256"])
        
        assert payload1["user_id"] == "user1"
        assert payload2["user_id"] == "user2"

class TestTokenVerification:
    """Test token verification functionality"""
    
    def test_verify_valid_token(self):
        """Test verification of a valid token"""
        user_id = "test-user-789"
        token = TokenManager.generate_token(user_id)
        
        payload = TokenManager.verify_token(token)
        
        assert payload is not None
        assert payload["user_id"] == user_id
    
    def test_verify_expired_token(self):
        """Test verification of an expired token"""
        user_id = "test-user-expired"
        
        # Create an expired token (expired 1 hour ago)
        payload = {
            "user_id": user_id,
            "iat": datetime.utcnow() - timedelta(hours=2),
            "exp": datetime.utcnow() - timedelta(hours=1),
        }
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        result = TokenManager.verify_token(expired_token)
        assert result is None
    
    def test_verify_invalid_token(self):
        """Test verification of an invalid token"""
        invalid_token = "invalid.token.string"
        
        result = TokenManager.verify_token(invalid_token)
        assert result is None
    
    def test_verify_tampered_token(self):
        """Test verification of a tampered token"""
        token = TokenManager.generate_token("test-user")
        
        # Tamper with the token by adding characters
        tampered_token = token + "tampered"
        
        result = TokenManager.verify_token(tampered_token)
        assert result is None
    
    def test_verify_wrong_secret(self):
        """Test token created with different secret fails verification"""
        # Create token with different secret
        payload = {
            "user_id": "test-user",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        wrong_token = jwt.encode(payload, "wrong-secret-key", algorithm="HS256")
        
        result = TokenManager.verify_token(wrong_token)
        assert result is None

class TestTokenRequiredDecorator:
    """Test the token_required decorator"""
    
    def test_access_public_endpoint(self, client):
        """Test accessing public endpoint without token"""
        response = client.get('/public')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "public endpoint"
    
    def test_access_protected_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get('/protected')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "missing" in data["error"].lower()
    
    def test_access_protected_with_valid_token(self, client):
        """Test accessing protected endpoint with valid token"""
        token = TokenManager.generate_token("test-user")
        
        response = client.get(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "protected endpoint"
    
    def test_access_protected_with_expired_token(self, client):
        """Test accessing protected endpoint with expired token"""
        # Create expired token
        payload = {
            "user_id": "test-user",
            "iat": datetime.utcnow() - timedelta(hours=2),
            "exp": datetime.utcnow() - timedelta(hours=1),
        }
        expired_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        
        response = client.get(
            '/protected',
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
    
    def test_access_protected_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        response = client.get(
            '/protected',
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        
        assert response.status_code == 401
    
    def test_access_protected_with_malformed_header(self, client):
        """Test accessing protected endpoint with malformed authorization header"""
        token = TokenManager.generate_token("test-user")
        
        # Missing "Bearer" prefix
        response = client.get(
            '/protected',
            headers={"Authorization": token}
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
        assert "format" in data["error"].lower()
    
    def test_access_protected_with_empty_token(self, client):
        """Test accessing protected endpoint with empty token"""
        response = client.get(
            '/protected',
            headers={"Authorization": "Bearer "}
        )
        
        assert response.status_code == 401

class TestSecurityBestPractices:
    """Test security best practices implementation"""
    
    def test_token_contains_no_sensitive_data(self):
        """Verify token doesn't contain sensitive information in plain text"""
        user_id = "test-user"
        token = TokenManager.generate_token(user_id)
        
        # Token should be encoded, not contain user_id in plain text
        assert user_id not in token
    
    def test_different_tokens_for_same_user(self):
        """Verify that generating multiple tokens for same user produces different tokens"""
        user_id = "test-user"
        
        import time
        token1 = TokenManager.generate_token(user_id)
        time.sleep(1)  # Ensure different iat timestamp
        token2 = TokenManager.generate_token(user_id)
        
        # Tokens should be different due to different iat timestamps
        assert token1 != token2
    
    def test_token_expiry_enforced(self):
        """Verify token expiry is properly enforced"""
        # Create token that expires in 1 second
        token = TokenManager.generate_token("test-user", expires_in=1)
        
        # Should be valid immediately
        payload = TokenManager.verify_token(token)
        assert payload is not None
        
        # Should be invalid after expiry (wait 2 seconds to be safe)
        import time
        time.sleep(2)
        payload = TokenManager.verify_token(token)
        assert payload is None

# Integration test
class TestAuthenticationFlow:
    """Test complete authentication flow"""
    
    def test_complete_auth_flow(self, client):
        """Test a complete authentication flow"""
        # Step 1: Generate token
        user_id = "integration-test-user"
        token = TokenManager.generate_token(user_id)
        assert token is not None
        
        # Step 2: Use token to access protected resource
        response = client.get(
            '/protected',
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        # Step 3: Verify token can be decoded
        payload = TokenManager.verify_token(token)
        assert payload["user_id"] == user_id

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
