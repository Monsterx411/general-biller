# Security utilities for the application

import hashlib
import hmac
import secrets
from typing import Optional

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
