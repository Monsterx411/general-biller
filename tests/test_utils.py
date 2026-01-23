# Unit tests for utility functions
import pytest
from src.utils import (
    validate_email,
    validate_phone,
    validate_zip_code,
    validate_account_number,
    format_currency
)

def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid.email") == False

def test_validate_phone():
    assert validate_phone("123-456-7890") == True
    assert validate_phone("invalid") == False

def test_validate_zip_code_usa():
    assert validate_zip_code("12345", "USA") == True
    assert validate_zip_code("12345-6789", "USA") == True

def test_validate_account_number():
    assert validate_account_number("123456789") == True
    assert validate_account_number("123") == False

def test_format_currency():
    assert format_currency(100.50, "USD") == "$100.50"
    assert format_currency(100.50, "CAD") == "C$100.50"
