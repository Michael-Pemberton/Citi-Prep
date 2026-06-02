from fastapi import FastAPI
from controllers.customers import router as customers_router
from controllers.accounts import router as accounts_router
from repository.data_store import seed

app = FastAPI(
    title="Banking REST API",
    description="A Banking REST API built with FastAPI.",
    version="1.0.0",
)

# Seed in-memory data on startup
seed()

# Register routers (Controllers)
app.include_router(customers_router)
app.include_router(accounts_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Banking API is running. Visit /docs for the interactive API explorer."}
