# Mock Whisper service for testing without the full Whisper model installed
import time
import numpy as np
from typing import Optional, Tuple
import structlog


logger = structlog.get_logger()


class WhisperServiceMock:
    """Mock Whisper service that returns dummy transcriptions for testing."""
    
    _instance: Optional['WhisperServiceMock'] = None
    _model: bool = True  # Mock as loaded
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        logger.info("Using MOCK Whisper service (install faster-whisper for real transcription)")
    
    @property
    def is_loaded(self) -> bool:
        return True
    
    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        language: str = "en"
    ) -> Tuple[str, float, float]:
        """
        Mock transcription - returns a sample question.
        """
        start_time = time.time()
        
        # Simulate processing time
        time.sleep(0.5)
        
        # Return mock transcription
        transcription = "how does your yolo model detect objects and what dataset did you use"
        confidence = 0.92
        processing_time = time.time() - start_time
        
        logger.info(
            "Mock transcription completed",
            duration=processing_time,
            text_length=len(transcription)
        )
        
        return transcription, confidence, processing_time
    
    def get_model_info(self) -> dict:
        """Get mock model info."""
        return {
            "model": "mock",
            "device": "cpu",
            "compute_type": "mock",
            "loaded": True,
            "note": "Install faster-whisper for real transcription"
        }
