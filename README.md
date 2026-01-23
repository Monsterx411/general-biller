# Loan Payment Manager (USA & Canada)

A comprehensive loan payment management system that enables users to make payments toward multiple types of loans in the USA and Canada. Manage all your loans in one unified platform.

## Features

### Supported Loan Types

1. **Credit Card Loans**
   - Track multiple credit card accounts
   - Monitor balances and minimum payments
   - Process credit card payments with interest tracking
   - Track due dates

2. **Personal Loans**
   - Support for both USA and Canada
   - Bank account integration for payments
   - Track personal loan balances
   - Monitor interest rates and payment schedules

3. **Home Loans (Mortgages)**
   - Track mortgage payments
   - Support for both USA and Canada
   - Property address tracking
   - Remaining term calculation
   - Bank transfer or check payment options

4. **Auto Loans**
   - Vehicle information tracking (Make, Model, Year, VIN)
   - Monthly payment management
   - Payment history tracking
   - Months remaining calculation

### Payment Methods

- **Bank Transfer** (ACH for USA, EFT for Canada)
  - USA: Account Number + Routing Number
  - Canada: Account Number + Transit Number

- **Check Payments**
  - For mortgage and personal loans
  - Complete payer information tracking

- **Credit Card** (For paying credit card balances)

### Regional Support

- **USA Features:**
  - Routing number support
  - State/ZIP code validation
  - US bank formats

- **Canada Features:**
  - Transit number support
  - Province/Postal code validation
  - Canadian bank formats

## Project Structure

```
Loan Payment Manager/
├── src/
│   ├── __init__.py
│   ├── payment/
│   │   ├── __init__.py
│   │   ├── credit_debit.py       # Credit card loan payments
│   │   ├── bank_account.py       # Personal loan payments
│   │   ├── mail_check.py         # Mortgage payments
│   │   └── appointment.py        # Auto loan payments
│   ├── bank_linking/
│   │   ├── __init__.py
│   │   └── bank_login.py         # Bank account integration
│   └── utils/
│       ├── __init__.py
│       ├── validators.py         # Input validation
│       └── helpers.py            # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_payment.py           # Payment module tests
│   ├── test_bank_linking.py      # Bank linking tests
│   └── test_utils.py             # Utility function tests
├── main.py                       # Main application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git configuration
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Monsterx411/general-biller.git
cd "general-biller"
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
export PYTHONPATH=$PWD
python main.py
```

The application provides an interactive menu interface for:

1. **Credit Card Loan Management**
   - Add credit card accounts
   - Track balances and interest
   - Make payments
   - View account details

2. **Personal Loan Management**
   - Configure bank accounts (USA/Canada)
   - Add multiple personal loans
   - Process payments
   - Track loan details

3. **Mortgage Management**
   - Add mortgage accounts
   - Set payment methods (bank/check)
   - Process payments
   - Track remaining term

4. **Auto Loan Management**
   - Add vehicle loans
   - Track vehicle information
   - Process payments
   - View payment history

## Testing

Run all tests:
```bash
export PYTHONPATH=$PWD
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_payment.py -v
pytest tests/test_bank_linking.py -v
pytest tests/test_utils.py -v
```

## Validation Features

The system includes comprehensive validation for:
- Email addresses
- Phone numbers
- ZIP codes (USA format: 12345 or 12345-6789)
- Postal codes (Canada format: A1A 1A1)
- Bank account numbers
- Routing numbers (USA - 9 digits)
- Transit numbers (Canada)

## Key Classes

### CreditCardLoanPayment
Manages credit card loan accounts and payments.

### PersonalLoanPayment
Handles personal loans with bank account integration for both USA and Canada.

### HomeLoanPayment
Manages mortgage payments with flexible payment methods.

### AutoLoanPayment
Tracks auto loans with vehicle information and payment history.

## API Examples

### Credit Card Loan
```python
cc = CreditCardLoanPayment()
cc.add_credit_card_loan("Visa", "1234", 5000, 150, 18.5, "12/25")
result = cc.process_payment("Visa", 500)
```

### Personal Loan
```python
personal = PersonalLoanPayment("USA")
personal.set_usa_bank_account("Chase", "Checking", "123456789", "021000021", "John Doe", "123 Main St", 10000)
personal.add_personal_loan("PL001", "SoFi", 15000, 300, 8.5, "15th")
result = personal.process_payment("PL001", 300)
```

### Mortgage
```python
mortgage = HomeLoanPayment("USA")
mortgage.add_mortgage("ML001", "Bank of America", "123 Oak St", 350000, 2100, 4.5, 360, "01st")
mortgage.set_payment_method_bank("123456789", routing_number="021000021")
result = mortgage.process_payment("ML001", 2100)
```

### Auto Loan
```python
auto = AutoLoanPayment()
vehicle = {"make": "Toyota", "model": "Camry", "year": "2022", "vin": "ABC123"}
auto.add_auto_loan("AL001", "Chase Auto", vehicle, 25000, 450, 6.5, 60, "10th")
result = auto.process_payment("AL001", 450)
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [ ] Complete bank linking integration
- [ ] Payment reminders and notifications
- [ ] PDF statement generation
- [ ] Multi-currency support
- [ ] API integration with major banks
- [ ] Mobile application
- [ ] Database persistence
- [ ] User authentication

---

**Note:** This is a financial management application. Ensure all sensitive data (account numbers, routing numbers) are properly secured and encrypted in production environments.
