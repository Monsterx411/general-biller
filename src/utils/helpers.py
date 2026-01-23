# Helper functions

def format_currency(amount, currency="USD"):
    """Format amount as currency"""
    if currency == "USD":
        return f"${amount:,.2f}"
    elif currency == "CAD":
        return f"C${amount:,.2f}"
    return f"{amount:,.2f}"

def format_phone(phone):
    """Format phone number"""
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone

def format_address(street, city, state, zip_code, country):
    """Format address for display"""
    return f"{street}\n{city}, {state} {zip_code}\n{country}"
