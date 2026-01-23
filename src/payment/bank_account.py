# Personal and General Loan Payment Processing - Production Grade

from datetime import datetime
from src.utils.validators import (
    validate_account_number, validate_routing_number, 
    validate_transit_number, validate_institution_number,
    validate_loan_amount, validate_interest_rate
)
from src.utils.security import SecurityManager

class PersonalLoanPayment:
    """Handle personal loan payments via bank account transfer with validation"""
    
    def __init__(self, country="USA"):
        self.country = country.upper()
        self.bank_account = {}
        self.loans = []
        self.transaction_history = []
        self.max_transaction = 100000  # $100k limit
    
    def set_usa_bank_account(self, bank_name, account_type, account_number, routing_number, owner_name, address, available_balance):
        """Set USA bank account for making payments with validation"""
        try:
            if not validate_account_number(account_number, "USA"):
                return {"status": "error", "message": "Invalid USA account number"}
            
            if not validate_routing_number(routing_number):
                return {"status": "error", "message": "Invalid routing number (must be 9 digits)"}
            
            available_balance = float(available_balance)
            if available_balance < 0:
                return {"status": "error", "message": "Balance cannot be negative"}
            
            self.bank_account = {
                "bank_name": bank_name,
                "account_type": account_type,
                "account_number": SecurityManager.mask_account_number(account_number),
                "account_number_full": account_number,  # Store for processing
                "routing_number": routing_number,
                "owner_name": owner_name,
                "address": address,
                "available_balance": available_balance,
                "country": "USA",
                "verified": True,
                "setup_at": datetime.now().isoformat()
            }
            return {"status": "success", "message": "USA bank account configured"}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid input: {str(e)}"}
    
    def set_canada_bank_account(self, bank_name, account_type, account_number, institution, transit_number, owner_name, address, available_balance):
        """Set Canada bank account for making payments with validation"""
        try:
            if not validate_account_number(account_number, "CANADA"):
                return {"status": "error", "message": "Invalid Canada account number"}
            
            if not validate_transit_number(transit_number):
                return {"status": "error", "message": "Invalid transit number (must be 5 digits)"}
            
            if not validate_institution_number(institution):
                return {"status": "error", "message": "Invalid institution number (must be 3 digits)"}
            
            available_balance = float(available_balance)
            if available_balance < 0:
                return {"status": "error", "message": "Balance cannot be negative"}
            
            self.bank_account = {
                "bank_name": bank_name,
                "account_type": account_type,
                "account_number": SecurityManager.mask_account_number(account_number),
                "account_number_full": account_number,
                "institution": institution,
                "transit_number": transit_number,
                "owner_name": owner_name,
                "address": address,
                "available_balance": available_balance,
                "country": "CANADA",
                "verified": True,
                "setup_at": datetime.now().isoformat()
            }
            return {"status": "success", "message": "Canada bank account configured"}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid input: {str(e)}"}
    
    def add_personal_loan(self, loan_id, lender_name, balance, monthly_payment, interest_rate, due_date):
        """Add a personal loan to track with validation"""
        try:
            if not validate_loan_amount(balance):
                return {"status": "error", "message": "Loan amount must be between $100 and $10,000,000"}
            
            if not validate_interest_rate(interest_rate):
                return {"status": "error", "message": "Interest rate must be between 0 and 50%"}
            
            loan = {
                "loan_id": loan_id,
                "lender_name": lender_name,
                "balance": float(balance),
                "original_balance": float(balance),
                "monthly_payment": float(monthly_payment),
                "interest_rate": float(interest_rate),
                "due_date": due_date,
                "loan_type": "personal",
                "status": "active",
                "created_at": datetime.now().isoformat()
            }
            self.loans.append(loan)
            return {"status": "success", "message": "Personal loan added", "loan": loan}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid input: {str(e)}"}
    
    def process_payment(self, loan_id, amount):
        """Process payment towards personal loan with fraud checks"""
        try:
            amount = float(amount)
            
            if not self.bank_account:
                return {"status": "error", "message": "Bank account not configured"}
            
            # Validate transaction
            validation = SecurityManager.validate_transaction(
                amount, 
                self.bank_account["available_balance"],
                self.max_transaction
            )
            
            if not validation["valid"]:
                return {"status": "error", "message": ", ".join(validation["errors"])}
            
            for loan in self.loans:
                if loan["loan_id"] == loan_id:
                    if loan["status"] != "active":
                        return {"status": "error", "message": "Loan is not active"}
                    
                    old_balance = loan["balance"]
                    loan["balance"] -= amount
                    self.bank_account["available_balance"] -= amount
                    
                    transaction = {
                        "transaction_id": f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        "loan_id": loan_id,
                        "amount": amount,
                        "old_balance": old_balance,
                        "new_balance": loan["balance"],
                        "account_balance": self.bank_account["available_balance"],
                        "timestamp": datetime.now().isoformat(),
                        "status": "completed"
                    }
                    self.transaction_history.append(transaction)
                    
                    return {
                        "status": "success",
                        "transaction_id": transaction["transaction_id"],
                        "amount_paid": amount,
                        "remaining_balance": loan["balance"],
                        "account_balance": self.bank_account["available_balance"],
                        "timestamp": transaction["timestamp"]
                    }
            
            return {"status": "error", "message": "Loan not found"}
        except (ValueError, TypeError) as e:
            return {"status": "error", "message": f"Invalid amount: {str(e)}"}
    
    def get_loan_details(self, loan_id):
        """Get details of a specific loan"""
        for loan in self.loans:
            if loan["loan_id"] == loan_id:
                return loan
        return None
    
    def get_transaction_history(self, loan_id=None):
        """Get transaction history"""
        if loan_id:
            return [t for t in self.transaction_history if t["loan_id"] == loan_id]
        return self.transaction_history
