#!/usr/bin/env python
"""
Interactive API Demo for Loan Payment Manager
Demonstrates all API endpoints with real examples
"""

import requests
import json
from time import sleep

# Configuration
BASE_URL = "http://127.0.0.1:5000/api"
token = None

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_response(response):
    print(f"\nStatus Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def get_auth_token():
    """Step 1: Get authentication token"""
    global token
    print_header("1. Authentication - Getting Access Token")
    
    response = requests.post(
        f"{BASE_URL}/v1/auth/token",
        json={"user_id": "demo-user-123"}
    )
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"\n✓ Token received: {token[:20]}...")
        return True
    return False

def list_loans():
    """Step 2: List available loan endpoints"""
    print_header("2. Listing Available Loan Endpoints")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/v1/loans", headers=headers)
    print_response(response)

def demo_credit_card():
    """Step 3: Credit Card Loan Demo"""
    print_header("3. Credit Card Loan Management")
    
    # Add credit card loan
    print("\n→ Adding Credit Card Loan...")
    response = requests.post(
        f"{BASE_URL}/v1/credit-card/loans",
        json={
            "card_type": "Visa",
            "card_suffix": "4532",
            "balance": 2500.00,
            "minimum_payment": 75.00,
            "interest_rate": 18.99,
            "due_date": "02/15"
        }
    )
    print_response(response)
    
    # Set payment method
    print("\n→ Setting Payment Method...")
    response = requests.post(
        f"{BASE_URL}/v1/credit-card/payment-method",
        json={
            "card_number": "4532123456789012",
            "expiry": "12/26",
            "cvv": "123",
            "billing_address": "123 Main St, New York, NY 10001"
        }
    )
    print_response(response)
    
    # Make payment
    print("\n→ Processing Payment...")
    response = requests.post(
        f"{BASE_URL}/v1/credit-card/pay",
        json={
            "card_type": "Visa",
            "card_suffix": "4532",
            "amount": 500.00
        }
    )
    print_response(response)

def demo_personal_loan():
    """Step 4: Personal Loan Demo"""
    print_header("4. Personal Loan Management")
    
    # Add personal loan
    print("\n→ Adding Personal Loan...")
    response = requests.post(
        f"{BASE_URL}/v1/personal/loans",
        json={
            "loan_id": "PL-2024-001",
            "amount": 15000.00,
            "interest_rate": 7.5,
            "term_months": 60,
            "country": "USA"
        }
    )
    print_response(response)
    
    # Set bank account
    print("\n→ Setting Bank Account (USA)...")
    response = requests.post(
        f"{BASE_URL}/v1/personal/bank-account",
        json={
            "account_number": "123456789",
            "routing_number": "021000021",
            "account_type": "checking",
            "bank_name": "Chase Bank"
        }
    )
    print_response(response)
    
    # Make payment
    print("\n→ Processing Payment...")
    response = requests.post(
        f"{BASE_URL}/v1/personal/pay",
        json={
            "loan_id": "PL-2024-001",
            "amount": 300.00
        }
    )
    print_response(response)

def demo_mortgage():
    """Step 5: Mortgage Demo"""
    print_header("5. Mortgage Management")
    
    # Add mortgage
    print("\n→ Adding Mortgage...")
    response = requests.post(
        f"{BASE_URL}/v1/mortgage/loans",
        json={
            "property_address": "456 Oak Street, Los Angeles, CA 90001",
            "loan_amount": 350000.00,
            "interest_rate": 4.5,
            "term_months": 360,
            "monthly_payment": 1773.40
        }
    )
    print_response(response)
    
    # Make payment via check
    print("\n→ Processing Check Payment...")
    response = requests.post(
        f"{BASE_URL}/v1/mortgage/pay",
        json={
            "property_address": "456 Oak Street, Los Angeles, CA 90001",
            "amount": 1773.40,
            "payment_method": "check",
            "payer_name": "John Doe",
            "payer_address": "456 Oak Street, Los Angeles, CA 90001"
        }
    )
    print_response(response)

def demo_auto_loan():
    """Step 6: Auto Loan Demo"""
    print_header("6. Auto Loan Management")
    
    # Add auto loan
    print("\n→ Adding Auto Loan...")
    response = requests.post(
        f"{BASE_URL}/v1/auto/loans",
        json={
            "vehicle_make": "Toyota",
            "vehicle_model": "Camry",
            "vehicle_year": 2023,
            "vin": "1HGBH41JXMN109186",
            "loan_amount": 28000.00,
            "interest_rate": 5.5,
            "term_months": 60,
            "monthly_payment": 532.50
        }
    )
    print_response(response)
    
    # Make payment
    print("\n→ Processing Payment...")
    response = requests.post(
        f"{BASE_URL}/v1/auto/pay",
        json={
            "vin": "1HGBH41JXMN109186",
            "amount": 532.50
        }
    )
    print_response(response)

def main():
    """Run complete API demo"""
    print_header("🚀 Loan Payment Manager - Interactive API Demo")
    print("\nMake sure the Flask API server is running on http://127.0.0.1:5000")
    print("Start the server with: flask --app src.api.app run --debug")
    
    input("\nPress Enter to start the demo...")
    
    try:
        # Check if server is running
        response = requests.get("http://127.0.0.1:5000/health", timeout=2)
        if response.status_code != 200:
            print("\n❌ API server is not responding correctly!")
            return
    except requests.exceptions.RequestException:
        print("\n❌ Cannot connect to API server!")
        print("Please start the server first with: flask --app src.api.app run --debug")
        return
    
    print("\n✓ API server is running!")
    
    # Run demo steps
    if not get_auth_token():
        print("\n❌ Failed to get authentication token. Aborting.")
        return
    
    sleep(1)
    list_loans()
    
    sleep(1)
    demo_credit_card()
    
    sleep(1)
    demo_personal_loan()
    
    sleep(1)
    demo_mortgage()
    
    sleep(1)
    demo_auto_loan()
    
    print_header("✅ Demo Complete!")
    print("\nAll API endpoints have been demonstrated successfully.")
    print("Check the terminal running the Flask server for detailed logs.")

if __name__ == "__main__":
    main()
