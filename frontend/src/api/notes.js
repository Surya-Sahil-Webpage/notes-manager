// notes.js (api layer)
// Contains all API call functions for the Notes resource.
// Pages import these functions — they never call axios directly.
// This keeps HTTP logic out of UI components.

import api from './axios'
// api → the pre-configured Axios instance from Phase 10
// baseURL is already set to http://localhost:8000


// ─── Get All Notes ────────────────────────────────────────────────────────────
// Calls GET /notes
// Returns array of note objects: [{id, title, content, created_at, updated_at}]
export const getAllNotes = async () => {
  const response = await api.get('/notes/')
  return response.data
  // response.data → Axios unwraps the HTTP response for you
  // response.data is the actual JSON array returned by FastAPI
}


// ─── Get Note By ID ───────────────────────────────────────────────────────────
// Calls GET /notes/{id}
// Returns a single note object
export const getNoteById = async (id) => {
  const response = await api.get(`/notes/${id}`)
  return response.data
}


// ─── Create Note ──────────────────────────────────────────────────────────────
// Calls POST /notes
// noteData shape: { title: string, content: string }
// Returns the newly created note object (with id and timestamps)
export const createNote = async (noteData) => {
  const response = await api.post('/notes/', noteData)
  return response.data
}


// ─── Update Note ──────────────────────────────────────────────────────────────
// Calls PUT /notes/{id}
// noteData shape: { title?: string, content?: string }
// Returns the updated note object
export const updateNote = async (id, noteData) => {
  const response = await api.put(`/notes/${id}`, noteData)
  return response.data
}


// ─── Delete Note ──────────────────────────────────────────────────────────────
// Calls DELETE /notes/{id}
// Returns { message: "Note with id X deleted successfully" }
export const deleteNote = async (id) => {
  const response = await api.delete(`/notes/${id}`)
  return response.data
}