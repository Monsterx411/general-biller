# General Biller (US & CA)

A comprehensive bill payment application that allows users to make payments to their billers using multiple payment methods.

## Features

### Payment Methods

1. **Credit/Debit Cards**
   - Validate and store card information
   - Match billing addresses with zip codes
   - Secure payment processing

2. **Bank Account Payments**
   - **USA Support:**
     - Bank Name
     - Account Type
     - Account Number
     - Routing Number
     - Account Owner Name and Address
   
   - **Canada Support:**
     - Bank Name
     - Account Type
     - Account Number
     - Institution
     - Bank Transit Number
     - Account Owner Name and Address

3. **Bank Linking**
   - Link bank accounts securely via login
   - Support for multiple banks

4. **Mail Check Payments**
   - Fill in biller address
   - Provide payer information
   - Specify payment amount
   - Automated check mailing

5. **Appointment Scheduling**
   - Book appointments for payments
   - Manage and track upcoming payments

## Project Structure

```
General Biller (US & CA)/
├── src/
│   ├── __init__.py
│   ├── payment/
│   │   ├── __init__.py
│   │   ├── credit_debit.py      # Credit/debit card payment handling
│   │   ├── bank_account.py      # Bank account payment handling
│   │   ├── mail_check.py        # Mail check payment handling
│   │   └── appointment.py       # Appointment scheduling
│   ├── bank_linking/
│   │   ├── __init__.py
│   │   └── bank_login.py        # Bank account linking
│   └── utils/
│       ├── __init__.py
│       ├── validators.py        # Input validation functions
│       └── helpers.py           # Helper functions
├── tests/
│   ├── test_payment.py          # Payment module tests
│   ├── test_bank_linking.py     # Bank linking tests
│   └── test_utils.py            # Utility function tests
├── main.py                      # Main application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── structure.txt                # Workspace structure documentation
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd "General Biller(us & ca)"
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
python main.py
```

This will start an interactive menu where you can:
- 1. Process credit/debit card payments
- 2. Process bank account payments
- 3. Link bank accounts
- 4. Send mail check payments
- 5. Book payment appointments
- 6. Exit

## Testing

Run unit tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_payment.py
pytest tests/test_bank_linking.py
pytest tests/test_utils.py
```

## Validation Functions

The application includes built-in validation for:
- Email addresses
- Phone numbers
- ZIP/Postal codes (USA & Canada formats)
- Account numbers
- Routing numbers (USA)

## Dependencies

- **requests** - HTTP library for external API calls
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework

## Module Documentation

### Payment Module
Handles all payment processing methods including credit cards, bank accounts, mail checks, and appointments.

### Bank Linking Module
Manages secure bank account linking through bank login credentials.

### Utils Module
Provides validation and formatting utilities for:
- Email validation
- Phone number validation
- ZIP code validation (country-specific)
- Currency formatting
- Address formatting

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please contact the development team or open an issue in the repository.

---

**Note:** This application is under development. Some features are placeholders and will be implemented in future versions.
