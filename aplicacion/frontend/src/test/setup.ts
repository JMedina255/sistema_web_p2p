import '@testing-library/jest-dom/vitest';

// Asegurar modo mock predeterminado durante pruebas unitarias desconectadas en Vitest
if (typeof import.meta !== 'undefined' && import.meta.env) {
  import.meta.env.VITE_SERVICE_MODE = 'mock';
}
