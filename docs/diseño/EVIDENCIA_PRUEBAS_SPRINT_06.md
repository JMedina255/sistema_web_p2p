# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 06
## «Marcación de Asistencia QR TOTP, Bitácora Docente con Firma SHA-256 e Historial (482 Pruebas Automatizadas)»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Estado:** **482 de 482 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Cobertura >85%)**

---

## Resumen Ejecutivo de Pruebas

| Métrica | Backend (Pytest) | Frontend (Vitest) | Total Consolidado |
| :--- | :---: | :---: | :---: |
| **Suites de Pruebas** | 16 suites | 24 suites | **40 suites** |
| **Pruebas Aprobadas** | 234 casos | 248 casos | **482 casos (100% éxito)** |
| **Cobertura de Código**| 88.5% | 84.1% | **>85% Cobertura Global** |

### Principales Suites Verificadas:
- `test_attendance.py`: 8 pruebas unitarias/integración de generación y verificación de tokens TOTP QR y control de asistencia efectiva.
- `test_bitacora.py`: 12 pruebas de validación de plazo de 48h, cálculo de hash SHA-256 inmutable y persistencia relacional.
- `SessionAttendanceView.test.tsx`: 5 pruebas de interacción visual, escaneo y marcado manual de asistencia.
- `BitacoraFormView.test.tsx`: 5 pruebas de bloqueo por expiración de 48h y despacho estructurado con firma criptográfica.
