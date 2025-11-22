import React, { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { Phone, PhoneOff, Mic, MicOff, Volume2, Loader2, MessageCircle } from 'lucide-react'
import { API_BASE_URL, WS_BASE_URL } from '../config'

function VoiceCallInterface({ orderData, isActive, sessionId, onCallStarted, onCallEnded }) {
  const [callActive, setCallActive] = useState(isActive)
  const [isMuted, setIsMuted] = useState(false)
  const [conversation, setConversation] = useState([])
  const [currentState, setCurrentState] = useState('INIT')
  const [isProcessing, setIsProcessing] = useState(false)
  const [inputText, setInputText] = useState('')
  const [currentSessionId, setCurrentSessionId] = useState(sessionId)
  const [isRecording, setIsRecording] = useState(false)
  
  const conversationEndRef = useRef(null)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const wsRef = useRef(null)

  useEffect(() => {
    conversationEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversation])

  const startCall = async () => {
    try {
      setIsProcessing(true)
      const response = await axios.post(`${API_BASE_URL}/api/start-call`, {
        order_data: orderData
      })
      
      const newSessionId = response.data.session_id
      setCurrentSessionId(newSessionId)
      setCallActive(true)
      onCallStarted({ session_id: newSessionId })
      
      // Connect WebSocket
      connectWebSocket(newSessionId)
      
      // Get initial greeting (agent will send it automatically via WebSocket)
      // The WebSocket connection will handle the initial message
      
      // Note: WebSocket connection is established in connectWebSocket function
    } catch (error) {
      console.error('Error starting call:', error)
      alert('Failed to start call. Please try again.')
    } finally {
      setIsProcessing(false)
    }
  }

  const connectWebSocket = (sessionId) => {
    // Use configured WebSocket URL
    const wsUrl = `${WS_BASE_URL}/ws/voice/${sessionId}`
    
    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      console.log('WebSocket connected')
    }

    ws.onmessage = async (event) => {
      if (event.data instanceof Blob) {
        // Audio data
        const audio = new Audio(URL.createObjectURL(event.data))
        audio.play().catch(err => console.error('Error playing audio:', err))
      } else {
        // Text data
        try {
          const data = JSON.parse(event.data)
          if (data.type === 'text') {
            if (data.message) {
              addMessage('assistant', data.message)
            }
            if (data.transcript) {
              addMessage('user', data.transcript)
            }
            if (data.state) {
              setCurrentState(data.state)
            }
          } else if (data.type === 'error') {
            addMessage('system', data.message)
          }
        } catch (e) {
          console.error('Error parsing WebSocket message:', e)
        }
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }
  }

  const endCall = async () => {
      if (currentSessionId) {
        try {
          await axios.delete(`${API_BASE_URL}/api/session/${currentSessionId}`)
        } catch (error) {
          console.error('Error ending call:', error)
        }
      }
    
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    
    setCallActive(false)
    setCurrentSessionId(null)
    setConversation([])
    onCallEnded()
  }

  const sendMessage = async (text) => {
    if (!text.trim() || !currentSessionId) return

    addMessage('user', text)
    setIsProcessing(true)

    try {
      const response = await axios.post(`${API_BASE_URL}/api/session/${currentSessionId}/process`, {
        text: text
      })

      addMessage('assistant', response.data.response)
      setCurrentState(response.data.state)
      
      // Generate and play audio
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({
          type: 'text',
          text: text
        }))
      }
    } catch (error) {
      console.error('Error sending message:', error)
      addMessage('system', 'Error processing message. Please try again.')
    } finally {
      setIsProcessing(false)
      setInputText('')
    }
  }

  const addMessage = (role, content) => {
    setConversation(prev => [...prev, {
      role,
      content,
      timestamp: new Date().toLocaleTimeString()
    }])
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        
        // Send audio via WebSocket
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(audioBlob)
        }
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
    } catch (error) {
      console.error('Error starting recording:', error)
      alert('Microphone access denied. Please enable microphone permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage(inputText)
    }
  }

  return (
    <div className="bg-white rounded-2xl shadow-2xl p-6 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Voice Agent</h2>
          <p className="text-sm text-gray-600">State: <span className="font-medium capitalize">{currentState.replace('_', ' ')}</span></p>
        </div>
        {!callActive ? (
          <button
            onClick={startCall}
            disabled={isProcessing}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl flex items-center space-x-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Starting...</span>
              </>
            ) : (
              <>
                <Phone className="w-5 h-5" />
                <span>Start Call</span>
              </>
            )}
          </button>
        ) : (
          <button
            onClick={endCall}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-xl flex items-center space-x-2 transition-colors"
          >
            <PhoneOff className="w-5 h-5" />
            <span>End Call</span>
          </button>
        )}
      </div>

      {/* Conversation Area */}
      <div className="flex-1 bg-gray-50 rounded-xl p-4 mb-4 overflow-y-auto max-h-96">
        {conversation.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <MessageCircle className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>Conversation will appear here</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {conversation.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg p-3 ${
                    msg.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : msg.role === 'system'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-white text-gray-800 border border-gray-200'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                  <p className="text-xs opacity-70 mt-1">{msg.timestamp}</p>
                </div>
              </div>
            ))}
            <div ref={conversationEndRef} />
          </div>
        )}
      </div>

      {/* Input Area */}
      {callActive && (
        <div className="space-y-3">
          {/* Voice Recording */}
          <div className="flex items-center justify-center space-x-4">
            {isRecording ? (
              <button
                onClick={stopRecording}
                className="bg-red-600 hover:bg-red-700 text-white p-4 rounded-full transition-colors animate-pulse"
              >
                <MicOff className="w-6 h-6" />
              </button>
            ) : (
              <button
                onClick={startRecording}
                disabled={isProcessing}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-4 rounded-full transition-colors disabled:opacity-50"
              >
                <Mic className="w-6 h-6" />
              </button>
            )}
            <span className="text-sm text-gray-600">
              {isRecording ? 'Recording... Click to stop' : 'Click to speak'}
            </span>
          </div>

          {/* Text Input */}
          <div className="flex space-x-2">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isProcessing}
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
            />
            <button
              onClick={() => sendMessage(inputText)}
              disabled={isProcessing || !inputText.trim()}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                'Send'
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default VoiceCallInterface

