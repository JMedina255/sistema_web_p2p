# Informe de Cierre Técnico, Preparación de Demostración y Consistencia Documental

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Fase:** Fase 05 — Cierre Técnico y Preparación de Demostración Institucional  
**Fecha de Emisión:** 07 de Noviembre de 2026  
**Entorno de Trabajo:** `C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion`  
**Rama:** `feat/formalizacion-ux-roles`  
**Equipo Consultor:** C-SharkTeam (EPIS - UPT)  

---

## 1. Resumen Ejecutivo

La **Fase 05 (05-A y 05-B)** concluye exitosamente la formalización integral del Sistema Web P2P de Mentorías Académicas para la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT). Tras la auditoría de historias de usuario (Fase 04-B) y el fortalecimiento de la seguridad RBAC (Fases 03 y 04), el sistema ha superado todos los bloqueos técnicos, normalizado sus estándares de calidad de código y preparado un entorno reproducible y aislado para demostraciones ante la cátedra y autoridades académicas.

### Logros Principales:
1. **Build de Producción Recuperado (Fase 05-A):** Subsanación de errores `TS2353` en los contratos de mocks de quórum (`MentorSessionsView.test.tsx`), habilitando compilaciones TypeScript (`tsc -b && vite build`) 100% limpias.
2. **Estandarización de Estilo Backend (Bloque A):** Formateo canónico con Ruff de 14 archivos backend pendientes, logrando 0 advertencias de linter y 90 archivos debidamente formateados.
3. **Escenarios de Demostración Aislados (Bloque B):** Implementación del script `prepare_demo_scenarios.py` (con soporte para `--dry-run` y SQLite local) y de la suite automatizada `test_demo_scenarios.py` que valida de extremo a extremo los escenarios DEMO-01 a DEMO-06.
4. **Blindaje de Mecanismos de Seguridad Residuales (Bloque C):** Deshabilitación estricta de la siembra automática de base de datos en entornos de producción (`seed_database()`), confirmación de autenticación 100% OTP criptográfica (sin contraseñas estáticas), verificación de expiración de JWT y eliminación de vías de escape o bypass por query params.
5. **Consistencia y Homologación Documental (Bloque D):** Conciliación formal no destructiva de la discrepancia de nomenclatura CUS08 vs CUS12/13, ratificación de la justificación técnica de Python 3.13.5 frente al borrador inicial de Python 3.11 en el SAD, y alineamiento de los tres niveles de abstracción (8 HUs, 16 RFs, 37 PBIs).
6. **Verificación Integral Verde (Bloque E):** 555 pruebas automatizadas aprobadas (311 en frontend, 244 en backend), 85.12% de cobertura de código en el backend y 0 errores en pipelines de compilación y linter.

---

## 2. Estado Final del Frontend

El frontend desarrollado en **React 19**, **TypeScript** y **Vite** se encuentra completamente operativo, formalizado sin marcas académicas informales y con navegación restringida por roles (RBAC).

| Métrica / Dimensión | Estado / Resultado | Detalle Técnico |
| :--- | :--- | :--- |
| **Build de Producción (`npm run build`)** | **Éxito (264 ms)** | `tsc -b && vite build` genera los bundles `dist/index.html` (0.47 kB), `dist/assets/index-*.css` (0.43 kB) y `dist/assets/index-*.js` (482.58 kB gzip: 128.50 kB). |
| **Linter ESLint (`npm run lint`)** | **0 errores / 0 advertencias** | Verificación estricta de reglas de accesibilidad (WCAG 2.1 AA), TypeScript y React Hooks. |
| **Pruebas Unitarias (`npm test -- --run`)** | **311 aprobadas / 0 fallos** | 29 suites de prueba en Vitest + Testing Library cubriendo componentes, servicios, navegación y flujos E2E. |
| **Navegación Contextual (RBAC)** | **Implementada y Verificada** | Menú dinámico que reacciona según rol activo (`mentoreado`, `mentor`, `administrador`, visitante). Guardas visuales deniegan acceso no autorizado con pantallas formales de bloqueo. |
| **Conmutación de Servicios** | **Parametrizable** | Control vía variable `VITE_SERVICE_MODE=api` (obligatorio para demo) o `mock` (pruebas visuales). |

### Componentes y Rutas Verificadas:
- `RecommendationFeedView` (`?tab=recomendaciones`): Catálogo personalizado para mentoreados con filtros curriculares y selector top-$k$.
- `MentorSessionsView` (`?tab=sesiones`): Consola del mentor para publicación de ofertas, seguimiento de quórum y resolución de contingencias.
- `AdminDashboardView` (`?tab=admin`): Panel directivo institucional para auditoría de quórum masivo y promoción/revocación de mentores (RN-03).
- `SessionAttendanceView`: Proyección de código QR dinámico y código numérico TOTP de 6 dígitos rotatorio cada 30 segundos (RN-12).
- `BitacoraFormView`: Registro de reporte pedagógico con validación de observaciones ($\ge 50$ caracteres), sellado SHA-256 y ventana de 48 horas.
- `CurriculumCatalogView` (`?tab=cursos`): Malla formativa oficial EPIS-UPT con asignaturas filtro y temas conceptuales.

---

## 3. Estado Final del Backend

El backend implementado en **FastAPI**, **SQLAlchemy 2.0**, **Pydantic v2** y **Uvicorn** proporciona servicios REST de alta disponibilidad, operando de manera híbrida sobre PostgreSQL (Supabase) o SQLite local/memoria con inicio diferido (*lazy loading*).

| Métrica / Dimensión | Estado / Resultado | Detalle Técnico |
| :--- | :--- | :--- |
| **Estilo y Linter Ruff (`ruff check`)** | **0 errores** | Análisis estático completo sobre 90 archivos fuente en `aplicacion/backend/`. |
| **Formateo Ruff (`ruff format --check`)** | **90 archivos conformes** | Estandarización de longitud de línea (100 caracteres), ordenamiento de imports (`isort`) y tipado estricto. |
| **Pruebas Pytest (`pytest tests/ -v`)** | **244 aprobadas / 0 fallos** | 24 módulos de prueba cubriendo autenticación, seguridad RBAC, quórum, asistencia, bitácora y escenarios demo. |
| **Cobertura de Código Backend** | **85.12% global** | Supera ampliamente el umbral institucional regulatorio del 70.0% (`fail-under=70`). |
| **Seguridad de Endpoints** | **Aislamiento Total** | Prohibición estricta de impersonación de roles; verificación estricta de JWT Bearer y rechazo de parámetros query espurios. |

---

## 4. Catálogo de Escenarios de Demostración (DEMO-01 a DEMO-06)

Para la presentación formal ante el docente evaluador y autoridades de la EPIS-UPT, se han preparado seis escenarios reproducibles que demuestran el cumplimiento normativo y funcional del sistema:

### DEMO-01: Acceso de Mentoreado, Catálogo y Reserva de Cupo
- **Propósito:** Mostrar la experiencia del estudiante de pregrado que ingresa a la plataforma, consulta la oferta pedagógica y gestiona su reserva de cupo.
- **Actor:** `estudiante.demo@upt.pe` (Rol: Mentoreado).
- **Procedimiento Paso a Paso:**
  1. Ingresar al frontend (`http://localhost:5173`).
  2. Solicitar código de acceso OTP para `estudiante.demo@upt.pe`.
  3. Ingresar el código OTP recibido (visible en terminal backend en modo dev).
  4. Aceptar el consentimiento informado institucional (Ley N° 29733).
  5. En la pestaña *Recomendaciones* o *Cursos*, explorar la oferta de Cálculo I.
  6. En la sesión `SES-DEMO-PUB01`, pulsar "Reservar Cupo" y ratificar intención de asistencia.
  7. Comprobar que en la sección "Mis Reservas" el estado figure como `CONFIRMADA`.

### DEMO-02: Publicación de Oferta Académica con Control de Antelación (RN-04)
- **Propósito:** Demostrar que un mentor acreditado (ciclo $\ge \text{VII}$) puede publicar ofertas de mentoría y que el sistema impide publicaciones con antelación menor a 24 horas.
- **Actor:** `mentor.demo@upt.pe` (Rol: Mentor, VIII Ciclo).
- **Procedimiento Paso a Paso:**
  1. Iniciar sesión como `mentor.demo@upt.pe`.
  2. En el menú superior, verificar la presencia de la pestaña *Sesiones de Mentoría*.
  3. Pulsar el botón "Publicar Nueva Sesión".
  4. Seleccionar la asignatura "Cálculo I", tema "Límites Notables y Asíntotas".
  5. Asignar fecha con al menos 48 horas de anticipación, modalidad *Presencial* (aforo automático de 10 cupos según RN-05) y aula física "Aula 201".
  6. Pulsar "Publicar Oferta" y constatar el registro inmediato en estado `PUBLICADA`.

### DEMO-03: Contingencia por Quórum Insuficiente en $T-24\text{ h}$ (RN-09 / RN-10)
- **Propósito:** Evidenciar que ante la falta de quórum reglamentario (menos del 50% de cupos cubiertos a 24 horas del inicio), el sistema **no cancela unilateralmente** la sesión, sino que habilita al mentor titular para tomar una decisión resolutiva.
- **Actor:** `mentor.demo@upt.pe` sobre la sesión `SES-DEMO-Q01` (2 confirmados de 10).
- **Procedimiento Paso a Paso:**
  1. Como mentor, ubicar en la vista de sesiones la tarjeta con etiqueta ámbar `QUORUM_INSUFICIENTE`.
  2. Pulsar "Resolver Contingencia".
  3. Evaluar las tres alternativas normativas disponibles:
     - **Confirmar Dictado (`PROCEED`):** Dictar con aforo reducido (transiciona a `CONFIRMADA`).
     - **Reprogramar (`RESCHEDULE`):** Asignar nueva fecha con $T > 24\text{ h}$ preservando los inscritos.
     - **Cancelar Sesión (`CANCEL`):** Ingresar motivo justificado; el sistema libera a los estudiantes inscritos sin penalización alguna (RN-10).
  4. Seleccionar una opción y verificar la actualización inmediata de la interfaz.

### DEMO-04: Pase de Asistencia Digital con Código QR Dinámico TOTP (RN-12)
- **Propósito:** Mostrar el registro ágil de asistencia presencial mediante tokens rotatorios que impiden el fraude de suplantación o capturas estáticas.
- **Actores:** `mentor.demo@upt.pe` (Proyector) y `estudiante.demo@upt.pe` (Check-in).
- **Procedimiento Paso a Paso:**
  1. En la sesión en curso `SES-DEMO-ASIS01`, el mentor pulsa "Abrir Control de Asistencia".
  2. Visualizar la pantalla de proyección que renderiza un código QR dinámico y un código numérico de 6 dígitos que expira cada 30 segundos.
  3. El estudiante mentoreado ingresa a la sesión desde su dispositivo y pulsa "Registrar Asistencia".
  4. Escanear el QR o tipear el código numérico de 6 dígitos.
  5. Comprobar en la consola del mentor cómo la nómina de asistencia se actualiza en tiempo real marcando al estudiante como `PRESENTE`.

### DEMO-05: Cierre de Sesión y Bitácora Pedagógica Sellada (RN-12)
- **Propósito:** Comprobar la rendición formativa de cuentas por parte del mentor dentro de la ventana reglamentaria de 48 horas post-sesión.
- **Actor:** `mentor.demo@upt.pe` sobre la sesión concluida `SES-DEMO-BIT01`.
- **Procedimiento Paso a Paso:**
  1. En la sesión concluida, pulsar "Registrar Bitácora Pedagógica".
  2. Constatar que el contador perentorio informa el tiempo restante de la ventana de 48 horas.
  3. Intentar enviar una observación corta (< 50 caracteres) y observar la validación pedagógica que bloquea el envío.
  4. Ingresar observaciones sustantivas ($\ge 50$ caracteres), seleccionar los temas efectivamente cubiertos y nivel de dificultad ("Medio").
  5. Pulsar "Firmar y Registrar Bitácora".
  6. Verificar que la sesión transiciona a `BITACORA_REGISTRADA`, se genera el hash SHA-256 de integridad y se acreditan provisionalmente las horas de mentoría (1.5 horas para 90 minutos).

### DEMO-06: Panel de Supervisión y Evaluación de Quórum por el Administrador
- **Propósito:** Demostrar las facultades de auditoría institucional, evaluación desatendida de quórum y gestión de mérito académico por la Coordinación de Tutoría.
- **Actor:** `admin.demo@upt.pe` (Rol: Administrador).
- **Procedimiento Paso a Paso:**
  1. Iniciar sesión como `admin.demo@upt.pe` y acceder a la pestaña *Panel Administrativo*.
  2. Ejecutar la acción "Evaluar Quórum Masivo ($T-24\text{ h}$)" para comprobar la auditoría de todas las sesiones activas en la ventana perentoria.
  3. En la sección "Administración de Roles", buscar un estudiante institucional (`2022073504@upt.pe`).
  4. Constatar la verificación de ciclo académico ($\ge \text{VII}$) para la concesión del rol de Mentor (RN-03).
  5. Intentar realizar estas acciones con una cuenta de mentoreado y comprobar la denegación estricta (403 Forbidden).

---

## 5. Procedimiento de Arranque del Sistema para la Demo

Para levantar la plataforma en el entorno local de demostración:

### Paso 1: Inicialización de la Base de Datos Aislada (Opcional si se requiere SQLite persistente)
```powershell
cd C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion\aplicacion\backend
# Generar base de datos SQLite pre-poblada con los 6 escenarios
..\.venv\Scripts\python.exe scripts/prepare_demo_scenarios.py --sqlite-path sqlite:///demo_epis_p2p.db
```

### Paso 2: Arranque del Servidor Backend FastAPI
```powershell
cd C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion\aplicacion\backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Verificación:* Acceder a `http://localhost:8000/docs` o `http://localhost:8000/api/v1/health`.

### Paso 3: Arranque del Servidor Frontend React Vite
```powershell
cd C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion\aplicacion\frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
*Verificación:* Abrir en el navegador web `http://localhost:5173`.

---

## 6. Matriz de Credenciales y Perfiles de Prueba

El sistema opera bajo autenticación institucional **100% passwordless (OTP)**. No existen contraseñas maestras ni estáticas:

| Correo de Prueba | Roles Asignados | Perfil Académico | Propósito en la Demostración |
| :--- | :--- | :--- | :--- |
| `estudiante.demo@upt.pe` | Mentoreado | Ciclo III (Pregrado) | DEMO-01 (Reservas, catálogo) y DEMO-04 (Asistencia QR). |
| `mentor.demo@upt.pe` | Mentor, Mentoreado | Ciclo VIII (Acreditado RN-03) | DEMO-02 (Ofertas), DEMO-03 (Quórum), DEMO-04/05 (Asistencia y Bitácora). |
| `admin.demo@upt.pe` | Administrador, Mentoreado | Coordinación de Tutoría EPIS | DEMO-06 (Auditoría, quórum masivo, gestión de roles). |
| `companero.demo@upt.pe` | Mentoreado | Ciclo III (Pregrado) | Segundo participante en sesión DEMO-03 para ilustrar quórum parcial. |

> **Mecanismo de acceso en modo demostración:** Al solicitar el acceso, el código OTP numérico de 6 dígitos se genera criptográficamente y se imprime en la terminal de ejecución del backend (`[AUTH DEV] >>> CÓDIGO OTP EMITIDO PARA ... <<<`).

---

## 7. Análisis de Riesgos de Seguridad Residuales y Mitigaciones

| Riesgo Auditado | Severidad | Diagnóstico | Mitigación Implementada |
| :--- | :---: | :--- | :--- |
| **Cuentas semilla con contraseñas fijas** | Alta | No existen contraseñas en el modelo relacional. | La autenticación es exclusivamente OTP. Se agregó un candado en `seed_database()` que aborta inmediatamente si `APP_ENV == 'production'`. |
| **Exposición de código OTP de prueba** | Media | El código OTP sólo se expone en consola si `APP_ENV == 'development'`. | En producción, `mock_hint` es estrictamente `None` y los códigos se almacenan hasheados con SHA-256 y salt criptográfico. |
| **Revocación de JWT sin estado** | Media | Los tokens JWT no poseen blacklist centralizada en Redis. | El tiempo de expiración es corto (60 minutos por defecto). La autorización re-valida roles en cada petición sensible contra el contexto de seguridad. |
| **Fallback silencioso a mock en frontend** | Media | Riesgo de que la UI simule éxito cuando el backend está caído. | Los adaptadores de API capturan errores de red y lanzan excepciones explícitas (`NETWORK_ERROR`), notificando al usuario que debe verificar la conexión con el backend local. |
| **Bypass de roles por query params** | Crítica | Históricamente existían parámetros que permitían actuar en nombre de otro usuario en pruebas preliminares. | En Fase 04 y 05-B se eliminó cualquier bypass. Todos los endpoints sensibles extraen la identidad exclusivamente del token JWT verificado. |

---

## 8. Reconciliación Documental Oficial

Se ratifican los acuerdos de consistencia registrados en `docs/formalizacion/08_HOMOLOGACION_INCONSISTENCIAS.md`:
1. **CUS08 vs CUS12/CUS13:** Se reconoce formalmente que `CUS08` en el SRS maestro FD03 (Cuadro 5.5) y las especificaciones técnicas `CUS12` (Asistencia) y `CUS13` (Bitácora) de Sprint 06 son expresiones complementarias que satisfacen el requerimiento **RF17**.
2. **Runtime Python:** Se ratifica la justificación técnica de **Python 3.13.5** registrada en el Sprint 01 (`PLAN_SPRINTS_Y_TAREAS.md`, commit `d6bc275`) frente a la mención de Python 3.11 en el SAD §2.5.
3. **Pirámide de Artefactos Funcionales:** Se mantiene la trazabilidad bidireccional entre las **8 Historias de Usuario originales**, los **16 Requerimientos Funcionales** del SRS y las **37 Tareas Técnicas / PBIs** completadas.

---

## 9. Estado de las Historias de Usuario al Cierre del Sprint 06

| Código HU | Título de la Historia de Usuario | Módulos y Tareas Asociadas | Estado al Cierre del Sprint 06 |
| :--- | :--- | :--- | :---: |
| **HU01** | Autenticación institucional passwordless y consentimiento legal | T-02 a T-06 / RF01, RF02, RN-02 | **100% Completada** |
| **HU02** | Perfil académico formativo y disponibilidad semanal | T-11 a T-13 / RF04, RNF04 | **100% Completada** |
| **HU03** | Publicación y administración de ofertas con control de antelación | T-14 a T-16 / RF08, RN-03, RN-04, RN-05 | **100% Completada** |
| **HU04** | Motor de recomendación pedagógica personalizada (EdRecSys) | T-17 a T-20 / RF09, RF10 | **100% Completada** |
| **HU05** | Reserva transaccional de cupos con control de aforo y quórum | T-21 a T-30 / RF12, RF13, RF15, RN-08, RN-09 | **100% Completada** |
| **HU06** | Contingencia de quórum, pase de asistencia TOTP y bitácoras | T-31 a T-37 / RF16, RF17, RN-10, RN-12 | **100% Completada** |
| **HU07** | Priorización algorítmica por vulnerabilidad y emparejamiento inteligente | RF11 | *Planificada Sprint 07* |
| **HU08** | Certificación institucional y acreditación de horas extracurriculares | RF18 | *Planificada Sprint 08* |

---

## 10. Inventario de Deuda Técnica Conocida (No Bloqueante para Demo)

1. **Lista Negra de Tokens Revocados (Blacklist JWT):** Actualmente la invalidación al cerrar sesión se ejecuta en el cliente (limpieza de `localStorage`). Para despliegues masivos se sugiere un almacén Redis en memoria para invalidación instantánea en el backend.
2. **Persistencia Híbrida de Memoria:** Los endpoints admiten almacenamiento en memoria volátil de respaldo cuando `DATABASE_URL` no está presente. Para producción, el backend debe exigir conexión activa a PostgreSQL.
3. **Consolidación de Notificaciones:** Las alertas de corte de quórum a $T-24\text{ h}$ se evalúan bajo demanda o cron interno; la emisión de correos SMTP institucionales está prevista para consolidarse en el Sprint 08.

---

## 11. Recomendaciones para los Sprints 07 y 08

1. **Sprint 07 (Priorización y Vulnerabilidad Académica):** Desarrollar los módulos asociados a `HU07` y `RF11` en el motor de recomendación, ponderando estudiantes con mayor número de reprobaciones previas en cursos filtro.
2. **Sprint 08 (Certificados y Auditoría Final):** Implementar la generación de constancias PDF firmadas digitalmente (`HU08` / `RF18`) y el cierre de ciclo académico.
3. **Conservación de la Rama `main`:** Mantener la política de commits limpios, verificados con pruebas automatizadas y formateados con Ruff antes de cualquier fusión mediante Pull Request formal.

---

## 12. Historial de Commits de la Fase 05

| Commit | Mensaje Canónico | Bloque / Propósito |
| :--- | :--- | :--- |
| `a1d198d` | `fix(frontend): corregir mocks de quorum y recuperar build de produccion` | **Fase 05-A:** Corrección TS2353 en mocks de quórum y recuperación de compilación limpia Vite. |
| `cf76605` | `style(backend): normalizar formato Ruff y preservar comportamiento` | **Bloque A:** Formateo de 14 archivos backend con Ruff; 0 errores de linter. |
| `bb9ce3c` | `test(demo): preparar escenarios reproducibles de mentoria` | **Bloque B:** Creación de `prepare_demo_scenarios.py`, suite `test_demo_scenarios.py` y doc en `.env.example`. |
| `5333dbe` | `fix(security): aislar mecanismos de demostracion` | **Bloque C:** Candado de seguridad para evitar siembra de datos de prueba en producción. |
| `806ffff` | `docs(formalizacion): homologar inconsistencias verificadas` | **Bloque D:** Documento formal de homologación CUS08 vs CUS12/13, Python 3.13.5 y conteo de artefactos. |

---
*Informe técnico elaborado y certificado por el Equipo Consultor C-SharkTeam (EPIS-UPT).*
