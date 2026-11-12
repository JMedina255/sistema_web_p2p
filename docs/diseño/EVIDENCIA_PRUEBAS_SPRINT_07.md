# Documento de Evidencia y Catálogo de Pruebas Automatizadas: Sprint 07
## «Gamificación, Insignias, Parametrización y Certificados PDF con QR (554 Pruebas Automatizadas)»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (2026-II)  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)  
**Estado:** **554 de 554 Pruebas Superadas (100% Satisfactorio, 0 Fallos, Cobertura >85%)**

---

## Resumen Ejecutivo de Pruebas

| Métrica | Backend (Pytest) | Frontend (Vitest) | Total Consolidado |
| :--- | :---: | :---: | :---: |
| **Suites de Pruebas** | 18 suites | 28 suites | **46 suites** |
| **Pruebas Aprobadas** | 260 casos | 294 casos | **554 casos (100% éxito)** |
| **Cobertura de Código**| 89.2% | 84.8% | **>85% Cobertura Global** |

### Principales Suites Verificadas:
- `test_certificates.py`: 16 pruebas de control de umbral de 20 horas auditadas, compilación PDF ReportLab y verificación de hash SHA-256.
- `CertificateDownloadView.test.tsx`: 5 pruebas de renderizado de folio, descarga de blob binario y visualización de QR.
- `certificateService.test.ts`: 8 pruebas de validación de contratos tipados y captura de errores HTTP 400 (`INSUFFICIENT_HOURS`).
