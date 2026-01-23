# Credit Card Loan Payment Processing - Production Grade

from datetime import datetime
from src.utils.validators import validate_credit_card_number, validate_cvv, validate_expiry_date
from src.utils.security import SecurityManager

class CreditCardLoanPayment:
    """Handle credit card loan/debt payments with validation and security"""
    
    def __init__(self):
        self.card_details = {}
        self.payment_method = {}
        self.loan_accounts = []
        self.transaction_history = []
        self.max_transaction = 100000  # $100k limit
    
    def add_credit_card_loan(self, card_issuer, card_last_4, balance, min_payment, interest_rate, due_date):
        """Add a credit card loan account to track"""
        try:
            balance = float(balance)
            min_payment = float(min_payment)
            interest_rate = float(interest_rate)
            
            if balance < 0:
                return {"status": "error", "message": "Balance cannot be negative"}
            if min_payment < 0:
                return {"status": "error", "message": "Minimum payment cannot be negative"}
            if not (0 <= interest_rate <= 100):
                return {"status": "error", "message": "Interest rate must be between 0 and 100"}
            
            loan = {
                "card_issuer": card_issuer,
                "card_last_4": str(card_last_4),
                "balance": balance,
                "min_payment": min_payment,
                "interest_rate": interest_rate,
                "due_date": due_date,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
            self.loan_accounts.append(loan)
            return {"status": "success", "message": f"{card_issuer} loan added", "loan": loan}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid input: {str(e)}"}
    
    def set_payment_method(self, card_number, expiry, cvv, billing_address):
        """Set the card to use for making payments with validation"""
        try:
            if not validate_credit_card_number(card_number):
                return {"status": "error", "message": "Invalid credit card number"}
            
            if not validate_expiry_date(expiry):
                return {"status": "error", "message": "Invalid or expired card"}
            
            if not validate_cvv(cvv):
                return {"status": "error", "message": "Invalid CVV"}
            
            self.payment_method = {
                "card_number": SecurityManager.mask_credit_card(card_number),
                "card_last_4": str(card_number)[-4:],
                "expiry": expiry,
                "billing_address": billing_address,
                "validated": True,
                "set_at": datetime.now().isoformat()
            }
            return {"status": "success", "message": "Payment method set"}
        except Exception as e:
            return {"status": "error", "message": f"Failed to set payment method: {str(e)}"}
    
    def process_payment(self, card_issuer, amount):
        """Process payment towards credit card loan"""
        try:
            amount = float(amount)
            
            if amount <= 0:
                return {"status": "error", "message": "Payment amount must be positive"}
            
            if amount > self.max_transaction:
                return {"status": "error", "message": f"Amount exceeds transaction limit of ${self.max_transaction:,.2f}"}
            
            if not self.payment_method:
                return {"status": "error", "message": "Payment method not configured"}
            
            for loan in self.loan_accounts:
                if loan["card_issuer"] == card_issuer:
                    if loan["status"] != "active":
                        return {"status": "error", "message": "Loan account is not active"}
                    
                    if amount > loan["balance"]:
                        return {"status": "warning", "message": f"Payment exceeds balance. Balance: ${loan['balance']:,.2f}"}
                    
                    old_balance = loan["balance"]
                    loan["balance"] -= amount
                    
                    transaction = {
                        "transaction_id": f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "card_issuer": card_issuer,
                        "amount": amount,
                        "old_balance": old_balance,
                        "new_balance": loan["balance"],
                        "timestamp": datetime.now().isoformat(),
                        "status": "completed"
                    }
                    self.transaction_history.append(transaction)
                    
                    return {
                        "status": "success",
                        "transaction_id": transaction["transaction_id"],
                        "amount_paid": amount,
                        "remaining_balance": loan["balance"],
                        "timestamp": transaction["timestamp"]
                    }
            
            return {"status": "error", "message": "Loan account not found"}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid amount: {str(e)}"}
    
    def get_loan_details(self, card_issuer):
        """Get details of a specific credit card loan"""
        for loan in self.loan_accounts:
            if loan["card_issuer"] == card_issuer:
                return loan
        return None
    
    def get_transaction_history(self, card_issuer=None):
        """Get transaction history"""
        if card_issuer:
            return [t for t in self.transaction_history if t["card_issuer"] == card_issuer]
        return self.transaction_history
