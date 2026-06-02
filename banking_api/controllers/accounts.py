from fastapi import APIRouter, HTTPException, Query
from models.models import AccountCreate, AccountUpdate, AccountResponse
import services.account_service as account_service

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("", response_model=list[AccountResponse])
def get_all_accounts():
    return account_service.get_all_accounts()


@router.get("/search", response_model=list[AccountResponse])
def get_account_by_name(name: str = Query(...)):
    return account_service.get_account_by_name(name)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(account_id: int):
    result = account_service.get_account_by_id(account_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")
    return result


@router.post("", response_model=AccountResponse, status_code=201)
def create_account(payload: AccountCreate):
    result = account_service.create_account(payload)
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer {payload.customer_id} not found.")
    return result


@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, payload: AccountUpdate):
    result = account_service.update_account(account_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")
    return result


@router.delete("/{account_id}", status_code=200)
def delete_account(account_id: int):
    success = account_service.delete_account(account_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")
    return {"message": f"Account {account_id} deleted."}