/**
 * Módulo de Resolución de Modo de Servicio (API vs Mock)
 * Sistema Web P2P — Mentorías Académicas EPIS-UPT (REL-P2P-02)
 *
 * Proporciona un mecanismo centralizado y blindado para:
 * 1. Resolver el modo operativo inicial respetando VITE_SERVICE_MODE y MODE=test.
 * 2. Prohibir terminantemente el modo mock si VITE_DISABLE_MOCK_MODE='true' o en producción (import.meta.env.PROD).
 * 3. Impedir que llamadas en tiempo de ejecución degraden a mock en entornos protegidos (Staging / Production).
 */

export function isMockModeDisabled(): boolean {
  return Boolean(
    import.meta.env.PROD ||
    import.meta.env.VITE_DISABLE_MOCK_MODE === 'true' ||
    import.meta.env.VITE_APP_ENV === 'staging' ||
    import.meta.env.VITE_STAGE === 'staging'
  );
}

export function resolveInitialServiceMode(): 'mock' | 'api' {
  if (isMockModeDisabled()) {
    return 'api';
  }
  const envMode = import.meta.env.VITE_SERVICE_MODE;
  if (envMode === 'mock') {
    return 'mock';
  }
  if (envMode === 'api') {
    return 'api';
  }
  if (import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

export function assertAllowedMode(mode: 'mock' | 'api'): 'mock' | 'api' {
  if (mode === 'mock' && isMockModeDisabled()) {
    console.error(
      'Violación de seguridad: El modo mock está estrictamente prohibido cuando VITE_DISABLE_MOCK_MODE=true o en entornos de producción/staging.'
    );
    return 'api';
  }
  return mode;
}
