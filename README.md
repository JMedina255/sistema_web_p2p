# Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

> **Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT
> **Curso:** Construcción de Software I
> **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas
> **Autores:**
> - ANTAYHUA MAMANI, Renzo Antonio (2022073504)
> - MEDINA QUISPE, Joan Cristian (2022074255)
> **Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado
> **Semestre Académico:** 2026-II

---

## 📌 1. Visión General del Sistema

El **Sistema Web P2P** es una plataforma institucional orientada a conectar a estudiantes de ciclos formativos iniciales (*Mentoreados*, ciclos I al IV) con estudiantes de rendimiento sobresaliente de ciclos superiores (*Mentores*, ciclos VII al X) para mitigar los altos índices de reprobación y deserción en asignaturas filtro críticas (*Cálculo I/II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*) de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

**Estado actual:** Fase de análisis — desarrollo del SAD. El SRS FD03 v2.0 es la fuente de nomenclatura; el SAD v1.1 analiza la arquitectura propuesta y su trazabilidad. La maqueta frontend usa datos simulados; backend, persistencia y despliegue siguen como propuestas para fases posteriores.

### Pilares Funcionales y Tecnológicos
1. **Recomendación personalizada:** RF06 y CUS02 analizan afinidad temática, disponibilidad y criterios de RN-11; RF24 incorpora prioridad institucional.
2. **Reserva, confirmación y quórum:** RF12–RF16 distinguen reserva provisional (CUS04), ratificación (CUS24), corte T−24 h (CUS23) y decisión del mentor ante quórum insuficiente (CUS07).
3. **Asistencia y bitácora:** RF17 y CUS08 permiten registrar asistencia y cerrar la sesión. El QR es una alternativa de marcado por el mentor, cuya política técnica queda pendiente de diseño.
4. **Auditoría y certificación:** CUS22 visa horas antes de la emisión CUS13 y descarga CUS09, conforme a RN-14; se propone PDF, correlativo, hash de integridad y consulta institucional.
5. **Acceso y privacidad:** RF01–RF02 y RNF01–RNF02 exigen OTP institucional, consentimiento y protección de datos. Su cumplimiento deberá verificarse al implementar la solución.

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
| **Matriz de Inconsistencias** | [`docs/matriz_inconsistencias.md`](docs/matriz_inconsistencias.md) | Registro de auditoría y resolución de discrepancias en requisitos y modelos. |
| **Catálogo de Pruebas** | [`docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) | Matriz formal de casos de prueba funcional, criterios de aceptación y verificación QA. |
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
├── docs/                                      # Acervo documental formal de ingeniería de software
│   ├── FD01-EPIS-Informe de Factibilidad.md  # Viabilidad operativa, técnica, económica y legal
│   ├── FD01-EPIS-Informe de Factibilidad.pdf # Versión compilada para revisión académica
│   ├── FD02-EPIS-Informe Vision de Proyecto.md # Visión, actores, posicionamiento y alcance
│   ├── FD02-EPIS-Informe Vision de Proyecto.pdf # Versión compilada para revisión directiva
│   ├── FD03-EPIS-Informe SRS de Proyecto.md  # Especificación formal de requisitos (SRS canónico IEEE 830)
│   ├── FD04-EPIS-Informe SAD de Proyecto.md  # Documento formal de arquitectura de software (Modelo 4+1)
│   ├── resumen_sistema_y_casos_de_uso.md     # Síntesis ejecutiva, flujo macro, matriz CUS y reglas de negocio
│   ├── diagramas_general.md                  # Bóveda consolidada y de hardening de diagramas PlantUML
│   ├── diagramas_secuencia_pruebas.md        # Diagramas de secuencia en lenguaje de análisis (ECB)
│   ├── matriz_inconsistencias.md             # Matriz de consistencia metodológica de análisis
│   ├── Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx # Catálogo de pruebas funcionales y de aceptación
│   ├── Requerimientos.md                     # Cuaderno de trabajo preliminar de requerimientos
│   ├── diagramas_de_secuencia.md             # Diagramas de secuencia en fase de análisis (SAD / ECB)
│   └── diseño.md                             # Guía preliminar de interfaz y estilos
├── frontend/                                  # Maqueta funcional SPA interactiva (React + Vite)
│   ├── src/
│   │   ├── components/                        # Componentes UI modulares
│   │   │   ├── BookingView.tsx                # Interfaz de reserva y selección de horarios
│   │   │   ├── ConsentModal.tsx               # Modal de consentimiento informado (Ley N° 29733)
│   │   │   ├── GamificationView.tsx           # Tablero de medallas, nivel y horas de servicio
│   │   │   ├── HomeView.tsx                   # Catálogo reactivo y buscador de mentorías
│   │   │   ├── ImageCarousel.tsx              # Banner institucional rotativo
│   │   │   ├── LateralDocks.tsx               # Barra lateral de accesos rápidos
│   │   │   ├── Navigation.tsx                 # Barra superior de navegación institucional
│   │   │   └── RecommendationView.tsx         # Vista de recomendaciones Top-k con badges
│   │   ├── data/
│   │   │   └── mockData.ts                    # Dataset simulado con cursos de la EPIS y métricas
│   │   ├── App.tsx                            # Orquestador de vistas y estado del cliente
│   │   ├── index.css                          # Estilos globales de la maqueta
│   │   └── main.tsx                           # Punto de entrada de la aplicación React
│   ├── public/                                # Recursos estáticos y vectoriales
│   ├── package.json                           # Manifiesto de dependencias y scripts de frontend
│   ├── tsconfig.json                          # Configuración de compilación TypeScript
│   └── vite.config.ts                         # Configuración del bundler Vite
├── reglas_documentacion.md                    # Manual de normas de documentación y hardening (v1.3)
├── rules_doc.md                               # Registro histórico de directrices iniciales
├── .gitignore                                 # Reglas de exclusión de git
└── README.md                                  # Mapa central de navegación del proyecto (este archivo)
```

---

## 🚀 5. Instalación y Ejecución de la Maqueta Web

### Requisitos Previos
- **Node.js:** Versión 18.0 o superior (recomendado Node.js 20 LTS).
- **npm:** Gestor de paquetes incluido con Node.js.
- **Git:** Para control de versiones.

### Pasos de Despliegue Local
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/JMedina255/sistema_web_p2p.git
   cd sistema_web_p2p
   ```

2. **Acceder al directorio del frontend e instalar dependencias:**
   ```bash
   cd frontend
   npm install
   ```

3. **Iniciar el servidor de desarrollo local:**
   ```bash
   npm run dev
   ```

4. **Acceder a la aplicación:**
   Abre tu navegador web en [http://localhost:5173](http://localhost:5173).

5. **Compilar para producción:**
   ```bash
   npm run build
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
