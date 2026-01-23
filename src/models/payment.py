from sqlalchemy import Column, Integer, String, Float
from .db import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(String(64), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(32), nullable=True)
