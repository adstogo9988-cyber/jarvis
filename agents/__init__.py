"""Sub-Agents Manager - Background task execution"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Any
import threading

logger = logging.getLogger(__name__)

class SubAgentManager:
    """Manage background tasks and sub-agents"""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks = {}
        self.lock = threading.Lock()
    
    def submit_task(self, task_id: str, function: Callable, *args, **kwargs) -> bool:
        """Submit a background task"""
        try:
            with self.lock:
                future = self.executor.submit(function, *args, **kwargs)
                self.active_tasks[task_id] = {
                    'future': future,
                    'status': 'running'
                }
            logger.info(f"✓ Task submitted: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Error submitting task: {e}")
            return False
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get status of a task"""
        with self.lock:
            if task_id not in self.active_tasks:
                return {'status': 'not_found'}
            
            task = self.active_tasks[task_id]
            future = task['future']
            
            if future.done():
                try:
                    result = future.result()
                    return {'status': 'completed', 'result': result}
                except Exception as e:
                    return {'status': 'error', 'error': str(e)}
            else:
                return {'status': 'running'}
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        try:
            with self.lock:
                if task_id in self.active_tasks:
                    self.active_tasks[task_id]['future'].cancel()
                    logger.info(f"✓ Task cancelled: {task_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error cancelling task: {e}")
            return False
    
    def get_all_tasks(self) -> Dict[str, Dict]:
        """Get all active tasks"""
        with self.lock:
            tasks = {}
            for task_id, task in self.active_tasks.items():
                if task['future'].done():
                    tasks[task_id] = {'status': 'completed'}
                else:
                    tasks[task_id] = {'status': 'running'}
            return tasks
    
    def shutdown(self):
        """Shutdown the executor"""
        self.executor.shutdown(wait=True)
        logger.info("✓ Sub-agent manager shutdown")
