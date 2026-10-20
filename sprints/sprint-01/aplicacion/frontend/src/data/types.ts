export interface HealthResponse {
  status: string;
  service: string;
  project: string;
  environment: string;
}

export interface DbHealthResponse {
  status: string;
  database: string;
  detail: string;
  latency_ms: number;
  environment: string;
}

export type HealthState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: HealthResponse; latencyMs: number; dbData?: DbHealthResponse }
  | { status: 'error'; message: string };
