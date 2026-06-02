from models.models import AccountType

# ── In-memory data store ─────────────────────

# Raw dicts are stored so we can mutate them freely without Pydantic freezing.
# Shape:  { id, account_number, account_type, balance, customer_id }
accounts: list[dict] = []

# Shape:  { id, name, email }   — accounts are looked up by customer_id
customers: list[dict] = []

_customer_id_counter: int = 0
_account_id_counter: int = 0


# ── ID generation ───────────────────────

def next_customer_id() -> int:
    global _customer_id_counter
    _customer_id_counter += 1
    return _customer_id_counter


def next_account_id() -> int:
    global _account_id_counter
    _account_id_counter += 1
    return _account_id_counter


# ── Seed data ─────────────────────────────

def seed():
    global _customer_id_counter, _account_id_counter

    seed_customers = [
        {"name": "John Smith",   "email": "john.smith@bank.com"},
        {"name": "Jane Doe",     "email": "jane.doe@bank.com"},
        {"name": "Alice Johnson","email": "alice.j@bank.com"},
        {"name": "Bob Williams", "email": "bob.w@bank.com"},
    ]

    seed_accounts_by_customer = [
        # John Smith
        [
            {"account_number": "S1001", "account_type": AccountType.savings,  "balance": 1000.00},
            {"account_number": "C1001", "account_type": AccountType.checking, "balance": 500.00},
        ],
        # Jane Doe
        [
            {"account_number": "S2001", "account_type": AccountType.savings,  "balance": 12000.00},
        ],
        # Alice Johnson
        [
            {"account_number": "S3001", "account_type": AccountType.savings,  "balance": 8500.00},
            {"account_number": "C3001", "account_type": AccountType.checking, "balance": 3200.00},
        ],
        # Bob Williams
        [
            {"account_number": "C4001", "account_type": AccountType.checking, "balance": 15000.00},
        ],
    ]

    for i, cdata in enumerate(seed_customers):
        cid = next_customer_id()
        customers.append({"id": cid, "name": cdata["name"], "email": cdata["email"]})

        for adata in seed_accounts_by_customer[i]:
            aid = next_account_id()
            accounts.append({
                "id": aid,
                "account_number": adata["account_number"],
                "account_type": adata["account_type"],
                "balance": adata["balance"],
                "customer_id": cid,
            })
