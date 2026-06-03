from models.models import AccountCreate, AccountUpdate, AccountType
import services.account_service as account_service
import services.customer_service as customer_service
from models.models import CustomerCreate


class TestAccounts:

    def test_create_account(self, db):
        customer = customer_service.create_customer(
            db,
            CustomerCreate(name="John", email="john@test.com")
        )

        payload = AccountCreate(
            account_number="S1001",
            account_type=AccountType.savings,
            balance=500.0,
            customer_id=customer.id
        )

        result = account_service.create_account(db, payload)

        assert result.account_number == "S1001"


    def test_get_account_by_id(self, db):
        customer = customer_service.create_customer(
            db,
            CustomerCreate(name="John", email="john@test.com")
        )

        account = account_service.create_account(
            db,
            AccountCreate(
                account_number="C1001",
                account_type=AccountType.checking,
                balance=200,
                customer_id=customer.id
            )
        )

        result = account_service.get_account_by_id(db, account.id)

        assert result.id == account.id


    def test_update_account(self, db):
        customer = customer_service.create_customer(
            db,
            CustomerCreate(name="John", email="john@test.com")
        )

        account = account_service.create_account(
            db,
            AccountCreate(
                account_number="U1001",
                account_type=AccountType.savings,
                balance=100,
                customer_id=customer.id
            )
        )

        updated = account_service.update_account(
            db,
            account.id,
            AccountUpdate(balance=999)
        )

        assert updated.balance == 999


    def test_delete_account(self, db):
        customer = customer_service.create_customer(
            db,
            CustomerCreate(name="John", email="john@test.com")
        )

        account = account_service.create_account(
            db,
            AccountCreate(
                account_number="D1001",
                account_type=AccountType.savings,
                balance=100,
                customer_id=customer.id
            )
        )

        success = account_service.delete_account(db, account.id)

        assert success is True