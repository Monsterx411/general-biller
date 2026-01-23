# Personal and General Loan Payment Processing

class PersonalLoanPayment:
    """Handle personal loan payments via bank account transfer"""
    
    def __init__(self, country="USA"):
        self.country = country
        self.bank_account = {}  # Account to pay FROM
        self.loans = []  # Personal loans to track
    
    def set_usa_bank_account(self, bank_name, account_type, account_number, routing_number, owner_name, address, available_balance):
        """Set USA bank account for making payments"""
        self.bank_account = {
            "bank_name": bank_name,
            "account_type": account_type,
            "account_number": account_number,
            "routing_number": routing_number,
            "owner_name": owner_name,
            "address": address,
            "available_balance": available_balance
        }
    
    def set_canada_bank_account(self, bank_name, account_type, account_number, institution, transit_number, owner_name, address, available_balance):
        """Set Canada bank account for making payments"""
        self.bank_account = {
            "bank_name": bank_name,
            "account_type": account_type,
            "account_number": account_number,
            "institution": institution,
            "transit_number": transit_number,
            "owner_name": owner_name,
            "address": address,
            "available_balance": available_balance
        }
    
    def add_personal_loan(self, loan_id, lender_name, balance, monthly_payment, interest_rate, due_date):
        """Add a personal loan to track"""
        loan = {
            "loan_id": loan_id,
            "lender_name": lender_name,
            "balance": balance,
            "monthly_payment": monthly_payment,
            "interest_rate": interest_rate,
            "due_date": due_date,
            "loan_type": "personal"
        }
        self.loans.append(loan)
        return loan
    
    def process_payment(self, loan_id, amount):
        """Process payment towards personal loan"""
        if self.bank_account.get("available_balance", 0) < amount:
            return {"status": "error", "message": "Insufficient funds"}
        
        for loan in self.loans:
            if loan["loan_id"] == loan_id:
                loan["balance"] -= amount
                self.bank_account["available_balance"] -= amount
                return {
                    "status": "success",
                    "amount_paid": amount,
                    "remaining_balance": loan["balance"],
                    "account_balance": self.bank_account["available_balance"]
                }
        return {"status": "error", "message": "Loan not found"}
    
    def get_loan_details(self, loan_id):
        """Get details of a specific loan"""
        for loan in self.loans:
            if loan["loan_id"] == loan_id:
                return loan
        return None
