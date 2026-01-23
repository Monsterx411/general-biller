# Credit Card Loan Payment Processing

class CreditCardLoanPayment:
    """Handle credit card loan/debt payments"""
    
    def __init__(self):
        self.card_details = {}
        self.payment_method = {}  # Card to make payment from
        self.loan_accounts = []  # Multiple credit card accounts
    
    def add_credit_card_loan(self, card_issuer, card_last_4, balance, min_payment, interest_rate, due_date):
        """Add a credit card loan account to track"""
        loan = {
            "card_issuer": card_issuer,
            "card_last_4": card_last_4,
            "balance": balance,
            "min_payment": min_payment,
            "interest_rate": interest_rate,
            "due_date": due_date
        }
        self.loan_accounts.append(loan)
        return loan
    
    def set_payment_method(self, card_number, expiry, cvv, billing_address):
        """Set the card to use for making payments"""
        self.payment_method = {
            "card_number": card_number[-4:],
            "expiry": expiry,
            "cvv": cvv,
            "billing_address": billing_address
        }
    
    def process_payment(self, card_issuer, amount):
        """Process payment towards credit card loan"""
        for loan in self.loan_accounts:
            if loan["card_issuer"] == card_issuer:
                loan["balance"] -= amount
                return {
                    "status": "success",
                    "amount_paid": amount,
                    "remaining_balance": loan["balance"]
                }
        return {"status": "error", "message": "Loan account not found"}
    
    def get_loan_details(self, card_issuer):
        """Get details of a specific credit card loan"""
        for loan in self.loan_accounts:
            if loan["card_issuer"] == card_issuer:
                return loan
        return None
