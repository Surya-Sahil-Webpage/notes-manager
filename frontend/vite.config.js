// vite.config.js
// Vite's build configuration file.
// Tells Vite which plugins to use when building/serving the app.

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
// @tailwindcss/vite → Tailwind v4's Vite plugin
// In v4, Tailwind is a Vite plugin, not a PostCSS plugin
// This replaces the old tailwind.config.js approach entirely

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),   // ← registers Tailwind as a Vite plugin
  ],
})