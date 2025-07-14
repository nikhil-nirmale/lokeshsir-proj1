import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Shield, 
  FileWarning, 
  Eye, 
  Lock, 
  Image,
  AlertOctagon
} from 'lucide-react';

import FileInput from '../components/ui/FileInput';
import Input from '../components/ui/Input';
import Checkbox from '../components/ui/Checkbox';
import Toggle from '../components/ui/Toggle';
import Button from '../components/ui/Button';
import Panel from '../components/ui/Panel';
import { AnalysisRequest, CheckType } from '../types';
import api from '../services/api';
import dbService from '../services/database';

const FileUploadPage: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [fileUrl, setFileUrl] = useState('');
  const [checks, setChecks] = useState<CheckType[]>([]);
  const [generateDerived, setGenerateDerived] = useState(true);
  const [onCriticalFailureContinue, setOnCriticalFailureContinue] = useState(false);
  const [forceOcr, setForceOcr] = useState(false);
  const [error, setError] = useState('');
  const [metadata, setMetadata] = useState({
    document_id: '',
    author: '',
    document_type: '',
  });

  // Check option definitions with icons and descriptions
  const checkOptions = [
    {
      value: 'macro',
      label: 'Macro Detection',
      description: 'Detect potentially malicious macros in documents',
      icon: <FileWarning className="w-5 h-5 text-warning" />,
    },
    {
      value: 'ads',
      label: 'Alternate Data Streams',
      description: 'Attackers can hide malicious code or payloads in these alternate streams without affecting the visible file size or content.',
      icon: <AlertOctagon className="w-5 h-5 text-error" />,
    },
    {
      value: 'password',
      label: 'Password Protection',
      description: 'Check if the document is password protected',
      icon: <Lock className="w-5 h-5 text-primary" />,
    },
    {
      value: 'steganography',
      label: 'Steganography Detection',
      description: 'Analyze for hidden content using steganography',
      icon: <Image className="w-5 h-5 text-secondary" />,
    },
    {
      value: 'ocr',
      label: 'OCR Text Extraction',
      description: 'Extract and analyze text content using OCR',
      icon: <Eye className="w-5 h-5 text-accent" />,
    },
  ];

  const handleCheckChange = (checkType: CheckType, checked: boolean) => {
    if (checked) {
      setChecks([...checks, checkType]);
    } else {
      setChecks(checks.filter(c => c !== checkType));
    }
  };

  const handleMetadataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setMetadata({
      ...metadata,
      [name]: value,
    });
  };

  const validateForm = (): boolean => {
    if (!file && !fileUrl) {
      setError('Please upload a file or provide a file URL');
      return false;
    }

    if (checks.length === 0) {
      setError('Please select at least one check to perform');
      return false;
    }

    setError('');
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const request: AnalysisRequest = {
        file: file,
        file_url: fileUrl || undefined,
        metadata: Object.entries(metadata).some(([_, v]) => v) ? metadata : undefined,
        checks,
        generate_derived: generateDerived,
        on_critical_failure_continue: onCriticalFailureContinue,
        force_ocr_even_if_invalid: forceOcr,
      };

      const response = await api.submitFileAnalysis(request);
      
      // Store file record in database
      await dbService.saveFileRecord({
        job_id: response.job_id,
        filename: file?.name || fileUrl.split('/').pop() || 'unknown',
        status: response.status,
        checks: JSON.stringify(checks),
        result_json: response.result ? JSON.stringify(response.result) : undefined,
      });

      // Navigate to status page
      navigate(`/status/${response.job_id}`);
    } catch (err) {
      console.error('Error submitting file for analysis:', err);
      setError('An error occurred while submitting the file for analysis');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="flex items-center mb-6">
        <Shield className="mr-3 h-8 w-8 text-primary" />
        <h1 className="text-2xl font-bold">Document Security Analysis</h1>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-error/10 border border-error/20 rounded-lg text-error">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <Panel 
          title="Document Upload"
          defaultOpen={true}
          className="mb-6"
        >
          <div className="space-y-4">
            <FileInput
              label="Upload Document"
              accept=".pdf,.docx,.doc,.xlsx,.xls,.pptx,.ppt,.png,.jpeg,.jpg"
              value={file}
              onChange={setFile}
              fullWidth
              disabled={!!fileUrl || isLoading}
            />

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-border"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-card text-muted">or</span>
              </div>
            </div>

            <Input
              label="Document URL"
              type="url"
              placeholder="https://example.com/document.pdf"
              value={fileUrl}
              onChange={(e) => setFileUrl(e.target.value)}
              fullWidth
              disabled={!!file || isLoading}
            />
          </div>
        </Panel>

        <Panel 
          title="Security Checks"
          defaultOpen={true}
          className="mb-6"
        >
          <div className="space-y-4">
            <p className="text-sm text-muted mb-4">
              Select one or more security checks to perform on the document:
            </p>
            <div className="grid gap-4 sm:grid-cols-2">
              {checkOptions.map(option => (
                <div 
                  key={option.value}
                  className="flex p-3 rounded-lg border border-border hover:border-primary/50 transition-colors"
                >
                  <div className="mr-3 mt-1">{option.icon}</div>
                  <div className="flex-1">
                    <Checkbox
                      label={option.label}
                      description={option.description}
                      id={`check-${option.value}`}
                      checked={checks.includes(option.value as CheckType)}
                      onChange={(e) => handleCheckChange(option.value as CheckType, e.target.checked)}
                      disabled={isLoading}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </Panel>

        <Panel 
          title="Advanced Options"
          className="mb-6"
        >
          <div className="space-y-6">
            <div className="space-y-4">
              <Toggle
                label="Generate Derived Document"
                description="Create a sanitized version of the document"
                defaultChecked={generateDerived}
                onChange={setGenerateDerived}
                disabled={isLoading}
              />
              
              <Toggle
                label="Continue on Critical Failure"
                description="Continue analysis even if critical checks fail"
                defaultChecked={onCriticalFailureContinue}
                onChange={setOnCriticalFailureContinue}
                disabled={isLoading}
              />
              
              <Toggle
                label="Force OCR"
                description="Force OCR processing even if document is invalid"
                defaultChecked={forceOcr}
                onChange={setForceOcr}
                disabled={isLoading}
              />
            </div>

            {/* <div className="pt-4 border-t border-border">
              <p className="text-sm font-medium mb-2">Optional Metadata</p>
              <p className="text-xs text-muted mb-4">
                Provide additional information about the document
              </p>
              
              <div className="grid gap-4 sm:grid-cols-3">
                <Input
                  label="Document ID"
                  name="document_id"
                  placeholder="DOC-12345"
                  value={metadata.document_id}
                  onChange={handleMetadataChange}
                  disabled={isLoading}
                  fullWidth
                />
                
                <Input
                  label="Author"
                  name="author"
                  placeholder="John Doe"
                  value={metadata.author}
                  onChange={handleMetadataChange}
                  disabled={isLoading}
                  fullWidth
                />
                
                <Input
                  label="Document Type"
                  name="document_type"
                  placeholder="Contract"
                  value={metadata.document_type}
                  onChange={handleMetadataChange}
                  disabled={isLoading}
                  fullWidth
                />
              </div>
            </div> */}
          </div>
        </Panel>

        <div className="flex justify-end">
          <Button
            type="submit"
            variant="primary"
            size="lg"
            isLoading={isLoading}
            disabled={isLoading}
          >
            Submit for Analysis
          </Button>
        </div>
      </form>
    </div>
  );
};

export default FileUploadPage;