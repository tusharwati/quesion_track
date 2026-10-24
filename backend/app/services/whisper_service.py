import time
import numpy as np
from typing import Optional, Tuple
import structlog
from faster_whisper import WhisperModel
from app.core.config import settings


logger = structlog.get_logger()


class WhisperService:
    _instance: Optional['WhisperService'] = None
    _model: Optional[WhisperModel] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._model is None:
            self._load_model()
    
    def _load_model(self):
        """Load Whisper model once and cache it."""
        try:
            logger.info(
                "Loading Whisper model",
                model=settings.stt_model,
                device=settings.stt_device,
                compute_type=settings.stt_compute_type
            )
            self._model = WhisperModel(
                settings.stt_model,
                device=settings.stt_device,
                compute_type=settings.stt_compute_type
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error("Failed to load Whisper model", error=str(e))
            raise
    
    @property
    def is_loaded(self) -> bool:
        return self._model is not None
    
    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000,
        language: str = "en"
    ) -> Tuple[str, float, float]:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Numpy array of audio samples
            sample_rate: Audio sample rate
            language: Language code (default: "en")
            
        Returns:
            Tuple of (transcription, confidence, processing_time)
        """
        if not self.is_loaded:
            raise RuntimeError("Whisper model not loaded")
        
        start_time = time.time()
        
        try:
            segments, info = self._model.transcribe(
                audio_data,
                language=language,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            transcription = " ".join([segment.text for segment in segments])
            confidence = np.mean([segment.avg_logprob for segment in segments]) if segments else 0.0
            confidence = np.exp(confidence)  # Convert log probability to probability
            
            processing_time = time.time() - start_time
            
            logger.info(
                "Transcription completed",
                duration=processing_time,
                language=info.language,
                language_probability=info.language_probability
            )
            
            return transcription.strip(), float(confidence), processing_time
            
        except Exception as e:
            logger.error("Transcription failed", error=str(e))
            raise
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "model": settings.stt_model,
            "device": settings.stt_device,
            "compute_type": settings.stt_compute_type,
            "loaded": self.is_loaded
        }
