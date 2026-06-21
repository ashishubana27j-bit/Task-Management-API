from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine, Base
from app.api.routes import auth, users, tasks, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables (safe to call multiple times)
    Base.metadata.create_all(bind=engine)
    
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])


@app.get("/")
def root():
    return {"message": "Task Management API", "version": settings.VERSION}


@app.get("/health")
def health_check():
    return {"status": "healthy"}