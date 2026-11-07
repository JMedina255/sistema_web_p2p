# 04 — Plan Maestro de Refactorización y Formalización del Sistema Web P2P

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)  
**Rama:** `feat/formalizacion-ux-roles`  
**Directorio de Trabajo:** `C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion`  
**Fecha de Elaboración:** 7 de noviembre de 2026  
**Documentos Relacionados:**  
- [`01_DIAGNOSTICO_INICIAL.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/formalizacion/01_DIAGNOSTICO_INICIAL.md)  
- [`02_INVENTARIO_INTERFACES.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/formalizacion/02_INVENTARIO_INTERFACES.md)  
- [`03_MATRIZ_ROLES_PERMISOS.md`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/docs/formalizacion/03_MATRIZ_ROLES_PERMISOS.md)  

---

## 1. Visión General y Principios de la Refactorización

El objetivo de esta intervención es convertir el Sistema Web P2P en una aplicación web interactiva, limpia, institucional y profesional, adecuada para la evaluación y demostración formal ante la cátedra y autoridades de la Escuela Profesional de Ingeniería de Sistemas.

### Principios Rectores:
1. **Preservación Incondicional de la Lógica de Negocio:** No se alteran algoritmos de recomendación, fórmulas de similitud (Jaccard/Dice), reglas de mérito (RN-03), aforos estándar (RN-05), cortes temporales (RN-08) ni transacciones pesimistas de concurrencia (RNF07).
2. **Desacoplamiento Estricto entre Documentación e Interfaz:** Los códigos de trazabilidad (`RF01`, `RN-05`, `CUS12`, `T-24`, etc.) permanecen íntegramente en los documentos SRS, SAD, bitácoras y comentarios de código, pero **se eliminan por completo de las vistas del usuario final**.
3. **Seguridad y Aislamiento por Defecto:** Ningún componente expondrá identidades ni datos ficticios hardcodeados. El acceso a cada vista dependerá de la autenticación institucional y el rol activo.
4. **Cero Regresiones Automatizadas:** Cada fase deberá verificar la estabilidad de la batería consolidada de pruebas unitarias y de integración.

---

## 2. Cronograma de Fases de Intervención (Fases 02 a 06)

```
[ Fase 01: Auditoría y Plan ]  <-- (Fase Actual Completada)
        │
        ▼
[ Fase 02: Limpieza Visual y Textos Institucionales ]
        │
        ▼
[ Fase 03: Arquitectura de Layout y Route Guards RBAC ]
        │
        ▼
[ Fase 04: Robustecimiento de Sesión y Autorización ]
        │
        ▼
[ Fase 05: Homologación Funcional de Flujos por Rol ]
        │
        ▼
[ Fase 06: Estabilización de Pruebas, CI y Cierre ]
```

---

## 3. Desglose Detallado de Cada Fase

### FASE 02 — Limpieza Visual y Desacoplamiento de Jerga Técnica
- **Objetivo:** Retirar todos los textos técnicos visibles (RF, RN, CUS, T-xx, nombres de autores, menciones a estado de desarrollo) de los componentes de usuario.
- **Dependencias:** Aprobación de la Fase 01.
- **Archivos a Intervenir:**
  - `LoginOtpView.tsx` (ocultar panel Dev Mock y códigos simulados).
  - `CurriculumCatalogView.tsx` (simplificar buscador y etiquetas).
  - `ProfileAvailabilityView.tsx` (redactar requisito de mérito amigable).
  - `OfferPublishView.tsx` (eliminar nombre Joan Medina hardcodeado; limpiar validación RN-04/RN-05).
  - `RecommendationFeedView.tsx` (limpiar referencias a EdRecSys v1.0, XAI y CUS03).
  - `BookingModalView.tsx` (eliminar jerga de ACID, bloqueo pesimista y RNF07).
  - `StudentBookingsView.tsx` (retirar mensajes *"en desarrollo por Renzo"*).
  - `MentorSessionsView.tsx` (limpiar textos normativos en contingencias).
  - `SessionAttendanceView.tsx` y `BitacoraFormView.tsx` (simplificar títulos e indicadores criptográficos).
- **Pruebas Requeridas:**
  - Ejecutar tests de renderizado de componentes frontend en Vitest para comprobar que los elementos WAI-ARIA y labels requeridos por testing-library sigan encontrándose.
- **Riesgos de Regresión:**
  - Pruebas que busquen textos exactos tipo `getByText(/RN-08/)`.
  - *Mitigación:* Ajustar selectores de prueba a roles semánticos (`getByRole`) o selectores por `data-testid` que preservan la trazabilidad técnica en atributos HTML no visibles.
- **Criterio de Aceptación (DoD):** Cero menciones visuales de códigos de requerimiento o tareas en la interfaz de usuario. Tono institucional impecable.

---

### FASE 03 — Arquitectura de Navegación, Layout y Route Guards
- **Objetivo:** Reemplazar el menú plano de 10 pestañas por un cascarón institucional modular con navegación segmentada por rol y protección de rutas.
- **Dependencias:** Fase 02.
- **Archivos a Intervenir:**
  - `App.tsx` (reestructuración del cascarón `AppShell`).
  - Creación de componentes compartidos:
    - `Header.tsx` (cabecera limpia sin botón Swagger visible al estudiante).
    - `Footer.tsx` (pie institucional formal).
    - `RoleNavigation.tsx` (barra de navegación contextual según rol activo).
    - `ProtectedRoute.tsx` (componente guardián que evalúa sesión, consentimiento y rol requerido).
- **Pruebas Requeridas:**
  - Pruebas de integración de navegación con Vitest simulando perfiles de Mentoreado, Mentor y Administrador.
  - Verificación de redirección automática al login ante intento de acceso a `/admin` o `/sessions` sin credenciales.
- **Riesgos de Regresión:**
  - Bloqueo involuntario de vistas públicas legítimas como el catálogo curricular.
  - *Mitigación:* Definir lista explícita de rutas públicas (`login`, `curriculum`) y privadas protegidas.
- **Criterio de Aceptación (DoD):** Ningún usuario no autenticado o con rol de mentoreado puede visualizar ni acceder al panel de administración ni a la gestión de sesiones de mentor.

---

### FASE 04 — Robustecimiento de Sesión y Autorización RBAC (Frontend y Backend)
- **Objetivo:** Eliminar la inferencia insegura de roles en el cliente y blindar los endpoints de backend contra usurpación de identidad y escalamiento de privilegios.
- **Dependencias:** Fase 03.
- **Archivos a Intervenir:**
  - **Frontend:**
    - `AuthContext.tsx` (eliminar reglas `email.startsWith('admin')`; respetar únicamente roles firmados en el token JWT o devueltos por la base de datos).
    - `roleService.ts` y `authService.ts` (asegurar envío de cabecera `Authorization: Bearer <token>` en todas las peticiones).
  - **Backend:**
    - `backend/app/api/v1/endpoints/roles.py` (exigir rol `administrador` verificado en JWT para ejecutar `/promote-mentor` y `/revoke-mentor`).
    - `backend/app/api/v1/endpoints/profiles.py` y `bookings.py` (restringir o eliminar el bypass de `explicit_email` sin token en `_resolve_authenticated_email`).
- **Pruebas Requeridas:**
  - `pytest tests/test_authorization.py`
  - `pytest tests/test_roles.py`
  - Verificación de rechazo con HTTP 401/403 ante tokens manipulados o ausentes.
- **Riesgos de Regresión:**
  - Fallo en tests existentes que invocaban endpoints sin token en entorno de pruebas.
  - *Mitigación:* Conservar un flag explícito de test runner (`TESTING=True` o inyector de dependencias de prueba) sin exponer la brecha en el servidor activo.
- **Criterio de Aceptación (DoD):** La asignación y conmutación de roles está 100% respaldada por el backend y protegida contra falsificación.

---

### FASE 05 — Homologación Funcional Integral de Flujos por Rol
- **Objetivo:** Validar de punta a punta los tres recorridos institucionales principales en la interfaz integrada:
  1. **Flujo Mentoreado:** Acceso institucional → Aceptación de consentimiento → Exploración de catálogo → Configuración de perfil y horario libre → Consulta de cartelera Top-k → Reserva de mentoría → Ratificación anticipada / Desistimiento.
  2. **Flujo Mentor:** Ingreso con rol mentor → Publicación de convocatoria con validación de antelación $\ge 24\text{ h}$ y aforo → Revisión de sesión convocada en tablero docente → Supervisión de quórum $\ge 50\%$ → Generación de QR dinámico TOTP para pase de lista → Llenado y firma criptográfica de bitácora pedagógica.
  3. **Flujo Administrador:** Acceso con credenciales administrativas → Supervisión general de métricas → Búsqueda de estudiantes y promoción a mentor verificando mérito RN-03 (ciclo $\ge \text{VII}$) → Auditoría de quórum de sesiones → Diagnóstico de telemetría de base de datos.
- **Dependencias:** Fases 02, 03 y 04.
- **Archivos a Intervenir:**
  - Ajustes de integración fina en `App.tsx`, `MentorSessionsView.tsx`, `AdminDashboardView.tsx`, `StudentBookingsView.tsx`.
- **Pruebas Requeridas:**
  - Recorrido demostrativo manual y ejecución de suites de integración E2E (`BookingIntegration.test.tsx`, `StudentBookingsIntegration.test.tsx`).
- **Criterio de Aceptación (DoD):** Los tres perfiles operan de forma autónoma, fluida y sin inconsistencias visuales ni funcionales.

---

### FASE 06 — Estabilización de Pruebas, Resolución de Deuda CI y Cierre
- **Objetivo:** Subsanar los errores pendientes de TypeScript y formato de backend para garantizar la certificación en CI/CD y preparar la entrega final.
- **Dependencias:** Fases 02 a 05.
- **Archivos a Intervenir:**
  - `aplicacion/frontend/src/services/offerService.ts` (incorporar propiedades opcionales `nueva_fecha_inicio?: string | null` y `motivo_cancelacion?: string | null` en `QuorumDecisionResponse` para resolver los 3 errores TS2353 en `MentorSessionsView.test.tsx`).
  - Formateo automatizado de los 12 archivos de backend con `ruff format aplicacion/backend`.
  - Verificación final de empaquetado de producción con `npm run build` (`tsc -b && vite build`).
- **Pruebas Requeridas:**
  - `npm run test` (100% suites Vitest pasando).
  - `pytest` (100% suites Pytest pasando).
  - `ruff check aplicacion/backend` (0 errores).
  - `npm run build` (empaquetado exitoso sin errores de tipado).
- **Criterio de Aceptación (DoD):** Repositorio limpio, CI verde al 100%, empaquetado de producción operativo y software listo para demostración formal.

---

## 4. Matriz de Dependencias y Responsabilidades

| Fase | Título | Dependencia Previa | Impacto en Código | Riesgo de Regresión | Pruebas Clave |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **01** | Diagnóstico y Plan | Ninguna | Documentación | Nulo | Verificación de worktree y HEAD |
| **02** | Limpieza Visual | Fase 01 | Frontend (Vistas) | Bajo | Vitest (textos y selectores) |
| **03** | Layout & Route Guards | Fase 02 | Frontend (Estructura) | Medio | Integración React / Sesión |
| **04** | Seguridad & RBAC | Fase 03 | Frontend & Backend | Alto | Pytest (auth/roles) / Vitest |
| **05** | Homologación de Flujos | Fase 04 | Frontend & Backend | Medio | Pruebas E2E / Demo en vivo |
| **06** | Estabilización & CI | Fase 05 | Tipos TS & Formato | Bajo | `npm run build` / `pytest` / `ruff` |
