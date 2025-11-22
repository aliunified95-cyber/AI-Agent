import React, { useState } from 'react'
import axios from 'axios'
import { Upload, FileText, Loader2, AlertCircle } from 'lucide-react'
import { API_BASE_URL } from '../config'

function PDFUpload({ onOrderParsed }) {
  const [isDragging, setIsDragging] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState(null)

  const handleFile = async (file) => {
    if (!file.type.includes('pdf')) {
      setError('Please upload a PDF file')
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('pdf_file', file)

      const response = await axios.post(`${API_BASE_URL}/api/parse-order`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      onOrderParsed(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Error parsing PDF. Please try again.')
    } finally {
      setIsUploading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    if (file) {
      handleFile(file)
    }
  }

  return (
    <div>
      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
          isDragging
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 hover:border-indigo-400'
        } ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
      >
        {isUploading ? (
          <div className="flex flex-col items-center">
            <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mb-4" />
            <p className="text-gray-600">Parsing PDF...</p>
          </div>
        ) : (
          <>
            <div className="flex flex-col items-center">
              <div className="bg-indigo-100 rounded-full p-4 mb-4">
                <Upload className="w-8 h-8 text-indigo-600" />
              </div>
              <p className="text-gray-700 font-medium mb-2">
                Drag and drop your PDF here
              </p>
              <p className="text-gray-500 text-sm mb-4">or</p>
              <label className="cursor-pointer">
                <span className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 transition-colors inline-block">
                  Browse Files
                </span>
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileInput}
                  className="hidden"
                />
              </label>
              <p className="text-gray-400 text-xs mt-4">
                Only PDF files are supported
              </p>
            </div>
          </>
        )}
      </div>

      {error && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-red-600" />
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}

export default PDFUpload

