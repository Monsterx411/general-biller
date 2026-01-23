# Unit tests for bank linking module
import pytest
from src.bank_linking import BankLink

def test_bank_link_creation():
    bank_link = BankLink()
    assert bank_link.linked_accounts == []

def test_link_bank_account():
    bank_link = BankLink()
    account = bank_link.link_bank_account("Chase", "user@example.com", "password123")
    assert account["bank_name"] == "Chase"
    assert account["linked"] == True
    assert len(bank_link.linked_accounts) == 1
