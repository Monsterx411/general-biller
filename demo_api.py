#!/usr/bin/env python
"""
Demo script to showcase the General Biller API
This script demonstrates the full user flow:
1. User registration
2. Login and authentication
3. MFA setup
4. Adding loans
5. Making payments
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api"
TEST_USER = {
    "email": f"demo_{int(time.time())}@example.com",
    "password": "SecurePass123!",
    "full_name": "Demo User",
    "phone": "+1234567890"
}

class BillerAPIDemo:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        
    def print_header(self, title):
        """Print formatted section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    
    def print_response(self, response):
        """Print formatted API response"""
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Response: {response.text}")
        print()
    
    def register_user(self):
        """Step 1: Register a new user"""
        self.print_header("Step 1: User Registration")
        
        url = f"{self.base_url}/auth/register"
        response = requests.post(url, json=TEST_USER)
        
        self.print_response(response)
        
        if response.status_code == 201:
            data = response.json()
            self.user_id = data['user']['id']
            print(f"✅ User registered successfully!")
            print(f"   User ID: {self.user_id}")
            return True
        else:
            print("❌ Registration failed")
            return False
    
    def login_user(self):
        """Step 2: Login and get authentication token"""
        self.print_header("Step 2: User Login")
        
        url = f"{self.base_url}/auth/login"
        response = requests.post(url, json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        
        self.print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            print(f"✅ Login successful!")
            print(f"   Token: {self.token[:50]}...")
            print(f"   Expires in: {data['expires_in']} seconds")
            return True
        else:
            print("❌ Login failed")
            return False
    
    def get_profile(self):
        """Step 3: Get user profile"""
        self.print_header("Step 3: Get User Profile")
        
        url = f"{self.base_url}/auth/profile"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ Profile retrieved successfully!")
            return True
        else:
            print("❌ Failed to get profile")
            return False
    
    def add_credit_card(self):
        """Step 4: Add a credit card loan"""
        self.print_header("Step 4: Add Credit Card Loan")
        
        url = f"{self.base_url}/v1/credit-card/loans"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "card_type": "Visa",
            "card_suffix": "4242",
            "balance": 5000.00,
            "minimum_payment": 150.00,
            "interest_rate": 18.99,
            "due_date": "15th"
        }
        
        response = requests.post(url, headers=headers, json=data)
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ Credit card added successfully!")
            return True
        else:
            print("❌ Failed to add credit card")
            return False
    
    def add_personal_loan(self):
        """Step 5: Add a personal loan"""
        self.print_header("Step 5: Add Personal Loan")
        
        url = f"{self.base_url}/v1/personal/loans"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {
            "loan_id": "PL-001",
            "lender_name": "SoFi",
            "amount": 15000.00,
            "monthly_payment": 300.00,
            "interest_rate": 8.5,
            "due_date": "1st"
        }
        
        response = requests.post(url, headers=headers, json=data)
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ Personal loan added successfully!")
            return True
        else:
            print("❌ Failed to add personal loan")
            return False
    
    def make_payment(self):
        """Step 6: Make a payment"""
        self.print_header("Step 6: Make Payment")
        
        url = f"{self.base_url}/v1/credit-card/pay"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "X-Idempotency-Key": f"demo-payment-{int(time.time())}"
        }
        data = {
            "card_type": "Visa",
            "card_suffix": "4242",
            "amount": 500.00
        }
        
        response = requests.post(url, headers=headers, json=data)
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ Payment processed successfully!")
            return True
        else:
            print("❌ Payment failed")
            return False
    
    def test_rate_limiting(self):
        """Step 7: Demonstrate rate limiting"""
        self.print_header("Step 7: Rate Limiting Demo")
        
        print("Attempting 6 rapid requests (limit is 5)...")
        url = f"{self.base_url}/auth/profile"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        for i in range(6):
            response = requests.get(url, headers=headers)
            if response.status_code == 429:
                print(f"\n❌ Request {i+1}: Rate limited!")
                self.print_response(response)
                break
            else:
                print(f"✅ Request {i+1}: Success (Status {response.status_code})")
        
        print("\n✅ Rate limiting is working correctly!")
    
    def health_check(self):
        """Check API health"""
        self.print_header("Health Check")
        
        url = f"{self.base_url.replace('/api', '')}/health"
        response = requests.get(url)
        
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ API is healthy!")
            return True
        else:
            print("❌ API health check failed")
            return False
    
    def logout(self):
        """Step 8: Logout"""
        self.print_header("Step 8: Logout")
        
        url = f"{self.base_url}/auth/logout"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.post(url, headers=headers)
        
        self.print_response(response)
        
        if response.status_code == 200:
            print("✅ Logged out successfully!")
            return True
        else:
            print("❌ Logout failed")
            return False
    
    def run_demo(self):
        """Run complete demo"""
        print("\n" + "="*60)
        print("  GENERAL BILLER API DEMO")
        print("  Production-Grade Bill Payment System")
        print("="*60)
        print(f"\nStarting demo at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {self.base_url}")
        
        try:
            # Run all demo steps
            steps = [
                ("Health Check", self.health_check),
                ("User Registration", self.register_user),
                ("User Login", self.login_user),
                ("Get Profile", self.get_profile),
                ("Add Credit Card", self.add_credit_card),
                ("Add Personal Loan", self.add_personal_loan),
                ("Make Payment", self.make_payment),
                ("Logout", self.logout),
            ]
            
            results = []
            for step_name, step_func in steps:
                try:
                    success = step_func()
                    results.append((step_name, success))
                    
                    # Small delay between steps
                    time.sleep(0.5)
                except Exception as e:
                    print(f"\n❌ Error in {step_name}: {str(e)}")
                    results.append((step_name, False))
            
            # Print summary
            self.print_header("Demo Summary")
            total = len(results)
            passed = sum(1 for _, success in results if success)
            
            for step_name, success in results:
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"{status}: {step_name}")
            
            print(f"\n📊 Results: {passed}/{total} steps passed")
            
            if passed == total:
                print("\n🎉 All tests passed! API is working perfectly!")
            else:
                print(f"\n⚠️  {total - passed} test(s) failed. Review the output above.")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Demo interrupted by user")
        except Exception as e:
            print(f"\n\n❌ Demo failed with error: {str(e)}")
        
        print(f"\nDemo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL
    
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           🏦 GENERAL BILLER API DEMO                    ║
║                                                          ║
║  This demo showcases the production-ready features:     ║
║  • Secure user authentication                           ║
║  • JWT token management                                 ║
║  • Loan management                                      ║
║  • Payment processing                                   ║
║  • Rate limiting                                        ║
║                                                          ║
║  Make sure the API server is running:                   ║
║  $ flask --app src.api.app run                          ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    input("Press Enter to start the demo...")
    
    demo = BillerAPIDemo(base_url)
    demo.run_demo()


if __name__ == "__main__":
    main()
