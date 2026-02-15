import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from "@tailwindcss/vite";
import path from 'path';
// https://vite.dev/config/
export default defineConfig({
  plugins: [tailwindcss(), vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: { // dev
    host: '0.0.0.0', // Allows Vite to listen on all interfaces
    port: 8080, // Ensure the port matches the one in your Dockerfile
    // watch: {
    //   usePolling: true
    // }
  },

})