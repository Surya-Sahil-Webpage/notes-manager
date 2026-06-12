// App.jsx
// Root component of the React application.
// Defines client-side routes using React Router.
// Every URL change renders the matching page component — no full page reload.

import { BrowserRouter, Routes, Route } from 'react-router-dom'
// BrowserRouter → wraps the entire app, enables HTML5 history-based routing
//                 uses the browser's History API (pushState) for clean URLs
//                 e.g. /notes, /notes/create — not /#/notes (that's HashRouter)
// Routes      → container that holds all Route definitions
//               renders the first Route that matches the current URL
// Route       → maps a URL path to a page component
//               path="/" + element={<NotesList />} means:
//               "when URL is /, render NotesList"

import NotesList from './pages/NotesList'
import CreateNote from './pages/CreateNote'
import EditNote from './pages/EditNote'

function App() {
  return (
    <BrowserRouter>
      {/* Routes evaluates the current URL and renders the matching page */}
      <Routes>

        {/* / → show all notes (home page) */}
        <Route path="/" element={<NotesList />} />

        {/* /create → show the create note form */}
        <Route path="/create" element={<CreateNote />} />

        {/* /edit/:id → show the edit form for a specific note */}
        {/* :id is a dynamic segment — /edit/1, /edit/42 both match this */}
        <Route path="/edit/:id" element={<EditNote />} />

      </Routes>
    </BrowserRouter>
  )
}

export default App