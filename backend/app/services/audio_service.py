import os
import tempfile
import base64
import numpy as np
import soundfile as sf
import librosa
import structlog
from typing import Tuple, Optional
from app.core.config import settings


logger = structlog.get_logger()


class AudioService:
    def __init__(self):
        self.upload_dir = settings.upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def validate_audio_file(self, file_path: str) -> bool:
        """Validate that a file is a valid audio file."""
        try:
            info = sf.info(file_path)
            return info.duration > 0
        except Exception:
            return False
    
    def process_uploaded_file(
        self,
        file_content: bytes,
        filename: str
    ) -> Tuple[np.ndarray, int]:
        """
        Process an uploaded audio file.
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        try:
            # Validate file size
            if len(file_content) > settings.max_audio_file_size:
                raise ValueError(f"File too large. Maximum size is {settings.max_audio_file_size} bytes")
            
            # Load audio file
            audio_data, sample_rate = self.load_audio_file(tmp_path)
            
            return audio_data, sample_rate
            
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def load_audio_file(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file and convert to mono 16kHz.
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            # Load with librosa (supports many formats)
            audio_data, sample_rate = librosa.load(file_path, sr=16000, mono=True)
            return audio_data, sample_rate
        except Exception as e:
            logger.error("Failed to load audio file", error=str(e), file=file_path)
            raise ValueError(f"Failed to load audio file: {str(e)}")
    
    def decode_base64_audio(self, base64_data: str) -> Tuple[np.ndarray, int]:
        """
        Decode base64 audio data.
        
        Args:
            base64_data: Base64 encoded audio data
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            # Decode base64
            audio_bytes = base64.b64decode(base64_data)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name
            
            try:
                # Load audio
                audio_data, sample_rate = self.load_audio_file(tmp_path)
                return audio_data, sample_rate
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                    
        except Exception as e:
            logger.error("Failed to decode base64 audio", error=str(e))
            raise ValueError(f"Failed to decode audio data: {str(e)}")
    
    def get_audio_duration(self, audio_data: np.ndarray, sample_rate: int) -> float:
        """Calculate audio duration in seconds."""
        return len(audio_data) / sample_rate
