import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  isMockModeDisabled,
  resolveInitialServiceMode,
  assertAllowedMode,
} from '../serviceMode';

describe('serviceMode (REL-P2P-02 / Hardening de Entornos y Modo Staging)', () => {
  beforeEach(() => {
    vi.stubEnv('PROD', false);
    vi.stubEnv('VITE_DISABLE_MOCK_MODE', '');
    vi.stubEnv('VITE_APP_ENV', 'development');
    vi.stubEnv('VITE_STAGE', 'dev');
    vi.stubEnv('VITE_SERVICE_MODE', 'api');
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it('determina que el modo mock está deshabilitado en compilaciones de producción (PROD=true)', () => {
    vi.stubEnv('PROD', true);
    expect(isMockModeDisabled()).toBe(true);
    expect(resolveInitialServiceMode()).toBe('api');
    expect(assertAllowedMode('mock')).toBe('api');
  });

  it('determina que el modo mock está deshabilitado cuando VITE_DISABLE_MOCK_MODE="true"', () => {
    vi.stubEnv('VITE_DISABLE_MOCK_MODE', 'true');
    vi.stubEnv('VITE_SERVICE_MODE', 'mock');
    expect(isMockModeDisabled()).toBe(true);
    expect(resolveInitialServiceMode()).toBe('api');
    expect(assertAllowedMode('mock')).toBe('api');
  });

  it('determina que el modo mock está deshabilitado en staging (VITE_APP_ENV="staging")', () => {
    vi.stubEnv('VITE_APP_ENV', 'staging');
    expect(isMockModeDisabled()).toBe(true);
    expect(resolveInitialServiceMode()).toBe('api');
    expect(assertAllowedMode('mock')).toBe('api');
  });

  it('determina que el modo mock está deshabilitado en staging (VITE_STAGE="staging")', () => {
    vi.stubEnv('VITE_STAGE', 'staging');
    expect(isMockModeDisabled()).toBe(true);
    expect(resolveInitialServiceMode()).toBe('api');
  });

  it('resuelve "api" cuando VITE_SERVICE_MODE="api" en entornos no productivos', () => {
    vi.stubEnv('VITE_SERVICE_MODE', 'api');
    expect(isMockModeDisabled()).toBe(false);
    expect(resolveInitialServiceMode()).toBe('api');
    expect(assertAllowedMode('api')).toBe('api');
  });

  it('resuelve "mock" cuando VITE_SERVICE_MODE="mock" en entorno de desarrollo', () => {
    vi.stubEnv('VITE_SERVICE_MODE', 'mock');
    expect(isMockModeDisabled()).toBe(false);
    expect(resolveInitialServiceMode()).toBe('mock');
    expect(assertAllowedMode('mock')).toBe('mock');
  });

  it('permite assertAllowedMode("api") en cualquier circunstancia', () => {
    vi.stubEnv('VITE_DISABLE_MOCK_MODE', 'true');
    expect(assertAllowedMode('api')).toBe('api');
  });
});
