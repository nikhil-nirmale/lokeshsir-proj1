🚀 MAPSO Microservice Deployment (Docker + Docker Compose)
📁 Project Structure (Simplified)
bash
Copy
Edit
mapso-microservice/
├── app/                    # FastAPI app code
├── tests/                 # Test files
├── Dockerfile             # Image build instructions
├── docker-compose.yml     # Multi-container config
├── requirements.txt       # Python dependencies
├── README.md
└── temp_files/            # Runtime file storage
🐳 1. Dockerfile (Single Container Build)
This builds a lightweight Python environment, installs dependencies, and runs FastAPI.

Dockerfile
Copy
Edit
FROM python:3.9-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/temp_files

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
✅ What it does:

Sets Python 3.9 as base.

Installs dependencies.

Copies app code into container.

Creates a runtime folder temp_files.

Starts the FastAPI server with uvicorn.

🧩 2. docker-compose.yml (Multi-Container Runtime)
yaml
Copy
Edit
version: "3.8"

services:
  mapso:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - .:/app
      - ./temp_files:/app/temp_files
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
      - PYTHONPATH=/app
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
✅ What it does:

Builds the app container using the Dockerfile.

Maps port 8001 (host) to 8001 (container).

Mounts project files into the container for live updates (--reload).

Passes necessary environment variables.

⚙️ 3. How to Deploy (Commands)
bash
Copy
Edit
# 1. Build and run the container(s)
docker-compose up --build

# 2. Access API Docs
http://localhost:8001/docs
🌐 Notes for Cloud/VPS (like GCP VM)
Ensure port 8001 is open in firewall rules.

You may use curl, Postman, or browser to test endpoints.

For production, remove --reload and set LOG_LEVEL=info.

✅ Summary
Component	Purpose
Dockerfile	Builds image for FastAPI app
docker-compose.yml	Runs app with configuration
docker-compose up	Builds & launches the container
localhost:8001	Default port for app access
