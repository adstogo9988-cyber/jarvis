"""File Operations - Create, delete, manage files and folders"""
import os
import shutil
import pandas as pd
import logging
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class FileOperations:
    """Handle file and folder operations"""
    
    @staticmethod
    def create_folder(path: str) -> bool:
        """Create a folder"""
        try:
            os.makedirs(path, exist_ok=True)
            logger.info(f"✓ Created folder: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating folder: {e}")
            return False
    
    @staticmethod
    def delete_folder(path: str, confirm: bool = True) -> bool:
        """Delete a folder"""
        try:
            if confirm and os.path.exists(path):
                shutil.rmtree(path)
                logger.info(f"✓ Deleted folder: {path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting folder: {e}")
            return False
    
    @staticmethod
    def create_file(path: str, content: str = "") -> bool:
        """Create a file with content"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✓ Created file: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return False
    
    @staticmethod
    def delete_file(path: str, confirm: bool = True) -> bool:
        """Delete a file"""
        try:
            if confirm and os.path.exists(path):
                os.remove(path)
                logger.info(f"✓ Deleted file: {path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    @staticmethod
    def list_files(path: str) -> List[Dict]:
        """List files in a folder"""
        try:
            if not os.path.exists(path):
                return []
            
            files = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                files.append({
                    'name': item,
                    'is_dir': os.path.isdir(item_path),
                    'size': os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            logger.info(f"Listed {len(files)} items in {path}")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []
    
    @staticmethod
    def open_file(path: str) -> bool:
        """Open a file with default application"""
        try:
            import subprocess
            if os.name == 'nt':
                os.startfile(path)
            elif os.name == 'posix':
                subprocess.Popen(['open', path])
            logger.info(f"✓ Opened file: {path}")
            return True
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            return False
    
    @staticmethod
    def move_file(source: str, destination: str) -> bool:
        """Move or rename a file"""
        try:
            shutil.move(source, destination)
            logger.info(f"✓ Moved {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            return False
    
    @staticmethod
    def create_csv(path: str, data: Dict) -> bool:
        """Create a CSV file"""
        try:
            df = pd.DataFrame(data)
            df.to_csv(path, index=False)
            logger.info(f"✓ Created CSV: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating CSV: {e}")
            return False
    
    @staticmethod
    def create_excel(path: str, data: Dict) -> bool:
        """Create an Excel file"""
        try:
            df = pd.DataFrame(data)
            df.to_excel(path, index=False)
            logger.info(f"✓ Created Excel: {path}")
            return True
        except Exception as e:
            logger.error(f"Error creating Excel: {e}")
            return False
    
    @staticmethod
    def read_file(path: str) -> Optional[str]:
        """Read file content"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"✓ Read file: {path}")
            return content
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return None
    
    @staticmethod
    def get_desktop_path() -> str:
        """Get Desktop folder path"""
        return str(Path.home() / "Desktop")
    
    @staticmethod
    def get_documents_path() -> str:
        """Get Documents folder path"""
        return str(Path.home() / "Documents")
