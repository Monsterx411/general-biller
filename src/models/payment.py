from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .db import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(String(64), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(32), nullable=True)
    
    # Enhanced fields
    user_id = Column(String(36), index=True)
    status = Column(String(20), default="completed")  # completed, pending, failed
    transaction_id = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "amount": self.amount,
            "method": self.method,
            "status": self.status,
            "transaction_id": self.transaction_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
