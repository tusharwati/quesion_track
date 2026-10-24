from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
import structlog
from app.database.base import get_db
from app.models.setting import Setting
from app.schemas.settings import SettingsResponse, SettingsUpdateRequest


logger = structlog.get_logger()
router = APIRouter(prefix="/api", tags=["settings"])


DEFAULT_SETTINGS = {
    "stt_model": "base",
    "language": "en",
    "recent_question_count": "2",
    "auto_correction": "true",
    "question_detection": "true",
    "theme": "light"
}


@router.get("/settings", response_model=SettingsResponse)
async def get_settings(db: Session = Depends(get_db)):
    """
    Get current application settings.
    """
    settings_dict = {}
    
    for key, default_value in DEFAULT_SETTINGS.items():
        setting = db.query(Setting).filter(Setting.key == key).first()
        if setting:
            settings_dict[key] = setting.value
        else:
            settings_dict[key] = default_value
    
    # Convert string values to proper types
    return SettingsResponse(
        stt_model=settings_dict.get("stt_model", "base"),
        language=settings_dict.get("language", "en"),
        recent_question_count=int(settings_dict.get("recent_question_count", "2")),
        auto_correction=settings_dict.get("auto_correction", "true").lower() == "true",
        question_detection=settings_dict.get("question_detection", "true").lower() == "true",
        theme=settings_dict.get("theme", "light")
    )


@router.put("/settings", response_model=SettingsResponse)
async def update_settings(
    settings_update: SettingsUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update application settings.
    """
    update_data = settings_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        # Convert value to string for storage
        str_value = str(value) if not isinstance(value, str) else value
        
        # Check if setting exists
        setting = db.query(Setting).filter(Setting.key == key).first()
        
        if setting:
            setting.value = str_value
        else:
            # Create new setting
            setting = Setting(key=key, value=str_value)
            db.add(setting)
    
    db.commit()
    
    logger.info("Updated settings", updates=update_data)
    
    # Return updated settings
    return await get_settings(db)
