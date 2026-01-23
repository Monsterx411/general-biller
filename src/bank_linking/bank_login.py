# Bank linking module for account login and verification

class BankLink:
    """Handle bank account linking via login"""
    
    def __init__(self):
        self.linked_accounts = []
    
    def link_bank_account(self, bank_name, username, password):
        """Link bank account by logging in"""
        # Placeholder for bank login verification
        account = {
            "bank_name": bank_name,
            "username": username,
            "linked": True
        }
        self.linked_accounts.append(account)
        return account
    
    def get_linked_accounts(self):
        """Get all linked bank accounts"""
        return self.linked_accounts
    
    def unlink_account(self, bank_name):
        """Unlink a bank account"""
        self.linked_accounts = [acc for acc in self.linked_accounts if acc["bank_name"] != bank_name]
