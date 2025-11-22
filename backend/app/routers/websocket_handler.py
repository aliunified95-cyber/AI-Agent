from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState
import json
import logging
import base64
from app.services.ai_agent import ZainVoiceAgent
from app.models.agent import AgentState
from app.services.voice_service import text_to_speech, speech_to_text

logger = logging.getLogger(__name__)

router = APIRouter()

# Store active WebSocket sessions
active_ws_sessions: dict = {}

@router.websocket("/voice/{session_id}")
async def voice_websocket(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time voice communication
    """
    await websocket.accept()
    
    try:
        # Get or create agent session
        from app.routers.voice_agent import active_sessions
        
        if session_id not in active_sessions:
            await websocket.send_json({
                "type": "error",
                "message": "Session not found. Please start a call first."
            })
            await websocket.close()
            return
        
        agent = active_sessions[session_id]
        active_ws_sessions[session_id] = websocket
        
        # Send initial greeting
        initial_response = agent.handle_init()
        
        # Send text response
        await websocket.send_json({
            "type": "text",
            "message": initial_response,
            "state": agent.state.value
        })
        
        # Generate and send audio
        try:
            audio_data = await text_to_speech(initial_response, agent.language or "en")
            await websocket.send_json({
                "type": "audio",
                "size": len(audio_data)
            })
            await websocket.send_bytes(audio_data)
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
        
        # Main message loop
        while True:
            try:
                # Receive message
                data = await websocket.receive()
                
                if "text" in data:
                    # Text message
                    message_data = json.loads(data["text"])
                    message_type = message_data.get("type")
                    
                    if message_type == "text":
                        user_input = message_data.get("text", "")
                        if user_input:
                            # Process with agent
                            response = await agent.process_input(user_input)
                            
                            # Send text response
                            await websocket.send_json({
                                "type": "text",
                                "message": response,
                                "state": agent.state.value
                            })
                            
                            # Generate and send audio
                            try:
                                audio_data = await text_to_speech(response, agent.language or "en")
                                await websocket.send_json({
                                    "type": "audio",
                                    "size": len(audio_data)
                                })
                                await websocket.send_bytes(audio_data)
                            except Exception as e:
                                logger.error(f"Error generating speech: {e}")
                    
                    elif message_type == "audio":
                        # Audio message (base64 encoded)
                        audio_base64 = message_data.get("audio", "")
                        if audio_base64:
                            # Decode audio
                            audio_bytes = base64.b64decode(audio_base64)
                            
                            # Convert to text
                            try:
                                transcript = await speech_to_text(audio_bytes, agent.language or "en")
                                
                                # Process with agent
                                response = await agent.process_input(transcript)
                                
                                # Send text response
                                await websocket.send_json({
                                    "type": "text",
                                    "message": response,
                                    "transcript": transcript,
                                    "state": agent.state.value
                                })
                                
                                # Generate and send audio
                                try:
                                    audio_data = await text_to_speech(response, agent.language or "en")
                                    await websocket.send_json({
                                        "type": "audio",
                                        "size": len(audio_data)
                                    })
                                    await websocket.send_bytes(audio_data)
                                except Exception as e:
                                    logger.error(f"Error generating speech: {e}")
                            except Exception as e:
                                logger.error(f"Error transcribing audio: {e}")
                                await websocket.send_json({
                                    "type": "error",
                                    "message": "Sorry, I couldn't understand that. Could you repeat?"
                                })
                
                elif "bytes" in data:
                    # Binary audio data
                    audio_bytes = data["bytes"]
                    
                    # Convert to text
                    try:
                        transcript = await speech_to_text(audio_bytes, agent.language or "en")
                        
                        # Process with agent
                        response = await agent.process_input(transcript)
                        
                        # Send text response
                        await websocket.send_json({
                            "type": "text",
                            "message": response,
                            "transcript": transcript,
                            "state": agent.state.value
                        })
                        
                        # Generate and send audio
                        try:
                            audio_data = await text_to_speech(response, agent.language or "en")
                            await websocket.send_json({
                                "type": "audio",
                                "size": len(audio_data)
                            })
                            await websocket.send_bytes(audio_data)
                        except Exception as e:
                            logger.error(f"Error generating speech: {e}")
                    except Exception as e:
                        logger.error(f"Error transcribing audio: {e}")
                        await websocket.send_json({
                            "type": "error",
                            "message": "Sorry, I couldn't understand that. Could you repeat?"
                        })
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for session {session_id}")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket handler: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": "An error occurred. Please try again."
                })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if session_id in active_ws_sessions:
            del active_ws_sessions[session_id]

