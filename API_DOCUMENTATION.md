# General Biller API Documentation

## Base URL
```
Development: http://localhost:5000/api
Production: https://yourdomain.com/api
```

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Rate Limiting

API endpoints have rate limiting to prevent abuse:
- Registration: 5 requests per hour per IP
- Login: 10 requests per 5 minutes per IP
- Other endpoints: Varies by endpoint

Rate limit headers included in responses:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 60
```

## Authentication Endpoints

### POST /auth/register

Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe",
  "phone": "+1234567890"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

**Success Response (201 Created):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone": "+1234567890",
    "is_active": true,
    "is_verified": false,
    "mfa_enabled": false,
    "created_at": "2026-01-31T10:30:00.000Z"
  }
}
```

**Error Responses:**
- 400: Invalid input (weak password, invalid email, duplicate email)
- 429: Rate limit exceeded

---

### POST /auth/login

Authenticate and receive access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "mfa_code": "123456"
}
```

Note: `mfa_code` is only required if MFA is enabled for the user.

**Success Response (200 OK):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "mfa_enabled": false,
    "last_login": "2026-01-31T10:30:00.000Z"
  }
}
```

**Error Responses:**
- 400: MFA code required
- 401: Invalid credentials or MFA code
- 403: Account locked or inactive
- 429: Rate limit exceeded

---

### POST /auth/logout

Logout and revoke current session.

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses:**
- 401: Invalid or missing token

---

### GET /auth/profile

Get current user profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "is_active": true,
  "is_verified": false,
  "mfa_enabled": true,
  "created_at": "2026-01-31T10:30:00.000Z",
  "last_login": "2026-01-31T12:00:00.000Z"
}
```

---

## Multi-Factor Authentication (MFA)

### POST /auth/mfa/setup

Initialize MFA setup and get QR code for authenticator app.

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "secret": "JBSWY3DPEHPK3PXP",
  "qr_code": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "provisioning_uri": "otpauth://totp/General%20Biller:user@example.com?secret=JBSWY3DPEHPK3PXP&issuer=General%20Biller"
}
```

**Instructions:**
1. Scan the QR code with your authenticator app (Google Authenticator, Authy, etc.)
2. Use the code from your app to call `/auth/mfa/enable`

---

### POST /auth/mfa/enable

Enable MFA after verifying with TOTP code.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "code": "123456"
}
```

**Success Response (200 OK):**
```json
{
  "message": "MFA enabled successfully"
}
```

**Error Responses:**
- 400: MFA code required or MFA not set up
- 401: Invalid MFA code

---

### POST /auth/mfa/disable

Disable MFA (requires password confirmation).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "password": "SecurePass123!"
}
```

**Success Response (200 OK):**
```json
{
  "message": "MFA disabled successfully"
}
```

**Error Responses:**
- 400: Password required
- 401: Invalid password

---

## Loan Management Endpoints

### POST /v1/credit-card/loans

Add a new credit card loan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "card_type": "Visa",
  "card_suffix": "4242",
  "balance": 5000.00,
  "minimum_payment": 150.00,
  "interest_rate": 18.99,
  "due_date": "15th"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Credit card loan added successfully",
  "loan_id": "Visa-4242"
}
```

---

### POST /v1/personal/loans

Add a new personal loan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "loan_id": "PL-001",
  "lender_name": "SoFi",
  "amount": 15000.00,
  "monthly_payment": 300.00,
  "interest_rate": 8.5,
  "due_date": "1st"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Personal loan added successfully",
  "loan_id": "PL-001"
}
```

---

### POST /v1/mortgage/loans

Add a new mortgage loan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "mortgage_id": "MTG-001",
  "lender_name": "Bank of America",
  "property_address": "123 Main St, Anytown, USA",
  "principal_balance": 350000.00,
  "monthly_payment": 2100.00,
  "interest_rate": 4.5,
  "remaining_term_months": 360,
  "due_date": "1st"
}
```

---

### POST /v1/auto/loans

Add a new auto loan.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "loan_id": "AUTO-001",
  "lender_name": "Chase Auto Finance",
  "vehicle_make": "Toyota",
  "vehicle_model": "Camry",
  "vehicle_year": "2022",
  "vin": "1HGBH41JXMN109186",
  "loan_amount": 25000.00,
  "monthly_payment": 450.00,
  "interest_rate": 6.5,
  "months_remaining": 60,
  "due_date": "10th"
}
```

---

## Payment Endpoints

### POST /v1/credit-card/pay

Make a payment toward credit card loan.

**Headers:**
```
Authorization: Bearer <token>
X-Idempotency-Key: <unique-key>
```

**Request Body:**
```json
{
  "card_type": "Visa",
  "card_suffix": "4242",
  "amount": 500.00
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "transaction_id": "TXN20260131103000",
  "amount": 500.00,
  "remaining_balance": 4500.00,
  "message": "Payment processed successfully"
}
```

---

### POST /v1/personal/pay

Make a payment toward personal loan.

**Headers:**
```
Authorization: Bearer <token>
X-Idempotency-Key: <unique-key>
```

**Request Body:**
```json
{
  "loan_id": "PL-001",
  "amount": 300.00
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "transaction_id": "TXN20260131103100",
  "amount": 300.00,
  "remaining_balance": 14700.00,
  "message": "Payment processed successfully"
}
```

---

## Bank Account Management

### POST /v1/personal/bank/usa

Set up USA bank account for personal loan payments (ACH).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "bank_name": "Chase",
  "account_type": "checking",
  "account_number": "123456789",
  "routing_number": "021000021",
  "owner_name": "John Doe",
  "address": "123 Main St, City, State 12345",
  "available_balance": 10000.00
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "USA bank account configured successfully"
}
```

Note: Account numbers are encrypted at rest and masked in API responses.

---

### POST /v1/personal/bank/canada

Set up Canadian bank account for personal loan payments (EFT).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "bank_name": "TD Canada Trust",
  "account_type": "chequing",
  "account_number": "1234567",
  "institution_number": "004",
  "transit_number": "12345",
  "owner_name": "John Doe",
  "address": "123 Main St, City, Province A1A 1A1",
  "available_balance": 10000.00
}
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid input",
  "details": ["Field 'email' is required", "Password is too weak"]
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Account locked",
  "locked_until": "2026-01-31T11:00:00.000Z"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Try again later.",
  "retry_after": 300
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## Idempotency

Payment endpoints support idempotency to prevent duplicate transactions:

**Header:**
```
X-Idempotency-Key: unique-client-generated-key
```

- Use a unique key for each payment request
- If the same key is used within 24 hours, the original response is returned
- Prevents accidental duplicate payments

**Example:**
```bash
curl -X POST https://api.example.com/api/v1/credit-card/pay \
  -H "Authorization: Bearer <token>" \
  -H "X-Idempotency-Key: pay-123456789" \
  -H "Content-Type: application/json" \
  -d '{"card_type": "Visa", "amount": 500.00}'
```

---

## Security Best Practices

1. **Always use HTTPS** in production
2. **Store tokens securely** (never in localStorage, prefer httpOnly cookies)
3. **Implement token refresh** before expiration
4. **Enable MFA** for all user accounts
5. **Use idempotency keys** for all payment operations
6. **Validate input** on the client side before sending
7. **Handle errors gracefully** and don't expose sensitive information

---

## Health Check Endpoints

### GET /health
Simple health check.

**Response:**
```json
{
  "status": "ok",
  "environment": "production"
}
```

### GET /readiness
Comprehensive readiness check.

**Response:**
```json
{
  "ready": true,
  "status": "all systems operational"
}
```

---

## Support

For API support or to report issues:
- Email: api-support@yourcompany.com
- Documentation: https://docs.yourcompany.com
- Status Page: https://status.yourcompany.com

---

**Last Updated:** January 31, 2026  
**API Version:** 1.0.0
