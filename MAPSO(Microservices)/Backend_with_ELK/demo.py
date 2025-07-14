# import msoffcrypto

# def check_docx_protection(filepath):
#     try:
#         with open(filepath, "rb") as f:
#             office_file = msoffcrypto.OfficeFile(f)
#             office_file.load_key(password=None)
#             office_file.decrypt(None)  # Raises an exception if encrypted
#             return "UNPROTECTED"
#     except Exception as e:
#         return "PROTECTED"

# # 👉 Test with your actual file
# if __name__ == "__main__":
#     filepath = r"C:\Users\koush\Desktop\Analista Projects\Micro Services\Docker with ELK\Samples\Macros\macros_with_password.docx"  # Update with your file path
#     result = check_docx_protection(filepath)
#     print(f"File: {filepath} is {result}")



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # best of all time
FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive

# Clean and update apt sources
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update --allow-releaseinfo-change --fix-missing

# Install system dependencies
RUN apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg \
    ca-certificates \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    tesseract-ocr \
    exiftool \
    libreoffice \
    libreoffice-core \
    libreoffice-writer \
    libreoffice-common \
    libreoffice-java-common \
    default-jre-headless \
    fonts-dejavu-core \
    fonts-dejavu-extra
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Clone Didier Stevens Suite (contains pdfid.py)

EXPOSE 5001
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]



