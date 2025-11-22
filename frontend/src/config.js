// API configuration
const isProduction = import.meta.env.PROD
const apiUrl = import.meta.env.VITE_API_URL || (isProduction 
  ? 'https://zain-ai-voice-agent.onrender.com' 
  : 'http://localhost:8000')

export const API_BASE_URL = apiUrl
export const WS_BASE_URL = apiUrl.replace(/^https?/, apiUrl.startsWith('https') ? 'wss' : 'ws')

