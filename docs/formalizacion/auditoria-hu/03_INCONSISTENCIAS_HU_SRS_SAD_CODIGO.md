# 03 — Registro de Inconsistencias entre Documentación, Código y Comportamiento Esperado

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Etapa:** Auditoría Integral de Cumplimiento Funcional (Fase 04-B)  
**Fecha de Auditoría:** 7 de noviembre de 2026  
**Rama:** `feat/formalizacion-ux-roles`  
**Commit Auditado:** `4cbf504`  
**Estado:** Documento Oficial de Auditoría SQA  

---

## 1. Resumen de Hallazgos

La auditoría integral de trazabilidad comparó las siguientes fuentes documentales y de código:
1. **SRS de Análisis:** `docs/analisis/FD03-EPIS-Informe SRS de Proyecto.md`
2. **SRS de Diseño (Vigente):** `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` (v2.1)
3. **SAD de Diseño (Vigente):** `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` (v2.0)
4. **Plan de Sprints:** `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (v1.2)
5. **Catálogo Oficial de Pruebas:** `docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`
6. **Bitácoras e Informes de Sprints:** `docs/sprints/sprint-01` al `sprint-06`
7. **Código Fuente Backend y Frontend:** `aplicacion/backend/` y `aplicacion/frontend/`
8. **Pruebas Automatizadas:** 237 pruebas Pytest y 311 pruebas Vitest.

Se identificaron **10 discrepancias e inconsistencias estructurales**, clasificadas por severidad e impacto.

---

## 2. Matriz de Inconsistencias Detectadas

| ID Inconsistencia | Severidad | Categoría | Componentes Afectados | Descripción de la Discrepancia |
|---|:---:|---|---|---|
| **INC-01** | **Crítica (P0)** | Compilación TypeScript | `aplicacion/frontend/` (`MentorSessionsView.test.tsx`) | `npm run build` falla por TS2353 al validar propiedades inexistentes (`motivo_cancelacion`) en el mock de `QuorumDecisionResponse`. |
| **INC-02** | **Alta (P1)** | Trazabilidad de Casos de Uso | `docs/sprints/sprint-06.md`, `README.md` | El Sprint 06 rotuló la asistencia como `CUS12` y la bitácora como `CUS13`, cuando en el SRS maestro corresponden formalmente a **`CUS08` / RF17**. |
| **INC-03** | **Media (P1)** | Estilo de Código Backend | `aplicacion/backend/` | `ruff check .` pasa al 100%, pero `ruff format --check .` reporta 14 archivos desalineados sintácticamente. |
| **INC-04** | **Alta (P1)** | Seguridad Arquitectural | `app/core/dependencies.py` | La autorización JWT confía en el claim `roles` del token sin revalidar en base de datos; la revocación de un rol no invalida JWTs activos hasta su expiración (60 min). |
| **INC-05** | **Media (P2)** | Arquitectura de Despliegue | SAD FD04 vs Entorno Local / CI | SAD define Python 3.11; el entorno real y CI ejecutan **Python 3.13.5** (desviación registrada pero pendiente de homologar en texto SAD). |
| **INC-06** | **Media (P2)** | Integración de Servicios | `app/services/auth_service.py` | La autenticación OTP simula el envío SMTP en servidor local / consola; no existe integración con servidor SMTP institucional o API de correos. |
| **INC-07** | **Media (P2)** | Integración de Infraestructura | `OfferPublishView.tsx`, `offer_service.py` | El aprovisionamiento de aulas físicas y enlaces virtuales (RF09) es manual; no hay integración con Google Meet API ni bots de Discord. |
| **INC-08** | **Baja (P2)** | Gestión de Estado Cliente | `offerService.ts`, `bookingService.ts` | En modo desconectado, las ofertas se guardan en `localStorage` y existen fachadas mock para desarrollo local que deben ser desactivadas en producción. |
| **INC-09** | **Baja (P3)** | Modelo de Datos y Gobernanza | `role_service.py` | En modo memoria/desarrollo, los roles se apoyan en un diccionario de 3 cuentas semilla; la interfaz web no dispone de un catálogo general paginado de alumnos. |
| **INC-10** | **Baja (P3)** | Metodología Documental | SRS / SAD vs Sprints | Disparidad de taxonomía: el SRS/SAD utiliza Casos de Uso (CUS/UWE), mientras que los Sprints utilizan PBIs, Tareas y una serie parcial de Historias de Usuario (HU-01 a HU-08). |

---

## 3. Análisis Detallado de Discrepancias

---

### INC-01: Falla de Compilación TypeScript en `npm run build`
- **Ubicación Exacta:** `aplicacion/frontend/src/components/__tests__/MentorSessionsView.test.tsx` (líneas 79, 143, 186).
- **Causa Raíz:**
  El archivo `offerService.ts` y el backend en `app/schemas/offer.py` definen la interfaz:
  ```typescript
  export interface QuorumDecisionResponse {
    id_sesion: number;
    codigo_sesion: string;
    decision: string;
    estado_nuevo: string;
    mensaje: string;
    nueva_fecha_inicio?: string | null;
  }
  ```
  Sin embargo, en el test unitario `MentorSessionsView.test.tsx` (creado en el commit `6ee1caa` del Sprint 06), los objetos simulados incluyeron:
  ```typescript
  motivo_cancelacion: null, // o string
  ```
- **Impacto:**
  - `npm test` (Vitest) ejecuta y pasa (311 pruebas OK) porque transpila sin validación de tipos estricta por defecto.
  - `npm run lint` (ESLint) pasa (0 errores).
  - Pero `npm run build` invoca `tsc -b && vite build`. El compilador de TypeScript rechaza el exceso de propiedades con el error `TS2353: Object literal may only specify known properties, and 'motivo_cancelacion' does not exist in type 'QuorumDecisionResponse'`.
- **Acción Correctiva para Fase 05:** Remover la propiedad `motivo_cancelacion` en las 3 líneas del test o agregarla como opcional (`motivo_cancelacion?: string | null`) en `QuorumDecisionResponse`.

---

### INC-02: Colisión y Confusión en la Numeración de Casos de Uso en Sprint 06
- **Ubicación Exacta:** `docs/sprints/sprint-06.md`, `docs/sprints/sprint-06/README.md`.
- **Causa Raíz:**
  En el SRS FD03 maestro (Cuadro 5.3 y Cuadro 5.5):
  - **`CUS08`**: "Registrar bitácora y control de asistencia efectiva" (vinculado a **RF17**).
  - **`CUS12`**: "Priorización institucional de asignaturas críticas" (vinculado a **RF24**, Sprint Posterior).
  - **`CUS13`**: "Parametrización de umbrales y emisión de certificados" (vinculado a **RF22**, Sprint 08).
  Sin embargo, en la documentación del Sprint 06, el autor rotuló erróneamente:
  - "Pase de asistencia digital (CUS12)"
  - "Bitácoras pedagógicas (CUS13)"
- **Impacto:** Genera confusión en la trazabilidad cruzada con el SRS y con el Catálogo de Pruebas Excel, donde la asistencia y bitácora están registradas bajo `CUS08`.
- **Acción Correctiva para Fase 05:** Homogeneizar los encabezados y referencias de `sprint-06.md` para señalar `CUS08` (RF17).

---

### INC-03: Desalineación Sintáctica de Formato en Backend (`ruff format`)
- **Ubicación Exacta:** 14 archivos en `aplicacion/backend/app/` y `aplicacion/backend/tests/`.
- **Causa Raíz:**
  El informe de la Fase 04 reportó `ruff check .` limpio (0 errores linter). Sin embargo, `python -m ruff format --check .` detecta diferencias de espaciado y saltos de línea en 14 archivos (ej. `dependencies.py`, `offers.py`, `test_security_rbac.py`, `test_profiles.py`).
- **Impacto:** Si un pipeline de CI en el futuro activa `ruff format --check`, el build fallaría por diferencias estilísticas menores.
- **Acción Correctiva para Fase 05:** Ejecutar `python -m ruff format .` para formatear los 14 archivos automáticamente sin alterar la lógica funcional.

---

### INC-04: Limitación en la Invalidación en Caliente de Tokens JWT
- **Ubicación Exacta:** `aplicacion/backend/app/core/dependencies.py` (`get_current_user`).
- **Causa Raíz:**
  Para optimizar el rendimiento y mantener la naturaleza sin estado (*stateless*) del protocolo JWT, `get_current_user` decodifica la firma y extrae los roles directamente de `payload.get("roles")`. Si un administrador revoca el rol de mentor a un estudiante mediante `POST /api/v1/roles/revoke-mentor`, el registro en base de datos cambia inmediatamente, pero si el usuario conserva un token JWT emitido previamente con vigencia de 60 minutos, el token continuará siendo aceptado por endpoints que solo leen el payload del token.
- **Impacto:** Brecha temporal de seguridad durante la ventana de vida del token (hasta 60 minutos).
- **Acción Correctiva para Fase 05 / Producción:** Para operaciones críticas o auditoría institucional, implementar una lista de revocación en caché (Redis o tabla de tokens revocados) o revalidar los roles vigentes en base de datos cuando se ejecuten acciones privilegiadas.

---

### INC-05: Discrepancia en la Versión de Runtime de Python
- **Ubicación Exacta:** `docs/diseño/FD04-EPIS-Informe SAD de Proyecto.md` (§2.5) vs `requirements.txt` / `.venv`.
- **Causa Raíz:**
  El SAD v1.1 preliminar prescribió Python 3.11. Durante el Sprint 01, el equipo migró el entorno local y el CI a **Python 3.13.5** para asegurar compatibilidad con versiones modernas de librerías y GitHub Actions, documentando la decisión en `PLAN_SPRINTS_Y_TAREAS.md` (commit `d6bc275`). Sin embargo, el texto estático del SAD no fue actualizado.
- **Impacto:** Bajo; es una discrepancia de documentación técnica.
- **Acción Correctiva para Fase 05:** Actualizar la mención de Python 3.11 a Python 3.13 en el SAD de diseño.

---

### INC-06: Despacho SMTP Simulado en Autenticación OTP
- **Ubicación Exacta:** `aplicacion/backend/app/services/auth_service.py` (`AuthService.request_otp`).
- **Causa Raíz:**
  No se han configurado credenciales reales de un proveedor SMTP institucional (ej. servidor de correos UPT, SendGrid o Amazon SES). En desarrollo local, el sistema imprime el código OTP en la consola del servidor y admite el código estático de prueba `123456`.
- **Impacto:** Adecuado para demostraciones académicas y pruebas unitarias aisladas, pero no reproducible en producción pública sin proveedor SMTP.
- **Acción Correctiva para Fase 05:** Mantener el modo de prueba local claramente documentado en la guía de demostración para los evaluadores.

---

### INC-07: Aprovisionamiento Manual de Aulas y Enlaces (RF09)
- **Ubicación Exacta:** `aplicacion/frontend/src/components/OfferPublishView.tsx`.
- **Causa Raíz:**
  El requerimiento RF09 ("Aprovisionamiento automatizado de infraestructura") prevé la integración con Google Calendar / Meet API y bots de Discord para generar enlaces automáticamente, así como asignación algorítmica de laboratorios físicos. Dicha integración fue diferida al backlog posterior (`PB-033` y `PB-034`). Actualmente, el formulario exige que el mentor ingrese manualmente el nombre del aula o el enlace.
- **Impacto:** La publicación de ofertas funciona correctamente, pero el aprovisionamiento depende del ingreso manual del mentor.
- **Acción Correctiva para Fase 05:** Documentar explícitamente en la presentación que el aprovisionamiento automatizado pertenece a la fase de integración externa posterior.

---

### INC-08: Doble Modo (API / Mock) en Servicios Frontend
- **Ubicación Exacta:** `bookingService.ts`, `recommendationService.ts`, `offerService.ts`.
- **Causa Raíz:**
  Para permitir el desarrollo desacoplado cuando el backend no está encendido o en las pruebas unitarias de Vitest, los servicios cliente implementan una arquitectura de fachada dual (`Api...Adapter` y `Mock...Adapter`). En Vitest, el modo por defecto es `mock`.
- **Impacto:** Aunque las pruebas unitarias pasan limpiamente con mocks, para una demostración en vivo integrada se debe garantizar que la variable de entorno `VITE_SERVICE_MODE=api` se encuentre activa para conectarse a FastAPI.
- **Acción Correctiva para Fase 05:** Validar en la guía de despliegue local que el frontend apunte a `VITE_SERVICE_MODE=api`.

---

### INC-09: Cuentas Semilla en Memoria vs Base de Datos Institucional
- **Ubicación Exacta:** `aplicacion/backend/app/services/role_service.py` (`_memory_roles`).
- **Causa Raíz:**
  Si la base de datos PostgreSQL no responde o en pruebas unitarias aisladas, el servicio recurre a un diccionario con 3 cuentas (`admin.epis@upt.pe`, `mentor.avanzado@upt.pe`, `2022073504@upt.pe`).
- **Impacto:** Conveniente para pruebas reproducibles sin base de datos externa, pero no representa el padrón institucional completo.
- **Acción Correctiva para Fase 05:** Asegurar que el script de seed oficial en PostgreSQL/Supabase inserte formalmente las tuplas en la tabla `usuario_roles`.

---

### INC-10: Coexistencia de Taxonomías Scrum y UWE/RUP
- **Ubicación Exacta:** Repositorio en general (`docs/sprints` vs `docs/analisis` / `docs/diseño`).
- **Causa Raíz:**
  El proyecto combina entregables formales universitarios basados en RUP/UWE (con Casos de Uso CUS01 al CUS24) con bitácoras de Sprints ágiles (con PBIs y Tareas). Las Historias de Usuario (`HU-xx`) solo se formularon explícitamente en el Sprint 02 (HU-03 a HU-08).
- **Impacto:** Requiere la matriz maestra de trazabilidad elaborada en esta auditoría para no confundir al evaluador académico.
- **Acción Correctiva:** Mantener el catálogo y matriz de trazabilidad como referencia unificadora oficial.
