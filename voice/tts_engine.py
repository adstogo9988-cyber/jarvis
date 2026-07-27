"""TTS Engine - Local Text-to-Speech"""
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Text-to-speech using Coqui TTS or pyttsx3 fallback"""
    
    def __init__(self, engine: str = "coqui", language: str = "en"):
        self.engine_name = engine
        self.language = language
        self.engine = None
        self.initialize_engine()
    
    def initialize_engine(self):
        """Initialize TTS engine"""
        if self.engine_name == "coqui":
            self._initialize_coqui()
        else:
            self._initialize_pyttsx3()
    
    def _initialize_coqui(self):
        """Initialize Coqui TTS"""
        try:
            from TTS.api import TTS
            logger.info("Loading Coqui TTS...")
            
            try:
                self.engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=True)
                logger.info("✓ Coqui TTS loaded on GPU")
            except:
                self.engine = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=False)
                logger.info("✓ Coqui TTS loaded on CPU")
        
        except Exception as e:
            logger.warning(f"Coqui TTS failed: {e}. Falling back to pyttsx3")
            self._initialize_pyttsx3()
    
    def _initialize_pyttsx3(self):
        """Initialize pyttsx3 as fallback"""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1.0)
            logger.info("✓ pyttsx3 initialized")
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """Speak text"""
        if not text:
            return False
        
        try:
            if self.engine is None:
                logger.error("TTS engine not initialized")
                return False
            
            if hasattr(self.engine, 'tts_to_file'):
                temp_file = "temp_jarvis_speech.wav"
                self.engine.tts_to_file(text=text, file_path=temp_file)
                self._play_audio_file(temp_file)
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return True
            else:
                self.engine.say(text)
                if blocking:
                    self.engine.runAndWait()
                return True
        
        except Exception as e:
            logger.error(f"Error in speak: {e}")
            return False
    
    def _play_audio_file(self, filepath: str):
        """Play audio file"""
        try:
            import sounddevice as sd
            from scipy.io import wavfile
            
            sample_rate, data = wavfile.read(filepath)
            sd.play(data, sample_rate)
            sd.wait()
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
    
    def speak_async(self, text: str):
        """Speak asynchronously"""
        try:
            if hasattr(self.engine, 'runAndWait'):
                self.engine.say(text)
            else:
                self.speak(text, blocking=False)
        except Exception as e:
            logger.error(f"Error in speak_async: {e}")
