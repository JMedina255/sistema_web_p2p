# Bitácora de Especificación Técnica, Desarrollo y Cierre – Sprint 08: Integración Integral del Flujo Formativo, Generación de Constancias PDF de Demostración, Auditoría Algorítmica de Precision@k y Cierre del MVP

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna – Facultad de Ingeniería (EPIS)  
**Semestre Académico:** 2026-II  
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado  
**Equipo Consultor:** Grupo 03 / C-SharkTeam  
**Roles y Asignación de Responsabilidades:**
- **Joan Cristian (Carlos) Medina Quispe** — Responsable de Frontend, Accesibilidad y Experiencia de Usuario UI/UX (Código Estudiantil: 2022074255)
- **Renzo Antonio Antayhua Mamani** — Responsable de Backend, Persistencia Relacional, Algoritmos y Seguridad (Código Estudiantil: 2022073504)  
**Rama Base de Integración:** `main`  
**Commits Oficiales de Cierre e Incremento Sprint 8:** [`ca730f3`](https://github.com/JMedina255/sistema_web_p2p/commit/ca730f3) y [`f28c442`](https://github.com/JMedina255/sistema_web_p2p/commit/f28c442) (14/11/2026)  
**Fecha de Corte Documental:** 14/11/2026  
**Estructura de Commits del Incremento Sprint 8 (Regla D-8.3):**
- `feat(backend): implement PDF demo certificate generation engine with watermark [T-42]` [`b24d578`](https://github.com/JMedina255/sistema_web_p2p/commit/b24d578)
- `feat(frontend): develop certificate download interface and progress bar [T-43]` [`c35e689`](https://github.com/JMedina255/sistema_web_p2p/commit/c35e689)
- `feat(backend): register certificate issuance and demo serial tracking in database [T-44]` [`d46f790`](https://github.com/JMedina255/sistema_web_p2p/commit/d46f790)
- `test(benchmark): evaluate Precision@3 and Precision@5 ranking metrics with ground-truth testbench [T-45]` [`e57a801`](https://github.com/JMedina255/sistema_web_p2p/commit/e57a801)
- `docs(metrics): document Precision@k evaluation results and algorithmic boundary conditions [T-46]` [`f68b912`](https://github.com/JMedina255/sistema_web_p2p/commit/f68b912)
- `feat(ui): integrate end-to-end user navigation flow and role-based guards in React App Shell [T-47]` [`cff8d40`](https://github.com/JMedina255/sistema_web_p2p/commit/cff8d40)
- `test(e2e): execute end-to-end integration test suites across mentee, mentor and admin roles [T-48]` [`4cbf504`](https://github.com/JMedina255/sistema_web_p2p/commit/4cbf504)
- `test(exploratory): perform WCAG 2.1 AA accessibility and cross-browser exploratory tests [T-49]` [`a1d198d`](https://github.com/JMedina255/sistema_web_p2p/commit/a1d198d)
- `chore(demo): configure reproducible demo environment and seed data fixtures [T-50]` [`bb9ce3c`](https://github.com/JMedina255/sistema_web_p2p/commit/bb9ce3c)
- `docs(closure): consolidate final MVP technical documentation and project closure audit [T-51]` [`ca730f3`](https://github.com/JMedina255/sistema_web_p2p/commit/ca730f3)

> [!NOTE]
> **Estado Técnico de Cierre del Sprint 8 y Culminación del Proyecto (14/11/2026):**  
> El presente documento constituye la **Bitácora de Especificación Técnica, Desarrollo y Cierre del Sprint 8**, así como el informe de culminación formal del ciclo de desarrollo ágil del Sistema Web P2P de Mentorías Académicas de la EPIS-UPT, elaborado conforme a las directrices de ingeniería **D-1 a D-10** de [`reglas_documentacion_diseño.md`](../../reglas_documentacion_diseño.md) y [`PLAN_SPRINTS_Y_TAREAS.md`](PLAN_SPRINTS_Y_TAREAS.md) (Tabla 5.9 / Cuadro 4.8).  
> La plataforma web concluye el ciclo de ocho sprints con el **100% de tareas completadas e integradas** (51 tareas oficiales culminadas de 51 planificadas, 91.0 horas-persona académicas invertidas con riguroso balance entre integrantes: 45.0 h Joan Medina y 46.0 h Renzo Antayhua).  
> El repositorio alcanza un banco automatizado definitivo de **556 pruebas de software aprobadas** (311 en frontend con Vitest distribuidas en 29 suites y 245 en backend con Pytest distribuidas en 19 suites, 0 defectos, 0 errores de linteo en ESLint/Ruff, coberturas de 83.50% en frontend y 85.0% en backend que superan holgadamente la meta del 70.0% de **RNF09**, y flujo de GitHub Actions aprobado con éxito).  
> Se formaliza la emisión de constancias digitales en formato PDF marcadas **DEMO** con código QR de verificación y firma criptográfica SHA-256 (**T-42 / T-43 / T-44** bajo **RF22 / RF23 / RN-14**), la evaluación empírica de relevancia algorítmica alcanzando $\text{Precision@3} = 83.3\%$ y $\text{Precision@5} = 80.0\%$ con latencia promedio de $12.4\text{ ms}$ (**T-45 / T-46** bajo **RF06 / RNF03**), el cierre de navegación integral sin fricciones de los cuatro roles institucionales (**T-47 / T-48 / T-49**), y el entorno reproducible con fixtures de demostración académica (**T-50 / T-51**).

---

## 1. Visión General, Alcance, Historias de Usuario y Ceremonias Scrum del Sprint 8

### 1.1. Propósito y Valor del Incremento

El **Sprint 8** representa el hito culminante del proyecto, unificando los incrementos de los siete sprints precedentes en un Producto Mínimo Viable (MVP) completamente navegable, demostrable y auditable para la cátedra de Construcción de Software I:

1. **Emisión y Descarga de Constancias PDF de Demostración (**PB-024** / **RF22** / **RF23** / **CUS13** / **CUS18** / **RN-14**):**  
   Implementa el motor de compilación binaria de documentos oficiales en PDF para el reconocimiento de la labor del estudiante mentor. El sistema evalúa en base de datos la suma de horas dictadas con bitácora aprobada por la administración (`visado_administrador = true`). Si el mentor alcanza o supera el umbral semestral parametrizado (20 horas efectivas según **RN-14**), la plataforma genera una constancia institucional formal con folio correlativo (`CERT-2026-II-XXXX`), sello criptográfico SHA-256, código QR de verificación institucional y la marca de agua obligatoria `"DEMO - FINES ACADÉMICOS"`.
2. **Auditoría Algorítmica y Evaluación de Precision@k (**PB-027** / **RF06** / **RNF03**):**  
   Ejecuta el banco de pruebas empírico (Testbench) sobre el algoritmo de recomendación híbrido (*EdRecSys*), midiendo la exactitud del ranking en espacios vectoriales silábicos con cohortes sintéticas etiquetadas con juicios de relevancia ground-truth. Certifica formalmente el cumplimiento de las métricas institucionales: $\text{Precision@3} \ge 0.80$ y $\text{Precision@5} \ge 0.75$, con un tiempo medio de inferencia menor a 15 ms, superando la restricción de latencia máxima de 1500 ms estipulada en **RNF03**.
3. **Integración Integral del Recorrido Formativo y Pruebas E2E Multirol (**PB-037** / **RNF06** / **RNF09** / **RNF10**):**  
   Consolida la arquitectura de navegación en el Shell Institucional de React, articulando fluidamente las vistas protegidas por rol (RBAC: Visitante $\rightarrow$ Mentoreado $\rightarrow$ Mentor $\rightarrow$ Administrador). Garantiza el recorrido completo de demostración: Acceso OTP $\rightarrow$ Consentimiento informado Ley 29733 $\rightarrow$ Catálogo curricular silábico $\rightarrow$ Perfiles y disponibilidad semanal 6×11 $\rightarrow$ Publicación de oferta $\rightarrow$ Cartelera Top-k $\rightarrow$ Reserva transaccional $\rightarrow$ Ratificación a $T-24\text{ h}$ $\rightarrow$ Evaluación automática de quórum $\rightarrow$ Pase de asistencia QR TOTP $\rightarrow$ Bitácora pedagógica con hash SHA-256 $\rightarrow$ Encuesta de calidad $\rightarrow$ Visado de horas $\rightarrow$ Descarga de constancia DEMO.

---

### 1.2. Historias de Usuario del Sprint 8

A continuación, se formalizan las historias de usuario oficiales correspondientes a los PBI del incremento final, junto a sus criterios de aceptación en sintaxis Given-When-Then (Gherkin):

#### HU-08.1: Emisión y Descarga de Constancia Oficial de Mentoría DEMO (PB-024)
- **Historia de Usuario:**  
  *Como* estudiante mentor con horas formativas debidamente visadas por Dirección,  
  *quiero* consultar mi progreso hacia el umbral de 20 horas y descargar mi constancia oficial en formato PDF vectorial con membrete, código QR, marca de agua DEMO y hash SHA-256,  
  *para que* pueda certificar curricularmente mi labor de acompañamiento académico universitario ante las autoridades de la EPIS-UPT.
- **Trazabilidad:** PB-024, RF22, RF23, CUS13, CUS18, RN-14, RNF02, RNF05.
- **Criterios de Aceptación (Gherkin):**
  - **Escenario 1 (Emisión Exitosa con $\ge 20.0$ Horas Visadas):**  
    *Dado* un mentor que acumula 20.0 o más horas en sesiones con `visado_administrador = true`,  
    *cuando* accede a `CertificateDownloadView.tsx` y acciona el botón "Emitir Constancia Oficial",  
    *entonces* el servidor genera el archivo PDF vectorial con folio correlativo único (`CERT-2026-II-XXXX`), inserta el registro en `certificados_horas`, estampa la marca de agua diagonal `"DEMO - FINES ACADÉMICOS"` y habilita la descarga inmediata del archivo binario.
  - **Escenario 2 (Bloqueo Estricto por Horas Acreditadas Insuficientes RN-14):**  
    *Dado* un mentor con menos de 20.0 horas visadas (ej. 16.0 horas acumuladas),  
    *cuando* consulta su panel de certificación,  
    *entonces* la barra de progreso refleja 80%, el botón de emisión permanece bloqueado exhibiendo el mensaje pedagógico "Te faltan 4.0 horas visadas para solicitar tu constancia oficial" y la invocación directa a la API retorna HTTP 400 Bad Request (`INSUFFICIENT_ACCREDITED_HOURS`).
  - **Escenario 3 (Verificación Forense mediante Código QR y Hash SHA-256):**  
    *Dado* un certificado generado y descargado,  
    *cuando* se escanea el código QR vectorial o se audita el hash criptográfico consignado al pie,  
    *entonces* el sistema redirige al validador institucional resolviendo los datos de expedición, folio, horas y periodo académico.

#### HU-08.2: Auditoría Algorítmica y Certificación de Precision@k (PB-027)
- **Historia de Usuario:**  
  *Como* equipo de ingeniería y docente de cátedra,  
  *quiero* ejecutar un testbench cuantitativo sobre el algoritmo híbrido *EdRecSys* utilizando cohortes sintéticas etiquetadas con juicios ground-truth,  
  *para que* se verifique empíricamente que la precisión en el Top-3 supera el 80% y en el Top-5 supera el 75% con tiempos de respuesta menores a 15 ms.
- **Trazabilidad:** PB-027, RF06, RNF03, RNF09.
- **Criterios de Aceptación (Gherkin):**
  - **Escenario 1 (Superación de Umbrales de Precisión Algorítmica):**  
    *Dado* el conjunto de datos de prueba representativo de 4 estudiantes mentoreados y 10 candidatos a mentor con matriz curricular silábica oficial,  
    *cuando* se ejecuta la suite de simulación `test_simulation.py`,  
    *entonces* el testbench reporta $\text{Precision@3} \ge 0.80$ y $\text{Precision@5} \ge 0.75$, certificando que los candidatos recomendados coinciden con los mentores idóneos según la cátedra.
  - **Escenario 2 (Latencia Sub-15ms e Invarianza Determinista RNF03):**  
    *Dado* el motor *EdRecSys* evaluado en 5 corridas consecutivas con permutación aleatoria en la lista de ofertas de entrada,  
    *cuando* se computa el tiempo medio de respuesta y el orden resultante,  
    *entonces* la latencia por inferencia no excede los 50 ms (registrando $12.4\text{ ms}$) y el ranking es 100% determinista e idéntico en todas las ejecuciones.

#### HU-08.3: Recorrido E2E del Shell Institucional y Cierre del MVP (PB-037)
- **Historia de Usuario:**  
  *Como* usuario en cualquiera de los cuatro roles institucionales (Visitante, Mentoreado, Mentor, Administrador),  
  *quiero* interactuar en un Shell Institucional unificado con sincronización de parámetros URL y guardas de seguridad RBAC,  
  *para que* sea posible recorrer el ciclo de vida completo de mentorías académicas de forma accesible y sin fricciones durante la defensa del proyecto.
- **Trazabilidad:** PB-037, RNF04, RNF05, RNF06, RNF08, RNF09, RNF10.
- **Criterios de Aceptación (Gherkin):**
  - **Escenario 1 (Navegación Fluida con Sincronización URL `?tab=`):**  
    *Dado* un usuario autenticado que navega entre las diferentes funcionalidades del sistema,  
    *cuando* selecciona una pestaña o utiliza los botones Atrás/Adelante del navegador,  
    *entonces* la vista se actualiza reactivamente conservando el parámetro de ruta en la URL sin provocar recargas completas de la página (`popstate`).
  - **Escenario 2 (Guardas de Acceso por Rol RBAC):**  
    *Dado* un estudiante con rol exclusivo de mentoreado que intenta acceder manualmente a `?tab=admin`,  
    *cuando* el componente `ProtectedView` evalúa los privilegios del token JWT,  
    *entonces* el sistema bloquea el renderizado de la bandeja administrativa, redirige al feed de recomendaciones y emite un mensaje formativo de acceso denegado.
  - **Escenario 3 (Puesta en Marcha Reproducible con Comando Único RNF10):**  
    *Dado* un evaluador o docente que clona el repositorio desde cero,  
    *cuando* ejecuta el aprovisionamiento de fixtures mediante `seed_demo_data.py`,  
    *entonces* el entorno crea automáticamente los usuarios base, asignaturas, ofertas y sesiones en distintos estados formativos para la demostración en vivo.

---

### 1.3. Matriz de Tareas y Planificación Técnica del Sprint 8

A continuación, se detalla la matriz de tareas del Sprint 8 conforme a [`PLAN_SPRINTS_Y_TAREAS.md`](PLAN_SPRINTS_Y_TAREAS.md) (Cuadro 4.8):

### Cuadro 1.1: Matriz de Tareas y Planificación Técnica del Sprint 8

| ID | Actividad Oficial | Responsable | Esfuerzo Planificado (h) | Estado de Entrega | Entregable y Criterio Verificable |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **T-42** | Implementar generación de constancias PDF de demostración. | Renzo Antayhua | 2.0 h | **100% Concluido** ✅ | Servicio `certificate_service.py`, compilación de PDF vectorial con membrete EPIS-UPT, marca de agua diagonal `"DEMO - FINES ACADÉMICOS"`, QR y firma SHA-256. |
| **T-43** | Desarrollar interfaz de descarga de constancias. | Joan Medina | 1.0 h | **100% Concluido** ✅ | Componente `CertificateDownloadView.tsx`, barra de progreso porcentual hacia las 20h (RN-14), botón accesible de descarga y visor PDF integrado. |
| **T-44** | Registrar constancias y folios de prueba. | Renzo Antayhua | 1.0 h | **100% Concluido** ✅ | Tabla relacional `certificados_horas`, control de unicidad de folio semestral, auditoría de descargas y estado `EMITIDO_DEMO`. |
| **T-45** | Evaluar Precision@3 y Precision@5 con datos etiquetados. | Renzo Antayhua | 2.0 h | **100% Concluido** ✅ | Script y suite de testbench algorítmico `test_simulation.py`, evaluación de 4 cohortes sintéticas representativas, reporte cuantitativo P@3 y P@5. |
| **T-46** | Documentar resultados y limitaciones de Precision@k. | Joan Medina | 1.0 h | **100% Concluido** ✅ | Informe analítico integrado en bitácora, análisis de sensibilidad frente a empates conceptuales, ponderación de materias críticas y limitaciones heurísticas. |
| **T-47** | Integrar navegación del flujo completo en React. | Joan Medina | 2.0 h | **100% Concluido** ✅ | Shell institucional `App.tsx` y `AppLayout.tsx`, sincronización reactiva de URL (`?tab=`), guardas de ruta por rol (RBAC) y navegación fluida sin recargas. |
| **T-48** | Ejecutar pruebas integrales por rol. | Renzo Antayhua | 2.0 h | **100% Concluido** ✅ | Suite de pruebas de integración E2E en Pytest (`test_e2e_lifecycle.py`), validación de aislamiento de roles y transiciones de estado de inicio a fin. |
| **T-49** | Realizar pruebas exploratorias de interfaz. | Joan Medina | 1.0 h | **100% Concluido** ✅ | Auditoría de accesibilidad WCAG 2.1 AA (contraste $\ge 4.5:1$, foco visible, lectores de pantalla) y comprobación responsiva en Chromium, Firefox y Safari. |
| **T-50** | Preparar entorno y datos reproducibles de demostración. | Joan Medina | 2.0 h | **100% Concluido** ✅ | Fixtures `seed_demo_data.py`, cuentas preconfiguradas con perfiles y sesiones en distintos estados formativos para demostración docente sin fricción. |
| **T-51** | Consolidar documentación y evidencias finales. | Ambos | 1.0 h (0.5/0.5) | **100% Concluido** ✅ | Auditoría final de directrices D-1 a D-10, actualización de bitácoras, verificación de cobertura global $\ge 70\%$ y cierre formal de rama `main`. |

Fuente: Elaboración propia a partir de `docs/sprints/PLAN_SPRINTS_Y_TAREAS.md` (Tabla 5.9 / Cuadro 4.8).

El Cuadro 1.1 confirma que las 15.0 horas académicas presupuestadas para la iteración final (7.5 h para Joan Medina y 7.5 h para Renzo Antayhua) fueron completadas al 100%, culminando la totalidad de compromisos de la planificación operativa del proyecto.

---

### 1.4. Imputación Detallada de Horas Académicas por Desarrollador

A continuación, se presenta la imputación horaria formal por cada desarrollador del Grupo 03, verificando el equilibrio estricto de carga técnica:

### Cuadro 1.2: Imputación de Horas Académicas por Desarrollador y Tarea (Sprint 8 y Cierre Global)

| Tarea / Actividad | Integrante Responsable | Rol Principal | Horas Planificadas | Horas Reales Invertidas | Desviación | Entregable Verificado |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **T-43** | Joan Cristian Medina | Frontend Developer | 1.0 h | 1.0 h | 0.0 h | `CertificateDownloadView.tsx` y barra 20h |
| **T-46** | Joan Cristian Medina | Frontend Developer | 1.0 h | 1.0 h | 0.0 h | Reporte analítico Precision@k y límites |
| **T-47** | Joan Cristian Medina | Frontend Developer | 2.0 h | 2.0 h | 0.0 h | Shell React, URL `?tab=` y guardas RBAC |
| **T-49** | Joan Cristian Medina | Frontend Developer | 1.0 h | 1.0 h | 0.0 h | Auditoría WCAG 2.1 AA y cross-browser |
| **T-50** | Joan Cristian Medina | Frontend Developer | 2.0 h | 2.0 h | 0.0 h | Fixtures demo `seed_demo_data.py` |
| **T-51 (FE)** | Joan Cristian Medina | Frontend Developer | 0.5 h | 0.5 h | 0.0 h | Consolidación de bitácoras y cierre |
| **T-42** | Renzo Antonio Antayhua | Backend Developer | 2.0 h | 2.0 h | 0.0 h | Compilador PDF DEMO con QR y SHA-256 |
| **T-44** | Renzo Antonio Antayhua | Backend Developer | 1.0 h | 1.0 h | 0.0 h | Tabla `certificados_horas` y folios |
| **T-45** | Renzo Antonio Antayhua | Backend Developer | 2.0 h | 2.0 h | 0.0 h | Testbench P@3 (83.3%) y P@5 (80.0%) |
| **T-48** | Renzo Antonio Antayhua | Backend Developer | 2.0 h | 2.0 h | 0.0 h | Suites E2E multirol `test_e2e_lifecycle.py` |
| **T-51 (BE)** | Renzo Antonio Antayhua | Backend Developer | 0.5 h | 0.5 h | 0.0 h | Auditoría D-1 a D-10 y verificación CI |
| **Ceremonias Scrum** | Joan Medina / Renzo Antayhua | Equipo Ágil | (Transversal) | Sincronizado | 0.0 h | 5 Dailies, Planning, Review, Retro |
| **Subtotal Joan S8**| **Joan Medina (Frontend)** | **Frontend / UI-UX** | **7.5 h** | **7.5 h** | **0.0 h** | **100% Concluido en Sprint 8** |
| **Subtotal Renzo S8**| **Renzo Antayhua (Backend)**| **Backend / DB-Sec** | **7.5 h** | **7.5 h** | **0.0 h** | **100% Concluido en Sprint 8** |
| **Total Sprint 8** | **Grupo 03 / C-SharkTeam** | **Equipo de Desarrollo** | **15.0 h** | **15.0 h** | **0.0 h** | **100% Cumplido** |
| **Gran Total S1–S8**| **Joan Medina (45.0h) / Renzo Antayhua (46.0h)** | **Proyecto P2P** | **91.0 h** | **91.0 h** | **0.0 h** | **Meta Institucional Culminada** |

Fuente: Elaboración propia a partir de las bitácoras de trabajo y `PLAN_SPRINTS_Y_TAREAS.md` (Cuadros 2.1 y 5.9).

El Cuadro 1.2 acredita el estricto cumplimiento de la capacidad neta planificada de 91.0 horas académicas distribuidas a lo largo de los 8 sprints (45.0 h para Joan Medina y 46.0 h para Renzo Antayhua), habiéndose alcanzado el 100% de los compromisos sin sobrecosto temporal ni tareas desatendidas.

---

### 1.5. Ceremonias Scrum del Sprint 8

Durante la iteración final se llevaron a cabo las cuatro ceremonias Scrum que estructuraron el cierre del proyecto:

1. **Sprint Planning (09/11/2026, 08:00 – 09:00):**  
   - *Participantes:* Joan Medina y Renzo Antayhua.  
   - *Sprint Goal:* *"Consolidar el MVP navegable de extremo a extremo, emitir constancias PDF de demostración con sello criptográfico y certificar el rendimiento del recomendador Top-k ante la cátedra"*.  
   - *Acuerdos:* Se asignaron las 10 tareas finales (T-42 a T-51), fijando el 13/11 como fecha de congelamiento de código (*code freeze*) y el 14/11 para la entrega documental final.
2. **Daily Scrums (Sincronizaciones Diarias de la Semana de Cierre):**  
   - *Daily Scrum Día 1 (09/11/2026):* Renzo avanzó con el compilador PDF vectorial en `certificate_service.py` con marca de agua diagonal; Joan diseñó la barra de avance hacia 20h en `CertificateDownloadView.tsx`.  
   - *Daily Scrum Día 2 (10/11/2026):* Renzo implementó el testbench algorítmico `test_simulation.py` para medir Precision@3 y Precision@5; Joan documentó los hallazgos analíticos sobre desempates por reputación.  
   - *Daily Scrum Día 3 (11/11/2026):* Joan unificó la navegación en el Shell Institucional `App.tsx` sincronizando `?tab=`; Renzo elaboró las pruebas de integración de ciclo de vida completo (`test_e2e_lifecycle.py`).  
   - *Daily Scrum Día 4 (12/11/2026):* Joan auditó la accesibilidad WCAG 2.1 AA en todas las vistas; Renzo verificó la persistencia de folios institucionales únicos (`CERT-2026-II-XXXX`).  
   - *Daily Scrum Día 5 (13/11/2026):* Se aprovisionaron los fixtures reproducibles `seed_demo_data.py` y se ejecutaron las suites consolidadas de frontend (311 tests) y backend (245 tests), logrando 0 defectos.
3. **Sprint Review (13/11/2026, 16:00 – 17:30):**  
   - *Demostración Integral:* Recorrido sin interrupciones del ciclo formativo completo: Acceso OTP $\rightarrow$ Consentimiento informado $\rightarrow$ Catálogo curricular $\rightarrow$ Disponibilidad 6×11 $\rightarrow$ Oferta $\rightarrow$ Feed Top-k $\rightarrow$ Reserva $\rightarrow$ Ratificación T-24h $\rightarrow$ Quórum $\rightarrow$ Asistencia QR TOTP $\rightarrow$ Bitácora SHA-256 $\rightarrow$ Encuesta $\rightarrow$ Visado $\rightarrow$ Emisión y descarga de constancia PDF DEMO.  
   - *Resultado:* Aprobación unánime del incremento por parte de los interesados académicos.
4. **Sprint Retrospective Final del Proyecto (14/11/2026, 10:00 – 11:30):**  
   - *Dinámica KPT Global del Ciclo de 8 Sprints:*  
     - **Keep (Prácticas de Excelencia):** Tipado estricto bidireccional (Pydantic v2 y TypeScript), cobertura continua superior al 80% (RNF09), y documentación con directrices D-1 a D-10.  
     - **Problem (Dificultades Superadas):** Concurrencia en aforos bajo disputas simultáneas (resuelta con `SELECT ... FOR UPDATE` en Sprint 4) y complejidad de pruebas temporales (resuelta con `freezegun`).  
     - **Try (Recomendaciones Futuras):** Contenerizar el stack completo mediante Docker Compose para despliegue en la infraestructura física de servidores de la EPIS-UPT.

---

## 2. Registro y Especificación de Frontend (Joan Medina)

---

### 2.1. T-43 – Interfaz de Descarga de Constancias Oficiales de Demostración (`CertificateDownloadView.tsx`)

- **Responsable:** Joan Cristian (Carlos) Medina Quispe.
- **Esfuerzo Planificado:** 1.0 hora.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-024, RF22, RF23, CUS18, RN-14, RNF05.

#### A. Especificaciones de la Vista de Certificación del Mentor
El componente [`CertificateDownloadView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/CertificateDownloadView.tsx) implementa el módulo de acreditación del estudiante mentor:

1. **Barra de Progreso Formativo hacia el Umbral Reglamentario (RN-14):**
   - Consulta `certificateService.getHoursSummary({ mentorEmail })`.
   - Despliega una barra de progreso institucional que contrasta las *Horas Acreditadas Visadas* frente a la meta reglamentaria de 20.0 horas semestrales (ej. `16.0 / 20.0 horas (80%)`).
   - Diferencia visualmente las horas acreditadas (visadas por la Escuela) de las horas en revisión provisional, educando al mentor sobre el proceso de fiscalización.
2. **Habilitación Condicional de Emisión:**
   - Si $\text{horas\_visadas} < 20.0$, el botón de emisión se mantiene bloqueado, exhibiendo una alerta formativa en color ámbar: *"Te faltan {20 - n} horas visadas para solicitar tu constancia oficial de mentoría"*.
   - Si $\text{horas\_visadas} \ge 20.0$, el botón *"Emitir Constancia Oficial"* se ilumina en color azul institucional (`#1C2A59`).
3. **Descarga Segura y Visualización In-Situ:**
   - Al accionar la emisión, despacha `POST /api/v1/certificates/generate`. La respuesta entrega el identificador y el blob binario del PDF.
   - Provee previsualización modal del documento y botón de descarga directa con nombre estandarizado `Constancia_Mentoria_EPIS_2026_II_{folio}.pdf`.

---

### 2.2. T-46 – Análisis Analítico de Rendimiento y Limitaciones de Precision@k

- **Responsable:** Joan Cristian Medina Quispe.
- **Esfuerzo Planificado:** 1.0 hora.
- **Estado Técnico:** **IMPLEMENTADO Y DOCUMENTADO ✅**.
- **Trazabilidad:** PB-027, RF06, RNF03.

#### A. Evaluación Crítica del Algoritmo de Recomendación
Se consolidan los hallazgos analíticos sobre el comportamiento del motor híbrido (*EdRecSys*):
- **Exactitud Lograda:** La evaluación con cohortes sintéticas demostró una precisión media de $\text{Precision@3} = 83.33\%$ y $\text{Precision@5} = 80.00\%$, superando los umbrales de referencia fijados en el plan.
- **Tratamiento de Empates (RN-11):** La regla de desempate jerárquico (reputación docente $\rightarrow$ menor carga de sesiones activas $\rightarrow$ condición de mentoría prioritaria) resolvió satisfactoriamente los casos de idéntica similitud coseno entre candidatos, garantizando un ordenamiento 100% determinista e invariable ante permutaciones en la entrada (verificado en 5 ejecuciones consecutivas con semilla controlada).
- **Limitaciones Identificadas:**
  1. *Dependencia del Padrón de Disponibilidad:* Si un estudiante y un mentor coinciden en temarios silábicos pero poseen matrices horarias completamente disjuntas (0 franjas de solapamiento), el score decae drásticamente debido a la penalización de agenda.
  2. *Cold-Start de Nuevos Mentores:* Mentores de reciente admisión sin calificaciones previas parten con reputación neutral (3.0/5.0), ubicándose por debajo de mentores consolidados ante empates temáticos.

---

### 2.3. T-47 – Integración de Navegación del Flujo Completo en React (`App.tsx` y `AppLayout.tsx`)

- **Responsable:** Joan Cristian Medina Quispe.
- **Esfuerzo Planificado:** 2.0 horas.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-037, RNF04, RNF05, RNF08.

#### A. Arquitectura del Shell Institucional y Control de Acceso RBAC
El componente central [`App.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/App.tsx) articula la experiencia de usuario:
1. **Sincronización Bidireccional de URL:** Cada cambio de pestaña actualiza el parámetro de búsqueda en el navegador (`?tab=recommendations`, `?tab=bookings`, `?tab=admin`, etc.) sin refrescar la página, permitiendo el uso fluido de los botones Atrás/Adelante del navegador (`popstate`).
2. **Guardas de Navegación por Rol (`ProtectedView.tsx`):** Bloquea de manera proactiva cualquier intento de renderizar interfaces fuera del rol activo. Si un mentoreado intenta acceder a `?tab=admin`, la guarda redirige a su pestaña predeterminada y emite un mensaje pedagógico.
3. **Conmutador Dinámico de Rol:** Para aquellos usuarios que poseen múltiples roles acreditados (ej. estudiante que es mentor y mentoreado simultáneamente), la barra superior permite alternar el contexto de trabajo con un solo clic, reconfigurando reactivamente los menús y permisos de visualización.

---

### 2.4. T-49 – Auditoría de Accesibilidad WCAG 2.1 AA y Pruebas Exploratorias

- **Responsable:** Joan Cristian Medina Quispe.
- **Esfuerzo Planificado:** 1.0 hora.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-037, RNF05, RNF08.

#### A. Resultados de la Verificación de Accesibilidad y Compatibilidad
- **Contraste Cromático:** Todos los elementos textuales cumplen con el ratio de contraste mínimo de $4.5:1$ sobre sus fondos según la paleta institucional (Azul Marino `#1C2A59` sobre blanco con ratio $11.2:1$; gris pizarra `#64748B` con ratio $4.6:1$).
- **Navegabilidad por Teclado:** Todas las acciones interactivas (apertura de modales, selección de estrellas, pestañas y botones de descarga) son plenamente operables mediante la tecla `Tab`, flechas direccionales y `Enter`/`Space`. Los modales implementan cerrojo de foco (`focus trap`) y soporte para tecla `Escape`.
- **Compatibilidad Multiplataforma:** Comprobado satisfactoriamente en Google Chrome (Chromium v120+), Mozilla Firefox (Gecko v121+) y Microsoft Edge.

---

### 2.5. T-50 – Entorno y Fixtures Reproducibles de Demostración (`seed_demo_data.py`)

- **Responsable:** Joan Cristian Medina Quispe.
- **Esfuerzo Planificado:** 2.0 horas.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-037, RNF09, RNF10.

#### A. Cuentas y Escenarios de Prueba Institucional
El script de inicialización aprovisiona cuentas representativas listas para el recorrido de defensa académica:
- `mentoreado@upt.pe`: Estudiante de II ciclo con perfil formativo configurado, asignaturas críticas registradas (Cálculo I, Algoritmos) y reservas en estados pendientes y ratificados.
- `mentor@upt.pe`: Estudiante de VIII ciclo acreditado, con ofertas publicadas, sesiones con quórum suficiente e insuficiente, y 22 horas acumuladas con bitácoras visadas listo para emitir constancia.
- `admin@upt.pe`: Cuenta de Dirección de Escuela habilitada para gestión de roles, auditoría de bitácoras y conmutación de horas formativas.

---

## 3. Catálogo de Pruebas y Evidencias de Frontend (Joan Medina)

### Cuadro 3.1: Matriz de Trazabilidad de Pruebas Automatizadas de Frontend (Sprint 8)

| Archivo de Prueba | Caso de Prueba Automatizado | Criterio de Aceptación Verificado | Aserción y Mock Técnico | Cobertura | Estado |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `CertificateDownloadView.test.tsx` | Barra de progreso formativo (RN-14) | Despliega correctamente el avance de horas y bloquea si horas < 20. | `expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '16')`; botón disabled. | 92.5% | ✅ PASS |
| `CertificateDownloadView.test.tsx` | Habilitación y descarga de PDF | Habilita botón al alcanzar 20h y dispara la descarga del blob binario. | `fireEvent.click(downloadBtn)` $\rightarrow$ invoca `certificateService.downloadPdf` retornando 200. | 94.1% | ✅ PASS |
| `App.test.tsx` | Enrutamiento RBAC por parámetros URL | Conduce a la pestaña autorizada y redirige accesos indebidos de rol. | Simulación de URL `?tab=admin` con rol mentoreado $\rightarrow$ redirige a `recommendations`. | 88.0% | ✅ PASS |
| `App.test.tsx` | Conmutador de roles en tiempo real | Alterna contexto entre mentoreado y mentor actualizando el menú dinámico. | `fireEvent.click(switchRoleBtn)` $\rightarrow$ menú despliega pestañas de mentor. | 90.3% | ✅ PASS |
| `AppLayout.test.tsx` | Accesibilidad y foco modal (WCAG 2.1 AA) | Verifica foco atrapado en diálogos y respuesta a tecla Escape. | `fireEvent.keyDown(modal, { key: 'Escape' })` $\rightarrow$ modal cerrado y foco devuelto. | 91.8% | ✅ PASS |

Fuente: Reporte de ejecución de Vitest en `aplicacion/frontend/` (Rama `main`, 14/11/2026).

---

## 4. Registro y Especificación de Backend, Persistencia y Seguridad (Renzo Antayhua)

---

### 4.1. T-42 – Motor de Generación de Constancias PDF de Demostración (`certificate_service.py`)

- **Responsable:** Renzo Antonio Antayhua Mamani.
- **Esfuerzo Planificado:** 2.0 horas.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-024, RF22, RF23, CUS18, RN-14, RNF02.

#### A. Especificaciones de Diseño del Documento PDF y Elementos de Seguridad
El servicio backend [`certificate_service.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/certificate_service.py) genera documentos PDF vectoriales estructurados con las siguientes capas de seguridad:
1. **Membrete Oficial y Trazabilidad:** Incluye los logotipos vectoriales de la Universidad Privada de Tacna y la Escuela Profesional de Ingeniería de Sistemas (EPIS).
2. **Marca de Agua Diagonal de Demostración:** Proyecta en ángulo de $45^\circ$ en color gris claro semi-transparente el texto obligatorio:
   $$\text{"DEMO - FINES ACADÉMICOS"}$$
   garantizando que el documento no sea utilizado como certificación profesional fuera del marco del curso.
3. **Código QR Vectorial de Verificación Institucional:** Inserta en la esquina inferior izquierda un código QR de alta resolución que codifica la URL institucional de validación:
   `https://epis.upt.edu.pe/p2p/certificados/verificar?folio=CERT-2026-II-XXXX`
4. **Sello Criptográfico SHA-256:** Calcula el hash criptográfico inmutable sobre la concatenación canónica del mentor, total de horas, fecha de emisión y folio:
   $$\text{Hash} = \text{SHA-256}(\text{mentor\_email} \parallel \text{horas} \parallel \text{folio} \parallel \text{emision\_timestamp})$$
   consignado al pie del documento para auditorías forenses de autenticidad.

---

### 4.2. T-44 – Persistencia y Registro de Constancias (`certificados_horas`)

- **Responsable:** Renzo Antonio Antayhua Mamani.
- **Esfuerzo Planificado:** 1.0 hora.
- **Estado Técnico:** **IMPLEMENTADO Y VERIFICADO ✅**.
- **Trazabilidad:** PB-024, RF22, RF23, RN-14, RNF02, RNF07.

#### A. Diccionario de Datos Físico — Entidad `certificados_horas` (Regla D-4)

### Cuadro 4.1: Diccionario Físico de Datos — Tabla `certificados_horas` (D-4)

| Columna | Tipo PostgreSQL | Restricciones | Clave Foránea (FK) | Descripción Funcional y Reglas |
| :--- | :--- | :--- | :--- | :--- |
| `id_certificado` | `SERIAL` | `PRIMARY KEY`, `NOT NULL` | — | Identificador correlativo del certificado emitido. |
| `id_mentor` | `VARCHAR(255)` | `NOT NULL`, `INDEX` | `usuarios(email) ON DELETE RESTRICT` | Correo institucional del mentor acreditado. |
| `codigo_folio` | `VARCHAR(50)` | `NOT NULL`, `UNIQUE` | — | Folio institucional único con formato `CERT-YYYY-SEM-XXXX`. |
| `periodo_academico`| `VARCHAR(20)` | `NOT NULL` | — | Semestre lectivo de la mentoría (ej. `2026-II`). |
| `horas_acreditadas`| `FLOAT` | `NOT NULL`, `CHECK (>= 20.0)` | — | Total de horas visadas acumuladas (mínimo 20h según RN-14). |
| `hash_firma` | `VARCHAR(64)` | `NOT NULL` | — | Huella criptográfica SHA-256 de autenticidad. |
| `estado` | `VARCHAR(30)` | `NOT NULL`, `DEFAULT 'EMITIDO_DEMO'`| — | Estado institucional del documento emitido. |
| `created_at` | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()` | — | Fecha y hora exacta de expedición en el servidor. |

Fuente: Elaboración propia conforme a la Regla D-4.

*Restricciones Adicionales:*
- `CONSTRAINT uq_mentor_periodo_certificado UNIQUE (id_mentor, periodo_academico)` (Impide la doble emisión de certificados para un mismo mentor en el mismo ciclo).
- `CONSTRAINT chk_horas_minimas_cert CHECK (horas_acreditadas >= 20.0)`

---

### 4.3. T-45 – Banco de Pruebas Algorítmico y Evaluación de Precision@k (`SimulationService`)

- **Responsable:** Renzo Antonio Antayhua Mamani.
- **Esfuerzo Planificado:** 2.0 horas.
- **Estado Técnico:** **IMPLEMENTADO Y AUDITADO ✅**.
- **Trazabilidad:** PB-027, RF06, RNF03.

#### A. Metodología de Evaluación y Juicios de Relevancia Ground-Truth
El servicio [`simulation_service.py`](file:///d:/sistema_web_p2p/aplicacion/backend/app/services/simulation_service.py) evalúa cuantitativamente el motor *EdRecSys* comparando los rankings inferidos frente a una cohorte sintética de 4 estudiantes mentoreados (Ciclos I a IV) y 10 candidatos a mentor (Ciclos VII a X) previamente etiquetados con relevancia conceptual ground-truth.

Se evalúa la precisión en las posiciones $k=3$ y $k=5$ mediante la formulación canónica:
$$\text{Precision@k} = \frac{|\text{Recomendados en Top-}k \cap \text{Relevantes}|}{k}$$

#### B. Resultados Cuantitativos del Testbench Algorítmico
A continuación, se resumen los resultados obtenidos en el entorno de pruebas automatizado:

### Cuadro 4.2: Balance Métrico de Relevancia y Rendimiento de Recomendación (Testbench)

| Métrica Evaluada | Umbral Exigido (RNF03) | Resultado Observado | Estado Técnico |
| :--- | :---: | :---: | :---: |
| **Precision@3** (Top-3) | $\ge 0.70$ (70.0%) | **0.833 (83.3%)** | ✅ Superado |
| **Precision@5** (Top-5) | $\ge 0.65$ (65.0%) | **0.800 (80.0%)** | ✅ Superado |
| **Latencia Media por Inferencia** | $\le 1500.0\text{ ms}$ (1.5s) | **12.4 ms** ($12,410\text{ }\mu\text{s}$) | ✅ Óptimo (120x más rápido) |
| **Invarianza Determinista** | 100% idéntico en 5 runs | **100% Determinista** (0 variaciones) | ✅ Conforme |
| **Filtro de Mérito RN-03** | 0% fuga de ciclo < VII | **0.0% tasa de fuga** (100% filtrado) | ✅ Conforme |

Fuente: Ejecución del testbench automatizado en `aplicacion/backend/tests/test_simulation.py` (09/11/2026).

---

### 4.4. Especificación de Contratos de API REST (Regla D-3)

### Cuadro 4.3: Contratos de Endpoints REST del Sprint 8 (D-3)

| Método | Ruta Canónica Versionada | Parámetros / Payload | Respuesta de Éxito | Códigos de Error HTTP | Regla / Propósito |
| :---: | :--- | :--- | :--- | :---: | :--- |
| `POST` | `/api/v1/certificates/generate` | Header: `Authorization: Bearer <JWT>` | `201 Created`<br>`CertificateMetaResponse` | `400 Bad Request` (Horas $< 20.0$)<br>`401 Unauthorized`<br>`409 Conflict` (Ya emitido) | **RF22 / RN-14**.<br>Genera y persiste constancia PDF DEMO. |
| `GET` | `/api/v1/certificates/{id}/download` | Path: `id: int` | `200 OK`<br>`application/pdf` (Binario) | `401 Unauthorized`<br>`404 Not Found` | **RF23**.<br>Descarga segura del archivo PDF compilado. |
| `GET` | `/api/v1/certificates/summary` | Query: `mentor_email: str` | `200 OK`<br>`HoursSummaryResponse` | `401 Unauthorized` | Resumen de horas visadas y progreso formativo. |
| `GET` | `/api/v1/simulation/benchmark` | None | `200 OK`<br>`BenchmarkMetricsResponse` | `500 Server Error` | **RF06 / RNF03**.<br>Ejecuta testbench y retorna Precision@k y latencias. |

Fuente: Elaboración propia conforme a la Regla D-3.

---

### 4.5. Diagramas de Arquitectura y Comportamiento en PlantUML

#### A. Modelo Entidad-Relación — Sprint 8 (Persistencia Integral del MVP)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
skinparam classFontSize 11
skinparam classAttributeFontSize 10

entity "usuarios" as Usuario {
    * email : VARCHAR(255) <<PK>>
    --
    * nombres : VARCHAR(100)
    * apellidos : VARCHAR(100)
    * ciclo_actual : INTEGER
}

entity "sesiones_mentoria" as Sesion {
    * id_sesion : INTEGER <<PK>>
    --
    * mentor_email : VARCHAR(255) <<FK>>
    * estado : VARCHAR(30)
    * duracion_minutos : INTEGER
}

entity "bitacoras_pedagogicas" as Bitacora {
    * id_bitacora : SERIAL <<PK>>
    --
    * id_sesion : INTEGER <<FK, Unique>>
    * horas_declaradas : FLOAT
    * visado_administrador : BOOLEAN
}

entity "certificados_horas" as Certificado {
    * id_certificado : SERIAL <<PK>>
    --
    * id_mentor : VARCHAR(255) <<FK>>
    * codigo_folio : VARCHAR(50) <<Unique>>
    * periodo_academico : VARCHAR(20)
    * horas_acreditadas : FLOAT
    * hash_firma : VARCHAR(64)
    * estado : VARCHAR(30)
    * created_at : TIMESTAMPTZ
}

Usuario ||--o{ Sesion : "dicta como mentor"
Sesion ||--|| Bitacora : "reporta desarrollo"
Usuario ||--o{ Certificado : "acredita horas en"
@enduml
```

#### B. Diagrama de Casos de Uso — Sprint 8 (Cierre del MVP)
```plantuml
@startuml
left to right direction
skinparam shadowing false
skinparam defaultFontName Arial

actor "Estudiante Mentor\n(>= 20h Acreditadas)" as Mentor
actor "Dirección EPIS / Administrador" as Admin
actor "Sistema / Testbench\n(Evaluador Algorítmico)" as Sistema

rectangle "Módulos Sprint 8: Cierre del MVP" {
    usecase "CUS13: Solicitar y emitir constancia de mentoría" as CUS13
    usecase "CUS18: Descargar constancia oficial en PDF (DEMO)" as CUS18
    usecase "CUS09: Verificar autenticidad con código QR" as CUS09
    usecase "CUS02: Evaluar ranking Top-k y Precision@k" as CUS02
    usecase "Validar umbral 20h visadas (RN-14)" as ReglaHoras
    usecase "Estampar marca de agua DEMO y hash SHA-256" as ReglaPDF
}

Mentor --> CUS13
Mentor --> CUS18
CUS13 ..> ReglaHoras : <<include>>
CUS13 ..> ReglaPDF : <<include>>

Admin --> CUS09
Sistema --> CUS02
@enduml
```

#### C. Máquina de Estados de la Entidad CertificadoHoras (Regla D-7)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial

[*] --> SOLICITADO : Mentor solicita emisión\n[horas_visadas >= 20.0] (RN-14)

SOLICITADO --> EMITIDO_DEMO : Compilador genera PDF vectorial\ncon marca de agua y hash SHA-256 (T-42)

EMITIDO_DEMO --> DESCARGADO : Mentor descarga documento PDF\ndesde CertificateDownloadView (T-43)

EMITIDO_DEMO --> ANULADO : Dirección detecta falsedad en bitácoras\n[proceso extraordinario de auditoría]

DESCARGADO --> [*]
ANULADO --> [*]
@enduml
```

### Cuadro 4.4: Matriz de Transiciones Válidas de Certificados (Regla D-7)

| Estado Origen | Estado Destino | Evento Disparador | Condición de Guarda | Actor Responsable |
| :--- | :--- | :--- | :--- | :--- |
| `[*]` | `SOLICITADO` | Clic en Emitir Constancia | $\text{horas\_visadas} \ge 20.0$, sin certificado previo | Estudiante Mentor |
| `SOLICITADO` | `EMITIDO_DEMO` | Generación exitosa de PDF | Inserción en `certificados_horas` y cálculo SHA-256 | Backend (CertificateService) |
| `EMITIDO_DEMO` | `DESCARGADO` | Solicitud de descarga binaria | Token JWT coincidente con titular o administrador | Estudiante Mentor |
| `EMITIDO_DEMO` | `ANULADO` | Revocación administrativa | Dictamen fundado de Dirección de Escuela | Administrador EPIS |

Fuente: Elaboración propia conforme a la Regla D-7.

**Transiciones Prohibidas:**
| Transición | Justificación de Negocio / Seguridad |
| :--- | :--- |
| `[*]` $\rightarrow$ `EMITIDO_DEMO` con horas $< 20.0$ | Violación terminante de la regla de mérito **RN-14**; el sistema bloquea en base de datos. |
| `ANULADO` $\rightarrow$ `EMITIDO_DEMO` | Un certificado revocado por irregularidad documental no puede rehabilitarse automáticamente. |

#### D. Diagrama de Secuencia de Emisión y Descarga de Constancia DEMO (Regla D-5)
```plantuml
@startuml
skinparam shadowing false
skinparam defaultFontName Arial
autonumber

actor "Estudiante Mentor" as Mentor
boundary "CertificateDownloadView" as UI
control "certificateService.ts" as Client
control "FastAPI (certificates.py)" as API
entity "CertificateService" as Domain
database "PostgreSQL" as DB

Mentor -> UI : Accede a "Mis Certificados"
UI -> Client : getHoursSummary(mentorEmail)
Client -> API : GET /api/v1/certificates/summary?mentor_email=...
API -> DB : SELECT sum(horas_declaradas) WHERE id_mentor=... AND visado_administrador=true
DB --> API : horas_visadas = 22.0
API --> Client : HTTP 200 OK (horas=22.0, eligible=true)
Client --> UI : Renderiza barra al 100% y activa botón "Emitir Constancia"

Mentor -> UI : Clic en "Emitir Constancia Oficial"
UI -> Client : generateCertificate()
Client -> API : POST /api/v1/certificates/generate (Bearer JWT)
activate API
API -> Domain : compile_demo_certificate(mentorEmail)
activate Domain
Domain -> DB : Validar unicidad (sin certificado en 2026-II)
DB --> Domain : No existe duplicado
Domain -> Domain : Generar folio correlativo ("CERT-2026-II-0042")
Domain -> Domain : Compilar PDF con marca de agua "DEMO - FINES ACADÉMICOS" y QR
Domain -> Domain : Calcular Hash SHA-256
Domain -> DB : INSERT INTO certificados_horas
DB --> Domain : Confirmación (id_certificado=7)
Domain --> API : Metadatos y ruta del binario PDF
deactivate Domain
API --> Client : HTTP 201 Created (id=7, folio="CERT-2026-II-0042")
deactivate API
Client --> UI : Muestra visor modal y activa botón de descarga directa
UI --> Mentor : Notificación de emisión exitosa y descarga automática de PDF
@enduml
```

---

### 4.6. Mapeo de Transformación de Datos entre Capas Arquitectónicas (Regla D-8.1)

### Cuadro 4.5: Mapeo de Atributos del Sprint 8 entre Capas Arquitectónicas (D-8.1)

| Columna PostgreSQL | Atributo SQLAlchemy | Campo Pydantic | JSON API | Interface TypeScript | Estado React |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id_certificado` (SERIAL) | `id_certificado: int` | `id_certificado: int` | `"id_certificado": 7` | `certificateId: number` | `certificate.id` |
| `codigo_folio` (VARCHAR) | `codigo_folio: str` | `codigo_folio: str` | `"codigo_folio": "CERT..."`| `folioCode: string` | `certificate.folio` |
| `horas_acreditadas` (FLOAT)| `horas_acreditadas: float`| `horas_acreditadas: float`| `"horas_acreditadas": 22.0`| `accreditedHours: number` | `hoursProgress` |
| `hash_firma` (VARCHAR) | `hash_firma: str` | `hash_firma: str` | `"hash_firma": "SHA256..."`| `signatureHash: string` | `certificate.hash` |
| `estado` (VARCHAR) | `estado: str` | `estado: str` | `"estado": "EMITIDO_DEMO"` | `certificateStatus: string` | `certStatus` |
| `periodo_academico` (VARCHAR)| `periodo_academico: str` | `periodo_academico: str` | `"periodo_academico": "2026-II"`| `academicPeriod: string`| `currentPeriod` |

Fuente: Elaboración propia conforme a la Regla D-8.1.

---

### 4.7. Catálogo Centralizado de Códigos de Error del Sprint 8 (Regla D-8.2)

### Cuadro 4.6: Catálogo Centralizado de Códigos de Error (Sprint 8) (D-8.2)

| Código Canónico | HTTP | Causa Técnica | Mensaje al Usuario en Frontend | Regla Vinculada |
| :--- | :---: | :--- | :--- | :---: |
| `INSUFFICIENT_ACCREDITED_HOURS`| 400 | El mentor tiene menos de 20.0 horas visadas por la Escuela. | No cumples con el umbral mínimo de 20 horas visadas para emitir la constancia. | RN-14 |
| `DUPLICATE_CERTIFICATE_ISSUANCE`| 409 | Ya existe una constancia emitida para el mentor en el ciclo 2026-II. | Ya se encuentra emitida tu constancia institucional para este período académico. | RF22 |
| `CERTIFICATE_NOT_FOUND` | 404 | El identificador o folio de constancia no existe en la base de datos. | La constancia solicitada no fue encontrada en el repositorio institucional. | RF23 |
| `CORRUPTED_DOCUMENT_STREAM` | 500 | Falla en la compilación vectorial o almacenamiento del archivo binario. | Error al generar el documento PDF. Por favor, reintente en unos momentos. | RNF07 |

Fuente: Elaboración propia conforme a la Regla D-8.2.

---

### 4.8. Registro de Decisiones Arquitectónicas (ADR) (Regla D-10.1)

### ADR-012: Generación Determinista de Constancias PDF con Marca de Agua DEMO, Hash SHA-256 y Folio Único

| Campo | Detalle de la Decisión Arquitectónica |
| :--- | :--- |
| **ID** | **ADR-012** |
| **Fecha** | 12/11/2026 |
| **Estado** | **Aprobada e Implementada** |
| **Contexto** | Se requería un mecanismo de emisión de constancias formalmente representativo para la evaluación de cátedra, pero con resguardos estrictos para evitar falsificaciones o su uso indebido fuera del ámbito académico. |
| **Decisión** | Compilar en backend documentos PDF con membretes de la EPIS-UPT, imponiendo por diseño una marca de agua indeleble `"DEMO - FINES ACADÉMICOS"`, un código QR que apunta a la verificación institucional y un hash SHA-256. La generación solo procede si la consulta agregada en PostgreSQL confirma $\ge 20.0$ horas con `visado_administrador = true` (**RN-14**). |
| **Consecuencias** | (+) Transparencia absoluta y valor probatorio en la demostración académica del MVP. (+) Blindaje contra uso fraudulento fuera del semestre lectivo. |
| **Requisitos Vinculados** | RF22, RF23, RN-14, CUS18, RNF02 |

### ADR-013: Metodología de Evaluación Desacoplada de Relevancia Algorítmica (Precision@k) sobre Espacios Vectoriales Sintéticos

| Campo | Detalle de la Decisión Arquitectónica |
| :--- | :--- |
| **ID** | **ADR-013** |
| **Fecha** | 12/11/2026 |
| **Estado** | **Aprobada e Implementada** |
| **Contexto** | En la fase de demostración académica, el volumen de datos de usuarios reales es reducido. Se requería una metodología rigurosa para verificar empíricamente la efectividad del ranking Top-k sin inventar métricas subjetivas. |
| **Decisión** | Implementar en `SimulationService` un generador determinista de cohortes sintéticas representativas de los 4 ciclos formativos de la EPIS-UPT, con juicios de relevancia ground-truth pre-etiquetados basados en la malla curricular oficial. Evaluar Precision@3 y Precision@5 de forma automatizada mediante Pytest. |
| **Consecuencias** | (+) Evaluación objetiva, reproducible y auditable frente al docente de cátedra (**RNF03**). (+) Certificación de latencias sub-15ms sin degradación del rendimiento. |
| **Requisitos Vinculados** | RF06, RNF03, CUS02, RNF09 |

---

## 5. Matriz Consolidada de Trazabilidad de Requerimientos, Reglas y Casos de Uso

### Cuadro 5.1: Matriz Consolidada de Trazabilidad Técnica (Sprint 8)

| Requerimiento Funcional | Módulo SRS | Reglas Asociadas | Casos de Uso | Tareas Vinculadas | Tratamiento en Sprint 8 |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **RF22** (Parametrización y emisión de certificados) | MOD-07 | RN-14 | CUS13, CUS18 | T-42, T-43, T-44 | **Núcleo Sprint 8.** Servicio `certificate_service.py`, validación de 20h visadas, PDF con marca DEMO y QR. |
| **RF23** (Descarga y verificación de certificados) | MOD-07 | RN-14 | CUS18 | T-43, T-44 | **Núcleo Sprint 8.** Endpoint `/download`, vista `CertificateDownloadView.tsx` con barra de avance y verificación de folio. |
| **RF06** (Ranking Top-k y motor de recomendación) | MOD-03 | RN-03, RN-11 | CUS02 | T-45, T-46 | **Núcleo Sprint 8.** Medición de Precision@3 (83.3%) y Precision@5 (80.0%), testbench determinista y latencias. |
| **RNF03** (Tiempo de respuesta de recomendación) | Rendimiento | Límites de latencia | CUS02 | T-45 | Latencia media observada de $12.4\text{ ms}$, ampliamente inferior al umbral de $1500\text{ ms}$. |
| **RNF05** (Accesibilidad universal WCAG 2.1 AA) | Usabilidad | Normas W3C | Todos | T-49 | Auditoría de contraste $\ge 4.5:1$, foco visible, lectores de pantalla y soporte integral de teclado. |
| **RNF06** (Facilidad de navegación e integración) | Usabilidad | Diseño modular | Todos | T-47, T-48 | Shell institucional en `App.tsx`, sincronización bidireccional URL `?tab=` y guardas RBAC fluidas. |
| **RNF09** (Cobertura de pruebas $\ge 70\%$) | Calidad | Estándar Cátedra | Todos | T-48, T-51 | **Cierre con 556 pruebas automatizadas aprobadas (85.0% Backend / 83.50% Frontend).** |
| **RNF10** (Despliegue y reproducibilidad) | Despliegue | Entornos de prueba | Todos | T-50, T-51 | Fixtures `seed_demo_data.py`, cuentas preconfiguradas para defensa y script de inicio con comando único. |

Fuente: Elaboración propia a partir del SRS (FD03), SAD (FD04) y `PLAN_SPRINTS_Y_TAREAS.md`.

---

## 6. Métricas Consolidadas de Calidad de Software, Estado Técnico y Cierre del Sprint 8 y Proyecto

### Cuadro 6.1: Balance Métrico Consolidado de Pruebas Automatizadas y Calidad de Software (Cierre Definitivo)

| Dimensión de Calidad | Herramienta de Auditoría | Umbral Requerido (RNF09) | Cierre Sprint 7 | Cierre Oficial MVP (Sprint 8) | Estado Técnico |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Suites de Prueba** | Vitest 2.1.8 / Pytest 9.1.1 | 100% aprobadas | 42 suites | **48 suites aprobadas** (29 FE / 19 BE) | ✅ Conforme |
| **Pruebas Automatizadas** | Vitest / Pytest | 100% aprobadas | 512 pruebas | **556 pruebas aprobadas** (311 FE / 245 BE) | ✅ Conforme (100% passing) |
| **Cobertura Frontend (Líneas)**| Vitest v8 | $\ge 70.0\%$ | 83.70% | **83.50%** | ✅ Superado con holgura |
| **Cobertura Backend (Líneas)** | Pytest-Cov | $\ge 70.0\%$ | 86.95% | **85.00%** (3127 stmts / 475 miss) | ✅ Superado ampliamente |
| **Linteo y Análisis Estático** | ESLint 9 / Ruff 0.8.0 | 0 defectos | 0 defectos | **0 defectos estáticos** | ✅ Conforme |
| **Formato y Estilizado** | Prettier / Ruff format | 100% estándar | 100% estándar | **100% estandarizado** | ✅ Conforme |
| **Precisión Algorítmica (P@3)** | Testbench de simulación | $\ge 70.0\%$ | N/A | **83.33%** | ✅ Superado |
| **Latencia Algorítmica** | Testbench de simulación | $\le 1500.0\text{ ms}$ | N/A | **12.4 ms** | ✅ Excepcional |
| **Integración Continua (CI)** | GitHub Actions (`ci.yml`) | Workflow verde | Success | **Success** | ✅ Conforme |

Fuente: Reportes de ejecución automatizada en entorno local y GitHub Actions sobre la rama `main`.

---

### Cuadro 6.2: Historial Completo de Commits del Incremento Sprint 8

| Commit SHA | Autor | Mensaje Canónico del Commit | Tarea / Hito Vinculado |
| :---: | :---: | :--- | :---: |
| [`b24d578`](https://github.com/JMedina255/sistema_web_p2p/commit/b24d578) | Renzo Antayhua | `feat(backend): implement PDF demo certificate generation engine with watermark [T-42]` | **T-42 (Backend)** |
| [`c35e689`](https://github.com/JMedina255/sistema_web_p2p/commit/c35e689) | Joan Medina | `feat(frontend): develop certificate download interface and progress bar [T-43]` | **T-43 (Frontend)** |
| [`d46f790`](https://github.com/JMedina255/sistema_web_p2p/commit/d46f790) | Renzo Antayhua | `feat(backend): register certificate issuance and demo serial tracking in database [T-44]` | **T-44 (Backend)** |
| [`e57a801`](https://github.com/JMedina255/sistema_web_p2p/commit/e57a801) | Renzo Antayhua | `test(benchmark): evaluate Precision@3 and Precision@5 ranking metrics with ground-truth testbench [T-45]` | **T-45 (Backend)** |
| [`f68b912`](https://github.com/JMedina255/sistema_web_p2p/commit/f68b912) | Joan Medina | `docs(metrics): document Precision@k evaluation results and algorithmic boundary conditions [T-46]` | **T-46 (Frontend)** |
| [`cff8d40`](https://github.com/JMedina255/sistema_web_p2p/commit/cff8d40) | Joan Medina | `feat(ui): integrate end-to-end user navigation flow and role-based guards in React App Shell [T-47]` | **T-47 (Frontend)** |
| [`4cbf504`](https://github.com/JMedina255/sistema_web_p2p/commit/4cbf504) | Renzo Antayhua | `test(e2e): execute end-to-end integration test suites across mentee, mentor and admin roles [T-48]` | **T-48 (Backend)** |
| [`a1d198d`](https://github.com/JMedina255/sistema_web_p2p/commit/a1d198d) | Joan Medina | `test(exploratory): perform WCAG 2.1 AA accessibility and cross-browser exploratory tests [T-49]` | **T-49 (Frontend)** |
| [`bb9ce3c`](https://github.com/JMedina255/sistema_web_p2p/commit/bb9ce3c) | Joan Medina | `chore(demo): configure reproducible demo environment and seed data fixtures [T-50]` | **T-50 (Frontend)** |
| [`ca730f3`](https://github.com/JMedina255/sistema_web_p2p/commit/ca730f3) | Ambos | `docs(closure): consolidate final MVP technical documentation and project closure audit [T-51]` | **T-51 (Ambos)** |
| [`f28c442`](https://github.com/JMedina255/sistema_web_p2p/commit/f28c442) | Joan Medina | `fix(integration): corregir flujo funcional de sesiones y reservas demo` | **S8 Cierre Definitivo** |

Fuente: Registro Git del repositorio oficial `sistema_web_p2p`.

---

### 6.1. Verificación de Criterios de Aceptación (Definition of Done)

Para el cierre formal del Sprint 8 y del ciclo de vida del MVP, se certifica el cumplimiento del 100% de los criterios:

- [x] **Criterio 1 (Generación de Constancias PDF DEMO):** Emisión restringida a mentores con $\ge 20.0$ horas visadas (**RN-14**), incorporando marca de agua diagonal `"DEMO - FINES ACADÉMICOS"`, código QR y hash SHA-256.
- [x] **Criterio 2 (Evaluación Cuantitativa de Precision@k):** $\text{Precision@3} \ge 80.0\%$ y $\text{Precision@5} \ge 75.0\%$ comprobadas formalmente con datos de prueba etiquetados ground-truth, con latencias medias menores a 15 ms.
- [x] **Criterio 3 (Recorrido de Demostración E2E Fluido):** Capacidad de recorrer íntegramente el flujo de los cuatro roles institucionales (Visitante, Mentoreado, Mentor y Administrador) sin bloqueos técnicos ni inconsistencias de estado.
- [x] **Criterio 4 (Accesibilidad y Usabilidad Universal):** Cumplimiento verificado de las pautas WCAG 2.1 AA en todas las interfaces de usuario del sistema.
- [x] **Criterio 5 (Reproducibilidad de Demostración):** Entorno y script de inicialización con cuentas preconfiguradas que permiten reproducir cualquier escenario pedagógico en la defensa ante cátedra.
- [x] **Criterio 6 (Calidad y Cobertura Integral):** Suite de 556 pruebas automatizadas aprobadas, coberturas de 85.0% en backend y 83.5% en frontend, 0 fallos de linteo y pipeline de CI en estado verde.

---

### 6.2. Cierre Definitivo del Ciclo de Sprints y Entrega Final del MVP

Con la culminación del **Sprint 8**, el equipo de desarrollo (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani) da por concluida con éxito la construcción del **Sistema Web P2P de Mentorías Académicas para la EPIS-UPT**:

- **Compromiso del Backlog Cumplido al 100%:** Las 51 tareas de ingeniería planificadas a lo largo de los 8 sprints fueron culminadas, verificadas mediante pruebas y respaldadas por documentación técnica rigurosa.
- **Arquitectura Robusta y Mantenible:** La separación desacoplada entre React 19 (TypeScript) y FastAPI (Python), respaldada por PostgreSQL con seguridad a nivel de fila (RLS), garantiza una solución escalable, segura y plenamente alineada con los estándares de acreditación universitaria (ICACIT).
- **Listo para Evaluación Académica:** El repositorio cuenta con guías de reproducción rápida, cuentas institucionales de prueba y suites de verificación automatizadas ejecutables con un solo comando.

---

## 7. Evidencias visuales y comprobación funcional del Sprint 08

---

### 7.1. Figura 7.1: Panel del Mentor con Barra de Horas Acreditadas
La interfaz [`CertificateDownloadView.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/components/CertificateDownloadView.tsx) exhibiendo la barra de progreso formativo al 100% (22.0 de 20.0 horas acreditadas visadas por Dirección) y el botón interactivo *"Emitir Constancia Oficial"* habilitado.

### 7.2. Figura 7.2: Previsualización de la Constancia Oficial de Mentoría (PDF)
Visor integrado desplegando la constancia generada con membrete oficial EPIS-UPT, folio alfanumérico correlativo `CERT-2026-II-0042` y desglose de horas dictadas.

### 7.3. Figura 7.3: Detalle de Seguridad: Marca de Agua DEMO y Código QR
Ampliación del documento PDF evidenciando la marca de agua diagonal `"DEMO - FINES ACADÉMICOS"`, el código QR de verificación institucional y la huella criptográfica SHA-256.

### 7.4. Figura 7.4: Bloqueo de Emisión por Horas Insuficientes (< 20h)
Comprobación visual de un mentor con 14 horas acumuladas: la interfaz bloquea el botón de emisión y despliega el aviso pedagógico indicando que faltan 6 horas visadas (**RN-14**).

### 7.5. Figura 7.5: Reporte Automatizado del Testbench Algorítmico (Precision@k)
Captura de la ejecución de `SimulationService.run_benchmark()` certificando $\text{Precision@3} = 0.833$, $\text{Precision@5} = 0.800$ y latencia media de $12.4\text{ ms}$.

### 7.6. Figura 7.6: Recorrido E2E – Navegación Fluida del Shell Institucional
Navegación reactiva en [`App.tsx`](file:///d:/sistema_web_p2p/aplicacion/frontend/src/App.tsx) mostrando la conmutación instantánea entre pestañas protegidas y preservación del parámetro `?tab=` en la URL del navegador.

### 7.7. Figura 7.7: Conmutador de Roles en Tiempo Real (RBAC)
Interacción en el menú de usuario alternando activamente entre el rol de Mentoreado y Mentor, adaptando la barra de navegación y las guardas de seguridad en milisegundos.

### 7.8. Figura 7.8: Comprobación de Accesibilidad WCAG 2.1 AA
Auditoría mediante inspector de accesibilidad comprobando navegación por teclado, contraste superior a $4.5:1$ y captura de foco en diálogos modales.

### 7.9. Figura 7.9: Inicialización de Fixtures Reproducibles de Demostración
Ejecución del script `seed_demo_data.py` en consola poblando la base de datos con asignaturas, temarios silábicos, perfiles y sesiones listas para defensa académica.

### 7.10. Figura 7.10: Suites de Pruebas Automatizadas (556 Tests) y CI Verde
Consola de pruebas reportando la aprobación unánime de las 556 pruebas automatizadas (311 en Vitest y 245 en Pytest), coberturas superiores al 83% y paso verde del workflow de GitHub Actions.
