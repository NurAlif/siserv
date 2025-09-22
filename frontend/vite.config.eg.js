import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 7778,
    host: '0.0.0.0', // Add this line
    allowedHosts: ['ai-ndhu-lab', '134.208.6.129']
  },
});
