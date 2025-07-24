import os
import subprocess
from app.models import CheckResult
import logging

logger = logging.getLogger(__name__)

def ads_check(file_path: str) -> CheckResult:
    """Check for Alternate Data Streams (Windows NTFS only)"""
    try:
        if not os.name == 'nt':
            return CheckResult(
                status="SKIPPED",
                details={"reason": "ADS check only available on Windows NTFS"}
            )
        
        # Use PowerShell to check for ADS
        command = f"Get-Item '{file_path}' -Stream * | Select-Object Stream"
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return CheckResult(
                status="ERROR",
                error=result.stderr
            )
        
        streams = [line.strip() for line in result.stdout.split('\n') 
                  if line.strip() and not line.strip().startswith('Stream')]
        
        # The main data stream is always present
        ads_present = len(streams) > 1
        
        return CheckResult(
            status="FAIL" if ads_present else "PASS",
            details={"streams": streams} if ads_present else None
        )
        
    except Exception as e:
        logger.error(f"ADS check failed: {str(e)}")
        return CheckResult(
            status="ERROR",
            error=str(e)
        )