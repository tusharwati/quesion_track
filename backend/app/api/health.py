from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import structlog
from app.database.base import get_db
from app.services.transcription_service import transcription_service
from app.schemas.transcription import HealthResponse


logger = structlog.get_logger()
router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    Returns system status including model loading state and database connectivity.
    """
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        database_connected = True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        database_connected = False
    
    # Check model status
    model_loaded = transcription_service.is_model_loaded()
    
    return HealthResponse(
        status="healthy" if database_connected and model_loaded else "degraded",
        model_loaded=model_loaded,
        database_connected=database_connected,
        version="1.0.0"
    )


@router.get("/status")
async def get_status():
    """
    Get detailed system status.
    """
    return {
        "status": "operational",
        "services": {
            "whisper": {
                "loaded": transcription_service.is_model_loaded(),
                "model": transcription_service.whisper_service.get_model_info() if transcription_service.is_model_loaded() else None
            },
            "glossary": {
                "term_count": len(transcription_service.get_glossary_terms())
            }
        }
    }
