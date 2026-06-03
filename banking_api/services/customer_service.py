from sqlalchemy.orm import Session
from repository.db_models import Customer, Account
from models.models import CustomerCreate, CustomerUpdate, CustomerResponse, AccountResponse


PREMIUM_THRESHOLD = 10_000


def _to_response(customer: Customer) -> CustomerResponse:
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        accounts=[
            AccountResponse(
                id=a.id,
                account_number=a.account_number,
                account_type=a.account_type,
                balance=float(a.balance),
                customer_id=a.customer_id
            )
            for a in customer.accounts
        ]
    )


def get_all_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_name(db: Session, name: str):
    return db.query(Customer).filter(Customer.name.contains(name)).all()


def get_premium_customers(db: Session):
    customers = db.query(Customer).all()

    result = []
    for c in customers:
        total = sum(a.balance for a in c.accounts)
        if total > PREMIUM_THRESHOLD:
            result.append(c)

    return result


def create_customer(db: Session, payload: CustomerCreate):
    customer = Customer(name=payload.name, email=payload.email)

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def update_customer(db: Session, customer_id: int, payload: CustomerUpdate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        return None

    if payload.name:
        customer.name = payload.name
    if payload.email:
        customer.email = payload.email

    db.commit()
    db.refresh(customer)

    return customer


def delete_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        return False

    db.delete(customer)
    db.commit()

    return True