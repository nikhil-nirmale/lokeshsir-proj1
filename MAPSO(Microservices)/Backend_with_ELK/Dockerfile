# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # best of all time
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
    default-jre \
    libreoffice-java-common \
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










# # # # # # # # # # # # # # # # # # # # # # # # # # # best of all time
# # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # Clean and update apt sources
# # # # # # # # # # # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # # # # # # # Install system dependencies
# # # # # # # # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra
# # # # # # # # # # # # # # # # # # # # RUN apt-get clean && git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect \
# # # # # # # # # # # # # # # # # # # #  && cd /opt/stegdetect && make && cp stegdetect /usr/local/bin \&& gem install zsteg && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # Clone Didier Stevens Suite (contains pdfid.py)

# # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]










# # # # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-bullseye

# # # # # # # # # # # # # # # # # # # # # # # # # # # Avoid interactive prompts
# # # # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # # # Clean cache and install system packages
# # # # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # #         git \
# # # # # # # # # # # # # # # # # # # # # # # # # #         build-essential \
# # # # # # # # # # # # # # # # # # # # # # # # # #         curl \
# # # # # # # # # # # # # # # # # # # # # # # # # #         gnupg \
# # # # # # # # # # # # # # # # # # # # # # # # # #         ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # # # #         tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # # # #         exiftool \
# # # # # # # # # # # # # # # # # # # # # # # # # #         libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # # # Optional: Clone Didier Stevens Suite for PDF tools (if needed)
# # # # # # # # # # # # # # # # # # # # # # # # # # RUN git clone https://github.com/DidierStevens/DidierStevensSuite.git /opt/DidierStevensSuite

# # # # # # # # # # # # # # # # # # # # # # # # # # # Set working directory
# # # # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # Copy all project files into container
# # # # # # # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # # # Expose Flask port
# # # # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001

# # # # # # # # # # # # # # # # # # # # # # # # # # # Run Flask app
# # # # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # good
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Clean, update, and retry logic
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get update && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         build-essential \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         curl \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         gnupg \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         exiftool \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-extra || apt-get install -f && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/*
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Final cleanup
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # Combine apt-get update + install in one layer
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # Replace the mirror with a stable one
# # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN sed -i 's|http://deb.debian.org|http://deb.debian.org|g' /etc/apt/sources.list && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         build-essential \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         curl \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         gnupg \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         exiftool \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]





# # # # # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # # # # Add dependencies separately to isolate issues
# # # # # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     ca-certificates && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libgl1 && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     exiftool && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     libreoffice || echo "⚠️ LibreOffice failed to install – continuing..." && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]







# # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # Step 1: Install system packages
# # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && \
# # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra \
# # # # # # # # # # # # # # # # # # # # # # # #     && gem install zsteg \
# # # # # # # # # # # # # # # # # # # # # # # #     && git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect \
# # # # # # # # # # # # # # # # # # # # # # # #     && cd /opt/stegdetect && make && cp stegdetect /usr/local/bin \
# # # # # # # # # # # # # # # # # # # # # # # #     && apt-get clean \
# # # # # # # # # # # # # # # # # # # # # # # #     && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # Step 2: Install Python packages
# # # # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # Step 3: Copy your app code
# # # # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

# # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # System & forensic tools
# # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && \
# # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # # # # # # # # # #     git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect && \
# # # # # # # # # # # # # # # # # # # # # # # #     cd /opt/stegdetect && make && cp stegdetect /usr/local/bin && \
# # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # Python dependencies
# # # # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # Copy app
# # # # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9

# # # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # # Step 1: Install system & stego tools
# # # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && \
# # # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # # #     libgl1-mesa-glx \
# # # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # # # # # # # # # #     git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect && \
# # # # # # # # # # # # # # # # # # # # # # # #     cd /opt/stegdetect && make && cp stegdetect /usr/local/bin && \
# # # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # # Step 2: Python dependencies
# # # # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # # Step 3: App code
# # # # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]

# # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9

# # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # STEP 1: Base tools
# # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # #     libgl1-mesa-glx \
# # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # STEP 2: Install LibreOffice separately (sometimes fails if bundled)
# # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && apt-get install -y libreoffice || echo "LibreOffice install failed but continuing"

# # # # # # # # # # # # # # # # # # # # # # # # STEP 3: Install zsteg + stegdetect
# # # # # # # # # # # # # # # # # # # # # # # RUN gem install zsteg && \
# # # # # # # # # # # # # # # # # # # # # # #     git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect && \
# # # # # # # # # # # # # # # # # # # # # # #     cd /opt/stegdetect && make || echo "stegdetect build failed" && \
# # # # # # # # # # # # # # # # # # # # # # #     cp /opt/stegdetect/stegdetect /usr/local/bin || echo "stegdetect not copied"

# # # # # # # # # # # # # # # # # # # # # # # # STEP 4: Python packages
# # # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # STEP 5: App setup
# # # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]





# # # # # # # # # # # # # # # # # # # # # # # FROM python:3.9

# # # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # # STEP 1: Safe APT Update & Install
# # # # # # # # # # # # # # # # # # # # # # # RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # # # #     libgl1-mesa-glx \
# # # # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # # STEP 2: Optional LibreOffice (can skip if failing)
# # # # # # # # # # # # # # # # # # # # # # # RUN apt-get update --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # # #     apt-get install -y libreoffice || echo "LibreOffice install failed, continuing..."

# # # # # # # # # # # # # # # # # # # # # # # # STEP 3: zsteg and stegdetect
# # # # # # # # # # # # # # # # # # # # # # # RUN gem install zsteg && \
# # # # # # # # # # # # # # # # # # # # # # #     git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect && \
# # # # # # # # # # # # # # # # # # # # # # #     cd /opt/stegdetect && make && cp stegdetect /usr/local/bin || echo "stegdetect build failed"

# # # # # # # # # # # # # # # # # # # # # # # # STEP 4: Python dependencies
# # # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # # STEP 5: App setup
# # # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]













# # # # # # # # # # # # # # # # # # # # # # FROM python:3.9

# # # # # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # # # # Use stable Debian mirror
# # # # # # # # # # # # # # # # # # # # # # RUN sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' /etc/apt/sources.list

# # # # # # # # # # # # # # # # # # # # # # # Step 1: Install system dependencies
# # # # # # # # # # # # # # # # # # # # # # RUN apt-get clean && rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # # #         build-essential \
# # # # # # # # # # # # # # # # # # # # # #         ruby \
# # # # # # # # # # # # # # # # # # # # # #         ruby-dev \
# # # # # # # # # # # # # # # # # # # # # #         curl \
# # # # # # # # # # # # # # # # # # # # # #         git \
# # # # # # # # # # # # # # # # # # # # # #         gnupg \
# # # # # # # # # # # # # # # # # # # # # #         ca-certificates \
# # # # # # # # # # # # # # # # # # # # # #         make \
# # # # # # # # # # # # # # # # # # # # # #         libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # # #         libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # # #         libsm6 \
# # # # # # # # # # # # # # # # # # # # # #         libxrender1 \
# # # # # # # # # # # # # # # # # # # # # #         libxext6 \
# # # # # # # # # # # # # # # # # # # # # #         libgl1-mesa-glx \
# # # # # # # # # # # # # # # # # # # # # #         tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # # #         exiftool \
# # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # # #         fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # # Step 2: Optional LibreOffice install (retry-safe)
# # # # # # # # # # # # # # # # # # # # # # RUN apt-get update && \
# # # # # # # # # # # # # # # # # # # # # #     apt-get install -y libreoffice || echo "LibreOffice install failed"

# # # # # # # # # # # # # # # # # # # # # # # Step 3: Install zsteg and stegdetect
# # # # # # # # # # # # # # # # # # # # # # RUN gem install zsteg && \
# # # # # # # # # # # # # # # # # # # # # #     git clone https://github.com/abeluck/stegdetect.git /opt/stegdetect && \
# # # # # # # # # # # # # # # # # # # # # #     cd /opt/stegdetect && make && cp stegdetect /usr/local/bin || echo "stegdetect build failed"

# # # # # # # # # # # # # # # # # # # # # # # Step 4: Python packages
# # # # # # # # # # # # # # # # # # # # # # COPY requirements.txt .
# # # # # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # # Step 5: App code
# # # # # # # # # # # # # # # # # # # # # # COPY . /app
# # # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # # # # # # # # # # # # FROM python:3.9

# # # # # # # # # # # # # # # # # # # # # # Set environment variables
# # # # # # # # # # # # # # # # # # # # # ENV PYTHONDONTWRITEBYTECODE=1
# # # # # # # # # # # # # # # # # # # # # ENV PYTHONUNBUFFERED=1

# # # # # # # # # # # # # # # # # # # # # # Update package sources (safe mirror replacement if required)
# # # # # # # # # # # # # # # # # # # # # RUN grep -lr "deb.debian.org" /etc/apt/ | xargs sed -i 's|http://deb.debian.org/debian|http://ftp.us.debian.org/debian|g' || true

# # # # # # # # # # # # # # # # # # # # # # System dependencies
# # # # # # # # # # # # # # # # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # # # #     ruby-dev \
# # # # # # # # # # # # # # # # # # # # #     rake \
# # # # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # # # # # # # # #     libjpeg-dev \
# # # # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # # # #     libgl1-mesa-glx \
# # # # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # # # #     tesseract-ocr-eng \
# # # # # # # # # # # # # # # # # # # # #     tesseract-ocr-osd \
# # # # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # # # # Install zsteg (via RubyGem)
# # # # # # # # # # # # # # # # # # # # # RUN gem install zsteg

# # # # # # # # # # # # # # # # # # # # # # Create app directory
# # # # # # # # # # # # # # # # # # # # # WORKDIR /app

# # # # # # # # # # # # # # # # # # # # # # Copy project files
# # # # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # # # # RUN pip install --upgrade pip
# # # # # # # # # # # # # # # # # # # # # RUN pip install -r requirements.txt

# # # # # # # # # # # # # # # # # # # # # # Expose port (update as needed)
# # # # # # # # # # # # # # # # # # # # # EXPOSE 5000

# # # # # # # # # # # # # # # # # # # # # # Run your Flask app (update if different)
# # # # # # # # # # # # # # # # # # # # # CMD ["python", "app.py"]







# # # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # # Clean and update apt sources
# # # # # # # # # # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # # # # # # Install system dependencies including stegdetect and zsteg
# # # # # # # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # # #     stegdetect \
# # # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # # # Clone Didier Stevens Suite (contains pdfid.py)

# # # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]









# # # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # # Clean and update apt sources
# # # # # # # # # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # # # # # Install dependencies for Python + OCR + zsteg + stegdetect
# # # # # # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # # #     automake \
# # # # # # # # # # # # # # # # # #     autoconf \
# # # # # # # # # # # # # # # # # #     libtool \
# # # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # # Build stegdetect from source
# # # # # # # # # # # # # # # # # # RUN git clone https://github.com/abeluck/stegdetect.git && \
# # # # # # # # # # # # # # # # # #     cd stegdetect && \
# # # # # # # # # # # # # # # # # #     ./configure && \
# # # # # # # # # # # # # # # # # #     make && \
# # # # # # # # # # # # # # # # # #     make install && \
# # # # # # # # # # # # # # # # # #     cd .. && rm -rf stegdetect

# # # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # # Configure APT to retry downloads and fix common issues
# # # # # # # # # # # # # # # # # RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80-retries && \
# # # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # # # # Install system dependencies including stegdetect and zsteg
# # # # # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # # #     automake \
# # # # # # # # # # # # # # # # #     autoconf \
# # # # # # # # # # # # # # # # #     libtool \
# # # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # (Optional) Install LibreOffice separately to reduce risk of hash mismatch
# # # # # # # # # # # # # # # # # # Enable this block if LibreOffice is required
# # # # # # # # # # # # # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends libreoffice && \
# # # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # # Build stegdetect from source
# # # # # # # # # # # # # # # # # RUN git clone https://github.com/abeluck/stegdetect.git && \
# # # # # # # # # # # # # # # # #     cd stegdetect && \
# # # # # # # # # # # # # # # # #     ./configure && \
# # # # # # # # # # # # # # # # #     make && \
# # # # # # # # # # # # # # # # #     make install && \
# # # # # # # # # # # # # # # # #     cd .. && rm -rf stegdetect

# # # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # # # Configure APT to retry downloads and fix common issues
# # # # # # # # # # # # # # # # RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80-retries && \
# # # # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # # # Install system dependencies (including for stegdetect and zsteg)
# # # # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # # # #     gcc \
# # # # # # # # # # # # # # # #     g++ \
# # # # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # # # #     automake \
# # # # # # # # # # # # # # # #     autoconf \
# # # # # # # # # # # # # # # #     libtool \
# # # # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # (Optional) Install LibreOffice separately to reduce mirror failure
# # # # # # # # # # # # # # # # # RUN apt-get update && \
# # # # # # # # # # # # # # # # #     apt-get install -y --no-install-recommends libreoffice && \
# # # # # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # # # Build stegdetect from source
# # # # # # # # # # # # # # # # RUN git clone https://github.com/abeluck/stegdetect.git && \
# # # # # # # # # # # # # # # #     cd stegdetect && \
# # # # # # # # # # # # # # # #     ./configure && \
# # # # # # # # # # # # # # # #     make && \
# # # # # # # # # # # # # # # #     make install && \
# # # # # # # # # # # # # # # #     cd .. && rm -rf stegdetect

# # # # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]







# # # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # # Add retry config and update
# # # # # # # # # # # # # # RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80-retries && \
# # # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # # Install system + build tools including GCC + libc
# # # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # # #     gcc \
# # # # # # # # # # # # # #     g++ \
# # # # # # # # # # # # # #     make \
# # # # # # # # # # # # # #     libc6-dev \
# # # # # # # # # # # # # #     curl \
# # # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # # #     git \
# # # # # # # # # # # # # #     automake \
# # # # # # # # # # # # # #     autoconf \
# # # # # # # # # # # # # #     libtool \
# # # # # # # # # # # # # #     pkg-config \
# # # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # # Build stegdetect from source
# # # # # # # # # # # # # # RUN git clone https://github.com/abeluck/stegdetect.git && \
# # # # # # # # # # # # # #     cd stegdetect && \
# # # # # # # # # # # # # #     autoreconf -fvi && \
# # # # # # # # # # # # # #     ./configure && \
# # # # # # # # # # # # # #     make && \
# # # # # # # # # # # # # #     make install && \
# # # # # # # # # # # # # #     cd .. && rm -rf stegdetect

# # # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # # Configure APT to retry and fix missing packages
# # # # # # # # # # # # # RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80-retries && \
# # # # # # # # # # # # #     apt-get clean && \
# # # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # # Install required system tools
# # # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # # #     build-essential \
# # # # # # # # # # # # #     gcc \
# # # # # # # # # # # # #     g++ \
# # # # # # # # # # # # #     make \
# # # # # # # # # # # # #     libc6-dev \
# # # # # # # # # # # # #     curl \
# # # # # # # # # # # # #     gnupg \
# # # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # # #     ruby \
# # # # # # # # # # # # #     git \
# # # # # # # # # # # # #     automake \
# # # # # # # # # # # # #     autoconf \
# # # # # # # # # # # # #     libtool \
# # # # # # # # # # # # #     pkg-config \
# # # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # # #     exiftool \
# # # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # # #     fonts-dejavu-extra && \
# # # # # # # # # # # # #     gem install zsteg && \
# # # # # # # # # # # # #     apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # # # Build stegdetect from source
# # # # # # # # # # # # # RUN git clone https://github.com/abeluck/stegdetect.git && \
# # # # # # # # # # # # #     cd stegdetect && \
# # # # # # # # # # # # #     autoreconf -fvi && \
# # # # # # # # # # # # #     ./configure && \
# # # # # # # # # # # # #     make && \
# # # # # # # # # # # # #     make install && \
# # # # # # # # # # # # #     cd .. && rm -rf stegdetect

# # # # # # # # # # # # # # Set working directory
# # # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # # Set Flask entry point (app1.py)
# # # # # # # # # # # # # ENV FLASK_APP=app1.py

# # # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]




# # # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # # Clean and update apt sources
# # # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # # Install system dependencies
# # # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # # #     build-essential \
# # # # # # # # # # # #     curl \
# # # # # # # # # # # #     gnupg \
# # # # # # # # # # # #     ca-certificates \
# # # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # # #     libsm6 \
# # # # # # # # # # # #     libxrender1 \
# # # # # # # # # # # #     libxext6 \
# # # # # # # # # # # #     libgl1 \
# # # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # # #     exiftool \
# # # # # # # # # # # #     libreoffice \
# # # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # # #     fonts-dejavu-extra
# # # # # # # # # # # # RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # # COPY . /app

# # # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # # # Clone Didier Stevens Suite (contains pdfid.py)

# # # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]






# # # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # # Clean and update apt sources
# # # # # # # # # # # RUN apt-get clean && \
# # # # # # # # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # # # # # # # #     apt-get update --allow-releaseinfo-change --fix-missing

# # # # # # # # # # # # Install dependencies
# # # # # # # # # # # RUN apt-get install -y --no-install-recommends \
# # # # # # # # # # #     build-essential \
# # # # # # # # # # #     curl \
# # # # # # # # # # #     gnupg \
# # # # # # # # # # #     ca-certificates \
# # # # # # # # # # #     libglib2.0-0 \
# # # # # # # # # # #     libsm6 \
# # # # # # # # # # #     libxrender1 \
# # # # # # # # # # #     libxext6 \
# # # # # # # # # # #     libgl1 \
# # # # # # # # # # #     tesseract-ocr \
# # # # # # # # # # #     exiftool \
# # # # # # # # # # #     libreoffice \
# # # # # # # # # # #     fonts-dejavu-core \
# # # # # # # # # # #     fonts-dejavu-extra \
# # # # # # # # # # #     wget \
# # # # # # # # # # #     libpcap-dev \
# # # # # # # # # # #     libjpeg62-turbo-dev \
# # # # # # # # # # #     unzip

# # # # # # # # # # # # Install stegdetect
# # # # # # # # # # # RUN curl -L -o stegdetect.zip https://github.com/zed-0xff/stegdetect/archive/refs/heads/master.zip && \
# # # # # # # # # # #     unzip stegdetect.zip && \
# # # # # # # # # # #     cd stegdetect-master && \
# # # # # # # # # # #     make && \
# # # # # # # # # # #     cp stegdetect /usr/local/bin/stegdetect && \
# # # # # # # # # # #     cd .. && rm -rf stegdetect-master stegdetect.zip

# # # # # # # # # # # # Cleanup to reduce image size
# # # # # # # # # # # RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # WORKDIR /app
# # # # # # # # # # # COPY . /app

# # # # # # # # # # # # Install Python dependencies
# # # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # # EXPOSE 5001
# # # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
# # # # # # # # # # FROM python:3.9-slim

# # # # # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # # # # Update and install dependencies
# # # # # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # # # # #         build-essential \
# # # # # # # # # #         curl \
# # # # # # # # # #         gnupg \
# # # # # # # # # #         ca-certificates \
# # # # # # # # # #         libglib2.0-0 \
# # # # # # # # # #         libsm6 \
# # # # # # # # # #         libxrender1 \
# # # # # # # # # #         libxext6 \
# # # # # # # # # #         libgl1 \
# # # # # # # # # #         tesseract-ocr \
# # # # # # # # # #         exiftool \
# # # # # # # # # #         libreoffice \
# # # # # # # # # #         fonts-dejavu-core \
# # # # # # # # # #         fonts-dejavu-extra \
# # # # # # # # # #         wget \
# # # # # # # # # #         libpcap-dev \
# # # # # # # # # #         libjpeg-dev \
# # # # # # # # # #         unzip \
# # # # # # # # # #     && apt-get clean && rm -rf /var/lib/apt/lists/*

# # # # # # # # # # # Install stegdetect (from GitHub fork that builds on modern systems)
# # # # # # # # # # RUN curl -L -o stegdetect.zip https://github.com/zed-0xff/stegdetect/archive/refs/heads/master.zip && \
# # # # # # # # # #     unzip stegdetect.zip && \
# # # # # # # # # #     cd stegdetect-master && \
# # # # # # # # # #     make && \
# # # # # # # # # #     cp stegdetect /usr/local/bin/stegdetect && \
# # # # # # # # # #     cd .. && rm -rf stegdetect-master stegdetect.zip

# # # # # # # # # # WORKDIR /app
# # # # # # # # # # COPY . /app

# # # # # # # # # # # Install Python dependencies
# # # # # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # # # # EXPOSE 5001
# # # # # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]












# # # # # # # FROM python:3.9-slim

# # # # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # # # # Refresh and fix any stale cache
# # # # # # # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # # # #     apt-get install -y --no-install-recommends \
# # # # # # #         build-essential \
# # # # # # #         curl \
# # # # # # #         gnupg \
# # # # # # #         ca-certificates \
# # # # # # #         libglib2.0-0 \
# # # # # # #         libsm6 \
# # # # # # #         libxrender1 \
# # # # # # #         libxext6 \
# # # # # # #         libgl1 \
# # # # # # #         tesseract-ocr \
# # # # # # #         exiftool \
# # # # # # #         libreoffice \
# # # # # # #         fonts-dejavu-core \
# # # # # # #         fonts-dejavu-extra \
# # # # # # #     && apt-get clean \
# # # # # # #     && rm -rf /var/lib/apt/lists/*

# # # # # # # WORKDIR /app
# # # # # # # COPY . /app

# # # # # # # # Python deps
# # # # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # # # EXPOSE 5001
# # # # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]







# # # # # FROM python:3.9-slim

# # # # # ENV DEBIAN_FRONTEND=noninteractive

# # # # # RUN apt-get clean && \
# # # # #     rm -rf /var/lib/apt/lists/* && \
# # # # #     mkdir -p /var/lib/apt/lists/partial && \
# # # # #     apt-get update --allow-releaseinfo-change --fix-missing && \
# # # # #     apt-get install -y --no-install-recommends \
# # # # #         build-essential \
# # # # #         curl \
# # # # #         gnupg \
# # # # #         ca-certificates \
# # # # #         libglib2.0-0 \
# # # # #         libsm6 \
# # # # #         libxrender1 \
# # # # #         libxext6 \
# # # # #         libgl1 \
# # # # #         tesseract-ocr \
# # # # #         exiftool \
# # # # #         libreoffice \
# # # # #         fonts-dejavu-core \
# # # # #         fonts-dejavu-extra \
# # # # #     && apt-get clean \
# # # # #     && rm -rf /var/lib/apt/lists/*

# # # # # WORKDIR /app
# # # # # COPY . /app

# # # # # RUN pip install --no-cache-dir --upgrade pip && \
# # # # #     pip install --no-cache-dir -r requirements.txt

# # # # # EXPOSE 5001

# # # # # CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]




# # # # # # next better one
# FROM python:3.9.18-slim-bullseye

# ENV DEBIAN_FRONTEND=noninteractive

# # Update and install system dependencies in one go
# # RUN apt-get update --allow-releaseinfo-change --fix-missing && \
# #     apt-get install -y --no-install-recommends \
# #         build-essential \
# #         curl \
# #         gnupg \
# #         ca-certificates \
# #         libglib2.0-0 \
# #         libsm6 \
# #         libxrender1 \
# #         libxext6 \
# #         libgl1 \
# #         tesseract-ocr \
# #         exiftool \
# #         libreoffice-writer \
# #         libreoffice-core \
# #         libreoffice-common \
# #         fonts-dejavu-core \
# #         fonts-dejavu-extra && \
# #     apt-get clean && rm -rf /var/lib/apt/lists/*
# RUN apt-get update --allow-releaseinfo-change --fix-missing && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         curl \
#         gnupg \
#         ca-certificates \
#         libglib2.0-0 \
#         libsm6 \
#         libxrender1 \
#         libxext6 \
#         libgl1 \
#         tesseract-ocr \
#         exiftool \
#         libreoffice-writer \
#         libreoffice-core \
#         libreoffice-common \
#         libreoffice-java-common \
#         openjdk-11-jre-headless \  
#         fonts-dejavu-core \
#         fonts-dejavu-extra && \
#     apt-get clean && rm -rf /var/lib/apt/lists/*


# # Set working directory
# WORKDIR /app

# # Copy all project files
# COPY . /app

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # Expose port for Flask app
# EXPOSE 5001

# # Start the Flask application
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
