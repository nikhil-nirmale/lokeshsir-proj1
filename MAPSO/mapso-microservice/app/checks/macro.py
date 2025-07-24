import olefile
from app.models import CheckResult
import logging

logger = logging.getLogger(__name__)

def macro_check(file_path: str) -> CheckResult:
    """Check for macros in Office documents"""
    try:
        if not file_path.lower().endswith(('.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx','pptm', 'xlsm', 'docm')):
            return CheckResult(
                status="PASS",
                details={"reason": "File is not an Office document"}
            )
        
        if file_path.lower().endswith(('.docx', '.xlsx', '.pptx')):
            # New Office formats (OOXML) - check for vbaProject.bin
            import zipfile
            try:
                with zipfile.ZipFile(file_path, 'r') as z:
                    has_macros = 'word/vbaProject.bin' in z.namelist() or \
                                'xl/vbaProject.bin' in z.namelist() or \
                                'ppt/vbaProject.bin' in z.namelist()
                return CheckResult(
                    status="FAIL" if has_macros else "PASS",
                    details={"has_macros": has_macros}
                )
            except zipfile.BadZipFile:
                return CheckResult(
                    status="ERROR",
                    error="Invalid Office document (not a valid ZIP file)"
                )
        
        # Legacy Office formats (OLE)
        if not olefile.isOleFile(file_path):
            return CheckResult(
                status="PASS",
                details={"reason": "File is not an OLE document"}
            )
        
        ole = olefile.OleFileIO(file_path)
        has_macros = any(
            stream for stream in ole.listdir() 
            if 'macros' in stream or 'VBA' in stream
        )
        ole.close()
        
        return CheckResult(
            status="FAIL" if has_macros else "PASS",
            details={"has_macros": has_macros}
        )
        
    except Exception as e:
        logger.error(f"Macro check failed: {str(e)}")
        return CheckResult(
            status="ERROR",
            error=str(e)
        )