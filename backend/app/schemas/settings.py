from pydantic import BaseModel, Field
from typing import Literal


class SettingsResponse(BaseModel):
    stt_model: Literal["tiny", "base", "small"] = "base"
    language: str = "en"
    recent_question_count: Literal[1, 2, 3, 5] = 2
    auto_correction: bool = True
    question_detection: bool = True
    theme: Literal["light", "dark", "system"] = "light"


class SettingsUpdateRequest(BaseModel):
    stt_model: Literal["tiny", "base", "small"] | None = None
    language: str | None = None
    recent_question_count: Literal[1, 2, 3, 5] | None = None
    auto_correction: bool | None = None
    question_detection: bool | None = None
    theme: Literal["light", "dark", "system"] | None = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "stt_model": "base",
                "language": "en",
                "recent_question_count": 2,
                "auto_correction": True,
                "question_detection": True,
                "theme": "light"
            }
        }
