import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const isProduction = process.env.NODE_ENV === 'production'
const backendUrl = process.env.VITE_API_URL || (isProduction ? 'https://zain-ai-voice-agent.onrender.com' : 'http://localhost:8000')

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: backendUrl,
        changeOrigin: true
      },
      '/ws': {
        target: backendUrl.replace('http', 'ws'),
        ws: true
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['lucide-react']
        }
      }
    }
  }
})

