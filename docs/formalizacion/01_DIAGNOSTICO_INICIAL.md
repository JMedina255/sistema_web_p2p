# 01 — Diagnóstico Inicial del Repositorio y Arquitectura del Sistema Web P2P

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)  
**Rama de Trabajo:** `feat/formalizacion-ux-roles`  
**Directorio de Trabajo:** `C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion`  
**Commit Base:** `6ee1caa` (*feat(sprint-06): implementar tareas de quorum, contingencia, asistencia QR y bitacoras pedagogicas con actualizacion integral del SRS*)  
**Fecha de Diagnóstico:** 7 de noviembre de 2026  
**Responsable:** Equipo de Ingeniería de Software — Área de Formalización y Calidad  

---

## 1. Contexto y Línea Base del Repositorio

El proyecto **Sistema Web P2P** ha culminado seis sprints metodológicos de desarrollo formativo bajo la metodología Scrum. A lo largo de esta evolución, se integraron paulatinamente los requerimientos funcionales (RF01 a RF17), no funcionales (RNF01 a RNF09), reglas de negocio (RN-01 a RN-13) y casos de uso (CUS01 a CUS24).

Si bien la lógica de negocio, las migraciones de base de datos relacional (Alembic `20261031_004` con 12 tablas en PostgreSQL/Supabase), el motor de recomendación *Top-k* (EdRecSys) y las políticas de concurrencia ACID con bloqueo pesimista (`SELECT FOR UPDATE`) se encuentran operativas, la interfaz de usuario React y los mecanismos de autorización frontend-backend presentan una fuerte orientación hacia la evaluación académica y el testbench técnico.

El presente diagnóstico establece la línea base formal de partida para la transición desde un **prototipo académico con telemetría de laboratorio visible** hacia una **aplicación web institucional limpia, usable, segura y preparada para demostración formal**.

---

## 2. Diagnóstico del Frontend (React 19 + TypeScript + Vite)

### 2.1. Sobrecarga de Jerga Académica y Notación Técnica en Interfaces
Se identificaron más de **300 referencias directas a códigos de ingeniería de software** incrustadas en títulos, etiquetas, alertas, botones, tooltips y mensajes de error orientados al usuario final:
- **62 ocurrencias de códigos de Requerimientos Funcionales** (`RF01`, `RF02`, `RF03`, `RF05`, `RF06`, `RF12`, `RF13`, `RF14`, `RF16`, `RF17`).
- **169 ocurrencias de Reglas de Negocio** (`RN-02`, `RN-03`, `RN-04`, `RN-05`, `RN-08`, `RN-09`, `RN-10`, `RN-11`, `RN-12`).
- **65 ocurrencias de Casos de Uso** (`CUS01`, `CUS02`, `CUS03`, `CUS04`, `CUS06`, `CUS07`, `CUS10`, `CUS12`, `CUS15`, `CUS17`, `CUS21`, `CUS24`).
- **76 ocurrencias de Tareas Operativas de Sprints** (`T-01`, `T-02`, `T-03`, `T-04`, `T-09`, `T-10`, `T-11`, `T-14`, `T-18`, `T-20`, `T-21`, `T-25`, `T-27`, `T-32`).
- **Textos con mención explícita a desarrolladores:** Mensajes como *"El servicio de ratificación en el servidor FastAPI está en desarrollo por Renzo"* en `StudentBookingsView.tsx` (líneas 362 y 427).

### 2.2. Exposición de Controles de Desarrollo y Datos Sensibles en Pantalla
- **Login OTP (`LoginOtpView.tsx`):**
  - Muestra un banner permanente de desarrollo con alternancia manual entre `Dev Mock` y `API Real (T-03)`.
  - En modo simulación, expone visualmente el código de verificación OTP generado (`mockCodeHint: '849201'`), anulando el propósito de seguridad del reto criptográfico.
- **Cabecera Institucional (`App.tsx`):**
  - Muestra un botón directo y público hacia `Swagger /docs ↗`, el cual es una herramienta de inspección para desarrolladores y no debe formar parte de la barra de navegación de estudiantes o docentes.
- **Tarjetas Informativas Inferiores (`App.tsx`):**
  - En la parte inferior del cascarón principal se renderizan tarjetas con títulos como *"🛡️ RF03 / RN-03: Asignación de Roles por Mérito"*, *"📊 RN-09: Quórum Mínimo Institucional"* y *"⚖️ RF02 / RN-02: Ley N° 29733"*, concebidas para sustentar tareas académicas ante el docente, pero inapropiadas para una experiencia de usuario final.

### 2.3. Ausencia de Protección de Rutas (Route Guards) y Navegación Abierta
- `App.tsx` renderiza un menú plano con 10 botones visibles sin importar el estado de autenticación del visitante.
- Un usuario no autenticado o un estudiante sin privilegios puede hacer clic en `🛡️ Panel Admin (T-04 / T-11)` o navegar a `http://localhost:5173/?tab=admin` y acceder directamente a `AdminDashboardView.tsx`.
- Las vistas `AdminDashboardView` y `MentorSessionsView` utilizan valores predeterminados (*fallback props*) como `adminEmail = 'admin.epis@upt.pe'` y `mentorEmail = studentEmail ?? 'mentor.avanzado@upt.pe'`. Esto permite que un visitante anónimo opere visualmente como administrador o mentor sin haber iniciado sesión institucional.

### 2.4. Duplicación de Estilos y Falta de Componentización Estándar
- Todo el estilo se maneja mediante objetos en línea (`style={{ ... }}`), dispersos a lo largo de componentes de más de 1,000 líneas (`StudentBookingsView.tsx`, `MentorSessionsView.tsx`, `RecommendationFeedView.tsx`, `BookingModalView.tsx`).
- No existe un sistema común de diseño, botones compartidos, alertas unificadas ni tipografía estandarizada.

---

## 3. Diagnóstico del Backend (FastAPI + SQLAlchemy + Pydantic v2)

### 3.1. Estado de la Persistencia y Migraciones
- **Conexión a Base de Datos:** Verificada exitosamente con PostgreSQL en Supabase mediante el Session Pooler (puerto 5432, IPv4). Latencia medida de 371 ms.
- **Migraciones Alembic:** La base de datos se encuentra en la revisión `20261031_004` (Head), con 12 tablas operativas.
- **Aislamiento Multi-inquilino / Multi-usuario:** Los modelos cuentan con estructuras adecuadas para segregación por `estudiante_email` y roles, pero algunos endpoints relajan la validación en entornos de desarrollo.

### 3.2. Autorización y Fallbacks en Modo Desarrollo
- En la función utilitaria `_resolve_authenticated_email` ([`profiles.py`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/backend/app/api/v1/endpoints/profiles.py)):
  ```python
  if explicit_email and explicit_email.strip():
      if settings.APP_ENV in ("development", "test", "testing"):
          return explicit_email.strip().lower()
  ```
  Esto permite que peticiones sin cabecera `Authorization: Bearer <token>` especifiquen arbitrariamente cualquier correo institucional en un parámetro de consulta (`query param`) y ejecuten operaciones en su nombre.
- En `roles.py`, la validación de autopromoción en `/promote-mentor`:
  ```python
  if caller_email.strip().lower() == payload.email.strip().lower() and "administrador" not in caller_roles:
      raise HTTPException(status_code=403, detail="...")
  ```
  Impide que un usuario se promueva a sí mismo, pero omite verificar si el usuario que llama posee rol de administrador cuando promueve a un tercero (`caller_email != payload.email`), lo cual representa una brecha de elevación de privilegios potencial.

---

## 4. Deuda Técnica y Hallazgos de CI Detectados

1. **Frontend — TypeScript (3 Errores TS2353):**
   - Archivo: [`MentorSessionsView.test.tsx`](file:///C:/Users/Admin/Desktop/Proyectos/sistema_web_p2p-formalizacion/aplicacion/frontend/src/components/__tests__/MentorSessionsView.test.tsx) (líneas 79, 143 y 186).
   - Causa: Propiedades `motivo_cancelacion` y `nueva_fecha_inicio` ausentes en la interfaz `QuorumDecisionResponse` de `offerService.ts`.
   - Estado: Afecta la compilación de producción (`tsc -b`) y Vitest en CI. No bloquea el servidor de desarrollo Vite.
2. **Backend — Formato con Ruff (12 Archivos):**
   - 12 archivos de backend presentan inconsistencias de salto de línea o indentación detectadas por `ruff format --check`.

---

## 5. Matriz de Riesgos Prioritarios

| ID | Riesgo Identificado | Impacto | Severidad | Categoría |
| :---: | :--- | :--- | :---: | :---: |
| **R-01** | Acceso irrestricto a vistas privilegiadas (Admin, Mentor) desde la interfaz mediante pestañas y URLs sin verificar sesión ni rol. | Un mentoreado o visitante no autenticado puede ingresar a la pantalla administrativa o de mentor. | **Crítica** | Seguridad / Frontend |
| **R-02** | Inferencia de roles en cliente mediante prefijos de correo (`email.startsWith('admin')`). | Suplantación de rol administrador o mentor en cliente con solo ingresar un correo que inicie con `admin` o `mentor.`. | **Crítica** | Autenticación / RBAC |
| **R-03** | Parámetros de consulta que sobrescriben la identidad (`explicit_email`) sin validar token JWT en modo desarrollo. | Peticiones HTTP pueden usurpar reservas, perfiles o disponibilidades de otros estudiantes. | **Alta** | Autorización / Backend |
| **R-04** | Exposición visual de códigos OTP simulados y alternador de Mock/API en la pantalla de bienvenida. | Sensación de prototipo incompleto y vulnerabilidad en una presentación formal de software. | **Alta** | Experiencia de Usuario (UX) |
| **R-05** | Saturación de códigos técnicos (RF, RN, CUS, T-xx, nombres de autores) en toda la UI. | Confusión cognitiva en el usuario final, pérdida de tono institucional universitario. | **Alta** | Usabilidad / Calidad |
| **R-06** | Identidades predeterminadas en componentes (`admin.epis@upt.pe`, `Joan Cristian Medina Quispe`). | Operaciones accidentales sobre datos simulados que no reflejan al usuario autenticado. | **Media** | Integridad de Datos |
| **R-07** | Deuda técnica acumulada en TypeScript (TS2353) y formateo de backend (Ruff). | Bloqueo en pipelines automatizados de CI/CD al ejecutar compilación de producción. | **Media** | Aseguramiento de Calidad |
