from fastapi import APIRouter, HTTPException, Query
from models.models import CustomerCreate, CustomerUpdate, CustomerResponse, AccountResponse
import repository.data_store as store

router = APIRouter(prefix="/api/customers", tags=["Customers"])

PREMIUM_THRESHOLD = 10_000.00


def _build_response(customer: dict) -> CustomerResponse:
    """Attach the customer's accounts and return a CustomerResponse."""
    accts = [
        AccountResponse(**a)
        for a in store.accounts
        if a["customer_id"] == customer["id"]
    ]
    return CustomerResponse(**customer, accounts=accts)


# GET /api/customers
@router.get("", response_model=list[CustomerResponse])
def get_all_customers():
    return [_build_response(c) for c in store.customers]


# GET /api/customers/premium  — must be declared BEFORE /{id}
@router.get("/premium", response_model=list[CustomerResponse])
def get_all_premium_customers():
    result = []
    for customer in store.customers:
        total = sum(
            a["balance"]
            for a in store.accounts
            if a["customer_id"] == customer["id"]
        )
        if total > PREMIUM_THRESHOLD:
            result.append(_build_response(customer))
    return result


# GET /api/customers/search?name=...
@router.get("/search", response_model=list[CustomerResponse])
def get_customer_by_name(name: str = Query(..., description="Full or partial customer name")):
    matches = [
        c for c in store.customers
        if name.lower() in c["name"].lower()
    ]
    return [_build_response(c) for c in matches]


# GET /api/customers/{id}
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: int):
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return _build_response(customer)


# POST /api/customers
@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer(payload: CustomerCreate):
    new_customer = {
        "id": store.next_customer_id(),
        "name": payload.name,
        "email": payload.email,
    }
    store.customers.append(new_customer)
    return _build_response(new_customer)


# PUT /api/customers/{id}
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate):
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")

    if payload.name is not None:
        customer["name"] = payload.name
    if payload.email is not None:
        customer["email"] = payload.email

    return _build_response(customer)


# DELETE /api/customers/{id}
@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id: int):
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")

    # Cascade-delete associated accounts
    store.accounts[:] = [a for a in store.accounts if a["customer_id"] != customer_id]
    store.customers.remove(customer)

    return {"message": f"Customer {customer_id} and all associated accounts deleted."}
