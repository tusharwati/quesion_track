from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import structlog
import time
from app.core.config import settings
from app.core.logging import setup_logging
from app.database.base import Base, engine
from app.api import health, transcription, settings as settings_api


# Setup logging
setup_logging()
logger = structlog.get_logger()


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(
    title="QuestionTrack API",
    description="Speech-to-text question tracking application API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error", errors=exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers
app.include_router(health.router)
app.include_router(transcription.router)
app.include_router(settings_api.router)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info(
        "Starting QuestionTrack API",
        version="1.0.0",
        environment=settings.api_host
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down QuestionTrack API")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "QuestionTrack API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }
