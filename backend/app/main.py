from fastapi import FastAPI, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
import os
import logging

from app.routers import pdf_parser, voice_agent, websocket_handler
from app.database import USE_DATABASE

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Zain Bahrain AI Voice Agent",
    description="AI-powered voice agent for order processing",
    version="1.0.0"
)

# CORS middleware
# Get allowed origins from environment or use defaults
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,https://zain-ai-voice-agent.onrender.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(pdf_parser.router, prefix="/api", tags=["PDF"])
app.include_router(voice_agent.router, prefix="/api", tags=["Voice Agent"])
app.include_router(websocket_handler.router, prefix="/ws", tags=["WebSocket"])

@app.get("/")
async def root():
    return {
        "message": "Zain Bahrain AI Voice Agent API", 
        "status": "running",
        "database_enabled": USE_DATABASE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database_enabled": USE_DATABASE
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("APP_ENV", "development") == "development"
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=reload)
