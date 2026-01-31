# General Biller - Project Information

## Project Name
**General Biller - Enterprise Bill Payment System**

## Short Description
Production-ready enterprise bill payment system for USA and Canada with bank-grade security, multi-factor authentication, and regulatory compliance.

## Full Description

General Biller is a comprehensive, enterprise-grade loan and bill payment management platform designed specifically for the USA and Canada markets. The system provides secure, compliant, and user-friendly management of multiple loan types including credit cards, personal loans, mortgages, and auto loans.

Built with modern security practices and compliance requirements in mind, General Biller implements:

### Security Features
- JWT-based authentication with 24-hour token expiration
- Multi-factor authentication (TOTP) with QR code provisioning
- Field-level encryption for sensitive data (Fernet/AES-128)
- PBKDF2-SHA256 password hashing with 100,000 iterations
- PCI DSS compliant credit card data handling
- API rate limiting and DDoS protection
- Security headers (HSTS, CSP, X-Frame-Options)
- Comprehensive audit logging

### Payment Processing
- USA ACH payments with routing number validation
- Canada EFT payments with transit number validation
- Credit card payment processing
- Check payment support for mortgages
- Transaction tracking and reconciliation
- Idempotency keys for duplicate prevention
- Multi-status transaction management (pending/completed/failed)

### Compliance Framework
- USA: GLBA, PCI DSS, FCRA compliance framework
- Canada: PIPEDA, FINTRAC compliance framework
- Comprehensive audit trails for regulatory requirements
- Transaction monitoring and reporting
- Data retention and privacy controls

### Technical Stack
- **Backend**: Python 3.8+, Flask, SQLAlchemy
- **Database**: PostgreSQL (production), SQLite (development)
- **Security**: Cryptography, PyJWT, passlib, pyotp
- **Frontend**: Next.js, React (optional)
- **Deployment**: Docker, Gunicorn, Nginx

## Topics/Tags
bill-payment, loan-management, payment-processing, banking, fintech, usa, canada, ach, eft, credit-card, mortgage, personal-loan, auto-loan, enterprise, security, compliance, pci-dss, glba, pipeda, flask, python, react, nextjs, jwt, mfa, encryption, audit-logging, postgresql, sqlalchemy

## Repository URL
https://github.com/Monsterx411/general-biller

## Documentation
- Main README: README.md
- API Documentation: API_DOCUMENTATION.md
- Security Guide: SECURITY.md
- Deployment Guide: DEPLOYMENT.md
- Enhancement Summary: ENHANCEMENT_SUMMARY.md

## License
MIT License - See LICENSE file

## Version
2.0.0

## Status
Production-Ready (Beta)

## Author
Monsterx411

## Support Contact
- Issues: https://github.com/Monsterx411/general-biller/issues
- Security: Report vulnerabilities privately through GitHub Security Advisories

## Last Updated
January 31, 2026
