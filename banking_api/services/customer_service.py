from models.models import CustomerCreate, CustomerUpdate, CustomerResponse, AccountResponse
import repository.data_store as store

PREMIUM_THRESHOLD = 10_000.00


def _build_response(customer: dict) -> CustomerResponse:
    accts = [
        AccountResponse(**a)
        for a in store.accounts
        if a["customer_id"] == customer["id"]
    ]
    return CustomerResponse(**customer, accounts=accts)


def get_all_customers() -> list[CustomerResponse]:
    return [_build_response(c) for c in store.customers]


def get_customer_by_id(customer_id: int) -> CustomerResponse | None:
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        return None
    return _build_response(customer)


def get_customer_by_name(name: str) -> list[CustomerResponse]:
    matches = [c for c in store.customers if name.lower() in c["name"].lower()]
    return [_build_response(c) for c in matches]


def get_premium_customers() -> list[CustomerResponse]:
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


def create_customer(payload: CustomerCreate) -> CustomerResponse:
    new_customer = {
        "id": store.next_customer_id(),
        "name": payload.name,
        "email": payload.email,
    }
    store.customers.append(new_customer)
    return _build_response(new_customer)


def update_customer(customer_id: int, payload: CustomerUpdate) -> CustomerResponse | None:
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        return None
    if payload.name is not None:
        customer["name"] = payload.name
    if payload.email is not None:
        customer["email"] = payload.email
    return _build_response(customer)


def delete_customer(customer_id: int) -> bool:
    customer = next((c for c in store.customers if c["id"] == customer_id), None)
    if not customer:
        return False
    store.accounts[:] = [a for a in store.accounts if a["customer_id"] != customer_id]
    store.customers.remove(customer)
    return True
