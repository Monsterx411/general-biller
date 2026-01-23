# Home Loan (Mortgage) Payment Processing

class HomeLoanPayment:
    """Handle home loan/mortgage payments"""
    
    def __init__(self, country="USA"):
        self.country = country
        self.mortgages = []
        self.payment_method = {}
    
    def add_mortgage(self, loan_id, lender_name, property_address, principal_balance, monthly_payment, interest_rate, remaining_term_months, due_date):
        """Add a mortgage loan to track"""
        mortgage = {
            "loan_id": loan_id,
            "lender_name": lender_name,
            "property_address": property_address,
            "principal_balance": principal_balance,
            "monthly_payment": monthly_payment,
            "interest_rate": interest_rate,
            "remaining_term_months": remaining_term_months,
            "due_date": due_date,
            "loan_type": "mortgage",
            "status": "active"
        }
        self.mortgages.append(mortgage)
        return mortgage
    
    def set_payment_method_bank(self, account_number, routing_number=None, transit_number=None):
        """Set bank account as payment method"""
        self.payment_method = {
            "method": "bank_transfer",
            "account_number": account_number,
            "routing_number": routing_number,
            "transit_number": transit_number
        }
    
    def set_payment_method_check(self, payer_name, address, phone, email):
        """Set check payment method"""
        self.payment_method = {
            "method": "check",
            "payer_name": payer_name,
            "address": address,
            "phone": phone,
            "email": email
        }
    
    def process_payment(self, loan_id, amount):
        """Process mortgage payment"""
        for mortgage in self.mortgages:
            if mortgage["loan_id"] == loan_id:
                mortgage["principal_balance"] -= amount
                mortgage["remaining_term_months"] -= 1
                return {
                    "status": "success",
                    "amount_paid": amount,
                    "remaining_balance": mortgage["principal_balance"],
                    "remaining_term": mortgage["remaining_term_months"]
                }
        return {"status": "error", "message": "Mortgage not found"}
    
    def get_mortgage_details(self, loan_id):
        """Get mortgage details"""
        for mortgage in self.mortgages:
            if mortgage["loan_id"] == loan_id:
                return mortgage
        return None
