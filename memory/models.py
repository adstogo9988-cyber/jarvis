"""Data Models for Jarvis Memory"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MemoryFact:
    """Store facts about the user"""
    fact: str
    category: str = "general"
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class Task:
    """Store tasks and reminders"""
    title: str
    description: str = ""
    due_date: Optional[str] = None
    completed: bool = False
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class Note:
    """Store notes"""
    title: str
    content: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class ChatMessage:
    """Store chat history"""
    role: str  # 'user' or 'jarvis'
    message: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
