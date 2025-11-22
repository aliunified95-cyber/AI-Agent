from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from app.services.ai_agent import ZainVoiceAgent
from app.database import get_db, USE_DATABASE
from app.db_service import DatabaseService
from sqlalchemy.orm import Session

router = APIRouter()

# Store active sessions in memory (for quick access)
active_sessions: Dict[str, ZainVoiceAgent] = {}

class StartCallRequest(BaseModel):
    order_data: Dict[str, Any]

@router.post("/start-call")
async def start_call(request: StartCallRequest):
    """
    Initialize voice agent for specific order
    """
    try:
        db_service = None
        order_id = request.order_data.get("order_id", f"ORDER-{uuid.uuid4().hex[:8]}")
        session_id = str(uuid.uuid4())
        
        # Use database if available
        if USE_DATABASE:
            try:
                from app.database import SessionLocal
                if SessionLocal:
                    db = SessionLocal()
                    try:
                        db_service = DatabaseService(db)
                        # Create or get order in database
                        order = db_service.create_order(request.order_data)
                        order_id = order.order_id
                        
                        # Create session
                        db_session = db_service.create_session(order.id, session_id)
                    finally:
                        db.close()
            except Exception as db_error:
                print(f"Database error (continuing without DB): {db_error}")
        
        # Create agent instance
        agent = ZainVoiceAgent(request.order_data, session_id, db_service)
        active_sessions[session_id] = agent
        
        return {
            "session_id": session_id,
            "order_id": order_id,
            "status": "started",
            "message": "Call session initialized",
            "database_enabled": USE_DATABASE
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting call: {str(e)}")

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    Get session information
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    agent = active_sessions[session_id]
    return {
        "session_id": session_id,
        "state": agent.state.value,
        "language": agent.language,
        "customer_authenticated": agent.customer_authenticated,
        "order_confirmed": agent.order_confirmed
    }

@router.post("/session/{session_id}/process")
async def process_message(session_id: str, message: Dict[str, str]):
    """
    Process text message from user
    """
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    agent = active_sessions[session_id]
    user_input = message.get("text", "")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Message text is required")
    
    try:
        response = await agent.process_input(user_input)
        return {
            "response": response,
            "state": agent.state.value,
            "conversation_history": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "state": msg.state,
                    "timestamp": msg.timestamp
                }
                for msg in agent.conversation_history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.delete("/session/{session_id}")
async def end_call(session_id: str):
    """
    End call session
    """
    # End session in database if available
    if USE_DATABASE:
        try:
            from app.database import SessionLocal
            if SessionLocal:
                db = SessionLocal()
                try:
                    db_service = DatabaseService(db)
                    db_session = db_service.end_session(session_id)
                finally:
                    db.close()
        except Exception as e:
            print(f"Database error ending session: {e}")
    
    # Remove from active sessions
    if session_id in active_sessions:
        del active_sessions[session_id]
        return {"status": "ended", "message": "Call session ended"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

