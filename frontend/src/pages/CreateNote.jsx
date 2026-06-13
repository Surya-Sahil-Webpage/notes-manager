// CreateNote.jsx
// Page that renders a form to create a new note.
// Controlled inputs — React owns all form state.
// On submit: calls POST /notes/, then navigates to home.

import { useState } from 'react'
// useState → stores form field values and UI state (submitting, error)

import { useNavigate } from 'react-router-dom'
// useNavigate → redirects to '/' after successful creation

import { createNote } from '../api/notes'
// createNote → calls POST /notes/ with form data

function CreateNote() {
  // ─── Form State ─────────────────────────────────────────────────────────────
  const [title, setTitle] = useState('')
  // title    → current value of the title input
  // ''       → starts empty

  const [content, setContent] = useState('')
  // content  → current value of the content textarea

  // ─── UI State ───────────────────────────────────────────────────────────────
  const [submitting, setSubmitting] = useState(false)
  // submitting → true while API call is in progress
  //              used to disable the submit button — prevents double submissions

  const [error, setError] = useState(null)
  // error    → stores error message if API call fails

  const navigate = useNavigate()

  // ─── Handle Submit ──────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault()
    // e.preventDefault() → stops the browser's default form behavior
    // Default behavior: reload the page and send a GET/POST to the current URL
    // We don't want that — we handle submission manually with Axios

    // Basic client-side validation
    // Pydantic will also validate on the backend, but catching it here
    // gives instant feedback without a network round-trip
    if (!title.trim() || !content.trim()) {
      setError('Both title and content are required.')
      return  // stop here — don't call the API
    }

    try {
      setSubmitting(true)   // disable submit button
      setError(null)        // clear previous errors

      await createNote({ title, content })
      // createNote sends: POST /notes/ with body { title, content }
      // On success, FastAPI returns the created note (201)
      // We don't need the return value here — just navigate away

      navigate('/')
      // Redirect to home page after successful creation
      // React Router updates the URL and renders NotesList
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create note.')
    } finally {
      setSubmitting(false)  // re-enable submit button
    }
  }

  // ─── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6">
      <div className="max-w-2xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Create Note</h1>

          {/* Back button — navigates to home without submitting */}
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 text-sm text-gray-600 bg-white border border-gray-300 rounded-xl hover:bg-gray-100 transition-colors"
          >
            ← Back
          </button>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-md p-8">

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl text-sm">
              {error}
            </div>
          )}

          {/* Form — onSubmit wired to handleSubmit */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-6">

            {/* Title Field */}
            <div className="flex flex-col gap-2">
              <label
                htmlFor="title"
                className="text-sm font-medium text-gray-700"
              >
                Title
              </label>
              <input
                id="title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                // e.target.value → the current text in the input
                // setTitle updates state on every keystroke
                placeholder="Enter note title..."
                className="px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            {/* Content Field */}
            <div className="flex flex-col gap-2">
              <label
                htmlFor="content"
                className="text-sm font-medium text-gray-700"
              >
                Content
              </label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Write your note here..."
                rows={6}
                // rows={6} → sets the visible height of the textarea
                className="px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={submitting}
              // disabled → prevents clicking while API call is in progress
              // Tailwind's disabled: variant styles it differently when disabled
              className="py-3 bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? 'Creating...' : 'Create Note'}
              {/* Shows different text during submission — clear feedback */}
            </button>

          </form>
        </div>
      </div>
    </div>
  )
}

export default CreateNote