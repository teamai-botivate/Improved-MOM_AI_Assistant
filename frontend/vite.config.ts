import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, URL } from 'url';

const certDir = fileURLToPath(new URL('./certs', import.meta.url));
const devHttpsKey = path.join(certDir, 'dev-key.pem');
const devHttpsCert = path.join(certDir, 'dev-cert.pem');
const useDevHttps = process.env.VITE_DEV_HTTPS === 'true';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 5173,
    https: useDevHttps ? {
      key: fs.readFileSync(devHttpsKey),
      cert: fs.readFileSync(devHttpsCert),
    } : undefined,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/uploads': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
});
