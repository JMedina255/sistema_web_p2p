# Bitácora de Ejecución — Sprint 3: Publicación de Ofertas (Avance Parcial T-14)

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
**Curso:** Construcción de Software I
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)
**Semestre Académico:** 2026-II
**Equipo:** Grupo 03 — Joan Cristian Medina Quispe (Joan) y Renzo Antonio Antayhua Mamani (Renzo)
**Rama de trabajo:** `main`
**Fecha de corte documental:** 26/10/2026
**Commits de desarrollo del Sprint 3:**
- [`6de5653`](https://github.com/JMedina255/sistema_web_p2p/commit/6de5653) — `feat(s3-frontend): implementar servicio tipado y validaciones de ofertas [T-14]`
- [`148d12d`](https://github.com/JMedina255/sistema_web_p2p/commit/148d12d) — `feat(s3-frontend): desarrollar formulario reactivo de publicacion de ofertas [T-14]`
- [`e197efb`](https://github.com/JMedina255/sistema_web_p2p/commit/e197efb) — `feat(s3-frontend): integrar publicacion de ofertas en navegacion principal [T-14]`

> [!IMPORTANT]
> **Alcance del Corte Operativo del Sprint 3 (26/10/2026):**
> El presente documento registra la culminación técnica y verificación exhaustiva de la tarea **T-14** (Formulario de publicación de ofertas), correspondiente al alcance asignado a Joan en la capa de frontend. Las tareas de backend **T-15** (API básica de ofertas) y **T-16** (Estructura de datos y relaciones de ofertas), asignadas a Renzo, se encuentran **pendientes de implementación**. El frontend opera actualmente mediante un adaptador mock explícito de desarrollo debidamente señalizado. **El Sprint 3 permanece en estado EN DESARROLLO y no se declara cerrado en su totalidad.**

---

## 1. Visión General y Alcance del Sprint 3

El **Sprint 3** tiene como objetivo fundamental habilitar el mecanismo por el cual los estudiantes habilitados con el rol de Mentor Académico (ciclos VII al X, conforme a la regla de mérito **RN-03**) pueden programar, parametrizar y publicar ofertas de asesoría docente grupal vinculadas a las materias críticas del plan de estudios (**RF08** / **CUS06**).

Este hito representa el eslabón formativo indispensable para alimentar el catálogo activo de mentorías que será indexado y procesado por el motor de recomendación inteligente *Top-k* híbrido en el **Sprint 4** (**RF06** / **CUS02**).

A continuación, se presenta la matriz operativa de asignación, estimación y estado técnico del Sprint 3:

### Cuadro 1.1: Matriz de Tareas y Estado Técnico de Desarrollo del Sprint 3

| ID | Actividad Oficial | Responsable | Esfuerzo Planificado (h) | Estado Técnico Actual | Entregable / Evidencia |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T-14** | Desarrollar formulario de publicación de ofertas. | Joan | 2 | **Implementado y Verificado** ✅ | Componente `OfferPublishView.tsx`, servicio `offerService.ts`, integración en `App.tsx` y 21 pruebas en Vitest. |
| **T-15** | Implementar API básica de gestión de ofertas. | Renzo | 2 | **Pendiente de Implementación** ⏳ | Endpoints `POST /api/v1/offers`, `GET /api/v1/offers` y validación de tokens JWT. |
| **T-16** | Crear estructura de datos y relaciones de ofertas. | Renzo | 1 | **Pendiente de Implementación** ⏳ | Modelo ORM `SesionMentoria`, migración Alembic 003 y restricciones relacionales. |

Fuente: Elaboración propia a partir de `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Tabla 5.4) y avance real en la rama `main`.

El cuadro anterior refleja un avance en esfuerzo de 2 horas de las 5 horas-persona planificadas para el sprint (40.0% del esfuerzo), habiéndose completado la totalidad de los requisitos de interfaz de usuario, accesibilidad y validaciones de negocio del cliente.

---

## 2. Registro de Ejecución — Tarea T-14 (Formulario de Publicación de Ofertas)

### 2.1. Alcance Implementado y Reglas de Negocio Incorporadas

La tarea **T-14** fue desarrollada por Joan respetando los estándares de diseño institucional (paleta EPIS-UPT `#1C2A59` y `#B99451`), accesibilidad WAI-ARIA y rigurosidad técnica:

1. **Selección Curricular Dinámica (CUS21 / RF05):**
   - El formulario consulta el catálogo oficial mediante `fetchCourses(true)` para poblar las asignaturas críticas de I a IV ciclo (*Cálculo I, Cálculo II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos, Base de Datos*).
   - Al seleccionar una asignatura, se dispara la carga reactiva de unidades temáticas silábicas oficiales (`fetchCourseDetail`), permitiendo vincular la clase a un tema conceptual específico.
   - Dispone de fallback local tipado para garantizar la operatividad de la interfaz durante pruebas sin conexión activa.

2. **Control Estricto de Aforos Inmutables (Regla RN-05 / CUS06-U02):**
   - El aforo de la clase se calcula y fija de forma automática según la modalidad pedagógica elegida:
     - **Modalidad Presencial:** exactamente **10 estudiantes** (aforo estándar para aulas y laboratorios de la EPIS).
     - **Modalidad Virtual:** exactamente **20 estudiantes** (aforo estándar para salas virtuales).
   - El campo en la interfaz es estrictamente de solo lectura (`readOnly`), imposibilitando cualquier manipulación del límite normativo por parte del usuario.

3. **Validación Reactiva de Antelación (Regla RN-04):**
   - **Restricción obligatoria ($T > 24\text{ h}$):** La sesión debe programarse con más de 24 horas de antelación respecto a la hora del sistema (`Date.now()`). Si la antelación es $\le 24\text{ h}$, el formulario despliega una alerta roja de infracción de la regla **RN-04** y deshabilita el botón de envío, protegiendo la ventana obligatoria de confirmación previa y cómputo de quórum a $T-24\text{ h}$ (**RN-08** y **RN-09**).
   - **Recomendación pedagógica ($T \ge 48\text{ h}$):** Si la antelación es mayor a 24 horas pero menor a 48 horas, se autoriza la publicación pero se muestra un aviso formativo ámbar sugiriendo programar con al menos 48 h para favorecer la difusión en el recomendador. Si es $\ge 48\text{ h}$, se muestra un distintivo verde de antelación óptima.

4. **Duración Lectiva Normalizada:**
   - Selector de duración en bloques pedagógicos de **60 minutos** (1 hora pedagógica) o **90 minutos** (1.5 horas pedagógicas), calculando automáticamente la hora estimada de término de la sesión.

5. **Infraestructura Físico-Virtual Diferenciada:**
   - **Presencial (RN-06):** Selección y sugerencia de recintos académicos del catálogo institucional de la EPIS (*Laboratorio de Cómputo 101*, *Lab Redes 202*, *Aula Magna 104*). La interfaz presenta estos espacios como aulas sugeridas preliminares; la validación y verificación automatizada de disponibilidad en tiempo real contra la carga lectiva regular (RN-06) corresponde al subsistema backend mediante el procesamiento de horarios.
   - **Virtual (RN-07):** Generación simulada en cliente de enlace de demostración con formato institucional Google Meet (`https://meet.google.com/upt-[codigo]-[hash]`) con opción de regeneración interactiva. La provisión desatendida y creación real de la sala de videoconferencia en el servicio institucional corresponde a la integración de backend (RN-07).

6. **Control de Flujo, Feedback y Prevención de Duplicados:**
   - Deshabilitación de envíos concurrentes mediante bandera `isSubmitting`.
   - Confirmación visual destacada tras la publicación, emitiendo un identificador simulado de sesión (`SES-XXXX`), estado `PUBLICADA` y tarjeta resumen en el almacenamiento local temporal.
   - Historial de ofertas publicadas por el mentor durante la sesión de trabajo.

### 2.2. Arquitectura de Software y Contratos TypeScript

Se diseñó el servicio tipado [`aplicacion/frontend/src/services/offerService.ts`](../../aplicacion/frontend/src/services/offerService.ts), estructurado bajo el patrón fachada con separación de adaptadores:

```typescript
export type SessionModality = 'presencial' | 'virtual';
export type SessionDuration = 60 | 90;

export interface PublishOfferPayload {
  id_asignatura: number;
  codigo_asignatura: string;
  nombre_asignatura: string;
  id_tema: number;
  nombre_tema: string;
  fecha_inicio: string; // ISO 8601
  duracion_minutos: SessionDuration;
  modalidad: SessionModality;
  aforo_maximo: number; // 10 para presencial, 20 para virtual (RN-05)
  espacio_asignado: string;
  mentor_email: string;
  mentor_nombre?: string;
  notas_adicionales?: string;
}

export interface PublishOfferResponse {
  id_oferta: string;
  codigo_sesion: string; // Formato SES-XXXX
  estado: 'PUBLICADA';
  mensaje: string;
  fecha_publicacion: string;
  aforo: number;
  espacio_asignado: string;
  modo: 'mock' | 'api';
  offer: PublishOfferPayload;
}
```

### 2.3. Delimitación Técnica: Publicación Simulada vs. Persistencia Real en Base de Datos

> [!WARNING]
> **Diferenciación de Entorno y Persistencia:**
> - **Comportamiento Actual (Modo Mock):** Las ofertas creadas mediante `OfferPublishView.tsx` se procesan a través del adaptador local `MockOfferAdapter`, almacenándose en memoria y en la clave `p2p_offers_mock_sprint03` del `localStorage` del navegador. La interfaz despliega de manera permanente y accesible el banner:
>   **«Modo de prueba local — Backend pendiente (T-14 · Joan)»**.
>   Los identificadores emitidos (formato `SES-XXXX`) corresponden exclusivamente a identificadores simulados de demostración local para el ciclo de vida del cliente, no a claves primarias ni secuencias relacionales persistidas.
> - **Persistencia Real en Base de Datos:** **No se encuentra activa.** La inserción física de registros en la tabla relacional `sesiones_mentoria` de PostgreSQL/Supabase depende estrictamente de la finalización de las tareas **T-15** y **T-16** asignadas a Renzo. El sistema no simula falsamente que los datos han sido replicados en el servidor.

---

## 3. Catálogo de Pruebas Automatizadas y Evidencias de Calidad (T-14)

El desarrollo de T-14 se contrastó frente a los casos de prueba estipulados en el catálogo oficial del proyecto ([`docs/analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](../analisis/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx)), implementando 21 pruebas automatizadas nuevas en Vitest.

A continuación, se detalla la matriz de correspondencia y resultados empíricos obtenidos:

### Cuadro 3.1: Matriz de Trazabilidad de Casos de Prueba del Catálogo (T-14)

| Caso de Prueba | Tipo / Nivel | Escenario Evaluado | Comportamiento Esperado | Resultado Observado en Vitest | Estado |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **CUS06-U01** | Unitaria / Componente | Validación de campos obligatorios en el servicio y formulario. | Rechazar payload carente de asignatura, tema, fecha, modalidad o infraestructura; listar mensajes de error específicos. | Errores detectados en `validateOfferPayload`, botón de envío deshabilitado en formulario. | ✅ Superado |
| **CUS06-U02** | Unitaria / Componente | Asignación de aforo automático por defecto según modalidad (RN-05). | Aplicar estrictamente 10 cupos para presencial y 20 para virtual; rechazar valores discordantes. | Aforo inmutable fijado en `STANDARD_CAPACITY`, actualizado reactivamente en el DOM. | ✅ Superado |
| **CUS06-F01** | Funcional / Sistema | Flujo interactivo de publicación con sugerencia de aula física (RN-06). | Permitir seleccionar curso, tema silábico, aula sugerida de laboratorio EPIS y registrar la oferta en modo mock con código `SES-XXXX`. | Oferta publicada exitosamente, tarjeta verde de confirmación y registro en historial. | ✅ Superado |
| **CUS06-F02** | Funcional / Sistema | Flujo de publicación virtual y validación de antelación temporal (RN-04 / RN-07). | Generar enlace Meet de demostración con formato institucional (@upt.pe); alertar y bloquear si antelación es $\le 24\text{ h}$; avisar si $< 48\text{ h}$. | Bloqueo perentorio con antelación $\le 24\text{ h}$, badge de recomendación con $36\text{ h}$, enlace Meet generado. | ✅ Superado |

Fuente: Elaboración propia a partir de `Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx` y ejecución de suites en `aplicacion/frontend/src/services/__tests__/offerService.test.ts` y `aplicacion/frontend/src/components/__tests__/OfferPublishView.test.tsx`.

La matriz anterior certifica que la capa de presentación y la lógica de validación del cliente cumplen rigurosamente con los cuatro criterios funcionales y unitarios definidos en la etapa de análisis para el caso canónico CUS06.

---

## 4. Métricas Consolidadas de Calidad de Software

Tras completar la implementación e integración de T-14, se ejecutó una auditoría integral sobre ambos subsistemas (`aplicacion/frontend` y `aplicacion/backend`):

A continuación, se detalla el balance de pruebas automatizadas, cobertura y análisis estático:

### Cuadro 4.1: Balance Métrico Consolidado de Pruebas y Cobertura (Sprint 3 Parcial)

| Dimensión de Calidad | Herramienta | Umbral RNF09 | Frontend (Joan: T-04, T-10, T-11, T-14) | Backend (Sprint 1 & 2) | Total Consolidado | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Suites de Prueba** | Vitest 2.1.8 / Pytest 9.1.1 | 100% aprobadas | 13 suites | 10 suites | **23 suites aprobadas** | ✅ Superado |
| **Pruebas Automatizadas** | Vitest / Pytest | 100% aprobadas | **87 pruebas** (0 fallos) | **84 pruebas** (0 fallos) | **171 pruebas aprobadas** | ✅ Superado |
| **Cobertura Frontend (Líneas)** | Vitest v8 | $\ge 70.0\%$ | **92.52%** | N/A | **92.52%** | ✅ Superado |
| **Cobertura Backend (Líneas)** | Pytest-Cov | $\ge 70.0\%$ | N/A | **91.00%** | **91.00%** | ✅ Superado |
| **Cobertura de T-14** | Vitest v8 | $\ge 70.0\%$ | `OfferPublishView.tsx`: **97.32%**<br>`offerService.ts`: **86.46%** | N/A (Backend pendiente) | **> 90% en módulo** | ✅ Superado |
| **Linteo Estático** | ESLint 9 / Ruff 0.9 | 0 errores | 0 errores, 0 warnings | 0 errores (All checks passed!) | **0 defectos estáticos** | ✅ Superado |
| **Formato de Código** | Prettier / Ruff format | 100% estándar | Código formateado | 49 archivos conformes | **100% estandarizado** | ✅ Superado |
| **Compilación de Producción** | Vite Build (`tsc -b`) | 0 errores tipado | 45 módulos en 1.30 s (`dist/`) | N/A | **Empaquetado limpio** | ✅ Superado |

Fuente: Elaboración propia a partir de las ejecuciones de `npm run test:coverage`, `npm run lint`, `npm run build` en `aplicacion/frontend` y `pytest tests/ --cov=app`, `ruff check .`, `ruff format --check .` en `aplicacion/backend`.

> [!NOTE]
> **Metodología de Reporte de Cobertura (Regla 3.2.7):**
> De conformidad con las directrices de documentación de software, las métricas de cobertura de frontend (Vitest v8) y backend (Pytest-Cov) se reportan de forma estrictamente independiente. No se presentan valores promediados ni agregados sin una metodología unificada de instrumentación que consolide líneas físicas ejecutadas. Ambos subsistemas superan individualmente con amplio margen el umbral normativo del 70.0% estipulado en el RNF09.

Los resultados confirman que el incremento mantiene los altos estándares de calidad institucional, incrementando la batería de pruebas de 150 a 171 pruebas automatizadas sin incurrir en regresiones sobre las funcionalidades de los sprints anteriores.

---

## 5. Secciones Reservadas para el Desarrollo de Backend (Renzo)

Las siguientes dos secciones quedan formalmente estructuradas como plantilla para que Renzo incorpore los detalles técnicos, artefactos y evidencias de persistencia una vez ejecutadas sus tareas asignadas:

---

### 5.1. T-15 — Implementación de API Básica de Gestión de Ofertas (Renzo)

- **Responsable:** Renzo Antonio Antayhua Mamani.
- **Estimación Planificada:** 2 horas.
- **Estado Técnico:** **PENDIENTE DE IMPLEMENTACIÓN ⏳**.
- **Trazabilidad:** RF08 (Publicación de ofertas), RF09 (Aprovisionamiento de espacios), CUS06.

#### A. Criterios de Aceptación
1. Exponer endpoint `POST /api/v1/offers` para recepción de payloads conformes al esquema de validación.
2. Validar que el usuario autenticado mediante Bearer JWT posea rol activo de Mentor Académico (**RN-03**).
3. Verificar la antelación mínima obligatoria $> 24\text{ h}$ en servidor (**RN-04**) y forzar aforos inmutables (**RN-05**).
4. Exponer endpoint `GET /api/v1/offers` con filtros opcionales por asignatura, ciclo y correo de mentor.
5. Devolver códigos HTTP semánticos: `201 Created`, `400 Bad Request` (infracción de antelación o aforo), `401 Unauthorized` y `403 Forbidden` (no mentor).

#### B. Registro de Implementación (Espacio reservado para Renzo)
*Espacio reservado para documentar routers FastAPI (`app/api/v1/endpoints/offers.py`), esquemas Pydantic (`app/schemas/offer.py`), inyección de dependencias y servicios de dominio (`app/services/offer_service.py`).*

#### C. Pruebas y Evidencias (Espacio reservado para Renzo)
*Espacio reservado para registrar la matriz de pruebas automatizadas en Pytest (`tests/test_offers.py`), tiempos de respuesta y porcentaje de cobertura alcanzado.*

#### D. Commits y Archivos Modificados (Espacio reservado para Renzo)
*Espacio reservado para listar hashes de commits, líneas modificadas y artefactos incorporados al repositorio.*

---

### 5.2. T-16 — Creación de Estructura de Datos y Relaciones de Ofertas (Renzo)

- **Responsable:** Renzo Antonio Antayhua Mamani.
- **Estimación Planificada:** 1 hora.
- **Estado Técnico:** **PENDIENTE DE IMPLEMENTACIÓN ⏳**.
- **Trazabilidad:** Modelo relacional físico, diccionario de datos SAD FD04, CUS06.

#### A. Criterios de Aceptación
1. Declarar modelo SQLAlchemy `SesionMentoria` / `OfertaMentoria` con claves foráneas íntegras a `usuarios` (mentor), `asignaturas` y `temas_silabicos`.
2. Incluir restricciones a nivel de base de datos (`CHECK (modalidad IN ('presencial', 'virtual'))`, restricciones de no nulidad y estados de sesión).
3. Generar y aplicar migración Alembic `003_mentoring_offers.py` sincronizada sobre la base de datos de Supabase.
4. Definir políticas de seguridad Row Level Security (RLS) para inserción exclusiva por mentores y lectura pública de ofertas publicadas.

#### B. Registro de Implementación (Espacio reservado para Renzo)
*Espacio reservado para documentar el modelo ORM (`app/models/offer.py`), migración Alembic generada y script SQL de políticas RLS correspondientes.*

#### C. Pruebas y Evidencias (Espacio reservado para Renzo)
*Espacio reservado para registrar pruebas de integridad referencial, transaccionalidad ACID y verificación de aplicación DDL en PostgreSQL.*

#### D. Commits y Archivos Modificados (Espacio reservado para Renzo)
*Espacio reservado para registrar commits y archivos de base de datos.*

---

## 6. Estado Técnico del Sprint 3, Riesgos y Próximos Pasos

A continuación, se detalla el balance cuantitativo de avance al cierre parcial del frontend:

### Cuadro 6.1: Balance de Cumplimiento Parcial del Sprint 3

| Componente de Evaluación | Planificado | Ejecutado (Joan) | Pendiente (Renzo) | % Avance Real |
| :--- | :---: | :---: | :---: | :---: |
| **Tareas del Sprint** | 3 tareas | 1 tarea (T-14) | 2 tareas (T-15, T-16) | **33.3%** |
| **Esfuerzo Estimado** | 5.0 horas | 2.0 horas | 3.0 horas | **40.0%** |
| **Pruebas Automatizadas del Sprint** | Variable | 21 pruebas frontend | Pruebas backend pendientes | **Parcial** |
| **Definition of Done (DoD) Integral** | 6 criterios | Criterios 1, 2, 3 en FE | Persistencia y DDL pendientes | **En Curso** |

Fuente: Elaboración propia a partir de la planificación del Sprint 3.

El balance anterior fundamenta que el Sprint 3 se encuentra formalmente **en desarrollo**, con su subsistema de cliente verificado y listo para el acoplamiento con la API RESTful de backend.

### 6.1. Riesgos Identificados y Dependencias
1. **Dependencia de Transición hacia el Sprint 4:** El motor de recomendación *Top-k* (Sprint 4: T-17 a T-24) requiere consultar las ofertas activas mediante endpoint REST. Si T-15 y T-16 sufren demoras, el recomendador deberá iniciar trabajando contra datos semilla locales en FastAPI.
2. **Desfase de Esquemas de Datos:** El contrato TypeScript definido en `offerService.ts` debe ser adoptado estrictamente por Renzo en los esquemas Pydantic de T-15 para evitar incompatibilidades de serialización.

### 6.2. Próximos Pasos Inmediatos
1. Notificar a Renzo la disponibilidad de los contratos tipados en `offerService.ts`.
2. Implementación de T-16 (modelo relacional y migración Alembic 003).
3. Implementación de T-15 (endpoints FastAPI y autenticación JWT).
4. Alternancia del modo en frontend de `'mock'` a `'api'` mediante `offerService.setMode('api')` y ejecución de pruebas E2E de integración.
5. Cierre definitivo del Sprint 3 mediante acta formal con doble firma.

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — Octubre 2026*
