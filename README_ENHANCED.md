# 🏦 General Biller - Enterprise Bill Payment System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security: Enhanced](https://img.shields.io/badge/security-enhanced-green.svg)](SECURITY.md)

A production-grade loan payment management system for USA and Canada with enterprise security features, multi-factor authentication, and compliance with banking standards.

## ✨ Key Features

### 🔒 **Enterprise Security**
- **User Authentication**: Secure registration and login with PBKDF2-SHA256 password hashing
- **Multi-Factor Authentication (MFA)**: TOTP-based 2FA with QR code support
- **Data Encryption**: Field-level encryption for sensitive data (account numbers, routing numbers)
- **Rate Limiting**: API protection against abuse and DDoS attacks
- **Audit Logging**: Comprehensive audit trail for compliance
- **Session Management**: JWT tokens with expiration and revocation
- **Account Lockout**: Automatic protection after failed login attempts

### 💳 **Supported Loan Types**
1. **Credit Card Loans** - Track balances, interest, and make payments
2. **Personal Loans** - Bank account integration for ACH/EFT payments
3. **Mortgages** - Property tracking with flexible payment methods
4. **Auto Loans** - Vehicle information and payment history

### 🌍 **Regional Support**
- **USA**: ACH payments, routing number validation, ZIP codes
- **Canada**: EFT payments, transit numbers, postal codes

### 🛡️ **Compliance Features**
- PCI DSS compliant card data handling
- GLBA privacy safeguards
- PIPEDA personal information protection
- Comprehensive audit logging
- Transaction monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (recommended for production) or SQLite (development)
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Monsterx411/general-biller.git
cd general-biller
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important:** Generate secure keys for production:
```bash
# Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

5. **Initialize database:**
```bash
# Run migrations
alembic upgrade head

# Or initialize directly
python -c "from src.models.db import init_db; init_db()"
```

6. **Run the application:**

**API Server:**
```bash
# Development
flask --app src.api.app run --debug

# Production
gunicorn src.api.app:app -w 4 -b 0.0.0.0:8000
```

**CLI Interface:**
```bash
python main.py
```

## 📚 Documentation

- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Security Guide](SECURITY.md) - Security features and best practices
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions

## 🔐 Authentication Flow

### 1. Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### 3. Use the Token
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer <your_token>"
```

## 💡 API Examples

### Add a Credit Card Loan
```bash
curl -X POST http://localhost:5000/api/v1/credit-card/loans \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "card_type": "Visa",
    "card_suffix": "4242",
    "balance": 5000.00,
    "minimum_payment": 150.00,
    "interest_rate": 18.99,
    "due_date": "15th"
  }'
```

### Make a Payment
```bash
curl -X POST http://localhost:5000/api/v1/credit-card/pay \
  -H "Authorization: Bearer <token>" \
  -H "X-Idempotency-Key: payment-$(date +%s)" \
  -H "Content-Type: application/json" \
  -d '{
    "card_type": "Visa",
    "amount": 500.00
  }'
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test suite:
```bash
pytest tests/test_auth.py -v          # Authentication tests
pytest tests/test_payment.py -v        # Payment tests
pytest tests/test_api.py -v            # API integration tests
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov-report=html
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM and database management
- **PostgreSQL/SQLite** - Database
- **Alembic** - Database migrations
- **PyJWT** - JWT authentication
- **Cryptography** - Data encryption
- **passlib** - Password hashing

### Security
- **Fernet** - Symmetric encryption
- **PBKDF2-SHA256** - Password hashing (100k iterations)
- **TOTP** - Multi-factor authentication
- **Rate Limiting** - API protection
- **Security Headers** - HSTS, CSP, X-Frame-Options

### Testing
- **pytest** - Test framework
- **pytest-cov** - Code coverage

## 📁 Project Structure

```
general-biller/
├── src/
│   ├── api/
│   │   ├── app.py                  # Flask application
│   │   ├── routes.py               # Loan/payment routes
│   │   └── auth_routes.py          # Authentication routes
│   ├── models/
│   │   ├── db.py                   # Database configuration
│   │   ├── user.py                 # User and session models
│   │   ├── loan.py                 # Loan model
│   │   ├── payment.py              # Payment model
│   │   └── audit.py                # Audit and transaction models
│   ├── payment/
│   │   ├── credit_debit.py         # Credit card payments
│   │   ├── bank_account.py         # Bank payments
│   │   ├── mail_check.py           # Check payments
│   │   └── appointment.py          # Auto loan payments
│   ├── utils/
│   │   ├── security.py             # Password hashing
│   │   ├── encryption.py           # Data encryption
│   │   ├── rate_limit.py           # Rate limiting
│   │   ├── security_middleware.py  # Security headers
│   │   ├── validators.py           # Input validation
│   │   └── token.py                # JWT management
│   └── config.py                   # Configuration
├── alembic/
│   └── versions/                   # Database migrations
├── tests/
│   ├── test_auth.py               # Authentication tests
│   ├── test_payment.py            # Payment tests
│   └── test_api.py                # API tests
├── frontend/                       # React frontend (optional)
├── main.py                        # CLI entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── API_DOCUMENTATION.md           # API reference
├── SECURITY.md                    # Security guide
├── DEPLOYMENT.md                  # Deployment guide
└── README.md                      # This file
```

## 🔒 Security Features

### Authentication & Authorization
- ✅ Secure user registration with email validation
- ✅ Strong password requirements (8+ chars, mixed case, numbers, symbols)
- ✅ PBKDF2-SHA256 password hashing (100,000 iterations)
- ✅ JWT token authentication (24-hour expiration)
- ✅ Multi-factor authentication (TOTP)
- ✅ Account lockout after 5 failed attempts
- ✅ Session tracking and revocation

### Data Protection
- ✅ Field-level encryption for sensitive data
- ✅ PCI DSS compliant card data handling
- ✅ Account number masking (shows last 4 digits)
- ✅ Secure key management
- ✅ HTTPS enforcement in production

### API Security
- ✅ Rate limiting on all endpoints
- ✅ Idempotency keys for payments
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ CORS configuration
- ✅ Request logging with unique IDs

### Compliance & Auditing
- ✅ Comprehensive audit logging
- ✅ Transaction history tracking
- ✅ Failed attempt monitoring
- ✅ User activity logging
- ✅ Regulatory compliance framework

## 🌐 Environment Variables

Required environment variables (see `.env.example`):

```env
# Application
ENVIRONMENT=development
SECRET_KEY=<generate-strong-key>
ENCRYPTION_KEY=<generate-fernet-key>

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Security
MAX_TRANSACTION_AMOUNT=100000
FRAUD_CHECK_ENABLED=true
```

## 🚢 Deployment

### Docker
```bash
docker-compose up -d
```

### Manual Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📊 Monitoring

Monitor these metrics:
- Failed login attempts
- API rate limit hits
- Transaction volumes
- Error rates
- Response times

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Run tests before submitting PR

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [API Docs](API_DOCUMENTATION.md), [Security](SECURITY.md)
- **Issues**: [GitHub Issues](https://github.com/Monsterx411/general-biller/issues)
- **Security**: security@yourcompany.com (for vulnerabilities)

## 🗺️ Roadmap

- [x] User authentication and authorization
- [x] Multi-factor authentication
- [x] Data encryption
- [x] Comprehensive audit logging
- [ ] Payment processor integration (Stripe, Plaid)
- [ ] Real-time payment notifications
- [ ] Advanced fraud detection
- [ ] Mobile app (React Native)
- [ ] Multi-currency support
- [ ] Scheduled payments
- [ ] PDF statement generation
- [ ] Email notifications
- [ ] KYC/AML integration

## 🙏 Acknowledgments

- Built with security best practices from OWASP
- Compliance framework based on USA/Canada banking regulations
- Inspired by modern fintech applications

---

**Version**: 2.0.0  
**Last Updated**: January 31, 2026

Made with ❤️ for secure bill payment management
