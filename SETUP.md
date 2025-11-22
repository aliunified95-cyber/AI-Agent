# Setup Guide - Zain Bahrain AI Voice Agent

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Step 1: Backend Setup

1. Open a terminal and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```bash
     venv\Scripts\activate.bat
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. The `.env` file is already configured with your API keys. If you need to modify it:
   - Copy `.env.example` to `.env` (if it doesn't exist)
   - Update the API keys as needed

6. Start the backend server:
```bash
python -m app.main
```

The backend will run on `http://localhost:8000`

### Step 2: Frontend Setup

1. Open a **new terminal** and navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the frontend development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

### Step 3: Using the Application

1. Open your browser and go to `http://localhost:3000`
2. Upload a PDF order summary file
3. Review the parsed order details
4. Click "Start Call" to begin the voice agent session
5. Interact with the agent using:
   - **Microphone button**: Speak to the agent
   - **Text input**: Type messages
6. Click "End Call" when finished

## Troubleshooting

### Backend Issues

**Import errors:**
- Make sure you've activated the virtual environment
- Run `pip install -r requirements.txt` again

**Port already in use:**
- Change the port in `backend/app/main.py` (line 40)
- Or stop the process using port 8000

**API key errors:**
- Check that `.env` file exists in the `backend` directory
- Verify API keys are correct

### Frontend Issues

**Module not found:**
- Run `npm install` again
- Delete `node_modules` and `package-lock.json`, then run `npm install`

**Port already in use:**
- Change the port in `frontend/vite.config.js`
- Or stop the process using port 3000

**WebSocket connection failed:**
- Make sure the backend is running
- Check that the proxy settings in `vite.config.js` match your backend URL

### Common Issues

**PDF parsing fails:**
- Ensure the PDF is a valid order summary
- Check that the PDF contains readable text (not just images)

**Voice not working:**
- Check browser microphone permissions
- Ensure HTTPS is used (required for microphone access in some browsers)
- For local development, use `http://localhost` (not `127.0.0.1`)

**Agent not responding:**
- Check browser console for errors
- Verify API keys are valid
- Check backend logs for errors

## API Keys Configuration

The following API keys are already configured in `backend/.env`:

- **Claude API Key**: For AI conversation handling (using cheapest model: claude-3-haiku)
- **ElevenLabs API Key**: For text-to-speech
- **ElevenLabs Voice ID**: Voice identifier for TTS
- **OpenAI API Key**: For speech-to-text (using Whisper-1)

## Development Notes

- The backend uses FastAPI with automatic API documentation at `http://localhost:8000/docs`
- The frontend uses Vite for fast development with hot module replacement
- WebSocket connections are used for real-time voice communication
- All API calls are proxied through Vite during development

## Production Deployment

For production deployment:

1. Build the frontend:
```bash
cd frontend
npm run build
```

2. Serve the frontend build files using a web server (nginx, Apache, etc.)

3. Deploy the backend using a production ASGI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

4. Use environment variables for API keys (never commit `.env` files)

5. Set up proper CORS settings for your domain

6. Use HTTPS for production (required for microphone access)

## Support

For issues or questions, refer to the main README.md file.

