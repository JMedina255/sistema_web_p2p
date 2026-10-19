export interface HealthResponse {
  status: string;
  service: string;
  project: string;
  environment: string;
}

export type HealthState =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: HealthResponse; latencyMs: number }
  | { status: 'error'; message: string };
