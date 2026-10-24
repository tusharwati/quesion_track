from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TranscriptionRequest(BaseModel):
    audio_data: Optional[str] = Field(None, description="Base64 encoded audio data")
    file_path: Optional[str] = Field(None, description="Path to uploaded audio file")


class TranscriptionResponse(BaseModel):
    raw_text: str
    corrected_text: str
    is_question: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time: float = Field(..., description="Processing time in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "raw_text": "how does your yolo model detect object and what data set you use",
                "corrected_text": "How does your YOLO model detect objects, and what dataset did you use?",
                "is_question": True,
                "confidence": 0.94,
                "processing_time": 0.82
            }
        }


class QuestionResponse(BaseModel):
    id: int
    raw_text: str
    corrected_text: str
    is_question: bool
    confidence: float
    processing_time: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    questions: list[QuestionResponse]
    total: int


class QuestionDeleteResponse(BaseModel):
    message: str
    id: Optional[int] = None


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    database_connected: bool
    version: str
