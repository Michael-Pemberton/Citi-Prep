from fastapi import APIRouter, HTTPException, Query
from models.models import AccountCreate, AccountUpdate, AccountResponse
import repository.data_store as store

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


# GET /api/accounts
@router.get("", response_model=list[AccountResponse])
def get_all_accounts():
    return [AccountResponse(**a) for a in store.accounts]


# GET /api/accounts/search?name=...
@router.get("/search", response_model=list[AccountResponse])
def get_account_by_name(name: str = Query(..., description="Full or partial customer name")):
    matched_ids = {
        c["id"]
        for c in store.customers
        if name.lower() in c["name"].lower()
    }
    results = [a for a in store.accounts if a["customer_id"] in matched_ids]
    return [AccountResponse(**a) for a in results]


# GET /api/accounts/{id}
@router.get("/{account_id}", response_model=AccountResponse)
def get_account_by_id(account_id: int):
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")
    return AccountResponse(**account)


# POST /api/accounts
@router.post("", response_model=AccountResponse, status_code=201)
def create_account(payload: AccountCreate):
    # Verify the customer exists
    customer = next((c for c in store.customers if c["id"] == payload.customer_id), None)
    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {payload.customer_id} not found. Cannot create account."
        )

    new_account = {
        "id": store.next_account_id(),
        "account_number": payload.account_number,
        "account_type": payload.account_type,
        "balance": payload.balance,
        "customer_id": payload.customer_id,
    }
    store.accounts.append(new_account)
    return AccountResponse(**new_account)


# PUT /api/accounts/{id}
@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: int, payload: AccountUpdate):
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")

    if payload.account_number is not None:
        account["account_number"] = payload.account_number
    if payload.account_type is not None:
        account["account_type"] = payload.account_type
    if payload.balance is not None:
        account["balance"] = payload.balance

    return AccountResponse(**account)


# DELETE /api/accounts/{id}
@router.delete("/{account_id}", status_code=200)
def delete_account(account_id: int):
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found.")

    store.accounts.remove(account)
    return {"message": f"Account {account_id} deleted."}
