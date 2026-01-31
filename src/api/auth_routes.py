"""
Authentication and user management routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import uuid
import pyotp
import qrcode
import io
import base64

from src.models.db import get_db
from src.models.user import User, UserSession
from src.models.audit import AuditLog
from src.utils.security import hash_password, verify_password, validate_password_strength
from src.utils.token import TokenManager
from src.utils.validators import validate_email
from src.utils.rate_limit import rate_limit, get_user_key

auth_bp = Blueprint("auth", __name__)


def log_audit(db, user_id, action, status, ip_address=None, context_data=None):
    """Helper to log audit events"""
    try:
        audit = AuditLog(
            user_id=user_id,
            action=action,
            status=status,
            ip_address=ip_address or request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:255],
            request_id=str(uuid.uuid4()),
            context_data=context_data
        )
        db.add(audit)
        db.commit()
    except Exception as e:
        # Log audit failure for monitoring
        print(f"AUDIT LOG FAILURE: {action} for user {user_id}: {str(e)}")
        # In production, send to monitoring service (e.g., Sentry, CloudWatch)


@auth_bp.post("/register")
@rate_limit(max_requests=5, window_seconds=3600)  # 5 registrations per hour per IP
def register():
    """
    Register a new user
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "full_name": "John Doe",
        "phone": "+1234567890"
    }
    """
    data = request.get_json(force=True)
    
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    full_name = data.get("full_name", "").strip()
    phone = data.get("phone", "").strip()
    
    # Validate required fields
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    # Validate email format
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    # Validate password strength
    password_check = validate_password_strength(password)
    if not password_check["valid"]:
        return jsonify({
            "error": "Password does not meet requirements",
            "details": password_check["errors"]
        }), 400
    
    # Check if user exists
    for db in get_db():
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            # Don't reveal if user exists (security best practice)
            return jsonify({"error": "Registration failed"}), 400
        
        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            full_name=full_name,
            phone=phone,
            is_active=True,
            is_verified=False  # Require email verification in production
        )
        user.set_password(password)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Log registration
        log_audit(db, user.id, "user.registered", "success", context_data={"email": email})
        
        return jsonify({
            "message": "Registration successful",
            "user": user.to_dict()
        }), 201


@auth_bp.post("/login")
@rate_limit(max_requests=10, window_seconds=300)  # 10 login attempts per 5 minutes
def login():
    """
    Authenticate user and return JWT token
    
    Request body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "mfa_code": "123456"  (optional, required if MFA enabled)
    }
    """
    data = request.get_json(force=True)
    
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    mfa_code = data.get("mfa_code", "").strip()
    
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400
    
    for db in get_db():
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Log failed attempt
            log_audit(db, None, "user.login_failed", "failure", 
                     context_data={"email": email, "reason": "user_not_found"})
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Check if account is locked
        if user.is_locked():
            log_audit(db, user.id, "user.login_locked", "failure",
                     context_data={"locked_until": user.locked_until.isoformat()})
            return jsonify({
                "error": "Account temporarily locked",
                "locked_until": user.locked_until.isoformat()
            }), 403
        
        # Verify password
        if not user.check_password(password):
            # Increment failed attempts
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            
            db.commit()
            
            log_audit(db, user.id, "user.login_failed", "failure",
                     context_data={"reason": "invalid_password", "attempts": user.failed_login_attempts})
            
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Check MFA if enabled
        if user.mfa_enabled:
            if not mfa_code:
                return jsonify({
                    "error": "MFA code required",
                    "mfa_required": True
                }), 400
            
            # Verify MFA code
            totp = pyotp.TOTP(user.mfa_secret)
            if not totp.verify(mfa_code, valid_window=1):
                log_audit(db, user.id, "user.login_failed", "failure",
                         context_data={"reason": "invalid_mfa"})
                return jsonify({"error": "Invalid MFA code"}), 401
        
        # Check if account is active
        if not user.is_active:
            log_audit(db, user.id, "user.login_inactive", "failure")
            return jsonify({"error": "Account is not active"}), 403
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        
        # Generate JWT token
        token = TokenManager.generate_token(user.id, expires_in=86400)
        
        # Create session
        session = UserSession(
            id=str(uuid.uuid4()),
            user_id=user.id,
            token_hash=hash_password(token)[:255],  # Store hash of token
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:255],
            expires_at=datetime.utcnow() + timedelta(seconds=86400)
        )
        db.add(session)
        db.commit()
        
        log_audit(db, user.id, "user.login_success", "success",
                 context_data={"session_id": session.id})
        
        return jsonify({
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 86400,
            "user": user.to_dict()
        }), 200


@auth_bp.post("/logout")
@rate_limit(max_requests=20, window_seconds=60)
def logout():
    """Logout user and revoke session"""
    token = None
    if "Authorization" in request.headers:
        try:
            token = request.headers["Authorization"].split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
    
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    payload = TokenManager.verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    user_id = payload.get("user_id")
    
    for db in get_db():
        # Revoke all user sessions (or just current one)
        sessions = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None)
        ).all()
        
        for session in sessions:
            session.revoke()
        
        db.commit()
        
        log_audit(db, user_id, "user.logout", "success")
        
        return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.post("/mfa/setup")
@rate_limit(max_requests=5, window_seconds=3600, key_func=get_user_key)
def setup_mfa():
    """
    Setup MFA for user
    Returns QR code for authenticator app
    """
    token = None
    if "Authorization" in request.headers:
        try:
            token = request.headers["Authorization"].split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
    
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    payload = TokenManager.verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    user_id = payload.get("user_id")
    
    for db in get_db():
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Generate TOTP secret
        secret = pyotp.random_base32()
        user.mfa_secret = secret
        
        # Generate provisioning URI
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(
            name=user.email,
            issuer_name="General Biller"
        )
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        db.commit()
        
        log_audit(db, user_id, "mfa.setup_initiated", "success")
        
        return jsonify({
            "secret": secret,
            "qr_code": f"data:image/png;base64,{qr_code_base64}",
            "provisioning_uri": provisioning_uri
        }), 200


@auth_bp.post("/mfa/enable")
@rate_limit(max_requests=5, window_seconds=300, key_func=get_user_key)
def enable_mfa():
    """
    Enable MFA after verifying code
    
    Request body:
    {
        "code": "123456"
    }
    """
    token = None
    if "Authorization" in request.headers:
        try:
            token = request.headers["Authorization"].split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
    
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    payload = TokenManager.verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    user_id = payload.get("user_id")
    data = request.get_json(force=True)
    code = data.get("code", "").strip()
    
    if not code:
        return jsonify({"error": "MFA code is required"}), 400
    
    for db in get_db():
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if not user.mfa_secret:
            return jsonify({"error": "MFA not set up. Call /mfa/setup first"}), 400
        
        # Verify code
        totp = pyotp.TOTP(user.mfa_secret)
        if not totp.verify(code, valid_window=1):
            log_audit(db, user_id, "mfa.enable_failed", "failure",
                     context_data={"reason": "invalid_code"})
            return jsonify({"error": "Invalid MFA code"}), 401
        
        # Enable MFA
        user.mfa_enabled = True
        db.commit()
        
        log_audit(db, user_id, "mfa.enabled", "success")
        
        return jsonify({"message": "MFA enabled successfully"}), 200


@auth_bp.post("/mfa/disable")
@rate_limit(max_requests=3, window_seconds=3600, key_func=get_user_key)
def disable_mfa():
    """
    Disable MFA (requires password confirmation)
    
    Request body:
    {
        "password": "current_password"
    }
    """
    token = None
    if "Authorization" in request.headers:
        try:
            token = request.headers["Authorization"].split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
    
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    payload = TokenManager.verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    user_id = payload.get("user_id")
    data = request.get_json(force=True)
    password = data.get("password", "")
    
    if not password:
        return jsonify({"error": "Password is required"}), 400
    
    for db in get_db():
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Verify password
        if not user.check_password(password):
            log_audit(db, user_id, "mfa.disable_failed", "failure",
                     context_data={"reason": "invalid_password"})
            return jsonify({"error": "Invalid password"}), 401
        
        # Disable MFA
        user.mfa_enabled = False
        user.mfa_secret = None
        db.commit()
        
        log_audit(db, user_id, "mfa.disabled", "success")
        
        return jsonify({"message": "MFA disabled successfully"}), 200


@auth_bp.get("/profile")
@rate_limit(max_requests=30, window_seconds=60, key_func=get_user_key)
def get_profile():
    """Get user profile"""
    token = None
    if "Authorization" in request.headers:
        try:
            token = request.headers["Authorization"].split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401
    
    if not token:
        return jsonify({"error": "Token is missing"}), 401
    
    payload = TokenManager.verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    user_id = payload.get("user_id")
    
    for db in get_db():
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user.to_dict()), 200
