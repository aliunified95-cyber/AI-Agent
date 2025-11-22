import os
import requests
from elevenlabs import ElevenLabs
from openai import OpenAI
import base64
import io

# Set API keys
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

async def text_to_speech(text: str, language: str = "en") -> bytes:
    """
    Convert text to speech using ElevenLabs API
    """
    try:
        if not elevenlabs_client:
            raise Exception("ElevenLabs API key not configured")
        
        # Generate audio using new API
        audio_generator = elevenlabs_client.text_to_speech.convert(
            voice_id=ELEVENLABS_VOICE_ID,
            text=text,
            model_id="eleven_multilingual_v2"  # Supports Arabic
        )
        
        # Collect all audio chunks
        audio_bytes = b""
        for chunk in audio_generator:
            audio_bytes += chunk
        
        return audio_bytes
    except Exception as e:
        raise Exception(f"Error generating speech: {str(e)}")

async def speech_to_text(audio_data: bytes, language: str = "en") -> str:
    """
    Convert speech to text using OpenAI Whisper (cheapest option)
    """
    try:
        # Create a file-like object from bytes
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.webm"
        
        # Transcribe using Whisper
        transcript = openai_client.audio.transcriptions.create(
            model="whisper-1",  # Cheapest OpenAI model for STT
            file=audio_file,
            language="ar" if language == "ar" else "en"
        )
        
        return transcript.text
    except Exception as e:
        raise Exception(f"Error transcribing speech: {str(e)}")

