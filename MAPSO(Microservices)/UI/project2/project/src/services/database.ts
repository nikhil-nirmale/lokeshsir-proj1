import { FileRecord } from '../types';

class MockDatabase {
  private records: Map<string, FileRecord> = new Map();
  private idCounter: number = 1;
  
  async initDatabase(): Promise<void> {
    console.log('Mock database initialized');
    return Promise.resolve();
  }
  
  async saveFileRecord(record: Omit<FileRecord, 'id' | 'created_at' | 'updated_at'>): Promise<string> {
    const id = this.idCounter++;
    const now = new Date().toISOString();
    
    const fullRecord: FileRecord = {
      id,
      ...record,
      created_at: now,
      updated_at: now,
    };
    
    this.records.set(record.job_id, fullRecord);
    return record.job_id;
  }
  
  async updateFileRecord(
    jobId: string, 
    updates: Partial<Omit<FileRecord, 'id' | 'job_id' | 'created_at' | 'updated_at'>>
  ): Promise<void> {
    const record = this.records.get(jobId);
    
    if (!record) {
      return;
    }
    
    const updated = {
      ...record,
      ...updates,
      updated_at: new Date().toISOString(),
    };
    
    this.records.set(jobId, updated);
  }
  
  async getFileRecordByJobId(jobId: string): Promise<FileRecord | null> {
    return this.records.get(jobId) || null;
  }
  
  async getRecentFileRecords(limit: number = 20): Promise<FileRecord[]> {
    return Array.from(this.records.values())
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, limit);
  }
  
  generateJsonDownloadUrl(jsonData: string): string {
    return `data:application/json;base64,${btoa(jsonData)}`;
  }
}

// Create mock database instance and export it directly
const dbService = new MockDatabase();

export default dbService;