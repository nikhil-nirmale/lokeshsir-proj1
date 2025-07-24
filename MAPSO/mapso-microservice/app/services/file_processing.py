from typing import Dict, List
from app.models import CheckType, CheckResult
from app.checks import (
    macro_check,
    ads_check,
    password_check,
    steganography_check,
    ocr_check
)
import os
import logging

logger = logging.getLogger(__name__)

async def process_file(
    file_path: str,
    checks: List[CheckType],
    fallback_on_critical: bool = False,
    force_ocr: bool = False,
    generate_derived: bool = True,
    ocr_output_format: str = "pdf"
) -> Dict[str, CheckResult]:
    """Process a file with the requested checks"""
    results = {}
    critical_failure = False
    
    try:
        # Perform checks in specified order
        for check in checks:
            if critical_failure and not fallback_on_critical and check != CheckType.OCR:
                results[check.value] = CheckResult(
                    status="SKIPPED",
                    error="Previous critical check failed"
                )
                continue
                
            try:
                if check == CheckType.MACRO:
                    results["macro"] = macro_check(file_path)
                elif check == CheckType.ADS:
                    results["ads"] = ads_check(file_path)
                elif check == CheckType.PASSWORD:
                    results["password"] = password_check(file_path)
                elif check == CheckType.STEGANOGRAPHY:
                    results["steganography"] = steganography_check(file_path)
                elif check == CheckType.OCR:
                    if not critical_failure or force_ocr:
                        results["ocr"] = await ocr_check(
                            file_path,
                            generate_output=generate_derived,
                            output_format=ocr_output_format
                        )
                    else:
                        results["ocr"] = CheckResult(
                            status="SKIPPED",
                            error="Critical checks failed and force_ocr not enabled"
                        )
                
                # Check if current check failed critically
                if check != CheckType.OCR and results[check.value].status != "PASS":
                    critical_failure = True
                    
            except Exception as e:
                logger.error(f"Error performing {check} check: {str(e)}")
                results[check.value] = CheckResult(
                    status="ERROR",
                    error=str(e)
                )
                if check != CheckType.OCR:
                    critical_failure = True
                    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise
        
    return results