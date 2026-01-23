from flask import Blueprint, request
from src.payment.credit_debit import CreditCardLoanPayment
from src.payment.bank_account import PersonalLoanPayment
from src.payment.mail_check import HomeLoanPayment
from src.payment.appointment import AutoLoanPayment
from src.models.db import get_db
from src.models.loan import Loan
from src.models.payment import Payment
from src.utils.token import TokenManager, token_required

api_bp = Blueprint("api", __name__)

# Instances for simplicity; in production consider per-request or a service layer
credit_service = CreditCardLoanPayment()
personal_service = PersonalLoanPayment()
mortgage_service = HomeLoanPayment()
auto_service = AutoLoanPayment()

@api_bp.post("/v1/auth/token")
def get_token():
    """Get authentication token (demo: accepts any user_id)"""
    data = request.get_json(force=True)
    user_id = data.get("user_id", "demo-user")
    token = TokenManager.generate_token(user_id)
    return {"access_token": token, "token_type": "Bearer", "expires_in": 86400}

@api_bp.get("/v1/loans")
@token_required
def list_loans():
    # Placeholder: would fetch from persistent storage
    return {
        "message": "Use specific endpoints to manage loans",
        "endpoints": [
            "/api/v1/credit-card/loans",
            "/api/v1/personal/loans",
            "/api/v1/mortgage/loans",
            "/api/v1/auto/loans",
        ],
    }

# Credit Card Loan endpoints
@api_bp.post("/v1/credit-card/loans")
def add_credit_card_loan():
    data = request.get_json(force=True)
    result = credit_service.add_credit_card_loan(
        data.get("card_type"),
        data.get("card_suffix"),
        float(data.get("balance")),
        float(data.get("minimum_payment")),
        float(data.get("interest_rate")),
        data.get("due_date"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        loan_id = f"{data.get('card_type','card')}-{data.get('card_suffix','0000')}"
        try:
            for db in get_db():
                # upsert-like: try fetch existing
                existing = db.query(Loan).filter(Loan.loan_id == loan_id).first()
                if not existing:
                    db.add(Loan(
                        loan_id=loan_id,
                        loan_type="credit_card",
                        balance=float(data.get("balance")),
                        interest_rate=float(data.get("interest_rate")),
                    ))
                db.commit()
        except Exception:
            pass
    return result, status_code

@api_bp.post("/v1/credit-card/payment-method")
def set_credit_card_payment_method():
    data = request.get_json(force=True)
    result = credit_service.set_payment_method(
        data.get("card_number"),
        data.get("expiry"),
        data.get("cvv"),
        data.get("billing_address"),
    )
    return result, (200 if result.get("status") == "success" else 400)

@api_bp.post("/v1/credit-card/pay")
def pay_credit_card():
    data = request.get_json(force=True)
    result = credit_service.process_payment(
        data.get("card_type"),
        float(data.get("amount")),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        loan_id = f"{data.get('card_type','card')}-{data.get('card_suffix','0000')}"
        try:
            for db in get_db():
                db.add(Payment(loan_id=loan_id, amount=float(data.get("amount")), method="credit_card"))
                # Update balance if loan exists
                loan = db.query(Loan).filter(Loan.loan_id == loan_id).first()
                if loan:
                    loan.balance = max(0.0, float(loan.balance) - float(data.get("amount")))
                db.commit()
        except Exception:
            pass
    return result, status_code

# Personal Loan endpoints
@api_bp.post("/v1/personal/loans")
def add_personal_loan():
    data = request.get_json(force=True)
    result = personal_service.add_personal_loan(
        data.get("loan_id"),
        data.get("lender_name", "Lender"),
        float(data.get("amount")) if data.get("amount") is not None else float(data.get("balance", 0)),
        float(data.get("monthly_payment", 300)),
        float(data.get("interest_rate", 10.0)),
        data.get("due_date", "12/27"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                existing = db.query(Loan).filter(Loan.loan_id == data.get("loan_id")).first()
                if not existing:
                    db.add(Loan(
                        loan_id=data.get("loan_id"),
                        loan_type="personal",
                        balance=float(data.get("amount")) if data.get("amount") is not None else float(data.get("balance", 0)),
                        interest_rate=float(data.get("interest_rate", 10.0)),
                    ))
                db.commit()
        except Exception:
            pass
    return result, status_code

@api_bp.post("/v1/personal/bank/usa")
def set_usa_bank():
    data = request.get_json(force=True)
    result = personal_service.set_usa_bank_account(
        data.get("bank_name", "Bank"),
        data.get("account_type", "checking"),
        data.get("account_number"),
        data.get("routing_number"),
        data.get("owner_name", "John Doe"),
        data.get("address", "123 Main St"),
        data.get("available_balance", 50000),
    )
    return result, (200 if result.get("status") == "success" else 400)

@api_bp.post("/v1/personal/bank/canada")
def set_canada_bank():
    data = request.get_json(force=True)
    result = personal_service.set_canada_bank_account(
        data.get("bank_name", "Bank"),
        data.get("account_type", "chequing"),
        data.get("account_number"),
        data.get("institution_number"),
        data.get("transit_number"),
        data.get("owner_name", "John Doe"),
        data.get("address", "123 Main St"),
        data.get("available_balance", 50000),
    )
    return result, (200 if result.get("status") == "success" else 400)

@api_bp.post("/v1/personal/pay")
def pay_personal_loan():
    data = request.get_json(force=True)
    result = personal_service.process_payment(
        data.get("loan_id"),
        float(data.get("amount")),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                db.add(Payment(loan_id=data.get("loan_id"), amount=float(data.get("amount")), method="bank"))
                loan = db.query(Loan).filter(Loan.loan_id == data.get("loan_id")).first()
                if loan:
                    loan.balance = max(0.0, float(loan.balance) - float(data.get("amount")))
                db.commit()
        except Exception:
            pass
    return result, status_code

# Mortgage endpoints
@api_bp.post("/v1/mortgage/loans")
def add_mortgage():
    data = request.get_json(force=True)
    result = mortgage_service.add_mortgage(
        data.get("mortgage_id"),
        data.get("lender_name", "Lender"),
        data.get("property_address"),
        float(data.get("principal_balance", data.get("loan_amount", 0))),
        float(data.get("monthly_payment", 1200)),
        float(data.get("interest_rate", 6.0)),
        int(data.get("remaining_term_months", 360)),
        data.get("due_date", "12/27"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                existing = db.query(Loan).filter(Loan.loan_id == data.get("mortgage_id")).first()
                if not existing:
                    db.add(Loan(
                        loan_id=data.get("mortgage_id"),
                        loan_type="mortgage",
                        balance=float(data.get("principal_balance", data.get("loan_amount", 0))),
                        interest_rate=float(data.get("interest_rate", 6.0)),
                    ))
                db.commit()
        except Exception:
            pass
    return result, status_code

@api_bp.post("/v1/mortgage/payment-method/bank")
def set_mortgage_bank_method():
    data = request.get_json(force=True)
    result = mortgage_service.set_payment_method_bank(
        data.get("routing_or_transit"),
        data.get("account_number"),
    )
    return result, (200 if result.get("status") == "success" else 400)

@api_bp.post("/v1/mortgage/pay")
def pay_mortgage():
    data = request.get_json(force=True)
    result = mortgage_service.process_payment(
        data.get("mortgage_id"),
        float(data.get("amount")),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                db.add(Payment(loan_id=data.get("mortgage_id"), amount=float(data.get("amount")), method="bank"))
                loan = db.query(Loan).filter(Loan.loan_id == data.get("mortgage_id")).first()
                if loan:
                    loan.balance = max(0.0, float(loan.balance) - float(data.get("amount")))
                db.commit()
        except Exception:
            pass
    return result, status_code

# Auto Loan endpoints
@api_bp.post("/v1/auto/loans")
def add_auto_loan():
    data = request.get_json(force=True)
    vehicle_info = data.get("vehicle_info") or f"{data.get('vehicle_make','') } {data.get('vehicle_model','')} {data.get('vehicle_year','')} {data.get('vin','')}".strip()
    result = auto_service.add_auto_loan(
        data.get("loan_id"),
        data.get("lender_name", "Lender"),
        vehicle_info,
        float(data.get("loan_amount", 0)),
        float(data.get("monthly_payment", 350)),
        float(data.get("interest_rate", 5.0)),
        int(data.get("months_remaining", 60)),
        data.get("due_date", "12/27"),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                existing = db.query(Loan).filter(Loan.loan_id == data.get("loan_id")).first()
                if not existing:
                    db.add(Loan(
                        loan_id=data.get("loan_id"),
                        loan_type="auto",
                        balance=float(data.get("loan_amount", 0)),
                        interest_rate=float(data.get("interest_rate", 5.0)),
                    ))
                db.commit()
        except Exception:
            pass
    return result, status_code

@api_bp.post("/v1/auto/pay")
def pay_auto_loan():
    data = request.get_json(force=True)
    result = auto_service.process_payment(
        data.get("loan_id"),
        float(data.get("amount")),
    )
    status_code = 200 if result.get("status") == "success" else 400
    if status_code == 200:
        try:
            for db in get_db():
                db.add(Payment(loan_id=data.get("loan_id"), amount=float(data.get("amount")), method="auto"))
                loan = db.query(Loan).filter(Loan.loan_id == data.get("loan_id")).first()
                if loan:
                    loan.balance = max(0.0, float(loan.balance) - float(data.get("amount")))
                db.commit()
        except Exception:
            pass
    return result, status_code
