from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc
import structlog
from app.models.question import Question


logger = structlog.get_logger()


class QuestionService:
    """
    Service for managing question history in the database.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_question(
        self,
        raw_text: str,
        corrected_text: str,
        is_question: bool,
        confidence: float,
        processing_time: float
    ) -> Question:
        """Create a new question record."""
        question = Question(
            raw_text=raw_text,
            corrected_text=corrected_text,
            is_question=is_question,
            confidence=confidence,
            processing_time=processing_time
        )
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        
        logger.info(
            "Created question",
            question_id=question.id,
            is_question=is_question,
            confidence=confidence
        )
        
        return question
    
    def get_question(self, question_id: int) -> Optional[Question]:
        """Get a question by ID."""
        return self.db.query(Question).filter(Question.id == question_id).first()
    
    def get_questions(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> tuple[List[Question], int]:
        """
        Get questions with optional search.
        
        Returns tuple of (questions, total_count)
        """
        query = self.db.query(Question)
        
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                (Question.raw_text.ilike(search_term)) |
                (Question.corrected_text.ilike(search_term))
            )
        
        total = query.count()
        questions = query.order_by(desc(Question.created_at)).offset(skip).limit(limit).all()
        
        return questions, total
    
    def get_recent_questions(self, count: int = 2) -> List[Question]:
        """Get the most recent questions."""
        return self.db.query(Question).filter(
            Question.is_question == True
        ).order_by(desc(Question.created_at)).limit(count).all()
    
    def delete_question(self, question_id: int) -> bool:
        """Delete a question by ID."""
        question = self.get_question(question_id)
        if question:
            self.db.delete(question)
            self.db.commit()
            logger.info("Deleted question", question_id=question_id)
            return True
        return False
    
    def clear_all_questions(self) -> int:
        """Delete all questions."""
        count = self.db.query(Question).delete()
        self.db.commit()
        logger.info("Cleared all questions", count=count)
        return count
