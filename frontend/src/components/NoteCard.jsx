// NoteCard.jsx
// Reusable component that displays a single note.
// Used by NotesList to render each note in the list.
// Receives note data and callback functions as props.

import { useNavigate } from 'react-router-dom'
// useNavigate → hook that returns a navigate function
// navigate('/edit/1') programmatically changes the URL
// Used when the Edit button is clicked

function NoteCard({ note, onDelete }) {
  // note     → the note object: { id, title, content, created_at, updated_at }
  // onDelete → function passed from NotesList, called when Delete is clicked
  //            NotesList owns the state, so it handles the actual deletion

  const navigate = useNavigate()
  // navigate is a function, not a component
  // calling navigate('/edit/1') pushes that URL into browser history

  // Format the timestamp into a readable date string
  // new Date(note.created_at) → converts ISO string to JS Date object
  // .toLocaleDateString() → formats as "1/15/2024" based on user's locale
  const formattedDate = new Date(note.created_at).toLocaleDateString()

  return (
    <div className="bg-white rounded-2xl shadow-md p-6 flex flex-col gap-3 hover:shadow-lg transition-shadow">

      {/* Note Title */}
      <h2 className="text-xl font-semibold text-gray-800 truncate">
        {note.title}
      </h2>

      {/* Note Content — clamped to 3 lines */}
      <p className="text-gray-600 text-sm line-clamp-3 flex-1">
        {note.content}
      </p>

      {/* Footer — date + action buttons */}
      <div className="flex items-center justify-between mt-2">

        {/* Created date */}
        <span className="text-xs text-gray-400">{formattedDate}</span>

        {/* Action Buttons */}
        <div className="flex gap-2">

          {/* Edit Button — navigates to /edit/:id */}
          <button
            onClick={() => navigate(`/edit/${note.id}`)}
            className="px-3 py-1 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Edit
          </button>

          {/* Delete Button — calls onDelete passed from NotesList */}
          <button
            onClick={() => onDelete(note.id)}
            className="px-3 py-1 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Delete
          </button>

        </div>
      </div>
    </div>
  )
}

export default NoteCard