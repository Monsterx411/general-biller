# Auto Loan Payment Processing

from datetime import datetime

class AutoLoanPayment:
    """Handle auto loan/vehicle loan payments"""
    
    def __init__(self):
        self.auto_loans = []
        self.payment_history = []
    
    def add_auto_loan(self, loan_id, lender_name, vehicle_info, loan_amount, monthly_payment, interest_rate, months_remaining, due_date):
        """Add an auto loan to track"""
        auto_loan = {
            "loan_id": loan_id,
            "lender_name": lender_name,
            "vehicle_info": vehicle_info,  # Make, model, year, VIN
            "loan_amount": loan_amount,
            "monthly_payment": monthly_payment,
            "interest_rate": interest_rate,
            "months_remaining": months_remaining,
            "due_date": due_date,
            "loan_type": "auto",
            "status": "active"
        }
        self.auto_loans.append(auto_loan)
        return auto_loan
    
    def process_payment(self, loan_id, amount):
        """Process auto loan payment"""
        for loan in self.auto_loans:
            if loan["loan_id"] == loan_id:
                loan["loan_amount"] -= amount
                loan["months_remaining"] -= 1
                
                payment_record = {
                    "loan_id": loan_id,
                    "amount": amount,
                    "date": datetime.now(),
                    "remaining_balance": loan["loan_amount"]
                }
                self.payment_history.append(payment_record)
                
                return {
                    "status": "success",
                    "amount_paid": amount,
                    "remaining_balance": loan["loan_amount"],
                    "months_remaining": loan["months_remaining"]
                }
        return {"status": "error", "message": "Auto loan not found"}
    
    def get_loan_details(self, loan_id):
        """Get auto loan details"""
        for loan in self.auto_loans:
            if loan["loan_id"] == loan_id:
                return loan
        return None
    
    def get_payment_history(self, loan_id):
        """Get payment history for a specific loan"""
        return [p for p in self.payment_history if p["loan_id"] == loan_id]
