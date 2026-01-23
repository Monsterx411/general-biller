# Unit tests for payment module
import pytest
from src.payment import CreditDebitPayment, BankAccount, MailCheckPayment, Appointment

def test_credit_debit_payment_creation():
    payment = CreditDebitPayment()
    assert payment.card_details == {}
    assert payment.billing_address == {}

def test_bank_account_creation():
    account = BankAccount("USA")
    assert account.country == "USA"
    assert account.account_info == {}

def test_mail_check_payment_creation():
    mail_check = MailCheckPayment()
    assert mail_check.check_amount == 0.0

def test_appointment_booking():
    appointment = Appointment()
    apt = appointment.book_appointment("Electric Company", 100.00, "2026-02-01", "10:00 AM")
    assert apt["biller_name"] == "Electric Company"
    assert apt["payment_amount"] == 100.00
