# INFORME GENERAL DE CIERRE: SPRINT 06
## «Marcación de Asistencia con Pase QR TOTP, Registro de Bitácoras con Firma SHA-256 e Historial Pedagógico»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor / Desarrollador:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Rol: Arquitectura Frontend, UI Accesible y Marcación QR (T-29, T-31, T-33)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Rol: Arquitectura Backend, Criptografía SHA-256 y Persistencia (T-30, T-32, T-34)  
**Fecha de Cierre:** 07 de Noviembre de 2026  
**Rama Base de Integración:** `main`  
**Estado:** **100% Concluido y Verificado en CI (482 Pruebas Automatizadas, 0 Fallos, Cobertura >85%)**

---

## 1. Ficha Ejecutiva del Sprint 06

| Parámetro | Valor Registrado / Evidencia Técnica |
| :--- | :--- |
| **Objetivo General** | Implementar la marcación de asistencia presencial/virtual mediante pases QR dinámicos TOTP (**RF17**, **RN-05**, **RN-12**); el registro estructurado de bitácoras pedagógicas con firma criptográfica SHA-256 en un plazo perentorio de 48 horas (**RF18**, **RN-12**); la consulta cronológica del historial académico (**RF19**); y el intercambio de recursos didácticos de sesión (**RF20**). |
| **PBI Cubiertos** | `PB-016` (Marcación de asistencia QR), `PB-017` (Bitácora docente con hash SHA-256), `PB-018` (Historial de sesiones y bitácoras), `PB-019` (Recursos didácticos). |
| **Requerimientos Trazados** | `RF17`, `RF18`, `RF19`, `RF20`, `RNF02`, `RNF05`, `RNF09`. |
| **Casos de Uso Abordados** | `CUS-012` (Registrar asistencia QR), `CUS-013` (Registrar bitácora docente), `CUS-014` (Visualizar historial y bitácoras). |
| **Reglas de Negocio** | `RN-05` (Aforo reglamentario), `RN-12` (Registro de bitácora en 48h y filtro de evaluación). |
| **Suites de Pruebas** | **482 pruebas automatizadas sin fallos** (234 backend Pytest / 248 frontend Vitest). |
| **Cobertura de Código** | Backend: 88.5% — Frontend: 84.1% (Superando el umbral del 70% de **RNF09**). |
| **Linteo y Formato** | 0 defectos en Ruff (Python) — 0 advertencias y 0 errores en ESLint 9 (React 18 / TypeScript). |

---

## 2. Componentes Construidos y Verificados

1. **Frontend UI/UX (Joan Medina):**
   - `QrPassView.tsx` / `QrScannerView.tsx`: Emisión y escaneo reactivo de pases QR TOTP con auto-refresco y contraste accesible.
   - `BitacoraRegisterView.tsx`: Formulario de cierre docente con selector de temas silábicos, control de asistencia efectiva y visualización de hash SHA-256.
   - `BitacoraHistoryView.tsx`: Historial cronológico con filtros por asignatura y visualización de observaciones docentes.
   - `SessionResourcesView.tsx`: Gestor de descarga de enlaces a diapositivas y repositorios de código.
2. **Backend API y Servicios (Renzo Antayhua):**
   - `app/api/v1/endpoints/attendance.py`: Endpoints `/api/v1/attendance/qr-pass` y `/api/v1/attendance/scan-qr`.
   - `app/api/v1/endpoints/bitacora.py`: Endpoints `/api/v1/bitacora/sessions/{id}` y `/api/v1/bitacora/history`.
   - `app/services/attendance_service.py`: Generador y validador de tokens efímeros HMAC-SHA256 con ventana de 60 segundos.
   - `app/services/bitacora_service.py`: Generador de hash criptográfico inmutable SHA-256 y validador de ventana temporal de 48 horas post-sesión (**RN-12**).
