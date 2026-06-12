// main.jsx
// Entry point of the React application.
// ReactDOM mounts the App component into the #root div in index.html.

import { StrictMode } from 'react'
// StrictMode → development tool that highlights potential problems
//              renders components twice in dev to detect side effects
//              has zero effect in production builds

import { createRoot } from 'react-dom/client'
// createRoot → React 18's rendering API
//              replaces the old ReactDOM.render()

import './index.css'    // Tailwind CSS — must be imported here to apply globally
import App from './App.jsx'

// Mount the App component into the <div id="root"> in index.html
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)