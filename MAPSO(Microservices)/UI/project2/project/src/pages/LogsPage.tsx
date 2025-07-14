import React, { useState, useEffect } from 'react';
import { Shield, Filter } from 'lucide-react';

import Panel from '../components/ui/Panel';
import Badge from '../components/ui/Badge';
import Button from '../components/ui/Button';
import { LogEntry, ValidoStatus } from '../types';
import api from '../services/api';

const LogsPage: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<{
    outcome?: ValidoStatus;
    search?: string;
  }>({});

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const logsData = await api.getLogs();
      setLogs(logsData);
    } catch (err) {
      console.error('Error fetching logs:', err);
      setError('Failed to fetch logs. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilter = (outcome?: ValidoStatus) => {
    setFilter(prev => ({
      ...prev,
      outcome: prev.outcome === outcome ? undefined : outcome,
    }));
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilter(prev => ({
      ...prev,
      search: e.target.value,
    }));
  };

  const filteredLogs = logs.filter(log => {
    if (filter.outcome && log.outcome !== filter.outcome) {
      return false;
    }
    
    if (filter.search) {
      const searchTerm = filter.search.toLowerCase();
      return (
        log.document_id.toLowerCase().includes(searchTerm) ||
        log.filename.toLowerCase().includes(searchTerm)
      );
    }
    
    return true;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatDuration = (ms: number) => {
    if (ms < 1000) {
      return `${ms}ms`;
    }
    return `${(ms / 1000).toFixed(2)}s`;
  };

  return (
    <div className="max-w-6xl mx-auto animate-fade-in">
      <div className="flex items-center mb-6">
        <Shield className="mr-3 h-8 w-8 text-primary" />
        <h1 className="text-2xl font-bold">System Logs</h1>
      </div>

      <Panel
        title="Log Viewer"
        defaultOpen={true}
        className="mb-6"
      >
        <div className="mb-4">
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <div className="relative flex-1">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg className="h-5 w-5 text-muted" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                type="search"
                className="input pl-10 w-full"
                placeholder="Search by filename or document ID"
                onChange={handleSearch}
              />
            </div>
            <div className="flex space-x-2">
              <Button
                variant={filter.outcome === 'VALID' ? 'success' : 'outline'}
                onClick={() => handleFilter('VALID')}
                leftIcon={<Filter className="w-4 h-4" />}
              >
                Valid
              </Button>
              <Button
                variant={filter.outcome === 'INVALID' ? 'error' : 'outline'}
                onClick={() => handleFilter('INVALID')}
                leftIcon={<Filter className="w-4 h-4" />}
              >
                Invalid
              </Button>
            </div>
          </div>

          {error && (
            <div className="p-4 bg-error/10 border border-error/20 rounded-lg text-error">
              {error}
            </div>
          )}

          {isLoading ? (
            <div className="text-center py-8">
              <div className="inline-block w-8 h-8 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
              <p className="mt-2 text-muted">Loading logs...</p>
            </div>
          ) : filteredLogs.length === 0 ? (
            <div className="text-center py-8 bg-muted/5 border border-border rounded-lg">
              <p className="text-muted">No logs found</p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b border-border bg-muted/5">
                    <th className="px-4 py-3 text-left text-sm font-medium">Timestamp</th>
                    <th className="px-4 py-3 text-left text-sm font-medium">Document</th>
                    <th className="px-4 py-3 text-left text-sm font-medium">Checks</th>
                    <th className="px-4 py-3 text-left text-sm font-medium">Outcome</th>
                    <th className="px-4 py-3 text-left text-sm font-medium">Duration</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {filteredLogs.map((log, index) => (
                    <tr 
                      key={index}
                      className="hover:bg-muted/5 transition-colors"
                    >
                      <td className="px-4 py-3 text-sm">
                        {formatDate(log.timestamp)}
                      </td>
                      <td className="px-4 py-3">
                        <div className="text-sm font-medium">{log.filename}</div>
                        <div className="text-xs text-muted">ID: {log.document_id}</div>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex flex-wrap gap-1">
                          {log.checks.map(check => (
                            <Badge key={check} variant="primary" size="sm">
                              {check}
                            </Badge>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3">
                        <Badge
                          variant={log.outcome === 'VALID' ? 'success' : 'error'}
                        >
                          {log.outcome}
                        </Badge>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {formatDuration(log.duration_ms)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </Panel>
    </div>
  );
};

export default LogsPage;