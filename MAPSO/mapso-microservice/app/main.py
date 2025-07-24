from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analysis, status
from app.config import settings
import logging

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="Microservice for digital document validation with cybersecurity checks and OCR",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(status.router, prefix="/api/v1", tags=["Status"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting MAPSO Microservice")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Temp file directory: {settings.temp_file_dir}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down MAPSO Microservice")