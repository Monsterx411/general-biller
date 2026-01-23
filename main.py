"""
Loan Payment Manager - USA & CANADA
Complete loan payment management system for multiple loan types
"""

from src.payment import CreditCardLoanPayment, PersonalLoanPayment, HomeLoanPayment, AutoLoanPayment
from src.bank_linking import BankLink
from src.utils import validate_email, validate_phone, format_currency

class LoanPaymentManager:
    """Main application class for loan payment management"""
    
    def __init__(self):
        self.credit_card_loans = CreditCardLoanPayment()
        self.personal_loans = PersonalLoanPayment()
        self.mortgages = HomeLoanPayment()
        self.auto_loans = AutoLoanPayment()
        self.bank_link = BankLink()
    
    def display_main_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("LOAN PAYMENT MANAGER - USA & CANADA")
        print("="*60)
        print("1. Credit Card Loan Payments")
        print("2. Personal Loan Payments")
        print("3. Home Loan (Mortgage) Payments")
        print("4. Auto Loan Payments")
        print("5. Bank Account Linking")
        print("6. View Payment History")
        print("7. Exit")
        print("="*60)
    
    def handle_credit_card_loans(self):
        """Handle credit card loan payments"""
        while True:
            print("\n--- Credit Card Loan Payments ---")
            print("1. Add Credit Card Loan Account")
            print("2. Make Payment")
            print("3. View Balance")
            print("4. Back to Main Menu")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                issuer = input("Card Issuer (e.g., Visa, Mastercard): ").strip()
                card_last4 = input("Last 4 digits of card: ").strip()
                balance = float(input("Current balance: $"))
                min_payment = float(input("Minimum payment: $"))
                interest_rate = float(input("Interest rate (%): "))
                due_date = input("Due date (MM/DD): ").strip()
                
                self.credit_card_loans.add_credit_card_loan(issuer, card_last4, balance, min_payment, interest_rate, due_date)
                print(f"✓ {issuer} card added successfully!")
            
            elif choice == "2":
                issuer = input("Card Issuer: ").strip()
                amount = float(input("Payment amount: $"))
                result = self.credit_card_loans.process_payment(issuer, amount)
                print(f"✓ Payment Status: {result['status']}")
                if result['status'] == 'success':
                    print(f"  Remaining Balance: ${result['remaining_balance']:,.2f}")
            
            elif choice == "3":
                issuer = input("Card Issuer: ").strip()
                loan = self.credit_card_loans.get_loan_details(issuer)
                if loan:
                    print(f"\nCard: {loan['card_issuer']} ****{loan['card_last_4']}")
                    print(f"Balance: ${loan['balance']:,.2f}")
                    print(f"Min Payment: ${loan['min_payment']:,.2f}")
                    print(f"Interest Rate: {loan['interest_rate']}%")
                    print(f"Due Date: {loan['due_date']}")
                else:
                    print("Card not found.")
            
            elif choice == "4":
                break
            else:
                print("Invalid option.")
    
    def handle_personal_loans(self):
        """Handle personal loan payments"""
        while True:
            print("\n--- Personal Loan Payments ---")
            print("1. Set Up Bank Account")
            print("2. Add Personal Loan")
            print("3. Make Payment")
            print("4. View Loan Details")
            print("5. Back to Main Menu")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                country = input("Country (USA/Canada): ").strip().upper()
                if country == "USA":
                    bank_name = input("Bank Name: ").strip()
                    acc_type = input("Account Type (Checking/Savings): ").strip()
                    acc_number = input("Account Number: ").strip()
                    routing = input("Routing Number: ").strip()
                    owner = input("Account Owner Name: ").strip()
                    address = input("Address: ").strip()
                    balance = float(input("Available Balance: $"))
                    self.personal_loans.set_usa_bank_account(bank_name, acc_type, acc_number, routing, owner, address, balance)
                    print("✓ USA bank account configured!")
                else:
                    bank_name = input("Bank Name: ").strip()
                    acc_type = input("Account Type: ").strip()
                    acc_number = input("Account Number: ").strip()
                    institution = input("Institution: ").strip()
                    transit = input("Transit Number: ").strip()
                    owner = input("Account Owner Name: ").strip()
                    address = input("Address: ").strip()
                    balance = float(input("Available Balance: $"))
                    self.personal_loans.set_canada_bank_account(bank_name, acc_type, acc_number, institution, transit, owner, address, balance)
                    print("✓ Canada bank account configured!")
            
            elif choice == "2":
                loan_id = input("Loan ID: ").strip()
                lender = input("Lender Name: ").strip()
                balance = float(input("Loan Balance: $"))
                monthly = float(input("Monthly Payment: $"))
                rate = float(input("Interest Rate (%): "))
                due = input("Due Date (MM/DD): ").strip()
                
                self.personal_loans.add_personal_loan(loan_id, lender, balance, monthly, rate, due)
                print("✓ Personal loan added!")
            
            elif choice == "3":
                loan_id = input("Loan ID: ").strip()
                amount = float(input("Payment Amount: $"))
                result = self.personal_loans.process_payment(loan_id, amount)
                print(f"✓ {result['status'].upper()}")
                if result['status'] == 'success':
                    print(f"  Remaining Balance: ${result['remaining_balance']:,.2f}")
                else:
                    print(f"  Error: {result['message']}")
            
            elif choice == "4":
                loan_id = input("Loan ID: ").strip()
                loan = self.personal_loans.get_loan_details(loan_id)
                if loan:
                    print(f"\nLoan ID: {loan['loan_id']}")
                    print(f"Lender: {loan['lender_name']}")
                    print(f"Balance: ${loan['balance']:,.2f}")
                    print(f"Monthly Payment: ${loan['monthly_payment']:,.2f}")
                    print(f"Interest Rate: {loan['interest_rate']}%")
                else:
                    print("Loan not found.")
            
            elif choice == "5":
                break
    
    def handle_mortgages(self):
        """Handle mortgage payments"""
        while True:
            print("\n--- Home Loan (Mortgage) Payments ---")
            print("1. Add Mortgage")
            print("2. Set Payment Method")
            print("3. Make Payment")
            print("4. View Mortgage Details")
            print("5. Back to Main Menu")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                loan_id = input("Loan ID: ").strip()
                lender = input("Lender Name: ").strip()
                property_addr = input("Property Address: ").strip()
                principal = float(input("Principal Balance: $"))
                monthly = float(input("Monthly Payment: $"))
                rate = float(input("Interest Rate (%): "))
                months = int(input("Months Remaining: "))
                due = input("Due Date (MM/DD): ").strip()
                
                self.mortgages.add_mortgage(loan_id, lender, property_addr, principal, monthly, rate, months, due)
                print("✓ Mortgage added!")
            
            elif choice == "2":
                method = input("Payment Method (bank/check): ").strip().lower()
                if method == "bank":
                    acc_num = input("Account Number: ").strip()
                    routing = input("Routing Number (USA) or Transit (Canada): ").strip()
                    self.mortgages.set_payment_method_bank(acc_num, routing_number=routing if len(routing)==9 else None, transit_number=routing if len(routing)!=9 else None)
                    print("✓ Bank payment method set!")
                else:
                    name = input("Payer Name: ").strip()
                    addr = input("Address: ").strip()
                    phone = input("Phone: ").strip()
                    email = input("Email: ").strip()
                    self.mortgages.set_payment_method_check(name, addr, phone, email)
                    print("✓ Check payment method set!")
            
            elif choice == "3":
                loan_id = input("Loan ID: ").strip()
                amount = float(input("Payment Amount: $"))
                result = self.mortgages.process_payment(loan_id, amount)
                print(f"✓ {result['status'].upper()}")
                if result['status'] == 'success':
                    print(f"  Remaining Balance: ${result['remaining_balance']:,.2f}")
                    print(f"  Months Remaining: {result['remaining_term']}")
            
            elif choice == "4":
                loan_id = input("Loan ID: ").strip()
                mortgage = self.mortgages.get_mortgage_details(loan_id)
                if mortgage:
                    print(f"\nLoan ID: {mortgage['loan_id']}")
                    print(f"Lender: {mortgage['lender_name']}")
                    print(f"Property: {mortgage['property_address']}")
                    print(f"Principal Balance: ${mortgage['principal_balance']:,.2f}")
                    print(f"Monthly Payment: ${mortgage['monthly_payment']:,.2f}")
                    print(f"Interest Rate: {mortgage['interest_rate']}%")
                    print(f"Months Remaining: {mortgage['remaining_term_months']}")
                else:
                    print("Mortgage not found.")
            
            elif choice == "5":
                break
    
    def handle_auto_loans(self):
        """Handle auto loan payments"""
        while True:
            print("\n--- Auto Loan Payments ---")
            print("1. Add Auto Loan")
            print("2. Make Payment")
            print("3. View Loan Details")
            print("4. View Payment History")
            print("5. Back to Main Menu")
            choice = input("Select option: ").strip()
            
            if choice == "1":
                loan_id = input("Loan ID: ").strip()
                lender = input("Lender Name: ").strip()
                make = input("Vehicle Make: ").strip()
                model = input("Vehicle Model: ").strip()
                year = input("Vehicle Year: ").strip()
                vin = input("VIN: ").strip()
                amount = float(input("Loan Amount: $"))
                monthly = float(input("Monthly Payment: $"))
                rate = float(input("Interest Rate (%): "))
                months = int(input("Months Remaining: "))
                due = input("Due Date (MM/DD): ").strip()
                
                vehicle = {"make": make, "model": model, "year": year, "vin": vin}
                self.auto_loans.add_auto_loan(loan_id, lender, vehicle, amount, monthly, rate, months, due)
                print("✓ Auto loan added!")
            
            elif choice == "2":
                loan_id = input("Loan ID: ").strip()
                amount = float(input("Payment Amount: $"))
                result = self.auto_loans.process_payment(loan_id, amount)
                print(f"✓ {result['status'].upper()}")
                if result['status'] == 'success':
                    print(f"  Remaining Balance: ${result['remaining_balance']:,.2f}")
                    print(f"  Months Remaining: {result['months_remaining']}")
            
            elif choice == "3":
                loan_id = input("Loan ID: ").strip()
                loan = self.auto_loans.get_loan_details(loan_id)
                if loan:
                    print(f"\nLoan ID: {loan['loan_id']}")
                    print(f"Lender: {loan['lender_name']}")
                    print(f"Vehicle: {loan['vehicle_info']['year']} {loan['vehicle_info']['make']} {loan['vehicle_info']['model']}")
                    print(f"Loan Amount: ${loan['loan_amount']:,.2f}")
                    print(f"Monthly Payment: ${loan['monthly_payment']:,.2f}")
                    print(f"Interest Rate: {loan['interest_rate']}%")
                    print(f"Months Remaining: {loan['months_remaining']}")
                else:
                    print("Loan not found.")
            
            elif choice == "4":
                loan_id = input("Loan ID: ").strip()
                history = self.auto_loans.get_payment_history(loan_id)
                if history:
                    print(f"\nPayment History for {loan_id}:")
                    for payment in history:
                        print(f"  - ${payment['amount']:,.2f} on {payment['date']} (Remaining: ${payment['remaining_balance']:,.2f})")
                else:
                    print("No payment history found.")
            
            elif choice == "5":
                break
    
    def run(self):
        """Run the main application loop"""
        print("\n" + "="*60)
        print("Welcome to Loan Payment Manager!")
        print("="*60)
        
        while True:
            self.display_main_menu()
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == "1":
                self.handle_credit_card_loans()
            elif choice == "2":
                self.handle_personal_loans()
            elif choice == "3":
                self.handle_mortgages()
            elif choice == "4":
                self.handle_auto_loans()
            elif choice == "5":
                print("\nBank Linking feature coming soon!")
            elif choice == "6":
                print("\nPayment history feature coming soon!")
            elif choice == "7":
                print("\nThank you for using Loan Payment Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = LoanPaymentManager()
    app.run()
