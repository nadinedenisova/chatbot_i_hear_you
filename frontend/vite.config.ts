import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': `/src`,
      '@components': '/src/components',
      '@pages': '/src/pages',
      '@routes': '/src/routes',
      '@utils': '/src/utils',
      '@assets': '/src/assets',
      '@store': '/src/store',
      '@api': '/src/api',
      '@shared': '/src/shared',
      '@hooks': '/src/hooks',
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://admin',
        changeOrigin: true,
      },
    },
  },
});
