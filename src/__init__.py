from fastapi import FastAPI
from src.products.routes import product_router
from src.category.routes import category_router
from contextlib import asynccontextmanager
from src.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server is starting...")
    init_db()  # Initialize the database
    yield
    print("Server has been stopped...")

version = "v1"

app = FastAPI(
    title="E-commerce Website",
    description="A REST API for E-commerce Website",
    version=version,
    lifespan=lifespan
)

app.include_router(product_router, prefix=f"/api/{version}/product", tags=['product'])
app.include_router(category_router, prefix=f"/api/{version}/category", tags=['category'])