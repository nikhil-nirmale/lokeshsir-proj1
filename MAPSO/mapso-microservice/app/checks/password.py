import os
from app.models import CheckResult
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def password_check(file_path: str) -> CheckResult:
    """Check if a file is password protected"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return _check_pdf_password(file_path)
        elif ext in ('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'):
            return _check_office_password(file_path)
        else:
            return CheckResult(
                status="SKIPPED",
                details={"reason": f"Password check not supported for {ext} files"}
            )
            
    except Exception as e:
        logger.error(f"Password check failed: {str(e)}")
        return CheckResult(
            status="ERROR",
            error=str(e)
        )

def _check_pdf_password(file_path: str) -> CheckResult:
    """Check if PDF is password protected"""
    try:
        from PyPDF2 import PdfReader
        try:
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                if reader.is_encrypted:
                    return CheckResult(
                        status="FAIL",
                        details={"protected": True}
                    )
                return CheckResult(
                    status="PASS",
                    details={"protected": False}
                )
        except Exception as e:
            # PyPDF2 raises an exception if the PDF is encrypted
            if "password" in str(e).lower():
                return CheckResult(
                    status="FAIL",
                    details={"protected": True}
                )
            raise
            
    except ImportError:
        return CheckResult(
            status="ERROR",
            error="PyPDF2 not installed"
        )

def _check_office_password(file_path: str) -> CheckResult:
    """Check if Office document is password protected"""
    try:
        import msoffcrypto
        try:
            with open(file_path, 'rb') as f:
                file = msoffcrypto.OfficeFile(f)
                if file.is_encrypted():
                    return CheckResult(
                        status="FAIL",
                        details={"protected": True}
                    )
                return CheckResult(
                    status="PASS",
                    details={"protected": False}
                )
        except Exception as e:
            if "password" in str(e).lower():
                return CheckResult(
                    status="FAIL",
                    details={"protected": True}
                )
            raise
            
    except ImportError:
        return CheckResult(
            status="ERROR",
            error="msoffcrypto-tool not installed"
        )