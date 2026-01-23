# Unit tests for payment module
import pytest
from src.payment import CreditCardLoanPayment, PersonalLoanPayment, HomeLoanPayment, AutoLoanPayment

def test_credit_card_loan_creation():
    payment = CreditCardLoanPayment()
    loan = payment.add_credit_card_loan("Visa", "1234", 5000, 150, 18.5, "12/25")
    assert loan["card_issuer"] == "Visa"
    assert loan["balance"] == 5000

def test_credit_card_payment():
    payment = CreditCardLoanPayment()
    payment.add_credit_card_loan("Mastercard", "5678", 3000, 100, 16.9, "01/20")
    result = payment.process_payment("Mastercard", 500)
    assert result["status"] == "success"
    assert result["remaining_balance"] == 2500

def test_personal_loan_creation():
    loan = PersonalLoanPayment("USA")
    personal_loan = loan.add_personal_loan("PL001", "SoFi", 15000, 300, 8.5, "15th")
    assert personal_loan["loan_id"] == "PL001"
    assert personal_loan["balance"] == 15000

def test_personal_loan_payment():
    loan = PersonalLoanPayment("USA")
    loan.set_usa_bank_account("Chase", "Checking", "123456789", "021000021", "John Doe", "123 Main St", 10000)
    loan.add_personal_loan("PL002", "LendingClub", 10000, 250, 9.2, "20th")
    result = loan.process_payment("PL002", 250)
    assert result["status"] == "success"
    assert result["remaining_balance"] == 9750

def test_mortgage_creation():
    mortgage = HomeLoanPayment("USA")
    home_loan = mortgage.add_mortgage("ML001", "Bank of America", "123 Oak St", 350000, 2100, 4.5, 360, "01st")
    assert home_loan["loan_id"] == "ML001"
    assert home_loan["principal_balance"] == 350000

def test_mortgage_payment():
    mortgage = HomeLoanPayment("USA")
    mortgage.add_mortgage("ML002", "Wells Fargo", "456 Elm St", 300000, 1800, 4.2, 360, "15th")
    result = mortgage.process_payment("ML002", 1800)
    assert result["status"] == "success"
    assert result["remaining_balance"] == 298200
    assert result["remaining_term"] == 359

def test_auto_loan_creation():
    auto = AutoLoanPayment()
    vehicle = {"make": "Toyota", "model": "Camry", "year": "2022", "vin": "ABC123"}
    loan = auto.add_auto_loan("AL001", "Chase Auto", vehicle, 25000, 450, 6.5, 60, "10th")
    assert loan["loan_id"] == "AL001"
    assert loan["loan_amount"] == 25000

def test_auto_loan_payment():
    auto = AutoLoanPayment()
    vehicle = {"make": "Honda", "model": "Civic", "year": "2023", "vin": "XYZ789"}
    auto.add_auto_loan("AL002", "Capital One Auto", vehicle, 20000, 400, 7.2, 60, "20th")
    result = auto.process_payment("AL002", 400)
    assert result["status"] == "success"
    assert result["remaining_balance"] == 19600
    assert result["months_remaining"] == 59
