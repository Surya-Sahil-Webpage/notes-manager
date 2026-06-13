// axios.js
import axios from 'axios'

const api = axios.create({
  // Use environment variable so URL differs between dev and production
  // In development: VITE_API_URL is not set → falls back to localhost
  // In production: Vercel injects VITE_API_URL as your Render URL
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default api