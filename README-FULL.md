# Loan Manager - Enterprise Payment Solution

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![License](https://img.shields.io/badge/License-MIT-yellow)

A production-ready, enterprise-grade loan payment management system supporting **USA & Canada** with comprehensive validation, security, and multi-platform deployment capabilities.

## Features

### 🏦 Multi-Loan Support
- **Credit Card Loans** - Luhn-validated card payments with fraud detection
- **Personal Loans** - USA & Canada bank account transfers with country-specific routing/transit numbers
- **Home Loans (Mortgages)** - Multi-method payment support (bank, check, etc.)
- **Auto Loans** - Vehicle tracking with payment history

### 🌍 Global Banking Support
- **USA**: Routing numbers, ZIP code validation, ACH transfers
- **Canada**: Transit numbers, institution numbers, postal code validation, EFT transfers

### 🔐 Enterprise Security
- JWT token authentication
- PBKDF2-SHA256 password hashing (100k iterations)
- Account and credit card masking
- Fraud detection with configurable limits
- Request logging with unique IDs
- Secure token generation

### ✅ Comprehensive Validation
- 15+ production-grade validators
- Luhn algorithm for credit cards
- CVV validation (3-4 digits)
- Expiry date validation (future-only)
- Loan amount validation ($100 - $10M range)
- Interest rate validation (0-50%)

### 📊 Data Persistence
- SQLAlchemy ORM for database abstraction
- JSON-based storage (dev mode)
- PostgreSQL (production)
- Alembic migrations for schema versioning
- Transaction history tracking

### 🚀 Full-Stack Deployment
- Docker & Docker Compose
- Gunicorn WSGI server
- Nginx reverse proxy with SSL support
- Next.js frontend
- Mobile-ready API

---

## Project Structure

```
.
├── src/
│   ├── api/              # Flask REST API
│   │   ├── app.py        # App factory, health checks, Swagger
│   │   └── routes.py     # API endpoints (v1)
│   ├── models/           # SQLAlchemy models
│   │   ├── db.py         # Database configuration
│   │   ├── loan.py       # Loan model
│   │   └── payment.py    # Payment model
│   ├── payment/          # Loan service modules
│   │   ├── credit_debit.py
│   │   ├── bank_account.py
│   │   ├── mail_check.py
│   │   └── appointment.py
│   ├── utils/            # Utilities
│   │   ├── validators.py # 15+ validators
│   │   ├── security.py   # Encryption, masking, fraud checks
│   │   ├── token.py      # JWT authentication
│   │   ├── middleware.py # Logging, error handling
│   │   ├── database.py   # JSON DB (legacy)
│   │   └── logger.py     # Logging config
│   └── config.py         # Environment-based config
├── frontend/             # Next.js React app
│   ├── pages/
│   │   ├── index.js
│   │   ├── credit-card.js
│   │   ├── personal.js
│   │   ├── mortgage.js
│   │   └── auto.js
│   ├── package.json
│   └── next.config.js
├── mobile/               # React Native Expo
│   └── README.md         # Setup guide
├── desktop/              # Electron/PyInstaller
│   └── README.md         # Setup guide
├── tests/                # Test suites
│   ├── test_payment.py
│   ├── test_api.py
│   ├── test_utils.py
│   └── test_bank_linking.py
├── alembic/              # Database migrations
├── nginx/                # Reverse proxy config
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Web + DB + Nginx stack
├── requirements.txt      # Python dependencies
├── deploy.sh             # Deployment script
└── README.md
```

---

## Quick Start (Local Development)

### Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- Docker & Docker Compose (optional)

### 1. Clone & Setup Python

```bash
git clone https://github.com/Monsterx411/general-biller.git
cd general-biller
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and set SECRET_KEY, ENCRYPTION_KEY, POSTGRES_PASSWORD
```

### 3. Run Tests

```bash
pytest tests/ -v
```

### 4. Run API Server

```bash
# Development (Flask dev server)
python -c "from src.api.app import create_app; app=create_app(); app.run(host='0.0.0.0', port=8000)"

# Production (Gunicorn)
gunicorn -b 0.0.0.0:8000 src.api.app:app
```

### 5. Test API

```bash
# Get token
curl -X POST http://localhost:8000/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user-123"}'

# Use token to access protected endpoint
TOKEN="<your-token-here>"
curl -X GET http://localhost:8000/api/v1/loans \
  -H "Authorization: Bearer $TOKEN"

# Create personal loan
curl -X POST http://localhost:8000/api/v1/personal/bank/usa \
  -H "Content-Type: application/json" \
  -d '{
    "bank_name": "Chase",
    "account_type": "checking",
    "account_number": "12345678901",
    "routing_number": "021000021",
    "owner_name": "John Doe",
    "address": "123 Main St",
    "available_balance": 100000
  }'

curl -X POST http://localhost:8000/api/v1/personal/loans \
  -H "Content-Type: application/json" \
  -d '{
    "loan_id": "PL-001",
    "lender_name": "Chase Bank",
    "amount": 15000,
    "monthly_payment": 300,
    "interest_rate": 12.5,
    "due_date": "12/27"
  }'

curl -X POST http://localhost:8000/api/v1/personal/pay \
  -H "Content-Type: application/json" \
  -d '{"loan_id": "PL-001", "amount": 300}'
```

### 6. Run Frontend

```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

---

## Docker Deployment

### Build & Run Full Stack

```bash
docker compose up -d --build
curl http://localhost/health
```

### Services
- **web** (Gunicorn): http://localhost:8000
- **db** (PostgreSQL): localhost:5432
- **nginx**: http://localhost:80

### View Logs

```bash
docker compose logs -f web
docker compose logs -f db
```

---

## Production Deployment (globe-swift.org)

### Prerequisites
- Ubuntu 22.04+ server
- Docker & Docker Compose installed
- Domain DNS pointing to server IP

### 1. Clone & Setup

```bash
git clone https://github.com/Monsterx411/general-biller.git
cd general-biller
cp .env.example .env
```

### 2. Set Environment Variables

```bash
# Edit .env:
ENVIRONMENT=production
DOMAIN=globe-swift.org
SECRET_KEY=<generate-strong-key>
ENCRYPTION_KEY=<generate-base64-key>
POSTGRES_PASSWORD=<strong-password>
```

### 3. Start Services

```bash
docker compose up -d --build
```

### 4. Configure HTTPS

#### Option A: Certbot (Let's Encrypt)

```bash
sudo apt install -y certbot
sudo certbot certonly --standalone -d globe-swift.org -d www.globe-swift.org
# Update nginx/ssl.conf with cert paths
docker compose restart nginx
```

#### Option B: Caddy (Automatic TLS)

Replace nginx service with Caddy, create Caddyfile:
```
globe-swift.org {
    reverse_proxy web:8000
}
```

### 5. Enable Monitoring

```bash
curl http://globe-swift.org/health
curl http://globe-swift.org/readiness
```

---

## API Documentation

### Authentication

**Get Token:**
```
POST /api/v1/auth/token
Content-Type: application/json

{
  "user_id": "user-123"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 86400
}
```

### Credit Card Loans

**Create Loan:**
```
POST /api/v1/credit-card/loans
```

**Make Payment:**
```
POST /api/v1/credit-card/pay
```

### Personal Loans

**Set Bank Account (USA):**
```
POST /api/v1/personal/bank/usa
```

**Set Bank Account (Canada):**
```
POST /api/v1/personal/bank/canada
```

**Create Loan:**
```
POST /api/v1/personal/loans
```

**Make Payment:**
```
POST /api/v1/personal/pay
```

### Mortgages

**Create Mortgage:**
```
POST /api/v1/mortgage/loans
```

**Make Payment:**
```
POST /api/v1/mortgage/pay
```

### Auto Loans

**Create Loan:**
```
POST /api/v1/auto/loans
```

**Make Payment:**
```
POST /api/v1/auto/pay
```

---

## Mobile Apps

### React Native (Expo)

```bash
npx create-expo-app mobile
cd mobile
# Configure API_BASE=https://globe-swift.org/api
expo build:android  # APK
expo build:ios      # IPA
```

### Capacitor (Web Wrapper)

```bash
npm create @capacitor/app
npx cap add android
npx cap add ios
```

---

## macOS Desktop App

### Electron

```bash
npm create electron-app
# Wrap frontend build
npm run make
```

### PyInstaller

```bash
pip install pyinstaller
pyinstaller -n LoanManager src/api/app.py
```

---

## Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Specific Test Suite

```bash
pytest tests/test_api.py -v
pytest tests/test_payment.py -v
pytest tests/test_utils.py -v
```

### Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## Database Migrations (Alembic)

### Create Migration

```bash
alembic revision --autogenerate -m "Add new column"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Downgrade

```bash
alembic downgrade -1
```

---

## Environment Variables

| Variable | Default | Notes |
|----------|---------|-------|
| `ENVIRONMENT` | development | production/testing |
| `DOMAIN` | localhost | Domain for CORS/deployment |
| `SECRET_KEY` | dev-key | Required for JWT signing |
| `ENCRYPTION_KEY` | None | Required for production |
| `DATABASE_URL` | sqlite | PostgreSQL for production |
| `POSTGRES_PASSWORD` | N/A | Database password |
| `MAX_TRANSACTION_AMOUNT` | 100000 | Max transaction in $ |
| `MAX_DAILY_TRANSACTIONS` | 10 | Daily limit count |
| `FRAUD_CHECK_ENABLED` | true | Enable fraud detection |
| `FRAUD_ALERT_THRESHOLD` | 10000 | Alert threshold in $ |

---

## Architecture

### Backend (Python/Flask)
- REST API with JWT auth
- 4 loan payment services
- SQLAlchemy ORM
- Comprehensive validation
- Fraud detection

### Database
- SQLAlchemy models
- PostgreSQL (production)
- Alembic migrations
- Transaction history

### Frontend (Next.js)
- Server-side rendering
- API integration
- Responsive design
- Loan management pages

### Deployment
- Docker containerization
- Nginx reverse proxy
- SSL/TLS support
- Health checks & monitoring

---

## Security Checklist

- ✅ JWT authentication on protected routes
- ✅ Password hashing (PBKDF2-SHA256)
- ✅ Account masking (****6789)
- ✅ Credit card masking (4532 **** **** 0366)
- ✅ Fraud detection with limits
- ✅ Request logging with IDs
- ✅ CORS configured
- ✅ SSL/TLS ready
- ✅ Rate limiting ready (extensible)
- ✅ Input validation on all endpoints

---

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### Database Connection Error
```bash
# Check PostgreSQL is running
docker compose logs db
# Reset migrations
alembic downgrade base
alembic upgrade head
```

### Token Expired
```bash
# Get new token
curl -X POST http://localhost:8000/api/v1/auth/token \
  -d '{"user_id":"user-123"}'
```

### SSL Certificate Issues
```bash
# Check cert expiry
openssl x509 -in /etc/letsencrypt/live/globe-swift.org/fullchain.pem -noout -dates
# Renew
certbot renew
```

---

## Contributing

1. Fork the repo
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see LICENSE file

---

## Support & Contact

- **GitHub**: https://github.com/Monsterx411/general-biller
- **API Docs**: http://localhost:8000/api/docs
- **Issues**: GitHub Issues

---

## Roadmap

- [ ] Stripe/Plaid integration
- [ ] Advanced analytics dashboard
- [ ] Email/SMS notifications
- [ ] Multi-currency support
- [ ] Machine learning fraud detection
- [ ] White-label capabilities
- [ ] Mobile native apps (React Native)
- [ ] OAuth2 integration

---

**Status**: Production Ready ✅  
**Last Updated**: January 2026  
**Version**: 1.0.0
