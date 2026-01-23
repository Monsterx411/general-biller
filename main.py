"""
General Biller (US & CA) - Main Application Entry Point
Handles bill payments through multiple payment methods
"""

from src.payment import CreditDebitPayment, BankAccount, MailCheckPayment, Appointment
from src.bank_linking import BankLink
from src.utils import validate_email, validate_phone, format_currency

class GeneralBiller:
    """Main application class for bill payment management"""
    
    def __init__(self):
        self.credit_debit = CreditDebitPayment()
        self.bank_account = BankAccount()
        self.mail_check = MailCheckPayment()
        self.appointment = Appointment()
        self.bank_link = BankLink()
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("GENERAL BILLER - USA & CANADA")
        print("="*50)
        print("1. Credit/Debit Card Payment")
        print("2. Bank Account Payment")
        print("3. Bank Linking")
        print("4. Mail Check Payment")
        print("5. Book Appointment")
        print("6. Exit")
        print("="*50)
    
    def run(self):
        """Run the main application loop"""
        print("Welcome to General Biller!")
        
        while True:
            self.display_menu()
            choice = input("\nSelect an option (1-6): ").strip()
            
            if choice == "1":
                self.handle_credit_debit_payment()
            elif choice == "2":
                self.handle_bank_account_payment()
            elif choice == "3":
                self.handle_bank_linking()
            elif choice == "4":
                self.handle_mail_check_payment()
            elif choice == "5":
                self.handle_appointment()
            elif choice == "6":
                print("\nThank you for using General Biller. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def handle_credit_debit_payment(self):
        """Handle credit/debit card payment"""
        print("\n--- Credit/Debit Card Payment ---")
        # Placeholder for payment handling
        print("Feature coming soon!")
    
    def handle_bank_account_payment(self):
        """Handle bank account payment"""
        print("\n--- Bank Account Payment ---")
        # Placeholder for payment handling
        print("Feature coming soon!")
    
    def handle_bank_linking(self):
        """Handle bank account linking"""
        print("\n--- Bank Linking ---")
        # Placeholder for bank linking handling
        print("Feature coming soon!")
    
    def handle_mail_check_payment(self):
        """Handle mail check payment"""
        print("\n--- Mail Check Payment ---")
        # Placeholder for mail check handling
        print("Feature coming soon!")
    
    def handle_appointment(self):
        """Handle appointment booking"""
        print("\n--- Book Appointment ---")
        # Placeholder for appointment handling
        print("Feature coming soon!")

if __name__ == "__main__":
    app = GeneralBiller()
    app.run()
