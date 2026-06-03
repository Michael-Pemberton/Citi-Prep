import pytest

from models.models import CustomerCreate, CustomerUpdate
import services.customer_service as customer_service


class TestCustomers:

    def test_create_customer(self, db):
        payload = CustomerCreate(
            name="John Smith",
            email="john@test.com"
        )

        result = customer_service.create_customer(db, payload)

        assert result.name == "John Smith"
        assert result.email == "john@test.com"


    def test_get_all_customers(self, db):
        customer_service.create_customer(
            db,
            CustomerCreate(name="A", email="a@test.com")
        )

        result = customer_service.get_all_customers(db)

        assert len(result) == 1


    def test_get_customer_by_id(self, db):
        created = customer_service.create_customer(
            db,
            CustomerCreate(name="Bob", email="bob@test.com")
        )

        result = customer_service.get_customer_by_id(db, created.id)

        assert result.id == created.id


    def test_update_customer(self, db):
        created = customer_service.create_customer(
            db,
            CustomerCreate(name="Old", email="old@test.com")
        )

        updated = customer_service.update_customer(
            db,
            created.id,
            CustomerUpdate(name="New Name")
        )

        assert updated.name == "New Name"


    def test_delete_customer(self, db):
        created = customer_service.create_customer(
            db,
            CustomerCreate(name="Delete", email="del@test.com")
        )

        success = customer_service.delete_customer(db, created.id)

        assert success is True