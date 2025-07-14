import axios from 'axios';
import { AnalysisRequest, AnalysisResponse, LogEntry } from '../types';

// Create axios instance with base URL
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analysis API functions
// export const submitFileAnalysis = async (analysisRequest: AnalysisRequest): Promise<AnalysisResponse> => {
//   const formData = new FormData();
  
//   // Add file if present
//   if (analysisRequest.file) {
//     formData.append('file', analysisRequest.file);
//   }
  
//   // Add file_url if present
//   if (analysisRequest.file_url) {
//     formData.append('file_url', analysisRequest.file_url);
//   }
  
//   // Add metadata if present
//   if (analysisRequest.metadata) {
//     formData.append('metadata', JSON.stringify(analysisRequest.metadata));
//   }
  
//   // Add checks
//   formData.append('checks', JSON.stringify(analysisRequest.checks));
  
//   // Add optional parameters
//   formData.append('generate_derived', String(analysisRequest.generate_derived ?? true));
//   formData.append('on_critical_failure_continue', String(analysisRequest.on_critical_failure_continue ?? false));
//   formData.append('force_ocr_even_if_invalid', String(analysisRequest.force_ocr_even_if_invalid ?? false));
  
//   const response = await api.post<AnalysisResponse>('/validate', formData, {
//     headers: {
//       'Content-Type': 'multipart/form-data',
//     },
//   });
  
//   return response.data;
// };
export const submitFileAnalysis = async (analysisRequest: AnalysisRequest): Promise<AnalysisResponse> => {
  const formData = new FormData();
  
  // Add file if present
  if (analysisRequest.file) {
    formData.append('file', analysisRequest.file);
  }

  // Add file_url if present
  if (analysisRequest.file_url) {
    formData.append('file_url', analysisRequest.file_url);
  }

  // Add metadata if present
  if (analysisRequest.metadata) {
    formData.append('metadata', JSON.stringify(analysisRequest.metadata));
  }

  // Correct way to append each check for Flask to read getlist('checks')
  if (Array.isArray(analysisRequest.checks)) {
    analysisRequest.checks.forEach((check) => {
      formData.append('checks', check); // NOT as JSON array
    });
  }

  // Add flags
  formData.append('generate_derived', String(analysisRequest.generate_derived ?? true));
  formData.append('on_critical_failure_continue', String(analysisRequest.on_critical_failure_continue ?? false));
  formData.append('force_ocr_even_if_invalid', String(analysisRequest.force_ocr_even_if_invalid ?? false));

  const response = await api.post<AnalysisResponse>('/validate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
export const getJobStatus = async (jobId: string): Promise<AnalysisResponse> => {
  const response = await api.get<AnalysisResponse>(`/status/${jobId}`);
  return response.data;
};

export const getLogs = async (limit: number = 20): Promise<LogEntry[]> => {
  const response = await api.get<LogEntry[]>('/logs', {
    params: { limit },
  });
  return response.data;
};

export default {
  submitFileAnalysis,
  getJobStatus,
  getLogs,
};