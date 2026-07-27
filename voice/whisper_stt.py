"""Whisper STT - Local Speech-to-Text"""
from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import logging
from typing import Optional
import io

logger = logging.getLogger(__name__)

class WhisperSTT:
    """Local speech-to-text using Faster Whisper"""
    
    def __init__(self, model_size: str = "base", language: str = "en"):
        self.model_size = model_size
        self.language = language
        self.model = None
        self.sample_rate = 16000
        self.load_model()
    
    def load_model(self):
        """Load Whisper model"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = WhisperModel(
                self.model_size,
                device="cuda",
                compute_type="float16"
            )
            logger.info("✓ Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper: {e}")
            logger.info("Trying CPU mode...")
            try:
                self.model = WhisperModel(
                    self.model_size,
                    device="cpu",
                    compute_type="int8"
                )
                logger.info("✓ Whisper model loaded on CPU")
            except Exception as e2:
                logger.error(f"Failed to load Whisper: {e2}")
    
    def record_audio(self, duration: float = 5.0, device: Optional[int] = None) -> Optional[np.ndarray]:
        """Record audio from microphone"""
        try:
            logger.info(f"Recording for {duration} seconds...")
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                device=device,
                dtype=np.float32
            )
            sd.wait()
            logger.info("✓ Recording complete")
            return audio.flatten()
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None
    
    def transcribe_audio(self, audio_data: np.ndarray) -> str:
        """Transcribe audio array to text"""
        if self.model is None:
            return "Error: Whisper model not loaded"
        
        try:
            audio_float32 = audio_data.astype(np.float32)
            if audio_float32.max() > 1.0:
                audio_float32 = audio_float32 / 32768.0
            
            segments, info = self.model.transcribe(
                audio_float32,
                language=self.language,
                beam_size=5
            )
            
            text = "".join([segment.text for segment in segments])
            logger.info(f"Transcribed: {text}")
            return text.strip()
        
        except Exception as e:
            logger.error(f"Error transcribing: {e}")
            return ""
    
    def listen_and_transcribe(self, duration: float = 5.0) -> str:
        """Record and transcribe in one function"""
        audio = self.record_audio(duration)
        if audio is not None:
            return self.transcribe_audio(audio)
        return ""
    
    def transcribe_file(self, filepath: str) -> str:
        """Transcribe audio from file"""
        if self.model is None:
            return "Error: Whisper model not loaded"
        
        try:
            segments, info = self.model.transcribe(
                filepath,
                language=self.language
            )
            text = "".join([segment.text for segment in segments])
            logger.info(f"Transcribed from file: {text}")
            return text.strip()
        except Exception as e:
            logger.error(f"Error transcribing file: {e}")
            return ""
