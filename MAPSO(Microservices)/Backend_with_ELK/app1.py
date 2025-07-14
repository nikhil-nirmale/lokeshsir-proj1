# damn good 
import zipfile
import os
import fitz  # PyMuPDF
import hashlib
from flask import Flask, request, jsonify, send_from_directory
import zipfile
import fitz  # PyMuPDF
import olefile
# from pdfid import pdfid
import msoffcrypto
# import aspose.slides as slides
# import comtypes.client
import pytesseract
from PIL import Image, UnidentifiedImageError
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json
import mysql.connector
import requests
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
import socket
from datetime import datetime
import time
from collections import defaultdict
import subprocess
# import pythoncom
# import win32com.client
from pdf2image import convert_from_path
from docx2pdf import convert as docx2pdf_convert
import tempfile
import shutil
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # 🔧 Required fix

# Custom Logstash TCP Handler
class LogstashTCPHandler(logging.Handler):
    def __init__(self, host='logstash', port=5959):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, record):
        try:
            # Create the log entry in the format your Logstash expects
            log_entry = {
                'message': record.getMessage(),
                'asctime': datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S,%f')[:-3],
                'level': record.levelname,
                'name': record.name,
                'module': record.module,
                'funcName': record.funcName,
                'lineno': record.lineno
            }
            
            # Add any extra fields from the log record
            if hasattr(record, 'uploaded_filename'):
                log_entry['uploaded_filename'] = record.uploaded_filename
            if hasattr(record, 'file_hash'):
                log_entry['file_hash'] = record.file_hash
            if hasattr(record, 'check'):
                log_entry['check'] = record.check
            if hasattr(record, 'result'):
                log_entry['result'] = record.result
            if hasattr(record, 'download_filename'):
                log_entry['download_filename'] = record.download_filename
            if hasattr(record, 'request_count'):
                log_entry['request_count'] = record.request_count
            if hasattr(record, 'time_since_last'):
                log_entry['time_since_last'] = record.time_since_last
            if hasattr(record, 'error_msg'):
                log_entry['error_msg'] = record.error_msg
            
            # Send to Logstash via TCP with proper formatting
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 second timeout
            sock.connect((self.host, self.port))
            # Ensure proper JSON formatting for Logstash
            message = json.dumps(log_entry, ensure_ascii=False, separators=(',', ':')) + '\n'
            sock.send(message.encode('utf-8'))
            sock.close()
            
        except Exception as e:
            # Fallback - print to console if Logstash is unavailable
            print(f"Failed to send log to Logstash: {e}")
            print(f"Log entry: {record.getMessage()}")

# Configurations
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)
# CORS(app)

CORS(app, origins=["http://localhost:5173"])

# Rate limiting storage
request_counts = defaultdict(list)  # {job_id: [timestamp1, timestamp2, ...]}
last_response_cache = {}  # {job_id: (response, timestamp)}
RATE_LIMIT_WINDOW = 60  # seconds
MAX_REQUESTS_PER_WINDOW = 10
CACHE_DURATION = 5  # seconds

# Logstash Logging Setup
LOG_FILE = 'app.log'
logHandler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=10)
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)

logger = logging.getLogger("central_logger")
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)
# Use the custom Logstash handler instead of the python-logstash library
logger.addHandler(LogstashTCPHandler())
# logger.addHandler(LogstashTCPHandler(
#     host=os.getenv("LOGSTASH_HOST", "logstash"),
#     port=int(os.getenv("LOGSTASH_PORT", 5959))
# ))
# Folder Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploaded_files')
PDF_FOLDER = os.path.join(BASE_DIR, 'converted_pdfs')
IMG_FOLDER = os.path.join(BASE_DIR, 'converted_images')
TEXT_FOLDER = os.path.join(BASE_DIR, 'extracted_texts')
JSON_FOLDER = os.path.join(BASE_DIR, 'json_responses')
DERIVED_FOLDER = os.path.join(BASE_DIR, 'derived_outputs')

for folder in [UPLOAD_FOLDER, PDF_FOLDER, IMG_FOLDER, TEXT_FOLDER, JSON_FOLDER, DERIVED_FOLDER]:
    os.makedirs(folder, exist_ok=True)

DB_CONFIG = {
    'host': 'host.docker.internal',
    'port': 3307,                    # Host port you've mapped MySQL toexit
    'user': 'root',
    'password': 'root',
    'database': 'macropos'
}

# Utility Functions
def clear_folder(folder_path):
    """Clear all files from a folder"""
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        # logger.info("Folder cleared", extra={"folder": folder_path})
    except Exception as e:
        logger.error("Failed to clear folder", extra={"folder": folder_path, "error": str(e)})

def clean_old_requests():
    """Clean old request timestamps to prevent memory leaks"""
    current_time = time.time()
    for job_id in list(request_counts.keys()):
        request_counts[job_id] = [
            ts for ts in request_counts[job_id] 
            if current_time - ts < RATE_LIMIT_WINDOW
        ]
        if not request_counts[job_id]:
            del request_counts[job_id]

def perform_ads_check(filepath):
    try:
        output = subprocess.check_output(['cmd', '/c', 'dir', '/r', filepath], stderr=subprocess.DEVNULL)
        decoded = output.decode(errors='ignore')
        result = ":$DATA" in decoded
        return {"result": "DETECTED" if result else "NOT DETECTED"}
    except Exception as e:
        return {"result": "UNKNOWN", "error": str(e)}


def is_rate_limited(job_id, client_ip):
    """Check if request should be rate limited"""
    current_time = time.time()
    clean_old_requests()
    
    # Check rate limit
    recent_requests = request_counts[job_id]
    if len(recent_requests) >= MAX_REQUESTS_PER_WINDOW:
        return True
    
    # Add current request
    request_counts[job_id].append(current_time)
    return False

def get_cached_response(job_id):
    """Get cached response if available and recent"""
    if job_id in last_response_cache:
        response, timestamp = last_response_cache[job_id]
        if time.time() - timestamp < CACHE_DURATION:
            return response
    return None

def cache_response(job_id, response):
    """Cache response for short duration"""
    last_response_cache[job_id] = (response, time.time())

def calculate_md5(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def to_bool_int(val):
    if isinstance(val, bool):
        return int(val)
    if isinstance(val, str):
        return 1 if val.lower() == 'true' else 0
    return int(bool(val))
def save_file_metadata(filename, file_hash, valid, generate_derived,on_critical_failure_continue,force_ocr_even_if_invalid):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_metadata (filename, file_hash, valid, generate_derived,on_critical_failure_continue,force_ocr_even_if_invalid) VALUES (%s, %s, %s,%s,%s,%s)",
                   (filename, file_hash, valid,to_bool_int(generate_derived),to_bool_int(on_critical_failure_continue),to_bool_int(force_ocr_even_if_invalid)))
    conn.commit()
    file_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return file_id

def save_check_to_db(file_id, check_type, result, error=None):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_checks (file_id, check_type, result, error) VALUES (%s, %s, %s,%s)",
                   (file_id, check_type, result, error))
    conn.commit()
    cursor.close()
    conn.close()

def save_derived_file(file_hash, content):
    """Save derived content to file"""
    try:
        derived_filename = f"{file_hash}_derived.txt"
        derived_path = os.path.join(DERIVED_FOLDER, derived_filename)
        with open(derived_path, 'w', encoding='utf-8') as f:
            f.write(content)
        # logger.info("Derived file saved", extra={"file_hash": file_hash, "path": derived_path})
        return derived_path
    except Exception as e:
        logger.error("Failed to save derived file", extra={"file_hash": file_hash, "error": str(e)})
        return None

# Check Functions
def perform_macro_check(filepath):
    # try:
    #     from oletools.olevba import VBA_Parser
    #     vbaparser = VBA_Parser(filepath)
    #     result = "PRESENT" if vbaparser.detect_vba_macros() else "ABSENT"
    #     return {"result": result}
    # except Exception as e:
    #     return {"result": "UNKNOWN", "error": str(e)}
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext in ['.doc', '.xls', '.ppt']:
        try:
            from oletools.olevba import VBA_Parser
            print(f"[INFO] Scanning {filepath} using oletools VBA_Parser")
            vbaparser = VBA_Parser(filepath)
            if vbaparser.detect_vba_macros():
                print("[DEBUG] Macros FOUND by VBA_Parser.")
                return {"result": "PRESENT"}
            else:
                print("[DEBUG] VBA_Parser ran successfully but found NO macros.")
                return {"result": "ABSENT"}
        except Exception as e:
            print(f"[ERROR] VBA_Parser failed on {filepath}: {e}")
            return {"result": "UNKNOWN", "error": str(e)}

    elif ext in ['.docx', '.xlsx', '.pptx', '.docm', '.xlsm', '.pptm']:
        try:
            print(f"[INFO] Scanning {filepath} using zipfile for vbaProject.bin")
            with zipfile.ZipFile(filepath, 'r') as z:
                has_macro = any('vbaProject.bin' in name for name in z.namelist())
                if has_macro:
                    print("[DEBUG] vbaProject.bin found in OpenXML file.")
                    return {"result": "PRESENT"}
                else:
                    print("[DEBUG] No macro project found in ZIP structure.")
                    return {"result": "ABSENT"}
        except Exception as e:
            print(f"[ERROR] zipfile failed on {filepath}: {e}")
            return {"result": "UNKNOWN", "error": str(e)}

    elif ext == '.pdf':
        try:
            print(f"[INFO] Scanning PDF for embedded JavaScript or actions: {filepath}")
            doc = fitz.open(filepath)
            suspicious = False

            # Inspect the full PDF structure
            for xref in range(1, doc.xref_length()):
                obj = doc.xref_object(xref)
                if "/JavaScript" in obj or "/JS" in obj or "/OpenAction" in obj:
                    suspicious = True
                    break

            if suspicious:
                return {"result": "PRESENT"}
            return {"result": "ABSENT"}

        except Exception as e:
            print(f"[ERROR] PDF macro-like scan failed: {e}")
            return {"result": "UNKNOWN", "error": str(e)}
        # elif ext == '.pdf':
    #     try:
    #         print(f"[INFO] Scanning PDF for embedded scripts or rich media: {filepath}")
    #         doc = fitz.open(filepath)
    #         suspicious = False
    #         for page in doc:
    #             if page.get_links():
    #                 suspicious = True
    #                 break
    #         for i in range(len(doc)):
    #             xrefs = doc.get_page_images(i)
    #             if any("/JS" in str(x) or "/JavaScript" in str(x) for x in xrefs):
    #                 suspicious = True
    #                 break
    #         if suspicious:
    #             return {"result": "PRESENT"}
    #         return {"result": "ABSENT"}
    #     except Exception as e:
    #         print(f"[ERROR] PDF macro-like scan failed: {e}")
    #         return {"result": "UNKNOWN", "error": str(e)}
    else:
        print(f"[WARN] Unsupported format for file: {filepath}")
        return {"result": "UNSUPPORTED_FORMAT"}
def perform_password_check(filepath):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.pdf':
            doc = fitz.open(filepath)
            return {"result": "PROTECTED" if doc.is_encrypted else "UNPROTECTED"}

            # return "PROTECTED" if doc.is_encrypted else "UNPROTECTED"
        elif ext == '.docx':
            try:
                # pdf_dir = "/app/converted_pdfs"
                filename_wo_ext = os.path.splitext(os.path.basename(filepath))[0]
                output_path = os.path.join(PDF_FOLDER, f"{filename_wo_ext}.pdf")
                success, pdf_path = convert_word_to_pdf(filepath, output_path)
                # if not success:
                #     logger.error("Word to PDF conversion failed", extra={"error_msg": pdf_path})
                #     return "PROTECTED"
                # else:
                #     doc = fitz.open(pdf_path)
                    # return {"result": "PROTECTED" if doc.is_encrypted else "UNPROTECTED"}
                if success:
                    if os.path.exists(pdf_path):
                        doc = fitz.open(pdf_path)
                        return {"result": "PROTECTED" if doc.is_encrypted else "UNPROTECTED"}
                    else:
                        logger.error("Converted PDF path does not exist", extra={"error_msg": pdf_path})
                        return {"result": "PROTECTED"}
                else:
                    logger.error("PDF conversion failed", extra={"error_msg": pdf_path})
                    return {"result": "Error", "error": pdf_path}
            except Exception as e:
                logger.error("Converted PDF check failed", extra={"error_msg": str(e)})
                return "Error"
        # elif ext in ['.docx', '.xlsx', '.pptx']:
        #     try:
        #         with open(filepath, "rb") as f:
        #             office_file = msoffcrypto.OfficeFile(f)
        #             office_file.load_key(password=None)
        #             office_file.decrypt(None)  # Raises an exception if encrypted
        #             return "UNPROTECTED"
        #     except Exception as e:
        #         logger.error("Word password check failed", extra={"error_msg": str(e)})
        #         return "PROTECTED"
        # # elif os.path.splitext(filepath)[1].lower() in ['.docx', '.xlsx', '.pptx']:
        #     ext = os.path.splitext(filepath)[1].lower()
        #     try:
        #         if ext in ['.docx', '.xlsx', '.pptx']:
        #             with open(filepath, "rb") as f:
        #                 office_file = msoffcrypto.OfficeFile(f)
        #                 office_file.load_key(password=None)
        #                 office_file.decrypt(None)  # Will raise if protected
        #                 return "UNPROTECTED"
        #         else:
        #             return "UNKNOWN"
        #     except Exception as e:
        #         return "PROTECTED"
        #     # with zipfile.ZipFile(filepath) as zf:
            #     result = "PROTECTED" if any(name.startswith('EncryptedPackage') for name in zf.namelist()) else "UNPROTECTED"
        elif ext in ['.xlsx', '.ppt','.xls','.pptx']:
        #     if olefile.isOleFile(filepath):
        #         ole = olefile.OleFileIO(filepath)
        #         result = "PROTECTED" if ole.exists('EncryptionInfo') or ole.exists('EncryptedPackage') else "UNPROTECTED"
        #         return {"result": result}
        #     else:
        #         result = "File Not Found"
        #         return {"result": result}
            try:
                with zipfile.ZipFile(filepath) as z:
                    encrypted = any("encryption" in name.lower() for name in z.namelist())
                    return {"result": "PROTECTED" if encrypted else "UNPROTECTED"}
            except zipfile.BadZipFile:
                pass  # not OpenXML

            # Check OLE (.xls, misnamed .xlsx)
            if olefile.isOleFile(filepath):
                ole = olefile.OleFileIO(filepath)
                if ole.exists("EncryptionInfo") or ole.exists("EncryptedPackage"):
                    return {"result": "PROTECTED"}
                else:
                    return {"result": "UNPROTECTED"}

            return {"result": "UNSUPPORTED_OR_CORRUPT_FILE"}
    except Exception as e:
        return {"result": "UNKNOWN", "error": str(e)}

# def perform_steganography_check(filepath):
#     try:
#         # output = subprocess.check_output([r'C:\\Tools\\exiftool-13.30_64\\exiftool.exe', filepath], stderr=subprocess.DEVNULL)
#         output = subprocess.check_output(['exiftool', filepath], stderr=subprocess.DEVNULL)
#         decoded = output.decode(errors='ignore')
#         suspicious_tags = ["Comment", "Software", "ImageDescription"]
#         suspicious = any(tag in decoded for tag in suspicious_tags)
#         result = "SUSPICIOUS" if suspicious else "CLEAN"
#         return {"result": result}
#     except Exception as e:
#         return {"result": "UNKNOWN", "error": str(e)}
# def perform_steganography_check(filepath):
#     import subprocess
#     try:
#         output = subprocess.check_output(['exiftool', filepath], stderr=subprocess.DEVNULL)
#         decoded = output.decode(errors='ignore').splitlines()
        
#         # Convert lines like 'Comment : something' into key-value pairs
#         metadata = dict(line.split(":", 1) for line in decoded if ":" in line)
#         suspicious_tags = {"Comment", "Software", "ImageDescription"}

#         # Normalize keys by stripping and comparing
#         suspicious = any(key.strip() in suspicious_tags for key in metadata.keys())
#         result = "SUSPICIOUS" if suspicious else "CLEAN"
#         return {"result": result}

#     except Exception as e:
#         return {"result": "UNKNOWN", "error": str(e)}
def perform_steganography_check(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    result = "CLEAN"

    try:
        if ext in ['.jpg', '.jpeg']:
            # 1. Check with stegdetect (JPEG-specific)
            try:
                output = subprocess.check_output(['stegdetect', filepath], stderr=subprocess.DEVNULL).decode()
                if filepath in output:
                    result = "SUSPICIOUS"
            except subprocess.CalledProcessError:
                result = "CLEAN"  # stegdetect may return non-zero even when clean

            # 2. Extra check with exiftool
            output = subprocess.check_output(['exiftool', filepath], stderr=subprocess.DEVNULL)
            lines = output.decode(errors='ignore').splitlines()
            metadata = dict(line.split(":", 1) for line in lines if ":" in line)
            suspicious_tags = {"Comment", "Software", "ImageDescription"}
            if any(k.strip() in suspicious_tags for k in metadata.keys()):
                result = "SUSPICIOUS"

        elif ext in ['.png', '.bmp']:
            # Use zsteg for LSB check
            try:
                output = subprocess.check_output(['zsteg', filepath], stderr=subprocess.DEVNULL).decode()
                if "ASCII" in output or "text" in output:
                    result = "SUSPICIOUS"
            except subprocess.CalledProcessError:
                result = "CLEAN"

        elif ext in ['.pdf', '.docx', '.pptx', '.xlsx']:
            # Use exiftool for structural metadata anomalies
            output = subprocess.check_output(['exiftool', filepath], stderr=subprocess.DEVNULL)
            lines = output.decode(errors='ignore').splitlines()
            metadata = dict(line.split(":", 1) for line in lines if ":" in line)
            suspicious_tags = {"Comment", "Creator", "Software", "Title", "Subject", "Producer", "Keywords"}
            if any(k.strip() in suspicious_tags for k in metadata.keys()):
                result = "SUSPICIOUS"

        else:
            result = "UNSUPPORTED"

    except Exception as e:
        return {"result": "UNKNOWN", "error": str(e)}

    return {"result": result}


# added extra
# def convert_docx_to_pdf_libreoffice(input_path, output_path):
#     try:
#         # LibreOffice will create the PDF with the same base name in the output directory
#         output_dir = os.path.dirname(output_path)
#         subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             input_path
#         ], check=True)
        
#         # The converted PDF will have the same basename but .pdf extension
#         base_name = os.path.splitext(os.path.basename(input_path))[0]
#         converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")
        
#         # Rename/move to your expected output_path if needed
#         if converted_pdf_path != output_path:
#             os.rename(converted_pdf_path, output_path)
            
#         return True, None
#     except Exception as e:
#         return False, str(e)
def convert_docx_to_pdf_libreoffice(input_path, output_path):
    try:
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

        if not os.path.exists(converted_pdf_path):
            return False, f"Conversion failed. PDF not found: {converted_pdf_path}"

        if converted_pdf_path != output_path:
            os.rename(converted_pdf_path, output_path)

        return True,output_path

    except Exception as e:
        return False,output_path

# 1st priority
# def convert_word_to_pdf_libreoffice(input_path, output_path):
#     try:
#         # LibreOffice will create the PDF with the same base name in the output directory
#         output_dir = os.path.dirname(output_path)
#         subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             input_path
#         ], check=True)
        
#         # The converted PDF will have the same basename but .pdf extension
#         base_name = os.path.splitext(os.path.basename(input_path))[0]
#         converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")
        
#         # Rename/move to your expected output_path if needed
#         if converted_pdf_path != output_path:
#             os.rename(converted_pdf_path, output_path)
            
#         return output_path
#     except Exception as e:
#         return e;

# def convert_word_to_pdf_libreoffice(input_path, output_path):
#     try:
#         if not os.path.exists(input_path):
#             return False, f"Input file does not exist: {input_path}"
        
#         output_dir = os.path.dirname(output_path)
#         os.makedirs(output_dir, exist_ok=True)

#         # Call LibreOffice headless conversion
#         result = subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             input_path
#         ], capture_output=True, check=True)

#         # Log stdout/stderr for debugging
#         stdout = result.stdout.decode(errors="ignore")
#         stderr = result.stderr.decode(errors="ignore")
#         print(f"[LibreOffice STDOUT] {stdout}")
#         print(f"[LibreOffice STDERR] {stderr}")

#         # Determine output file path
#         base_name = os.path.splitext(os.path.basename(input_path))[0]
#         converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

#         if not os.path.exists(converted_pdf_path):
#             return False, f"Conversion failed. Output PDF not found: {converted_pdf_path}"

#         # Move to exact expected path if needed
#         if converted_pdf_path != output_path:
#             os.rename(converted_pdf_path, output_path)

#         return True, output_path

#     except subprocess.CalledProcessError as e:
#         return False, f"LibreOffice failed: {e.stderr.decode(errors='ignore') if e.stderr else str(e)}"
#     except Exception as e:
        # return False, str(e)
def convert_word_to_pdf_libreoffice(input_path, output_path):
    try:
        if not os.path.exists(input_path):
            return f"Input file does not exist: {input_path}"
        
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        result = subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], capture_output=True, check=True)

        stdout = result.stdout.decode(errors="ignore")
        stderr = result.stderr.decode(errors="ignore")
        print(f"[LibreOffice STDOUT] {stdout}")
        print(f"[LibreOffice STDERR] {stderr}")

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

        if not os.path.exists(converted_pdf_path):
            return f"Conversion failed: PDF not found"

        if converted_pdf_path != output_path:
            os.rename(converted_pdf_path, output_path)

        return output_path

    except subprocess.CalledProcessError as e:
        return e.stderr.decode(errors="ignore") if e.stderr else str(e)
    except Exception as e:
        return str(e)



import subprocess
import os

def convert_ppt_to_pdf_libreoffice(input_path, output_path):
    try:
        output_dir = os.path.dirname(output_path)
        
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)

        # Build expected output PDF path
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

        # Rename to expected output path if needed
        if converted_pdf_path != output_path:
            os.rename(converted_pdf_path, output_path)

        return True, None
    
    except Exception as e:
        return False, str(e)



def convert_pptx_to_jpg(input_path, output_path):
    with slides.Presentation(input_path) as presentation:
        presentation.save(output_path, slides.export.SaveFormat.PDF)
# def convert_pptx_to_jpg(input_path, output_dir):
#     subprocess.run([
#         "libreoffice",
#         "--headless",
#         "--convert-to", "jpg",
#         "--outdir", output_dir,
#         input_path
#     ], check=True)
# 
def perform_ocr(filepath, generate_derived, file_hash):
    try:
        ext = os.path.splitext(filepath)[1].lower()
        print('ext:',ext)
        full_text = ""
        print('entered perform OCR')
        if ext == ".pdf":
            print('Entered perform OCR PDF')
            doc = fitz.open(filepath)
            if len(doc) == 0:
                return {"result": "FAILED", "error": "Empty PDF"}
            for i in range(len(doc)):
                page = doc.load_page(i)
                pix = page.get_pixmap()
                img_path = os.path.join(IMG_FOLDER, f"page{i+1}.png")
                with open(img_path, "wb") as img_file:
                    img_file.write(pix.tobytes())
                try:
                    text = pytesseract.image_to_string(Image.open(img_path))
                    full_text += text + "\n"
                except UnidentifiedImageError:
                    continue

        # elif ext == ".docx":
        #     clear_folder(PDF_FOLDER)
        #     converted_pdf = os.path.join(PDF_FOLDER, "converted.pdf")
        #     try:
        #         # pythoncom.CoInitialize()
        #         docx2pdf_convert(filepath, converted_pdf)
        #         # pythoncom.CoUninitialize()
        #     except Exception as e:
        #         return {"result": "FAILED", "error": f"Docx-to-PDF conversion failed: {str(e)}"}
        #     return perform_ocr(converted_pdf, generate_derived, file_hash)
        elif ext == ".docx":
            print('Entered perform OCR docx')
            # clear_folder(PDF_FOLDER)
            converted_pdf = os.path.join(PDF_FOLDER, "converted.pdf")
            success, error = convert_docx_to_pdf_libreoffice(filepath, converted_pdf)
            if not success:
                return {"result": "FAILED", "error": f"Docx-to-PDF conversion failed: {error}"}
            return perform_ocr(converted_pdf, generate_derived, file_hash)
        elif ext in [".ppt", ".pptx"]:
            print('Entered perform OCR ppt')
            # clear_folder(PDF_FOLDER)
            converted_pdf = os.path.join(PDF_FOLDER, "converted.pdf")
            success, error = convert_ppt_to_pdf_libreoffice(filepath, converted_pdf)
            if not success:
                return {"result": "FAILED", "error": f"PPT-to-PDF conversion failed: {error}"}
            return perform_ocr(converted_pdf, generate_derived, file_hash)
        
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif']:
            print('Entered into images')
            img_path = os.path.join(IMG_FOLDER, os.path.basename(filepath))
            shutil.copy2(filepath, img_path)  # Use copy instead of rename to preserve original
            try:
                print('getting text')
                full_text = pytesseract.image_to_string(Image.open(img_path))
                print('full text:', full_text)
            except UnidentifiedImageError:
                return {"result": "FAILED", "error": "Unable to process image file"}

        else:
            return {"result": "FAILED", "error": f"Unsupported file type for OCR: {ext}"}
        print('still there outside full text')
        if full_text.strip():
            print('eneterd full_text')
            text_file_path = os.path.join(TEXT_FOLDER, "ocr_output.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print('generate_derived value:',generate_derived)
            if str(generate_derived).lower()=='true':
                print('entered here')
                derived_path = save_derived_file(file_hash, full_text)
                return {"result": "TEXT EXTRACTED", "text_file": text_file_path, "derived": derived_path}
            return {"result": "TEXT EXTRACTED", "text_file": text_file_path}
        else:
            return {"result": "FAILED", "error": "No readable text"}

    except Exception as e:
        return {"result": "FAILED", "error": str(e)}

# PDF Conversion Functions
def convert_to_pdf(filepath, output_folder):
    """Convert various document formats to PDF"""
    try:
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        print('ext:',ext)
        
        output_path = os.path.join(output_folder, f"{name}.pdf")
        
        if ext == '.pdf':
            # Already PDF, just copy
            shutil.copy2(filepath, output_path)
            # logger.info("PDF file copied", extra={"original_file": filename, "output_path": output_path})
            return output_path
            
        elif ext in ['.doc', '.docx']:
            print('entered into docx')
            return convert_word_to_pdf_libreoffice(filepath, output_path)
            
        elif ext in ['.xls', '.xlsx']:
            return convert_excel_to_pdf(filepath, output_path)
            
        elif ext in ['.ppt', '.pptx']:
            return convert_pptx_to_jpg(filepath, output_path)
            
        
        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return convert_image_to_pdf(filepath, output_path)
            
        else:
            logger.warning("Unsupported file format for PDF conversion", extra={"extension": ext})
            return None
            
    except Exception as e:
        logger.error("PDF conversion failed", extra={"error": str(e), "file": filepath})
        return None
def convert_pptx_to_pdf_libreoffice(input_path, output_path):
    try:
        output_dir = os.path.dirname(output_path)
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)

        base_name = os.path.splitext(os.path.basename(input_path))[0]
        converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

        if converted_pdf_path != output_path:
            os.rename(converted_pdf_path, output_path)

        return output_path
    except Exception as e:
        logger.error("PPTX to PDF conversion failed", extra={"error": str(e)})
        return None

# def convert_word_to_pdf(filepath, output_path):
#     """Convert Word documents to PDF using COM automation"""
#     try:
#         # pythoncom.CoInitialize()
#         word = win32com.client.Dispatch("Word.Application")
#         word.Visible = False
        
#         doc = word.Documents.Open(os.path.abspath(filepath))
#         doc.SaveAs(os.path.abspath(output_path), FileFormat=17)  # 17 = PDF format
#         doc.Close()
#         word.Quit()
#         # pythoncom.CoUninitialize()
        
#         # logger.info("Word document converted to PDF", extra={"input": filepath, "output": output_path})
#         return output_path
#     except Exception as e:
#         logger.error("Word to PDF conversion failed", extra={"error": str(e)})
#         return None
def convert_word_to_pdf(input_path, output_path):
    output_dir = os.path.dirname(output_path)
    try:
        # Run LibreOffice to convert the file
        subprocess.run([
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", output_dir,
            input_path
        ], check=True)

        # Infer the actual converted file path
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        converted_pdf_path = os.path.join(output_dir, base_name + ".pdf")

        # Move to desired output path if needed
        if converted_pdf_path != output_path:
            os.rename(converted_pdf_path, output_path)

        return True, output_path
    except Exception as e:
        return False, str(e)
# def convert_word_to_pdf(input_path, output_path):
#     output_dir = os.path.dirname(output_path)
#     try:
#         subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             input_path
#         ], check=True)

#         generated_pdf = os.path.join(output_dir, os.path.splitext(os.path.basename(input_path))[0] + ".pdf")
        
#         if os.path.exists(generated_pdf):
#             return generated_pdf
#         else:
#             return "PDF not generated"
#     except Exception as e:
#         return str(e)







# def convert_word_to_pdf(input_path, output_dir):
#     try:
#         result = subprocess.run([
#             "libreoffice",
#             "--headless",
#             "--convert-to", "pdf",
#             "--outdir", output_dir,
#             input_path
#         ], capture_output=True, check=True)

#         base_name = os.path.splitext(os.path.basename(input_path))[0]
#         pdf_path = os.path.join(output_dir, base_name + ".pdf")

#         if not os.path.exists(pdf_path):
#             return False, "Conversion failed or PDF not found"

#         return True, pdf_path

#     except Exception as e:
#         return False, str(e)


def convert_excel_to_pdf(file_path):
    # try:
    #     with zipfile.ZipFile(filepath) as zf:
    #         if 'xl/workbook.xml' not in zf.namelist():
    #             return True
    #         return False
    # except RuntimeError as e:
    #     # Encrypted files throw this error
    #     if 'encrypted' in str(e).lower():
    #         return True
    #     return False
    # except Exception as e:
    #     print("Error:", e)
    #     return False
    try:
        with open(file_path, "rb") as f:
            office_file = msoffcrypto.OfficeFile(f)
            if office_file.is_encrypted():
                print(os.path.abspath(file_path))  # ✅ Return full file path
                return file_path
            return file_path
    except Exception as e:
        print(f"Error with {file_path}: {e}")
        return False
# def convert_powerpoint_to_pdf(filepath, output_path):
#     """Convert PowerPoint documents to PDF using COM automation"""
#     try:
#         # pythoncom.CoInitialize()
#         powerpoint = win32com.client.Dispatch("PowerPoint.Application")
#         powerpoint.Visible = True
        
#         presentation = powerpoint.Presentations.Open(os.path.abspath(filepath))
#         presentation.SaveAs(os.path.abspath(output_path), 32)  # 32 = PDF format
#         presentation.Close()
#         powerpoint.Quit()
#         # pythoncom.CoUninitialize()
        
#         logger.info("PowerPoint document converted to PDF", extra={"input": filepath, "output": output_path})
#         return output_path
#     except Exception as e:
#         logger.error("PowerPoint to PDF conversion failed", extra={"error": str(e)})
#         return None

# def convert_text_to_pdf(filepath, output_path):
#     """Convert text file to PDF using reportlab"""
#     try:
#         from reportlab.pdfgen import canvas
#         from reportlab.lib.pagesizes import letter
        
#         c = canvas.Canvas(output_path, pagesize=letter)
#         width, height = letter
        
#         with open(filepath, 'r', encoding='utf-8') as f:
#             text = f.read()
        
#         # Simple text to PDF conversion
#         y = height - 50
#         for line in text.split('\n'):
#             if y < 50:  # New page
#                 c.showPage()
#                 y = height - 50
#             c.drawString(50, y, line[:80])  # Limit line length
#             y -= 15
            
#         c.save()
#         logger.info("Text file converted to PDF", extra={"input": filepath, "output": output_path})
#         return output_path
#     except Exception as e:
#         logger.error("Text to PDF conversion failed", extra={"error": str(e)})
#         return None

def convert_image_to_pdf(filepath, output_path):
    """Convert image to PDF"""
    try:
        image = Image.open(filepath)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output_path, 'PDF')
        
        # logger.info("Image converted to PDF", extra={"input": filepath, "output": output_path})
        return output_path
    except Exception as e:
        logger.error("Image to PDF conversion failed", extra={"error": str(e)})
        return None

def convert_pdf_to_images(pdf_path, output_folder, file_hash):
    """Convert PDF pages to individual images"""
    try:
        # Convert PDF to images using pdf2image
        
        images = convert_from_path(pdf_path, dpi=200)
        
        image_paths = []
        for i, image in enumerate(images):
            image_filename = f"{file_hash}_page_{i+1}.png"
            image_path = os.path.join(output_folder, image_filename)
            image.save(image_path, 'PNG')
            image_paths.append(image_path)
            
        # logger.info("PDF converted to images", extra={
        #     "pdf_path": pdf_path, 
        #     "pages_converted": len(images),
        #     "output_folder": output_folder
        # })
        return image_paths
    except Exception as e:
        logger.error("PDF to images conversion failed", extra={"error": str(e)})
        return []

# Routes
@app.route('/status/<int:job_id>', methods=['GET'])
def get_status(job_id):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    
    # Check cache first
    cached_response = get_cached_response(job_id)
    if cached_response:
        # logger.info("Status served from cache", extra={"job_id": job_id, "client_ip": client_ip})
        return cached_response
    
    # Check rate limiting
    if is_rate_limited(job_id, client_ip):
        logger.warning("Rate limit exceeded", extra={
            "job_id": job_id, 
            "client_ip": client_ip,
            "request_count": len(request_counts[job_id])
        })
        return jsonify({"error": "Too many requests. Please wait before retrying."}), 429
    
    # Count recent requests for logging
    request_count = len(request_counts[job_id])
    time_since_last = None
    if len(request_counts[job_id]) > 1:
        time_since_last = f"{(request_counts[job_id][-1] - request_counts[job_id][-2]) * 1000:.0f}ms"
    
    # logger.info("Status requested", extra={
    #     "job_id": job_id, 
    #     "client_ip": client_ip,
    #     "request_count": request_count,
    #     "time_since_last": time_since_last
    # })
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM file_metadata WHERE id = %s", (job_id,))
    metadata = cursor.fetchone()
    print('metadata from status:',metadata)
    cursor.execute("SELECT * FROM file_checks WHERE file_id = %s", (job_id,))
    checks = cursor.fetchall()
    cursor.close()
    conn.close()

    if not metadata:
        logger.warning("Job not found", extra={"job_id": job_id, "client_ip": client_ip})
        return jsonify({"error": "Job not found"}), 404

    response_data = {
        "job_id": job_id,
        "status": "done",
        "result": {
            "valido_status": "VALID" if metadata["valid"] else "INVALID",
            "generate_derived":metadata['generate_derived'],
            'on_critical_failure_continue':metadata['on_critical_failure_continue'],
            "force_ocr_even_if_invalid": metadata['force_ocr_even_if_invalid'],
            "checks": [{
                "name": check["check_type"],
                "result": check["result"],
                "error": check["error"]
            } for check in checks]
        }
    }
    response = jsonify(response_data)
    print('reponse:',response)

    cache_response(job_id, response)
    
    # logger.info("Status retrieved successfully", extra={
    #     "job_id": job_id, 
    #     "valid": metadata["valid"],
    #     "client_ip": client_ip,
    #     "served_from_db": True
    # })
    
    return response

@app.route('/download/json/<int:job_id>', methods=['GET'])
def download_result_json_by_id(job_id):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    logger.info("JSON download requested", extra={"job_id": job_id, "client_ip": client_ip})
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash FROM file_metadata WHERE id = %s", (job_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        logger.warning("Job ID not found for JSON download", extra={"job_id": job_id, "client_ip": client_ip})
        return jsonify({"error": "Job ID not found"}), 404

    file_hash = row[0]
    filename = f"{file_hash}_results.json"
    logger.info("JSON file downloaded", extra={"job_id": job_id, "download_filename": filename, "client_ip": client_ip})
    return send_from_directory(JSON_FOLDER, filename, as_attachment=True)

@app.route('/download/ocr/<int:job_id>', methods=['GET'])
def download_ocr_file_by_id(job_id):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    logger.info("OCR download requested", extra={"job_id": job_id, "client_ip": client_ip})
    
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash FROM file_metadata WHERE id = %s", (job_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        logger.warning("Job ID not found for OCR download", extra={"job_id": job_id, "client_ip": client_ip})
        return jsonify({"error": "Job ID not found"}), 404

    file_hash = row[0]
    filename = f"{file_hash}_derived.txt"
    logger.info("OCR file downloaded", extra={"job_id": job_id, "download_filename": filename, "client_ip": client_ip})
    return send_from_directory(DERIVED_FOLDER, filename, as_attachment=True)
def save_temp_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath

def convert_google_drive_link(url):
    if 'docs.google.com/document/d/' in url:
        try:
            doc_id = url.split('/d/')[1].split('/')[0]
            return f"https://docs.google.com/uc?export=download&id={doc_id}"
        except:
            pass
    return url

def download_file_from_url(url):
    url = convert_google_drive_link(url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download file")
    filename = url.split("/")[-1].split("?")[0] or "downloaded_file.docx"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath, filename

@app.route('/validate', methods=['POST'])
def validate_document():
    clear_folder(UPLOAD_FOLDER)
    clear_folder(PDF_FOLDER)
    clear_folder(IMG_FOLDER)
    clear_folder(TEXT_FOLDER)
    clear_folder(JSON_FOLDER)
    clear_folder(DERIVED_FOLDER)
    file = request.files.get('file')
    # print('request:',request.data)
    # print('request1:',request.form.get('generate_derived'))
    file_url = request.form.get('file_url')
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    logger.info("Document validation started", extra={"client_ip": client_ip})
    # if file:
    #     filepath = save_temp_file(file)
    #     filename = file.filename
    # elif file_url:
    #     filepath, filename = download_file_from_url(file_url)
    # else:
    #     return jsonify({"error": "No file or URL provided"}), 400

    # file = request.files.get('file')
    checks = request.form.getlist('checks[]') or request.form.getlist('checks')
    print('checks:',checks)
    # New parameters
    generate_derived = request.form.get('generate_derived')
    print('generate_derived result:',generate_derived)
    on_critical_failure_continue = request.form.get('on_critical_failure_continue')
    force_ocr_even_if_invalid = request.form.get('force_ocr_even_if_invalid')    
    logger.info("Validation parameters", extra={
        "checks": checks,
        "generate_derived": generate_derived,
        "on_critical_failure_continue": on_critical_failure_continue,
        "force_ocr_even_if_invalid": force_ocr_even_if_invalid,
        "client_ip": client_ip
    })
    
    if not file:
        logger.error("No file provided in validation request", extra={"client_ip": client_ip})
        return jsonify({"error": "No file provided"}), 400
        
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    file_hash = calculate_md5(filepath)
    # logger.info("File uploaded successfully", extra={
    #     "uploaded_filename": filename, 
    #     "file_hash": file_hash,
    #     "client_ip": client_ip
    # })

    # STEP 1: Convert to PDF if needed
    pdf_path = convert_to_pdf(filepath, PDF_FOLDER)
    if pdf_path:
        print('pdf_path',pdf_path)
        pass
        # logger.info("File converted to PDF", extra={"pdf_path": pdf_path, "file_hash": file_hash})
    else:
        logger.warning("PDF conversion failed or not applicable", extra={"file_hash": file_hash})

    
    
    
    
    
    # STEP 2: Convert PDF to images if PDF exists
    image_paths = []
    if pdf_path and os.path.exists(pdf_path):
        image_paths = convert_pdf_to_images(pdf_path, IMG_FOLDER, file_hash)
        if image_paths:
            pass
            # logger.info("PDF converted to images", extra={
            #     "image_count": len(image_paths), 
            #     "file_hash": file_hash
            # })

    # STEP 3: Perform requested checks
    results = {}
    critical_passed = True
    critical_checks_failed = []
    
    # Define critical checks (those that affect validity)
    critical_checks = ['macro', 'password', 'steganography', 'ads']
    
    for check in checks:
        logger.info("Starting check", extra={"check": check, "file_hash": file_hash})
        
        try:
            if check == 'macro':
                result = perform_macro_check(filepath)
            elif check == 'password':
                result = perform_password_check(filepath)
            elif check == 'steganography':
                result = perform_steganography_check(filepath)
            elif check == 'ads':
                # Add ADS check implementation here
                result = perform_ads_check(filepath)  # You'll need to implement this function
            elif check == 'ocr':
                # OCR check - initially run without derived file generation
                result = perform_ocr(filepath, True, file_hash)
            else:
                result = {"result": "UNKNOWN", "error": "Unsupported check"}
                
            logger.info("Check completed", extra={"check": check, "result": result['result'], "file_hash": file_hash})
            results[check] = result
            
            # Check if critical check failed
            if check in critical_checks:
                if result['result'] not in ['ABSENT', 'UNPROTECTED','PROTECTED', 'NOT_APPLICABLE', 'CLEAN','DETECTED','NOT DETECTED']:
                    critical_checks_failed.append(check)
                    if not on_critical_failure_continue:
                        logger.warning("Critical check failed, stopping validation", extra={
                            "check": check, 
                            "result": result['result'], 
                            "file_hash": file_hash
                        })
                        critical_passed = False
                        break
                    else:
                        critical_passed = False
                        
        except Exception as e:
            logger.error("Check failed with exception", extra={
                "check": check, 
                "error": str(e), 
                "file_hash": file_hash
            })
            results[check] = {"result": "ERROR", "error": str(e)}
            
            if check in critical_checks and not on_critical_failure_continue:
                logger.warning("Critical check error, stopping validation", extra={
                    "check": check, 
                    "error": str(e), 
                    "file_hash": file_hash
                })
                critical_passed = False
                break

    # STEP 4: Handle OCR with special conditions
    has_text_extracted = False
    ocr_result = results.get('ocr', {})
    
    if 'ocr' in checks:
        has_text_extracted = ocr_result.get('result') == 'TEXT EXTRACTED'
        
        # Handle force_ocr_even_if_invalid
        if force_ocr_even_if_invalid and not critical_passed:
            logger.info("Forcing OCR derived file creation despite invalid result", extra={
                "file_hash": file_hash,
                "critical_passed": critical_passed
            })
            
            # If OCR hasn't been run with derived generation, run it again
            if generate_derived=='false' and ocr_result.get('result') == 'TEXT EXTRACTED':
                print('entered')
                logger.info("Re-running OCR with derived file generation", extra={"file_hash": file_hash})
                # ocr_result_with_derived = perform_ocr(filepath, True, file_hash)
                results['ocr'] = ocr_result_with_derived
                
    # STEP 5: Determine final validity
    # File is valid if:
    # 1. All critical checks passed AND OCR extracted text, OR
    # 2. All critical checks passed (regardless of OCR if OCR not requested), OR
    # 3. OCR extracted text and no critical checks were requested
    if 'ocr' in checks:
        valid = critical_passed and has_text_extracted
    else:
        valid = critical_passed
    
    # Save metadata and check results
    # generate_derived = request.form.get('generate_derived')
    # on_critical_failure_continue = request.form.get('on_critical_failure_continue')
    # force_ocr_even_if_invalid = request.form.get('force_ocr_even_if_invalid') 
    file_id = save_file_metadata(filename, file_hash, valid,generate_derived,on_critical_failure_continue,force_ocr_even_if_invalid)

    for check, result in results.items():
        save_check_to_db(file_id, check, result['result'], result.get('error'))

    # STEP 6: Handle derived file creation based on conditions
    derived_file_created = False
    derived_file_path = None
    
    if 'ocr' in results:
        print('entered in this loop')
        ocr_check_result = results['ocr']
        should_create_derived = False
        
        # Conditions for creating derived file:
        # 1. generate_derived=true AND ocr check passed AND overall result is valid
        # 2. force_ocr_even_if_invalid=true AND ocr check passed (even if overall result is invalid)
        if generate_derived=='true' and ocr_check_result.get('result') == 'TEXT EXTRACTED':
            print('entered first case')
            print('converted:',str(should_create_derived).lower())
            should_create_derived = True
            print('converted1:',str(should_create_derived).lower())
        elif generate_derived=='false' and ocr_check_result.get('result') == 'TEXT EXTRACTED':
            print('entered second case')
            should_create_derived = False
        if generate_derived=='true' and ocr_check_result.get('result') == 'FAILED':
            print('entered third case')
            should_create_derived = False
        elif generate_derived=='false' and ocr_check_result.get('result') == 'FAILED':
            print('entered fourth case')
            should_create_derived = False
        elif force_ocr_even_if_invalid=='true' and ocr_check_result.get('result')=="FAILED":
            print('entered fifth case')
            should_create_derived = False
        elif force_ocr_even_if_invalid=='false' and ocr_check_result.get('result')=="FAILED":
            print('entered sixth case')
            should_create_derived = False
        elif force_ocr_even_if_invalid=='true' and ocr_check_result.get('result')=="TEXT EXTRACTED":
            print('entered seventh case')
            should_create_derived = True
        elif on_critical_failure_continue=='true' and ocr_check_result.get('result')=="FAILED":
            print('entered night case')
            should_create_derived = False
        elif on_critical_failure_continue=='false' and ocr_check_result.get('result')=="FAILED":
            print('entered tenth case')
            should_create_derived = False
        elif on_critical_failure_continue=='true' and ocr_check_result.get('result')=="TEXT EXTRACTED":
            print('entered eleven case')
            should_create_derived = True
        # else:
        #     should_create_derived = False
        print('should_create_derived:',should_create_derived)
        # Create derived file if conditions are met
        if str(should_create_derived).lower() == "true":
            print('entered 893')
            logger.info("Creating derived file based on conditions", extra={
                "file_hash": file_hash,
                "generate_derived": generate_derived,
                "force_ocr_even_if_invalid": force_ocr_even_if_invalid,
                "valid": valid
            })
            
            # Re-run OCR with derived file generation
            ocr_result_with_derived = perform_ocr(filepath, True, file_hash)
            print('ocr_result_with_derived:',ocr_result_with_derived)
            print('ocr_result_with_derived:',ocr_result_with_derived)
            if ocr_result_with_derived.get('result') == 'TEXT EXTRACTED':
                derived_file_path = ocr_result_with_derived.get('result')
                print('derived_file_path:',derived_file_path)
                derived_file_created = derived_file_path is not None
                print('derived_file_created status:',derived_file_created)
                # Update the OCR result to include derived file info
                results['ocr'] = ocr_result_with_derived
            
        logger.info("Derived file handling completed", extra={
            "file_hash": file_hash,
            "derived_created": derived_file_created,
            "generate_derived": generate_derived,
            "force_ocr_even_if_invalid": force_ocr_even_if_invalid,
            "valid": valid,
            "should_create_derived": should_create_derived
        })

    # STEP 7: Create response payload
    response_payload = {
        "@timestamp": datetime.utcnow().isoformat(),
        "filename": filename,
        "file_hash": file_hash,
        "valid": valid,
        "job_id": file_id,
        "checks": results,
        "parameters": {
            "generate_derived": generate_derived,
            "on_critical_failure_continue": on_critical_failure_continue,
            "force_ocr_even_if_invalid": force_ocr_even_if_invalid
        },
        "critical_checks_failed": critical_checks_failed,
        "derived_file_created": derived_file_created,
        # "derived_file_url": f"/derived_outputs/{file_hash}_derived.txt" if derived_file_created else None,
        "derived_file_url": derived_file_path if derived_file_created and derived_file_path else None,
        "conversions": {
            "pdf_created": pdf_path is not None,
            "images_created": len(image_paths),
            "pdf_path": os.path.basename(pdf_path) if pdf_path else None,
            "image_files": [os.path.basename(img) for img in image_paths] if image_paths else []
        }
    }

    # Save JSON response
    with open(os.path.join(JSON_FOLDER, f"{file_hash}_results.json"), 'w') as f:
        json.dump(response_payload, f, indent=2)

    logger.info("Document validation completed", extra={
        "file_hash": file_hash, 
        "job_id": file_id, 
        "valid": valid,
        "checks_performed": list(results.keys()),
        "critical_checks_failed": critical_checks_failed,
        "pdf_converted": pdf_path is not None,
        "images_created": len(image_paths),
        "derived_file_created": derived_file_created,
        "client_ip": client_ip
    })

    return jsonify(response_payload)



@app.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested")
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})

if __name__ == '__main__':
    logger.info("Flask application starting", extra={"port": 5001, "debug": True})
    # logger.addHandler(LogstashTCPHandler(host='logstash', port=5959))
    app.run(debug=True, port=5001)