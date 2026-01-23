# Unit tests for utility functions
import pytest
from src.utils import (
    validate_email,
    validate_phone,
    validate_zip_code,
    validate_account_number,
    validate_routing_number,
    validate_transit_number,
    validate_institution_number,
    validate_credit_card_number,
    validate_cvv,
    validate_expiry_date,
    validate_loan_amount,
    validate_interest_rate,
    format_currency,
    SecurityManager
)

# Email validation tests
def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid.email") == False
    assert validate_email("user+tag@domain.co.uk") == True

# Phone validation tests
def test_validate_phone():
    assert validate_phone("123-456-7890") == True
    assert validate_phone("(123) 456-7890") == True
    assert validate_phone("invalid") == False

# ZIP code validation tests
def test_validate_zip_code_usa():
    assert validate_zip_code("12345", "USA") == True
    assert validate_zip_code("12345-6789", "USA") == True
    assert validate_zip_code("invalid", "USA") == False

def test_validate_zip_code_canada():
    assert validate_zip_code("K1A 0B1", "CANADA") == True
    assert validate_zip_code("K1A0B1", "CANADA") == True
    assert validate_zip_code("invalid", "CANADA") == False

# Account number validation tests
def test_validate_account_number():
    assert validate_account_number("123456789", "USA") == True
    assert validate_account_number("12345678", "USA") == True
    assert validate_account_number("123", "USA") == False
    assert validate_account_number("1234567", "CANADA") == True
    assert validate_account_number("123456", "CANADA") == False

# Routing number validation tests
def test_validate_routing_number():
    assert validate_routing_number("021000021") == True
    assert validate_routing_number("12345678") == False
    assert validate_routing_number("abcdefghi") == False

# Transit number validation tests
def test_validate_transit_number():
    assert validate_transit_number("12345") == True
    assert validate_transit_number("1234") == False
    assert validate_transit_number("123456") == False

# Institution number validation tests
def test_validate_institution_number():
    assert validate_institution_number("123") == True
    assert validate_institution_number("12") == False
    assert validate_institution_number("1234") == False

# Credit card validation tests
def test_validate_credit_card_number():
    # Valid test card numbers
    assert validate_credit_card_number("4532015112830366") == True  # Visa
    assert validate_credit_card_number("invalid") == False
    assert validate_credit_card_number("123456789") == False

def test_validate_cvv():
    assert validate_cvv("123") == True
    assert validate_cvv("1234") == True
    assert validate_cvv("12") == False
    assert validate_cvv("abc") == False

def test_validate_expiry_date():
    assert validate_expiry_date("12/27") == True  # Future date
    assert validate_expiry_date("01/30") == True
    assert validate_expiry_date("13/25") == False  # Invalid month
    assert validate_expiry_date("00/25") == False  # Invalid month
    assert validate_expiry_date("12-25") == False  # Wrong format

# Loan validation tests
def test_validate_loan_amount():
    assert validate_loan_amount(5000) == True
    assert validate_loan_amount(50) == False  # Too low
    assert validate_loan_amount(15000000) == False  # Too high
    assert validate_loan_amount("invalid") == False

def test_validate_interest_rate():
    assert validate_interest_rate(5.5) == True
    assert validate_interest_rate(0) == True
    assert validate_interest_rate(50) == True
    assert validate_interest_rate(55) == False  # Too high
    assert validate_interest_rate(-1) == False

# Formatting tests
def test_format_currency():
    assert format_currency(100.50, "USD") == "$100.50"
    assert format_currency(100.50, "CAD") == "C$100.50"

# Security tests
def test_mask_account_number():
    masked = SecurityManager.mask_account_number("123456789")
    assert masked == "*****6789"
    assert "123456789" not in masked

def test_mask_credit_card():
    masked = SecurityManager.mask_credit_card("4532015112830366")
    assert "4532" in masked
    assert "0366" in masked
    assert "0111" not in masked

def test_hash_password():
    password = "test_password_123"
    hashed, salt = SecurityManager.hash_password(password)
    assert hashed != password
    assert salt != ""
    
    # Verify password
    assert SecurityManager.verify_password(password, hashed, salt) == True
    assert SecurityManager.verify_password("wrong_password", hashed, salt) == False
