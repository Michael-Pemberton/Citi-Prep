from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
import services.account_service as account_service

from models.models import (
    AccountCreate,
    AccountUpdate,
    AccountResponse
)

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("", response_model=list[AccountResponse])
def get_all_accounts(db: Session = Depends(get_db)):
    return account_service.get_all_accounts(db)


@router.get("/search", response_model=list[AccountResponse])
def get_account_by_name(
    name: str = Query(...),
    db: Session = Depends(get_db)
):
    return account_service.get_account_by_name(db, name)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(
    account_id: int,
    db: Session = Depends(get_db)
):
    result = account_service.get_account_by_id(db, account_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found."
        )

    return result


@router.post("", response_model=AccountResponse, status_code=201)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db)
):
    result = account_service.create_account(db, payload)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {payload.customer_id} not found."
        )

    return result


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    payload: AccountUpdate,
    db: Session = Depends(get_db)
):
    result = account_service.update_account(db, account_id, payload)

    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found."
        )

    return result


@router.delete("/{account_id}", status_code=200)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    success = account_service.delete_account(db, account_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found."
        )

    return {"message": f"Account {account_id} deleted."}