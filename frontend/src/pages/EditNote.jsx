// EditNote.jsx
// Page that pre-fills a form with an existing note's data and updates it.
// Requires fetching the note on mount before showing the form.

import { useState, useEffect } from 'react'
// useState  → stores form values and UI state
// useEffect → fetches existing note data when the component mounts

import { useNavigate, useParams } from 'react-router-dom'
// useNavigate → redirects to '/' after successful update
// useParams   → extracts dynamic URL segments
//               on route /edit/:id, useParams() returns { id: "3" }
//               note: id is always a STRING from the URL — convert to int if needed

import { getNoteById, updateNote } from '../api/notes'
// getNoteById → GET /notes/{id} — fetches the existing note to pre-fill form
// updateNote  → PUT /notes/{id} — sends the updated data

function EditNote() {
  // ─── Extract Note ID from URL ────────────────────────────────────────────────
  const { id } = useParams()
  // id → the :id segment from the URL as a string e.g. "3"
  // destructured directly from the params object

  const navigate = useNavigate()

  // ─── Form State ─────────────────────────────────────────────────────────────
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  // Both start empty — they get populated once the note is fetched

  // ─── UI State ───────────────────────────────────────────────────────────────
  const [loading, setLoading] = useState(true)
  // loading → true while fetching the existing note
  // shows a loading state instead of an empty form

  const [submitting, setSubmitting] = useState(false)
  // submitting → true while the PUT request is in progress

  const [error, setError] = useState(null)
  // error → stores any error message (fetch failed, update failed, not found)

  // ─── Fetch Existing Note on Mount ───────────────────────────────────────────
  useEffect(() => {
    fetchNote()
  }, [id])
  // [id] as dependency → re-fetch if the id in the URL changes
  // e.g. user navigates from /edit/1 directly to /edit/2
  // without id in deps, the form would still show note 1's data

  const fetchNote = async () => {
    try {
      setLoading(true)
      setError(null)

      const note = await getNoteById(id)
      // GET /notes/{id} → returns the note object

      // Pre-populate the form with existing values
      // This is what makes Edit different from Create
      setTitle(note.title)
      setContent(note.content)
    } catch (err) {
      // 404 → note doesn't exist (user manually typed a bad URL)
      // Other errors → network issue, server down
      if (err.response?.status === 404) {
        setError('Note not found.')
      } else {
        setError('Failed to load note.')
      }
    } finally {
      setLoading(false)
    }
  }

  // ─── Handle Submit ──────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!title.trim() || !content.trim()) {
      setError('Both title and content are required.')
      return
    }

    try {
      setSubmitting(true)
      setError(null)

      await updateNote(id, { title, content })
      // PUT /notes/{id} with updated title and content
      // Backend's NoteUpdate schema accepts partial updates
      // but we send both fields since the user can see and edit both

      navigate('/')
      // Redirect to home — updated note will appear in the list
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Note not found.')
      } else {
        setError(err.response?.data?.detail || 'Failed to update note.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  // ─── Render: Loading State ───────────────────────────────────────────────────
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500 text-lg">Loading note...</p>
      </div>
    )
  }

  // ─── Render: Note Not Found ──────────────────────────────────────────────────
  // If fetch failed with 404, show error + back button
  // Don't render the form — there's nothing to edit
  if (error && !submitting) {
    const isFetchError = !title && !content
    // isFetchError → true if we never successfully loaded the note
    // (title and content are still empty from useState initialization)
    // vs a submit error where title and content are populated

    if (isFetchError) {
      return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center gap-4">
          <p className="text-red-500 text-lg">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors"
          >
            ← Back to Notes
          </button>
        </div>
      )
    }
  }

  // ─── Render: Edit Form ───────────────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6">
      <div className="max-w-2xl mx-auto">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Edit Note</h1>

          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 text-sm text-gray-600 bg-white border border-gray-300 rounded-xl hover:bg-gray-100 transition-colors"
          >
            ← Back
          </button>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-2xl shadow-md p-8">

          {/* Error Message — shown for submit errors */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-600 rounded-xl text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-6">

            {/* Title Field — pre-populated with existing title */}
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
                placeholder="Enter note title..."
                className="px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              />
            </div>

            {/* Content Field — pre-populated with existing content */}
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
                className="px-4 py-3 border border-gray-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 transition resize-none"
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">

              {/* Cancel — goes back without saving */}
              <button
                type="button"
                onClick={() => navigate('/')}
                className="flex-1 py-3 bg-white text-gray-600 font-medium border border-gray-300 rounded-xl hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>

              {/* Submit */}
              <button
                type="submit"
                disabled={submitting}
                className="flex-1 py-3 bg-blue-500 text-white font-medium rounded-xl hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? 'Saving...' : 'Save Changes'}
              </button>

            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default EditNote