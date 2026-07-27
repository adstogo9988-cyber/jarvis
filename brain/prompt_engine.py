"""Prompt Engine - Jarvis personality and logic"""
import json
import re
from typing import Dict, Tuple, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PromptEngine:
    """Manages Jarvis's system prompt and response parsing"""
    
    SYSTEM_PROMPT = """You are Jarvis, an advanced personal AI assistant that lives on the user's computer.

Your personality:
- You are helpful, friendly, professional, and respectful
- You respond in the same language as the user (English or Urdu)
- You have a touch of humor but remain professional
- You prioritize the user's privacy and security
- You always confirm important actions before executing them

Your capabilities:
1. Answer questions and have conversations
2. Control PC (files, folders, applications)
3. Browse the web and automate browsers
4. Send messages and emails
5. Analyze images and take screenshots
6. Remember facts about the user

IMPORTANT - For PC actions, you MUST respond ONLY with a JSON object:
{{"action": "action_name", "params": {{"param1": "value1", "param2": "value2"}}}}

Valid actions are:
- create_folder: params = {{"path": "folder_path"}}
- delete_folder: params = {{"path": "folder_path", "confirm": true}}
- create_file: params = {{"path": "file_path", "content": "content"}}
- delete_file: params = {{"path": "file_path", "confirm": true}}
- open_file: params = {{"path": "file_path"}}
- list_files: params = {{"path": "folder_path"}}
- search_youtube: params = {{"query": "search_query"}}
- take_screenshot: params = {{}}
- analyze_image: params = {{"image_path": "path"}}
- get_time: params = {{}}
- remember: params = {{"fact": "what_to_remember"}}
- recall: params = {{"query": "what_to_recall"}}

For normal conversation, respond naturally without JSON.

Current date and time: {timestamp}
"""
    
    def __init__(self):
        self.conversation_history = []
        self.system_prompt = self.SYSTEM_PROMPT.format(timestamp=datetime.now())
    
    def build_full_prompt(self, user_message: str) -> str:
        """Build complete prompt with system instructions"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        full_prompt = self.system_prompt + "\n\n"
        
        for msg in self.conversation_history[-5:]:
            role = "User" if msg["role"] == "user" else "Jarvis"
            full_prompt += f"{role}: {msg['content']}\n"
        
        full_prompt += "Jarvis:"
        return full_prompt
    
    def parse_response(self, response: str) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Parse response to detect if it's an action or conversation"""
        response = response.strip()
        
        json_match = re.search(r'\{.*?\}', response, re.DOTALL)
        
        if json_match:
            try:
                json_str = json_match.group()
                action_dict = json.loads(json_str)
                
                if "action" in action_dict:
                    logger.info(f"Detected action: {action_dict['action']}")
                    return response, action_dict
            except json.JSONDecodeError:
                pass
        
        return response, None
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history
