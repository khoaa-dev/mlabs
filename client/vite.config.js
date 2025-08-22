
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/contacts': 'http://localhost:5143',
      '/messages': 'http://localhost:5143',
      '/static': 'http://localhost:5143'
    }
  }
})