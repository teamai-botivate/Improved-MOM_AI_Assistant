"""FastAPI application entry point – Google Sheets backed."""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api.router import api_router
from app.api.logs import install_buffer_handler
from app.services.scheduler_service import start_scheduler, shutdown_scheduler
from app.services.google_sheets_service import init_sheets

# Configure logging at a level that shows everything
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn") # Use uvicorn's logger settings
logging.getLogger("recording_api").setLevel(logging.INFO)
logging.getLogger("ai_service").setLevel(logging.INFO)
logging.getLogger("googleapiclient.discovery_cache").setLevel(logging.ERROR)

install_buffer_handler()

settings = get_settings()

# Ensure upload directory exists before mounting StaticFiles
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup - initialise Google Sheets tabs
    init_sheets()
    start_scheduler()
    yield
    # Shutdown
    shutdown_scheduler()


app = FastAPI(
    title=settings.APP_NAME,
    version="2.0.0",
    description="AI-Powered Minutes of Meeting Management System – Google Sheets Database",
    lifespan=lifespan,
)

# Define allowed origins. FRONTEND_URL can be a single URL, a comma-separated
# list, or "*" to allow any frontend origin.
configured_origins = [
    origin.strip().rstrip("/")
    for origin in settings.FRONTEND_URL.split(",")
    if origin.strip()
]
allow_any_origin = "*" in configured_origins
origins = [
    origin for origin in configured_origins
    if origin != "*"
] + [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[] if allow_any_origin else origins,
    allow_origin_regex=".*" if allow_any_origin else None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger = logging.getLogger("meeting_creation")
    try:
        body = await request.body()
        body_str = body.decode("utf-8")
    except Exception:
        body_str = "<binary or non-utf8 data>"
    
    logger.error("Validation error: %s", exc.errors())
    logger.error("Request body: %s", body_str)
    
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": body_str},
    )

app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled exception while processing %s %s",
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
@app.head("/") # Explicitly allow HEAD requests for Render health checks
async def root():
    return {"message": f"Welcome to {settings.APP_NAME} API. Visit /docs for documentation."}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME, "database": "Google Sheets"}
