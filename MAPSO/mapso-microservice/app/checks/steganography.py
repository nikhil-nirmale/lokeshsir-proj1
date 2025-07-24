import os
from app.models import CheckResult
import logging
import subprocess

logger = logging.getLogger(__name__)

def steganography_check(file_path: str) -> CheckResult:
    """Check for steganography in image files"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext not in ('.jpg', '.jpeg', '.png', '.bmp', '.tiff'):
            return CheckResult(
                status="SKIPPED",
                details={"reason": f"Steganography check not supported for {ext} files"}
            )
        
        # Use exiftool to check for anomalies
        try:
            result = subprocess.run(
                ["exiftool", file_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return CheckResult(
                    status="ERROR",
                    error=result.stderr
                )
            
            output = result.stdout.lower()
            suspicious = any(
                term in output 
                for term in ['comment', 'hidden', 'steganography', 'unexpected']
            )
            
            return CheckResult(
                status="FAIL" if suspicious else "PASS",
                details={"suspicious": suspicious}
            )
            
        except FileNotFoundError:
            return CheckResult(
                status="ERROR",
                error="exiftool not installed"
            )
            
    except Exception as e:
        logger.error(f"Steganography check failed: {str(e)}")
        return CheckResult(
            status="ERROR",
            error=str(e)
        )