from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from database import Base
from models.models import AccountType


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    accounts = relationship(
        "Account",
        back_populates="customer",
        cascade="all, delete"
    )


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(50), unique=True, nullable=False)

    account_type = Column(Enum(AccountType), nullable=False)

    balance = Column(Numeric(12, 2), nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="accounts")