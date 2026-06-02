from fastapi import APIRouter, HTTPException, Query
from models.models import CustomerCreate, CustomerUpdate, CustomerResponse
import services.customer_service as customer_service

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerResponse])
def get_all_customers():
    return customer_service.get_all_customers()


@router.get("/premium", response_model=list[CustomerResponse])
def get_all_premium_customers():
    return customer_service.get_premium_customers()


@router.get("/search", response_model=list[CustomerResponse])
def get_customer_by_name(name: str = Query(...)):
    return customer_service.get_customer_by_name(name)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id: int):
    result = customer_service.get_customer_by_id(customer_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return result


@router.post("", response_model=CustomerResponse, status_code=201)
def create_customer(payload: CustomerCreate):
    return customer_service.create_customer(payload)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate):
    result = customer_service.update_customer(customer_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return result


@router.delete("/{customer_id}", status_code=200)
def delete_customer(customer_id: int):
    success = customer_service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return {"message": f"Customer {customer_id} and all associated accounts deleted."}