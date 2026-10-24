# Bitácora de Ejecución — Sprint 2: Roles, Currículo y Perfiles

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)  
**Semestre Académico:** 2026-II  
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe (Joan) y Renzo Antonio Antayhua Mamani (Renzo)  
**Rama de trabajo:** `feat/sprint-02-roles-curriculo-perfiles`  
**Fecha de corte:** 23/10/2026  
**Commit principal de la sesión:** [`3766a08`](https://github.com/JMedina255/sistema_web_p2p/commit/3766a08fa98d49bc6107a9fd278568f289f7fe74)  

> [!NOTE]
> **Alcance de la Sesión de Trabajo (23/10/2026):**  
> En esta sesión se ejecutaron, probaron y publicaron las **tres tareas asignadas a Joan para el Sprint 2** (**T-04**, **T-10** y **T-11**), correspondientes a la capa cliente interactiva, gobernanza de privacidad, búsqueda curricular avanzada y matriz semanal de disponibilidad horaria. Las tareas de backend y persistencia asignadas a Renzo (**T-05**, **T-08**, **T-12** y **T-13**) permanecen estructuradas conforme al plan y pendientes de integración.

---

## 1. Visión General y Alcance del Sprint 2

El **Sprint 2** tiene como objetivo consolidar la gobernanza legal de protección de datos personales conforme a la **Ley N° 29733** (**RF02** / **RN-02**), enriquecer la exploración interactiva del catálogo curricular oficial (**RF05** / **CUS21**), administrar la jerarquía de roles institucionales y verificación de mérito (**RF03** / **CUS10** / **RN-03**), y capturar los perfiles formativos junto a la agenda semanal de disponibilidad horaria (**RF04** / **CUS15**), insumo indispensable para el motor de recomendación Top-k (Sprint 4).

A continuación, se presenta la matriz canónica de asignación y esfuerzo planificado para el Sprint 2, distinguiendo el estado técnico actual de cada actividad:

### Cuadro 1.1: Actividades y Estado Técnico de Desarrollo del Sprint 2

| ID | Actividad Oficial | Responsable | Estimación Planificada (h) | Estado Técnico Actual | Entregable / Evidencia |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T-04** | Desarrollar formulario de consentimiento digital. | Joan | 2 | **Verificado localmente** ✅ | Componente `ConsentModalView.tsx`, servicio `consentService.ts` y 9 pruebas Vitest. |
| **T-05** | Implementar persistencia del consentimiento. | Renzo | 1 | *Pendiente de integración* | Tabla `consentimientos_legales`, marcas temporales y endpoint de persistencia. |
| **T-08** | Desarrollar endpoints de administración de roles. | Renzo | 3 | *Pendiente de integración* | Tabla `usuario_roles`, endpoints de promoción a mentor y verificación de mérito. |
| **T-10** | Implementar interfaz de consulta del catálogo curricular. | Joan | 2 | **Verificado localmente** ✅ | Componente `CurriculumCatalogView.tsx` con buscador en tiempo real y temas silábicos. |
| **T-11** | Desarrollar formulario de perfiles y disponibilidad. | Joan | 3 | **Verificado localmente** ✅ | Componente `ProfileAvailabilityView.tsx`, `profileService.ts` y grilla semanal 6×11. |
| **T-12** | Implementar API de perfiles y horarios. | Renzo | 2 | *Pendiente de integración* | Tablas `perfiles_academicos`, `disponibilidades_horarias` y endpoints REST. |
| **T-13** | Ejecutar pruebas de autorización entre usuarios. | Renzo | 1 | *Pendiente de integración* | Pruebas de seguridad RLS: aislamiento de perfiles privados y denegación de autopromoción. |

Fuente: Elaboración propia a partir de `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Tabla 5.3) y avance consolidado en la rama `feat/sprint-02-roles-curriculo-perfiles`.

---

## 2. Registro de Ejecución — Tarea T-04 (Consentimiento Digital — Ley N° 29733)

### 2.1. Alcance Implementado
- **Componente Interactivo (`aplicacion/frontend/src/components/ConsentModalView.tsx`):**
  - Implementación del formulario institucional de consentimiento informado para el tratamiento de datos personales, en estricto cumplimiento del marco legal de la **Ley N° 29733 (Ley de Protección de Datos Personales del Perú)** y su Reglamento (D.S. N° 003-2013-JUS) (**RF02** / **CUS01**).
  - Bloque normativo institucional scrollable y accesible (`role="region"` y `aria-label`) que explicita:
    1. *Finalidad exclusiva:* tratamiento de calificaciones y asignaturas filtro matriculadas para el algoritmo Top-k y convalidación de horas extracurriculares.
    2. *Datos tratados:* correo institucional, código de estudiante, notas de cursos filtro, temas declarados de refuerzo/fortaleza y agenda horaria semanal.
    3. *Ejercicio de Derechos ARCO:* información clara para solicitar acceso, rectificación, cancelación u oposición ante la Dirección de la EPIS-UPT.
    4. *Prohibición de transferencia:* garantía de no comercialización ni cesión a terceros ajenos a la UPT.
  - **Casilla de Conformidad Expresa:** checkbox obligatorio que condiciona la habilitación del botón *"Aceptar y Continuar"*.
  - **Bloqueo Preventivo ante Rechazo (Regla RN-02):** botón *"Rechazar y Salir"* que cancela la sesión, revoca el consentimiento y emite una alerta informativa bloqueando el acceso a las funciones del sistema.
  - **Soporte de Auditoría:** visualización de la marca temporal UTC y versión de términos (`2026-II-v1.0`) cuando el consentimiento se encuentra formalizado.

- **Servicio y Adaptador de Datos (`aplicacion/frontend/src/services/consentService.ts`):**
  - Interfaz tipada `ConsentStatus` (`hasConsented`, `consentedAt`, `termsVersion`, `email`, `mode`).
  - Métodos `getConsentStatus()`, `acceptConsent()` y `revokeConsent()`.
  - Modo dual (`mock` / `api`): persistencia en `localStorage` para pruebas deterministas y contrato listo para consumir `POST /api/v1/consent/accept` cuando se culmine la tarea **T-05** de Renzo.

### 2.2. Comprobaciones Realizadas y Resultados Observados

A continuación, se detalla la matriz de verificación de las 9 pruebas automatizadas asociadas a la tarea T-04:

### Cuadro 2.1: Matriz de Pruebas de Consentimiento Digital (T-04)

| Componente / Suite | Escenario de Prueba | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **`consentService`** | Consulta de usuario no registrado | Retornar `hasConsented: false` y versión vigente | `hasConsented: false`, `termsVersion: 2026-II-v1.0` | ✅ Exitoso |
| **`consentService`** | Aceptación con correo institucional | Registrar timestamp UTC y persistir estado | `success: true`, estampa temporal registrada | ✅ Exitoso |
| **`consentService`** | Intento con correo externo (`@gmail.com`) | Rechazar por falta de dominio institucional | Lanza error de validación de dominio `@upt.pe` | ✅ Exitoso |
| **`consentService`** | Revocación o rechazo voluntario | Limpiar registro y dejar `hasConsented: false` | `hasConsented: false` verificado en almacén | ✅ Exitoso |
| **`ConsentModalView`** | Renderizado del encabezado institucional | Desplegar título, badge y cláusulas Ley 29733 | Elementos del DOM presentes y accesibles | ✅ Exitoso |
| **`ConsentModalView`** | Control de botón de aceptación | Permanecer deshabilitado hasta marcar checkbox | Botón `disabled` pasa a activo tras clic | ✅ Exitoso |
| **`ConsentModalView`** | Flujo de aceptación exitosa | Disparar callback `onConsentAccepted` y mensaje | Callback ejecutado, notificación verde desplegada | ✅ Exitoso |
| **`ConsentModalView`** | Flujo de rechazo bloqueante (RN-02) | Disparar callback `onConsentRejected` y alerta | Callback invocado, mensaje de bloqueo visible | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/services/__tests__/consentService.test.ts` y `src/components/__tests__/ConsentModalView.test.tsx`.

---

## 3. Registro de Ejecución — Tarea T-10 (Consulta Avanzada del Catálogo Curricular)

### 3.1. Alcance Implementado
- **Componente Enriquecido (`aplicacion/frontend/src/components/CurriculumCatalogView.tsx`):**
  - Evolución de la vista base del Sprint 1 hacia una **interfaz de consulta y exploración curricular avanzada** conforme a **RF05** y **CUS21**:
    1. **Buscador Reactivo en Tiempo Real:** entrada de texto que filtra instantáneamente por nombre de asignatura (*Cálculo I*, *Base de Datos*), código oficial (*CALC-101*, *BDD-401*) y búsqueda profunda dentro de la taxonomía de temas silábicos (*Límites*, *Punteros*, *Recursividad*, *Normalización*, *Herencia*).
    2. **Filtro Multifactorial por Ciclo:** selector dinámico para aislar materias por ciclo formativo (Todos, Ciclo I, II, III o IV).
    3. **Delimitación de Cursos Críticos:** casilla para filtrar exclusivamente las 5 materias filtro formativas con alta tasa de deserción.
    4. **Contador Dinámico de Coincidencias:** badge informativo que indica cuántas materias y temas cumplen con los criterios de búsqueda.
    5. **Visualizador Jerárquico de Sílabo:** desglose de unidades conceptuales silábicas con resaltado visual (`badge` *"Coincidencia"*) en los temas que concuerdan con el término ingresado.
    6. **Ponderador Top-k:** visualización de créditos lectivos y factor de ponderación algorítmica para recomendación (ej. `1.2x`, `1.3x`).

### 3.2. Comprobaciones Realizadas y Resultados Observados

### Cuadro 3.1: Matriz de Pruebas de Consulta Curricular Avanzada (T-10)

| Prueba Automatizada | Escenario Evaluado | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| `test 1: Render inicial` | Carga del catálogo desde API | Desplegar tarjetas con Cálculo I y Algoritmos | 2 asignaturas iniciales renderizadas | ✅ Exitoso |
| `test 2: Detalle silábico` | Clic en asignatura Algoritmos | Cargar detalle con unidad silábica de Punteros C++ | Temas silábicos desplegados en panel derecho | ✅ Exitoso |
| `test 3: Buscador textual` | Ingreso de término `"CALC"` en buscador | Mantener Cálculo I y ocultar Algoritmos | Filtrado en tiempo real verificado en DOM | ✅ Exitoso |
| `test 4: Manejo de errores` | Fallo de conexión de red simulado | Desplegar alerta amigable de error al usuario | Alerta `role="alert"` con texto informativo | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/components/__tests__/CurriculumCatalogView.test.tsx`.

---

## 4. Registro de Ejecución — Tarea T-11 (Perfiles Formativos y Matriz de Disponibilidad)

### 4.1. Alcance Implementado
- **Componente Integral (`aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`):**
  - Interfaz organizada en dos secciones funcionales vinculadas conforme a **RF04**, **CUS15**, **RNF04** y **RNF08**:
    1. **Pestaña 1 — Perfil Formativo Académico:**
       - Selector de Ciclo Académico Actual (Ciclos I al X).
       - Selector de Rol / Intención: *Mentoreado* (demanda de asesoría) vs. *Postulante a Mentor* (oferta formativa).
       - **Validación de Mérito Institucional (Regla RN-03):** detección preventiva y alerta visible si un estudiante con ciclo $< \text{VII}$ intenta postularse a Mentor, informando que la tutoría avanzada está normativamente restringida a los ciclos VII a X.
       - Selección interactiva de materias filtro de interés (necesidades o fortalezas) sobre el catálogo EPIS-UPT.
       - Selector de Modalidad Preferida: *Presencial* (laboratorios EPIS), *Virtual* (Google Meet/Discord) o *Híbrida*.
       - Campo de texto para semblanza y temas específicos de enfoque.
    2. **Pestaña 2 — Agenda Semanal de Disponibilidad Horaria:**
       - Grilla interactiva semanal: **6 columnas de días (Lunes a Sábado)** × **11 franjas horarias de 1 hora (08:00 a 20:00)**.
       - Alternancia de disponibilidad mediante clic en celdas (indicador visual de color verde esmeralda y marca de verificación).
       - Atajos rápidos de selección masiva: *"🌅 Mañanas (08:00 - 12:00)"*, *"🌇 Tardes (14:00 - 18:00)"* y *"🗑️ Limpiar semana"*.
       - Contador reactivo de bloques comprometidos (ej. *"8 bloques de 1 hora seleccionados"*).
  - Botón de guardado unificado *"💾 Guardar Perfil y Disponibilidad"* con feedback de carga y alertas de confirmación.

- **Servicio y Adaptador (`aplicacion/frontend/src/services/profileService.ts`):**
  - Interfaces tipadas `AcademicProfile` y `AvailabilitySlot`.
  - Métodos `getProfile()`, `saveProfile()`, `getAvailability()`, `saveAvailability()` y `validateMentorEligibility()`.
  - Persistencia local en modo mock en `localStorage` con claves `p2p_profile_*` y `p2p_availability_*`, asegurando persistencia entre recargas y pruebas sin depender del backend.

### 4.2. Comprobaciones Realizadas y Resultados Observados

### Cuadro 4.1: Matriz de Pruebas de Perfiles y Disponibilidad Horaria (T-11)

| Suite / Prueba | Escenario Evaluado | Comportamiento Esperado | Resultado Observado | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **`profileService`** | Validación de regla RN-03 | Ciclo 6: ineligible; Ciclo 7 y 10: eligible | Booleanos correctos y mensaje de regla | ✅ Exitoso |
| **`profileService`** | Obtención de perfil por defecto | Retornar perfil institucional inicializado | Perfil tipado con materias de interés | ✅ Exitoso |
| **`profileService`** | Guardado y recuperación | Persistir biografía y modalidad virtual | Datos idénticos recuperados en consulta | ✅ Exitoso |
| **`profileService`** | Bloqueo de postulación inválida | Lanzar error si rol mentor tiene ciclo < 7 | Excepción con motivo RN-03 arrojada | ✅ Exitoso |
| **`profileService`** | Guardado de agenda horaria | Persistir array de slots y contar total | 2 slots guardados con horarios correctos | ✅ Exitoso |
| **`ProfileView`** | Render inicial de formulario | Desplegar selectores de ciclo y rol | Elementos interactivos presentes | ✅ Exitoso |
| **`ProfileView`** | Disparo de alerta RN-03 | Mostrar advertencia al pulsar Postulante a Mentor | Banner rojo de mérito RN-03 visible | ✅ Exitoso |
| **`ProfileView`** | Pestaña de agenda semanal | Mostrar grilla de Lunes a Sábado | 6 columnas de días y horarios renderizados | ✅ Exitoso |
| **`ProfileView`** | Botón Limpiar agenda | Reiniciar selección horaria a 0 horas | Contador indica `0 bloques de 1 hora` | ✅ Exitoso |
| **`ProfileView`** | Guardado exitoso general | Guardar datos y disparar callback `onSaved` | Mensaje de éxito y callback ejecutado | ✅ Exitoso |

Fuente: Pruebas unitarias en `src/services/__tests__/profileService.test.ts` y `src/components/__tests__/ProfileAvailabilityView.test.tsx`.

---

## 5. Integración y Navegación SPA del Sprint 2

- **Componente Principal (`aplicacion/frontend/src/App.tsx`):**
  - Se actualizó la barra de navegación institucional superior con cinco pestañas temáticas activas para el Sprint 2:
    1. `🔐 Acceso & OTP (T-02)`: flujo de acceso institucional de 2 pasos.
    2. `⚖️ Consentimiento Ley 29733 (T-04)`: vista del formulario de consentimiento digital.
    3. `📚 Catálogo Curricular (T-10)`: buscador avanzado de asignaturas filtro y temarios.
    4. `👤 Perfil & Disponibilidad (T-11)`: configuración del perfil académico y agenda semanal.
    5. `🛰️ Monitor de Servicios (T-01)`: estado operativo de FastAPI y Supabase.
- **Prueba de Integración de Navegación (`aplicacion/frontend/src/__tests__/App.test.tsx`):**
  - Valida la alternancia reactiva entre las cinco vistas sin errores de ciclo de vida ni desbordamientos en el DOM virtual.

---

## 6. Métricas Consolidadas de Calidad y Cobertura (Vitest v8)

Al término del desarrollo de las tareas de Joan, se ejecutó la suite completa de pruebas unitarias y de integración junto con el análisis estático de estilos y compilación de producción:

### Cuadro 6.1: Resultados de Calidad, Linteo y Cobertura Frontend (Sprint 2 — Tareas de Joan)

| Métrica / Comprobación | Herramienta | Umbral Requerido | Resultado Real Observado | Estado |
| :--- | :--- | :---: | :---: | :---: |
| **Suites de Pruebas** | Vitest 2.1.8 | Todas aprobadas | **11 suites aprobadas (100%)** | ✅ Exitoso |
| **Total de Pruebas** | Vitest 2.1.8 | 100% aprobadas | **66 pruebas pasadas (0 fallidas, 0 omitidas)** | ✅ Exitoso |
| **Cobertura en Líneas** | Vitest Coverage (v8) | $\ge 70.0\%$ (RNF09) | **91.10%** (+21.10% sobre la meta) | ✅ Exitoso |
| **Cobertura en Sentencias** | Vitest Coverage (v8) | $\ge 70.0\%$ (RNF09) | **91.10%** (+21.10% sobre la meta) | ✅ Exitoso |
| **Cobertura en Ramas** | Vitest Coverage (v8) | — | **75.18%** | ✅ Exitoso |
| **Cobertura en Funciones** | Vitest Coverage (v8) | — | **71.96%** | ✅ Exitoso |
| **Análisis Estático (Lint)** | ESLint 9 + TypeScript | 0 errores / 0 warnings | **0 errores, 0 advertencias** | ✅ Exitoso |
| **Compilación de Producción** | `tsc -b && vite build` | 0 errores de tipado | **43 módulos compilados en 1.43s (0 errores)** | ✅ Exitoso |

Fuente: Registro de ejecución de `npm run test:coverage`, `npm run lint` y `npm run build` en `aplicacion/frontend`.

---

## 7. Registro de Versiones y Comandos Reproducibles

### 7.1. Detalle del Commit
```bash
commit 3766a08fa98d49bc6107a9fd278568f289f7fe74
Author: JMedina255 <jm2022074255@virtual.upt.pe>
Date:   Fri Oct 23 15:23:24 2026 -0500

    feat(s2-frontend): implementar consentimiento digital, catalogo curricular avanzado y perfil con disponibilidad [T-04, T-10, T-11]
```
- **Rama:** `feat/sprint-02-roles-curriculo-perfiles`
- **Seguimiento remoto:** `origin/feat/sprint-02-roles-curriculo-perfiles` (publicado exitosamente en GitHub).
- **PR sugerido:** `https://github.com/JMedina255/sistema_web_p2p/pull/new/feat/sprint-02-roles-curriculo-perfiles`

### 7.2. Comandos para Validación Local Reproducible
```powershell
# 1. Acceder al directorio frontend
cd aplicacion/frontend

# 2. Verificar linteo y ausencia de advertencias
npm run lint

# 3. Ejecutar suite completa de 66 pruebas con reporte de cobertura
npm run test:coverage

# 4. Probar empaquetado de producción
npm run build

# 5. Iniciar servidor de desarrollo para inspección interactiva
npm run dev
```

---

## 8. Conclusiones y Próximos Pasos del Sprint 2

1. **Culminación del Alcance de Joan:** Se completaron satisfactoriamente las tres tareas asignadas a Joan (**T-04**, **T-10** y **T-11**), alcanzando 7 horas planificadas de esfuerzo verificadas con código limpio, tipado estricto en TypeScript y 66 pruebas unitarias y de componentes.
2. **Habilitación para las Tareas de Renzo:** La interfaz y los adaptadores de datos (`consentService.ts` y `profileService.ts`) cuentan con firmas tipadas preparadas para enlazarse con los endpoints que construirá Renzo en las tareas **T-05** (persistencia de consentimiento), **T-08** (administración de roles) y **T-12** (API de perfiles y horarios).
3. **Cierre de Sprint 2:** Una vez completadas las tareas de Renzo y ejecutadas las pruebas de autorización multi-perfil (**T-13**), se procederá al merge hacia `main` y a la emisión del informe académico formal del Sprint 02.
