"""
User model for authentication and authorization
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from src.utils.security import hash_password, verify_password


class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    full_name = Column(String(255))
    phone = Column(String(20))
    
    # Security
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(32))  # TOTP secret (encrypted in production)
    
    # Audit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime)
    
    # Relationships
    loans = relationship("Loan", back_populates="user")
    sessions = relationship("UserSession", back_populates="user", foreign_keys='UserSession.user_id')
    audit_logs = relationship("AuditLog", back_populates="user", foreign_keys='AuditLog.user_id')
    
    def set_password(self, password: str):
        """Hash and set password"""
        self.password_hash = hash_password(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        return verify_password(password, self.password_hash)
    
    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        data = {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "phone": self.phone,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "mfa_enabled": self.mfa_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
        
        if include_sensitive:
            data["is_locked"] = self.is_locked()
            data["failed_attempts"] = self.failed_login_attempts
            
        return data


class UserSession(Base):
    """User session tracking"""
    __tablename__ = "user_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)  # Hashed JWT token
    
    # Session info
    ip_address = Column(String(45))  # IPv6 compatible
    user_agent = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="sessions", foreign_keys=[user_id])
    
    def is_valid(self) -> bool:
        """Check if session is still valid"""
        now = datetime.utcnow()
        return (
            self.revoked_at is None and
            self.expires_at > now
        )
    
    def revoke(self):
        """Revoke this session"""
        self.revoked_at = datetime.utcnow()
