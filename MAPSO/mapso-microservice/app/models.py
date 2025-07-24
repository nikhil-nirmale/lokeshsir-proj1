from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class CheckType(str, Enum):
    MACRO = "macro"
    ADS = "ads"
    PASSWORD = "password"
    STEGANOGRAPHY = "steganography"
    OCR = "ocr"

class Metadata(BaseModel):
    document_id: Optional[str] = Field(None, example="doc123")
    author: Optional[str] = Field(None, example="John Doe")
    document_type: Optional[str] = Field(None, example="contract")

class FallbackOptions(BaseModel):
    on_critical_failure_continue: bool = Field(False)
    force_ocr_even_if_invalid: bool = Field(False)

class OcrConfig(BaseModel):
    generate_derived: bool = Field(True)
    output_format: str = Field("pdf", regex="^(pdf|txt)$")
    include_text_inline: bool = Field(False)

class AnalysisRequest(BaseModel):
    file: Optional[str] = Field(None, description="Base64 encoded file")
    file_url: Optional[str] = Field(None, description="URL to fetch file")
    metadata: Optional[Metadata] = None
    checks: List[CheckType]
    fallback: Optional[FallbackOptions] = None
    ocr_config: Optional[OcrConfig] = None

class CheckResult(BaseModel):
    status: str
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    document_id: str
    filename: str
    file_hash: str
    checks: Dict[str, CheckResult]
    valid: Optional[bool] = None
    note: Optional[str] = None
    derived_file_url: Optional[str] = None
    ocr_text: Optional[str] = None

class StatusResponse(BaseModel):
    job_id: str
    status: str
    created_at: str
    progress: Optional[int] = None
    result_url: Optional[str] = None
    error: Optional[str] = None