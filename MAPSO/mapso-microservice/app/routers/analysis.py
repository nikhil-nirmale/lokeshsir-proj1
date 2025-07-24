from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
import hashlib
import os
from datetime import datetime
from app.models import (
    AnalysisRequest,
    AnalysisResponse,
    CheckType,
    CheckResult,
    StatusResponse
)
from app.config import settings
from app.services.file_processing import process_file
from app.services.job_manager import JobManager
import logging

router = APIRouter()
job_manager = JobManager()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    checks: list[CheckType] = [],
    metadata: Optional[str] = None,
    fallback_on_critical: bool = False,
    force_ocr: bool = False,
    generate_derived: bool = True,
    ocr_output_format: str = "pdf"
):
    """Endpoint for direct file upload analysis"""
    try:
        # Validate file size
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size: {settings.max_file_size} bytes"
            )

        # Generate document ID and filename
        document_id = str(uuid.uuid4())
        temp_filename = os.path.join(settings.temp_file_dir, f"{document_id}_{file.filename}")
        
        # Save file temporarily
        with open(temp_filename, "wb") as buffer:
            buffer.write(await file.read())
        
        # Calculate file hash
        file_hash = hashlib.md5(open(temp_filename, "rb").read()).hexdigest()
        
        # Process the file
        results = await process_file(
            file_path=temp_filename,
            checks=checks,
            fallback_on_critical=fallback_on_critical,
            force_ocr=force_ocr,
            generate_derived=generate_derived,
            ocr_output_format=ocr_output_format
        )
        
        # Clean up
        os.remove(temp_filename)
        
        return AnalysisResponse(
            document_id=document_id,
            filename=file.filename,
            file_hash=file_hash,
            checks=results,
            valid=all(result.status == "PASS" for result in results.values()),
            note="Analysis completed successfully",
            derived_file_url=f"/results/{document_id}.{ocr_output_format}" if generate_derived else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during document processing"
        )

@router.post("/analyze/async", response_model=StatusResponse)
async def analyze_document_async(
    request: AnalysisRequest
):
    """Endpoint for asynchronous analysis via file URL"""
    try:
        job_id = str(uuid.uuid4())
        job_manager.create_job(
            job_id=job_id,
            request=request.dict(),
            status="queued",
            created_at=datetime.utcnow().isoformat()
        )
        
        # In a real implementation, you would queue this for background processing
        # For now, we'll just return the job status
        return StatusResponse(
            job_id=job_id,
            status="queued",
            created_at=job_manager.get_job(job_id)["created_at"]
        )
        
    except Exception as e:
        logger.error(f"Error creating async job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating job"
        )