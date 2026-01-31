import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///loan_manager.db")

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


def init_db():
    """Initialize all database tables"""
    from .loan import Loan
    from .payment import Payment
    from .user import User, UserSession
    from .audit import AuditLog, Transaction
    Base.metadata.create_all(bind=engine)


def get_db():
    """Yield a SQLAlchemy session and ensure proper close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
