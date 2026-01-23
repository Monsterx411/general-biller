# Payment module init file
from .credit_debit import CreditCardLoanPayment
from .bank_account import PersonalLoanPayment
from .mail_check import HomeLoanPayment
from .appointment import AutoLoanPayment

__all__ = ["CreditCardLoanPayment", "PersonalLoanPayment", "HomeLoanPayment", "AutoLoanPayment"]
