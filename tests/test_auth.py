"""
Tests for authentication and security features
"""

import pytest
import json
from src.api.app import create_app
from src.models.db import get_db, init_db
from src.models.user import User


@pytest.fixture
def app():
    """Create test application"""
    import os
    os.environ['ENVIRONMENT'] = 'testing'
    os.environ['DATABASE_URL'] = 'sqlite:///test_auth.db'
    
    app = create_app()
    app.config['TESTING'] = True
    
    with app.app_context():
        init_db()
    
    yield app
    
    # Cleanup
    try:
        os.remove('test_auth.db')
    except FileNotFoundError:
        pass  # File doesn't exist, which is fine
    except Exception as e:
        print(f"Warning: Could not remove test database: {e}")


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestUserRegistration:
    """Test user registration"""
    
    def test_register_success(self, client):
        """Test successful registration"""
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'full_name': 'Test User',
            'phone': '+1234567890'
        })
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['email'] == 'test@example.com'
        assert data['user']['is_verified'] == False
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/api/auth/register', json={
            'email': 'test2@example.com',
            'password': 'weak',
            'full_name': 'Test User'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Password does not meet requirements' in data['error']
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email"""
        response = client.post('/api/auth/register', json={
            'email': 'invalid-email',
            'password': 'SecurePass123!',
            'full_name': 'Test User'
        })
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Invalid email format' in data['error']
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email"""
        # Register first user
        client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'SecurePass123!',
            'full_name': 'User 1'
        })
        
        # Try to register with same email
        response = client.post('/api/auth/register', json={
            'email': 'duplicate@example.com',
            'password': 'SecurePass456!',
            'full_name': 'User 2'
        })
        
        assert response.status_code == 400


class TestUserLogin:
    """Test user login"""
    
    def setup_method(self):
        """Create test user before each test"""
        self.test_email = 'login@example.com'
        self.test_password = 'SecurePass123!'
    
    def test_login_success(self, client):
        """Test successful login"""
        # Register user
        client.post('/api/auth/register', json={
            'email': self.test_email,
            'password': self.test_password,
            'full_name': 'Login Test'
        })
        
        # Login
        response = client.post('/api/auth/login', json={
            'email': self.test_email,
            'password': self.test_password
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        assert 'expires_in' in data
        assert data['token_type'] == 'Bearer'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'WrongPass123!'
        })
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid credentials' in data['error']
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register user
        client.post('/api/auth/register', json={
            'email': self.test_email,
            'password': self.test_password,
            'full_name': 'Test User'
        })
        
        # Try login with wrong password
        response = client.post('/api/auth/login', json={
            'email': self.test_email,
            'password': 'WrongPass123!'
        })
        
        assert response.status_code == 401


class TestAccountLockout:
    """Test account lockout after failed attempts"""
    
    def test_account_lockout(self, client):
        """Test account locks after 5 failed attempts"""
        email = 'lockout@example.com'
        password = 'SecurePass123!'
        
        # Register user
        client.post('/api/auth/register', json={
            'email': email,
            'password': password,
            'full_name': 'Lockout Test'
        })
        
        # Try 5 failed logins
        for i in range(5):
            response = client.post('/api/auth/login', json={
                'email': email,
                'password': 'WrongPassword123!'
            })
            assert response.status_code == 401
        
        # 6th attempt should show account locked
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password  # Even with correct password
        })
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'locked' in data['error'].lower()


class TestMFA:
    """Test multi-factor authentication"""
    
    def get_auth_token(self, client):
        """Helper to get auth token"""
        email = 'mfa@example.com'
        password = 'SecurePass123!'
        
        # Register
        client.post('/api/auth/register', json={
            'email': email,
            'password': password,
            'full_name': 'MFA Test'
        })
        
        # Login
        response = client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })
        
        data = json.loads(response.data)
        return data['access_token']
    
    def test_mfa_setup(self, client):
        """Test MFA setup"""
        token = self.get_auth_token(client)
        
        response = client.post('/api/auth/mfa/setup',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'secret' in data
        assert 'qr_code' in data
        assert 'provisioning_uri' in data
    
    def test_mfa_setup_unauthorized(self, client):
        """Test MFA setup without authentication"""
        response = client.post('/api/auth/mfa/setup')
        
        assert response.status_code == 401


class TestRateLimiting:
    """Test rate limiting"""
    
    def test_registration_rate_limit(self, client):
        """Test registration rate limiting"""
        # Try to register 6 times quickly (limit is 5 per hour)
        for i in range(6):
            response = client.post('/api/auth/register', json={
                'email': f'ratelimit{i}@example.com',
                'password': 'SecurePass123!',
                'full_name': f'User {i}'
            })
            
            if i < 5:
                assert response.status_code in [201, 400]  # 400 if duplicate
            else:
                # 6th request should be rate limited
                assert response.status_code == 429
                data = json.loads(response.data)
                assert 'Rate limit exceeded' in data['error']


class TestEncryption:
    """Test data encryption"""
    
    def test_password_hashing(self):
        """Test password is hashed, not stored in plaintext"""
        from src.utils.security import hash_password, verify_password
        
        password = 'SecurePass123!'
        hashed = hash_password(password)
        
        # Hash should be different from password
        assert hashed != password
        
        # Should verify correctly
        assert verify_password(password, hashed)
        
        # Should not verify with wrong password
        assert not verify_password('WrongPass123!', hashed)
    
    def test_account_masking(self):
        """Test account number masking"""
        from src.utils.encryption import get_encryption
        
        encryption = get_encryption()
        account_number = '1234567890'
        
        masked = encryption.mask_account_number(account_number)
        assert masked == '******7890'
        assert len(masked) == len(account_number)
    
    def test_data_encryption_decryption(self):
        """Test data encryption and decryption"""
        from src.utils.encryption import get_encryption
        
        encryption = get_encryption()
        sensitive_data = '1234567890'
        
        # Encrypt
        encrypted = encryption.encrypt(sensitive_data)
        assert encrypted != sensitive_data
        
        # Decrypt
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == sensitive_data


class TestAuditLogging:
    """Test audit logging"""
    
    def test_login_audit_log(self, client, app):
        """Test login creates audit log"""
        email = 'audit@example.com'
        password = 'SecurePass123!'
        
        # Register
        client.post('/api/auth/register', json={
            'email': email,
            'password': password,
            'full_name': 'Audit Test'
        })
        
        # Login
        client.post('/api/auth/login', json={
            'email': email,
            'password': password
        })
        
        # Check audit log
        with app.app_context():
            from src.models.audit import AuditLog
            for db in get_db():
                logs = db.query(AuditLog).filter(
                    AuditLog.action == 'user.login_success'
                ).all()
                
                assert len(logs) > 0
                log = logs[0]
                assert log.status == 'success'
                assert log.ip_address is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
