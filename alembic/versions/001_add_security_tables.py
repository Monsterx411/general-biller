"""Add user authentication and audit tables

Revision ID: 001_add_security_tables
Revises: 
Create Date: 2026-01-31

This migration adds:
- users table for authentication
- user_sessions table for session management
- audit_logs table for compliance
- transactions table for detailed payment tracking
- Enhanced loan and payment tables with relationships
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '001_add_security_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Upgrade database schema"""
    
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=True),
        sa.Column('mfa_enabled', sa.Boolean(), nullable=True),
        sa.Column('mfa_secret', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=True),
        sa.Column('locked_until', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create user_sessions table
    op.create_table('user_sessions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('token_hash', sa.String(length=255), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('last_activity', sa.DateTime(), nullable=True),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_sessions_user_id'), 'user_sessions', ['user_id'], unique=False)
    
    # Create audit_logs table
    op.create_table('audit_logs',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=True),
        sa.Column('session_id', sa.String(length=36), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=255), nullable=True),
        sa.Column('request_id', sa.String(length=36), nullable=True),
        sa.Column('old_value', sa.JSON(), nullable=True),
        sa.Column('new_value', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_timestamp'), 'audit_logs', ['timestamp'], unique=False)
    
    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('transaction_id', sa.String(length=100), nullable=False),
        sa.Column('idempotency_key', sa.String(length=100), nullable=True),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('loan_id', sa.String(length=100), nullable=False),
        sa.Column('amount', sa.String(length=50), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=True),
        sa.Column('fee', sa.String(length=50), nullable=True),
        sa.Column('payment_method', sa.String(length=50), nullable=False),
        sa.Column('payment_method_details', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('status_reason', sa.Text(), nullable=True),
        sa.Column('processor', sa.String(length=50), nullable=True),
        sa.Column('processor_transaction_id', sa.String(length=100), nullable=True),
        sa.Column('processor_response', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('processed_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('fraud_score', sa.String(length=10), nullable=True),
        sa.Column('fraud_checks', sa.JSON(), nullable=True),
        sa.Column('reconciled', sa.Boolean(), nullable=True),
        sa.Column('reconciled_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_transaction_id'), 'transactions', ['transaction_id'], unique=True)
    op.create_index(op.f('ix_transactions_idempotency_key'), 'transactions', ['idempotency_key'], unique=True)
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_transactions_loan_id'), 'transactions', ['loan_id'], unique=False)
    op.create_index(op.f('ix_transactions_status'), 'transactions', ['status'], unique=False)
    
    # Add columns to existing loans table if it exists
    try:
        op.add_column('loans', sa.Column('user_id', sa.String(length=36), nullable=True))
        op.add_column('loans', sa.Column('monthly_payment', sa.Float(), nullable=True))
        op.add_column('loans', sa.Column('due_date', sa.String(length=10), nullable=True))
        op.add_column('loans', sa.Column('created_at', sa.DateTime(), nullable=True))
        op.add_column('loans', sa.Column('updated_at', sa.DateTime(), nullable=True))
        op.create_index(op.f('ix_loans_user_id'), 'loans', ['user_id'], unique=False)
        op.create_foreign_key('fk_loans_user_id', 'loans', 'users', ['user_id'], ['id'])
    except Exception as e:
        print(f"Note: Could not add columns to loans table: {e}")
    
    # Add columns to existing payments table if it exists
    try:
        op.add_column('payments', sa.Column('user_id', sa.String(length=36), nullable=True))
        op.add_column('payments', sa.Column('status', sa.String(length=20), nullable=True))
        op.add_column('payments', sa.Column('transaction_id', sa.String(length=100), nullable=True))
        op.add_column('payments', sa.Column('created_at', sa.DateTime(), nullable=True))
        op.create_index(op.f('ix_payments_user_id'), 'payments', ['user_id'], unique=False)
    except Exception as e:
        print(f"Note: Could not add columns to payments table: {e}")


def downgrade():
    """Downgrade database schema"""
    
    # Remove added columns from payments table
    try:
        op.drop_index(op.f('ix_payments_user_id'), table_name='payments')
        op.drop_column('payments', 'created_at')
        op.drop_column('payments', 'transaction_id')
        op.drop_column('payments', 'status')
        op.drop_column('payments', 'user_id')
    except Exception:
        pass
    
    # Remove added columns from loans table
    try:
        op.drop_constraint('fk_loans_user_id', 'loans', type_='foreignkey')
        op.drop_index(op.f('ix_loans_user_id'), table_name='loans')
        op.drop_column('loans', 'updated_at')
        op.drop_column('loans', 'created_at')
        op.drop_column('loans', 'due_date')
        op.drop_column('loans', 'monthly_payment')
        op.drop_column('loans', 'user_id')
    except Exception:
        pass
    
    # Drop new tables
    op.drop_index(op.f('ix_transactions_status'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_loan_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_idempotency_key'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_transaction_id'), table_name='transactions')
    op.drop_table('transactions')
    
    op.drop_index(op.f('ix_audit_logs_timestamp'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    
    op.drop_index(op.f('ix_user_sessions_user_id'), table_name='user_sessions')
    op.drop_table('user_sessions')
    
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
