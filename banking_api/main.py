from fastapi import FastAPI
from controllers.customers import router as customers_router
from controllers.accounts import router as accounts_router
from database import Base, engine
from repository.db_models import Customer, Account


app = FastAPI(
    title="Banking REST API",
    description="A Banking REST API built with FastAPI.",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

# Register routers (Controllers)
app.include_router(customers_router)
app.include_router(accounts_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Banking API is running. Visit /docs for the interactive API explorer."}
