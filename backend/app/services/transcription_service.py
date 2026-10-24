from typing import Tuple
import numpy as np
import structlog
from app.services.whisper_service import WhisperService
from app.services.glossary_service import GlossaryService
from app.services.question_detector import question_detector


logger = structlog.get_logger()


class TranscriptionService:
    """
    Main transcription service that orchestrates the entire pipeline:
    Audio → Speech-to-Text → Technical Term Correction → Question Detection
    """
    
    def __init__(self):
        self.whisper_service = WhisperService()
        self.glossary_service = GlossaryService()
        self.question_detector = question_detector
    
    def process_audio(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        language: str = "en",
        auto_correct: bool = True,
        detect_questions: bool = True
    ) -> Tuple[str, str, bool, float, float]:
        """
        Process audio through the complete transcription pipeline.
        
        Args:
            audio_data: Numpy array of audio samples
            sample_rate: Audio sample rate
            language: Language code
            auto_correct: Whether to apply technical term correction
            detect_questions: Whether to detect questions
            
        Returns:
            Tuple of (raw_text, corrected_text, is_question, confidence, processing_time)
        """
        # Step 1: Speech-to-Text
        raw_text, confidence, processing_time = self.whisper_service.transcribe(
            audio_data,
            sample_rate=sample_rate,
            language=language
        )
        
        if not raw_text:
            return raw_text, raw_text, False, confidence, processing_time
        
        # Step 2: Technical Term Correction
        corrected_text = raw_text
        if auto_correct:
            corrected_text = self.glossary_service.correct_text(raw_text)
        
        # Step 3: Question Detection
        is_question = False
        if detect_questions:
            is_question, detection_confidence = self.question_detector.detect(corrected_text)
            # Adjust confidence based on question detection
            confidence = (confidence + detection_confidence) / 2
            
            # Step 4: Question Correction (if it's a question)
            if is_question:
                corrected_text = self.question_detector.correct_question(corrected_text)
        
        return raw_text, corrected_text, is_question, confidence, processing_time
    
    def is_model_loaded(self) -> bool:
        """Check if the Whisper model is loaded."""
        return self.whisper_service.is_loaded
    
    def get_glossary_terms(self):
        """Get all glossary terms."""
        return self.glossary_service.get_all_terms()
    
    def add_glossary_term(self, term: str, case_sensitive: bool = True):
        """Add a term to the glossary."""
        self.glossary_service.add_term(term, case_sensitive)
    
    def import_glossary_from_file(self, file_path: str) -> int:
        """Import glossary terms from a file."""
        return self.glossary_service.import_terms_from_file(file_path)


# Singleton instance
transcription_service = TranscriptionService()
