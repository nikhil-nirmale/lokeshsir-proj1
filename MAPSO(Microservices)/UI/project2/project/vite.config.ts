import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
});
// // // // // import { defineConfig } from 'vite';
// // // // // import react from '@vitejs/plugin-react';

// // // // // // https://vitejs.dev/config/
// // // // // export default defineConfig({
// // // // //   plugins: [react()],
// // // // //   optimizeDeps: {
// // // // //     exclude: ['lucide-react'],
// // // // //   },
// // // // //   server: {
// // // // //     host: '0.0.0.0',
// // // // //     port: 5173,
// // // // //     watch: {
// // // // //       usePolling: true, // Needed for Docker on Windows/file system watching
// // // // //     }
// // // // //   }
// // // // // });


// // // // import { defineConfig } from 'vite';
// // // // import react from '@vitejs/plugin-react';

// // // // export default defineConfig({
// // // //   plugins: [react()],
// // // //   optimizeDeps: {
// // // //     exclude: ['lucide-react'],
// // // //   },
// // // //   server: {
// // // //     host: '0.0.0.0',
// // // //     port: 5173,
// // // //     watch: {
// // // //       usePolling: true,
// // // //     },
// // // //     proxy: {
// // // //       '/api': {
// // // //         target: 'http://localhost:5001',
// // // //         changeOrigin: true,
// // // //         secure: false,
// // // //       }
// // // //     }
// // // //   }
// // // // });







// // import { defineConfig } from 'vite';
// // import react from '@vitejs/plugin-react';

// // export default defineConfig({
// //   plugins: [react()],
// //   optimizeDeps: {
// //     exclude: ['lucide-react'],
// //   },
// //   server: {
// //     host: '0.0.0.0',
// //     port: 5173,
// //     watch: {
// //       usePolling: true,
// //     },
// //     proxy: {
// //       '/api': {
// //         target: 'http://backend:5001',
// //         changeOrigin: true,
// //         secure: false,
// //       }
// //     }
// //   }
// // });
// // vite.config.js
// import { defineConfig } from 'vite';
// import react from '@vitejs/plugin-react';

// export default defineConfig({
//   plugins: [react()],
//   server: {
//     host: true, // This allows access from network IP as well as localhost
//     port: 5173, // Or your preferred port
//     proxy: {
//       '/api': { // Any request starting with /api
//         target: 'http://localhost:5001', // Or 'http://127.0.0.1:5001'
//         changeOrigin: true, // Changes the origin header to the target URL
//         rewrite: (path) => path.replace(/^\/api/, ''), // Rewrites /api/validate to /validate for your backend
//       },
//     },
//   },
// });