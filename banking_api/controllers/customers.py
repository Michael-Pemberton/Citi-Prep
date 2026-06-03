from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
import services.customer_service as service
from models.models import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/api/customers", tags=["Customers"])


@router.get("", response_model=list[CustomerResponse])
def get_all(db: Session = Depends(get_db)):
    return service.get_all_customers(db)


@router.get("/search", response_model=list[CustomerResponse])
def search(name: str = Query(...), db: Session = Depends(get_db)):
    return service.get_customer_by_name(db, name)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_by_id(customer_id: int, db: Session = Depends(get_db)):
    result = service.get_customer_by_id(db, customer_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return result


@router.post("", response_model=CustomerResponse, status_code=201)
def create(payload: CustomerCreate, db: Session = Depends(get_db)):
    return service.create_customer(db, payload)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    result = service.update_customer(db, customer_id, payload)
    if not result:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return result


@router.delete("/{customer_id}", status_code=200)
def delete(customer_id: int, db: Session = Depends(get_db)):
    success = service.delete_customer(db, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found.")
    return {"message": f"Customer {customer_id} deleted."}
