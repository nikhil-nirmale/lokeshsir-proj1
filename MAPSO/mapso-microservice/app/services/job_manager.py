from typing import Dict, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class JobManager:
    def __init__(self):
        self.jobs: Dict[str, dict] = {}
        
    def create_job(self, job_id: str, request: dict, status: str, created_at: str) -> None:
        """Create a new job entry"""
        self.jobs[job_id] = {
            "request": request,
            "status": status,
            "created_at": created_at,
            "progress": 0,
            "result": None,
            "error": None
        }
        logger.info(f"Created new job {job_id}")
        
    def update_job(self, job_id: str, status: str, progress: Optional[int] = None, 
                 result: Optional[dict] = None, error: Optional[str] = None) -> bool:
        """Update an existing job"""
        if job_id not in self.jobs:
            return False
            
        if status:
            self.jobs[job_id]["status"] = status
        if progress is not None:
            self.jobs[job_id]["progress"] = progress
        if result:
            self.jobs[job_id]["result"] = result
        if error:
            self.jobs[job_id]["error"] = error
            
        logger.info(f"Updated job {job_id}: status={status}, progress={progress}")
        return True
        
    def get_job(self, job_id: str) -> Optional[dict]:
        """Get job details"""
        return self.jobs.get(job_id)
        
    def delete_job(self, job_id: str) -> bool:
        """Delete a job"""
        if job_id in self.jobs:
            del self.jobs[job_id]
            logger.info(f"Deleted job {job_id}")
            return True
        return False