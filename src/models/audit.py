"""
Audit logging models for compliance and security
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class AuditLog(Base):
    """Comprehensive audit log for all user actions"""
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Who
    user_id = Column(String(36), ForeignKey('users.id'), index=True)  # Null for system actions
    session_id = Column(String(36))
    
    # What
    action = Column(String(100), nullable=False, index=True)  # e.g., "payment.created", "user.login"
    resource_type = Column(String(50))  # e.g., "loan", "payment", "user"
    resource_id = Column(String(100))
    
    # When
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # How
    ip_address = Column(String(45))
    user_agent = Column(String(255))
    request_id = Column(String(36))
    
    # Details
    old_value = Column(JSON)  # State before action
    new_value = Column(JSON)  # State after action
    meta_data = Column(JSON)  # Additional context (renamed from metadata to avoid conflict)
    
    # Result
    status = Column(String(20))  # success, failure, error
    error_message = Column(Text)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs", foreign_keys=[user_id])
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "ip_address": self.ip_address,
            "status": self.status,
            "metadata": self.meta_data,
        }


class Transaction(Base):
    """
    Detailed transaction log for payment processing
    Separate from Payment for audit and reconciliation
    """
    __tablename__ = "transactions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Transaction identification
    transaction_id = Column(String(100), unique=True, nullable=False, index=True)
    idempotency_key = Column(String(100), unique=True, index=True)  # Prevent duplicates
    
    # Parties
    user_id = Column(String(36), nullable=False, index=True)
    loan_id = Column(String(100), nullable=False, index=True)
    
    # Amount details
    amount = Column(String(50), nullable=False)  # Store as string to avoid float precision issues
    currency = Column(String(3), default="USD")
    fee = Column(String(50), default="0.00")
    
    # Payment details
    payment_method = Column(String(50), nullable=False)  # bank, card, check
    payment_method_details = Column(JSON)  # Encrypted account details
    
    # Status tracking
    status = Column(String(20), default="pending", index=True)  # pending, processing, completed, failed, refunded
    status_reason = Column(Text)
    
    # Processing
    processor = Column(String(50))  # stripe, plaid, internal
    processor_transaction_id = Column(String(100))
    processor_response = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Fraud detection
    fraud_score = Column(String(10))  # 0-100 risk score
    fraud_checks = Column(JSON)  # Results of fraud checks
    
    # Reconciliation
    reconciled = Column(Boolean, default=False)
    reconciled_at = Column(DateTime)
    
    def to_dict(self):
        """Convert to dictionary (safe for API responses)"""
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "loan_id": self.loan_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "payment_method": self.payment_method,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
