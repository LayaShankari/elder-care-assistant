from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database.db import engine
from app.database.base import Base
from app.api.routes import (
    auth, health, reminders, chat, family, emergency
)
from app.middleware.error_handler import ErrorHandlerMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Elder Care Assistant API...")
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    logger.info("Shutting down Elder Care Assistant API...")

app = FastAPI(
    title="Elder Care Assistant API",
    description="AI-powered health monitoring and companion system for elderly care",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

trusted_hosts = settings.TRUSTED_HOSTS
if not trusted_hosts or trusted_hosts == [""]:
    trusted_hosts = ["*"]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)
app.add_middleware(ErrorHandlerMiddleware)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(reminders.router, prefix="/api/v1/reminders", tags=["reminders"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(family.router, prefix="/api/v1/family", tags=["family"])
app.include_router(emergency.router, prefix="/api/v1/emergency", tags=["emergency"])

@app.get("/health", tags=["status"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/", tags=["root"])
async def root():
    """API Root"""
    return {
        "name": "Elder Care Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
