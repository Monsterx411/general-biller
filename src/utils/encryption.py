"""
Encryption utilities for sensitive data protection
PCI DSS compliant field-level encryption
"""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from src.config import get_config


class DataEncryption:
    """
    Handles encryption/decryption of sensitive data (account numbers, routing numbers)
    Uses Fernet (AES-128 CBC with HMAC) for symmetric encryption
    """
    
    def __init__(self):
        config = get_config()
        encryption_key = config.ENCRYPTION_KEY
        
        if not encryption_key:
            # Generate a key for development only (production must set ENCRYPTION_KEY)
            print("WARNING: No ENCRYPTION_KEY set. Generating temporary key for development.")
            encryption_key = Fernet.generate_key().decode()
        
        # Ensure key is properly formatted
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()
        
        self.cipher = Fernet(encryption_key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt sensitive data
        
        Args:
            plaintext: The data to encrypt
            
        Returns:
            Base64 encoded encrypted string
        """
        if not plaintext:
            return plaintext
            
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()
            
        encrypted = self.cipher.encrypt(plaintext)
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt sensitive data
        
        Args:
            encrypted_text: Base64 encoded encrypted string
            
        Returns:
            Decrypted plaintext string
        """
        if not encrypted_text:
            return encrypted_text
            
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            # Log error but don't expose details
            print(f"Decryption error: {type(e).__name__}")
            return None
    
    def mask_account_number(self, account_number: str, visible_digits: int = 4) -> str:
        """
        Mask account number showing only last N digits
        
        Args:
            account_number: Full account number
            visible_digits: Number of digits to show at end
            
        Returns:
            Masked account number (e.g., "****5678")
        """
        if not account_number or len(account_number) <= visible_digits:
            return account_number
            
        mask_length = len(account_number) - visible_digits
        return "*" * mask_length + account_number[-visible_digits:]
    
    def mask_card_number(self, card_number: str) -> str:
        """
        Mask credit card number (PCI DSS compliant)
        Shows first 6 and last 4 digits
        
        Args:
            card_number: Full card number
            
        Returns:
            Masked card number (e.g., "424242******4242")
        """
        if not card_number or len(card_number) < 10:
            return card_number
            
        # PCI DSS allows first 6 and last 4
        visible_start = min(6, len(card_number) - 4)
        visible_end = 4
        
        masked_length = len(card_number) - visible_start - visible_end
        return card_number[:visible_start] + "*" * masked_length + card_number[-visible_end:]


# Singleton instance
_encryption_instance = None

def get_encryption():
    """Get or create encryption instance"""
    global _encryption_instance
    if _encryption_instance is None:
        _encryption_instance = DataEncryption()
    return _encryption_instance
