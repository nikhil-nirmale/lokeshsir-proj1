// // Security Check Types
// export type CheckType = 'macro' | 'ads' | 'password' | 'steganography' | 'ocr';

// export type CheckResult = 'PRESENT' | 'NOT_DETECTED' | 'ERROR' | 'SKIPPED';

// export type ValidoStatus = 'VALID' | 'INVALID' | 'UNKNOWN';

// export type JobStatus = 'queued' | 'processing' | 'done' | 'failed';

// // Request and Response Types
// export interface AnalysisRequest {
//   file?: File;
//   file_url?: string;
//   metadata?: {
//     document_id?: string;
//     author?: string;
//     document_type?: string;
//     [key: string]: any;
//   };
//   checks: CheckType[];
//   generate_derived?: boolean;
//   on_critical_failure_continue?: boolean;
//   force_ocr_even_if_invalid?: boolean;
// }

// export interface CheckReportItem {
//   name: CheckType;
//   result: CheckResult;
//   error?: string;
//   details?: any;
// }

// export interface AnalysisResponse {
//   job_id: string;
//   status: JobStatus;
//   progress: number;
//   result?: {
//     valido_status: ValidoStatus;
//     checks: CheckReportItem[];
//     derived_file_url?: string;
//     notes?: string;
//   };
//   error?: string;
// }

// // Log Types
// export interface LogEntry {
//   timestamp: string;
//   document_id: string;
//   filename: string;
//   checks: CheckType[];
//   outcome: ValidoStatus;
//   duration_ms: number;
// }

// // Database Types
// export interface FileRecord {
//   id: number;
//   job_id: string;
//   filename: string;
//   status: JobStatus;
//   checks: string; // JSON string of check types
//   result_json?: string;
//   created_at: string;
//   updated_at: string;
// }



// Security Check Types
export type CheckType = 'macro' | 'ads' | 'password' | 'steganography' | 'ocr';

export type CheckResult = 'PRESENT' | 'NOT_DETECTED' | 'ERROR' | 'SKIPPED';

export type ValidoStatus = 'VALID' | 'INVALID' | 'UNKNOWN';

export type JobStatus = 'queued' | 'processing' | 'done' | 'failed';

// Request and Response Types
export interface AnalysisRequest {
  file?: File;
  file_url?: string;
  metadata?: {
    document_id?: string;
    author?: string;
    document_type?: string;
    [key: string]: any;
  };
  checks: CheckType[];
  generate_derived?: boolean;
  on_critical_failure_continue?: boolean;
  force_ocr_even_if_invalid?: boolean;
}

export interface CheckReportItem {
  name: CheckType;
  result: CheckResult;
  error?: string;
  details?: any;
}

export interface AnalysisResult {
  valido_status: ValidoStatus;
  checks: CheckReportItem[];
  force_ocr_even_if_invalid: number;  // Changed to number to match API (0/1)
  generate_derived: number;           // Changed to number to match API (0/1)
  on_critical_failure_continue: number;
  derived_file_url?: string;
  notes?: string;
}

export interface AnalysisResponse {
  job_id: string;
  status: JobStatus;
  progress: number;
  result?: AnalysisResult;
  error?: string;
}

// Log Types
export interface LogEntry {
  timestamp: string;
  document_id: string;
  filename: string;
  checks: CheckType[];
  outcome: ValidoStatus;
  duration_ms: number;
}

// Database Types
export interface FileRecord {
  id: number;
  job_id: string;
  filename: string;
  status: JobStatus;
  checks: string; // JSON string of check types
  result_json?: string;
  created_at: string;
  updated_at: string;
}