"""Ollama Client - Connect to local Ollama server"""
import requests
import json
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class OllamaClient:
    """Manages connection to local Ollama server"""
    
    def __init__(self, server_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.server_url = server_url
        self.model = model
        self.is_connected = False
        self.check_connection()
    
    def check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.server_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self.is_connected = True
                logger.info("✓ Connected to Ollama server")
                return True
        except Exception as e:
            logger.error(f"✗ Cannot connect to Ollama: {e}")
            self.is_connected = False
            return False
        return False
    
    def list_models(self) -> list:
        """Get list of available models"""
        if not self.is_connected:
            return []
        try:
            response = requests.get(f"{self.server_url}/api/tags", timeout=5)
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            logger.info(f"Available models: {models}")
            return models
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Download a model (requires Ollama CLI)"""
        logger.info(f"Pulling model: {model_name}")
        try:
            import subprocess
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=3600
            )
            if result.returncode == 0:
                logger.info(f"✓ Model {model_name} pulled successfully")
                self.model = model_name
                return True
            else:
                logger.error(f"Error pulling model: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Exception while pulling model: {e}")
            return False
    
    def chat(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        """Send a prompt to the model and get response"""
        if not self.is_connected:
            return "Error: Ollama server not connected"
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }
            
            response = requests.post(
                f"{self.server_url}/api/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                logger.error(f"API error: {response.status_code}")
                return "Error: Could not get response from Ollama"
        
        except requests.exceptions.Timeout:
            logger.error("Timeout waiting for Ollama response")
            return "Error: Request timed out"
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"
    
    def generate_with_system(self, system_prompt: str, user_message: str, 
                            temperature: float = 0.7, max_tokens: int = 512) -> str:
        """Generate response with system prompt"""
        full_prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
        return self.chat(full_prompt, temperature, max_tokens)
