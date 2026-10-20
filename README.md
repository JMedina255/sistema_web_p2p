# Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

> **Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
> **Curso:** Construcción de Software I
> **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
> **Autores:**
> - ANTAYHUA MAMANI, Renzo Antonio (2022073504)
> - MEDINA QUISPE, Joan Cristian (2022074255)
>   
> **Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
>
> **Semestre Académico:** 2026-II

---

## 📌 1. Visión General del Sistema

El **Sistema Web P2P** es una plataforma institucional orientada a conectar a estudiantes de ciclos formativos iniciales (*Mentoreados*, ciclos I al IV) con estudiantes de rendimiento sobresaliente de ciclos superiores (*Mentores*, ciclos VII al X) para mitigar los altos índices de reprobación y deserción en asignaturas filtro críticas (*Cálculo I/II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*) de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

**Estado actual:** Fase de construcción — **Sprint 1 Culminado y Verificado**. La solución se desarrolla en `aplicacion/` (React SPA + FastAPI RESTful con persistencia en PostgreSQL/Supabase conforme a **RNF09**). La totalidad de las 6 tareas planificadas han sido completadas y verificadas:
- **Tareas de Joan:** **T-01** (entorno base y conexión técnica a Supabase `p2p-epis-dev`), **T-02** (interfaz de acceso institucional `@upt.pe` con desafío OTP) y **T-06** (suite de pruebas iniciales y flujo de CI en GitHub Actions verificado exitosamente en el run [`39331555735`](https://github.com/JMedina255/sistema_web_p2p/actions/runs/39331555735)).
- **Tareas de Renzo:** **T-09** (modelos ORM, migración Alembic con datos semilla de las **5 materias filtro**: *Cálculo I, Cálculo II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*, y endpoints RESTful de catálogo curricular), **T-03** (API real de autenticación OTP `/api/v1/auth/otp/*`, adaptador `ApiAuthAdapter` en frontend y emisión de tokens JWT de sesión con algoritmo HS256) y **T-07** (políticas de seguridad Row Level Security RLS en script SQL y guía de configuración para Supabase).
- **Aseguramiento de Calidad:** Suite consolidada de **96 pruebas automatizadas** (46 en frontend y 50 en backend) con cobertura superior al 91%, superando holgadamente la meta mínima de **RNF09** ($\ge 70\%$). El directorio `frontend/` se conserva como maqueta de referencia visual. El SRS FD03 v2.0 es la fuente canónica de requisitos y el SAD FD04 v1.1 orienta la arquitectura técnica.

### Pilares Funcionales y Tecnológicos
1. **Recomendación personalizada:** RF06 y CUS02 analizan afinidad temática, disponibilidad y criterios de RN-11; RF24 incorpora prioridad institucional sobre las 5 materias filtro.
2. **Reserva, confirmación y quórum:** RF12–RF16 distinguen reserva provisional (CUS04), ratificación (CUS24), corte T−24 h (CUS23) y decisión del mentor ante quórum insuficiente (CUS07).
3. **Asistencia y bitácora:** RF17 y CUS08 permiten registrar asistencia y cerrar la sesión. El QR es una alternativa de marcado por el mentor, cuya política técnica queda pendiente de diseño.
4. **Auditoría y certificación:** CUS22 visa horas antes de la emisión CUS13 y descarga CUS09, conforme a RN-14; se propone PDF, correlativo, hash de integridad y consulta institucional.
5. **Acceso y privacidad:** RF01–RF02 y RNF01–RNF02 exigen OTP institucional, consentimiento y protección de datos con políticas RLS de PostgreSQL/Supabase.

---

## 📚 2. Mapa de Documentación Oficial de Ingeniería de Software

La documentación se desarrolla bajo UWE y la estructura de requisitos adoptada en el SRS. La revisión actual alinea el SAD y sus secuencias; las discrepancias heredadas de otros artefactos se registran en la matriz de inconsistencias:

| Entregable / Documento | Ubicación | Descripción y Alcance Metodológico |
| :--- | :--- | :--- |
| **Resumen Ejecutivo del Sistema** | [`docs/resumen_sistema_y_casos_de_uso.md`](docs/resumen_sistema_y_casos_de_uso.md) | **Lectura recomendada:** Visión concisa, flujo macro de 5 fases, matriz de 17 CUS críticos, relaciones de precedencia, máquinas de estado y síntesis de reglas de negocio. |
| **FD01: Informe de Factibilidad** | [`docs/FD01-EPIS-Informe de Factibilidad.md`](docs/FD01-EPIS-Informe%20de%20Factibilidad.md) | Evaluación exhaustiva de viabilidad operativa, técnica, económica y legal en el ámbito universitario de la UPT. |
| **FD02: Informe Visión del Proyecto** | [`docs/FD02-EPIS-Informe Vision de Proyecto.md`](docs/FD02-EPIS-Informe%20Vision%20de%20Proyecto.md) | Oportunidades de negocio, definición de stakeholders, posicionamiento del producto y características principales. |
| **FD03: Informe SRS de Proyecto** | [`docs/FD03-EPIS-Informe SRS de Proyecto.md`](docs/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | **Especificación de Requisitos de Software canónica:** Catálogo de 24 CUS, modelos ECB, diagramas de actividades con objetos, diagramas de secuencia y clases parciales. |
| **FD04: Informe SAD de Proyecto** | [`docs/FD04-EPIS-Informe SAD de Proyecto.md`](docs/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | **SAD v1.1 en análisis:** Vistas 4+1 propuestas, nomenclatura del SRS, matrices de trazabilidad y decisiones pendientes de diseño. |
| **Bóveda General de Diagramas** | [`docs/diagramas_general.md`](docs/diagramas_general.md) | Bóveda de artefactos. La sección 14 mantiene copias de los diagramas y cuadros vigentes del SAD y sus secuencias. |
| **Diagramas de Secuencia (SAD Análisis)** | [`docs/diagramas_de_secuencia.md`](docs/diagramas_de_secuencia.md) | **Secuencias v2.2 en análisis:** Acceso con OTP y consentimiento, Top-k, reserva/confirmación/quórum y bitácora/asistencia/visado; códigos CUS del SRS. |
| **Flujos por Perfil y Diagrama de Paquetes** | [`docs/flujos_por_perfil_y_diagrama_paquetes.md`](docs/flujos_por_perfil_y_diagrama_paquetes.md) | **Flujos y Arquitectura de Maquetación:** Diagramas de flujo de actividades para Administrador, Mentor y Mentoreado con mapeo biunívoco a paquetes. |
| **Matriz de Inconsistencias** | [`docs/matriz_inconsistencias.md`](docs/matriz_inconsistencias.md) | Registro de auditoría y resolución de discrepancias en requisitos y modelos. |
| **Catálogo de Pruebas** | [`docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) | Matriz formal de casos de prueba funcional, criterios de aceptación y verificación QA. |
| **Plan de Sprints y Tareas** | [`docs/sprints/PLAN_SPRINTS_Y_TAREAS.md`](docs/sprints/PLAN_SPRINTS_Y_TAREAS.md) | **Planificación Scrum:** Desglose del Product Backlog (37 PBI), capacidad (91 h) y asignación operativa (T-01 a T-51). |
| **Bitácora de Sprint 1** | [`docs/sprints/sprint-01.md`](docs/sprints/sprint-01.md) | **Registro de Ejecución S1:** Culminación integral de T-01, T-02, T-03, T-06, T-07 y T-09 con 96 pruebas automatizadas. |
| **Guía de Configuración Supabase** | [`docs/supabase_setup_guide.md`](docs/supabase_setup_guide.md) | **Paso a paso para el usuario:** Conexión con Session Pooler, migración Alembic, RLS script y JWT Secret. |
| **Reglas de Documentación (Hardening)** | [`reglas_documentacion.md`](reglas_documentacion.md) | Estándares obligatorios de granularidad en análisis, estructura quíntuple de tablas, estándar PlantUML y reglas de sincronización. |

---

## 🏛️ 3. Módulos Funcionales del Sistema

La arquitectura del sistema se estructura en 8 módulos interconectados que orquestan el flujo integral de mentoría entre pares, desde la autenticación federada y priorización de cursos, hasta el control de asistencia, certificación con firma digital y supervisión institucional:

```text
┌────────────────────────────────────────────────────────┐
│            ECOSISTEMA P2P  -  EPIS UPT (2026)          │
└───────────────────────────┬────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    MOD-01    │     │    MOD-02    │     │    MOD-03    │
│ Autenticación│     │ Recomendación│     │ Oferta y     │
│ 2FA / RLS    │     │ Top-k Híbrido│     │ Demanda P2P  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    MOD-04    │     │    MOD-05    │     │    MOD-06    │
│ Reservas y   │     │ Asistencia QR│     │ Calidad CSAT │
│ Quórum T-24h │     │ y Bitácoras  │     │ e Insignias  │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌──────────────┐            ┌──────────────┐
       │    MOD-07    │            │    MOD-08    │
       │ Certificación│            │ Auditoría y  │
       │ SHA-256 + QR │            │ Analítica    │
       └──────────────┘            └──────────────┘
```

Los módulos conservan la denominación canónica del Cuadro 5.1 del SRS y se relacionan directamente con sus requisitos funcionales (`RF01` al `RF26`), sirviendo como base de entrada a la matriz de trazabilidad del SAD:

### Cuadro 3.1: Módulos canónicos del SRS

| Código | Módulo | RF |
| :--- | :--- | :--- |
| **MOD-01** | Seguridad, Autenticación y Gobernanza | RF01, RF02, RF03 |
| **MOD-02** | Gestión Curricular y Perfiles Académicos | RF04, RF05 |
| **MOD-03** | Motor de Recomendación Inteligente (*EdRecSys*) | RF06, RF07 |
| **MOD-04** | Planificación, Espacios y Agendamiento | RF08, RF09, RF10, RF11 |
| **MOD-05** | Quórum, Confirmación y Cancelaciones | RF12, RF13, RF14, RF15, RF16 |
| **MOD-06** | Trazabilidad, Bitácoras y Evaluación | RF17, RF18, RF19, RF20 |
| **MOD-07** | Gamificación, Reputación y Certificación | RF21, RF22, RF23 |
| **MOD-08** | Supervisión y Analítica Institucional | RF24, RF25, RF26 |

Fuente: SRS FD03 v2.0, cuadros 5.1 y 5.3.

La secuencia funcional del flujo comprende: acceso y perfil institucional (`MOD-01`), gestión de cursos prioritarios y perfiles (`MOD-02`), recomendación algorítmica *Top-k* (`MOD-03`), agendamiento de franjas y reserva de espacios (`MOD-04`), control perentorio de quórum a $T-24\text{ h}$ (`MOD-05`), registro pedagógico de bitácoras y asistencia por QR (`MOD-06`), reconocimiento por gamificación y certificación digital SHA-256 (`MOD-07`), y supervisión directiva por el Comité de Tutoría de la EPIS (`MOD-08`).

---

## 📁 4. Estructura del Repositorio

```text
Proyecto_Sistema_Web_P2P/
├── aplicacion/                                # Aplicación desacoplada oficial (Sprint 1 en adelante)
│   ├── backend/                               # API RESTful (FastAPI + SQLAlchemy + Alembic + Pytest)
│   │   ├── app/
│   │   │   ├── api/v1/endpoints/              # Endpoints RESTful: health.py, auth.py, curriculum.py
│   │   │   ├── core/                          # Configuración pydantic-settings y seguridad criptográfica JWT/OTP
│   │   │   ├── db/                            # Conexión diferida, session pooler y migraciones Alembic
│   │   │   │   └── migrations/versions/       # Migración canónica 001 con catálogo de 5 materias filtro
│   │   │   ├── models/                        # Modelos ORM: Asignatura, TemaConceptual, AuthChallenge
│   │   │   ├── schemas/                       # Esquemas Pydantic tipados de entrada y respuesta
│   │   │   ├── services/                      # Servicios de dominio: AuthService, CurriculumService
│   │   │   └── main.py                        # Punto de entrada de FastAPI con middleware CORS
│   │   ├── scripts/
│   │   │   └── supabase_rls_setup.sql         # Script SQL canónico de Row Level Security (T-07)
│   │   ├── tests/                             # 48 pruebas unitarias y de integración (85% de cobertura)
│   │   ├── alembic.ini                        # Configuración de migraciones hacia PostgreSQL
│   │   ├── pyproject.toml                     # Configuración centralizada de Ruff, Coverage y Pytest
│   │   └── requirements.txt                   # Dependencias reproducibles fijadas con == (incluye PyJWT)
│   └── frontend/                              # SPA cliente reactiva (React 19 + TypeScript + Vite + Vitest)
│       ├── src/
│       │   ├── components/                    # Componentes UI: LoginOtpView, CurriculumCatalogView, HealthStatus
│       │   ├── services/                      # Servicios: apiClient.ts, authService.ts (Mock y ApiAuthAdapter)
│       │   ├── data/                          # Tipos TypeScript de dominio
│       │   ├── App.tsx                        # Orquestador con selector de pestañas (Auth, Catálogo, Servicios)
│       │   └── main.tsx                       # Punto de entrada ReactDOM
│       ├── package.json                       # Dependencias y scripts de prueba y cobertura
│       └── vite.config.ts                     # Configuración del empaquetador Vite con soporte de Vitest
├── docs/                                      # Acervo documental formal de ingeniería de software
│   ├── sprints/
│   │   ├── PLAN_SPRINTS_Y_TAREAS.md           # Planificación Scrum canónica (37 PBI, 91 h, S1–S8)
│   │   └── sprint-01.md                       # Bitácora oficial de ejecución del Sprint 1 (H1 al H7)
│   ├── supabase_setup_guide.md                # Guía canónica paso a paso para vincular proyecto Supabase
│   ├── FD01-EPIS-Informe de Factibilidad.md  # Viabilidad operativa, técnica, económica y legal
│   ├── FD02-EPIS-Informe Vision de Proyecto.md # Visión, actores, posicionamiento y alcance
│   ├── FD03-EPIS-Informe SRS de Proyecto.md  # Especificación formal de requisitos (SRS canónico IEEE 830)
│   ├── FD04-EPIS-Informe SAD de Proyecto.md  # Documento formal de arquitectura de software (Modelo 4+1)
│   ├── resumen_sistema_y_casos_de_uso.md     # Síntesis ejecutiva, flujo macro, matriz CUS y reglas de negocio
│   ├── diagramas_general.md                  # Bóveda consolidada y de hardening de diagramas PlantUML
│   ├── diagramas_secuencia_pruebas.md        # Diagramas de secuencia en lenguaje de análisis (ECB)
│   ├── matriz_inconsistencias.md             # Matriz de consistencia metodológica de análisis
│   ├── Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx # Catálogo de pruebas funcionales y de aceptación
│   ├── flujos_por_perfil_y_diagrama_paquetes.md # Diagramas de flujo por actor y diagrama de paquetes con mockups
│   └── diseño.md                             # Guía preliminar de interfaz y estilos
├── frontend/                                  # Maqueta funcional de referencia visual (conservada)
├── reglas_documentacion.md                    # Manual de normas de documentación y hardening (v1.3)
├── rules_doc.md                               # Registro histórico de directrices iniciales
├── .gitignore                                 # Reglas de exclusión de git
└── README.md                                  # Mapa central de navegación del proyecto (este archivo)
```

---

## 🚀 5. Maquetación Web: Estado del Desarrollo y Credenciales de Acceso

### 5.1 Estado Actual de la Maquetación
- **Fase del Proyecto:** Maquetación funcional de alta fidelidad (Frontend SPA) en **React 19 + TypeScript + Vite 8**.
- **Nivel de Interactividad:** 100% funcional en cliente. Integra navegación reactiva, validaciones de formularios, simulación de corte de quórum a $T-24\text{ h}$, generación de pases QR efímeros, escaneo de tickets, flujo de bitácoras docentes y emisión de diplomas digitales con hash SHA-256.
- **Seguridad en Acceso:** El acceso a la plataforma es **estrictamente manual** mediante usuario institucional y contraseña (se deshabilitaron accesos automáticos de 1 clic para validar formalmente el flujo de autenticación RBAC y el consentimiento de la Ley N° 29733).
- **Trazabilidad Arquitectónica:** Cada componente de la interfaz responde directamente a los paquetes lógicos del sistema (`MOD-01` al `MOD-08`), tal como se detalla en [`docs/flujos_por_perfil_y_diagrama_paquetes.md`](docs/flujos_por_perfil_y_diagrama_paquetes.md).

### 5.2 Credenciales Oficiales para Evaluación de Flujos

Para validar la experiencia diferenciada por actor institucional, se encuentran preconfiguradas las siguientes tres credenciales:

| Rol Institucional | Nombre del Usuario | Usuario | Contraseña | Vistas y Flujos Habilitados en Maqueta |
| :--- | :--- | :---: | :---: | :--- |
| **Administrado (Tutoría)** | **Ing. Liliana Vega Bernal** | `admin` | `admin123` | • Tablero analítico institucional de KPIs y deserción (CUS14).<br>• Auditoría de bitácoras y visado oficial de horas (CUS22).<br>• Emisión de certificados foliados con hash SHA-256 (CUS13).<br>• Calibración del factor $\alpha \in [1.05, 1.50]$ para cursos críticos (CUS12). |
| **Mentor Académico** | **Joan Medina Q** (VIII Ciclo) | `mentor` | `mentor123` | • Publicación de ofertas en materias aprobadas $\ge 14$ (CUS06/09).<br>• Gestión de citas y corte de quórum en $T-24\text{ h}$ con dictado excepcional (CUS09/07).<br>• Verificación de asistencia en aula por código QR efímero (CUS11).<br>• Rendición docente: registro de bitácora post-sesión (CUS10).<br>• Consulta de horas visadas oficiales y descarga de certificado (CUS16/09). |
| **Estudiante Mentoreado** | **Renzo Antayhua M** (II Ciclo) | `mentoreado` | `mentoreado123` | • Firma de consentimiento informado digital Ley N° 29733 (RF01).<br>• Consulta del recomendador híbrido Top-k con afinidad temática (CUS02).<br>• Registro de solicitudes temáticas por demanda (CUS03).<br>• Reserva de cupo y ratificación obligatoria en $T-24\text{ h}$ (CUS24).<br>• Visualización de ticket digital con código QR de acceso (CUS11).<br>• Encuesta anónima de calidad pedagógica CSAT post-mentoría (CUS05). |

### 5.3 Despliegue y Ejecución Local

#### A. Aplicación Desacoplada (Sprint 1 — `aplicacion/`)
1. **Backend API (FastAPI + Python 3.13 — comprobado localmente en `.venv`: Python 3.13.5; antecedente planificado: Python 3.11):**
   ```powershell
   cd aplicacion/backend
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

   # Análisis estático (Ruff: 0 errores, 0 advertencias)
   ruff check .
   ruff format --check .

   # Aplicar migraciones con datos semilla a Supabase (T-09)
   alembic upgrade head

   # Pruebas automatizadas y cobertura (Pytest: 50 pruebas pasadas; 91.62% de cobertura)
   pytest

   # Servidor de desarrollo
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   • API Docs (Swagger): **[http://localhost:8000/docs](http://localhost:8000/docs)**  
   • Health Check Backend: **[http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)**  
   • Diagnóstico BD Supabase (dev): **[http://localhost:8000/api/v1/health/db](http://localhost:8000/api/v1/health/db)**  
   • Catálogo Curricular: **[http://localhost:8000/api/v1/curriculum/courses](http://localhost:8000/api/v1/curriculum/courses)**

2. **Frontend SPA (React 19 + TypeScript + Vite + Node 22 — comprobado localmente: v22.17.1):**
   ```powershell
   cd aplicacion/frontend
   npm ci

   # Análisis estático (ESLint: 0 errores, 0 advertencias)
   npm run lint

   # Pruebas unitarias y cobertura (Vitest: 46 pruebas pasadas; 93.81% líneas, 76.92% ramas, 78.94% funciones)
   npm run test:coverage
   npm run build

   # Servidor de desarrollo
   npm run dev
   ```
   • Aplicación Web: **[http://localhost:5173](http://localhost:5173)**  
   • Pestaña *"Acceso & OTP de Prueba (T-02 / T-03)"*: Permite interactuar con el flujo de dos pasos CUS01/RF01 tanto con el adaptador Mock como contra la API real emitiendo tokens JWT de sesión.  
   • Pestaña *"Catálogo Curricular (T-09)"*: Visualiza interactivamente las 5 materias filtro y sus unidades silábicas.  
   • Pestaña *"Monitor de Servicios & BD (T-01)"*: Monitor en tiempo real de FastAPI y diagnóstico de base de datos Supabase (`SELECT 1`).

#### B. Maqueta de Referencia Visual (`frontend/`)
Para consultar la maqueta de referencia original con datos simulados en memoria:
```bash
cd frontend
npm install
npm run dev
```


---

## 🛡️ 6. Normas de Calidad y Reglas de Hardening

El proyecto opera bajo directrices de aseguramiento de la calidad registradas en [`reglas_documentacion.md`](reglas_documentacion.md):
- **Regla 1:** Fase de análisis y desarrollo del SAD; nomenclatura del SRS y separación de requisitos, propuestas y validaciones futuras.
- **Regla 2:** Estructura quíntuple estándar en toda tabla (Presentación → Título → Tabla MD → Fuente → Análisis/Conclusión).
- **Regla 3:** Uso exclusivo de diagramas PlantUML limpios, ejecutables y mantenibles.
- **Regla 4:** Codificación UTF-8 estricta en archivos Markdown.
- **Regla 5:** Hardening continuo y sincronización inmediata con [`docs/diagramas_general.md`](docs/diagramas_general.md).
- **Regla 6:** Estructura canónica de 4 tablas para las narrativas de casos de uso (Ficha, Flujo Principal, Alternativos, Excepciones).
- **Regla 7:** Sincronización y actualización continua del archivo [`README.md`](README.md) ante cualquier evolución de ingeniería.

---

## ⚖️ 7. Marco Legal y Ético

El SRS establece el siguiente contexto normativo para el análisis. Su vigencia, aplicabilidad y cumplimiento institucional deben revisarse antes de producción:
- **Ley N° 29733 (Ley de Protección de Datos Personales del Perú):** Principio de consentimiento previo, expreso e informado; derecho de revocación; protección de identidad en métricas y encuestas. El modelo preliminar aún requiere resolver la separación de respuestas y datos identificables.
- **Ley Universitaria N° 30220 (Art. 40 - Tutoría y Consejería):** Reconocimiento formal de la mentoría académica entre pares como actividad formativa y solidaria computable para la convalidación de horas de servicio estudiantil ante la Dirección de Escuela de la EPIS-UPT.

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — 2026*
