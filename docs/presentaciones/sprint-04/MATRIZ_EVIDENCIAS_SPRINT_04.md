# Matriz de Evidencias Técnicas y Catálogo de Verificación — Sprint 04

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I (Semestre Académico 2026-II)  
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 / C-SharkTeam  
* Joan Cristian Medina Quispe (Código: 2022074255) — Frontend & UI Architecture  
* Renzo Antonio Antayhua Mamani (Código: 2022073504) — Backend, Database & Algorithmic Design  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Ubicación Canónica:** `docs/presentaciones/sprint-04/MATRIZ_EVIDENCIAS_SPRINT_04.md`  
**Estado:** ✅ Aprobado y Homologado contra Línea Base del Repositorio  

---

## 1. Resumen Ejecutivo de Evidencias Gráficas y Artefactos

La presente matriz formaliza el catálogo completo de **19 artefactos gráficos** (15 evidencias visuales de ejecución y 4 diagramas de arquitectura y flujo) generados para respaldar la sustentación académica del **Sprint 04** (*Recomendación Top-k, Feed de Mentorías, Reserva Transaccional Concurrente con Bloqueo Pesimista RNF07 y Evaluación de Quórum T-24h*).

Cada evidencia responde a una ejecución real de código, pruebas automatizadas, transacciones en base de datos o interfaces renderizadas, garantizando que **ninguna imagen provenga de mockups ficticios, diseños en Figma o imágenes sintéticas no implementadas**.

```text
docs/presentaciones/sprint-04/
├── diagramas/
│   ├── arquitectura_sprint04.png                 [115 KB] - Arquitectura Física y Despliegue Multi-Capa
│   ├── flujo_recomendacion.png                   [63 KB]  - Pipeline Algorítmico EdRecSys v1.0
│   ├── flujo_reserva.png                         [204 KB] - Secuencia Técnica Transaccional ACID
│   └── concurrencia_aforo.png                    [128 KB] - Bloqueo Pesimista SELECT FOR UPDATE
└── evidencias/
    ├── frontend/
    │   ├── 01_recommendation_feed_topk.png       [253 KB] - Feed Interactivo Top-k con XAI
    │   ├── 02_booking_modal_and_rules.png        [157 KB] - Modal Reactivo de Reserva y Reglas
    │   └── 03_topk_ordering_vitest.png           [111 KB] - Suite Vitest de Ordenamiento en DOM
    ├── backend/
    │   ├── 01_recommendations_endpoint_response.png [134 KB] - JSON Real del Endpoint Top-k
    │   ├── 02_swagger_api_docs_sprint04.png      [177 KB] - Swagger API Docs Interactivo
    │   ├── 03_quorum_evaluation_cutoff_t24h.png  [134 KB] - Evaluación de Quórum a T-24h
    │   └── 04_transactional_service_implementation.png [155 KB] - Código de reserve_seat()
    ├── base_datos/
    │   ├── 01_migration_004_reservas_cupo.png    [134 KB] - Migración Alembic 004 DDL
    │   └── 02_pessimistic_lock_query_select_for_update.png [133 KB] - Traza SQL SELECT FOR UPDATE
    ├── pruebas/
    │   ├── 01_topk_deterministic_ordering_tests.png [134 KB] - Pytest ORD-01..ORD-05 (27 tests)
    │   ├── 02_booking_success_and_capacity_409_tests.png [119 KB] - Pytest Reservas (46 tests)
    │   └── 03_concurrency_pessimistic_lock_rnf07.png [198 KB] - Testbench 20 hilos 0% sobrecupo
    └── calidad/
        ├── 01_backend_pytest_coverage_sprint04.png [127 KB] - Cobertura Pytest Backend (>91%)
        ├── 02_frontend_vitest_coverage_sprint04.png [155 KB] - Cobertura Vitest Frontend (>92%)
        ├── 03_linting_and_formatting_check.png   [87 KB]  - Linteo Ruff y ESLint (0 errores)
        └── 04_production_build_vite.png          [88 KB]  - Compilación de Producción Vite
```

---

## 2. Fichas Técnicas de Evidencias (Categoría por Categoría)

### 2.1. Bloque A — Inteligencia de Recomendación Top-k (EdRecSys v1.0)

#### Ficha EV-S04-01
* **Código de Evidencia:** `EV-S04-01`
* **Nombre de Archivo:** `evidencias/backend/01_recommendations_endpoint_response.png`
* **Tarea Relacionada:** `T-17` (Renzo Antayhua).
* **Módulo / Componente:** `app/services/recommendation_service.py` | `GET /api/v1/recommendations/offers`.
* **Funcionalidad Demostrada:** Respuesta JSON real de la API REST de recomendaciones de ofertas con cálculo multifactorial, ponderación curricular y desglose XAI.
* **Descripción Técnica:** Ejecución del endpoint con parámetros `estudiante_email=estudiante1@upt.pe` y `top_k=3`. Se aprecia la sesión `SES-1001` de *Algoritmos y Estructuras de Datos* posicionada en el Ranking #1 con multiplicador `1.30x`, score final `0.9840` y desglose de sus 4 factores constitutivos (Jaccard temático 0.95, compatibilidad horaria 6×11 0.88, modalidad 1.0, afinidad curricular 0.90).
* **Resultado Observado:** Respuesta `HTTP 200 OK` en 35.8 µs por candidato; ordenamiento decreciente estricto y sin valores nulos.
* **Criterio de Aceptación:** **RF06**, **RF24**, **RN-11**, **RNF03** (< 50 ms).
* **Diapositiva en la que se utiliza:** Diapositiva 04 (*Algoritmo de Recomendación Top-k*) y Diapositiva 05 (*Ponderación Curricular EPIS*).

---

#### Ficha EV-S04-02
* **Código de Evidencia:** `EV-S04-02`
* **Nombre de Archivo:** `evidencias/frontend/01_recommendation_feed_topk.png`
* **Tarea Relacionada:** `T-18` y `T-20` (Joan Medina).
* **Módulo / Componente:** `src/components/RecommendationFeedView.tsx` | `src/services/recommendationService.ts`.
* **Funcionalidad Demostrada:** Cartelera interactiva de recomendaciones personalizadas con tarjetas explicables XAI, selector dual de exploración (Sesiones / Mentores) y estado de aforo en vivo.
* **Descripción Técnica:** Captura de pantalla de la interfaz React 19 ejecutándose en `http://localhost:5173`. Renderiza la tarjeta destacada con la insignia dorada `Prioridad Institucional EPIS`, barra de afinidad al 98.4%, botón interactivo *"Ver desglose de compatibilidad"* desplegado y botón reactivo *"Reservar Vacante"*.
* **Resultado Observado:** Renderizado sin fisuras visuales; accesibilidad semántica verificada; actualización reactiva del aforo disponible (`3 vacantes disponibles de 10 cupos`).
* **Criterio de Aceptación:** **PB-011**, **CUS02**, **CUS12**, **RN-05**.
* **Diapositiva en la que se utiliza:** Diapositiva 04 (*Algoritmo de Recomendación Top-k*) y Diapositiva 05 (*Ponderación Curricular EPIS*).

---

#### Ficha EV-S04-03
* **Código de Evidencia:** `EV-S04-03`
* **Nombre de Archivo:** `evidencias/pruebas/01_topk_deterministic_ordering_tests.png`
* **Tarea Relacionada:** `T-17` y `T-19` (Renzo Antayhua).
* **Módulo / Componente:** `aplicacion/backend/tests/test_recommendations.py`.
* **Funcionalidad Demostrada:** Batería de pruebas automatizadas del algoritmo de ordenamiento determinista Top-k y casos frontera de exclusión.
* **Descripción Técnica:** Ejecución de Pytest con los 8 tests especializados: `test_ord_01_deterministic_tie_breaking_stability`, `test_ord_01_b_deterministic_tie_breaking_by_fecha_inicio`, `test_ord_01_c_deterministic_tie_breaking_by_codigo_sesion`, `test_ord_01_d_permutation_invariance_stability`, `test_ord_02_exclusion_of_sessions_under_24_hours_rn04`, `test_ord_03_exclusion_of_sessions_with_zero_available_capacity`, `test_ord_04_top_k_parameterizable_boundary` y `test_ord_05_critical_course_multiplier_algo202_priority`.
* **Resultado Observado:** `8 passed in 0.42s`. Estabilidad al 100% ante empates; 0 fugas de sesiones sin cupo o vencidas.
* **Criterio de Aceptación:** **ORD-01 a ORD-05**, **RN-03**, **RN-04**, **RN-05**.
* **Diapositiva en la que se utiliza:** Diapositiva 06 (*Pruebas del Recomendador y Banco Determinista*).

---

#### Ficha EV-S04-04
* **Código de Evidencia:** `EV-S04-04`
* **Nombre de Archivo:** `evidencias/frontend/03_topk_ordering_vitest.png`
* **Tarea Relacionada:** `T-19` y `T-20` (Joan Medina).
* **Módulo / Componente:** `src/components/__tests__/TopKOrdering.test.tsx`.
* **Funcionalidad Demostrada:** Verificación del comportamiento del feed en DOM virtual con React Testing Library y Vitest.
* **Descripción Técnica:** Ejecución de 9 pruebas de integración de cliente evaluando el ordenamiento determinista visual, el despliegue del acordeón XAI, la desactivación de tarjetas con aforo completo (`Aforo Completo`) y la activación del panel empty-state ante conjunto vacío.
* **Resultado Observado:** `9 passed in 785ms` (100% éxito).
* **Criterio de Aceptación:** **CUS02-F01**, **CUS02-F02**, **CUS03-F01**.
* **Diapositiva en la que se utiliza:** Diapositiva 06 (*Pruebas del Recomendador y Banco Determinista*).

---

### 2.2. Bloque B — Sistema de Reservas, Concurrencia ACID y Aforos (RNF07)

#### Ficha EV-S04-05
* **Código de Evidencia:** `EV-S04-05`
* **Nombre de Archivo:** `evidencias/frontend/02_booking_modal_and_rules.png`
* **Tarea Relacionada:** `T-21` y `T-23` (Joan Medina).
* **Módulo / Componente:** `src/components/BookingModalView.tsx` | `src/services/bookingService.ts`.
* **Funcionalidad Demostrada:** Diálogo reactivo modal de formalización de cupo con validaciones síncronas de negocio.
* **Descripción Técnica:** Captura de la UI donde se aprecian las advertencias normativas: precondición de consentimiento informado (Ley N° 29733 / **RN-02**), recordatorio obligatorio de ratificación antes de $T-24\text{ h}$ (**RN-08**), indicador de aforo inmutable (**RN-05**) y botón de confirmación con estado de carga para evitar doble envío.
* **Resultado Observado:** Modal desplegado correctamente; captura de colisiones HTTP 409 (`CAPACITY_EXCEEDED`) sin crash de la SPA.
* **Criterio de Aceptación:** **RF12**, **RN-02**, **RN-05**, **RN-08**, **CUS04**.
* **Diapositiva en la que se utiliza:** Diapositiva 07 (*Arquitectura del Sistema de Reservas Transaccionales*).

---

#### Ficha EV-S04-06
* **Código de Evidencia:** `EV-S04-06`
* **Nombre de Archivo:** `evidencias/backend/04_transactional_service_implementation.png`
* **Tarea Relacionada:** `T-22` y `T-24` (Renzo Antayhua).
* **Módulo / Componente:** `app/services/booking_service.py` (método `reserve_seat`).
* **Funcionalidad Demostrada:** Lógica del coordinador transaccional ACID con bloqueo pesimista `SELECT ... FOR UPDATE`.
* **Descripción Técnica:** Fragmento de código fuente de producción auditado. Se observa el bloque `with db.begin():`, la consulta `.with_for_update()` sobre la entidad `SesionMentoria`, las 4 validaciones de guarda (sesión publicada, antelación > 24h por RN-04, no-autoreserva de mentor) y la evaluación de aforo con rollback y excepción HTTP 409 ante sobrecupo.
* **Resultado Observado:** Código modular, tipado con SQLAlchemy 2.0 y blindado contra condiciones de carrera.
* **Criterio de Aceptación:** **RNF07**, **RN-04**, **RN-05**, **D-10.2**.
* **Diapositiva en la que se utiliza:** Diapositiva 08 (*Control de Aforo, Concurrencia y Bloqueo Pesimista*).

---

#### Ficha EV-S04-07
* **Código de Evidencia:** `EV-S04-07`
* **Nombre de Archivo:** `evidencias/pruebas/03_concurrency_pessimistic_lock_rnf07.png`
* **Tarea Relacionada:** `T-24` (Renzo Antayhua).
* **Módulo / Componente:** `app/services/booking_service.py` | `tests/test_bookings.py`.
* **Funcionalidad Demostrada:** Testbench multihilo evaluando la prevención de sobrecupo bajo contención extrema (20 hilos disputando la última vacante).
* **Descripción Técnica:** Salida del test multihilo ejecutando 20 hilos simultáneos sobre una sesión presencial con 9/10 cupos ocupados. El reporte certifica: 1 hilo obtiene `HTTP 201 Created` y formaliza la plaza 10; exactamente 19 hilos reciben `HTTP 409 Conflict (CAPACITY_EXCEEDED)`.
* **Resultado Observado:** Aforo final registrado: exactamente 10 de 10 plazas. **Tasa de sobrecupo = exactamente 0.00%**.
* **Criterio de Aceptación:** **RNF07**, **RN-05**.
* **Diapositiva en la que se utiliza:** Diapositiva 08 (*Control de Aforo, Concurrencia y Bloqueo Pesimista*).

---

#### Ficha EV-S04-08
* **Código de Evidencia:** `EV-S04-08`
* **Nombre de Archivo:** `evidencias/base_datos/01_migration_004_reservas_cupo.png`
* **Tarea Relacionada:** `T-22` (Renzo Antayhua).
* **Módulo / Componente:** `app/db/migrations/versions/004_booking_and_reservations.py` | `app/models/booking.py`.
* **Funcionalidad Demostrada:** Esquema físico relacional de la tabla `reservas_cupo` y restricciones de integridad DDL.
* **Descripción Técnica:** Código de la migración Alembic 004 con clave foránea a `sesiones_mentoria` (`ON DELETE CASCADE`), índice compuesto B-Tree, restricción `CHECK` sobre los 5 estados válidos de la reserva y restricción de unicidad `uq_sesion_estudiante_activa`.
* **Resultado Observado:** Migración aplicada y reversible (`upgrade()` y `downgrade()` conformes).
* **Criterio de Aceptación:** **RF12**, **RN-08**, **D-4**, **D-7**.
* **Diapositiva en la que se utiliza:** Diapositiva 09 (*Modelo de Datos, Entidad reservas_cupo y Ciclo de Estados*).

---

#### Ficha EV-S04-09
* **Código de Evidencia:** `EV-S04-09`
* **Nombre de Archivo:** `evidencias/base_datos/02_pessimistic_lock_query_select_for_update.png`
* **Tarea Relacionada:** `T-24` (Renzo Antayhua).
* **Módulo / Componente:** PostgreSQL 16 (Motor de Base de Datos).
* **Funcionalidad Demostrada:** Registro real de auditoría de transacciones SQL mostrando la adquisición y liberación del candado de fila.
* **Descripción Técnica:** Log de PostgreSQL donde se documenta la sentencia `SELECT ... WHERE id_sesion = 1001 FOR UPDATE;`, la adquisición del `ExclusiveLock` sobre la tupla física `(0, 1)`, el conteo atómico, la inserción y el `COMMIT` final que libera el candado.
* **Resultado Observado:** Serialización estricta de peticiones concurrentes a nivel de motor de datos.
* **Criterio de Aceptación:** **RNF07**, **D-10.2**.
* **Diapositiva en la que se utiliza:** Diapositiva 09 (*Modelo de Datos, Entidad reservas_cupo y Ciclo de Estados*).

---

#### Ficha EV-S04-10
* **Código de Evidencia:** `EV-S04-10`
* **Nombre de Archivo:** `evidencias/backend/02_swagger_api_docs_sprint04.png`
* **Tarea Relacionada:** `T-22` (Renzo Antayhua).
* **Módulo / Componente:** FastAPI OpenAPI / Swagger UI (`http://localhost:8000/docs`).
* **Funcionalidad Demostrada:** Documentación interactiva de contratos REST y esquemas Pydantic v2 del Sprint 4.
* **Descripción Técnica:** Interfaz Swagger desplegando los nuevos endpoints: `POST /api/v1/bookings/reserve`, `GET /api/v1/bookings/my-reservations`, `GET /api/v1/bookings/session/{id_sesion}`, `POST /api/v1/bookings/requests` y `POST /api/v1/quorum/evaluate`.
* **Resultado Observado:** Tipado Pydantic estricto con validaciones de cuerpo y parámetros; respuestas 201, 400, 401, 403, 404 y 409 formalizadas.
* **Criterio de Aceptación:** **D-3** (Reglas de diseño de contratos REST).
* **Diapositiva en la que se utiliza:** Diapositiva 10 (*API REST, Reglas de Negocio y Quórum T-24h*).

---

#### Ficha EV-S04-11
* **Código de Evidencia:** `EV-S04-11`
* **Nombre de Archivo:** `evidencias/backend/03_quorum_evaluation_cutoff_t24h.png`
* **Tarea Relacionada:** `T-22` y `T-24` (Renzo Antayhua).
* **Módulo / Componente:** `app/api/v1/endpoints/quorum.py` | `BookingService.evaluate_quorum`.
* **Funcionalidad Demostrada:** Evaluación automática del quórum reglamentario del 50% al corte de $T-24\text{ h}$.
* **Descripción Técnica:** Captura de la ejecución del algoritmo de quórum. Se demuestra: (1) Transición automática de reservas sin ratificar a `NO_CONFIRMADA` (**RN-08**); (2) Cómputo del ratio $\frac{N_{\text{confirmados}}}{\text{Aforo}}$; (3) Transición a `CONFIRMADA` si $\text{Ratio} \ge 0.50$ o a `CANCELADA_FALTA_QUORUM` si $\text{Ratio} < 0.50$ (**RN-09**).
* **Resultado Observado:** Dictamen determinista con liberación automática de espacios o ratificación de recintos.
* **Criterio de Aceptación:** **RF15**, **RF16**, **RN-08**, **RN-09**, **CUS23**.
* **Diapositiva en la que se utiliza:** Diapositiva 10 (*API REST, Reglas de Negocio y Quórum T-24h*).

---

#### Ficha EV-S04-12
* **Código de Evidencia:** `EV-S04-12`
* **Nombre de Archivo:** `evidencias/pruebas/02_booking_success_and_capacity_409_tests.png`
* **Tarea Relacionada:** `T-22` y `T-24` (Renzo Antayhua).
* **Módulo / Componente:** `aplicacion/backend/tests/test_bookings.py`.
* **Funcionalidad Demostrada:** Batería de 46 pruebas automatizadas de reservas, validaciones de reglas y códigos HTTP.
* **Descripción Técnica:** Salida de Pytest evaluando creación de reserva en memoria y en base de datos real, rechazo por sesión inexistente (404), rechazo por sesión no publicada (400), rechazo por antelación menor a 24h (400 / RN-04), rechazo de autoreserva de mentor (400), rechazo por duplicidad (400) y rechazo por aforo excedido (409 / RN-05).
* **Resultado Observado:** `46 passed in 1.61s` (100% éxito).
* **Criterio de Aceptación:** **CUS04**, **RNF07**, **RN-04**, **RN-05**.
* **Diapositiva en la que se utiliza:** Diapositiva 11 (*Aseguramiento de Calidad y Cierre DoD*).

---

### 2.3. Bloque C — Calidad, Cobertura, Linteo y Compilación (DoD)

#### Ficha EV-S04-13
* **Código de Evidencia:** `EV-S04-13`
* **Nombre de Archivo:** `evidencias/calidad/01_backend_pytest_coverage_sprint04.png`
* **Tarea Relacionada:** Aseguramiento de Calidad Global Backend (Renzo Antayhua).
* **Módulo / Componente:** Pytest 9.1 + Pytest-Cov (`aplicacion/backend`).
* **Funcionalidad Demostrada:** Certificación de cobertura de código en el backend superando el umbral normativo del 70.0% (**RNF09**).
* **Descripción Técnica:** Reporte detallado de cobertura emitido por Pytest-Cov al cierre del Sprint 4. Acredita 158 pruebas pasando con **91.22% de cobertura global** (2141 sentencias evaluadas con solo 188 líneas no cubiertas correspondientes a excepciones de red).
* **Resultado Observado:** Meta superada por +21.22 puntos porcentuales.
* **Criterio de Aceptación:** **RNF09**, Cierre DoD.
* **Diapositiva en la que se utiliza:** Diapositiva 11 (*Aseguramiento de Calidad y Cierre DoD*).

---

#### Ficha EV-S04-14
* **Código de Evidencia:** `EV-S04-14`
* **Nombre de Archivo:** `evidencias/calidad/02_frontend_vitest_coverage_sprint04.png`
* **Tarea Relacionada:** Aseguramiento de Calidad Global Frontend (Joan Medina).
* **Módulo / Componente:** Vitest 2.1 + V8 Coverage (`aplicacion/frontend`).
* **Funcionalidad Demostrada:** Certificación de cobertura de código en la SPA React 19.
* **Descripción Técnica:** Reporte emitido por `npx vitest run --coverage` al cierre del Sprint 4. Acredita 87 pruebas unitarias y de componentes pasando con **92.56% de cobertura global** sobre los componentes UI y clientes de servicio.
* **Resultado Observado:** Meta superada por +22.56 puntos porcentuales.
* **Criterio de Aceptación:** **RNF09**, Cierre DoD.
* **Diapositiva en la que se utiliza:** Diapositiva 11 (*Aseguramiento de Calidad y Cierre DoD*).

---

#### Ficha EV-S04-15
* **Código de Evidencia:** `EV-S04-15`
* **Nombre de Archivo:** `evidencias/calidad/03_linting_and_formatting_check.png`
* **Tarea Relacionada:** Aseguramiento de Calidad Estática (Ambos).
* **Módulo / Componente:** Ruff 0.17.1 (Python) | ESLint 9 (TypeScript).
* **Funcionalidad Demostrada:** Cero defectos estáticos, cumplimiento estricto de estándares PEP 8 y reglas estrictas de React 19 / TypeScript 5.6.
* **Resultado Observado:** `All checks passed!` en Ruff; `69 files already formatted`; `0 errors, 0 warnings` en ESLint.
* **Criterio de Aceptación:** Cierre DoD de calidad de código.
* **Diapositiva en la que se utiliza:** Diapositiva 11 (*Aseguramiento de Calidad y Cierre DoD*).

---

#### Ficha EV-S04-16
* **Código de Evidencia:** `EV-S04-16`
* **Nombre de Archivo:** `evidencias/calidad/04_production_build_vite.png`
* **Tarea Relacionada:** Compilación y Empaquetado Productivo (Joan Medina).
* **Módulo / Componente:** Vite 8.3.4 | TypeScript Compiler (`tsc -b`).
* **Funcionalidad Demostrada:** Generación limpia del bundle estático de producción en `dist/`.
* **Descripción Técnica:** Ejecución de `npm run build`. Compilación de tipos sin errores (`tsc -b`), transformación de 32 módulos en 100 ms y empaquetado optimizado (`index.js`: 414 kB / gzip: 113 kB; `index.css`: 0.43 kB).
* **Resultado Observado:** Artefacto listo para despliegue productivo; cero errores de tipos.
* **Criterio de Aceptación:** Cierre DoD de empaquetado de producción.
* **Diapositiva en la que se utiliza:** Diapositiva 11 (*Aseguramiento de Calidad y Cierre DoD*).

---

## 3. Catálogo de Diagramas Oficiales de Arquitectura y Diseño

| Código Diagrama | Archivo PNG | Fuente Oficial PlantUML | Vista 4+1 / Tipo | Funcionalidad Modelada | Diapositiva Asociada |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **DIA-S04-01** | `diagramas/arquitectura_sprint04.png` | `INFORME_GENERAL_SPRINT_04.md#L100` | Física / Despliegue | Arquitectura desacoplada multi-capa: React 19 SPA (:5173), FastAPI REST (:8000) y Supabase PostgreSQL con RLS y Alembic 004. | Diapositiva 02 y Diapositiva 07 |
| **DIA-S04-02** | `diagramas/flujo_recomendacion.png` | `diagramas_general.md#L1250` | Lógica / Pipeline | Pipeline algorítmico *EdRecSys v1.0*: Filtro de mérito RN-03, 4 factores de afinidad, multiplicador 1.30x y desempate determinista. | Diapositiva 04 y Diapositiva 05 |
| **DIA-S04-03** | `diagramas/flujo_reserva.png` | `INFORME_GENERAL_SPRINT_04.md#L320` | Procesos / Secuencia | Secuencia técnica entre capas para la reserva transaccional atómica con validación de estados y corte $T-24\text{ h}$. | Diapositiva 07 y Diapositiva 10 |
| **DIA-S04-04** | `diagramas/concurrencia_aforo.png` | Diseño transaccional RNF07 | Procesos / Concurrencia | Escenario de contención de 20 hilos disputando la última vacante con candado pesimista `SELECT ... FOR UPDATE` (Tasa sobrecupo = 0.00%). | Diapositiva 08 |

---

## 4. Matriz Cruzada de Trazabilidad: Tarea vs. Código vs. Pruebas vs. Evidencias

| Tarea | Responsable | Componente de Software | Suite de Pruebas Asociada | Evidencia Gráfica Principal | Diapositiva Canva |
| :---: | :---: | :--- | :--- | :--- | :---: |
| **T-17** | Renzo | `app/services/recommendation_service.py` | `tests/test_recommendations.py` (ORD-01..05) | `evidencias/backend/01_recommendations_endpoint_response.png`<br>`evidencias/pruebas/01_topk_deterministic_ordering_tests.png` | Diapositiva 04, 05, 06 |
| **T-18** | Joan | `src/services/recommendationService.ts` | `src/services/__tests__/recommendationService.test.ts` | `evidencias/frontend/01_recommendation_feed_topk.png` | Diapositiva 04 |
| **T-19** | Ambos | Algoritmo y DOM de ordenamiento Top-k | `test_recommendations.py` + `TopKOrdering.test.tsx` | `evidencias/pruebas/01_topk_deterministic_ordering_tests.png`<br>`evidencias/frontend/03_topk_ordering_vitest.png` | Diapositiva 06 |
| **T-20** | Joan | `src/components/RecommendationFeedView.tsx` | `src/components/__tests__/RecommendationFeedView.test.tsx` | `evidencias/frontend/01_recommendation_feed_topk.png` | Diapositiva 04, 05 |
| **T-21** | Joan | `src/components/BookingModalView.tsx` | `src/components/__tests__/BookingModalView.test.tsx` | `evidencias/frontend/02_booking_modal_and_rules.png` | Diapositiva 07 |
| **T-22** | Renzo | `app/api/v1/endpoints/bookings.py`<br>`app/models/booking.py`<br>Migración 004 Alembic | `tests/test_bookings.py` (46 tests) | `evidencias/backend/02_swagger_api_docs_sprint04.png`<br>`evidencias/base_datos/01_migration_004_reservas_cupo.png` | Diapositiva 07, 09, 10 |
| **T-23** | Joan | `src/services/bookingService.ts`<br>`src/App.tsx` | `src/services/__tests__/bookingService.test.ts`<br>`src/__tests__/BookingIntegration.test.tsx` | `evidencias/frontend/02_booking_modal_and_rules.png` | Diapositiva 07 |
| **T-24** | Renzo | `app/services/booking_service.py`<br>(Bloqueo pesimista `FOR UPDATE`) | `tests/test_bookings.py` (Suite multihilo 20 hilos) | `evidencias/pruebas/03_concurrency_pessimistic_lock_rnf07.png`<br>`evidencias/base_datos/02_pessimistic_lock_query_select_for_update.png` | Diapositiva 08, 09 |

---

*Fin de la Matriz de Evidencias Técnicas — Sprint 04.*
