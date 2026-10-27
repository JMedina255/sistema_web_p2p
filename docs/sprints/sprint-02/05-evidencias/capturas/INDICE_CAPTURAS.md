# Índice de Capturas de Pantalla del Sistema — Sprint 02

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Sprint:** 02 — Roles, Currículo, Perfiles y Consentimiento Informado (Ley N° 29733)  
**Commit de Corte:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74) / [`786dd62`](https://github.com/JMedina255/sistema_web_p2p/commit/786dd621d024e2def6383e1d925ef36a3f8ea72f)  
**Ubicación canónica:** `docs/sprints/sprint-02/05-evidencias/capturas/`  
**Ubicación histórica de respaldo:** `docs/diseño/imagenes/sprint-02/`

---

## Inventario de Capturas del Incremento Operativo

| N° | Archivo | Funcionalidad Demostrada | Requisito Satisfecho | Tarea | Componentes de Implementación |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **01** | [`01_consent_modal_ley29733.png`](01_consent_modal_ley29733.png) | Formulario modal accesible de consentimiento digital para tratamiento de datos personales bajo la **Ley N° 29733**, con cláusulas de finalidad académica y bloqueo preventivo ante rechazo voluntario. | **RF02**, **RNF02**, **RN-02** | **T-04** (Joan), **T-05** (Renzo) | Frontend: `ConsentModalView.tsx`, `consentService.ts`<br>Backend: `consent.py`, `consent_service.py`<br>BD: tabla `consentimientos_legales` |
| **02** | [`02_curriculum_advanced_search.png`](02_curriculum_advanced_search.png) | Interfaz interactiva de consulta avanzada del catálogo curricular con búsqueda predictiva en tiempo real, desglose por ciclo formativo y navegación temática silábica profunda. | **RF05**, **CUS21** | **T-10** (Joan) | Frontend: `CurriculumCatalogView.tsx`<br>Backend: `curriculum.py`<br>BD: tablas `asignaturas_filtro`, `temas_conceptuales` |
| **03** | [`03_profile_merit_validation.png`](03_profile_merit_validation.png) | Verificación de mérito académico institucional conforme a la regla **RN-03**, mostrando advertencia preventiva en frontend y denegación en backend (**HTTP 400 `MERIT_RULE_VIOLATION`**) si `ciclo_actual < 7`. | **RF03**, **RN-03**, **CUS10** | **T-08** (Renzo), **T-11** (Joan) | Frontend: `ProfileAvailabilityView.tsx`<br>Backend: `roles.py`, `role_service.py`<br>BD: tablas `roles`, `usuario_roles` |
| **04** | [`04_weekly_availability_grid.png`](04_weekly_availability_grid.png) | Formulario de perfil formativo y grilla interactiva de disponibilidad semanal de **6 días (Lunes a Sábado) × 11 franjas horarias (08:00 a 19:00)** con selección matricial y reemplazo atómico transaccional. | **RF04**, **CUS15** | **T-11** (Joan), **T-12** (Renzo) | Frontend: `ProfileAvailabilityView.tsx`, `profileService.ts`<br>Backend: `profiles.py`, `profile_service.py`<br>BD: tablas `perfiles_academicos`, `disponibilidades_horarias` |
| **05** | [`05_swagger_api_docs_sprint02.png`](05_swagger_api_docs_sprint02.png) | Documentación técnica interactiva de la API REST mediante Swagger UI / OpenAPI v3, evidenciando contratos fuertemente tipados con esquemas Pydantic v2 y códigos de estado HTTP estandarizados. | **RNF09** | **T-05**, **T-08**, **T-12** (Renzo) | Backend: `app/main.py`, routers `/api/v1/consent`, `/api/v1/roles`, `/api/v1/profiles`<br>Esquemas: `app/schemas/` |
| **06** | [`06_backend_pytest_coverage_sprint02.png`](06_backend_pytest_coverage_sprint02.png) | Reporte empírico de ejecución y cobertura de pruebas automatizadas en backend con Pytest y Pytest-Cov (**84 pruebas pasando al 100%, 0 fallos, 90.64% de cobertura de código** al corte de S2). | **RNF09** | **T-05**, **T-08**, **T-12**, **T-13** (Renzo) | Backend: suites `test_consent.py`, `test_roles.py`, `test_profiles.py`, `test_authorization.py` |
| **07** | [`07_frontend_vitest_coverage_sprint02.png`](07_frontend_vitest_coverage_sprint02.png) | Reporte empírico de ejecución y cobertura de pruebas automatizadas en frontend con Vitest y Testing Library (**66 pruebas pasando al 100%, 0 fallos, 91.10% de cobertura de código** al commit `3766a08`). | **RNF09** | **T-04**, **T-10**, **T-11** (Joan) | Frontend: suites `ConsentModalView.test.tsx`, `CurriculumCatalogView.test.tsx`, `ProfileAvailabilityView.test.tsx`, `consentService.test.ts`, `profileService.test.ts` |

---

*Nota de integridad:* Las presentes capturas corresponden a ejecuciones verificables del sistema sobre la rama `feat/sprint-02-roles-curriculo-perfiles` y no constituyen maquetas o prototipos estáticos ilustrativos.
