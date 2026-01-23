from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(String(64), unique=True, nullable=False)
    loan_type = Column(String(32), nullable=False)  # credit_card, personal, mortgage, auto
    balance = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
