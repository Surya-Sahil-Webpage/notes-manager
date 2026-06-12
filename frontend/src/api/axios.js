// axios.js
// Creates a pre-configured Axios instance for all API calls.
// Instead of writing the full URL every time:
//   axios.get("http://localhost:8000/notes")
// You write:
//   api.get("/notes")
// The base URL is set once here and reused everywhere.

import axios from 'axios'
// axios → the HTTP client library installed in Step 2

const api = axios.create({
  // baseURL → prepended to every request URL made with this instance
  // All your FastAPI routes start with http://localhost:8000
  // In production this will change to your Render URL — change it in one place
  baseURL: 'http://localhost:8000',

  headers: {
    // Tell the backend every request body is JSON
    'Content-Type': 'application/json',
  },
})

// Export the configured instance
// Every page/component imports this instead of raw axios
export default api