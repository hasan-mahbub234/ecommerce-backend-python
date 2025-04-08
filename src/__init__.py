from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.products.routes import product_router
from src.category.routes import category_router
from src.sub_category.routes import sub_category_router
from src.TopRated.blogs.route import blog_router
from src.TopRated.expert.route import expert_router
from src.TopRated.patner.route import patner_router
from src.TopRated.porfolio.route import portfolio_router
from src.TopRated.project.route import project_router
from src.TopRated.review.route import review_router
from src.TopRated.wedo.route import wedo_router
from contextlib import asynccontextmanager
from src.db.database import init_db
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


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

# 🔹 Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PATCH, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)



upload_folder = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
app.mount("/uploads", StaticFiles(directory=upload_folder), name="uploads")


app.include_router(product_router, prefix=f"/api/{version}/product", tags=['product'])
app.include_router(category_router, prefix=f"/api/{version}/category", tags=['category'])
app.include_router(sub_category_router, prefix=f"/api/{version}/sub_category", tags=['sub_category'])
app.include_router(blog_router, prefix=f"/api/{version}/blogs", tags=['blogs'])
app.include_router(expert_router, prefix=f"/api/{version}/experts", tags=['experts'])
app.include_router(patner_router, prefix=f"/api/{version}/patners", tags=['patners'])
app.include_router(portfolio_router, prefix=f"/api/{version}/portfolios", tags=['portfolios'])
app.include_router(project_router, prefix=f"/api/{version}/projects", tags=['projects'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(wedo_router, prefix=f"/api/{version}/wedos", tags=['wedos'])