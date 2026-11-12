# INFORME GENERAL DE CIERRE: SPRINT 07
## «Gamificación e Insignias del Mentor, Parametrización Institucional y Emisión Digital de Certificados con Código QR»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor / Desarrollador:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Rol: Arquitectura Frontend, Gamificación UI y Descarga de Certificados (T-35, T-37, T-39, T-41)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Rol: Arquitectura Backend, Motor PDF ReportLab y Auditoría de Horas (T-36, T-38, T-40, T-42)  
**Fecha de Cierre:** 10 de Noviembre de 2026  
**Rama Base de Integración:** `main`  
**Estado:** **100% Concluido y Verificado en CI (554 Pruebas Automatizadas, 0 Fallos, Cobertura >85%)**

---

## 1. Ficha Ejecutiva del Sprint 07

| Parámetro | Valor Registrado / Evidencia Técnica |
| :--- | :--- |
| **Objetivo General** | Materializar el subsistema de gamificación con cálculo dinámico de reputación y tablero de insignias (**RF21**, **RN-13**); la parametrización institucional de umbrales y autorización de certificados por la Dirección de Escuela (**RF22**, **RN-14**); y la generación digital de certificados oficiales en formato PDF con folio correlativo único, hash SHA-256 y código QR de verificación institucional (**RF23**). |
| **PBI Cubiertos** | `PB-020` (Reputación e insignias de mérito), `PB-021` (Umbral de horas y autorización), `PB-022` (Emisión digital de certificados PDF con QR). |
| **Requerimientos Trazados** | `RF21`, `RF22`, `RF23`, `RNF02`, `RNF05`, `RNF09`. |
| **Casos de Uso Abordados** | `CUS-018` (Emitir constancia institucional de horas), `CUS-019` (Gestionar insignias y reputación gamificada). |
| **Reglas de Negocio** | `RN-13` (Encuestas de calidad y reputación en 24h), `RN-14` (Certificación con mínimo 20 horas auditadas). |
| **Suites de Pruebas** | **554 pruebas automatizadas sin fallos** (260 backend Pytest / 294 frontend Vitest). |
| **Cobertura de Código** | Backend: 89.2% — Frontend: 84.8% (Superando ampliamente el umbral del 70% de **RNF09**). |
| **Linteo y Formato** | 0 defectos en Ruff (Python) — 0 advertencias y 0 errores en ESLint 9 (React 18 / TypeScript). |

---

## 2. Componentes Construidos y Verificados

1. **Frontend UI/UX (Joan Medina):**
   - `MentorBadgesView.tsx`: Tablero interactivo de reputación estelar e insignias desbloqueadas por mérito pedagógico.
   - `AdminCertificatesView.tsx`: Panel administrativo de revisión de horas auditadas y autorización de emisión de certificados.
   - `CertificateDownloadView.tsx`: Vista de descarga de certificados PDF con visor integrado y enlace de verificación pública.
2. **Backend API y Servicios (Renzo Antayhua):**
   - `app/api/v1/endpoints/certificates.py`: Endpoints de autorización, generación binaria y verificación pública con código QR.
   - `app/services/gamification_service.py`: Algoritmo de actualización de reputación y evaluador de insignias automáticas.
   - `app/services/certificate_service.py`: Validador del umbral mínimo de 20 horas (**RN-14**) y asignador de folios únicos.
   - `app/services/pdf_generator_service.py`: Motor programático ReportLab que compila el expediente PDF/A con firmas institucionales y QR vectorial.
