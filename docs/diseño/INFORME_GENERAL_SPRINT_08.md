# INFORME GENERAL DE CIERRE: SPRINT 08
## «Priorización de Asignaturas Críticas, Tablero de Analítica Institucional, Auditoría Administrativa y Cierre del Sistema»

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor / Desarrollador:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Rol: Arquitectura Frontend, Tableros Analíticos y Accesibilidad (T-43, T-45, T-47, T-49, T-51)  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Rol: Arquitectura Backend, Analítica OLAP, Auditoría de Trazas y Cierre (T-44, T-46, T-48, T-50)  
**Fecha de Cierre:** 12 de Noviembre de 2026  
**Rama Base de Integración:** `main`  
**Estado:** **100% Concluido y Verificado en CI (627 Pruebas Automatizadas, 0 Fallos, Cobertura >85%) — SISTEMA COMPLETO Y LISTO PARA PILOTO INSTITUCIONAL**

---

## 1. Ficha Ejecutiva del Sprint 08

| Parámetro | Valor Registrado / Evidencia Técnica |
| :--- | :--- |
| **Objetivo General** | Formalizar la priorización administrativa de materias críticas con realce algorítmico (**RF24**, **RN-11**); desplegar el tablero directivo de analítica académica y métricas de retención ICACIT (**RF25**); e instrumentar el panel de auditoría administrativa de bitácoras, validación de horas y verificación de consentimientos Ley N° 29733 (**RF26**), culminando la totalidad de requerimientos del sistema. |
| **PBI Cubiertos** | `PB-023` (Priorización de materias filtro), `PB-024` (Tablero analítico institucional), `PB-025` (Auditoría administrativa de bitácoras y gobernanza). |
| **Requerimientos Trazados** | `RF24`, `RF25`, `RF26`, `RNF02`, `RNF03`, `RNF04`, `RNF09`. |
| **Casos de Uso Abordados** | `CUS-020` (Configurar parámetros institucionales), `CUS-011` / `CUS-015` (Generar reportes y métricas de analítica), `CUS-016` / `CUS-022` (Auditar trazas de seguridad y gestionar catálogo). |
| **Reglas de Negocio** | `RN-02` (Inmutabilidad de consentimientos), `RN-11` (Ponderación algorítmica de asignaturas críticas), `RN-14` (Visado y auditoría de horas computables). |
| **Suites de Pruebas** | **627 pruebas automatizadas sin fallos** (280 backend Pytest / 347 frontend Vitest) distribuidas en 56 suites. |
| **Cobertura de Código** | Backend: 89.6% — Frontend: 85.2% (Superando ampliamente el umbral del 70% de **RNF09**). |
| **Linteo y Formato** | 0 defectos en Ruff (Python) — 0 advertencias y 0 errores en ESLint 9 (React 18 / TypeScript). |
| **Compilación Frontend**| Empaquetamiento de producción limpio en Vite (`dist/`), cero advertencias de tipos TypeScript (`tsc -b`). |

---

## 2. Componentes Construidos y Verificados

1. **Frontend UI/UX (Joan Medina):**
   - `AdminAnalyticsView.tsx`: Tablero de analítica gerencial con gráficos de demanda, tasas de ausentismo y distribución de sesiones.
   - `AdminAuditView.tsx`: Panel de auditoría de trazas de seguridad, fiscalización de bitácoras y consentimientos bajo la Ley N° 29733.
   - `AdminSettingsView.tsx`: Formulario de configuración de umbrales semestrales, aforos y materias prioritarias.
2. **Backend API y Servicios (Renzo Antayhua):**
   - `app/api/v1/endpoints/analytics.py`: Endpoints de consolidación de KPIs institucionales agregados y anonimizados.
   - `app/api/v1/endpoints/audit.py`: Endpoints de fiscalización administrativa de bitácoras y trazas de auditoría.
   - `app/services/analytics_service.py`: Motor analítico OLAP que computa indicadores de retención estudiantil y eficiencia pedagógica.
   - `app/services/audit_service.py`: Gestor de consultas de auditoría y visado formal de horas de mentoría.
