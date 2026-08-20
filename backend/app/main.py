from fastapi import FastAPI

from app.api.routers.products import router as products_router
from app.services.database import check_database_connection
from app.api.routers.auth import router as auth_router

app = FastAPI(
    title="Agri-Chain Supply Transparency API",
    description="Backend API for agricultural supply chain transparency",
    version="1.0.0",
)


app.include_router(products_router)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Agri-Chain Backend API is running"
    }


@app.get("/health")
def health():
    database_status = check_database_connection()

    return {
        "success": True,
        "status": "healthy",
        "database": "connected" if database_status else "disconnected"
    }
app.include_router(products_router)
app.include_router(auth_router)