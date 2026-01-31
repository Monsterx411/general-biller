# Security utilities for the application

import hashlib
import hmac
import secrets
from typing import Optional
from passlib.hash import pbkdf2_sha256

class SecurityManager:
    """Manage security operations including encryption and hashing"""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> tuple:
        """Hash a password with salt"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return hashed.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Verify a password against its hash"""
        new_hash, _ = SecurityManager.hash_password(password, salt)
        return hmac.compare_digest(new_hash, hashed)
    
    @staticmethod
    def mask_account_number(account_number: str) -> str:
        """Mask account number for display (show only last 4 digits)"""
        if len(account_number) < 4:
            return "****"
        return f"{'*' * (len(account_number) - 4)}{account_number[-4:]}"
    
    @staticmethod
    def mask_credit_card(card_number: str) -> str:
        """Mask credit card for display"""
        card_str = str(card_number).replace(" ", "")
        if len(card_str) < 8:
            return "****"
        return f"{card_str[:4]} **** **** {card_str[-4:]}"
    
    @staticmethod
    def generate_secure_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def validate_transaction(amount: float, account_balance: float, transaction_limit: float = 100000) -> dict:
        """Validate transaction against fraud rules"""
        errors = []
        
        if amount <= 0:
            errors.append("Amount must be positive")
        
        if amount > transaction_limit:
            errors.append(f"Amount exceeds transaction limit of ${transaction_limit:,.2f}")
        
        if amount > account_balance:
            errors.append("Insufficient funds")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


# Enhanced password hashing using passlib (production-ready)
def hash_password(password: str) -> str:
    """Hash password using PBKDF2-SHA256 with 100k iterations"""
    return pbkdf2_sha256.hash(password, rounds=100000)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        return pbkdf2_sha256.verify(password, password_hash)
    except Exception:
        return False


def validate_password_strength(password: str) -> dict:
    """
    Validate password meets security requirements
    Requirements: 8+ chars, uppercase, lowercase, number, special char
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        errors.append("Password must contain at least one special character")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
