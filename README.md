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

### Pilares Funcionales y Tecnológicos
1. **Motor de Recomendación Adaptativo *Top-k*:** Emparejamiento híbrido basado en afinidad temática (similitud coseno en espacios vectoriales curriculares), compatibilidad horaria y reputación docente histórica (`RN-06`).
2. **Corte Perentorio y Gobernanza de Quórum en $T-24\text{ h}$:** Regla de negocio automatizada (`RN-08`/`RN-09`) que exige a los estudiantes ratificar asistencia antes de las 24 horas del inicio; si el aforo confirmado es menor al 50%, se activa la gestión de contingencia (`CUS07`, `RN-10`) liberando recursos de aulas físicas y salas virtuales.
3. **Trazabilidad y Validación en Aula:** Registro de asistencia mediante códigos QR criptográficamente dinámicos con vigencia de 60 segundos (`RNF04`, `CUS11`) y rendición de bitácoras docentes obligatorias dentro de las 24 horas post-sesión (`RN-12`, `CUS10`).
4. **Fe Pública y Certificación Digital:** Fiscalización y visado de horas académicas por el Comité de Tutoría (`CUS22`, `RN-14`) para la emisión de certificados oficiales foliados con firma digital, hash SHA-256 y validación pública vía QR (`CUS13`/`CUS09`).
5. **Cumplimiento Legal y Privacidad:** Consentimiento informado digital expreso y disociación de identidad mediante hashes irreversibles para encuestas y analíticas de acuerdo a la **Ley N° 29733 (Ley de Protección de Datos Personales del Perú)** y el Art. 40 de la **Ley Universitaria N° 30220**.

---

## 📚 2. Mapa de Documentación Oficial de Ingeniería de Software

Toda la documentación técnica del ciclo de vida del software se encuentra estandarizada, sincronizada y auditada bajo la metodología UWE (UML-based Web Engineering) y el estándar IEEE 830:

| Entregable / Documento | Ubicación | Descripción y Alcance Metodológico |
| :--- | :--- | :--- |
| **Resumen Ejecutivo del Sistema** | [`docs/resumen_sistema_y_casos_de_uso.md`](docs/resumen_sistema_y_casos_de_uso.md) | **Lectura recomendada:** Visión concisa, flujo macro de 5 fases, matriz de 17 CUS críticos, relaciones de precedencia, máquinas de estado y síntesis de reglas de negocio. |
| **FD01: Informe de Factibilidad** | [`docs/FD01-EPIS-Informe de Factibilidad.md`](docs/FD01-EPIS-Informe%20de%20Factibilidad.md) | Evaluación exhaustiva de viabilidad operativa, técnica, económica y legal en el ámbito universitario de la UPT. |
| **FD02: Informe Visión del Proyecto** | [`docs/FD02-EPIS-Informe Vision de Proyecto.md`](docs/FD02-EPIS-Informe%20Vision%20de%20Proyecto.md) | Oportunidades de negocio, definición de stakeholders, posicionamiento del producto y características principales. |
| **FD03: Informe SRS de Proyecto** | [`docs/FD03-EPIS-Informe SRS de Proyecto.md`](docs/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md) | **Especificación de Requisitos de Software canónica:** Catálogo de 24 CUS, modelos ECB, diagramas de actividades con objetos, diagramas de secuencia y clases parciales. |
| **FD04: Informe SAD de Proyecto** | [`docs/FD04-EPIS-Informe SAD de Proyecto.md`](docs/FD04-EPIS-Informe%20SAD%20de%20Proyecto.md) | **Documento de Arquitectura de Software:** Representación 4+1 Vistas, objetivos ISO/IEC 25010, análisis de requerimientos y modelado técnico integral. |
| **Bóveda General de Diagramas** | [`docs/diagramas_general.md`](docs/diagramas_general.md) | **Hardening visual:** Bóveda sincronizada en espejo con más de 70 diagramas PlantUML rigurosamente estandarizados. |
| **Diagramas de Secuencia (Pruebas)** | [`docs/diagramas_secuencia_pruebas.md`](docs/diagramas_secuencia_pruebas.md) | **Entorno de pruebas de análisis:** Diagramas de secuencia en lenguaje conceptual ECB para los 4 casos de uso núcleo (CUS06, CUS07, CUS23, CUS13). |
| **Matriz de Inconsistencias** | [`docs/matriz_inconsistencias.md`](docs/matriz_inconsistencias.md) | Registro de auditoría y resolución de discrepancias en requisitos y modelos. |
| **Catálogo de Pruebas** | [`docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx`](docs/Catalogo_Pruebas_P2P_Mentorias_EPIS.xlsx) | Matriz formal de casos de prueba funcional, criterios de aceptación y verificación QA. |
| **Reglas de Documentación (Hardening)** | [`reglas_documentacion.md`](reglas_documentacion.md) | Estándares obligatorios de granularidad en análisis, estructura quíntuple de tablas, estándar PlantUML y reglas de sincronización. |

---

## 🏛️ 3. Módulos Funcionales del Sistema

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ECOSISTEMA P2P - EPIS UPT (2026)                    │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│    MOD-01    │             │    MOD-02    │             │    MOD-03    │
│ Autenticación│             │ Recomendación│             │ Oferta y     │
│ 2FA / RLS    │             │ Top-k Híbrido│             │ Demanda P2P  │
└──────┬───────┘             └──────┬───────┘             └──────┬───────┘
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│    MOD-04    │             │    MOD-05    │             │    MOD-06    │
│ Reservas y   │             │ Asistencia QR│             │ Calidad CSAT │
│ Quórum T-24h │             │ y Bitácoras  │             │ e Insignias  │
└──────┬───────┘             └──────┬───────┘             └──────┬───────┘
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
              ┌──────────────┐            ┌──────────────┐
              │    MOD-07    │            │    MOD-08    │
              │ Certificación│            │ Auditoría y  │
              │ SHA-256 + QR │            │ Analítica    │
              └──────────────┘            └──────────────┘
```

- **MOD-01 (Seguridad y Perfiles):** Autenticación OAuth 2.0 institucional con 2FA TOTP, perfiles diferenciados y control de acceso RLS.
- **MOD-02 (Motor de Recomendación):** Generación de ranking personalizado *Top-k* con bonificación por cursos críticos (`RN-11`).
- **MOD-03 (Oferta y Demanda):** Publicación de franjas horarias y solicitudes temáticas estudiantiles por demanda insatisfecha.
- **MOD-04 (Reserva y Quórum):** Bloqueo provisional, ratificación perentoria en $T-24\text{ h}$ y corte automático de aforo al 50%.
- **MOD-05 (Asistencia y Bitácora):** Emisión y escaneo de códigos QR dinámicos en aula, y redacción de bitácoras docentes (< 24h).
- **MOD-06 (Calidad y Gamificación):** Encuestas de satisfacción CSAT bajo anonimato y acreditación de medallas e insignias formativas.
- **MOD-07 (Certificación Digital):** Generación de constancias foliadas con código hash SHA-256, validador público y conteo de horas.
- **MOD-08 (Auditoría y Analítica):** Panel directivo para visado de bitácoras por el Comité de Tutoría e inteligencia de retención académica.

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
│   ├── diagramas_de_secuencia.md             # Apunte preliminar de secuencias
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
│   │   ├── index.css                          # Estilos globales y utilidades Tailwind CSS
│   │   └── main.tsx                           # Punto de entrada de la aplicación React
│   ├── public/                                # Recursos estáticos y vectoriales
│   ├── package.json                           # Manifiesto de dependencias y scripts de frontend
│   ├── tsconfig.json                          # Configuración de compilación TypeScript
│   └── vite.config.ts                         # Configuración del bundler Vite
├── reglas_documentacion.md                    # Manual de normas de documentación y hardening (v1.2)
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
- **Regla 1:** Granularidad obligatoria en lenguaje natural formal en fase de análisis.
- **Regla 2:** Estructura quíntuple estándar en toda tabla (Presentación → Título → Tabla MD → Fuente → Análisis/Conclusión).
- **Regla 3:** Uso exclusivo de diagramas PlantUML limpios, ejecutables y mantenibles.
- **Regla 4:** Codificación UTF-8 estricta en archivos Markdown.
- **Regla 5:** Hardening continuo y sincronización inmediata con [`docs/diagramas_general.md`](docs/diagramas_general.md).
- **Regla 6:** Estructura canónica de 4 tablas para las narrativas de casos de uso (Ficha, Flujo Principal, Alternativos, Excepciones).
- **Regla 7:** Sincronización y actualización continua del archivo [`README.md`](README.md) ante cualquier evolución de ingeniería.

---

## ⚖️ 7. Marco Legal y Ético

El desarrollo de este sistema cumple de forma estricta con:
- **Ley N° 29733 (Ley de Protección de Datos Personales del Perú):** Principio de consentimiento previo, expreso e informado; derecho de revocación; disociación irreversible de identidad mediante hashes criptográficos en métricas de satisfacción y datasets analíticos.
- **Ley Universitaria N° 30220 (Art. 40 - Tutoría y Consejería):** Reconocimiento formal de la mentoría académica entre pares como actividad formativa y solidaria computable para la convalidación de horas de servicio estudiantil ante la Dirección de Escuela de la EPIS-UPT.

---
*Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna — 2026*
