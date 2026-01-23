# Utility functions for validation

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    import re
    pattern = r'^[\d\s\-\+\(\)]{10,}$'
    return re.match(pattern, phone) is not None

def validate_zip_code(zip_code, country="USA"):
    """Validate zip/postal code based on country"""
    import re
    if country == "USA":
        pattern = r'^\d{5}(-\d{4})?$'
    elif country == "Canada":
        pattern = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
    else:
        return False
    return re.match(pattern, zip_code) is not None

def validate_account_number(account_number):
    """Validate account number format"""
    return len(account_number) >= 8 and account_number.isalnum()

def validate_routing_number(routing_number):
    """Validate routing number format (USA)"""
    return len(routing_number) == 9 and routing_number.isdigit()
