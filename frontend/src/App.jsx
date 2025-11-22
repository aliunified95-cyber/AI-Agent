import React, { useState } from 'react'
import PDFUpload from './components/PDFUpload'
import OrderDisplay from './components/OrderDisplay'
import VoiceCallInterface from './components/VoiceCallInterface'
import { Upload, Phone, FileText } from 'lucide-react'

function App() {
  const [orderData, setOrderData] = useState(null)
  const [isCallActive, setIsCallActive] = useState(false)
  const [sessionId, setSessionId] = useState(null)

  const handleOrderParsed = (data) => {
    setOrderData(data)
    setIsCallActive(false)
    setSessionId(null)
  }

  const handleCallStarted = (session) => {
    setSessionId(session.session_id)
    setIsCallActive(true)
  }

  const handleCallEnded = () => {
    setIsCallActive(false)
    setSessionId(null)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-2xl mb-8 p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="bg-gradient-to-br from-red-500 to-red-600 p-3 rounded-xl">
                <Phone className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-800">Zain Bahrain</h1>
                <p className="text-gray-600">AI Voice Agent System</p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">System Online</span>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Upload & Order Info */}
          <div className="lg:col-span-1 space-y-6">
            {/* PDF Upload Section */}
            {!orderData && (
              <div className="bg-white rounded-2xl shadow-2xl p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <Upload className="w-6 h-6 text-indigo-600" />
                  <h2 className="text-xl font-semibold text-gray-800">Upload Order PDF</h2>
                </div>
                <PDFUpload onOrderParsed={handleOrderParsed} />
              </div>
            )}

            {/* Order Display */}
            {orderData && (
              <div className="bg-white rounded-2xl shadow-2xl p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <FileText className="w-6 h-6 text-indigo-600" />
                  <h2 className="text-xl font-semibold text-gray-800">Order Details</h2>
                </div>
                <OrderDisplay orderData={orderData} />
              </div>
            )}
          </div>

          {/* Right Column - Voice Interface */}
          <div className="lg:col-span-2">
            {orderData ? (
              <VoiceCallInterface
                orderData={orderData}
                isActive={isCallActive}
                sessionId={sessionId}
                onCallStarted={handleCallStarted}
                onCallEnded={handleCallEnded}
              />
            ) : (
              <div className="bg-white rounded-2xl shadow-2xl p-12 text-center">
                <div className="max-w-md mx-auto">
                  <div className="bg-gradient-to-br from-indigo-100 to-purple-100 rounded-full w-32 h-32 flex items-center justify-center mx-auto mb-6">
                    <Upload className="w-16 h-16 text-indigo-600" />
                  </div>
                  <h3 className="text-2xl font-semibold text-gray-800 mb-2">
                    Get Started
                  </h3>
                  <p className="text-gray-600">
                    Upload an order PDF to begin testing the AI voice agent
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

