import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import repository.data_store as store
from repository.data_store import seed
from models.models import CustomerCreate, CustomerUpdate
import services.customer_service as customer_service


@pytest.fixture(autouse=True)
def reset_store():
    store.customers.clear()
    store.accounts.clear()
    store._customer_id_counter = 0
    store._account_id_counter = 0
    seed()


class TestGetAllCustomers:
    def test_getAllCustomers_success(self):
        result = customer_service.get_all_customers()
        assert len(result) == 4

    def test_getAllCustomers_fail_returns_empty_after_clear(self):
        store.customers.clear()
        result = customer_service.get_all_customers()
        assert result == []


class TestGetCustomerById:
    def test_getCustomerById_success(self):
        result = customer_service.get_customer_by_id(1)
        assert result is not None
        assert result.name == "John Smith"

    def test_getCustomerById_fail_notFound(self):
        result = customer_service.get_customer_by_id(999)
        assert result is None


class TestGetCustomerByName:
    def test_getCustomerByName_success(self):
        result = customer_service.get_customer_by_name("Jane")
        assert len(result) >= 1
        assert any("Jane" in c.name for c in result)

    def test_getCustomerByName_fail_noMatch(self):
        result = customer_service.get_customer_by_name("ZZZNoMatch")
        assert result == []


class TestGetPremiumCustomers:
    def test_getPremiumCustomers_success(self):
        # Jane ($12k), Alice ($11.7k), Bob ($15k) — all > $10,000
        result = customer_service.get_premium_customers()
        assert len(result) == 3

    def test_getPremiumCustomers_fail_nonPremiumExcluded(self):
        # John Smith ($1,500 total) should NOT appear
        result = customer_service.get_premium_customers()
        names = [c.name for c in result]
        assert "John Smith" not in names


class TestCreateCustomer:
    def test_createCustomer_success(self):
        payload = CustomerCreate(name="Carol White", email="carol@bank.com")
        result = customer_service.create_customer(payload)
        assert result is not None
        assert result.name == "Carol White"

    def test_createCustomer_fail_notInStoreBeforeCall(self):
        before = len(store.customers)
        payload = CustomerCreate(name="New Person", email="new@bank.com")
        customer_service.create_customer(payload)
        assert len(store.customers) == before + 1


class TestUpdateCustomer:
    def test_updateCustomer_success(self):
        payload = CustomerUpdate(name="John A. Smith", email="john.a@bank.com")
        result = customer_service.update_customer(1, payload)
        assert result is not None
        assert result.name == "John A. Smith"

    def test_updateCustomer_fail_notFound(self):
        payload = CustomerUpdate(name="Ghost")
        result = customer_service.update_customer(999, payload)
        assert result is None


class TestDeleteCustomer:
    def test_deleteCustomer_success(self):
        result = customer_service.delete_customer(1)
        assert result is True
        assert customer_service.get_customer_by_id(1) is None

    def test_deleteCustomer_fail_notFound(self):
        result = customer_service.delete_customer(999)
        assert result is False
