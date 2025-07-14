import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import Layout from './components/Layout';
import FileUploadPage from './pages/FileUploadPage';
import StatusPage from './pages/StatusPage';
import LogsPage from './pages/LogsPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<FileUploadPage />} />
            <Route path="/status/:jobId?" element={<StatusPage />} />
            <Route path="/logs" element={<LogsPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;