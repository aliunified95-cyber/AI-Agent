# Zain Bahrain AI Voice Agent

A professional AI-powered voice agent system for processing customer orders from Zain Bahrain's digital store. The system handles order confirmation, modifications, eligibility checks, and customer interactions through natural voice conversations in both Arabic (Bahraini dialect) and English.

🌐 **Live Demo**: https://zain-ai-voice-agent.onrender.com

## Features

- 📄 **PDF Order Parsing** - Automatically extract order data from PDF summary forms
- 🎤 **Voice Interface** - Real-time speech-to-text and text-to-speech
- 🤖 **AI Agent** - Intelligent conversation handling with state machine
- 🌐 **Bilingual Support** - Arabic (Bahraini dialect) and English
- 💬 **WebSocket Communication** - Real-time bidirectional communication
- 🎨 **Modern UI** - Professional, responsive React interface

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **Claude API** (claude-3-haiku) - AI conversation handling
- **OpenAI Whisper** - Speech-to-text
- **ElevenLabs** - Text-to-speech
- **pdfplumber** - PDF parsing

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **WebSocket** - Real-time communication

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. The `.env` file is already configured with your API keys. If you need to modify it, copy `.env.example` to `.env` and update the values.

5. Run the server:
```bash
python -m app.main
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. **Upload Order PDF**: Click "Browse Files" or drag and drop a PDF order summary
2. **Review Order**: Check the parsed order details in the left panel
3. **Start Call**: Click "Start Call" to begin the voice agent session
4. **Interact**: 
   - Use the microphone button to speak
   - Or type messages in the text input
5. **End Call**: Click "End Call" when finished

## API Endpoints

### PDF Parsing
- `POST /api/parse-order` - Upload and parse PDF order

### Voice Agent
- `POST /api/start-call` - Initialize a new call session
- `GET /api/session/{session_id}` - Get session information
- `POST /api/session/{session_id}/process` - Process text message
- `DELETE /api/session/{session_id}` - End call session

### WebSocket
- `WS /ws/voice/{session_id}` - Real-time voice communication

## Conversation Flow

The agent follows a state machine with these states:

1. **INIT** - Call initiated
2. **LANGUAGE_SELECT** - Language preference
3. **AUTH** - Name and CPR verification
4. **OWNERSHIP_CHECK** - Verify caller is order owner
5. **ORDER_CONFIRM** - Read back order details
6. **MODIFICATION** - Handle order changes
7. **ELIGIBILITY_CHECK** - Credit control validation
8. **COMMITMENT_APPROVAL** - Handle approval if needed
9. **CROSS_SELL** - Offer accessories
10. **EKYC_SEND** - Send digital signing link
11. **CLOSE** - End call

## Configuration

API keys are configured in `backend/.env`:
- `CLAUDE_API_KEY` - Anthropic Claude API key
- `ELEVENLABS_API_KEY` - ElevenLabs API key
- `ELEVENLABS_VOICE_ID` - ElevenLabs voice ID
- `OPENAI_API_KEY` - OpenAI API key (for Whisper STT)

## Notes

- The system uses the cheapest models:
  - Claude: `claude-3-haiku-20240307`
  - OpenAI: `whisper-1` for STT
- The voice agent speaks in Bahraini Gulf dialect for Arabic
- All financial details are read exactly as shown in the system
- Device changes require new orders (current order must be cancelled)
- Plan changes are allowed in any direction

## Development

### Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── models/          # Data models
│   │   ├── routers/         # API routes
│   │   └── services/        # Business logic
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   └── package.json
└── README.md
```

## License

This project is proprietary software for Zain Bahrain.

