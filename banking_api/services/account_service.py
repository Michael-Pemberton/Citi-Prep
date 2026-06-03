from sqlalchemy.orm import Session
from repository.db_models import Account, Customer
from models.models import AccountCreate, AccountUpdate


def get_all_accounts(db: Session):
    return db.query(Account).all()


def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()


def get_account_by_name(db: Session, name: str):
    return (
        db.query(Account)
        .join(Customer)
        .filter(Customer.name.contains(name))
        .all()
    )


def create_account(db: Session, payload: AccountCreate):
    customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()

    if not customer:
        return None

    account = Account(
        account_number=payload.account_number,
        account_type=payload.account_type,
        balance=payload.balance,
        customer_id=payload.customer_id
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account


def update_account(db: Session, account_id: int, payload: AccountUpdate):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        return None

    if payload.account_number:
        account.account_number = payload.account_number
    if payload.account_type:
        account.account_type = payload.account_type
    if payload.balance is not None:
        account.balance = payload.balance

    db.commit()
    db.refresh(account)

    return account


def delete_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        return False

    db.delete(account)
    db.commit()

    return True