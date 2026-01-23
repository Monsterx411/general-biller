# Utility functions for validation

import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\d\s\-\+\(\)]{10,}$'
    return re.match(pattern, phone) is not None

def validate_zip_code(zip_code, country="USA"):
    """Validate zip/postal code based on country"""
    if country.upper() == "USA":
        pattern = r'^\d{5}(-\d{4})?$'
    elif country.upper() == "CANADA":
        pattern = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
    else:
        return False
    return re.match(pattern, zip_code) is not None

def validate_account_number(account_number, country="USA"):
    """Validate account number format"""
    account_number = str(account_number).strip()
    if country.upper() == "USA":
        return 8 <= len(account_number) <= 17 and account_number.isalnum()
    elif country.upper() == "CANADA":
        return 7 <= len(account_number) <= 12 and account_number.isalnum()
    return False

def validate_routing_number(routing_number):
    """Validate routing number format (USA - 9 digits)"""
    routing_str = str(routing_number).strip()
    return len(routing_str) == 9 and routing_str.isdigit()

def validate_transit_number(transit_number):
    """Validate transit number format (Canada - 5 digits)"""
    transit_str = str(transit_number).strip()
    return len(transit_str) == 5 and transit_str.isdigit()

def validate_institution_number(institution_number):
    """Validate Canadian institution number (3 digits)"""
    inst_str = str(institution_number).strip()
    return len(inst_str) == 3 and inst_str.isdigit()

def validate_credit_card_number(card_number):
    """Validate credit card using Luhn algorithm"""
    card_str = str(card_number).replace(" ", "").replace("-", "")
    if not card_str.isdigit() or len(card_str) < 13 or len(card_str) > 19:
        return False
    
    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    return luhn_checksum(card_str) == 0

def validate_cvv(cvv):
    """Validate CVV (3-4 digits)"""
    cvv_str = str(cvv).strip()
    return len(cvv_str) in [3, 4] and cvv_str.isdigit()

def validate_expiry_date(expiry_date):
    """Validate credit card expiry date (MM/YY format)"""
    try:
        if len(expiry_date) != 5 or expiry_date[2] != '/':
            return False
        month, year = expiry_date.split('/')
        month = int(month)
        year = int(year)
        
        if month < 1 or month > 12:
            return False
        
        current_year = datetime.now().year % 100
        current_month = datetime.now().month
        
        if year < current_year or (year == current_year and month < current_month):
            return False
        
        if year > current_year + 20:  # Cards valid for max 20 years
            return False
        
        return True
    except (ValueError, IndexError):
        return False

def validate_loan_amount(amount):
    """Validate loan amount is positive and reasonable"""
    try:
        amount = float(amount)
        return 100 <= amount <= 10000000  # Between $100 and $10M
    except (ValueError, TypeError):
        return False

def validate_interest_rate(rate):
    """Validate interest rate is reasonable"""
    try:
        rate = float(rate)
        return 0 <= rate <= 50  # Between 0% and 50%
    except (ValueError, TypeError):
        return False

def validate_date_format(date_str):
    """Validate date format (MM/DD)"""
    try:
        if len(date_str) != 5 or date_str[2] != '/':
            return False
        month, day = date_str.split('/')
        month = int(month)
        day = int(day)
        return 1 <= month <= 12 and 1 <= day <= 31
    except (ValueError, IndexError):
        return False
