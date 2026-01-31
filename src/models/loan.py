from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(String(64), unique=True, nullable=False)
    loan_type = Column(String(32), nullable=False)  # credit_card, personal, mortgage, auto
    balance = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    
    # User relationship
    user_id = Column(String(36), ForeignKey('users.id'), index=True)
    user = relationship("User", back_populates="loans")
    
    # Additional fields
    monthly_payment = Column(Float)
    due_date = Column(String(10))  # MM/DD format
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "loan_id": self.loan_id,
            "loan_type": self.loan_type,
            "balance": self.balance,
            "interest_rate": self.interest_rate,
            "monthly_payment": self.monthly_payment,
            "due_date": self.due_date,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
