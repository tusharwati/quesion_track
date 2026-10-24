from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import structlog
from app.database.base import get_db
from app.services.transcription_service import transcription_service
from app.services.audio_service import AudioService
from app.services.question_service import QuestionService
from app.schemas.transcription import TranscriptionResponse, QuestionResponse, QuestionListResponse, QuestionDeleteResponse
import time


logger = structlog.get_logger()
router = APIRouter(prefix="/api", tags=["transcription"])


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file to transcribe"),
    db: Session = Depends(get_db)
):
    """
    Transcribe audio file and extract questions.
    
    Accepts audio files (WAV, MP3, FLAC, etc.) and returns transcription
    with technical term correction and question detection.
    """
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        allowed_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.webm', '.mp4'}
        file_ext = '.' + file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Process audio
        audio_service = AudioService()
        audio_data, sample_rate = audio_service.process_uploaded_file(file_content, file.filename)
        
        # Check for empty audio
        duration = audio_service.get_audio_duration(audio_data, sample_rate)
        if duration < 0.1:
            raise HTTPException(status_code=400, detail="Audio file is too short or empty")
        
        logger.info("Processing audio file", filename=file.filename, duration=duration)
        
        # Transcribe
        raw_text, corrected_text, is_question, confidence, processing_time = transcription_service.process_audio(
            audio_data,
            sample_rate=sample_rate
        )
        
        # Save to database if it's a question
        if is_question and raw_text:
            question_service = QuestionService(db)
            question = question_service.create_question(
                raw_text=raw_text,
                corrected_text=corrected_text,
                is_question=is_question,
                confidence=confidence,
                processing_time=processing_time
            )
            logger.info("Saved question to database", question_id=question.id)
        
        return TranscriptionResponse(
            raw_text=raw_text,
            corrected_text=corrected_text,
            is_question=is_question,
            confidence=confidence,
            processing_time=processing_time
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        logger.error("Transcription validation error", error=str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Transcription failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/questions", response_model=QuestionResponse)
async def create_question(
    raw_text: str,
    corrected_text: str,
    is_question: bool = True,
    confidence: float = 0.9,
    processing_time: float = 0.0,
    db: Session = Depends(get_db)
):
    """
    Manually create a question entry.
    """
    question_service = QuestionService(db)
    question = question_service.create_question(
        raw_text=raw_text,
        corrected_text=corrected_text,
        is_question=is_question,
        confidence=confidence,
        processing_time=processing_time
    )
    
    return question


@router.get("/questions", response_model=QuestionListResponse)
async def list_questions(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    """
    List all questions with optional search.
    """
    question_service = QuestionService(db)
    questions, total = question_service.get_questions(skip=skip, limit=limit, search=search)
    
    return QuestionListResponse(
        questions=[QuestionResponse.from_orm(q) for q in questions],
        total=total
    )


@router.get("/questions/recent", response_model=list[QuestionResponse])
async def get_recent_questions(
    count: int = 2,
    db: Session = Depends(get_db)
):
    """
    Get recent questions (latest N questions).
    """
    question_service = QuestionService(db)
    questions = question_service.get_recent_questions(count=count)
    
    return [QuestionResponse.from_orm(q) for q in questions]


@router.delete("/questions/{question_id}", response_model=QuestionDeleteResponse)
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific question by ID.
    """
    question_service = QuestionService(db)
    deleted = question_service.delete_question(question_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return QuestionDeleteResponse(message="Question deleted successfully", id=question_id)


@router.delete("/questions", response_model=QuestionDeleteResponse)
async def clear_all_questions(db: Session = Depends(get_db)):
    """
    Delete all questions from history.
    """
    question_service = QuestionService(db)
    count = question_service.clear_all_questions()
    
    return QuestionDeleteResponse(message=f"Cleared {count} questions")
