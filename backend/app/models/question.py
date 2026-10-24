from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(String, nullable=False)
    corrected_text = Column(String, nullable=False)
    is_question = Column(Boolean, default=True)
    confidence = Column(Float, default=0.0)
    processing_time = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "raw_text": self.raw_text,
            "corrected_text": self.corrected_text,
            "is_question": self.is_question,
            "confidence": self.confidence,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
