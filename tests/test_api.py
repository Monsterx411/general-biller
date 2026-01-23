import pytest
from src.api.app import create_app
from src.utils.token import TokenManager

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_readiness(client):
    response = client.get('/readiness')
    assert response.status_code in [200, 503]
    assert 'ready' in response.json or 'status' in response.json

def test_get_token(client):
    response = client.post('/api/v1/auth/token', json={'user_id': 'test-user'})
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert response.json['token_type'] == 'Bearer'

def test_list_loans_without_auth(client):
    response = client.get('/api/v1/loans')
    assert response.status_code == 401

def test_list_loans_with_auth(client):
    token = TokenManager.generate_token('test-user')
    response = client.get('/api/v1/loans', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'endpoints' in response.json

def test_add_credit_card_loan(client):
    response = client.post('/api/v1/credit-card/loans', json={
        'card_type': 'Visa',
        'card_suffix': '1234',
        'balance': 5000,
        'minimum_payment': 150,
        'interest_rate': 18.5,
        'due_date': '12/27'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_add_personal_loan(client):
    # Setup bank account first
    client.post('/api/v1/personal/bank/usa', json={
        'bank_name': 'Test Bank',
        'account_type': 'checking',
        'account_number': '12345678901',
        'routing_number': '021000021',
        'owner_name': 'Jane Doe',
        'address': '123 Main St',
        'available_balance': 100000
    })
    
    response = client.post('/api/v1/personal/loans', json={
        'loan_id': 'PL-001',
        'lender_name': 'Lender',
        'amount': 15000,
        'monthly_payment': 300,
        'interest_rate': 12.5,
        'due_date': '12/27'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_process_personal_payment(client):
    # Setup bank
    client.post('/api/v1/personal/bank/usa', json={
        'bank_name': 'Test Bank',
        'account_type': 'checking',
        'account_number': '12345678901',
        'routing_number': '021000021',
        'owner_name': 'Jane Doe',
        'address': '123 Main St',
        'available_balance': 100000
    })
    
    # Add loan
    client.post('/api/v1/personal/loans', json={
        'loan_id': 'PL-PAY-TEST',
        'lender_name': 'Lender',
        'amount': 15000,
        'monthly_payment': 300,
        'interest_rate': 12.5,
        'due_date': '12/27'
    })
    
    # Make payment
    response = client.post('/api/v1/personal/pay', json={
        'loan_id': 'PL-PAY-TEST',
        'amount': 300
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['remaining_balance'] == 14700.0

def test_add_mortgage(client):
    response = client.post('/api/v1/mortgage/loans', json={
        'mortgage_id': 'M-001',
        'lender_name': 'Lender',
        'property_address': '123 Main St',
        'principal_balance': 250000,
        'monthly_payment': 1200,
        'interest_rate': 6.0,
        'remaining_term_months': 360,
        'due_date': '12/27'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_add_auto_loan(client):
    response = client.post('/api/v1/auto/loans', json={
        'loan_id': 'AL-001',
        'lender_name': 'Lender',
        'vehicle_make': 'Toyota',
        'vehicle_model': 'Camry',
        'vehicle_year': 2020,
        'vin': 'VIN123',
        'loan_amount': 25000,
        'monthly_payment': 350,
        'interest_rate': 5.0,
        'months_remaining': 60,
        'due_date': '12/27'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'
