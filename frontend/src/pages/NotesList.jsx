// NotesList.jsx
// Home page — displays all notes fetched from GET /notes.
// Handles loading state, empty state, and note deletion.

import { useState, useEffect } from 'react'
// useState  → stores and updates component data (notes array, loading flag)
//             when state changes, React re-renders the component automatically
// useEffect → runs side effects after render
//             "side effect" = anything outside React's render cycle: API calls,
//             timers, subscriptions
//             useEffect(() => { ... }, []) with empty [] = runs once on mount

import { useNavigate } from 'react-router-dom'
// useNavigate → used to navigate to /create when "New Note" button is clicked

import { getAllNotes, deleteNote } from '../api/notes'
// getAllNotes → fetches all notes from GET /notes
// deleteNote  → deletes a note from DELETE /notes/{id}

import NoteCard from '../components/NoteCard'
// NoteCard → reusable component that renders one note

function NotesList() {
  // ─── State ──────────────────────────────────────────────────────────────────
  const [notes, setNotes] = useState([])
  // notes     → array of note objects fetched from the backend
  // setNotes  → function to update the notes array
  // []        → initial value: empty array (no notes loaded yet)

  const [loading, setLoading] = useState(true)
  // loading   → true while API call is in progress
  // false     → once data is fetched (or failed)
  // Used to show a loading spinner instead of an empty page

  const [error, setError] = useState(null)
  // error     → stores error message if the API call fails
  // null      → no error initially

  const navigate = useNavigate()

  // ─── Fetch Notes on Mount ────────────────────────────────────────────────────
  useEffect(() => {
    // This function runs once when NotesList first renders (mounts)
    // The empty dependency array [] means: "run this effect only on mount"
    // If you put [notes] here instead, it would run every time notes changes → infinite loop
    fetchNotes()
  }, [])  // ← empty array = run once on mount only

  const fetchNotes = async () => {
    try {
      setLoading(true)       // show loading state before API call
      setError(null)         // clear any previous errors

      const data = await getAllNotes()  // GET /notes → array of notes
      setNotes(data)                    // store in state → triggers re-render
    } catch (err) {
      // err.response?.data?.detail → FastAPI's error message (if available)
      // err.message → generic Axios error (network down, timeout, etc.)
      setError(err.response?.data?.detail || 'Failed to fetch notes')
    } finally {
      setLoading(false)      // hide loading state whether success or failure
    }
  }

  // ─── Handle Delete ────────────────────────────────────────────────────────
  const handleDelete = async (id) => {
    // Confirm before deleting — prevents accidental deletion
    if (!window.confirm('Are you sure you want to delete this note?')) return

    try {
      await deleteNote(id)   // DELETE /notes/{id}

      // Update state by filtering out the deleted note
      // This avoids a full re-fetch — faster and no extra API call
      // filter creates a new array without the deleted note
      setNotes(prev => prev.filter(note => note.id !== id))
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to delete note')
    }
  }

  // ─── Render ───────────────────────────────────────────────────────────────

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500 text-lg">Loading notes...</p>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6">

      {/* Header */}
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Notes</h1>

          {/* Navigate to Create Note page */}
          <button
            onClick={() => navigate('/create')}
            className="px-5 py-2 bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-600 transition-colors"
          >
            + New Note
          </button>
        </div>

        {/* Empty state — when no notes exist */}
        {notes.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-400 text-lg">No notes yet.</p>
            <p className="text-gray-400 text-sm mt-1">Click "+ New Note" to create one.</p>
          </div>
        ) : (
          /* Notes Grid — responsive: 1 col mobile, 2 col tablet, 3 col desktop */
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {notes.map(note => (
              // key → required by React when rendering lists
              // React uses key to identify which item changed/added/removed
              // Always use a stable unique id — never use array index as key
              <NoteCard
                key={note.id}
                note={note}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default NotesList