"""Wake Word Detector - Always listening for 'Hello Jarvis'"""
import logging
from typing import Callable, Optional
import threading

logger = logging.getLogger(__name__)

class WakeWordDetector:
    """Detects wake word to activate Jarvis"""
    
    def __init__(self, wake_word: str = "Hello Jarvis", sensitivity: float = 0.5):
        self.wake_word = wake_word.lower()
        self.sensitivity = sensitivity
        self.is_listening = False
        self.on_wake_word = None
        self.listen_thread = None
    
    def set_wake_callback(self, callback: Callable):
        """Set callback function when wake word is detected"""
        self.on_wake_word = callback
    
    def start_listening(self):
        """Start listening for wake word in background thread"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        logger.info(f"Started listening for wake word: {self.wake_word}")
    
    def stop_listening(self):
        """Stop listening for wake word"""
        self.is_listening = False
        logger.info("Stopped listening for wake word")
    
    def _listen_loop(self):
        """Background listening loop"""
        from voice.whisper_stt import WhisperSTT
        
        stt = WhisperSTT(model_size="tiny")
        
        while self.is_listening:
            try:
                text = stt.listen_and_transcribe(duration=3.0)
                
                if text:
                    if self.wake_word in text.lower():
                        logger.info(f"✓ Wake word detected!")
                        if self.on_wake_word:
                            self.on_wake_word(text)
            
            except Exception as e:
                logger.error(f"Error in wake word detection: {e}")
    
    def is_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        return self.wake_word in text.lower()
