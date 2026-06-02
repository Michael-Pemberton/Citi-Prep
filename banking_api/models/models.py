from pydantic import BaseModel
from typing import Optional, List
from enum import Enum


class AccountType(str, Enum):
    savings = "Savings"
    checking = "Checking"


# --- Request / Response Models ---

class AccountCreate(BaseModel):
    account_number: str
    account_type: AccountType
    balance: float
    customer_id: int


class AccountUpdate(BaseModel):
    account_number: Optional[str] = None
    account_type: Optional[AccountType] = None
    balance: Optional[float] = None


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: AccountType
    balance: float
    customer_id: int


class CustomerCreate(BaseModel):
    name: str
    email: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    accounts: List[AccountResponse] = []
