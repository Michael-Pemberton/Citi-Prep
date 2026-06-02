from models.models import AccountCreate, AccountUpdate, AccountResponse
import repository.data_store as store


def get_all_accounts() -> list[AccountResponse]:
    return [AccountResponse(**a) for a in store.accounts]


def get_account_by_id(account_id: int) -> AccountResponse | None:
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        return None
    return AccountResponse(**account)


def get_account_by_name(name: str) -> list[AccountResponse]:
    matched_ids = {
        c["id"]
        for c in store.customers
        if name.lower() in c["name"].lower()
    }
    results = [a for a in store.accounts if a["customer_id"] in matched_ids]
    return [AccountResponse(**a) for a in results]


def create_account(payload: AccountCreate) -> AccountResponse | None:
    customer = next((c for c in store.customers if c["id"] == payload.customer_id), None)
    if not customer:
        return None
    new_account = {
        "id": store.next_account_id(),
        "account_number": payload.account_number,
        "account_type": payload.account_type,
        "balance": payload.balance,
        "customer_id": payload.customer_id,
    }
    store.accounts.append(new_account)
    return AccountResponse(**new_account)


def update_account(account_id: int, payload: AccountUpdate) -> AccountResponse | None:
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        return None
    if payload.account_number is not None:
        account["account_number"] = payload.account_number
    if payload.account_type is not None:
        account["account_type"] = payload.account_type
    if payload.balance is not None:
        account["balance"] = payload.balance
    return AccountResponse(**account)


def delete_account(account_id: int) -> bool:
    account = next((a for a in store.accounts if a["id"] == account_id), None)
    if not account:
        return False
    store.accounts.remove(account)
    return True
