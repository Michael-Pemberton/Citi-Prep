import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import repository.data_store as store
from repository.data_store import seed
from models.models import AccountCreate, AccountUpdate, AccountType
import services.account_service as account_service


@pytest.fixture(autouse=True)
def reset_store():
    store.customers.clear()
    store.accounts.clear()
    store._customer_id_counter = 0
    store._account_id_counter = 0
    seed()


class TestGetAllAccounts:
    def test_getAllAccounts_success(self):
        result = account_service.get_all_accounts()
        assert len(result) == 6

    def test_getAllAccounts_fail_returns_empty_after_clear(self):
        store.accounts.clear()
        result = account_service.get_all_accounts()
        assert result == []


class TestGetAccountById:
    def test_getAccountById_success(self):
        result = account_service.get_account_by_id(1)
        assert result is not None
        assert result.account_number == "S1001"

    def test_getAccountById_fail_notFound(self):
        result = account_service.get_account_by_id(999)
        assert result is None


class TestGetAccountByName:
    def test_getAccountByName_success(self):
        result = account_service.get_account_by_name("Jane")
        assert len(result) >= 1

    def test_getAccountByName_fail_noMatch(self):
        result = account_service.get_account_by_name("ZZZNoMatch")
        assert result == []


class TestCreateAccount:
    def test_createAccount_success(self):
        payload = AccountCreate(
            account_number="S9001",
            account_type=AccountType.savings,
            balance=750.00,
            customer_id=2
        )
        result = account_service.create_account(payload)
        assert result is not None
        assert result.account_number == "S9001"

    def test_createAccount_fail_customerNotFound(self):
        payload = AccountCreate(
            account_number="S9999",
            account_type=AccountType.savings,
            balance=500.00,
            customer_id=999
        )
        result = account_service.create_account(payload)
        assert result is None


class TestUpdateAccount:
    def test_updateAccount_success(self):
        payload = AccountUpdate(balance=9999.99)
        result = account_service.update_account(1, payload)
        assert result is not None
        assert result.balance == 9999.99

    def test_updateAccount_fail_notFound(self):
        payload = AccountUpdate(balance=100.00)
        result = account_service.update_account(999, payload)
        assert result is None


class TestDeleteAccount:
    def test_deleteAccount_success(self):
        result = account_service.delete_account(1)
        assert result is True
        assert account_service.get_account_by_id(1) is None

    def test_deleteAccount_fail_notFound(self):
        result = account_service.delete_account(999)
        assert result is False
