
// beeter
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Shield, AlertCircle, CheckCircle, XCircle, FileText, Download } from 'lucide-react';

import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import ProgressBar from '../components/ui/ProgressBar';
import Panel from '../components/ui/Panel';
import Badge from '../components/ui/Badge';
import { AnalysisResponse, CheckReportItem, ValidoStatus } from '../types';
import api from '../services/api';
import dbService from '../services/database';

const StatusPage: React.FC = () => {
  const { jobId: urlJobId } = useParams<{ jobId?: string }>();
  const [jobId, setJobId] = useState(urlJobId && urlJobId !== 'undefined' ? urlJobId : '');
  const [jobData, setJobData] = useState<AnalysisResponse | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [derivedUrl, setDerivedUrl] = useState('');

  const fetchJobStatus = async (id: string) => {
    if (!id) return;
    setIsLoading(true);
    setError('');
    try {
      const response = await api.getJobStatus(id);
      setJobData(response);
      const ocrCheck = response.result?.checks?.find(
        (c) => c.name === 'ocr'
      );
      setDerivedUrl(ocrCheck ? `http://localhost:5001/download/ocr/${id}` : '');

      await dbService.updateFileRecord(id, {
        status: response.status,
        result_json: JSON.stringify(response.result, null, 2),
      });

      setIsPolling(response.status === 'queued' || response.status === 'processing');
    } catch (err) {
      console.error('Error fetching job status:', err);
      setError('Failed to fetch job status');
      setIsPolling(false);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (jobId) fetchJobStatus(jobId);
  }, [jobId]);

  useEffect(() => {
    let interval: number | undefined;
    if (isPolling) {
      interval = window.setInterval(() => fetchJobStatus(jobId), 3000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPolling, jobId]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobId) return setError('Please enter a job ID');
    fetchJobStatus(jobId);
  };

  const statusColors: Record<string, string> = {
    queued: 'bg-muted text-foreground',
    processing: 'bg-primary text-white',
    done: 'bg-success text-white',
    failed: 'bg-error text-white',
  };

  const validoStatusConfig: Record<ValidoStatus, { icon: JSX.Element; color: string }> = {
    VALID: { icon: <CheckCircle className="w-5 h-5" />, color: 'success' },
    INVALID: { icon: <XCircle className="w-5 h-5" />, color: 'error' },
    UNKNOWN: { icon: <AlertCircle className="w-5 h-5" />, color: 'warning' },
  };

  const checkResultConfig: Record<string, { icon: JSX.Element; color: string }> = {
    PRESENT: { icon: <CheckCircle className="w-5 h-5" />, color: 'warning' },
    NOT_DETECTED: { icon: <CheckCircle className="w-5 h-5" />, color: 'success' },
    ERROR: { icon: <AlertCircle className="w-5 h-5" />, color: 'error' },
    SKIPPED: { icon: <AlertCircle className="w-5 h-5" />, color: 'muted' },
  };

  const checkTypeIcons: Record<string, JSX.Element> = {
    macro: <FileText className="w-5 h-5 text-warning" />,
    ads: <AlertCircle className="w-5 h-5 text-error" />,
    password: <Shield className="w-5 h-5 text-primary" />,
    steganography: <FileText className="w-5 h-5 text-secondary" />,
    ocr: <FileText className="w-5 h-5 text-accent" />,
  };

  const renderCheckResult = (check: CheckReportItem) => {
    const config = checkResultConfig[check.result] || checkResultConfig.ERROR;
    const icon = checkTypeIcons[check.name] || <FileText className="w-5 h-5" />;
    return (
      <Panel key={check.name} title={
        <div className="flex items-center justify-between w-full">
          <div className="flex items-center">{icon}<span className="ml-2 capitalize">{check.name} Check</span></div>
          <Badge variant={config.color as any} size="md" className="flex items-center space-x-1">
            {config.icon}<span>{check.result}</span>
          </Badge>
        </div>
      } className="mb-4">
        <div className="space-y-2">
          {check.error && (
            <div className="p-3 bg-error/10 border border-error/20 rounded text-sm">
              <p className="font-medium">Error:</p>
              {/* <p>{check.error}</p> */}
              <p>{typeof check.error === 'string' ? check.error : JSON.stringify(check.error)}</p>
            </div>
          )}
        </div>
      </Panel>
    );
  };

  // Check if derived results should be enabled
  const shouldEnableDerivedResults = (jobData?.result &&
    jobData.result.force_ocr_even_if_invalid === 1 && jobData.result.checks) ||  (jobData?.result &&
    jobData.result.generate_derived === 1);

  return (
    <div className="max-w-4xl mx-auto animate-fade-in">
      <div className="flex items-center mb-6">
        <Shield className="mr-3 h-8 w-8 text-primary" />
        <h1 className="text-2xl font-bold">Job Status</h1>
      </div>

      {!urlJobId && (
        <form onSubmit={handleSubmit} className="mb-8">
          <Panel title="Check Job Status" defaultOpen={true}>
            <div className="flex flex-col md:flex-row gap-4">
              <Input label="Job ID" value={jobId} onChange={(e) => setJobId(e.target.value)} placeholder="Enter job ID" fullWidth className="flex-1" />
              <div className="flex items-end">
                <Button type="submit" variant="primary" isLoading={isLoading} disabled={isLoading || !jobId}>Check Status</Button>
              </div>
            </div>
            {error && <div className="mt-4 text-sm text-error">{error}</div>}
          </Panel>
        </form>
      )}

      {jobData?.status && (
        <div>
          <div className="bg-card rounded-lg border p-6 mb-6">
            <div className="flex flex-col md:flex-row justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold mb-1">Job: {jobData.job_id}</h2>
                <div className="flex items-center">
                  <span className={`inline-block w-2 h-2 rounded-full mr-2 ${statusColors[jobData.status] || 'bg-muted'}`} />
                  <Badge variant={statusColors[jobData.status] || 'default'}>
                    {(jobData.status || 'unknown').toUpperCase()}
                  </Badge>
                </div>
              </div>

              <div className="mt-4 md:mt-0 flex gap-3">
                <a
                  href={`http://127.0.0.1:5001/download/json/${jobData.job_id}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 border border-gray-300 rounded bg-white hover:bg-gray-100 flex items-center"
                  download
                >
                  <Download className="w-4 h-4 mr-2" />
                  Download Results
                </a>

                {shouldEnableDerivedResults ? (
                  <a
                    href={`http://127.0.0.1:5001/download/ocr/${jobData.job_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 border border-gray-300 rounded bg-white hover:bg-gray-100 flex items-center"
                    download
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Derived Results
                  </a>
                ) : (
                  <button
                    disabled
                    className="px-4 py-2 border border-gray-200 rounded bg-gray-100 text-gray-400 flex items-center cursor-not-allowed"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Derived Results
                  </button>
                )}
              </div>
            </div>

            {(jobData.status === 'queued' || jobData.status === 'processing') && (
              <ProgressBar value={jobData.progress} max={100} label="Processing" variant="primary" animated />
            )}
          </div>

          {jobData.result && (
            <div className="space-y-6">
              <div className="bg-card rounded-lg border p-6 mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold">Analysis Results</h2>
                  <Badge
                    variant={validoStatusConfig[jobData.result.valido_status]?.color || 'warning'}
                    size="lg"
                    className="flex items-center space-x-2"
                  >
                    {validoStatusConfig[jobData.result.valido_status]?.icon}
                    <span>{jobData.result.valido_status || 'UNKNOWN'}</span>
                  </Badge>
                </div>
              </div>

              <h3 className="font-bold text-lg mb-3">Security Check Results</h3>
              <div className="space-y-3">
                {jobData.result.checks.map(renderCheckResult)}
              </div>
            </div>
          )}

          <div className="mt-8 text-center">
            <Link to="/">
              <Button variant="outline">Upload Another Document</Button>
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatusPage;