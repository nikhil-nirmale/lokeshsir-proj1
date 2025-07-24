from fastapi import APIRouter, HTTPException
from app.models import StatusResponse
from typing import Dict
import datetime

router = APIRouter()

# Mock database for job status (replace with real DB in production)
job_db: Dict[str, dict] = {}

@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_job_status(job_id: str):
    """Check the status of an async processing job"""
    job = job_db.get(job_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    
    return StatusResponse(
        job_id=job_id,
        status=job["status"],
        created_at=job["created_at"],
        progress=job.get("progress"),
        result_url=job.get("result_url"),
        error=job.get("error")
    )