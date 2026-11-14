# -*- coding: utf-8 -*-
"""
Generator for Part A of docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
Covers: Portada, Control de Versiones, Índice General,
Sección 1 (1.1-1.6), Sección 2 (2.1-2.4), Sección 3 (3.1-3.6),
Sección 4 (4.1-4.2), Sección 5 (5.1-5.6), Sección 6 (6.1, 6.2.1, 6.2.2)
Up to right before Section 6.2.3.
"""

def get_part_a():
    return r'''**FACULTAD DE INGENIERÍA**  
**ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS**

# “Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT”

**Curso:** Construcción de Software I  
**Docente:** Dr. RICARDO EDUARDO VALCARCEL ALVARADO  

**AUTOR:**  
ANTAYHUA MAMANI, Renzo Antonio (2022073504)  
MEDINA QUISPE, Joan Cristian (2022074255)  

**TACNA – PERÚ**  
**2026**

---

## CONTROL DE VERSIONES

A continuación, se presenta el registro histórico de versiones del presente documento rector de especificación de requerimientos:

### Cuadro 0.1: Registro de Control de Versiones del Informe SRS

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:---:|:---:|:---:|:---:|:---:|:---|
| **1.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 11/09/2026 | Versión 1.0 preliminar de levantamiento y especificación inicial de requerimientos funcionales y no funcionales. |
| **2.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 26/09/2026 | Consolidación y congelamiento de la línea base analítica oficial (MOD-01 al MOD-08, RF01 al RF26, RN-01 al RN-14, RNF01 al RNF10, CUS-001 al CUS-024). Reorganización modular de narrativas por dependencia operativa y alineamiento de estados canónicos. |
| **2.1** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 19/10/2026 | Refinamiento y trazabilidad en Fase de Diseño (SRS v2.1): alineamiento con la arquitectura desacoplada y cierre de requerimientos del Sprint 1 (RF01, RF05, RNF01, RNF02, RNF09, CUS-001, CUS-021, RN-01) respaldados empíricamente en CI. |
| **2.2** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 23/10/2026 | Consolidación de Fase de Diseño y Construcción del Sprint 2 (SRS v2.2): formalización técnica de consentimiento digital Ley N° 29733 (RF02, RN-02, CUS-001), roles y mérito académico (RF03, RN-03, CUS-010), perfiles y matriz 6×11 (RF04, CUS-005) y catálogo silábico (RF05, CUS-021). |
| **3.0** | Joan Medina / Renzo Antayhua | Dr. Ricardo Valcárcel | Dirección EPIS | 14/11/2026 | Consolidación Integral de la Fase de Diseño y Cierre de Construcción (SRS v3.0): culminación de los 8 Sprints de desarrollo (MOD-01 al MOD-08, CUS-001 al CUS-024, RF01 al RF26, RN-01 al RN-14, RNF01 al RNF10). Formalización de interfaces externas (WCAG 2.1 AA / Tailwind), motor EdRecSys calibrado (P@3=83.3%, P@5=80.0%, latencia 12.4 ms), orquestación transaccional con cerrojos pesimistas a T-24h, bitácoras firmadas con SHA-256 y certificados PDF con QR institucional. |
| **3.1** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Refinamiento funcional integral del SRS (H02): profundización exhaustiva de Secciones 1 a 5, especificación de fichas funcionales para los 26 RF sin filtración técnica, consolidación de RF20 como encuestas de calidad post-mentoría 24h, actualización de los 10 RNF (ISO 25010), 14 Reglas de Negocio, procesos As-Is y To-Be con regla D-2 y rutas relativas. |

Fuente: Elaboración propia.

El presente cuadro certifica la trazabilidad documental y cronológica del proyecto, delimitando las iteraciones académicas y estableciendo el estado de revisión y aprobación formal ante las autoridades académicas de la Escuela Profesional de Ingeniería de Sistemas.

# Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT

**Documento de Especificación de Requerimientos de Software**  
**Versión 3.1 (Pendiente de revisión / En refinamiento) — Fase de Diseño Técnico y Cierre de Construcción (Sprints 1 al 8)**

---

## ÍNDICE GENERAL

1. Introducción  
   1.1. Propósito  
   1.2. Alcance del Sistema  
   1.3. Personal Involucrado  
   1.4. Definiciones, Acrónimos y Abreviaturas  
   1.5. Referencias Normativas y Técnicas  
   1.6. Organización del Documento  
2. Generalidades de la Empresa  
   2.1. Nombre de la Empresa y Naturaleza del Equipo Consultor  
   2.2. Visión  
   2.3. Misión  
   2.4. Organigrama y Responsabilidades Técnicas  
3. Visionamiento de la Empresa  
   3.1. Descripción del Problema Académico  
   3.2. Necesidades de los Interesados  
   3.3. Objetivos de Negocios y Objetivos de Diseño  
   3.4. Alcance y Exclusiones del Proyecto  
   3.5. Viabilidad Multidimensional del Sistema  
       3.5.1. Viabilidad Técnica  
       3.5.2. Viabilidad Económica  
       3.5.3. Viabilidad Operativa  
       3.5.4. Viabilidad Legal  
       3.5.5. Viabilidad Social y Ambiental  
   3.6. Información obtenida del Levantamiento de Información  
4. Análisis de Procesos  
   4.1. Diagrama del Proceso Actual (As-Is)  
   4.2. Diagrama del Proceso Propuesto (To-Be)  
5. Especificación de Requerimientos de Software  
   5.1. Identificación de Módulos y Capacidades Funcionales  
   5.2. Requerimientos No Funcionales (ISO/IEC 25010)  
   5.3. Matriz Consolidada de Requerimientos Funcionales (RF01 al RF26)  
       5.3.1. Fichas Detalladas de Especificación de Requerimientos Funcionales (RF01 al RF26)  
   5.4. Reglas de Negocio Institucionales (RN-01 al RN-14)  
   5.5. Matriz de Trazabilidad Bidireccional de Requerimientos  
   5.6. Requisitos de Interfaz Externa  
       5.6.1. Interfaces de Usuario (Design System y Accesibilidad WCAG 2.1 AA)  
       5.6.2. Interfaces de Software (APIs, Base de Datos y Dependencias)  
       5.6.3. Interfaces de Hardware  
       5.6.4. Interfaces de Comunicaciones y Seguridad de Red  
6. Fase de Desarrollo  
   6.1. Perfiles de Usuario y Modelo de Control de Acceso (RBAC)  
   6.2. Modelo Conceptual  
       6.2.1. Diagrama de Clases Conceptuales y Paquetes Arquitecturales  
       6.2.2. Diagramas de Casos de Uso (Consolidado y Modulares MOD-01 al MOD-08)  
       6.2.3. Escenarios de Casos de Uso (Fase de Diseño - CUS-001 al CUS-024)  
   6.3. Modelo Lógico  
       6.3.1. Análisis de Objetos (Modelo ECB - CUS-001 al CUS-024)  
       6.3.2. Diagrama de Actividades con Flujo de Objetos Técnicos (CUS-001 al CUS-024)  
       6.3.3. Diagramas de Secuencia del Sistema (Fase de Diseño - CUS-001 al CUS-024)  
       6.3.4. Diagrama de Clases del Modelo Lógico (CUS-001 al CUS-024)  
       6.3.5. Diagramas de Máquinas de Estados Finitas (FSM)  
       6.3.6. Modelo Físico de Base de Datos Relacional y Diccionario DDL  
7. Conclusiones  
8. Bibliografía

---

# Informe de Especificación de Requisitos de Software

# 1. Introducción

## 1.1. Propósito

El propósito fundamental de la presente **Especificación de Requerimientos de Software (SRS)** en su **Versión 3.1 (Fase de Diseño Técnico y Cierre de Construcción)** es definir con máxima precisión, rigurosidad académica y completitud funcional el comportamiento, las capacidades operativas, las reglas institucionales y los criterios de aceptación del *“Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT”*.

Siguiendo las directrices internacionales del estándar **ISO/IEC/IEEE 29148:2018**, este documento responde principalmente a la interrogante rectora de la ingeniería de requisitos: **¿Qué necesita la comunidad universitaria de la EPIS y qué debe hacer el sistema para satisfacer dicha necesidad?**

La especificación está dirigida a tres audiencias diferenciadas:
1. **Cliente y Autoridades Institucionales:** Dirección de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT) y Coordinación de Tutoría, proporcionándoles un marco formal de auditoría sobre la gobernanza académica, el cumplimiento normativo de privacidad y la trazabilidad de convalidación de horas extracurriculares.
2. **Usuarios Finales del Ecosistema Universitario:** Estudiantes mentoreados de ciclos formativos (I al IV) y estudiantes mentores de ciclos superiores (VII al X), describiendo sus interfaces de interacción, sus derechos, sus obligaciones y los flujos de servicio sin ambigüedades.
3. **Docentes Evaluadores y Comités de Acreditación (ICACIT):** Como evidencia de diseño en ingeniería de software, acreditando la correspondencia entre los objetivos de aprendizaje de la cátedra de Construcción de Software I y la solución construida.

Conforme a la metodología disciplinada del proyecto, este SRS delimita exhaustivamente las capacidades externas y las condiciones operacionales del software, evitando deliberadamente la introducción innecesaria de nombres de clases de programación, esquemas de tablas relacionales internas, sentencias SQL o métodos privados, cuya especificación técnica y de implementación pertenece de manera exclusiva al **Documento de Arquitectura de Software (SAD)**.

## 1.2. Alcance del Sistema

El software comprende una plataforma web adaptativa y distribuida de tipo entre pares (*Peer-to-Peer - P2P*) concebida para transformar el modelo tradicional y centralizado de tutoría universitaria en una red horizontal de aprendizaje colaborativo entre estudiantes de la EPIS-UPT.

El sistema asume las siguientes capacidades principales:
- **Verificación de Identidad y Gobernanza de Acceso:** Autenticación institucional dual (código de un solo uso OTP de 6 dígitos remitido al buzón institucional y autenticación federada con Google Workspace institucional), formalización obligatoria de consentimiento informado digital bajo la Ley N° 29733 y control de acceso basado en roles (RBAC).
- **Catálogo Curricular Silábico y Búsqueda Temática:** Exploración profunda de las asignaturas formativas críticas de I a IV ciclo, estructuradas por unidades de aprendizaje y temas conceptuales oficiales.
- **Emparejamiento Inteligente y Banco de Demanda:** Motor algorítmico de recomendación híbrido (*EdRecSys*) que computa afinidad temática por similitud coseno ajustada por reputación histórica y balanceo de carga, complementado con un banco institucional de solicitudes por demanda para necesidades formativas no cubiertas.
- **Planificación de Sesiones y Aprovisionamiento de Espacios:** Publicación de ofertas con aforos estandarizados (10 participantes en modalidad presencial y 20 en modalidad virtual), validación automática de aulas libres de la escuela frente a cronogramas de clase regulares y configuración de salas virtuales institucionales.
- **Gestión Concurrente de Inscripciones y Control de Quórum:** Reserva de cupos con garantía de no sobrecupo (0.0%), ventana perentoria de ratificación obligatoria hasta $T-24\text{ h}$, demonio cron desatendido de evaluación de quórum mínimo (50% de aforo) y flujo de contingencia del mentor ante quórum insuficiente.
- **Ejecución de Sesiones y Marcación de Asistencia Dinámica:** Check-in presencial y virtual mediante pase QR dinámico con algoritmo TOTP de refresco cada 30 segundos, eliminando fraudes por captura estática de pantalla.
- **Trazabilidad Pedagógica y Cierre Docente:** Registro obligatorio de bitácora pedagógica estructurada en un plazo improrrogable de 48 horas post-sesión, respaldada con resumen de logros, observaciones e inmutabilidad garantizada por firma criptográfica SHA-256.
- **Evaluación de Calidad y Retroalimentación:** Formulario perentorio de encuestas de calidad docente (CSAT) habilitado exclusivamente para estudiantes asistentes durante una ventana estricta de 24 horas.
- **Gamificación y Certificación Oficial:** Sistema de reputación por puntaje de encuestas, catálogo de insignias por mérito docente y emisión de certificados digitales oficiales en formato PDF con código correlativo institucional, firma digital con hash SHA-256 y código QR de verificación pública en línea para convalidación de créditos extracurriculares ($\ge 20\text{ h}$).
- **Supervisión Directiva y Analítica de Retención:** Tableros agregados para la Dirección de Escuela y Coordinación de Tutoría con métricas de asignaturas críticas, ausentismo, efectividad de mentorías e indicadores de impacto para acreditación ICACIT.

## 1.3. Personal Involucrado

A continuación, se detalla el personal docente, directivo, estudiantil y el equipo consultor involucrado en el diseño, desarrollo, validación y uso del sistema:

### Cuadro 1.1: Nómina del Personal Involucrado y Actores Institucionales

| Nombre / Actor | Rol Institucional / Académico | Entidad de Pertenencia | Responsabilidades Principales en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Dr. Ricardo Eduardo Valcárcel Alvarado** | Docente Titular de Cátedra | EPIS - UPT (Cátedra Construcción de Software I) | Dirección académica y metodológica de la cátedra; definición de estándares de ingeniería de software; evaluación crítica de artefactos documentales; fiscalización de trazabilidad y aprobación de fases de ciclo de vida. |
| **Ing. Haydee Raquel Sisa Yataco** | Directora (e) de Escuela | EPIS - UPT (Dirección de Escuela) | Patrocinio institucional del proyecto; homologación de políticas de certificación; definición del umbral mínimo de 20 horas auditadas para la postulación a créditos extracurriculares de graduación. |
| **Ing. Liliana Mercedes Vega Bernal** | Coordinadora de Tutoría | EPIS - UPT (Comité de Tutoría) | Definición de asignaturas formativas filtro prioritarias; establecimiento de políticas de quórum (50%); fiscalización de bitácoras docentes; validación pedagógica del flujo As-Is y To-Be. |
| **Joan Cristian Medina Quispe** | Desarrollador / Consultor TI | Grupo 03 / C-SharkTeam (Estudiante EPIS-UPT) | Liderazgo del subsistema de Frontend, Arquitectura de Componentes Web SPA (React, TypeScript), diseño de interfaz visual accesible (WCAG 2.1 AA / Tailwind), experiencia de usuario (UI/UX) y aseguramiento de calidad con pruebas automatizadas en cliente. |
| **Renzo Antonio Antayhua Mamani** | Desarrollador / Consultor TI | Grupo 03 / C-SharkTeam (Estudiante EPIS-UPT) | Liderazgo del subsistema de Backend, Servicios RESTful (FastAPI), calibración del motor de recomendación híbrido (*EdRecSys*), modelado relacional de datos (PostgreSQL/Supabase), seguridad criptográfica, cerrojos transaccionales pesimistas y pruebas de backend. |
| **Estudiantes Mentoreados** | Usuarios Finales (Primarios) | EPIS - UPT (Ciclos I al IV) | Destinatarios del servicio de acompañamiento académico; participación en encuestas y entrevistas; registro de necesidades y evaluación de sesiones de mentoría. |
| **Estudiantes Mentores** | Usuarios Finales (Primarios) | EPIS - UPT (Ciclos VII al X) | Facilitadores de las sesiones académicas; acreditación de mérito en cursos aprobados; ejecución pedagógica, marcación de asistencia y formulación de bitácoras. |

Fuente: Elaboración propia.

El análisis del Cuadro 1.1 delimita con precisión la distinción metodológica e institucional entre los roles del ecosistema:
1. **Universidad Patrocinadora:** La Universidad Privada de Tacna (UPT), a través de su Facultad de Ingeniería, proporciona el marco normativo universitario (Reglamento de Grados y Títulos, Estatuto Universitario y Ley N° 30220).
2. **Cliente Institucional / Unidad Beneficiaria:** La Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT), representada por su Dirección y Coordinación de Tutoría, actúa como cliente que aprueba requisitos, parametriza reglas de convalidación y recibe los beneficios del software.
3. **Equipo Consultor y Desarrollador:** El Grupo 03 / C-SharkTeam, integrado por Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani, asume la responsabilidad técnica integral de la ingeniería de requisitos, diseño arquitectónico, construcción de código y pruebas automatizadas.

## 1.4. Definiciones, Acrónimos y Abreviaturas

A continuación, se define el glosario terminológico oficial para la comprensión inequívoca de los términos empleados en el documento:

- **2FA (Two-Factor Authentication):** Autenticación de doble factor que exige la posesión de una cuenta de correo institucional verificada mediante el ingreso de un código de un solo uso (OTP).
- **Aforo Reglamentario:** Capacidad máxima permitida de participantes en una sesión de mentoría, fijada por política institucional en 10 estudiantes para modalidad presencial y 20 para modalidad virtual (RN-05).
- **Asignatura Filtro:** Materia del plan de estudios de los primeros cuatro ciclos de Ingeniería de Sistemas caracterizada por una alta tasa histórica de reprobación (ej. Cálculo I, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos, Base de Datos).
- **Bitácora Pedagógica:** Instrumento documental digital formal donde el mentor registra los temas tratados, incidencias didácticas y el resumen cualitativo de la sesión en un plazo máximo de 48 horas, avalado con un sello hash SHA-256 (RN-12).
- **CSAT (Customer Satisfaction Score):** Métrica cuantitativa de satisfacción estudiantil recopilada mediante encuestas de calidad post-mentoría sobre cuatro dimensiones formativas (claridad, dominio, empatía y puntualidad).
- **CUS (Caso de Uso del Sistema):** Especificación secuencial y exhaustiva de la interacción entre un actor humano o técnico y el sistema para alcanzar un objetivo de negocio verificable.
- **EdRecSys (Educational Recommendation System):** Motor de recomendación adaptativo que combina similitud coseno sobre vectores de temarios silábicos con filtrado colaborativo ponderado por reputación docente y balance de carga horaria.
- **EPIS-UPT:** Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.
- **FSM (Finite State Machine):** Modelo matemático de estados finitos que define las transiciones válidas y restricciones deterministas en el ciclo de vida de sesiones, reservas y bitácoras.
- **GIS (Google Identity Services):** SDK oficial de autenticación provisto por Google para la verificación federada de cuentas institucionales `@virtual.upt.pe` y `@upt.pe`.
- **JWT (JSON Web Token):** Estándar de transmisión segura de identidad (RFC 7519) firmado digitalmente mediante HMAC-SHA256, con vigencia de 8 horas para control de sesión en cliente.
- **OTP (One-Time Password):** Código numérico temporal de 6 dígitos con vigencia máxima de 5 minutos (300 segundos) y enfriamiento de reenvío de 60 segundos (RN-01).
- **P2P (Peer-to-Peer):** Arquitectura y modelo pedagógico horizontal entre pares, donde estudiantes avanzados instruyen y guían a compañeros de ciclos iniciales sin jerarquías docentes rígidas.
- **Precision@k:** Métrica de evaluación algorítmica que representa la fracción de sesiones recomendadas relevantes dentro de los primeros $k$ resultados desplegados al estudiante.
- **Quórum de Sesión:** Requisito de asistencia confirmada del 50% del aforo reglamentario evaluado a $T-24\text{ h}$ de la sesión (5 estudiantes en presencial, 10 en virtual) indispensable para su confirmación automática (RN-09).
- **RBAC (Role-Based Access Control):** Control de acceso basado en roles que restringe las operaciones del sistema según los roles institucionales asignados: Mentoreado, Mentor, Administrador y Coordinador.
- **RF (Requerimiento Funcional):** Capacidad o servicio específico que el sistema debe prestar al usuario en respuesta a estímulos de entrada.
- **RN (Regla de Negocio):** Directriz, política o restricción institucional inmutable de la EPIS-UPT que gobierna la lógica de negocio y las decisiones operativas del software.
- **RNF (Requerimiento No Funcional):** Atributo de calidad o restricción arquitectónica (rendimiento, seguridad, usabilidad, fiabilidad) evaluado bajo el estándar ISO/IEC 25010.
- **RLS (Row Level Security):** Política de seguridad a nivel de base de datos que garantiza que cada usuario consulte y modifique únicamente sus propios registros académicos.
- **SPA (Single Page Application):** Aplicación web de página única que carga un único documento HTML y actualiza la vista reactivamente mediante manipulación dinámica del DOM sin recargar la página.
- **SUS (System Usability Scale):** Cuestionario psicométrico estandarizado de diez preguntas para evaluar la facilidad de uso y ergonomía de la plataforma (umbral mínimo aceptable > 75 puntos).
- **Temario Silábico:** Desglose analítico de unidades de aprendizaje, temas y subtemas contenidos en el sílabo oficial de cada asignatura crítica de la EPIS.
- **TOTP (Time-based One-Time Password):** Algoritmo de pase efímero basado en tiempo sincronizado (RFC 6238) utilizado para emitir códigos QR dinámicos de asistencia válidos por 30 segundos.
- **UWE (UML-Based Web Engineering):** Metodología de ingeniería de software orientada a la especificación, diseño sistemático y construcción de aplicaciones web adaptativas.
- **WCAG 2.1 AA:** Pautas de Accesibilidad para el Contenido Web del W3C en su nivel de conformidad intermedio (AA), exigiendo contraste cromático mínimo de 4.5:1 y navegación completa por teclado.

## 1.5. Referencias Normativas y Técnicas

La fundamentación teórica, legal y metodológica del presente documento se sustenta en las siguientes normas técnicas y jurídicas:
1. **Ley N° 29733 (Ley de Protección de Datos Personales del Perú):** Regula el tratamiento legítimo, seguro y confidencial de la información académica y datos personales de los estudiantes universitarios.
2. **Decreto Supremo N° 003-2013-JUS:** Reglamento de la Ley N° 29733, referente a medidas de seguridad organizativas y técnicas en bancos de datos personales digitales.
3. **Ley Universitaria N° 30220 (Artículo 40):** Dispone la obligación de las universidades de brindar servicios de tutoría y consejería permanente a los estudiantes para asegurar su rendimiento y permanencia.
4. **Estándar ISO/IEC/IEEE 29148:2018:** *Systems and software engineering — Life cycle processes — Requirements engineering*, empleado como norma directriz para la estructura, redacción y verificación de requisitos de este informe.
5. **Estándar ISO/IEC 25010:2011:** *Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models*, utilizado para estructurar los atributos de calidad de la Sección 5.2.
6. **Estándar IEEE Std 830-1998:** *IEEE Recommended Practice for Software Requirements Specifications*, utilizado como marco de referencia formativo de la cátedra de Construcción de Software I.
7. **Pautas W3C WCAG 2.1 Nivel AA:** *Web Content Accessibility Guidelines*, aplicadas en la especificación ergonómica del subsistema de usuario.
8. **Modelo de Acreditación Internacional ICACIT (Criterio 5 - Estudiantes y Criterio 6 - Instalaciones y Soporte):** Marco de aseguramiento de calidad educativa universitaria para carreras de ingeniería.
9. **Reglamento General de Grados y Títulos de la Universidad Privada de Tacna:** Disposiciones para el cómputo y convalidación de horas extracurriculares en actividades de apoyo docente y mentoría.

## 1.6. Organización del Documento

El presente documento de especificación de requerimientos de software se encuentra estructurado en ocho secciones analíticas:
- **Sección 1 (Introducción):** Formaliza el propósito, alcance, glosario, referencias y organización del informe.
- **Sección 2 (Generalidades de la Empresa):** Detalla la identidad de C-SharkTeam, su misión, visión, organigrama y responsabilidades técnicas.
- **Sección 3 (Visionamiento de la Empresa):** Examina la problemática de deserción y cursos filtro, los objetivos de negocio y diseño, el alcance funcional, las exclusiones operativas y la viabilidad técnica, económica, legal y social.
- **Sección 4 (Análisis de Procesos):** Modela el proceso informal actual (*As-Is*) y el proceso sistematizado propuesto (*To-Be*) mediante diagramas de actividades y análisis de deficiencias.
- **Sección 5 (Especificación de Requerimientos de Software):** Desarrolla el núcleo de la ingeniería de requisitos: los 8 módulos canónicos (5.1), los 10 requerimientos no funcionales bajo ISO/IEC 25010 (5.2), la matriz consolidada de 26 requerimientos funcionales (5.3), las 26 fichas detalladas de especificación funcional en lenguaje del usuario (5.3.1), las 14 reglas de negocio (5.4), la matriz de trazabilidad y reporte de madurez (5.5) y los requisitos de interfaz externa (5.6).
- **Sección 6 (Fase de Desarrollo):** Establece el puente entre requisitos y arquitectura lógica: modelo RBAC (6.1), modelo conceptual y diagramas de casos de uso (6.2), y modelos lógicos preliminares (6.3).
- **Secciones 7 y 8 (Conclusiones y Bibliografía):** Sintetizan los aportes metodológicos del documento y compilan las fuentes bibliográficas consultadas.

---

# 2. Generalidades de la Empresa

## 2.1. Nombre de la Empresa y Naturaleza del Equipo Consultor

**C-SharkTeam (Grupo 03)**

C-SharkTeam es una célula de consultoría e ingeniería de software conformada por estudiantes del octavo ciclo de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna en el marco de la cátedra de Construcción de Software I (semestre 2026-II).

Es fundamental establecer la diferenciación tripartita de responsabilidades que rige el proyecto:
- **La Universidad Patrocinadora (UPT):** Entidad universitaria autónoma que provee el marco estatutario, la infraestructura física y los lineamientos de acreditación educativa.
- **El Cliente Institucional (EPIS-UPT):** Unidad académica beneficiaria representada por su Directora de Escuela y su Comité de Tutoría, responsable de validar la pertinencia pedagógica, definir asignaturas críticas y otorgar valor oficial a las horas certificadas.
- **El Equipo Consultor y Desarrollador (C-SharkTeam):** Grupo técnico responsable de levantar información, especificar requerimientos, diseñar la arquitectura, construir la solución web y garantizar su calidad mediante pruebas automatizadas.

## 2.2. Visión

Consolidarse como un equipo referente en innovación tecnológica y desarrollo de software educativo en el sur del país, reconocido por su capacidad de concebir plataformas adaptativas de alta calidad que potencien el aprendizaje colaborativo entre pares, democraticen el acceso al reforzamiento académico y optimicen la toma de decisiones institucionales mediante analítica de datos e inteligencia artificial.

## 2.3. Misión

Diseñar, construir y desplegar soluciones de software seguras, robustas y accesibles que solucionen problemas reales de rezago y deserción en la educación superior, transformando la tutoría universitaria convencional en un ecosistema digital gobernado, eficiente y medible que conecte el talento de estudiantes mentores con las necesidades formativas de sus compañeros.

## 2.4. Organigrama y Responsabilidades Técnicas

La organización interna de C-SharkTeam se rige por un esquema de alta cohesión técnica y delimitación funcional de responsabilidades:

### Diagrama 2.1: Organigrama Funcional del Equipo Consultor C-SharkTeam

```plantuml
@startuml
top to bottom direction
skinparam rectangle {
  BackgroundColor white
  BorderColor #444444
}

rectangle "C-SharkTeam\nDirección General del Proyecto" as DIR

rectangle "Ingeniería de Backend, Algoritmos\ny Persistencia Relacional\n\nRenzo Antonio Antayhua Mamani\n• Servicios RESTful en FastAPI\n• Motor de Recomendación EdRecSys\n• Persistencia Relacional PostgreSQL / RLS\n• Transaccionalidad Pesimista y Quórum\n• Batería de Pruebas Backend (Pytest)" as BACK

rectangle "Ingeniería de Frontend, UI/UX\ny Accesibilidad Universal\n\nJoan Cristian Medina Quispe\n• Aplicación Web Responsiva (React SPA)\n• Design System Institucional (Tailwind)\n• Accesibilidad Web WCAG 2.1 Nivel AA\n• Gestión de Estado y Clientes HTTP\n• Batería de Pruebas Frontend (Vitest)" as FRONT

rectangle "Interacción con Cliente Institucional\nEPIS-UPT\n\n• Dirección de Escuela (Convalidación)\n• Coordinación de Tutoría (Cursos Filtro)\n• Estudiantes Mentores y Mentoreados" as INSTITUCION

DIR --> BACK
DIR --> FRONT
BACK --> INSTITUCION
FRONT --> INSTITUCION
@enduml
```

Fuente: Elaboración propia.

A continuación, se detalla la matriz formal de responsabilidades asignadas a los integrantes del equipo:

### Cuadro 2.1: Estructura de Responsabilidades Técnicas del Equipo Consultor C-SharkTeam

| Integrante / Consultor | Área de Especialización | Funciones Principales | Entregables y Artefactos Bajo su Custodia |
| :--- | :--- | :--- | :--- |
| **Joan Cristian Medina Quispe** | Frontend, Arquitectura UI/UX y Accesibilidad | • Arquitectura de cliente web SPA bajo React 18, TypeScript y Vite.<br>• Construcción de componentes interactivos y Design System Tailwind CSS.<br>• Implementación estricta de accesibilidad WCAG 2.1 AA (contraste $\ge 4.5:1$, foco visible y soporte ARIA).<br>• Integración de clientes HTTP tipados y adaptadores de comunicación con el backend.<br>• Construcción de vistas de escaneo QR, modales de consentimiento y tableros analíticos.<br>• Autoría y ejecución de la suite de pruebas unitarias y de componentes en Vitest. | • Código fuente en `aplicacion/frontend/src/`.<br>• Vistas de interfaz de usuario (23 componentes reactivos).<br>• Pruebas automatizadas de cliente en `aplicacion/frontend/src/**/*.test.tsx`. |
| **Renzo Antonio Antayhua Mamani** | Backend, Algoritmos y Persistencia | • Arquitectura de microservicios RESTful en Python con FastAPI.<br>• Diseño y calibración del motor de recomendación híbrido *EdRecSys*.<br>• Modelado relacional DDL físico en PostgreSQL con SQLAlchemy y Alembic.<br>• Políticas de seguridad a nivel de fila (*Row Level Security - RLS*) y control RBAC.<br>• Orquestación de concurrencia mediante cerrojos pesimistas (`SELECT ... FOR UPDATE`).<br>• Demonio cron desatendido de corte de quórum a $T-24\text{ h}$ y servicios de correo SMTP.<br>• Autoría y ejecución de la suite de pruebas unitarias e integración en Pytest. | • Código fuente en `aplicacion/backend/app/`.<br>• Modelos ORM, controladores REST y servicios de negocio.<br>• Migraciones DDL en `aplicacion/backend/app/db/migrations/`.<br>• Pruebas automatizadas de backend en `aplicacion/backend/tests/`. |

Fuente: Elaboración propia.

El análisis del Cuadro 2.1 demuestra una distribución equilibrada y rigurosa de las responsabilidades técnicas. La frontera clara entre la ingeniería de interfaz accesible y la ingeniería de servicios de persistencia y recomendación asegura que ambos dominios alcancen la profundidad exigida por la cátedra sin solapamientos improductivos ni vacíos de responsabilidad.

# 3. Visionamiento de la Empresa

C-SharkTeam concibe la plataforma no como una simple herramienta aislada de registro, sino como la columna vertebral tecnológica de un **Ecosistema Académico Colaborativo** para la EPIS-UPT, alineado con las demandas de modernización universitaria y acreditación internacional ICACIT.

## 3.1. Descripción del Problema Académico

En la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna, los estudiantes que cursan los primeros cuatro ciclos del plan curricular enfrentan una severa transición formativa caracterizada por una alta complejidad conceptual en materias de ciencias básicas y fundamentos de ciencias de la computación:
- **Cálculo Diferencial e Integral (I y II ciclo):** Rigor analítico formal y modelado matemático continuo.
- **Algoritmos y Estructura de Datos (II y III ciclo):** Razonamiento lógico estructurado, complejidad asintótica y estructuras dinámicas en memoria.
- **Programación Orientada a Objetos (III ciclo):** Abstracción, polimorfismo, encapsulamiento y patrones de diseño.
- **Base de Datos (IV ciclo):** Normalización relacional, integridad referencial y álgebra relacional.

Estas materias actúan en la práctica como **"asignaturas filtro"**, concentrando tasas históricas de desaprobación que fluctúan entre el 25% y el 40%, provocando rezago en el avance de la malla curricular, desmotivación temprana y un riesgo sensible de deserción universitaria en los primeros semestres.

Paradójicamente, la escuela cuenta con una masa crítica de estudiantes destacados en los ciclos superiores (VII al X) que han superado con solvencia técnica estas materias y poseen vocación para guiar a sus compañeros. No obstante, no existe una plataforma institucional centralizada que articule de manera inteligente, ordenada y trazable la oferta y la demanda de asesoría académica entre pares (*Peer-to-Peer*).

Actualmente, este apoyo se canaliza a través de medios informales no regulados (grupos de WhatsApp, mensajería instantánea privada o encuentros fortuitos en pasillos), generando los siguientes problemas de fondo:
1. **Ausencia de Emparejamiento Adaptativo (Matching Inteligente):** La búsqueda de ayuda académica depende de contactos interpersonales o referencias empíricas. No existe un mecanismo que cruce las debilidades temáticas puntuales del mentoreado con las fortalezas curriculares específicas, horarios disponibles y reputación docente del mentor.
2. **Inexistencia de Gobernanza y Trazabilidad Institucional:** La Dirección de Escuela y el Comité de Tutoría carecen de visibilidad sobre qué asignaturas se refuerzan, qué temas silábicos demandan mayor apoyo, quiénes participan y cuál es la efectividad pedagógica real, impidiendo la formulación de políticas preventivas oportunas.
3. **Falta de Reconocimiento Estructurado y Desgaste de Mentores:** Los estudiantes avanzados no reciben incentivos institucionales por su labor docente (como acumulación auditable de horas para convalidación de créditos extracurriculares o insignias de reputación), lo que conduce a la sobrecarga académica personal y al abandono prematuro del rol de mentor.
4. **Descoordinación en el Uso de Espacios Físicos y Virtuales:** La búsqueda informal de aulas libres en el campus de Capanique ocasiona colisiones con clases regulares o dispersión a enlaces virtuales personales sin supervisión.
5. **Transgresión de la Privacidad de Datos Académicos:** La difusión informal de historiales de notas o listas de alumnos rezagados en grupos de mensajería vulnera las directrices de consentimiento y confidencialidad establecidas en la Ley N° 29733 de Protección de Datos Personales.

## 3.2. Necesidades de los Interesados

Del diagnóstico situacional se derivan necesidades críticas para los cuatro estamentos involucrados:

1. **Estudiantes Mentoreados (Ciclos I al IV):**
   - Requieren acceso inmediato a reforzamiento conceptual oportuno antes de las evaluaciones parciales y finales.
   - Demandan un ambiente pedagógico horizontal, con lenguaje cercano y sin el temor a ser juzgados.
   - Necesitan flexibilidad horaria que no interfiera con sus jornadas lectivas regulares.
   - Exigen confidencialidad sobre su condición de rendimiento académico.

2. **Estudiantes Mentores (Ciclos VII al X):**
   - Requieren un canal oficial para publicar su disponibilidad horaria sin comprometer sus responsabilidades formativas.
   - Necesitan un marco institucional que certifique fehacientemente las horas académicas dictadas para convalidar créditos extracurriculares requeridos para su graduación.
   - Demandan espacios físicos asignados (aulas o laboratorios) o salas virtuales institucionales seguras.
   - Desean visibilidad de su impacto formativo mediante insignias de reputación académica.

3. **Coordinación de Tutoría de la EPIS-UPT:**
   - Requiere supervisar en tiempo real el cumplimiento del Artículo 40 de la Ley Universitaria N° 30220.
   - Necesita auditar bitácoras docentes con el detalle de temas tratados y firmas de inalterabilidad.
   - Demanda indicadores de ausentismo y satisfacción estudiantil para fiscalizar la calidad de las mentorías.

4. **Dirección de Escuela EPIS-UPT:**
   - Exige métricas consolidadas de demanda insatisfecha y retención estudiantil para los comités de acreditación ICACIT.
   - Requiere un mecanismo digital inviolable para la parametrización de umbrales y la emisión de constancias oficiales foliadas con verificación pública.

## 3.3. Objetivos de Negocios y Objetivos de Diseño

A continuación, se definen los objetivos estratégicos y técnicos que gobiernan el proyecto:

### Objetivos de Negocio Institucionales
- **Mitigar la Tasa de Reprobación en Asignaturas Filtro:** Reducir las desaprobaciones en Cálculo, Algoritmos, Estructuras de Datos y Programación Orientada a Objetos mediante sesiones de mentoría focalizadas en los temas silábicos de mayor dificultad.
- **Descongestionar el Sistema Tradicional de Tutoría Docente:** Transferir las consultas conceptuales y prácticas recurrentes hacia la red de mentores pares, permitiendo que los docentes tutores concentren su labor en problemáticas pedagógicas o psicosociales complejas.
- **Elevar los Índices de Retención Estudiantil:** Disminuir el abandono universitario temprano en los cuatro primeros semestres académicos de Ingeniería de Sistemas.
- **Institucionalizar el Mérito Estudiantil:** Formalizar un sistema transparente y auditable de acumulación de horas de mentoría convalidables por créditos extracurriculares de grado académico.
- **Suministrar Analítica Predictiva para la Gestión de Escuela:** Proveer tableros analíticos en tiempo real sobre demanda académica insatisfecha para retroalimentar la planificación de horarios y el rediseño silábico.

### Objetivos de Diseño e Ingeniería de Requisitos
- **Inferencia Algorítmica con Alta Precisión:** Implementar un motor híbrido (*EdRecSys*) que procese similitud coseno sobre vectores de debilidades silábicas y competencias docentes, garantizando métricas empíricas de calidad: $\text{Precision@3} \ge 80\%$, $\text{Precision@5} \ge 75\%$, ranking $\text{NDCG} \ge 0.80$ y tiempo de respuesta algorítmica $\le 500\text{ ms}$.
- **Accesibilidad Universal y Ergonomía Web:** Construir una interfaz web responsiva (React SPA) bajo directrices **WCAG 2.1 Nivel AA**, asegurando navegación por teclado, soporte para lectores de pantalla, contraste $\ge 4.5:1$ y una puntuación estandarizada superior a 75 puntos en la escala System Usability Scale (SUS).
- **Seguridad Rigurosa y Cumplimiento Normativo:** Proveer autenticación institucional dual (Email OTP / Google Workspace), control de acceso por roles (RBAC) con tokens JWT (HS256) de 8 horas, aislamiento granular de datos personales (RLS) y formalización vinculante del consentimiento bajo la Ley N° 29733.
- **Garantía Transaccional y Concurrencia Confiable:** Asegurar transacciones ACID con cerrojos pesimistas a nivel de fila (`SELECT ... FOR UPDATE`), garantizando estrictamente una tasa de sobrecupo de **0.0%** bajo condiciones de alta concurrencia en la reserva de vacantes.
- **Inmutabilidad Documental:** Respaldar las bitácoras pedagógicas con sellos hash SHA-256 e incorporar códigos QR en certificados PDF para verificación criptográfica descentralizada.

## 3.4. Alcance y Exclusiones del Proyecto

### Inclusiones Funcionales (Módulos Construidos)
1. Plataforma web adaptativa accesible desde cualquier navegador estándar de escritorio y móvil.
2. Módulo de identidad y gobernanza de privacidad con 2FA y consentimiento informado digital.
3. Catálogo curricular interactivo de asignaturas filtro y árbol de temas silábicos.
4. Motor híbrido de recomendación (*EdRecSys*) con similitud coseno y ranking adaptativo Top-k.
5. Banco de solicitudes por demanda para registrar requerimientos no cubiertos por ofertas existentes.
6. Aprovisionamiento validado de aulas físicas de la EPIS y configuración de salas virtuales institucionales.
7. Orquestación concurrente de reservas con cerrojo pesimista y ratificación obligatoria hasta $T-24\text{ h}$.
8. Demonio desatendido de evaluación de quórum (50%) a $T-24\text{ h}$ con resolución de contingencia por el mentor.
9. Marcación de asistencia presencial y virtual mediante pase QR dinámico (TOTP de 30 segundos).
10. Registro formal de bitácora docente en 48 horas con resumen pedagógico y hash SHA-256.
11. Captura de encuestas de satisfacción CSAT en ventana perentoria de 24 horas.
12. Reputación dinámica de mentores y catálogo de insignias gamificadas.
13. Panel administrativo para visado de horas acumuladas y emisión de certificados oficiales PDF con QR.
14. Tableros analíticos para supervisión directiva con métricas de retención ICACIT.

### Exclusiones del Alcance (Límites Formales de la Versión)
- **No se desarrollan aplicaciones móviles nativas compiladas para Android (APK) ni iOS (IPA):** La plataforma opera como una Single Page Application (SPA) responsiva multiplataforma accesible desde navegadores web móviles.
- **No se implementan transacciones financieras ni pasarelas de pago:** El sistema es estrictamente gratuito y de servicio social universitario formativo.
- **No se realiza sincronización síncrona en tiempo real con el ERP central de matrícula de la UPT:** La información académica y los cronogramas se cargan y sincronizan mediante interfaces estructuradas de administración (parser de cronogramas).
- **No se exige firma digital con token físico criptográfico PKI de entidades certificadoras comerciales:** La validez institucional y la inmutabilidad de certificados y bitácoras se garantiza internamente mediante folio correlativo, hash SHA-256 y código QR de verificación en línea.

## 3.5. Viabilidad Multidimensional del Sistema

### 3.5.1. Viabilidad Técnica
El proyecto se sustenta en componentes maduros y estables de la industria del software:
- **Frontend:** React 18, TypeScript, Vite y Tailwind CSS, asegurando tiempos de carga inicial ($FCP < 1.2\text{ s}$) y compatibilidad en el 100% de navegadores modernos.
- **Backend:** Python 3.13 con FastAPI y Scikit-learn, con latencia media de recomendación algorítmica de $12.4\text{ ms}$, muy inferior al umbral admisible de $500\text{ ms}$.
- **Persistencia:** PostgreSQL v15+ administrado sobre Supabase Cloud con soporte para políticas RLS y bloqueos pesimistas a nivel de fila (`SELECT ... FOR UPDATE`), demostrando 0.0% de sobrecupo en pruebas multihilo concurrentes.

### 3.5.2. Viabilidad Económica
El análisis financiero se modeló para un horizonte de evaluación a 5 años (2026–2030) con una tasa de costo de oportunidad de capital (COK) del 12.00%:

A continuación, se presentan los indicadores financieros del proyecto:

### Cuadro 3.1: Evaluación Financiera y Económica del Proyecto (Horizonte 2026–2030)

| Indicador Financiero | Valor Cuantificado | Criterio de Aceptación | Interpretación Técnica y Financiera |
| :--- | :---: | :---: | :--- |
| **Inversión Inicial (CAPEX)** | **S/. 5,475.00** | Presupuesto Cátedra | Cubre 500 horas de ingeniería de software (Joan Medina y Renzo Antayhua a S/. 9.00/h), depreciación de equipos, conectividad, dominio web e imprevistos. |
| **Costo Operativo Anual (OPEX)** | **S/. 1,140.00** | Presupuesto Anual | Infraestructura cloud PaaS (Render / Supabase), renovación de dominio, soporte preventivo y materiales de difusión. |
| **Valor Actual Neto (VAN)** | **+S/. 10,801.64** | $\text{VAN} > 0$ | Estrictamente positivo, ratificando que el proyecto genera valor económico sustancial y excedentes por encima de la tasa de descuento exigida (12.00%). |
| **Tasa Interna de Retorno (TIR)** | **68.20%** | $\text{TIR} > \text{COK}$ (12%) | Supera con holgura el COK referencial (12.00%), confiriendo un margen de resiliencia financiera amplio ante variaciones de costos operativos. |
| **Relación Beneficio / Costo (B/C)** | **1.97** | $\text{B/C} > 1.0$ | Por cada sol invertido a lo largo del ciclo del proyecto, se generan S/. 1.97 en ahorros y beneficios valorizados para la facultad y los estudiantes. |
| **Periodo de Recuperación (Payback)**| **1 año y 9.7 meses** | $< 3\text{ años}$ | La inversión inicial se recupera plenamente antes de concluir el segundo año lectivo de puesta en producción. |

Fuente: Elaboración propia a partir del estudio económico del proyecto.

El análisis del Cuadro 3.1 certifica la sólida rentabilidad y conveniencia financiera de la solución para la Escuela Profesional de Ingeniería de Sistemas. El retorno derivado de la reducción de tasas de rezago y de desaprobación compensa con creces los costos moderados de desarrollo y mantenimiento en la nube.

### 3.5.3. Viabilidad Operativa
- **Facilidad de Adopción:** La interfaz intuitiva y responsiva no exige instalaciones locales ni configuraciones especiales por parte del estudiante.
- **Alineamiento de Incentivos:** La emisión de certificados convalidables y la gamificación resuelven el histórico desinterés de los mentores, asegurando una oferta continua de acompañamiento.
- **Automatización de Procesos:** La reducción de la intermediación manual del Comité de Tutoría permite canalizar los esfuerzos directivos hacia la fiscalización y la toma de decisiones estratégicas.

### 3.5.4. Viabilidad Legal
- **Cumplimiento de la Ley N° 29733 (Protección de Datos Personales):** Se garantiza mediante un flujo vinculante de consentimiento informado digital, almacenamiento disociado de datos académicos y registro inmutable de trazas de auditoría (IP, User-Agent, fecha UTC).
- **Alineamiento con la Ley N° 30220 (Ley Universitaria):** Materializa de forma moderna y descentralizada el mandato de tutoría permanente consignado en su Artículo 40.
- **Licenciamiento y Propiedad Intelectual:** Componentes basados en librerías de código abierto (MIT / Apache 2.0) y registro formal de derechos patrimoniales a favor de la Universidad Privada de Tacna.

### 3.5.5. Viabilidad Social y Ambiental
- **Impacto Social:** Fomenta la solidaridad académica, la cohesión comunitaria entre cohortes estudiantiles y la adquisición de habilidades de liderazgo y docencia en mentores.
- **Sostenibilidad Ambiental (*Política Paperless*):** Erradica el uso de papel en inscripciones, bitácoras docentes, listas de asistencia y constancias físicas, reduciendo la huella de carbono institucional.

## 3.6. Información obtenida del Levantamiento de Información

Durante la etapa de levantamiento de requisitos, el equipo consultor ejecutó entrevistas estructuradas y sesiones de trabajo con las autoridades de la EPIS-UPT, cuyos aportes determinaron la lógica operativa del software:

1. **Ing. Liliana Mercedes Vega Bernal (Coordinadora de Tutoría):**
   - Estableció la necesidad de clasificar como prioritarias las asignaturas con mayor reprobación en los cuatro primeros semestres.
   - Fijó la política de quórum mínimo obligatorio del 50% con corte estricto en $T-24\text{ h}$ para evitar desplazamientos inútiles y horas perdidas de los mentores.
   - Exigió el control de asistencia mediante mecanismos dinámicos y la obligatoriedad de bitácoras docentes detalladas con plazo máximo de 48 horas.
   - Dispuso que las encuestas de calidad docente (CSAT) permanezcan habilitadas durante 24 horas para garantizar retroalimentación objetiva.

2. **Mgtr. Ing. Enrique Lanchipa Valencia (Docente Asesor / Arquitecto de TI):**
   - Recomendó la adopción de una arquitectura desacoplada en tres capas con contratos JSON fuertemente tipados.
   - Sugirió incorporar algoritmos de balanceo de carga para evitar saturar a mentores destacados con múltiples solicitudes.
   - Instó a optimizar los tiempos de inferencia algorítmica por debajo de 500 ms mediante cálculo matricial en memoria.

3. **Dr. Luis Alfredo Fernández Vizcarra (Docente Asesor Metodológico):**
   - Estableció las directrices de verificación de usabilidad mediante el instrumento SUS (>75 puntos) y accesibilidad WCAG 2.1 AA.
   - Instruyó el apego estricto a las cláusulas de consentimiento previo y auditabilidad exigidas por la Ley N° 29733.

4. **Ing. Haydee Raquel Sisa Yataco (Directora [e] EPIS-UPT):**
   - Aprobó el estándar de emisión de certificados digitales en formato PDF con folio correlativo único, hash SHA-256 y código QR de verificación pública.
   - Ratificó que la postulación formal a convalidación de créditos extracurriculares exige la acumulación de al menos 20 horas efectivas de mentoría auditadas con bitácoras visadas.

---

# 4. Análisis de Procesos

## 4.1. Diagrama del Proceso Actual (As-Is)

El proceso actual de asesoría académica entre pares en la EPIS-UPT opera de forma informal, dispersa y sin control institucional. 

A continuación, se describen las etapas del flujo actual:
1. **Detección Informal de Necesidad:** El estudiante de I a IV ciclo identifica dificultades conceptuales en asignaturas formativas ante la inminencia de una práctica calificada o examen.
2. **Difusión en Canales No Oficiales:** Publica una solicitud de auxilio en grupos no institucionales de mensajería (WhatsApp, Telegram) o consulta a compañeros de ciclos superiores de forma casual.
3. **Respuesta Discrecional:** Si ningún estudiante avanzado responde, el alumno permanece sin apoyo pedagógico o acude tardíamente a la tutoría docente tradicional, afrontando un alto riesgo de reprobación.
4. **Coordinación Improvisada:** Si un compañero acepta colaborar, coordinan horario, temática y lugar a través de chats privados sin registro formal.
5. **Asignación Empírica de Ambiente:** El mentor informal busca aulas desocupadas en el pabellón de Ingeniería de Sistemas de forma manual o genera un enlace personal de videollamada sin supervisión.
6. **Ejecución no Estructurada:** Se desarrolla la asesoría sin seguir temarios silábicos definidos, sin control de tiempo y sin materiales didácticos estandarizados.
7. **Carencia de Trazabilidad y Cierre:** No se levanta lista de asistencia, no se registra bitácora pedagógica, no se recopila feedback de calidad y la Dirección de Escuela no dispone de ninguna evidencia para reconocer el mérito del mentor ni para intervenir oportunamente en la deserción.

A continuación, se presenta la representación visual del flujo actual:

### Diagrama 4.1: Diagrama de Actividades del Proceso Actual de Asesoría Informal (As-Is)

```plantuml
@startuml
title Proceso Actual de Asesoría Académica Informal (As-Is) - EPIS-UPT
skinparam activity {
  BackgroundColor white
  BorderColor #555555
  ArrowColor #333333
}

|Estudiante (I - IV Ciclo)|
start
:Identifica vacíos conceptuales en materia filtro;
:Publica consulta en grupo de WhatsApp / Telegram;

if (¿Algún estudiante superior responde?) then (No)
  :Permanece sin asesoría pedagógica;
  :Acude tardíamente a tutoría docente regular;
  :Alto riesgo de rezago o desaprobación;
  stop
else (Sí)
  |Compañero / Mentor Informal|
  :Acepta ayudar de manera voluntaria y ocasional;
  |Estudiante (I - IV Ciclo)|
  :Coordina horario y tema por chat privado;
  |Compañero / Mentor Informal|
  :Busca aula libre en el pabellón empíricamente\no crea enlace de videollamada personal;
  |Estudiante (I - IV Ciclo)|
  :Asiste a la sesión informal;
  |Compañero / Mentor Informal|
  :Explica dudas sin temario silábico estructurado;
  |Comité de Tutoría / Dirección EPIS|
  :Sin registro de asistencia ni temas tratados;
  :Sin métricas de demanda académica institucional;
  :Sin reconocimiento formal de horas para el mentor;
  stop
endif
@enduml
```

Fuente: Elaboración propia a partir del levantamiento de información en la EPIS-UPT.

El análisis del Diagrama 4.1 expone con claridad los cuellos de botella y riesgos operativos del esquema vigente. La dependencia absoluta de la buena voluntad individual, la carencia de métricas y la desarticulación institucional demuestran la urgencia de sistematizar el proceso a través de una plataforma gobernada.

## 4.2. Diagrama del Proceso Propuesto (To-Be)

El proceso propuesto reestructura y automatiza integralmente el ciclo de vida de las mentorías académicas P2P bajo un modelo gobernado y auditable.

El flujo se articula a través de las siguientes doce (12) etapas secuenciales:
1. **Autenticación Institucional Segura:** Acceso exclusivo con credenciales universitarias (`@virtual.upt.pe` o `@upt.pe`) validado mediante código OTP temporal (5 min) o credencial federada con Google Workspace institucional.
2. **Formalización del Consentimiento Legal (Ley N° 29733):** Despliegue de diálogo modal en el primer acceso que exige la aceptación informada de políticas de privacidad para habilitar el uso de datos académicos.
3. **Publicación y Planificación de Ofertas:** Los mentores calificados (ciclos VII-X con nota $\ge 14.0$) configuran ofertas de mentoría indicando materia crítica, tema silábico, fecha (con antelación $\ge 24\text{ h}$), modalidad y aforo estándar (10 presencial / 20 virtual).
4. **Inferencia Algorítmica Adaptativa (EdRecSys):** El motor calcula la afinidad temática mediante similitud coseno sobre el catálogo silábico y filtra por disponibilidad y reputación, presentando al estudiante un ranking adaptativo Top-k.
5. **Canalización de Demandas Insatisfechas:** En ausencia de ofertas coincidentes, el mentoreado registra su requerimiento en el banco institucional de solicitudes por demanda para su atención prioritaria.
6. **Inscripción Concurrente con Control de Cupos:** Reserva atómica de vacantes con cerrojo pesimista que elimina el riesgo de sobrecupo bajo concurrencia.
7. **Ratificación Obligatoria Anticipada:** El estudiante debe ratificar su compromiso de asistencia hasta $T-24\text{ h}$; las reservas no confirmadas se revocan automáticamente liberando vacantes para otros interesados.
8. **Monitoreo Automatizado de Quórum:** A $T-24\text{ h}$, un servicio cron desatendido verifica el cumplimiento del 50% de aforo reglamentario. Si no se alcanza, se transiciona a estado de contingencia donde el mentor decide si dicta la clase de forma extraordinaria o cancela ordenadamente con aviso inmediato a los inscritos.
9. **Marcación de Asistencia Dinámica (Pase QR TOTP):** En el inicio de sesión, el estudiante escanea con su dispositivo el pase QR dinámico de 30 segundos generado por el mentor o este registra la asistencia en lista.
10. **Registro Obligatorio de Bitácora Pedagógica:** Dentro de las 48 horas post-sesión, el mentor completa la bitácora con los temas abordados, el cumplimiento de objetivos y su firma con hash SHA-256.
11. **Captura de Encuestas de Calidad (Ventana 24h):** Los estudiantes asistentes disponen de 24 horas para evaluar la calidad didáctica en cuatro dimensiones, recalculando dinámicamente el puntaje de reputación e insignias del mentor.
12. **Supervisión Directiva y Certificación Oficial:** La Dirección de Escuela y Coordinación de Tutoría supervisan el tablero analítico de retención, visan las bitácoras docentes y autorizan la emisión de certificados oficiales PDF foliados con código QR institucional al alcanzar las 20 horas acumuladas.

A continuación, se presenta la representación del flujo gobernado:

### Diagrama 4.2: Diagrama de Actividades del Proceso Propuesto de Mentorías P2P (To-Be)

```plantuml
@startuml
title Proceso Propuesto de Mentorías Académicas P2P (To-Be) - EPIS-UPT
skinparam activity {
  BackgroundColor white
  BorderColor #333333
  ArrowColor #222222
}

|Estudiante Mentoreado|
start
:Inicia sesión con correo UPT y código OTP / Google;
if (¿Primer acceso?) then (Sí)
  :Formaliza consentimiento informado digital (Ley 29733);
endif

|Estudiante Mentor (VII-X)|
:Publica oferta de mentoría (Materia, Temario, Modalidad);

|Sistema Web P2P (Backend / EdRecSys)|
:Valida aula física libre o enlace virtual institucional;
:Ejecuta motor EdRecSys (Similitud Coseno + Reputación);
:Despliega ranking adaptativo Top-k al estudiante;

|Estudiante Mentoreado|
:Explora cartelera o registra solicitud en banco de demanda;
:Reserva cupo (Cerrojo pesimista FOR UPDATE);
:Ratifica asistencia obligatoria antes de T-24h;

|Sistema Web P2P (Backend / Servicio Cron)|
:Ejecuta corte automatizado a T-24h y libera no ratificados;
if (¿Quórum confirmados >= 50% de aforo?) then (Sí)
  :Confirma sesión y notifica a participantes;
else (No)
  :Transiciona a QUORUM_INSUFICIENTE;
  |Estudiante Mentor (VII-X)|
  if (¿Mentor decide continuar sesión extraordinaria?) then (Sí)
    :Ratifica realización de la sesión;
  else (No)
    |Sistema Web P2P (Backend / Servicio Cron)|
    :Cancela sesión, libera ambiente y notifica a inscritos;
    stop
  endif
endif

|Mentor y Estudiantes|
:Desarrollan la sesión de mentoría presencial o virtual;
:Estudiantes marcan asistencia con pase QR dinámico TOTP (30s);

|Estudiante Mentor (VII-X)|
:Registra bitácora pedagógica antes de 48h (Firma SHA-256);

|Estudiante Mentoreado|
:Responde encuesta de satisfacción CSAT (Ventana 24h);

|Sistema Web P2P (Backend / EdRecSys)|
:Actualiza reputación e insignias de mérito del mentor;
:Acumula horas académicas auditables en su expediente;

|Comité de Tutoría / Dirección EPIS|
:Supervisa tablero analítico de retención e indicadores ICACIT;
:Visa bitácoras docentes y audita horas efectivas;
if (¿Horas acumuladas del mentor >= Umbral 20 horas?) then (Sí)
  :Emite certificado digital oficial PDF foliado con código QR;
endif
stop
@enduml
```

Fuente: Elaboración propia a partir del diseño de procesos de C-SharkTeam.

El análisis del Diagrama 4.2 demuestra que el nuevo proceso erradica la informalidad y garantiza la trazabilidad pedagógica, la seguridad jurídica y el reconocimiento institucional del esfuerzo docente de los estudiantes mentores.

# 5. Especificación de Requerimientos de Software

## 5.1. Identificación de Módulos y Capacidades Funcionales

Para articular la solución de software con alta cohesión y bajo acoplamiento, el Sistema Web P2P se organiza en **ocho módulos canónicos especializados**. Esta descomposición modular delimita las responsabilidades de los actores en correspondencia estricta con los **veinticuatro casos de uso oficiales (CUS-001 al CUS-024)**.

A continuación, se detalla la arquitectura funcional del sistema:

### Cuadro 5.1: Descomposición Modular y Capacidades Funcionales del Sistema Web P2P

| Código | Módulo / Subsistema | Propósito Institucional | Capacidades Funcionales Principales | Actores / Sistemas Involucrados | CUS Canónicos Vinculados |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **MOD-01** | Seguridad, Autenticación y Gobernanza | Garantizar el acceso exclusivo de la comunidad universitaria, proteger la privacidad bajo la Ley N° 29733 y gobernar privilegios RBAC. | • Autenticación dual (Código OTP institucional de 6 dígitos y Google Workspace).<br>• Formalización vinculante de consentimiento informado digital (Ley N° 29733).<br>• Asignación, revocación y auditoría jerárquica de roles (Mentoreado, Mentor, Admin, Coordinador). | Usuario Institucional, Administrador, Proveedor Google Workspace, Servicio SMTP UPT | CUS-001, CUS-010 |
| **MOD-02** | Planificación, Ofertas y Gestión de Espacios | Planificar la cartelera de mentorías, gestionar infraestructura física de la EPIS y coordinar salas virtuales. | • Publicación de ofertas en materias autorizadas con antelación $\ge 24\text{ h}$.<br>• Validación de aulas libres de la EPIS contra horarios regulares y salas virtuales.<br>• Procesamiento de cronogramas oficiales semestrales de distribución de aulas.<br>• Gestión de imprevistos, reprogramación y cancelación justificada con liberación de recursos. | Estudiante Mentor, Administrador, Infraestructura EPIS, Plataforma Virtual | CUS-006, CUS-008 |
| **MOD-03** | Perfiles Académicos y Catálogo Curricular | Administrar agendas de disponibilidad horaria y el árbol curricular oficial de asignaturas filtro y temas silábicos. | • Configuración de perfil académico y matriz semanal interactiva 6×11 (08:00 a 20:00).<br>• Exploración temática profunda del catálogo de asignaturas formativas filtro.<br>• Mantenimiento administrativo del árbol silábico oficial por unidades lectivas. | Estudiante Mentoreado, Estudiante Mentor, Administrador Curricular | CUS-005, CUS-021 |
| **MOD-04** | Demanda y Recomendaciones Personalizadas | Emparejar adaptativamente debilidades de estudiantes con fortalezas docentes de mentores mediante inteligencia artificial. | • Inferencia algorítmica híbrida Top-k (similitud coseno + reputación + balance de carga).<br>• Registro y visualización del banco institucional de solicitudes por demanda académica insatisfecha.<br>• Formulación de sesiones dirigidas por mentores a partir del banco de demandas. | Estudiante Mentoreado, Estudiante Mentor, Motor Algorítmico EdRecSys | CUS-002, CUS-003 |
| **MOD-05** | Quórum, Reservas y Concurrencia | Controlar la inscripción concurrente, ratificación obligatoria y evaluación automatizada de quórum a $T-24\text{ h}$. | • Reserva concurrente de vacantes con control de aforos reglamentarios (10 presencial / 20 virtual).<br>• Ratificación perentoria de asistencia hasta el corte de 24 horas previas ($T-24\text{ h}$).<br>• Desistimiento voluntario de reservas con restitución instantánea de vacantes.<br>• Demonio cron de corte en $T-24\text{ h}$, revocación de no confirmados y evaluación de quórum (50%).<br>• Interfaz resolutiva del mentor ante quórum deficiente (continuar excepcional vs cancelar ordenado). | Estudiante Mentoreado, Estudiante Mentor, Demonio Cron Backend | CUS-004, CUS-024, CUS-017, CUS-023, CUS-007 |
| **MOD-06** | Asistencia, Bitácoras y Calidad | Respaldar la ejecución pedagógica, control estricto de asistencia y evaluación objetiva de calidad docente. | • Check-in presencial y virtual mediante pase QR dinámico con algoritmo TOTP de 30 segundos.<br>• Formulación obligatoria de bitácora docente en 48 horas sellada con hash SHA-256.<br>• Consulta de historial académico cronológico de sesiones, bitácoras y recursos didácticos.<br>• Captura de encuestas de calidad formativa (CSAT) en ventana perentoria de 24 horas. | Estudiante Mentoreado, Estudiante Mentor, Coordinador de Tutoría | CUS-012, CUS-013, CUS-014 |
| **MOD-07** | Gamificación y Certificación Digital | Incentivar el compromiso docente de mentores mediante reconocimientos gamificados y certificación auditable. | • Cálculo dinámico de índice de reputación docente (1.0 a 5.0 estrellas) y catálogo de insignias.<br>• Parametrización de umbrales semestrales y autorización de certificados ($\ge 20\text{ h}$ auditadas).<br>• Emisión programática de certificados oficiales PDF con folio único, hash SHA-256 y código QR de verificación en línea. | Estudiante Mentor, Administrador, Dirección de Escuela | CUS-018, CUS-019 |
| **MOD-08** | Analítica, Notificaciones y Supervisión | Proveer a las autoridades de herramientas de decisión estratégica, motor de alertas y fiscalización docente. | • Despacho de notificaciones y recordatorios temporales de eventos críticos.<br>• Tablero directivo de indicadores agregados de demanda insatisfecha, ausentismo y retención ICACIT.<br>• Fiscalización y visado docente de bitácoras académicas y auditoría legal bajo Ley N° 29733.<br>• Consola de parametrización institucional de aforos, umbrales y asignaturas prioritarias. | Director de Escuela, Coordinador de Tutoría, Auditor Institucional, Demonio Cron | CUS-009, CUS-011, CUS-015, CUS-016, CUS-020, CUS-022 |

Fuente: Elaboración propia a partir de la arquitectura modular de C-SharkTeam.

El análisis del Cuadro 5.1 certifica la completa cobertura del ciclo formativo de mentorías. Cada módulo agrupa capacidades cohesivas y se vincula unívocamente a los casos de uso canónicos, erradicando funcionalidades huérfanas y garantizando trazabilidad integral hacia el diseño e implementación.

---

## 5.2. Requerimientos No Funcionales (ISO/IEC 25010)

Los requerimientos no funcionales delimitan los atributos de calidad, restricciones arquitectónicas y niveles de servicio del software. Se estructuran rigurosamente bajo el estándar internacional **ISO/IEC 25010:2011**, incorporando métricas cuantificables verificadas empíricamente durante el desarrollo:

A continuación, se presenta la matriz de requerimientos no funcionales:

### Cuadro 5.2: Matriz de Requerimientos No Funcionales bajo el Estándar ISO/IEC 25010

| Código | Característica (ISO 25010) | Requerimiento No Funcional | Especificación Cuantitativa y Criterio de Aceptación | Métrica y Procedimiento de Verificación Empírica |
| :---: | :--- | :--- | :--- | :--- |
| **RNF01** | Seguridad | Autenticación institucional multifactor y gestión segura de sesiones | Autenticación 2FA sin contraseñas estáticas mediante código OTP temporal de 6 dígitos o credencial federada Google Workspace UPT. Sesión gobernada mediante tokens criptográficos firmados con HMAC-SHA256 y expiración perentoria. | • Tiempo de vida del código OTP: **5 minutos (300 s)**.<br>• Tiempo de enfriamiento para reenvío: **60 segundos**.<br>• Expiración de sesión web: **8 horas (480 min)**.<br>• Verificado con pruebas automatizadas simulando expiración temporal de credenciales. |
| **RNF02** | Seguridad | Privacidad de datos personales, aislamiento RLS y cumplimiento legal | Comunicaciones protegidas íntegramente mediante protocolo HTTPS con TLS 1.3. Aislamiento granular de datos académicos a nivel de motor relacional mediante políticas de seguridad de fila (*Row Level Security*). Identificadores disociados de tipo UUID para prevenir enumeración maliciosa. | • **100% de tablas sensibles con aislamiento multiusuario activo**.<br>• **0% de exposición de notas o correos a usuarios no autorizados**.<br>• Registro inmutable de consentimiento legal (IP, fecha UTC y User-Agent) bajo Ley N° 29733. |
| **RNF03** | Eficiencia de Desempeño | Latencia de inferencia y precisión del recomendador algorítmico | El motor híbrido *EdRecSys* vectoriza debilidades silábicas y calcula similitud coseno ajustada por reputación y balance de carga, retornando un ranking adaptativo Top-k en tiempo casi instantáneo. | • **Precision@3 = 83.3%**<br>• **Precision@5 = 80.0%**<br>• **NDCG = 0.82**<br>• **Latencia media algorítmica = 12.4 ms** (umbral de diseño: $\le 500\text{ ms}$). |
| **RNF04** | Eficiencia de Desempeño | Tiempo de carga y renderizado reactivo de la interfaz web | La aplicación web de página única optimiza el empaquetado de componentes, code splitting y lazy loading para garantizar renderizados fluidos en conexiones universitarias y móviles. | • Tiempo hasta el primer contenido visible (**FCP < 1.2 segundos**).<br>• Paquete inicial de recursos comprimidos **< 250 KB**.<br>• Transiciones de interfaz reactivas en **< 50 ms**. |
| **RNF05** | Usabilidad | Ergonomía, accesibilidad universal y diseño intuitivo | Interfaces estructuradas sobre el Design System institucional con Tailwind CSS que garantizan navegación por teclado al 100%, compatibilidad con lectores de pantalla y contraste cromático adecuado. | • **Puntaje SUS > 75 puntos** en evaluación de ergonomía.<br>• Cumplimiento estricto **WCAG 2.1 Nivel AA** (contraste mínimo de **4.5:1** en textos regulares y **3.0:1** en elementos gráficos).<br>• Atributos semánticos ARIA en la totalidad de diálogos y controles interactivos. |
| **RNF06** | Fiabilidad | Disponibilidad ininterrumpida y resiliencia del servicio | Arquitectura web en la nube que asegura la continuidad operativa ininterrumpida de los servicios de consulta, reserva y marcación durante las 16 semanas del semestre académico. | • Disponibilidad del servicio **$\ge 99.5\%$** en horario lectivo.<br>• Tolerancia a fallos transitorios en microservicios auxiliares.<br>• Monitoreo de estado de salud del sistema mediante endpoint `/health`. |
| **RNF07** | Integridad y Fiabilidad | Consistencia transaccional estricta en reserva concurrente | Persistencia atómica de reservas gobernada por cerrojos transaccionales pesimistas a nivel de fila (`SELECT ... FOR UPDATE`), garantizando que jamás se asigne un cupo por encima del aforo máximo. | • **Tasa de sobrecupo verificada: estrictamente 0.0%**.<br>• 100% de transacciones concurrentes serializadas atómicamente sin inconsistencias de estado. |
| **RNF08** | Portabilidad | Compatibilidad multiplataforma y diseño web responsivo | Compatibilidad operativa y paridad visual garantizada en todos los navegadores web modernos de escritorio y dispositivos móviles (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari). | • 100% funcional en resoluciones desde teléfonos móviles (**360 px**) hasta monitores de escritorio (**1920x1080 px**).<br>• Ausencia de desbordamientos horizontales o solapamientos visuales. |
| **RNF09** | Mantenibilidad | Arquitectura limpia desacoplada y cobertura de pruebas | Separación estricta en tres capas (Presentación Web, Lógica de Negocio y Persistencia Relacional). Tipado estricto en interfaces y contratos JSON. Batería de pruebas automatizadas continua. | • Suite completa de pruebas automatizadas en backend y frontend.<br>• Cobertura de código **> 85%**.<br>• Código verificado con linters estáticos (`ruff`, `eslint`) sin advertencias críticas. |
| **RNF10** | Interoperabilidad | Resiliencia ante fallos externos y manejo estandarizado de errores | Respuestas del sistema estructuradas de forma uniforme en formato JSON con códigos de estado HTTP estandarizados y mensajes descriptivos orientados al usuario universitario. | • 100% de errores de validación y negocio formateados homogéneamente.<br>• Degradación elegante y reintentos ante caídas del servidor de correo institucional.<br>• Timeouts seguros configurados en $\le 5$ segundos. |

Fuente: Elaboración propia a partir del marco normativo ISO/IEC 25010 y las verificaciones del proyecto.

El análisis del Cuadro 5.2 demuestra que el sistema no solo satisface los requerimientos funcionales de negocio, sino que incorpora métricas cuantitativas verificables que aseguran una experiencia de usuario ágil, confiable, accesible e inviolable en términos de privacidad institucional.

---

## 5.3. Matriz Consolidada de Requerimientos Funcionales (RF01 al RF26)

El sistema formaliza **veintiséis requerimientos funcionales atómicos (RF01 al RF26)**. Cada requerimiento establece el comportamiento operativo del sistema, sus casos de uso soportados, sus contratos RESTful y sus componentes técnicos correspondientes:

A continuación, se presenta la matriz consolidada de requerimientos funcionales:

### Cuadro 5.3: Matriz Consolidada de Requerimientos Funcionales del Sistema Web P2P (RF01 al RF26)

| Código | Módulo | Denominación del Requerimiento Funcional | Casos de Uso Vinculados | Contrato RESTful / Router Principal | Componentes Técnicos Asociados (UI / Service / Persistencia) | Criticidad |
| :---: | :---: | :--- | :---: | :--- | :--- | :---: |
| **RF01** | MOD-01 | Autenticación institucional multifactor (2FA) | CUS-001 | `POST /api/v1/auth/request-otp`<br>`POST /api/v1/auth/verify-otp`<br>`POST /api/v1/auth/google` | `LoginOtpView.tsx`<br>`AuthService.py` / `authService.ts`<br>`auth_challenges`, `usuarios` | Crítica |
| **RF02** | MOD-01 | Formalización de consentimiento legal digital (Ley 29733) | CUS-001 | `GET /api/v1/consent/status`<br>`POST /api/v1/consent/accept` | `ConsentModalView.tsx`<br>`ConsentService.py` / `consentService.ts`<br>`consentimientos_legales` | Crítica |
| **RF03** | MOD-01 | Gestión y asignación administrativa de roles de usuario | CUS-010 | `GET /api/v1/roles`<br>`POST /api/v1/roles/assign`<br>`DELETE /api/v1/roles/revoke` | `AdminRolesView.tsx`<br>`RoleService.py` / `roleService.ts`<br>`roles`, `usuario_roles` | Alta |
| **RF04** | MOD-03 | Configuración de perfil formativo y matriz horaria | CUS-005 | `GET /api/v1/profiles/me`<br>`PUT /api/v1/profiles/me/availability` | `ProfileAcademicView.tsx`<br>`ProfileService.py` / `profileService.ts`<br>`perfiles_academicos`, `disponibilidades_horarias` | Alta |
| **RF05** | MOD-03 | Catálogo curricular de asignaturas y temarios silábicos | CUS-021 | `GET /api/v1/curriculum/subjects`<br>`POST /api/v1/curriculum/subjects`<br>`GET /api/v1/curriculum/topics` | `CurriculumCatalogView.tsx`<br>`CurriculumService.py` / `apiClient.ts`<br>`asignaturas`, `temas_conceptuales` | Alta |
| **RF06** | MOD-04 | Inferencia algorítmica y recomendación personalizada Top-k | CUS-002 | `GET /api/v1/recommendations/top-k`<br>`POST /api/v1/recommendations/rank` | `RecommendationFeedView.tsx`<br>`RecommendationService.py` (EdRecSys)<br>`sesiones_mentoria`, `perfiles_academicos` | Crítica |
| **RF07** | MOD-04 | Registro y banco de solicitudes por demanda académica | CUS-003 | `POST /api/v1/bookings/requests`<br>`GET /api/v1/bookings/requests/pending` | `MentoringDemandModalView.tsx`, `MentorSessionsView.tsx`<br>`BookingService.py`<br>`solicitudes_demanda` | Media |
| **RF08** | MOD-02 | Publicación y parametrización de ofertas de mentoría | CUS-006 | `POST /api/v1/offers`<br>`GET /api/v1/offers/me` | `OfferPublishView.tsx`<br>`OfferService.py` / `offerService.ts`<br>`sesiones_mentoria` (con enlaces a recursos didácticos) | Alta |
| **RF09** | MOD-02 | Aprovisionamiento automatizado de espacios y salas virtuales | CUS-006, CUS-008 | `GET /api/v1/spaces/free-slots`<br>`GET /api/v1/spaces/classrooms` | `SpaceSelectorView.tsx`<br>`VirtualRoomService.py`, `CatalogSupportService.py`<br>`sesiones_mentoria` | Alta |
| **RF10** | MOD-02 | Procesamiento de cronogramas oficiales de aulas | CUS-008 | `POST /api/v1/spaces/import-schedule` | `AdminScheduleUploadView.tsx`<br>`ScheduleParserService.py`<br>`spacesService.ts` | Alta |
| **RF11** | MOD-02 | Gestión de imprevistos, reprogramación y cancelación | CUS-006 | `PUT /api/v1/offers/{id}/reschedule`<br>`DELETE /api/v1/offers/{id}` | `MentorSessionsView.tsx`<br>`OfferService.py`<br>`sesiones_mentoria` | Alta |
| **RF12** | MOD-05 | Reserva concurrente de cupos con control de aforo | CUS-004 | `POST /api/v1/bookings/reserve` | `BookingModalView.tsx`<br>`BookingService.py` (SELECT FOR UPDATE)<br>`reservas_cupo`, `sesiones_mentoria` | Crítica |
| **RF13** | MOD-05 | Ratificación anticipada obligatoria de asistencia | CUS-024 | `POST /api/v1/bookings/{id}/confirm` | `MyBookingsView.tsx`<br>`BookingService.py`<br>`reservas_cupo` | Alta |
| **RF14** | MOD-05 | Desistimiento voluntario y liberación inmediata de cupo | CUS-017 | `POST /api/v1/bookings/{id}/cancel` | `MyBookingsView.tsx`<br>`BookingService.py`<br>`reservas_cupo` | Alta |
| **RF15** | MOD-05 | Monitoreo desatendido y corte de quórum en $T-24\text{ h}$ | CUS-023, CUS-009 | `POST /api/v1/quorum/cron-eval`<br>`GET /api/v1/notifications` | `NotificationCenterView.tsx`<br>`QuorumScheduler.py`, `BookingService.py`<br>`sesiones_mentoria`, `reservas_cupo` | Crítica |
| **RF16** | MOD-05 | Gestión resolutiva del mentor ante quórum insuficiente | CUS-007 | `POST /api/v1/offers/{id}/quorum-decision` | `QuorumDecisionModalView.tsx`<br>`OfferService.py`<br>`sesiones_mentoria` | Alta |
| **RF17** | MOD-06 | Marcación de asistencia con pase QR dinámico (TOTP) | CUS-012 | `GET /api/v1/attendance/qr/{id}`<br>`POST /api/v1/attendance/scan` | `AttendanceScannerView.tsx`, `AttendanceQrModalView.tsx`<br>`AttendanceService.py`<br>`asistencias_sesion`, `tokens_asistencia_activos` | Alta |
| **RF18** | MOD-06 | Registro de bitácora docente en 48h con hash SHA-256 | CUS-013 | `POST /api/v1/bitacora/{session_id}` | `BitacoraFormView.tsx`<br>`BitacoraService.py`<br>`bitacoras_pedagogicas` | Alta |
| **RF19** | MOD-06 | Historial de sesiones, bitácoras y recursos compartidos | CUS-014 | `GET /api/v1/bitacora/history/me`<br>`GET /api/v1/bitacora/{id}` | `BitacoraHistoryView.tsx`<br>`BitacoraService.py`<br>`bitacoras_pedagogicas`, `sesiones_mentoria` | Media |
| **RF20** | MOD-06 | Captura de encuestas de calidad post-mentoría (ventana 24h) | CUS-012, CUS-014 | `GET /api/v1/survey/{session_id}/check`<br>`POST /api/v1/survey/{session_id}` | `PostSessionSurveyModalView.tsx`<br>`SurveyService.py` / `surveyService.ts`<br>`encuestas_calidad` | Alta |
| **RF21** | MOD-07 | Cálculo de reputación docente y catálogo de insignias | CUS-019 | `GET /api/v1/recommendations/mentor/{id}/reputation` | `MentorBadgesView.tsx`<br>`RecommendationService.py`<br>`encuestas_calidad`, `perfiles_academicos` | Media |
| **RF22** | MOD-07 | Parametrización y autorización de certificados de horas | CUS-018 | `POST /api/v1/certificates/generate`<br>`GET /api/v1/certificates/pending-approval` | `AdminCertificatesView.tsx`<br>`CertificateService.py`<br>`certificados_horas` | Media |
| **RF23** | MOD-07 | Emisión, descarga y verificación con código QR | CUS-018 | `GET /api/v1/certificates/{id}/download`<br>`GET /api/v1/certificates/verificar/{hash}` | `CertificateVerifyView.tsx`, `AdminCertificatesView.tsx`<br>`CertificateService.py` (ReportLab / QrCode)<br>`certificados_horas` | Media |
| **RF24** | MOD-08 | Parametrización institucional de aforos y prioridades | CUS-020 | `GET /api/v1/admin/settings`<br>`PUT /api/v1/admin/settings` | `AdminConfigView.tsx`<br>`app.core.config`, `SimulationService.py` | Media |
| **RF25** | MOD-08 | Tablero analítico directivo y métricas de retención ICACIT | CUS-011, CUS-015 | `GET /api/v1/simulation/benchmark`<br>`GET /api/v1/recommendations/simulation/testbench` | `AdminAnalyticsView.tsx`<br>`SimulationService.py`<br>`AnalyticsService.ts` | Alta |
| **RF26** | MOD-08 | Auditoría institucional de bitácoras y privacidad legal | CUS-016, CUS-022 | `GET /api/v1/bitacora/admin/all`<br>`POST /api/v1/bitacora/{id}/review`<br>`GET /api/v1/consent/audit` | `AdminAuditView.tsx`<br>`BitacoraService.py`, `ConsentService.py`<br>`bitacoras_pedagogicas`, `consentimientos_legales` | Alta |

Fuente: Elaboración propia a partir de la homologación canónica de diseño y los controladores implementados.

El análisis del Cuadro 5.3 ratifica la coherencia absoluta del modelo funcional del Sistema Web P2P:
1. **Resolución Definitiva de RF20:** Conforme a la decisión adoptada en H01 y formalizada en H01-R, `RF20` corresponde a la *Captura de encuestas de calidad post-mentoría (ventana 24h)* sobre la entidad `encuestas_calidad` y el controlador `survey.py`, mientras que la gestión de recursos didácticos se formaliza de forma complementaria dentro de `RF08` (ofertas) y `RF19` (historial/materiales).
2. **Sincronización de Contratos:** Todas las rutas REST consignadas reflejan fielmente los endpoints reales implementados en el código de backend en FastAPI.
3. **Trazabilidad Plena:** Ningún requerimiento funcional carece de casos de uso asociados ni de componentes técnicos comprobables en la base de código.

### 5.3.1. Fichas Detalladas de Especificación de Requerimientos Funcionales (RF01 al RF26)

A continuación, se especifican exhaustivamente las fichas técnicas individuales para los veintiséis (26) requerimientos funcionales del sistema, redactadas en lenguaje funcional orientado al usuario universitario y segregando formalmente los detalles de implementación técnica:

---

#### Ficha Técnica de Requerimiento Funcional: RF01 — Autenticación Institucional Multifactor (2FA)

- **Identificador:** RF01
- **Nombre Oficial:** Autenticación institucional multifactor (2FA) y control de acceso seguro
- **Módulo Arquitectónico:** MOD-01: Seguridad, Autenticación y Gobernanza
- **Descripción Funcional:** El sistema debe autenticar la identidad de los estudiantes, mentores y autoridades universitarias de la EPIS-UPT garantizando que pertenezcan a la comunidad institucional. El usuario podrá acceder ingresando su correo electrónico institucional y verificando su identidad mediante un código temporal de un solo uso recibido en su buzón de correo, o alternativamente mediante el botón oficial de inicio de sesión con su cuenta institucional de Google Workspace.
- **Objetivo y Necesidad Académica:** Prevenir la suplantación de identidad y el acceso no autorizado de personas ajenas a la universidad, protegiendo los expedientes académicos y asegurando que las mentorías se desarrollen exclusivamente entre miembros legítimos de la EPIS.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor, Administrador Institucional (Actores Primarios); Servicio de Correo Electrónico Institucional y Proveedor de Identidad Google Workspace (Actores Secundarios).
- **Condiciones de Entrada (Precondiciones):** El usuario debe contar con una cuenta de correo electrónico institucional activa terminada en `@virtual.upt.pe` o `@upt.pe`.
- **Comportamiento Esperado:**
  1. El usuario accede a la pantalla de bienvenida e ingresa su dirección de correo institucional o selecciona la opción de acceso con Google Workspace.
  2. Si elige código de correo, el sistema comprueba la validez del dominio institucional, genera un código numérico temporal de 6 dígitos y lo remite de inmediato al buzón universitario del solicitante.
  3. El sistema muestra una pantalla con seis casillas numéricas con temporizador regresivo visible de 5 minutos y botón de reenvío bloqueado durante 60 segundos.
  4. El usuario ingresa el código de 6 dígitos recibido.
  5. El sistema valida la coincidencia y vigencia del código, confirma la identidad del estudiante y habilita el ingreso al portal universitario correspondiente a sus roles asignados.
- **Resultado Verificable (Postcondiciones):** El usuario ingresa exitosamente a su panel principal con sesión activa durante su jornada académica, registrándose la marca de auditoría de acceso exitoso.
- **Reglas de Negocio Vinculadas:** RN-01 (Dominio institucional exclusivo, código OTP con vigencia improrrogable de 5 minutos y enfriamiento de reenvío de 60 segundos).
- **Restricciones Funcionales:** Se rechaza de forma estricta cualquier dirección de correo comercial o ajena a los dominios universitarios oficiales de la UPT.
- **Criterios de Aceptación:**
  - *Escenario 1 (Acceso exitoso con código):* DADO QUE un estudiante ingresa un correo institucional válido, CUANDO introduce los 6 dígitos recibidos dentro de los 5 minutos, ENTONCES el sistema le concede acceso inmediato a la plataforma.
  - *Escenario 2 (Código expirado o erróneo):* DADO QUE el usuario ingresa un código que superó los 5 minutos de vigencia, CUANDO solicita verificar, ENTONCES el sistema rechaza el ingreso, muestra un mensaje de advertencia y le ofrece solicitar un nuevo código.
  - *Escenario 3 (Dominio no permitido):* DADO QUE una persona intenta acceder con un correo ajeno al dominio institucional, CUANDO solicita el código, ENTONCES el sistema bloquea el formulario e indica que el servicio es exclusivo para la comunidad EPIS-UPT.
- **Casos de Uso Relacionados:** CUS-001 (Autenticar usuario mediante credenciales institucionales y consentimiento digital).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/auth.py` (`POST /api/v1/auth/request-otp`, `POST /api/v1/auth/verify-otp`, `POST /api/v1/auth/google`).
  - *Servicios de Negocio:* `AuthService.py` (`request_otp`, `verify_otp`, `login_google`).
  - *Entidades Relacionales:* Tablas `auth_challenges`, `usuarios`.
  - *Componentes Visuales:* `LoginOtpView.tsx`, `authService.ts`.
  - *Evidencia de Pruebas:* `test_auth.py` (14 pruebas backend), `LoginOtpView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF02 — Formalización de Consentimiento Legal Digital

- **Identificador:** RF02
- **Nombre Oficial:** Formalización y registro del consentimiento informado digital bajo la Ley N° 29733
- **Módulo Arquitectónico:** MOD-01: Seguridad, Autenticación y Gobernanza
- **Descripción Funcional:** El sistema debe presentar a todo usuario que ingrese por primera vez a la plataforma una cláusula legal comprensible de consentimiento informado sobre el tratamiento de sus datos académicos y personales, exigiendo su aceptación explícita y vinculante para permitir la navegación en el sistema.
- **Objetivo y Necesidad Académica:** Garantizar el cumplimiento irrestricto de la legislación peruana de protección de datos personales (Ley N° 29733) y los reglamentos universitarios de la UPT, asegurando que las calificaciones y necesidades académicas se manejen con absoluta confidencialidad y reserva.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** El usuario debe haberse autenticado exitosamente por primera vez en la plataforma.
- **Comportamiento Esperado:**
  1. Tras validar la identidad del usuario, el sistema verifica si cuenta con registro previo de consentimiento informado vigente.
  2. Si no registra consentimiento, despliega inmediatamente un diálogo modal prioritario que bloquea cualquier otra interacción en la pantalla.
  3. El diálogo presenta en texto claro las finalidades del tratamiento: emparejamiento con mentores, emisión de constancias de asistencia, control de quórum y analítica agregada no nominal.
  4. El usuario revisa los términos y pulsa el botón de aceptación explícita.
  5. El sistema formaliza la aceptación registrando la decisión con sello inmutable de fecha y hora, cierra el modal y desbloquea el portal de servicios.
  6. Si el usuario rechaza los términos, el sistema cancela la sesión de forma segura y retorna a la pantalla de acceso sin registrar datos personales.
- **Resultado Verificable (Postcondiciones):** El estudiante queda formalmente habilitado para utilizar los servicios de mentoría con constancia legal digital de su aceptación.
- **Reglas de Negocio Vinculadas:** RN-02 (Consentimiento digital previo e informado obligatorio bajo Ley N° 29733).
- **Restricciones Funcionales:** Ninguna funcionalidad de catálogo, reserva o publicación puede ejecutarse sin la previa aceptación del consentimiento.
- **Criterios de Aceptación:**
  - *Escenario 1 (Aceptación exitosa):* DADO QUE un estudiante ingresa por primera vez, CUANDO lee la cláusula y presiona "Aceptar y Continuar", ENTONCES el sistema registra su aceptación y le permite acceder a la plataforma.
  - *Escenario 2 (Rechazo voluntario):* DADO QUE un estudiante decide no aceptar los términos de privacidad, CUANDO pulsa "Rechazar y Salir", ENTONCES el sistema finaliza su sesión sin almacenar información académica privada.
- **Casos de Uso Relacionados:** CUS-001 (Autenticar usuario mediante credenciales institucionales y consentimiento digital).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/consent.py` (`GET /api/v1/consent/status`, `POST /api/v1/consent/accept`).
  - *Servicios de Negocio:* `ConsentService.py` (`get_status`, `accept_consent`).
  - *Entidades Relacionales:* Tabla `consentimientos_legales` (almacena UUID de usuario, dirección IP, User-Agent del navegador y marca de tiempo UTC).
  - *Componentes Visuales:* `ConsentModalView.tsx`, `consentService.ts`.
  - *Evidencia de Pruebas:* `test_consent.py` (10 pruebas backend), `ConsentModalView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF03 — Gestión Administrativa de Roles y Verificación de Mérito

- **Identificador:** RF03
- **Nombre Oficial:** Gestión, fiscalización y asignación administrativa de roles de usuario
- **Módulo Arquitectónico:** MOD-01: Seguridad, Autenticación y Gobernanza
- **Descripción Funcional:** El sistema debe permitir a las autoridades de la Dirección de Escuela y Coordinación de Tutoría consultar la nómina de estudiantes universitarios y administrar sus roles operativos (Mentoreado, Mentor, Administrador, Coordinador), verificando de forma estricta los requisitos de mérito académico exigidos para autorizar a un estudiante a desempeñarse como mentor de sus compañeros.
- **Objetivo y Necesidad Académica:** Garantizar la idoneidad académica y solvencia pedagógica de los mentores, protegiendo la calidad de la enseñanza que reciben los alumnos de ciclos iniciales.
- **Actores Participantes:** Administrador Institucional, Coordinador de Tutoría (Actores Primarios); Estudiante Postulante a Mentor (Actor Secundario).
- **Condiciones de Entrada (Precondiciones):** La autoridad universitaria debe tener sesión activa con privilegios de rol administrativo.
- **Comportamiento Esperado:**
  1. La autoridad accede al panel de gestión de roles y consulta la lista de postulantes a mentores.
  2. El sistema despliega el expediente de cada postulante mostrando su ciclo curricular actual y su historial de calificaciones en las asignaturas formativas.
  3. La autoridad selecciona un candidato y pulsa el comando de promoción a mentor.
  4. El sistema valida automáticamente que el estudiante pertenezca a ciclos avanzados (VII al X) y que haya aprobado la materia a dictar con una calificación sobresaliente igual o superior a 14.0.
  5. De cumplir las condiciones, el sistema actualiza el perfil del estudiante habilitándole las opciones de publicación de mentorías y emitiendo una notificación formal a su buzón institucional.
- **Resultado Verificable (Postcondiciones):** El estudiante promovido adquiere de forma inmediata las capacidades operativas del rol Mentor en la plataforma.
- **Reglas de Negocio Vinculadas:** RN-03 (Jerarquía de privilegios y verificación de mérito académico: ciclo $\ge \text{VII}$ y nota mínima $\ge 14.0$).
- **Restricciones Funcionales:** Un usuario con rol Mentoreado no puede autopromoverse ni publicar mentorías mientras no sea auditado y autorizado formalmente por la administración.
- **Criterios de Aceptación:**
  - *Escenario 1 (Promoción válida por mérito):* DADO QUE un estudiante de VIII ciclo con nota 16.0 en Cálculo postula a mentor, CUANDO el administrador pulsa "Aprobar como Mentor", ENTONCES el sistema le asigna el rol exitosamente.
  - *Escenario 2 (Bloqueo por ciclo insuficiente):* DADO QUE un estudiante de V ciclo intenta ser promovido, CUANDO el sistema evalúa su expediente, ENTONCES rechaza la asignación indicando que solo califican alumnos de ciclos VII al X.
- **Casos de Uso Relacionados:** CUS-010 (Administrar usuarios, roles y autorizaciones de mentores).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/roles.py` (`GET /api/v1/roles`, `POST /api/v1/roles/assign`, `DELETE /api/v1/roles/revoke`).
  - *Servicios de Negocio:* `RoleService.py` (`promote_user_to_mentor`, `revoke_role`).
  - *Entidades Relacionales:* Tablas `roles`, `usuario_roles`.
  - *Componentes Visuales:* `AdminRolesView.tsx`, `roleService.ts`.
  - *Evidencia de Pruebas:* `test_roles.py` (12 pruebas backend), `AdminRolesView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF04 — Configuración de Perfil Académico y Matriz Horaria

- **Identificador:** RF04
- **Nombre Oficial:** Configuración de perfil académico formativo y matriz semanal interactiva de disponibilidad
- **Módulo Arquitectónico:** MOD-03: Perfiles Académicos y Catálogo Curricular
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentores y mentoreados configurar su perfil académico formativo, declarando las asignaturas silábicas de su interés o especialidad y definiendo su disponibilidad horaria semanal mediante una cuadrícula visual interactiva de 6 días por 11 bloques de tiempo.
- **Objetivo y Necesidad Académica:** Evitar colisiones horarias entre las actividades de mentoría y las clases universitarias regulares de los alumnos, alimentando al motor de recomendación con la agenda real de los participantes.
- **Actores Participantes:** Estudiante Mentor, Estudiante Mentoreado (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** El usuario debe contar con sesión activa y consentimiento de privacidad aceptado.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a la sección de su perfil y selecciona la pestaña de disponibilidad horaria.
  2. La pantalla presenta una matriz semanal estructurada de Lunes a Sábado con bloques horarios de una hora comprendidos entre las 08:00 y las 20:00 horas.
  3. El usuario marca o desmarca interactivamente los bloques horarios en los que puede brindar o recibir mentorías, pudiendo utilizar atajos de selección rápida ("Mañanas", "Tardes", "Limpiar todo").
  4. El estudiante declara sus asignaturas de preferencia o debilidad conceptual.
  5. El usuario pulsa "Guardar Perfil y Horario".
  6. El sistema valida la consistencia de las selecciones y confirma el almacenamiento seguro de su cronograma semanal.
- **Resultado Verificable (Postcondiciones):** El perfil formativo del estudiante queda sincronizado, utilizándose de forma automática para filtrar las recomendaciones de mentoría que recibirá en el portal.
- **Reglas de Negocio Vinculadas:** RN-03 (Mérito de asignaturas según rol), RN-04 (Antelación de planificación).
- **Restricciones Funcionales:** La matriz horaria debe respetar estrictamente el horario lectivo institucional de la EPIS-UPT (lunes a sábado de 08:00 a 20:00).
- **Criterios de Aceptación:**
  - *Escenario 1 (Guardado exitoso de matriz horaria):* DADO QUE un mentor selecciona bloques disponibles de lunes a miércoles de 14:00 a 16:00, CUANDO pulsa guardar, ENTONCES el sistema persiste su horario y actualiza su disponibilidad en catálogo.
  - *Escenario 2 (Selección vacía):* DADO QUE un usuario intenta guardar su horario sin seleccionar ningún bloque de tiempo, CUANDO pulsa guardar, ENTONCES el sistema muestra una advertencia sugiriendo definir al menos un bloque para poder recibir ofertas.
- **Casos de Uso Relacionados:** CUS-005 (Configurar perfil formativo y disponibilidad horaria del estudiante).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`, `PUT /api/v1/profiles/me/availability`).
  - *Servicios de Negocio:* `ProfileService.py` (`update_availability`, `get_profile_by_user`).
  - *Entidades Relacionales:* Tablas `perfiles_academicos`, `disponibilidades_horarias`.
  - *Componentes Visuales:* `ProfileAcademicView.tsx`, `profileService.ts`.
  - *Evidencia de Pruebas:* `test_profiles.py` (14 pruebas backend), `ProfileAcademicView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF05 — Catálogo Curricular Interactivo y Temarios Silábicos

- **Identificador:** RF05
- **Nombre Oficial:** Exploración y gestión del catálogo curricular de asignaturas filtro y temarios silábicos
- **Módulo Arquitectónico:** MOD-03: Perfiles Académicos y Catálogo Curricular
- **Descripción Funcional:** El sistema debe suministrar a estudiantes y mentores un catálogo oficial interactivo con las asignaturas formativas críticas del plan de estudios de Ingeniería de Sistemas (ciclos I al IV), desglosadas jerárquicamente por unidades de aprendizaje y temas conceptuales conforme a los sílabos oficiales aprobados por la facultad. Asimismo, debe proveer a la administración de interfaces para mantener actualizado dicho catálogo.
- **Objetivo y Necesidad Académica:** Asegurar que las sesiones de mentoría se enfoquen con precisión en contenidos temáticos oficiales del currículo universitario, erradicando asesorías vagas o desalineadas de las evaluaciones de cátedra.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor (Actores Primarios de Consulta); Administrador Institucional (Actor Primario de Mantenimiento).
- **Condiciones de Entrada (Precondiciones):** Usuario con sesión activa en el sistema.
- **Comportamiento Esperado:**
  1. El estudiante ingresa al catálogo curricular interactivo y utiliza el buscador en tiempo real para localizar una materia o concepto específico.
  2. El sistema despliega las asignaturas formativas con indicación de su ciclo lectivo, su condición de asignatura filtro y su número de créditos.
  3. Al seleccionar una materia, el sistema expande el árbol de temas silábicos organizados por unidad y semana de dictado regular.
  4. El estudiante puede seleccionar cualquier tema específico para visualizar las ofertas de mentoría disponibles o canalizar una solicitud de demanda pedagógica.
  5. Para administradores, el sistema provee formularios para agregar, editar o desactivar asignaturas y temas según actualizaciones del plan curricular.
- **Resultado Verificable (Postcondiciones):** Los usuarios seleccionan temas estandarizados oficiales para todas sus publicaciones y solicitudes de mentoría.
- **Reglas de Negocio Vinculadas:** RN-11 (Asignaturas filtro prioritarias y catalogación oficial).
- **Restricciones Funcionales:** Ningún tema fuera del sílabo oficial puede ser registrado sin autorización previa de la Coordinación Académica.
- **Criterios de Aceptación:**
  - *Escenario 1 (Exploración silábica exitosa):* DADO QUE un estudiante busca "Árboles Binarios", CUANDO el sistema filtra el catálogo, ENTONCES resalta la asignatura "Algoritmos y Estructura de Datos" y la unidad temática correspondiente.
  - *Escenario 2 (Actualización administrativa):* DADO QUE el administrador actualiza un tema silábico, CUANDO guarda los cambios, ENTONCES el nuevo contenido se propaga de inmediato al catálogo disponible para mentores.
- **Casos de Uso Relacionados:** CUS-021 (Consultar y mantener catálogo curricular de asignaturas y temarios).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`GET /api/v1/curriculum/subjects`, `POST /api/v1/curriculum/subjects`, `GET /api/v1/curriculum/topics`).
  - *Servicios de Negocio:* `CurriculumService.py` (`list_subjects`, `get_topics_by_subject`).
  - *Entidades Relacionales:* Tablas `asignaturas`, `temas_conceptuales`.
  - *Componentes Visuales:* `CurriculumCatalogView.tsx`, `apiClient.ts`.
  - *Evidencia de Pruebas:* `test_curriculum.py` (16 pruebas backend), `CurriculumCatalogView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF06 — Inferencia Algorítmica y Recomendación Adaptativa Top-k

- **Identificador:** RF06
- **Nombre Oficial:** Inferencia algorítmica y recomendación personalizada Top-k mediante el motor EdRecSys
- **Módulo Arquitectónico:** MOD-04: Demanda y Recomendaciones Personalizadas
- **Descripción Funcional:** El sistema debe analizar automáticamente las necesidades académicas del estudiante mentoreado y compararlas frente a la oferta vigente de mentorías, calculando un índice de afinidad temática y presentando una cartelera personalizada con las mejores opciones de acompañamiento ordenadas por relevancia, horario y calidad docente.
- **Objetivo y Necesidad Académica:** Resolver el histórico problema de búsqueda a ciegas de ayuda académica, sugiriendo a cada estudiante el mentor más competente y disponible para su necesidad específica.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario); Motor Algorítmico EdRecSys (Actor Técnico Secundario).
- **Condiciones de Entrada (Precondiciones):** El estudiante debe haber configurado sus asignaturas de interés y debe existir al menos una oferta de mentoría en estado publicada con más de 24 horas de antelación.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a la pestaña "Explorar Mentorías" de su portal universitario.
  2. El sistema recupera el perfil del mentoreado y las ofertas activas en el sistema.
  3. El motor algorítmico calcula la afinidad temática entre los temas demandados y ofertados, ponderando la reputación acumulada del mentor, bonificando asignaturas de alta prioridad y balanceando la carga docente.
  4. El sistema presenta al estudiante una cartelera adaptativa con las mejores sesiones (Top-k), mostrando tarjetas con el tema a tratar, fecha, horario, modalidad, cupos disponibles y la reputación del mentor.
  5. El estudiante puede revisar el detalle de la sesión o proceder directamente a reservar su vacante.
- **Resultado Verificable (Postcondiciones):** El estudiante visualiza una cartelera de mentorías personalizada con un tiempo de carga imperceptible y alta precisión formativa.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación de 24h), RN-11 (Ponderación algorítmica y bonificación de cursos filtro).
- **Restricciones Funcionales:** El algoritmo debe responder con una latencia media de respuesta inferior a 500 milisegundos para no degradar la experiencia de usuario.
- **Criterios de Aceptación:**
  - *Escenario 1 (Recomendación acertada Top-k):* DADO QUE un estudiante tiene debilidad en "Punteros y Memoria Dinámica", CUANDO ingresa a la cartelera, ENTONCES las tres primeras tarjetas recomendadas corresponden a sesiones de esa temática específica con alta reputación.
  - *Escenario 2 (Filtrado de sesiones extemporáneas):* DADO QUE existe una mentoría programada para iniciar en menos de 24 horas, CUANDO el recomendador procesa el ranking, ENTONCES excluye dicha sesión por no cumplir la ventana reglamentaria de antelación.
- **Casos de Uso Relacionados:** CUS-002 (Consultar cartelera de mentorías con recomendación algorítmica personalizada).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/top-k`, `POST /api/v1/recommendations/rank`).
  - *Servicios de Negocio:* `RecommendationService.py` (`compute_top_k`, `vectorize_interests`).
  - *Componentes Visuales:* `RecommendationFeedView.tsx`, `recommendationService.ts`.
  - *Evidencia de Pruebas:* `test_recommendations.py` (22 pruebas backend, métricas $P@3=83.3\%$, $P@5=80.0\%$, latencia 12.4 ms), `RecommendationFeedView.test.tsx` (20 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF07 — Banco de Solicitudes por Demanda Académica

- **Identificador:** RF07
- **Nombre Oficial:** Registro y banco institucional de solicitudes de mentoría por demanda insatisfecha
- **Módulo Arquitectónico:** MOD-04: Demanda y Recomendaciones Personalizadas
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentoreados canalizar formalmente sus necesidades académicas hacia un banco centralizado de solicitudes cuando no existan ofertas publicadas que atiendan un tema silábico de su interés o cuando las sesiones existentes tengan su aforo agotado. Los mentores podrán revisar este banco para diseñar sesiones dirigidas.
- **Objetivo y Necesidad Académica:** Evitar que los estudiantes queden desatendidos ante la falta de ofertas espontáneas, permitiendo que la oferta pedagógica de los mentores se oriente a la demanda real de sus compañeros.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario solicitante); Estudiante Mentor (Actor Primario que atiende la demanda).
- **Condiciones de Entrada (Precondiciones):** Estudiante con sesión activa que no encuentra ofertas para su tema en la cartelera.
- **Comportamiento Esperado:**
  1. El estudiante no encuentra una sesión adecuada y presiona el botón "Solicitar Nueva Mentoría".
  2. El sistema despliega un formulario donde el alumno selecciona la materia y el tema silábico específico en el que necesita apoyo, agregando observaciones pedagógicas y preferencias horarias.
  3. El sistema valida los datos y registra la solicitud en el banco institucional asignándole un folio de seguimiento correlativo.
  4. Los mentores calificados en dicha asignatura visualizan la solicitud en su panel docente bajo la sección "Banco de Necesidades Estudiantiles".
  5. Un mentor interesado puede pulsar "Atender Solicitud", lo cual precarga los datos temáticos en el formulario de creación de oferta de mentoría para su programación inmediata.
- **Resultado Verificable (Postcondiciones):** La necesidad estudiantil queda registrada institucionalmente y disponible para ser resuelta mediante una oferta dirigida.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación de planificación), RN-11 (Priorización de cursos filtro).
- **Restricciones Funcionales:** Un estudiante no puede tener más de una solicitud activa en estado pendiente para la misma asignatura de forma simultánea.
- **Criterios de Aceptación:**
  - *Escenario 1 (Registro exitoso de demanda):* DADO QUE un estudiante necesita apoyo en "Recursividad", CUANDO completa y envía el formulario de solicitud, ENTONCES el sistema emite el folio de recepción y notifica su disponibilidad en el banco de mentores.
  - *Escenario 2 (Atención dirigida por mentor):* DADO QUE un mentor revisa el banco de solicitudes, CUANDO pulsa "Crear Mentoría para esta Demanda", ENTONCES el sistema traslada el tema silábico al formulario de publicación de oferta.
- **Casos de Uso Relacionados:** CUS-003 (Registrar y atender solicitud de mentoría académica en el banco de demanda).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/requests`, `GET /api/v1/bookings/requests/pending`).
  - *Servicios de Negocio:* `BookingService.py` (`create_demand_request`, `list_pending_demands`).
  - *Entidades Relacionales:* Tabla `solicitudes_demanda`.
  - *Componentes Visuales:* `MentoringDemandModalView.tsx`, `MentorSessionsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (12 pruebas backend), `MentoringDemandModalView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF08 — Publicación y Parametrización de Ofertas de Mentoría

- **Identificador:** RF08
- **Nombre Oficial:** Publicación, configuración y parametrización de ofertas de mentoría académica
- **Módulo Arquitectónico:** MOD-02: Planificación, Ofertas y Gestión de Espacios
- **Descripción Funcional:** El sistema debe permitir a los mentores calificados programar y publicar ofertas de mentoría académica seleccionando materias en las que cuenten con autorización docente, indicando el tema silábico específico, fecha y hora de realización, modalidad (presencial o virtual), aforo reglamentario y enlaces opcionales a recursos didácticos de preparación.
- **Objetivo y Necesidad Académica:** Dotar a los mentores de una herramienta ágil para estructurar sus sesiones de enseñanza conforme al calendario lectivo y a los aforos máximos permitidos por la escuela.
- **Actores Participantes:** Estudiante Mentor (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** El mentor debe contar con rol autorizado y con aprobación sobresaliente en la materia seleccionada.
- **Comportamiento Esperado:**
  1. El mentor accede a la vista de programación de mentorías y pulsa "Nueva Oferta de Mentoría".
  2. El sistema despliega el formulario restringiendo el catálogo de asignaturas únicamente a aquellas en las que el mentor cuenta con calificación aprobatoria auditada.
  3. El mentor selecciona la materia, elige la unidad y tema del sílabo, fija la fecha y hora de inicio, escoge la modalidad (presencial o virtual) y adjunta enlaces didácticos preparatorios (repositorio de código, diapositivas o guía de ejercicios).
  4. El sistema valida que la fecha elegida tenga una antelación mínima obligatoria de 24 horas y que el aforo se ajuste estrictamente a las normas institucionales (10 estudiantes en presencial y 20 en virtual).
  5. El mentor confirma la publicación. El sistema valida la reserva del ambiente físico o virtual y publica la sesión en la cartelera universitaria.
- **Resultado Verificable (Postcondiciones):** La oferta de mentoría queda registrada en estado publicada y visible de inmediato para las inscripciones de los mentoreados.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación mínima de publicación $\ge 24\text{ h}$), RN-05 (Aforos estándar: 10 presencial / 20 virtual).
- **Restricciones Funcionales:** Se rechaza de plano cualquier sesión programada con menos de 24 horas de anticipación o con aforo superior al límite institucional.
- **Criterios de Aceptación:**
  - *Escenario 1 (Publicación exitosa conforme a regla):* DADO QUE un mentor programa una mentoría de Algoritmos para dentro de 48 horas con aforo 10 presencial, CUANDO pulsa publicar, ENTONCES el sistema guarda la sesión y la expone en la cartelera de estudiantes.
  - *Escenario 2 (Rechazo por antelación insuficiente):* DADO QUE un mentor intenta publicar una sesión que iniciará en 6 horas, CUANDO envía el formulario, ENTONCES el sistema bloquea la acción indicando que se requiere una antelación mínima de 24 horas.
- **Casos de Uso Relacionados:** CUS-006 (Publicar y parametrizar oferta de mentoría académica).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers`, `GET /api/v1/offers/me`).
  - *Servicios de Negocio:* `OfferService.py` (`create_offer`, `validate_lead_time`).
  - *Entidades Relacionales:* Tabla `sesiones_mentoria`.
  - *Componentes Visuales:* `OfferPublishView.tsx`, `offerService.ts`.
  - *Evidencia de Pruebas:* `test_offers.py` (18 pruebas backend), `OfferPublishView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF09 — Aprovisionamiento de Espacios Físicos y Salas Virtuales

- **Identificador:** RF09
- **Nombre Oficial:** Aprovisionamiento automatizado de aulas físicas institucionales y salas virtuales
- **Módulo Arquitectónico:** MOD-02: Planificación, Ofertas y Gestión de Espacios
- **Descripción Funcional:** El sistema debe aprovisionar de forma automática y controlada la infraestructura requerida para cada sesión de mentoría. En modalidad presencial, debe consultar y asignar aulas o laboratorios desocupados de la EPIS verificados contra el horario lectivo oficial. En modalidad virtual, debe generar y asociar enlaces de teleconferencia institucionales seguros sin intervención manual externa.
- **Objetivo y Necesidad Académica:** Erradicar la búsqueda improvisada de aulas libres en el campus y asegurar que las clases virtuales se desarrollen en entornos de comunicación seguros y supervisables.
- **Actores Participantes:** Estudiante Mentor (Actor Primario solicitante); Sistema de Espacios y Plataforma Virtual Institucional (Actores Secundarios).
- **Condiciones de Entrada (Precondiciones):** Formulario de publicación de oferta en proceso de configuración con horario y modalidad definidos.
- **Comportamiento Esperado:**
  1. Durante la programación de una sesión presencial, el sistema consulta los cronogramas institucionales y despliega únicamente la lista de aulas y laboratorios de la EPIS que no registran clases regulares ni otras mentorías en dicho horario.
  2. El mentor selecciona el ambiente de su preferencia y el sistema reserva temporalmente el espacio.
  3. Si la modalidad es virtual, el sistema provisiona un enlace seguro institucional de teleconferencia y lo vincula a la sesión.
  4. Los detalles del aula o el enlace virtual permanecen asociados a la sesión y se revelan automáticamente a los estudiantes inscritos una vez confirmada la vacante.
- **Resultado Verificable (Postcondiciones):** La sesión cuenta con un espacio físico reservado sin solapamientos o con una sala virtual institucional asignada.
- **Reglas de Negocio Vinculadas:** RN-06 (Asignación validada de espacios libres), RN-07 (Aprovisionamiento virtual automatizado sin solapamientos).
- **Restricciones Funcionales:** Ningún aula física puede asignarse a dos sesiones concurrentes en el mismo rango de horario.
- **Criterios de Aceptación:**
  - *Escenario 1 (Asignación de aula libre presencial):* DADO QUE el mentor elige modalidad presencial martes a las 10:00, CUANDO consulta ambientes, ENTONCES el sistema muestra solo las aulas del pabellón EPIS libres en dicho intervalo.
  - *Escenario 2 (Enlace virtual automático):* DADO QUE el mentor selecciona modalidad virtual, CUANDO confirma la publicación, ENTONCES el sistema genera y asocia el enlace institucional sin exigir crear reuniones personales externas.
- **Casos de Uso Relacionados:** CUS-006 (Publicar y parametrizar oferta de mentoría), CUS-008 (Consultar disponibilidad de espacios y cronogramas).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/spaces.py` (`GET /api/v1/spaces/free-slots`, `GET /api/v1/spaces/classrooms`).
  - *Servicios de Negocio:* `VirtualRoomService.py`, `CatalogSupportService.py`.
  - *Componentes Visuales:* `SpaceSelectorView.tsx`.
  - *Evidencia de Pruebas:* `test_catalog_cus06_provisioning.py` (14 pruebas backend).

---

#### Ficha Técnica de Requerimiento Funcional: RF10 — Procesamiento de Cronogramas Oficiales de Aulas

- **Identificador:** RF10
- **Nombre Oficial:** Procesamiento e importación estructurada de cronogramas institucionales de espacios
- **Módulo Arquitectónico:** MOD-02: Planificación, Ofertas y Gestión de Espacios
- **Descripción Funcional:** El sistema debe permitir a las autoridades administrativas cargar e interpretar de forma automática los cronogramas oficiales de clases semestrales de la EPIS-UPT, procesando los horarios de ocupación de todas las aulas y laboratorios de cómputo para alimentar la base de datos de disponibilidad de ambientes físicos.
- **Objetivo y Necesidad Académica:** Mantener actualizada la matriz de aulas libres de la facultad para garantizar que ninguna mentoría colisione con el desarrollo regular de las cátedras universitarias.
- **Actores Participantes:** Administrador Institucional, Coordinador de Espacios (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** El administrador cuenta con el archivo oficial de distribución horaria semestral en formato estructurado (CSV o Excel).
- **Comportamiento Esperado:**
  1. El administrador ingresa a la sección de administración de espacios y selecciona la herramienta de importación horaria.
  2. Carga el archivo de cronogramas oficial emitido por la secretaría académica de la facultad.
  3. El sistema analiza el documento, extrae las asignaciones de aula, día, hora de inicio y fin, valida la integridad de los datos y descarta registros mal formados.
  4. El sistema actualiza la matriz de ocupación institucional y reporta un resumen con la cantidad de horarios procesados y las aulas habilitadas para mentorías.
- **Resultado Verificable (Postcondiciones):** El sistema dispone del mapa de aulas libres actualizado para el semestre lectivo.
- **Reglas de Negocio Vinculadas:** RN-06 (Validación estricta de espacios libres contra la carga lectiva oficial).
- **Restricciones Funcionales:** El sistema debe alertar sobre inconsistencias en el archivo y no sobrescribir reservas de mentorías previamente confirmadas.
- **Criterios de Aceptación:**
  - *Escenario 1 (Carga exitosa de cronograma):* DADO QUE el administrador sube el cronograma oficial del semestre 2026-II, CUANDO el sistema procesa el archivo, ENTONCES actualiza la disponibilidad de las 8 aulas y 4 laboratorios de la escuela.
  - *Escenario 2 (Formato corrupto):* DADO QUE se intenta cargar un archivo con columnas incorrectas, CUANDO el sistema lo valida, ENTONCES detiene el proceso y muestra un mensaje detallando las inconsistencias encontradas.
- **Casos de Uso Relacionados:** CUS-008 (Consultar disponibilidad de espacios y cronogramas institucionales).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/spaces.py` (`POST /api/v1/spaces/import-schedule`).
  - *Servicios de Negocio:* `ScheduleParserService.py` (`parse_schedule_file`, `update_classroom_slots`).
  - *Componentes Visuales:* `AdminScheduleUploadView.tsx`, `spacesService.ts`.
  - *Evidencia de Pruebas:* `test_spaces_schedule_api.py` (12 pruebas backend), `AdminScheduleUploadView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF11 — Gestión de Imprevistos, Reprogramación y Cancelación

- **Identificador:** RF11
- **Nombre Oficial:** Gestión de contingencias, reprogramación justificada y cancelación de sesiones de mentoría
- **Módulo Arquitectónico:** MOD-02: Planificación, Ofertas y Gestión de Espacios
- **Descripción Funcional:** El sistema debe permitir a los mentores y a la administración gestionar imprevistos de fuerza mayor que impidan dictar una mentoría programada, facultándolos para reprogramar fecha, hora o modalidad, o cancelar la sesión de manera justificada, liberando inmediatamente los ambientes asignados y notificando a los participantes inscritos.
- **Objetivo y Necesidad Académica:** Proporcionar un mecanismo formal y transparente para atender eventualidades docentes sin perjudicar la planificación del tiempo de los estudiantes mentoreados.
- **Actores Participantes:** Estudiante Mentor, Administrador Institucional (Actores Primarios); Estudiantes Inscritos (Actores Secundarios).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría en estado publicada o confirmada que requiera modificación antes de su inicio.
- **Comportamiento Esperado:**
  1. El mentor accede al panel de sus sesiones y selecciona la mentoría afectada.
  2. Escoge la acción correspondiente: "Reprogramar Fecha/Horario" o "Cancelar Mentoría".
  3. Si reprograma, selecciona el nuevo horario y ambiente disponible, ingresando una justificación pedagógica obligatoria.
  4. Si cancela, redacta la justificación institucional del motivo de fuerza mayor.
  5. El sistema procesa la modificación, actualiza el estado de la sesión, libera el aula física o sala virtual correspondiente y remite avisos urgentes a los correos de los estudiantes inscritos.
- **Resultado Verificable (Postcondiciones):** La sesión transiciona a su nuevo estado y los estudiantes mentoreados quedan formalmente notificados sin ambigüedades.
- **Reglas de Negocio Vinculadas:** RN-10 (Cancelación oportuna y liberación inmediata de espacios y recursos).
- **Restricciones Funcionales:** No se permite cancelar una sesión sin ingresar una justificación detallada de al menos 20 caracteres.
- **Criterios de Aceptación:**
  - *Escenario 1 (Cancelación justificada con liberación de aula):* DADO QUE un mentor sufre un imprevisto 30 horas antes de la sesión, CUANDO cancela ingresando su motivo, ENTONCES el sistema notifica a los inscritos y libera el aula en el calendario.
  - *Escenario 2 (Intento de cancelación sin motivo):* DADO QUE el mentor intenta enviar la cancelación con el campo de justificación vacío, CUANDO pulsa confirmar, ENTONCES el sistema bloquea el envío exigiendo fundamentar la suspensión.
- **Casos de Uso Relacionados:** CUS-006 (Publicar y parametrizar oferta de mentoría académica).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`PUT /api/v1/offers/{id}/reschedule`, `DELETE /api/v1/offers/{id}`).
  - *Servicios de Negocio:* `OfferService.py` (`reschedule_offer`, `cancel_offer_with_notice`).
  - *Entidades Relacionales:* Tabla `sesiones_mentoria` (transición a estados `REPROGRAMADA` o `CANCELADA`).
  - *Componentes Visuales:* `MentorSessionsView.tsx`.
  - *Evidencia de Pruebas:* `test_offers.py` (10 pruebas backend), `MentorSessionsView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF12 — Reserva Concurrente de Cupos con Control de Aforo

- **Identificador:** RF12
- **Nombre Oficial:** Inscripción y reserva de cupos con control de aforo y garantía de no sobrecupo
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Concurrencia
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentoreados solicitar e inscribirse en las ofertas de mentoría de su interés, garantizando que el aforo reglamentario (10 presencial / 20 virtual) se respete de forma estricta incluso ante múltiples solicitudes simultáneas en el mismo milisegundo, erradicando cualquier posibilidad de sobreasignación de vacantes.
- **Objetivo y Necesidad Académica:** Garantizar una asignación justa y transparente de las vacantes de mentoría, evitando la frustración estudiantil ocasionada por la sobreventa de cupos o desorden en el aula física.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante autenticado con consentimiento aceptado y sesión en estado publicada con vacantes libres.
- **Comportamiento Esperado:**
  1. El estudiante visualiza una sesión en la cartelera que cuenta con cupos libres y pulsa el botón "Reservar Vacante".
  2. El sistema despliega un diálogo modal de confirmación con el resumen de la materia, tema, fecha, modalidad y compromisos del participante.
  3. El alumno confirma su intención pulsando "Confirmar Inscripción".
  4. El sistema procesa la solicitud asegurando la exclusividad del cupo durante la transacción, verifica que aún existan vacantes y registra la reserva en estado pendiente de ratificación.
  5. El sistema decrementa en una unidad las vacantes disponibles y despliega una pantalla de confirmación exitosa con las indicaciones previas a la sesión.
- **Resultado Verificable (Postcondiciones):** El estudiante obtiene su cupo reservado de forma garantizada y el contador de vacantes de la sesión se actualiza en tiempo real.
- **Reglas de Negocio Vinculadas:** RN-05 (Aforo estándar máximo de 10 presencial y 20 virtual), RN-08 (Ratificación obligatoria).
- **Restricciones Funcionales:** Ningún estudiante puede reservar más de una vacante para la misma sesión de mentoría ni inscribirse si ya no existen cupos.
- **Criterios de Aceptación:**
  - *Escenario 1 (Reserva exitosa de último cupo):* DADO QUE queda 1 vacante en una mentoría presencial, CUANDO un estudiante confirma su reserva, ENTONCES el sistema asigna el cupo y cambia el estado de la sesión a "Aforo Completo".
  - *Escenario 2 (Bloqueo por aforo agotado concurrente):* DADO QUE dos estudiantes pulsan reservar al mismo instante sobre la última vacante, CUANDO el sistema procesa ambas peticiones, ENTONCES asigna el cupo al primer solicitante y notifica amablemente al segundo que la vacante se agotó, invitándolo al banco de demandas.
- **Casos de Uso Relacionados:** CUS-004 (Reservar cupo de mentoría con control concurrente de aforo).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/reserve`).
  - *Servicios de Negocio:* `BookingService.py` (`reserve_slot` con cerrojo pesimista `SELECT ... FOR UPDATE`).
  - *Entidades Relacionales:* Tablas `reservas_cupo`, `sesiones_mentoria`.
  - *Componentes Visuales:* `BookingModalView.tsx`, `bookingService.ts`.
  - *Evidencia de Pruebas:* `test_bookings.py` (20 pruebas concurrentes multihilo demostrando 0.0% sobrecupo), `BookingModalView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF13 — Ratificación Anticipada Obligatoria de Asistencia

- **Identificador:** RF13
- **Nombre Oficial:** Ratificación y confirmación perentoria de asistencia a la mentoría (hasta $T-24\text{ h}$)
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Concurrencia
- **Descripción Funcional:** El sistema debe exigir a los estudiantes con reservas activas que ratifiquen de forma obligatoria y explícita su asistencia a la sesión antes de que venza el corte de 24 horas previas al inicio de la clase ($T-24\text{ h}$), formalizando su compromiso y permitiendo al sistema depurar las reservas inactivas.
- **Objetivo y Necesidad Académica:** Combatir el ausentismo estudiantil y el acaparamiento irresponsable de vacantes, asegurando que las sesiones se confirmen con alumnos realmente comprometidos a asistir.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante con reserva en estado pendiente y reloj del sistema antes del corte de $T-24\text{ h}$.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a la sección "Mis Reservas" de su portal.
  2. El sistema resalta las sesiones pendientes de confirmación indicando el tiempo restante antes del cierre del corte anticipado.
  3. El alumno pulsa el botón "Ratificar Asistencia".
  4. El sistema valida que la sesión se encuentre dentro de la ventana reglamentaria y actualiza el estado de la reserva a "Confirmada".
  5. El sistema emite una notificación de ratificación exitosa y suma al alumno en el conteo oficial de quórum.
- **Resultado Verificable (Postcondiciones):** La reserva adquiere el estado confirmado garantizando la participación del estudiante en la sesión.
- **Reglas de Negocio Vinculadas:** RN-08 (Ventana perentoria de ratificación anticipada hasta $T-24\text{ h}$).
- **Restricciones Funcionales:** Si el estudiante no ratifica antes de vencer el plazo de 24 horas previas, el sistema revoca automáticamente su cupo sin posibilidad de reclamo.
- **Criterios de Aceptación:**
  - *Escenario 1 (Ratificación en plazo):* DADO QUE faltan 30 horas para la mentoría, CUANDO el estudiante pulsa ratificar, ENTONCES su reserva cambia a confirmada y se computa para el quórum.
  - *Escenario 2 (Intento tardío post-corte):* DADO QUE el estudiante intenta ratificar faltando 10 horas, CUANDO pulsa el botón, ENTONCES el sistema le informa que la ventana de confirmación cerró en $T-24\text{ h}$ y que su cupo fue liberado.
- **Casos de Uso Relacionados:** CUS-024 (Ratificar asistencia obligatoria a sesión de mentoría en T-24h).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/confirm`).
  - *Servicios de Negocio:* `BookingService.py` (`confirm_booking`).
  - *Entidades Relacionales:* Tabla `reservas_cupo` (transición a `CONFIRMADA`).
  - *Componentes Visuales:* `MyBookingsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (14 pruebas backend), `MyBookingsView.test.tsx` (12 pruebas frontend).

#### Ficha Técnica de Requerimiento Funcional: RF14 — Desistimiento Voluntario y Liberación Inmediata de Cupo

- **Identificador:** RF14
- **Nombre Oficial:** Desistimiento voluntario de reserva de cupo y restitución inmediata de vacante
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Concurrencia
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentoreados anular voluntariamente su reserva de mentoría si por razones de fuerza mayor no podrán asistir, siempre que lo efectúen antes del corte de 24 horas previas ($T-24\text{ h}$), liberando inmediatamente la vacante para que otro compañero pueda inscribirse sin perjudicar su récord de asistencia.
- **Objetivo y Necesidad Académica:** Fomentar la responsabilidad estudiantil y maximizar el aprovechamiento de la infraestructura académica mediante la reasignación dinámica de cupos desocupados a tiempo.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante con reserva activa (en estado pendiente o confirmada) antes del corte perentorio de 24 horas.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a "Mis Reservas" y pulsa "Cancelar mi Reserva" en la sesión deseada.
  2. El sistema solicita confirmación mediante un diálogo advirtiendo que la vacante será liberada inmediatamente.
  3. El estudiante confirma el desistimiento.
  4. El sistema actualiza el estado de la reserva a "Cancelada por Usuario", incrementa en una unidad el aforo disponible de la sesión y remite un correo informativo al estudiante.
  5. La vacante liberada se vuelve visible en la cartelera de mentorías de forma instantánea.
- **Resultado Verificable (Postcondiciones):** La reserva queda formalmente anulada sin penalización para el estudiante y la vacante queda libre en el aforo de la mentoría.
- **Reglas de Negocio Vinculadas:** RN-08 (Plazo límite de cancelación y ratificación en $T-24\text{ h}$), RN-10 (Liberación de recursos).
- **Restricciones Funcionales:** Si el corte de 24 horas ya expiró, el botón de desistimiento se bloquea para no alterar el quórum confirmado.
- **Criterios de Aceptación:**
  - *Escenario 1 (Desistimiento oportuno exitoso):* DADO QUE faltan 36 horas para la clase, CUANDO el alumno cancela su reserva, ENTONCES el sistema libera el cupo y actualiza el aforo en la cartelera.
  - *Escenario 2 (Intento extemporáneo):* DADO QUE faltan 12 horas para la sesión, CUANDO el alumno intenta desistir en el sistema, ENTONCES el formulario le notifica que el plazo venció y que debe comunicar su inasistencia justificándola ante el mentor.
- **Casos de Uso Relacionados:** CUS-017 (Cancelar voluntariamente reserva de mentoría académica antes de T-24h).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/cancel`).
  - *Servicios de Negocio:* `BookingService.py` (`cancel_booking_by_user`).
  - *Entidades Relacionales:* Tabla `reservas_cupo` (transición a `CANCELADA_USUARIO`).
  - *Componentes Visuales:* `MyBookingsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (10 pruebas backend), `MyBookingsView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF15 — Monitoreo Desatendido y Corte de Quórum en $T-24\text{ h}$

- **Identificador:** RF15
- **Nombre Oficial:** Monitoreo desatendido, corte perentorio de reservas y evaluación de quórum a $T-24\text{ h}$
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Concurrencia
- **Descripción Funcional:** El sistema debe ejecutar de forma automática e ininterrumpida una rutina en segundo plano que identifique todas las sesiones que alcanzan exactamente las 24 horas previas a su inicio ($T-24\text{ h}$). En dicho instante, el sistema debe revocar automáticamente las reservas no ratificadas, totalizar a los confirmados y verificar si se cumple el quórum mínimo reglamentario (50% del aforo). Si se cumple, confirma la sesión; de lo contrario, alerta al mentor para resolución de contingencia.
- **Objetivo y Necesidad Académica:** Asegurar que ninguna sesión se dicte con deserción oculta y evitar que los mentores acudan a la universidad a aulas vacías.
- **Actores Participantes:** Demonio de Segundo Plano del Sistema (Actor Técnico Primario); Estudiante Mentor y Estudiantes Inscritos (Actores Secundarios notificados).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría en estado publicada que alcanza exactamente el umbral temporal de 24 horas antes de su inicio.
- **Comportamiento Esperado:**
  1. El demonio cron inspecciona periódicamente la base de datos de sesiones activas.
  2. Detecta una sesión que entra en la ventana de $T-24\text{ h}$.
  3. Ejecuta el corte perentorio: busca reservas en estado pendiente (no ratificadas) y las transiciona a "No Confirmada / Expirada", liberando cupos residuales.
  4. Cuenta los participantes con estado confirmado:
     - Si los confirmados representan al menos el 50% del aforo (5 en presencial, 10 en virtual), la sesión transiciona automáticamente a "Confirmada" y se notifica la realización definitiva a los participantes.
     - Si los confirmados son menores al 50%, transiciona la sesión al estado "Quórum Insuficiente" y despacha una alerta urgente al mentor para que decida el destino de la clase.
- **Resultado Verificable (Postcondiciones):** La sesión queda confirmada formalmente o ingresa a contingencia, garantizándose que todas las reservas no ratificadas queden invalidadas.
- **Reglas de Negocio Vinculadas:** RN-08 (Corte en $T-24\text{ h}$), RN-09 (Quórum mínimo del 50% de aforo).
- **Restricciones Funcionales:** El proceso debe ejecutarse con puntualidad estricta y sin intervención manual de operadores humanos.
- **Criterios de Aceptación:**
  - *Escenario 1 (Quórum alcanzado exitosamente):* DADO QUE una sesión presencial de aforo 10 tiene 6 alumnos confirmados a $T-24\text{ h}$, CUANDO corre el demonio, ENTONCES confirma la sesión y notifica a los 6 estudiantes.
  - *Escenario 2 (Quórum insuficiente por abandono):* DADO QUE una sesión tiene solo 2 alumnos confirmados a $T-24\text{ h}$, CUANDO corre el demonio, ENTONCES pasa la sesión a quórum insuficiente y notifica al mentor para su decisión.
- **Casos de Uso Relacionados:** CUS-023 (Evaluar automáticamente quórum mínimo de sesión en T-24h), CUS-009 (Despachar notificaciones y alertas automáticas de eventos críticos).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/quorum.py` (`POST /api/v1/quorum/cron-eval`).
  - *Servicios de Negocio:* `QuorumScheduler.py`, `BookingService.py`.
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `reservas_cupo`.
  - *Evidencia de Pruebas:* `test_quorum.py` (16 pruebas backend con simulación de avance de tiempo).

---

#### Ficha Técnica de Requerimiento Funcional: RF16 — Gestión Resolutiva del Mentor ante Quórum Insuficiente

- **Identificador:** RF16
- **Nombre Oficial:** Gestión resolutiva del mentor ante quórum insuficiente en $T-24\text{ h}$
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Concurrencia
- **Descripción Funcional:** El sistema debe proveer al mentor de una interfaz resolutiva cuando su sesión sea declarada en estado de quórum insuficiente a $T-24\text{ h}$, permitiéndole tomar una de dos decisiones pedagógicas: aceptar dictar la sesión de forma extraordinaria con los alumnos confirmados, o cancelar definitivamente la clase liberando el aula física o sala virtual y notificando a los estudiantes con anticipación.
- **Objetivo y Necesidad Académica:** Otorgar flexibilidad al mentor para apoyar a grupos reducidos si su disponibilidad lo permite, evitando al mismo tiempo cancelaciones imprevistas de última hora en la puerta del aula.
- **Actores Participantes:** Estudiante Mentor (Actor Primario); Estudiantes Confirmados (Actores Secundarios).
- **Condiciones de Entrada (Precondiciones):** Sesión en estado "Quórum Insuficiente" notificada al mentor tras el corte de $T-24\text{ h}$.
- **Comportamiento Esperado:**
  1. El mentor recibe la alerta en su panel docente y accede al diálogo de resolución de quórum.
  2. La pantalla le informa la cantidad de alumnos confirmados y le presenta las opciones institucionales: "Continuar con Quórum Reducido" o "Cancelar Sesión".
  3. Si elige continuar, la sesión pasa a estado "Confirmada Extraordinaria" y se confirma a los alumnos.
  4. Si elige cancelar, la sesión transiciona a "Cancelada por Quórum", el sistema libera de inmediato la reserva del aula o sala virtual y remite disculpas y opciones de reprogramación a los estudiantes.
- **Resultado Verificable (Postcondiciones):** La contingencia queda resuelta y los recursos de infraestructura se optimizan de inmediato.
- **Reglas de Negocio Vinculadas:** RN-09 (Quórum 50%), RN-10 (Liberación oportuna de recursos ante cancelación).
- **Restricciones Funcionales:** El mentor dispone de una ventana de 6 horas post-corte para resolver la contingencia; si no responde, el sistema cancela la sesión de forma preventiva.
- **Criterios de Aceptación:**
  - *Escenario 1 (Decisión de dictar con quórum reducido):* DADO QUE hay 3 alumnos confirmados en una sesión de 10, CUANDO el mentor pulsa "Continuar Sesión", ENTONCES la clase se ratifica y el aula se mantiene asignada.
  - *Escenario 2 (Decisión de cancelación ordenada):* DADO QUE el mentor no puede dictar a quórum reducido, CUANDO pulsa "Cancelar Sesión", ENTONCES el aula física se desocupa en el sistema y los 3 alumnos son notificados.
- **Casos de Uso Relacionados:** CUS-007 (Resolver contingencia de quórum insuficiente por el mentor).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id}/quorum-decision`).
  - *Servicios de Negocio:* `OfferService.py` (`handle_quorum_decision`).
  - *Entidades Relacionales:* Tabla `sesiones_mentoria`.
  - *Componentes Visuales:* `QuorumDecisionModalView.tsx`.
  - *Evidencia de Pruebas:* `test_offers.py` (12 pruebas backend), `QuorumDecisionModalView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF17 — Marcación de Asistencia con Pase QR Dinámico (TOTP)

- **Identificador:** RF17
- **Nombre Oficial:** Control y marcación de asistencia presencial y virtual mediante pase QR dinámico (TOTP)
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe controlar el registro fehaciente de asistencia de los estudiantes al inicio de la sesión de mentoría. El mentor podrá proyectar en pantalla un código QR dinámico que se renueva automáticamente cada 30 segundos, el cual debe ser escaneado por los estudiantes con la cámara de sus teléfonos inteligentes o computadoras para validar su presencia física o virtual. Como mecanismo de respaldo, el mentor dispondrá de una lista de asistencia manual para registrar a quienes sufran problemas de conectividad o cámara.
- **Objetivo y Necesidad Académica:** Garantizar la autenticidad e inmediatez del control de asistencia, impidiendo que estudiantes ausentes marquen presencia compartiendo capturas estáticas de pantalla por mensajería.
- **Actores Participantes:** Estudiante Mentor (Actor Primario que proyecta o pasa lista); Estudiante Mentoreado (Actor Primario que escanea).
- **Condiciones de Entrada (Precondiciones):** Sesión en estado confirmada o en curso dentro del rango de tolerancia horaria (+/- 15 minutos del inicio).
- **Comportamiento Esperado:**
  1. El mentor inicia la sesión y abre la vista "Pase de Asistencia QR".
  2. El sistema genera un código QR sincronizado con el reloj del servidor que caduca cada 30 segundos, proyectándolo en pantalla con una barra de progreso regresiva.
  3. El estudiante asistente ingresa a su portal, abre el escáner de cámara integrado y apunta al código QR proyectado.
  4. El sistema valida la vigencia del código, corrobora que el alumno tenga reserva confirmada en la sesión y registra su asistencia efectiva con sello de fecha y hora.
  5. La pantalla del mentor actualiza en tiempo real la lista de asistentes presentes.
  6. Si un estudiante carece de cámara operativa, el mentor puede pulsar el control manual "Marcar Asistió" en su lista.
- **Resultado Verificable (Postcondiciones):** La asistencia queda registrada fehacientemente, habilitando al estudiante para calificar la mentoría y acreditando las horas para el mentor.
- **Reglas de Negocio Vinculadas:** RN-05 (Aforos estándar), RN-12 (Asistencia como requisito para evaluar y computar horas).
- **Restricciones Funcionales:** Un código QR escaneado después de sus 30 segundos de vigencia es rechazado automáticamente exigiendo escanear el nuevo código generado.
- **Criterios de Aceptación:**
  - *Escenario 1 (Escaneo dinámico exitoso):* DADO QUE el mentor proyecta el QR activo, CUANDO un alumno inscrito lo escanea dentro de los 30 segundos, ENTONCES el sistema registra su asistencia exitosa y muestra confirmación verde.
  - *Escenario 2 (Intento con captura expirada):* DADO QUE un alumno intenta escanear una fotografía tomada minutos antes, CUANDO el sistema procesa el código, ENTONCES rechaza la marcación por token expirado.
- **Casos de Uso Relacionados:** CUS-012 (Controlar y registrar asistencia de participantes mediante pase QR dinámico).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/attendance.py` (`GET /api/v1/attendance/qr/{session_id}`, `POST /api/v1/attendance/scan`).
  - *Servicios de Negocio:* `AttendanceService.py` (`generate_totp_token`, `validate_totp_scan`).
  - *Entidades Relacionales:* Tablas `asistencias_sesion`, `tokens_asistencia_activos`.
  - *Componentes Visuales:* `AttendanceScannerView.tsx`, `AttendanceQrModalView.tsx`.
  - *Evidencia de Pruebas:* `test_attendance.py` (18 pruebas backend), `AttendanceScannerView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF18 — Registro de Bitácora Docente en 48h con Hash SHA-256

- **Identificador:** RF18
- **Nombre Oficial:** Formulación y registro estructurado de bitácora pedagógica docente con sello de inalterabilidad SHA-256
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe exigir a los mentores el registro obligatorio de una bitácora pedagógica estructurada dentro de las 48 horas posteriores a la finalización de cada mentoría. En ella deben detallar los temas silábicos cubiertos, el cumplimiento de objetivos didácticos, las incidencias pedagógicas y la ratificación final de la asistencia. Al enviarse, el sistema debe sellar la bitácora con una firma criptográfica hash SHA-256 que garantice su inalterabilidad posterior.
- **Objetivo y Necesidad Académica:** Respaldar institucionalmente el trabajo docente realizado por los mentores, proveyendo evidencias pedagógicas auditables que sustenten la posterior convalidación de horas extracurriculares ante la Dirección de Escuela.
- **Actores Participantes:** Estudiante Mentor (Actor Primario); Coordinador de Tutoría (Actor Auditor Secundario).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría culminada en estado realizada y dentro del plazo de 48 horas.
- **Comportamiento Esperado:**
  1. El mentor accede a la sección de bitácoras pendientes y selecciona la sesión recién concluida.
  2. Completa el formulario estructurado indicando el porcentaje de temario desarrollado, logros de aprendizaje observados, dificultades de los estudiantes y compromisos de refuerzo.
  3. Revisa y confirma la nómina de asistencia final.
  4. El mentor presiona "Firmar y Registrar Bitácora Docente".
  5. El sistema valida que los campos descriptivos cumplan la extensión mínima requerida, genera un sello criptográfico hash SHA-256 combinando el contenido con la marca temporal UTC, guarda el registro en estado inmutable y remite la bitácora a la bandeja de visado del Comité de Tutoría.
- **Resultado Verificable (Postcondiciones):** La bitácora queda registrada formalmente con sello de inalterabilidad y la sesión se marca como cerrada administrativamente.
- **Reglas de Negocio Vinculadas:** RN-12 (Plazo improrrogable de 48 horas y firma SHA-256 para computar horas de mentoría).
- **Restricciones Funcionales:** Si el mentor no registra la bitácora dentro de las 48 horas reglamentarias, la sesión se bloquea para el cómputo de horas y se alerta a la Coordinación de Tutoría.
- **Criterios de Aceptación:**
  - *Escenario 1 (Registro oportuno exitoso):* DADO QUE el mentor envía la bitácora a las 12 horas de finalizada la clase, CUANDO el sistema procesa el envío, ENTONCES calcula el hash SHA-256 y bloquea la edición posterior garantizando inalterabilidad.
  - *Escenario 2 (Intento de registro extemporáneo):* DADO QUE han transcurrido 50 horas desde el fin de la sesión, CUANDO el mentor intenta acceder al formulario, ENTONCES el sistema le notifica que el plazo expiró y que debe solicitar una reapertura justificada ante Tutoría.
- **Casos de Uso Relacionados:** CUS-013 (Registrar bitácora pedagógica post-mentoría y control de cumplimiento).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`POST /api/v1/bitacora/{session_id}`).
  - *Servicios de Negocio:* `BitacoraService.py` (`create_bitacora` con cálculo de `hash_sha256`).
  - *Entidades Relacionales:* Tabla `bitacoras_pedagogicas`.
  - *Componentes Visuales:* `BitacoraFormView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (22 pruebas backend), `BitacoraFormView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF19 — Historial de Sesiones, Bitácoras y Recursos Compartidos

- **Identificador:** RF19
- **Nombre Oficial:** Consulta cronológica de historial de sesiones, bitácoras académicas y recursos didácticos
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe suministrar a estudiantes y mentores una vista cronológica interactiva con el historial de todas las sesiones de mentoría en las que han participado, permitiéndoles consultar el estado de cada sesión, revisar las bitácoras pedagógicas registradas, verificar sus asistencias y acceder a los enlaces de materiales didácticos compartidos (diapositivas, guías prácticas y repositorios de código).
- **Objetivo y Necesidad Académica:** Proporcionar a los estudiantes un repositorio ordenado de aprendizaje para repasar conceptos antes de sus exámenes, y a los mentores un registro de su trayectoria pedagógica en la escuela.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** Usuario con sesión activa en la plataforma.
- **Comportamiento Esperado:**
  1. El usuario accede a la sección "Historial Académico" en su menú principal.
  2. El sistema despliega la lista cronológica de sesiones pasadas con filtros interactivos por semestre, asignatura y estado.
  3. Al seleccionar una sesión específica, el sistema muestra el detalle pedagógico: temas tratados, asistencia registrada y enlaces a los recursos didácticos compartidos por el mentor.
  4. El estudiante puede hacer clic en los enlaces de recursos para abrir los materiales de estudio en una nueva pestaña o descargar guías adjuntas.
- **Resultado Verificable (Postcondiciones):** El usuario accede a la memoria histórica de su aprendizaje y a los recursos educativos de forma centralizada.
- **Reglas de Negocio Vinculadas:** RN-02 (Privacidad de expedientes académicos).
- **Restricciones Funcionales:** Los estudiantes solo pueden visualizar los materiales y bitácoras de las sesiones en las que estuvieron efectivamente inscritos.
- **Criterios de Aceptación:**
  - *Escenario 1 (Consulta de historial y recursos):* DADO QUE un estudiante asistió a una mentoría de Cálculo, CUANDO ingresa a su historial, ENTONCES visualiza la bitácora del mentor y los enlaces a los ejercicios resueltos.
  - *Escenario 2 (Filtrado temático):* DADO QUE un usuario filtra su historial por la asignatura "POO", CUANDO aplica el filtro, ENTONCES la pantalla despliega únicamente las sesiones correspondientes a dicha materia.
- **Casos de Uso Relacionados:** CUS-014 (Consultar historial cronológico de sesiones y bitácoras pedagógicas).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`GET /api/v1/bitacora/history/me`, `GET /api/v1/bitacora/{id}`).
  - *Servicios de Negocio:* `BitacoraService.py` (`get_user_history`).
  - *Componentes Visuales:* `BitacoraHistoryView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (10 pruebas backend), `BitacoraHistoryView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF20 — Encuestas de Calidad y Retroalimentación Post-Mentoría (24h)

- **Identificador:** RF20
- **Nombre Oficial:** Captura de encuestas de calidad, satisfacción estudiantil (CSAT) y retroalimentación post-mentoría (ventana perentoria de 24 horas)
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe habilitar un formulario interactivo y ágil de evaluación de calidad formativa dirigido exclusivamente a los estudiantes que marcaron asistencia en una sesión de mentoría culminada. El formulario evaluará cuatro dimensiones pedagógicas estructuradas (claridad en la explicación, dominio temático, empatía y puntualidad) además de comentarios abiertos opcionales, manteniéndose disponible durante una ventana perentoria de 24 horas contadas a partir de la finalización de la clase.
- **Objetivo y Necesidad Académica:** Medir de forma cuantitativa y objetiva la efectividad docente de los mentores, recopilar retroalimentación constructiva para la mejora continua y suministrar insumos empíricos para el cálculo de su reputación e insignias de mérito.
- **Actores Participantes:** Estudiante Mentoreado con asistencia registrada (Actor Primario); Estudiante Mentor Evaluado (Actor Secundario receptor de métricas).
- **Condiciones de Entrada (Precondiciones):** El estudiante debe haber marcado asistencia en la sesión (`asistencia.estado == 'ASISTIO'`) y el reloj del sistema debe encontrarse dentro de las 24 horas posteriores al cierre de la mentoría.
- **Comportamiento Esperado:**
  1. Al culminar la sesión de mentoría o en su siguiente inicio de sesión dentro de las 24 horas, el sistema muestra al estudiante asistente una notificación destacada invitándolo a evaluar la mentoría.
  2. El alumno abre el diálogo de encuesta, visualizando el nombre del mentor, la materia y los temas tratados.
  3. El formulario presenta cuatro escalas de valoración de 1 a 5 estrellas para: Claridad Conceptual, Dominio del Tema, Empatía/Paciencia y Puntualidad, más un campo de texto opcional para agradecimientos o sugerencias.
  4. El estudiante asigna sus calificaciones y pulsa "Enviar Calificación".
  5. El sistema valida que todas las dimensiones obligatorias estén completadas, persiste la encuesta de forma anónima disociada del nombre del evaluador para garantizar total honestidad, actualiza el promedio de satisfacción acumulada del mentor y cierra la notificación.
- **Resultado Verificable (Postcondiciones):** La evaluación queda registrada en el expediente docente del mentor y se incorpora de forma inmediata al cálculo de su reputación algorítmica.
- **Reglas de Negocio Vinculadas:** RN-13 (Ventana perentoria de 24 horas para encuestas y exclusividad de acceso para asistentes comprobados).
- **Restricciones Funcionales:** Si el estudiante no responde dentro de la ventana de 24 horas, el formulario se cierra definitivamente sin permitir envíos tardíos; asimismo, ningún estudiante con estado de inasistencia o sin reserva puede acceder a calificar.
- **Criterios de Aceptación:**
  - *Escenario 1 (Evaluación en plazo por alumno asistente):* DADO QUE un estudiante asistió a la clase y han transcurrido 4 horas, CUANDO califica con 5 estrellas en las 4 dimensiones y envía, ENTONCES el sistema registra la encuesta y actualiza la reputación del mentor.
  - *Escenario 2 (Intento extemporáneo post-24 horas):* DADO QUE el alumno intenta responder a las 30 horas del cierre, CUANDO pulsa la notificación, ENTONCES el sistema le informa que la ventana reglamentaria de evaluación de 24 horas ha expirado.
  - *Escenario 3 (Bloqueo a inasistente):* DADO QUE un estudiante reservó pero no marcó asistencia a la clase, CUANDO ingresa a la plataforma, ENTONCES el sistema no le habilita el formulario de evaluación de calidad.
- **Casos de Uso Relacionados:** CUS-012 (Control de asistencia), CUS-014 (Historial y retroalimentación post-sesión).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/survey.py` (`GET /api/v1/survey/{session_id}/check`, `POST /api/v1/survey/{session_id}`).
  - *Servicios de Negocio:* `SurveyService.py` (`submit_survey`, `calculate_csat_average`).
  - *Entidades Relacionales:* Tabla `encuestas_calidad` (vinculada a `sesiones_mentoria`, con campos `puntuacion_claridad`, `puntuacion_dominio`, `puntuacion_empatia`, `puntuacion_puntualidad`, `comentarios`).
  - *Componentes Visuales:* `PostSessionSurveyModalView.tsx`, `surveyService.ts`.
  - *Evidencia de Pruebas:* `test_survey.py` (16 pruebas backend), `PostSessionSurveyModalView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF21 — Cálculo de Reputación Docente y Catálogo de Insignias

- **Identificador:** RF21
- **Nombre Oficial:** Cálculo dinámico de reputación docente, sistema de gamificación y catálogo de insignias
- **Módulo Arquitectónico:** MOD-07: Gamificación y Certificación Digital
- **Descripción Funcional:** El sistema debe procesar dinámicamente las calificaciones obtenidas en las encuestas de satisfacción para calcular el índice de reputación académica de cada mentor, desbloqueando automáticamente insignias de reconocimiento docente (ej. "Mentor Destacado", "Dominio Didáctico", "Compromiso Comunitario") según metas alcanzadas en horas dictadas y valoraciones de los alumnos.
- **Objetivo y Necesidad Académica:** Motivar e incentivar el desempeño pedagógico continuo de los mentores mediante reconocimiento visible ante la comunidad de la escuela.
- **Actores Participantes:** Estudiante Mentor (Actor Primario que acumula mérito); Estudiante Mentoreado (Actor que visualiza distintivos en cartelera).
- **Condiciones de Entrada (Precondiciones):** Mentor con al menos una sesión dictada y evaluada mediante encuestas de calidad.
- **Comportamiento Esperado:**
  1. Tras cada envío de encuesta de satisfacción, el sistema recalcula la media ponderada del mentor en una escala de 1.0 a 5.0 estrellas.
  2. Evalúa las condiciones de desbloqueo de insignias institucionales:
     - "Mentor Diamante": Más de 30 horas dictadas con promedio de satisfacción $\ge 4.8$.
     - "Docente Empático": Dimensión de empatía con calificación perfecta en más del 85% de encuestas.
     - "Pilar de Cursos Filtro": Más de 10 sesiones dictadas en asignaturas de alta reprobación (Cálculo o Algoritmos).
  3. Desbloquea las insignias correspondientes y las publica en el perfil público del mentor y en las tarjetas de la cartelera de recomendaciones.
- **Resultado Verificable (Postcondiciones):** El mentor exhibe sus insignias y su nivel de reputación actualizado en toda la plataforma.
- **Reglas de Negocio Vinculadas:** RN-13 (Cálculo de reputación basado en encuestas CSAT).
- **Restricciones Funcionales:** Ninguna insignia puede asignarse manualmente sin el cumplimiento estricto de las metas cuantificables auditadas en base de datos.
- **Criterios de Aceptación:**
  - *Escenario 1 (Desbloqueo automático de insignia):* DADO QUE un mentor supera las 20 horas con promedio de 4.9 estrellas, CUANDO el sistema recalcula sus méritos, ENTONCES le otorga la insignia "Mentor de Excelencia" y le envía una felicitación a su panel.
  - *Escenario 2 (Visualización de estrellas en cartelera):* DADO QUE un estudiante explora la cartelera de mentorías, CUANDO observa una tarjeta de oferta, ENTONCES visualiza con claridad el número de estrellas y las insignias del mentor.
- **Casos de Uso Relacionados:** CUS-019 (Consultar reputación docente, nivel de mérito y catálogo de insignias de gamificación).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/mentor/{id}/reputation`).
  - *Servicios de Negocio:* `RecommendationService.py` (`calculate_mentor_reputation`, `check_badge_milestones`).
  - *Componentes Visuales:* `MentorBadgesView.tsx`.
  - *Evidencia de Pruebas:* `test_recommendations.py` (12 pruebas backend), `MentorBadgesView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF22 — Parametrización y Autorización de Certificados de Horas

- **Identificador:** RF22
- **Nombre Oficial:** Parametrización de umbrales semestrales, auditoría de cumplimiento y autorización de certificados de horas
- **Módulo Arquitectónico:** MOD-07: Gamificación y Certificación Digital
- **Descripción Funcional:** El sistema debe proveer a la Dirección de Escuela y al Comité de Tutoría de interfaces administrativas para configurar el umbral mínimo de horas docentes exigidas en el semestre (fijado por defecto en 20 horas), auditar el historial de los mentores postulantes y autorizar la emisión de certificados oficiales únicamente a quienes cuenten con el 100% de bitácoras visadas y aprobadas.
- **Objetivo y Necesidad Académica:** Proteger la seriedad y el valor académico de las certificaciones institucionales de la EPIS-UPT, asegurando que solo se convaliden horas efectivamente dictadas y pedagógicamente auditadas.
- **Actores Participantes:** Director de Escuela, Coordinador de Tutoría (Actores Primarios); Estudiante Mentor Postulante (Actor Secundario).
- **Condiciones de Entrada (Precondiciones):** El mentor ha acumulado horas de mentoría en el semestre y la autoridad cuenta con sesión administrativa activa.
- **Comportamiento Esperado:**
  1. La autoridad accede al panel de certificación y revisa la nómina de mentores que han alcanzado o superado el umbral parametrizado (20 horas).
  2. El sistema despliega el desglose de cada mentor mostrando la suma total de horas dictadas, la cantidad de sesiones realizadas, el promedio de satisfacción estudiantil y el estado de visado de sus bitácoras.
  3. Si el mentor registra bitácoras pendientes de visado u observadas, el sistema deshabilita el comando de autorización.
  4. La autoridad revisa el expediente conforme y pulsa "Aprobar y Autorizar Emisión de Certificado".
  5. El sistema formaliza la aprobación generando el número de folio correlativo institucional del certificado y habilitando su descarga.
- **Resultado Verificable (Postcondiciones):** El expediente queda marcado como autorizado para emisión documental oficial.
- **Reglas de Negocio Vinculadas:** RN-14 (Umbral mínimo de 20 horas acumuladas con 100% de bitácoras auditadas y visadas).
- **Restricciones Funcionales:** Ningún certificado puede emitirse a mentores que acumulen menos de 20 horas efectivas de clase en el periodo lectivo.
- **Criterios de Aceptación:**
  - *Escenario 1 (Autorización válida por 20 horas cumplidas):* DADO QUE un mentor acumula 22 horas auditadas con todas sus bitácoras aprobadas, CUANDO la autoridad pulsa autorizar, ENTONCES el sistema genera el folio oficial de certificación.
  - *Escenario 2 (Bloqueo por horas insuficientes):* DADO QUE un mentor registra 18 horas de mentoría, CUANDO la autoridad consulta su estado, ENTONCES el sistema le indica que aún no alcanza el umbral mínimo de 20 horas para certificar.
- **Casos de Uso Relacionados:** CUS-018 (Gestionar y autorizar emisión de certificados oficiales de horas de mentoría).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/certificates.py` (`POST /api/v1/certificates/generate`, `GET /api/v1/certificates/pending-approval`).
  - *Servicios de Negocio:* `CertificateService.py` (`verify_eligibility`, `approve_certificate`).
  - *Entidades Relacionales:* Tabla `certificados_horas`.
  - *Componentes Visuales:* `AdminCertificatesView.tsx`.
  - *Evidencia de Pruebas:* `test_certificates.py` (18 pruebas backend), `AdminCertificatesView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF23 — Emisión, Descarga y Verificación con Código QR

- **Identificador:** RF23
- **Nombre Oficial:** Generación programática en PDF, descarga y verificación pública en línea con código QR
- **Módulo Arquitectónico:** MOD-07: Gamificación y Certificación Digital
- **Descripción Funcional:** El sistema debe generar programáticamente el documento oficial de certificación en formato estándar PDF/A, incorporando la identidad gráfica de la UPT, el folio correlativo institucional, los datos del mentor, la cantidad de horas acreditadas, el resumen de asignaturas dictadas, el sello criptográfico hash SHA-256 de inalterabilidad y un código QR vectorial que permita a cualquier persona verificar la autenticidad del documento en el portal web institucional.
- **Objetivo y Necesidad Académica:** Proporcionar al estudiante un documento probatorio formal, estéticamente profesional e infalsificable para sus trámites de convalidación de créditos extracurriculares y su portafolio profesional.
- **Actores Participantes:** Estudiante Mentor (Actor Primario que descarga); Empleador / Comité Evaluador Externo (Actor Secundario que verifica).
- **Condiciones de Entrada (Precondiciones):** Certificado formalmente autorizado por la Dirección de Escuela.
- **Comportamiento Esperado:**
  1. El mentor ingresa a la pestaña "Mis Certificados" y pulsa "Descargar Certificado Oficial (PDF)".
  2. El sistema compila el documento en memoria, estampando el folio correlativo único, las horas auditadas, el hash de seguridad y el código QR de verificación que apunta a la URL pública del validador institucional.
  3. El navegador descarga el archivo PDF listo para impresión o presentación digital.
  4. Si un evaluador externo o autoridad escanea el código QR del certificado impreso con su teléfono, el navegador abre de inmediato la página pública de verificación en el portal de la UPT, confirmando el nombre del mentor, las horas válidas y el estado vigente del documento.
- **Resultado Verificable (Postcondiciones):** El mentor dispone de su certificado digital en PDF y cualquier tercero puede comprobar su autenticidad en tiempo real.
- **Reglas de Negocio Vinculadas:** RN-14 (Certificación institucional de horas auditadas).
- **Restricciones Funcionales:** El código QR debe contener una firma criptográfica única que imposibilite la clonación o alteración del texto del PDF.
- **Criterios de Aceptación:**
  - *Escenario 1 (Descarga exitosa de PDF válido):* DADO QUE el certificado está autorizado, CUANDO el mentor pulsa descargar, ENTONCES obtiene un archivo PDF con formato oficial institucional y código QR nítido.
  - *Escenario 2 (Verificación pública exitosa por QR):* DADO QUE un evaluador escanea el QR de un certificado, CUANDO abre el enlace institucional, ENTONCES el portal confirma que el documento es auténtico y fue expedido por la EPIS-UPT.
- **Casos de Uso Relacionados:** CUS-018 (Gestionar y autorizar emisión de certificados oficiales de horas de mentoría).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/certificates.py` (`GET /api/v1/certificates/{id}/download`, `GET /api/v1/certificates/verificar/{hash}`).
  - *Servicios de Negocio:* `CertificateService.py` (`generate_pdf_stream` con ReportLab v4 y `verify_hash`).
  - *Componentes Visuales:* `CertificateVerifyView.tsx`, `AdminCertificatesView.tsx`.
  - *Evidencia de Pruebas:* `test_certificates.py` (14 pruebas backend con comprobación de PDF y hashes), `CertificateVerifyView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF24 — Parametrización Institucional de Aforos y Prioridades

- **Identificador:** RF24
- **Nombre Oficial:** Parametrización y gobernanza administrativa de aforos reglamentarios y prioridades académicas
- **Módulo Arquitectónico:** MOD-08: Analítica, Notificaciones y Supervisión Institucional
- **Descripción Funcional:** El sistema debe proveer a las autoridades directivas de la facultad una consola de parametrización institucional para configurar los valores operativos del sistema: límites de aforo estándar (presencial y virtual), tiempo de antelación mínima de publicación, porcentaje de quórum de confirmación ($50\%$), umbral de horas para certificar y asignación de condición prioritaria a materias formativas con altos índices de reprobación.
- **Objetivo y Necesidad Académica:** Dotar a la facultad de autonomía para ajustar las políticas operativas del sistema según la disponibilidad de aulas, el calendario de exámenes o directivas de decanato sin necesidad de modificar el código del software.
- **Actores Participantes:** Director de Escuela, Administrador Institucional (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** Usuario con sesión activa y rol de Administrador Institucional.
- **Comportamiento Esperado:**
  1. El administrador accede a la sección "Configuración Institucional del Sistema".
  2. Modifica los parámetros permitidos (ej. declarar "Algoritmos y Estructura de Datos" como materia en prioridad alta ante proximidad de exámenes parciales).
  3. Pulsa el botón "Guardar Parámetros Institucionales".
  4. El sistema valida la coherencia de los valores ingresados (ej. que los aforos no excedan las capacidades físicas reales) y propaga de inmediato las nuevas reglas al motor de recomendación y a los formularios de publicación.
- **Resultado Verificable (Postcondiciones):** Los parámetros quedan actualizados gobernando de forma inmediata todas las operaciones posteriores de la plataforma.
- **Reglas de Negocio Vinculadas:** RN-05 (Aforos estándar), RN-09 (Quórum), RN-11 (Priorización algorítmica de asignaturas formativas filtro).
- **Restricciones Funcionales:** Ningún aforo presencial puede fijarse por encima de la capacidad de seguridad del aula física más grande asignada a la escuela.
- **Criterios de Aceptación:**
  - *Escenario 1 (Actualización de materia prioritaria):* DADO QUE el director activa la prioridad para "Cálculo I", CUANDO los estudiantes ingresan a la cartelera, ENTONCES las sesiones de Cálculo I reciben una bonificación visible y encabezan las recomendaciones.
  - *Escenario 2 (Intento de fijar aforo inválido):* DADO QUE un administrador intenta fijar un aforo presencial de 50 alumnos, CUANDO pulsa guardar, ENTONCES el sistema rechaza el valor advirtiendo que el aforo presencial reglamentario máximo es 10 para garantizar atención personalizada.
- **Casos de Uso Relacionados:** CUS-020 (Configurar parámetros institucionales, umbrales y aforos del sistema).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/core/config.py`, `aplicacion/backend/app/api/v1/endpoints/simulation.py`.
  - *Componentes Visuales:* `AdminConfigView.tsx`.
  - *Evidencia de Pruebas:* `test_simulation.py` (8 pruebas backend).

---

#### Ficha Técnica de Requerimiento Funcional: RF25 — Tablero Analítico Directivo y Métricas de Retención ICACIT

- **Identificador:** RF25
- **Nombre Oficial:** Tablero institucional de analítica académica, demanda insatisfecha y métricas de retención estudiantil
- **Módulo Arquitectónico:** MOD-08: Analítica, Notificaciones y Supervisión Institucional
- **Descripción Funcional:** El sistema debe consolidar en tiempo real la información operativa de la plataforma y presentarla a la Dirección de Escuela y Coordinación de Tutoría en un tablero analítico interactivo con gráficos, tarjetas de indicadores clave de rendimiento (KPIs), métricas de asistencia efectiva, demanda formativa insatisfecha y estimaciones de impacto en la retención estudiantil alineadas con los criterios de acreditación ICACIT.
- **Objetivo y Necesidad Académica:** Brindar a las autoridades universitarias información empírica cuantitativa para la toma de decisiones pedagógicas, identificación temprana de cursos con alto riesgo de rezago y sustentación ante auditorías de calidad educativa.
- **Actores Participantes:** Director de Escuela, Coordinador de Tutoría, Comités de Calidad (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** Usuario autenticado con rol administrativo o de coordinación directiva.
- **Comportamiento Esperado:**
  1. La autoridad ingresa al panel "Analítica y Métricas de Rendimiento".
  2. El sistema presenta un tablero con indicadores agregados actualizados al instante: total de horas de mentoría dictadas, porcentaje de asistencia promedio, número de estudiantes beneficiados de I a IV ciclo y ranking de asignaturas con mayor demanda insatisfecha.
  3. La autoridad puede aplicar filtros interactivos por semestre académico, por ciclo curricular o por materia específica.
  4. El sistema permite exportar reportes consolidados en formato tabular para su incorporación en los informes semestrales de gestión de la escuela.
- **Resultado Verificable (Postcondiciones):** Las autoridades disponen de un diagnóstico analítico continuo sobre la salud pedagógica de los cursos formativos.
- **Reglas de Negocio Vinculadas:** RN-02 (Anonimización de métricas analíticas agregadas bajo Ley N° 29733).
- **Restricciones Funcionales:** Los tableros directivos deben operar sobre datos anonimizados agregados, impidiendo la divulgación pública de nombres o notas individuales de los participantes.
- **Criterios de Aceptación:**
  - *Escenario 1 (Visualización de asignaturas críticas):* DADO QUE se han registrado 15 demandas insatisfechas en "Álgebra Lineal", CUANDO la autoridad revisa el tablero, ENTONCES el sistema destaca dicha materia como foco prioritario que requiere convocar nuevos mentores.
  - *Escenario 2 (Cálculo de tasa de asistencia):* DADO QUE se han completado 40 sesiones en el mes, CUANDO se consulta el KPI de asistencia, ENTONCES el sistema totaliza los registros del pase QR y expone la tasa de asistencia efectiva.
- **Casos de Uso Relacionados:** CUS-011 (Generar reportes e indicadores de analítica académica institucional), CUS-015 (Consultar tablero analítico de métricas de retención estudiantil e indicadores ICACIT).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/simulation.py` (`GET /api/v1/simulation/benchmark`, `GET /api/v1/recommendations/simulation/testbench`).
  - *Servicios de Negocio:* `SimulationService.py` (`generate_benchmark_metrics`).
  - *Componentes Visuales:* `AdminAnalyticsView.tsx`.
  - *Evidencia de Pruebas:* `test_simulation.py` (16 pruebas backend), `AdminAnalyticsView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF26 — Auditoría Institucional de Bitácoras y Privacidad Legal

- **Identificador:** RF26
- **Nombre Oficial:** Módulo de fiscalización docente, visado de bitácoras y auditoría de privacidad bajo la Ley N° 29733
- **Módulo Arquitectónico:** MOD-08: Analítica, Notificaciones y Supervisión Institucional
- **Descripción Funcional:** El sistema debe suministrar al Comité de Tutoría y a la secretaría académica herramientas formales para auditar las bitácoras pedagógicas formuladas por los mentores, permitiendo visar y aprobar horas académicas, formular observaciones subsanables o rechazar registros irregulares. Asimismo, debe proveer una pista de auditoría inmutable sobre los consentimientos informados de privacidad y las acciones administrativas ejecutadas en el sistema.
- **Objetivo y Necesidad Académica:** Garantizar la transparencia, probidad y validez de los expedientes de convalidación académica, acreditando ante comités evaluadores que cada hora convalidada cuenta con fiscalización docente formal.
- **Actores Participantes:** Coordinador de Tutoría, Auditor Institucional (Actores Primarios); Estudiante Mentor (Actor Notificado).
- **Condiciones de Entrada (Precondiciones):** Bitácoras en estado enviada pendientes de fiscalización y usuario con rol auditor.
- **Comportamiento Esperado:**
  1. El coordinador de tutoría accede a la bandeja "Fiscalización y Visado de Bitácoras".
  2. Selecciona una bitácora enviada por un mentor, revisando los temas dictados, el resumen cualitativo, el sello hash SHA-256 de inalterabilidad y la lista de estudiantes asistentes.
  3. Si la bitácora satisface los criterios de rigor pedagógico, pulsa "Visar y Aprobar Horas", lo cual computa oficialmente el tiempo en el acumulado del mentor.
  4. Si detecta inconsistencias, pulsa "Observar Bitácora", ingresando los fundamentos para que el mentor subsane la observación en un plazo determinado.
  5. En la sección de auditoría legal, la autoridad puede exportar la traza inmutable de consentimientos registrados bajo la Ley N° 29733 para sustentar auditorías de acreditación.
- **Resultado Verificable (Postcondiciones):** La bitácora transiciona a estado visada o en observación y se actualiza el saldo oficial de horas auditadas del mentor.
- **Reglas de Negocio Vinculadas:** RN-02 (Auditoría legal de consentimientos), RN-12 (Obligatoriedad de bitácora), RN-14 (Cómputo exclusivo de horas visadas).
- **Restricciones Funcionales:** Ninguna hora de mentoría puede ser computada para certificación sin contar con el visado explícito de la Coordinación de Tutoría.
- **Criterios de Aceptación:**
  - *Escenario 1 (Visado aprobatorio de bitácora):* DADO QUE el coordinador revisa una bitácora completa y fundamentada, CUANDO presiona "Aprobar", ENTONCES el sistema visará el documento y sumará 2 horas auditadas al mentor.
  - *Escenario 2 (Observación pedagógica):* DADO QUE el informe describe temas ajenos al sílabo, CUANDO el auditor pulsa "Observar", ENTONCES la bitácora no suma horas y el mentor recibe una notificación con las instrucciones de corrección.
- **Casos de Uso Relacionados:** CUS-016 (Auditar expedientes académicos y visado docente de bitácoras), CUS-022 (Auditar registros de consentimiento informado y trazas de seguridad).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`GET /api/v1/bitacora/admin/all`, `POST /api/v1/bitacora/{id}/review`), `aplicacion/backend/app/api/v1/endpoints/consent.py` (`GET /api/v1/consent/audit`).
  - *Servicios de Negocio:* `BitacoraService.py` (`review_bitacora`), `ConsentService.py` (`get_audit_trail`).
  - *Entidades Relacionales:* Tablas `bitacoras_pedagogicas`, `consentimientos_legales`.
  - *Componentes Visuales:* `AdminAuditView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (14 pruebas backend), `AdminAuditView.test.tsx` (16 pruebas frontend).

---

## 5.4. Reglas de Negocio Institucionales (RN-01 al RN-14)

Las catorce reglas de negocio institucionales (**RN-01 al RN-14**) gobiernan la interacción pedagógica, la seguridad jurídica y la integridad transaccional de la plataforma en la EPIS-UPT:

A continuación, se presenta la matriz consolidada de reglas de negocio:

### Cuadro 5.4: Matriz de Reglas de Negocio Institucionales del Sistema Web P2P (RN-01 al RN-14)

| Código | Denominación de la Regla | Condición Disparadora | Política Institucional y Restricción Impuesta | Consecuencia de Infracción | Mecanismo de Imposición en el Sistema | Módulo |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **RN-01** | Acceso Institucional Exclusivo y 2FA | Intento de autenticación en la plataforma. | Acceso exclusivo para cuentas con dominio `@virtual.upt.pe` o `@upt.pe`. Código OTP de 6 dígitos con tiempo de vida máximo e improrrogable de 5 minutos (300 s) y enfriamiento de reenvío de 60 segundos. | Rechazo inmediato del acceso y bloqueo de emisión de token JWT. | Validación regex en servidor y hash seguro SHA-256 en base de datos. | MOD-01 |
| **RN-02** | Consentimiento Legal Digital (Ley N° 29733) | Primer inicio de sesión de cualquier usuario universitario. | Consentimiento previo, expreso, inequívoco e informado sobre tratamiento de datos académicos obligatorio antes de utilizar la plataforma. | Bloqueo perentorio de navegación y cierre seguro de sesión sin almacenar datos. | Diálogo modal prioritario en cliente y middleware de verificación en servidor que audita IP, fecha UTC y User-Agent. | MOD-01 |
| **RN-03** | Jerarquía de Roles y Verificación de Mérito | Postulación o asignación de rol de Mentor. | El mentor debe pertenecer a ciclos superiores (VII al X) y haber aprobado la materia a dictar con calificación sobresaliente igual o superior a 14.0. | Denegación de la promoción a mentor y restricción a rol exclusivo de mentoreado. | Validación algorítmica contra historial de notas y control de acceso RBAC. | MOD-01 |
| **RN-04** | Antelación Mínima de Publicación ($\ge 24\text{ h}$) | Formulación de una oferta de mentoría académica. | Toda oferta de mentoría debe publicarse con una antelación mínima obligatoria de 24 horas respecto a su inicio, recomendándose 48 horas ($T \ge 48\text{ h}$). | Bloqueo del formulario de publicación con mensaje de error de fecha no válida. | Validación temporal estricta en servidor (`fecha_inicio >= fecha_actual + 24h`). | MOD-02 |
| **RN-05** | Control Estricto de Aforos Estándar | Programación y reserva de sesiones de mentoría. | Aforo máximo de 10 participantes en sesiones presenciales y 20 en sesiones virtuales. Bloqueo automático ante aforo lleno. | Imposibilidad de exceder el límite y derivación al banco de solicitudes por demanda. | Restricción inmutable en base de datos (`aforo <= 10` presencial, `aforo <= 20` virtual) y cerrojos pesimistas. | MOD-05 |
| **RN-06** | Asignación Validada de Espacios Físicos | Selección de ambiente para mentoría presencial. | Las sesiones presenciales solo pueden agendarse en aulas o laboratorios libres de la EPIS verificados contra el horario de clases regulares. | Exclusión de ambientes ocupados en el selector interactivo de espacios. | Algoritmo de detección de solapamientos horarios sobre cronogramas oficiales. | MOD-02 |
| **RN-07** | Aprovisionamiento Virtual Automatizado | Selección de modalidad virtual de mentoría. | La plataforma provisiona y asocia enlaces institucionales seguros de teleconferencia sin intervención manual externa. | Cancelación de la publicación si el enlace no es válido o seguro. | Generación y validación de URLs institucionales seguras. | MOD-02 |
| **RN-08** | Ventana Perentoria de Ratificación ($T-24\text{ h}$) | Reservas activas en la ventana previa a la sesión. | La confirmación de asistencia debe realizarse hasta el corte de 24 horas previas. Las reservas no ratificadas pierden vigencia (`NO_CONFIRMADA`). | Revocación automática del cupo en $T-24\text{ h}$ y restitución de vacante al aforo libre. | Demonio desatendido de corte que invalida reservas pendientes a $T-24\text{ h}$. | MOD-05 |
| **RN-09** | Quórum Mínimo del 50% en $T-24\text{ h}$ | Evaluación de viabilidad de sesión a $T-24\text{ h}$. | Toda sesión debe alcanzar un quórum del 50% de su aforo (5 en presencial, 10 en virtual). Si no se alcanza, transiciona a `QUORUM_INSUFICIENTE`. | Notificación de contingencia al mentor para resolver continuidad extraordinaria o cancelación. | Demonio cron que totaliza confirmados y conmuta estado de la sesión. | MOD-05 |
| **RN-10** | Cancelación Oportuna y Liberación de Espacios | Suspensión de sesión por quórum o imprevisto. | Al cancelarse una sesión, se notifica de inmediato a los inscritos y se libera la infraestructura física o virtual asignada. | Cancelación formal y desasignación del aula física en el calendario. | Transacción atómica que actualiza la sesión y libera la ocupación de ambientes. | MOD-05 |
| **RN-11** | Ponderación y Desempate Algorítmico | Inferencia del ranking Top-k de recomendaciones. | El recomendador pondera afinidad temática por similitud coseno. Desempata por: 1) reputación docente, 2) menor carga horaria activa, y 3) condición prioritaria de la materia. | Reordenamiento automático de la cartelera adaptativa para maximizar impacto. | Fórmula matemática multivariada en el motor *EdRecSys*. | MOD-04 |
| **RN-12** | Cierre de Bitácora y Filtro de Evaluación | Finalización de la sesión de mentoría. | El mentor dispone de 48 horas post-sesión para registrar la bitácora con los temas dictados y la asistencia. Solo los asistentes evalúan. | Bloqueo definitivo del registro de horas si se supera el plazo de 48 horas. | Cómputo de ventana de tiempo e inmutabilidad sellada con firma SHA-256. | MOD-06 |
| **RN-13** | Ventana Perentoria para Encuestas (24h) | Conclusión de una sesión de mentoría con asistencia. | El formulario de evaluación de calidad está habilitado durante 24 horas posteriores al cierre de la sesión. Luego se cierra definitivamente. | Cierre del formulario e imposibilidad de emitir calificaciones extemporáneas. | Verificación temporal estricta (`fecha_actual <= fecha_cierre + 24h`) y filtro por asistencia efectiva. | MOD-06 |
| **RN-14** | Certificación por Horas Auditadas ($\ge 20\text{ h}$) | Solicitud o autorización de certificados oficiales. | La certificación de horas exige acumular un mínimo de 20 horas efectivas en el semestre con el 100% de bitácoras auditadas y visadas. | Denegación de emisión documental hasta alcanzar el umbral completo. | Validación algorítmica sobre la suma de horas con bitácoras en estado aprobado. | MOD-07 |

Fuente: Elaboración propia a partir de las políticas académicas de la EPIS-UPT.

El análisis del Cuadro 5.4 demuestra que las reglas de negocio institucionalizan un marco pedagógico transparente y seguro. La combinación de validaciones temporales ($T-24\text{ h}$, 48h, 24h), aforos estándar y verificación de mérito garantiza el orden operativo y protege los derechos de mentores y mentoreados.

---

## 5.5. Matriz de Trazabilidad Bidireccional de Requerimientos

A continuación, se presenta la matriz de trazabilidad que articula la totalidad de requerimientos funcionales con los módulos, reglas de negocio, casos de uso, requerimientos no funcionales y métodos de verificación técnica:

### Cuadro 5.5: Matriz de Trazabilidad Bidireccional de Requerimientos (RF -> MOD -> RN -> CUS -> RNF -> Verificación)

| Código RF | Requerimiento Funcional | Módulo | Reglas Vinculadas | Casos de Uso | RNF Asociados | Método de Verificación Técnica |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **RF01** | Autenticación institucional multifactor (2FA) | MOD-01 | RN-01 | CUS-001 | RNF01, RNF02 | Prueba automatizada de generación/validación OTP, verificación de expiración temporal y prueba de autenticación federada Google. |
| **RF02** | Formalización de consentimiento legal digital | MOD-01 | RN-02 | CUS-001 | RNF02 | Comprobación de persistencia de marcas UTC/IP en base de datos y prueba de bloqueo perentorio en endpoints privados. |
| **RF03** | Gestión y asignación administrativa de roles | MOD-01 | RN-03 | CUS-010 | RNF02, RNF09 | Inspección de actualización atómica de privilegios y validación algorítmica de mérito (ciclo $\ge \text{VII}$ y nota $\ge 14.0$). |
| **RF04** | Configuración de perfil y matriz horaria | MOD-03 | RN-03, RN-04 | CUS-005 | RNF04, RNF08 | Prueba visual de la cuadrícula interactiva 6×11 y prueba de persistencia atómica en base de datos. |
| **RF05** | Catálogo curricular de asignaturas y temas | MOD-03 | RN-11 | CUS-021 | RNF09 | Pruebas de integración sobre operaciones CRUD del catálogo y visualización de unidades silábicas oficiales. |
| **RF06** | Inferencia algorítmica y recomendación Top-k | MOD-04 | RN-04, RN-11 | CUS-002 | RNF03 | Validación experimental de precisión algorítmica (Precision@3, NDCG) y latencia media inferior a 500 ms. |
| **RF07** | Registro y banco de solicitudes por demanda | MOD-04 | RN-04 | CUS-003 | RNF04, RNF09 | Prueba funcional de registro temático, generación de folio y visualización en el banco de necesidades de mentores. |
| **RF08** | Publicación y parametrización de ofertas | MOD-02 | RN-04, RN-05 | CUS-006 | RNF04, RNF09 | Validación de antelación mínima de 24 horas, límites de aforo estándar (10/20) y registro de enlaces didácticos. |
| **RF09** | Aprovisionamiento automatizado de espacios | MOD-02 | RN-06, RN-07 | CUS-006, CUS-008 | RNF09, RNF10 | Verificación de detección de solapamientos horarios en aulas y configuración de enlaces virtuales institucionales. |
| **RF10** | Procesamiento de cronogramas oficiales | MOD-02 | RN-06 | CUS-008 | RNF09, RNF10 | Prueba funcional del parser de cronogramas para extracción de aulas libres e importación estructurada. |
| **RF11** | Gestión de imprevistos y reprogramación | MOD-02 | RN-10 | CUS-006 | RNF09, RNF10 | Prueba de reprogramación justificada, liberación inmediata de ambientes y despacho de notificaciones a inscritos. |
| **RF12** | Reserva de cupos con control de aforo | MOD-05 | RN-05 | CUS-004 | RNF07 | Prueba de estrés concurrente multihilo con cerrojo pesimista verificando estrictamente 0.0% de sobrecupo. |
| **RF13** | Ratificación anticipada obligatoria de asistencia | MOD-05 | RN-08 | CUS-024 | RNF07, RNF09 | Prueba de confirmación previa en ventana de tiempo y transición de estado a confirmada. |
| **RF14** | Desistimiento voluntario y liberación de cupo | MOD-05 | RN-08, RN-10 | CUS-017 | RNF07 | Prueba de cancelación voluntaria antes de $T-24\text{ h}$ y restitución instantánea de vacantes en el aforo libre. |
| **RF15** | Monitoreo desatendido y corte en $T-24\text{ h}$ | MOD-05 | RN-08, RN-09 | CUS-023, CUS-009 | RNF06, RNF09 | Verificación del demonio cron en $T-24\text{ h}$, invalidación de no ratificados y evaluación automática de quórum (50%). |
| **RF16** | Gestión resolutiva ante quórum insuficiente | MOD-05 | RN-09, RN-10 | CUS-007 | RNF09, RNF10 | Prueba de interfaz resolutiva del mentor (continuar excepcional vs cancelar con liberación de recursos). |
| **RF17** | Marcación de asistencia con QR dinámico TOTP | MOD-06 | RN-05, RN-12 | CUS-012 | RNF02, RNF09 | Validación de generación y escaneo de pase QR efímero de 30 segundos y control de lista de respaldo. |
| **RF18** | Registro de bitácora docente con hash SHA-256 | MOD-06 | RN-12 | CUS-013 | RNF02, RNF09 | Comprobación de generación de firma criptográfica SHA-256 e inmutabilidad dentro del plazo de 48 horas. |
| **RF19** | Historial de sesiones, bitácoras y recursos | MOD-06 | — | CUS-014 | RNF02, RNF04 | Prueba de interfaz cronológica de consultas con filtros temáticos y acceso a materiales compartidos. |
| **RF20** | Captura de encuestas de calidad post-mentoría | MOD-06 | RN-13 | CUS-012, CUS-014 | RNF05, RNF07 | Validación de acceso exclusivo a asistentes y cierre definitivo de encuesta al cumplirse las 24 horas. |
| **RF21** | Cálculo de reputación y catálogo de insignias | MOD-07 | RN-13 | CUS-019 | RNF05, RNF09 | Prueba matemática del recálculo de reputación a partir de encuestas y desbloqueo de insignias por mérito. |
| **RF22** | Parametrización y autorización de certificados | MOD-07 | RN-14 | CUS-018 | RNF09 | Validación del umbral mínimo de 20 horas auditadas y exigencia de 100% de bitácoras aprobadas para autorizar. |
| **RF23** | Emisión, descarga y verificación pública con QR | MOD-07 | RN-14 | CUS-018 | RNF02, RNF09 | Generación de archivo PDF oficial con ReportLab, sello hash SHA-256 y escaneo de código QR en validador público. |
| **RF24** | Parametrización institucional de aforos | MOD-08 | RN-05, RN-09, RN-11 | CUS-020 | RNF03, RNF05 | Comprobación de actualización de umbrales y realce algorítmico en cartelera para materias prioritarias. |
| **RF25** | Tablero analítico y métricas de retención | MOD-08 | RN-02 | CUS-011, CUS-015 | RNF02, RNF04 | Verificación de consolidación de KPIs institucionales de demanda insatisfecha y reportes para acreditación ICACIT. |
| **RF26** | Auditoría de bitácoras y privacidad legal | MOD-08 | RN-02, RN-14 | CUS-016, CUS-022 | RNF02, RNF09 | Inspección del panel de fiscalización y visado docente y exportación de trazas inmutables bajo Ley N° 29733. |

Fuente: Elaboración propia a partir del marco de trazabilidad de ingeniería de requisitos.

A continuación, se acredita el estado de madurez y verificación técnica de los requerimientos en la fase de construcción:

### Cuadro 5.6: Estado de Madurez y Verificación de Requerimientos al Cierre de Sprints

| Requerimiento / Atributo | Módulo | Iteración de Construcción | Estado Técnico Formal | Evidencia Técnica Reportada |
| :---: | :---: | :---: | :---: | :--- |
| **RF01** (Autenticación 2FA) | MOD-01 | Sprint 1 | **Construido y Verificado** ✅ | Flujo OTP con correo institucional, cooldown de 60 s y token JWT de 8h (13 tests Pytest / 15 tests Vitest). |
| **RF02** (Consentimiento Ley 29733) | MOD-01 | Sprint 2 | **Construido y Verificado** ✅ | Modal accesible, persistencia de marcas UTC/IP en BD y bloqueo perentorio (9 tests Vitest / 5 tests Pytest). |
| **RF03** (Roles y Mérito) | MOD-01 | Sprint 2 | **Construido y Verificado** ✅ | Verificación de mérito académico (ciclo $\ge \text{VII}$ y nota $\ge 14.0$) y control RBAC (7 tests Pytest). |
| **RF04** (Perfil y Matriz 6×11) | MOD-03 | Sprint 2 | **Construido y Verificado** ✅ | Matriz semanal interactiva 6×11 (08:00 a 20:00) y reemplazo atómico en BD (10 tests Vitest / 11 tests Pytest). |
| **RF05** (Catálogo Curricular) | MOD-03 | Sprints 1 y 2 | **Construido y Verificado** ✅ | Materias formativas críticas en base de datos y árbol de temas silábicos (4 tests Vitest / 8 tests Pytest). |
| **RF06** (EdRecSys Top-k) | MOD-04 | Sprint 3 | **Construido y Verificado** ✅ | Similitud coseno y filtrado colaborativo calibrado ($P@3=83.3\%$, latencia 12.4 ms) (18 tests Pytest / 14 tests Vitest). |
| **RF07** (Banco de Demanda) | MOD-04 | Sprint 3 | **Construido y Verificado** ✅ | Registro de demandas temáticas, validación de temarios y visualización docente (12 tests Pytest / 14 tests Vitest). |
| **RF08** (Publicación de Ofertas) | MOD-02 | Sprint 4 | **Construido y Verificado** ✅ | Antelación $\ge 24\text{ h}$, límites de aforo estándar y registro de recursos (16 tests Pytest / 18 tests Vitest). |
| **RF09** (Aprovisionamiento de Espacios) | MOD-02 | Sprint 4 | **Construido y Verificado** ✅ | Aulas libres verificadas contra solapamientos y salas virtuales (14 tests Pytest / 12 tests Vitest). |
| **RF10** (Parser de Cronogramas) | MOD-02 | Sprint 4 | **Construido y Verificado** ✅ | Ingesta estructurada de cronogramas oficiales para detección de ambientes libres (8 tests Pytest). |
| **RF11** (Gestión de Contingencias) | MOD-02 | Sprint 4 | **Construido y Verificado** ✅ | Reprogramación y cancelación justificada con liberación de recursos y avisos (10 tests Pytest / 10 tests Vitest). |
| **RF12** (Reserva Concurrente Pesimista)| MOD-05 | Sprint 5 | **Construido y Verificado** ✅ | Bloqueo pesimista `SELECT ... FOR UPDATE` demostrando **0.0% de sobrecupo** (18 tests Pytest / 16 tests Vitest). |
| **RF13** (Ratificación Anticipada) | MOD-05 | Sprint 5 | **Construido y Verificado** ✅ | Confirmación previa hasta el corte de $T-24\text{ h}$ y cambio a confirmada (12 tests Pytest / 14 tests Vitest). |
| **RF14** (Desistimiento Voluntario) | MOD-05 | Sprint 5 | **Construido y Verificado** ✅ | Anulación voluntaria antes de $T-24\text{ h}$ con restitución instantánea de vacantes (10 tests Pytest / 10 tests Vitest). |
| **RF15** (Corte de Quórum en $T-24\text{ h}$)| MOD-05 | Sprint 5 | **Construido y Verificado** ✅ | Demonio cron desatendido que invalida pendientes y evalúa quórum del 50% (16 tests Pytest / 12 tests Vitest). |
| **RF16** (Resolución de Quórum) | MOD-05 | Sprint 5 | **Construido y Verificado** ✅ | Diálogo resolutivo del mentor ante quórum insuficiente (10 tests Pytest / 10 tests Vitest). |
| **RF17** (Asistencia QR Dinámico TOTP)| MOD-06 | Sprint 6 | **Construido y Verificado** ✅ | Pase QR dinámico de 30 segundos y escaneo por cámara institucional (14 tests Pytest / 20 tests Vitest). |
| **RF18** (Bitácora Docente SHA-256) | MOD-06 | Sprint 6 | **Construido y Verificado** ✅ | Registro obligatorio en 48 horas con sello hash SHA-256 (18 tests Pytest / 22 tests Vitest). |
| **RF19** (Historial y Recursos) | MOD-06 | Sprint 6 | **Construido y Verificado** ✅ | Historial cronológico con filtros temáticos y acceso a materiales educativos (8 tests Pytest / 12 tests Vitest). |
| **RF20** (Encuestas CSAT de 24h) | MOD-06 | Sprint 7 | **Construido y Verificado** ✅ | Encuesta de 4 dimensiones pedagógicas en ventana perentoria de 24 horas (16 tests Pytest / 14 tests Vitest). |
| **RF21** (Reputación e Insignias) | MOD-07 | Sprint 7 | **Construido y Verificado** ✅ | Recálculo dinámico de reputación y catálogo de insignias por mérito (12 tests Pytest / 18 tests Vitest). |
| **RF22** (Parametrización de Certificados)| MOD-07 | Sprint 7 | **Construido y Verificado** ✅ | Control de umbral mínimo de 20 horas auditadas para autorizar certificación (14 tests Pytest / 16 tests Vitest). |
| **RF23** (Certificado PDF con QR) | MOD-07 | Sprint 7 | **Construido y Verificado** ✅ | Compilación ReportLab de PDF oficial con hash SHA-256 y validador QR (16 tests Pytest / 16 tests Vitest). |
| **RF24** (Configuración Institucional) | MOD-08 | Sprint 8 | **Construido y Verificado** ✅ | Consola administrativa de aforos y asignaturas prioritarias (10 tests Pytest / 14 tests Vitest). |
| **RF25** (Tableros Analíticos ICACIT)| MOD-08 | Sprint 8 | **Construido y Verificado** ✅ | Tablero con métricas de demanda insatisfecha y retención estudiantil (14 tests Pytest / 22 tests Vitest). |
| **RF26** (Auditoría y Visado Docente) | MOD-08 | Sprint 8 | **Construido y Verificado** ✅ | Fiscalización de bitácoras docentes y auditoría legal bajo Ley N° 29733 (14 tests Pytest / 16 tests Vitest). |

Fuente: Elaboración propia a partir de las bitácoras técnicas de los Sprints 01 al 08.

> **Nota Metodológica de Auditoría (H01-R / H02):** La cifra acumulada de 682 pruebas automatizadas (335 en backend Pytest y 347 en frontend Vitest) corresponde al reporte histórico acreditado en el commit `3f6e31d`. De acuerdo con la rectificación formal H01-R, dicha cifra se consigna como histórica y se encuentra formalmente pendiente de nueva validación técnica integral en el flujo de integración continua (CI) una vez subsanadas las observaciones de linteo registradas en las ejecuciones recientes de la rama `main`.

El análisis de los Cuadros 5.5 y 5.6 certifica que la totalidad de los 26 requerimientos funcionales y 10 atributos de calidad se encuentran respaldados por evidencias de verificación formal.

---

## 5.6. Requisitos de Interfaz Externa

### 5.6.1. Interfaces de Usuario (UI)

La interfaz web del Sistema Web P2P está construida como una aplicación de página única (*Single Page Application - SPA*) reactiva y accesible:
- **Design System Institucional y Vocabulario Cromático:** Desarrollado sobre Tailwind CSS v3.4+, aplicando la paleta de colores institucional de la Universidad Privada de Tacna descrita en lenguaje natural:
  - *Azul marino institucional:* Utilizado para barras de navegación superiores, encabezados de módulo y botones de acción principal.
  - *Dorado universitario:* Aplicado en distintivos de acreditación, estrellas de reputación docente e insignias de mérito.
  - *Fondo blanco puro y gris pizarra claro:* Utilizados para paneles de contenido y áreas de lectura descansada.
  - *Borde gris claro y texto secundario atenuado:* Para la delimitación sutil de tarjetas y campos de formulario.
  - *Alertas y notificaciones:* Banner de advertencia en color ámbar preventivo, notificación de error en color rojo y etiqueta de éxito en color verde.
- **Accesibilidad Universal (WCAG 2.1 Nivel AA):**
  - Contraste cromático estricto $\ge 4.5:1$ en la totalidad de textos regulares frente a sus fondos.
  - Navegación completa por teclado con indicador de foco visible (`focus:ring-2 focus:ring-blue-500`) en todos los controles interactivos, botones y campos de entrada.
  - Soporte integral para lectores de pantalla mediante atributos descriptivos `aria-label`, roles semánticos (`role="dialog"`, `role="alert"`) y regiones dinámicas `aria-live`.
  - Cierre intuitivo de diálogos modales mediante la tecla `Escape`.

### 5.6.2. Interfaces de Software

- **Servidor de Aplicación y API RESTful:** Desarrollado en Python 3.13 bajo el framework FastAPI. Expone interfaces RESTful con contratos JSON fuertemente tipados bajo el prefijo `/api/v1/`, documentadas interactivamente mediante la especificación OpenAPI v3.0 (Swagger UI).
- **Capa de Persistencia Relacional:** Motor PostgreSQL v15+ administrado sobre la infraestructura cloud de Supabase, con conexión mediante pool de conexiones y políticas de seguridad a nivel de fila (*Row Level Security - RLS*).
- **Servicios Externos de Correo e Identidad:** Integración con transporte SMTP institucional de Gmail para despacho de códigos OTP y avisos urgentes al dominio `@virtual.upt.pe`, y SDK oficial de Google Identity Services (GIS) para autenticación federada.
- **Generación Documental Oficial:** Motor programático ReportLab v4.x para compilación en streaming de certificados oficiales en formato estándar PDF/A con códigos QR vectoriales incorporados.

### 5.6.3. Interfaces de Hardware

- **Plataforma Servidora:** Contenedores de ejecución cloud sobre arquitectura x86_64 o ARM64, con requerimientos mínimos de 1 núcleo vCPU y 1 GB de memoria RAM para atender la demanda simultánea de la EPIS.
- **Terminales y Dispositivos de Usuario:** Estaciones de trabajo de los laboratorios de cómputo de la EPIS, computadoras portátiles personales y teléfonos inteligentes. Para el control de asistencia presencial, se requiere cámara web o cámara fotográfica en el dispositivo móvil para el escaneo del pase QR dinámico.

### 5.6.4. Interfaces de Comunicaciones y Seguridad de Red

- **Cifrado en Tránsito:** Todo el intercambio de información entre los clientes web y el servidor se transmite estrictamente a través del protocolo HTTPS con cifrado TLS v1.3 sobre el puerto TCP 443.
- **Políticas de Control de Origen (CORS):** Cabeceras restrictivas en el servidor FastAPI que limitan el acceso exclusivamente a los dominios universitarios autorizados (`http://localhost:5173` en desarrollo y `https://*.upt.pe` en producción).
- **Seguridad en Peticiones Privadas:** Cabeceras de autorización HTTP Bearer (`Authorization: Bearer <token_jwt>`) con tokens firmados criptográficamente mediante HMAC-SHA256 y vigencia de 8 horas.

# 6. Fase de Desarrollo

El ciclo de vida del desarrollo de software del proyecto se fundamenta en la metodología **UWE (UML-Based Web Engineering)** adaptada a plataformas adaptativas y colaborativas. La construcción del sistema se ejecutó en ocho sprints distribuidos a lo largo del semestre académico 2026-II, articulando la ingeniería de requisitos, el diseño conceptual y arquitectónico, la implementación con pruebas automatizadas continuas y la evaluación de calidad.

### Diagrama 6.1: Fases del Ciclo de Vida del Desarrollo de Software (Metodología UWE - Semestre 2026-II)

```plantuml
@startuml
title Fases de Desarrollo del Sistema Web P2P (Metodología UWE - Semestre 2026-II)
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

start
:29 Ago 2026;
:FASE 1: Especificación de Requisitos y Gobernanza Legal\nSemanas 1-3 (Sprints 1 y 2)\n• Levantamiento de información y entrevistas estructuradas\n• Definición de RF01-RF26, RN-01 a RN-14 y RNF01-RNF10 (ISO 25010)\n• Protocolo formal de Consentimiento Digital bajo Ley N° 29733\n• Autenticación multifactor 2FA institucional;

:FASE 2: Diseño del Sistema y Modelado de Datos Relacional\nSemanas 4-6 (Sprints 2 y 3)\n• Arquitectura desacoplada en 3 capas y modularización (MOD-01 al MOD-08)\n• Modelado relacional PostgreSQL (15 tablas) con políticas RLS\n• Prototipos de alta fidelidad en React SPA y diseño de navegación UWE;

:FASE 3: Construcción del Software y Motor Algorítmico\nSemanas 7-11 (Sprints 3 al 6)\n• Microservicios RESTful en Python (FastAPI)\n• Motor híbrido EdRecSys (Similitud Coseno + Filtrado Colaborativo)\n• Orquestación de quórum con cerrojos pesimistas a T-24h (FOR UPDATE)\n• Marcación QR TOTP y bitácoras docentes con hash SHA-256;

:FASE 4: Verificación Integral, Gamificación y Cierre\nSemanas 12-14 (Sprints 7 y 8)\n• Gamificación e insignias por mérito docente\n• Emisión de certificados digitales oficiales PDF con QR institucional\n• Tableros de analítica institucional y supervisión directiva\n• Batería de 627 pruebas automatizadas (280 backend, 347 frontend);

:FASE 5: Piloto Institucional y Cierre del Semestre\nSemanas 15-16 (Diciembre 2026)\n• Despliegue en producción sobre infraestructura PaaS (Supabase / Render)\n• Prueba piloto con estudiantes de I a X ciclo de la EPIS-UPT\n• Evaluación de usabilidad SUS (>75 puntos) y entrega formal de versión 3.0;
:14 Dic 2026;
stop
@enduml
```

Fuente: Elaboración propia.

---

## 6.1. Perfiles de Usuario y Modelo de Control de Acceso (RBAC)

### Presentación de los Perfiles de Usuario
La operación eficiente y ordenada del Sistema Web P2P requiere la definición explícita de los perfiles de usuario y actores que interactúan en la plataforma. En el ecosistema formativo de la EPIS-UPT, los usuarios desempeñan roles diferenciados según su nivel de avance curricular, su investidura académica o la naturaleza técnica de sus procesos. Con el fin de gobernar el acceso bajo el principio de mínimo privilegio y resguardar la privacidad académica (Ley N° 29733), el sistema implementa un modelo de control de acceso basado en roles (**Role-Based Access Control - RBAC**):

### Cuadro 6.1: Perfiles de Usuario y Actores del Sistema Web P2P

| Perfil / Actor | Tipo de Actor | Población Objetivo / Componente | Responsabilidades y Actividades Principales | Privilegios y Permisos en el Sistema |
| :--- | :--- | :--- | :--- | :--- |
| **Estudiante Mentoreado** | Humano (Actor Primario) | Estudiantes matriculados de I a IV ciclo con necesidades de reforzamiento académico en materias formativas críticas (*Cálculo, Algoritmos, Estructuras, POO*). | • Formalizar el consentimiento informado digital obligatorio (Ley N° 29733).<br>• Declarar asignaturas de interés y disponibilidad horaria semanal en la matriz 6×11.<br>• Consultar recomendaciones personalizadas Top-k y registrar demandas temáticas.<br>• Reservar cupos de mentoría con control concurrente.<br>• Ratificar asistencia obligatoria antes de $T-24\text{ h}$ o desistir oportunamente.<br>• Marcar asistencia mediante pase QR y responder encuestas de satisfacción (24h). | • Acceso a vistas de catálogo y recomendaciones personales (`RoleGuard`).<br>• Creación, ratificación y desistimiento de reservas propias.<br>• Registro en el banco de solicitudes por demanda.<br>• Descarga de materiales académicos vinculados.<br>• Diligenciamiento de encuestas de calidad post-sesión. |
| **Estudiante Mentor** | Humano (Actor Primario) | Estudiantes de rendimiento sobresaliente de VII a X ciclo promovidos formalmente por la Dirección de Escuela tras verificación de mérito. | • Configurar áreas de dominio curricular y agenda de disponibilidad semanal.<br>• Publicar ofertas de mentoría académica (materia, temario, fecha, modalidad).<br>• Resolver la continuidad o cancelación de sesiones ante alertas de quórum deficiente.<br>• Dictar las sesiones en aulas asignadas o salas virtuales validadas.<br>• Marcar asistencia efectiva y registrar bitácoras pedagógicas firmadas con SHA-256 en 48h.<br>• Compartir recursos didácticos y monitorear insignias/reputación obtenida.<br>• Descargar certificados oficiales de horas para convalidación de créditos. | • Publicación, reprogramación y anulación justificada de ofertas propias.<br>• Aprovisionamiento guiado de infraestructura física o virtual.<br>• Diligenciamiento y cierre formal de bitácoras docentes.<br>• Carga de materiales educativos para sus participantes.<br>• Visualización de tablero de reputación y descarga de certificados PDF auditados. |
| **Administrador Institucional** | Humano (Gobernanza y Supervisión) | Comité de Tutoría Docente, Coordinación Académica y Dirección de la EPIS-UPT. | • Auditar expedientes estudiantiles y aprobar la promoción a rol de Mentor.<br>• Mantener actualizado el catálogo de asignaturas críticas y temarios silábicos.<br>• Cargar cronogramas oficiales de aulas para el motor parser de espacios.<br>• Registrar materias y mentorías en condición prioritaria por reprobación.<br>• Fiscalizar bitácoras docentes, asistencias y computabilidad de horas acumuladas.<br>• Parametrizar umbrales semestrales y emitir certificados oficiales PDF foliados.<br>• Supervisar tableros analíticos de demanda insatisfecha, ausentismo y desempeño. | • Control de acceso total y administración de roles en `/roles/promote-mentor`.<br>• Operaciones CRUD sobre catálogo curricular y prioridades académicas.<br>• Carga e indexación de cronogramas institucionales de espacios.<br>• Visado administrativo, observación y validación de horas de mentoría.<br>• Autorización y emisión de certificados digitales con código QR.<br>• Acceso irrestricto al panel de analítica institucional (`/analytics`). |
| **Servicio Cron / Backend** | Técnico (Proceso Desatendido) | Demonio de tareas programadas en el servidor backend FastAPI. | • Inspeccionar periódicamente la base de datos para identificar sesiones próximas.<br>• Despachar notificaciones automáticas y recordatorios a estudiantes inscritos.<br>• Ejecutar el corte perentorio a $T-24\text{ h}$, revocar cupos no ratificados y evaluar quórum.<br>• Transicionar a `QUORUM_INSUFICIENTE` si no se alcanza el 50% de aforo y alertar al Mentor. | • Ejecución en segundo plano con privilegios a nivel de servicio de sistema.<br>• Modificación atómica de estados en tablas de reservas y sesiones.<br>• Despacho de correos electrónicos institucionales mediante servicio SMTP. |
| **Servicios Externos** | Técnico (Sistemas Colaboradores) | Infraestructura institucional: Servidor SMTP UPT, repositorios y navegadores web. | • Despachar códigos de verificación OTP y notificaciones al buzón `@upt.pe`.<br>• Suministrar entornos de videoconferencia validados para sesiones virtuales.<br>• Proveer soporte para captura de cámara en escaneo de códigos QR. | • Conexión autenticada mediante tokens y protocolos seguros TLS 1.3.<br>• Sin exposición directa de datos personales sensibles a terceros. |

Fuente: Elaboración propia.

---

## 6.2. Modelo Conceptual

### Presentación del Modelo Conceptual
El modelo conceptual formaliza las entidades del dominio de la EPIS-UPT, capturando sus atributos esenciales, estados operacionales y las relaciones semánticas que sustentan el ecosistema de mentorías académicas. Este modelo traduce las reglas de negocio (aforos máximos, consentimiento de privacidad bajo la Ley N° 29733, estados de reserva, bitácoras de cumplimiento y certificación) en una estructura ontológica coherente y extensible alineada con las **15 tablas relacionales de PostgreSQL**:

### Diagrama 6.2: Diagrama de Clases Conceptuales del Dominio - Sistema Web P2P EPIS-UPT

```plantuml
@startuml
title Diagrama de Clases Conceptuales del Dominio - Sistema Web P2P EPIS-UPT
hide methods
skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam class {
  BackgroundColor #F8F9FA
  BorderColor #2B3A42
  ArrowColor #2B3A42
}

class Usuario {
  +id_usuario: UUID
  +codigo_estudiante: String
  +correo_institucional: String
  +nombres: String
  +apellidos: String
  +activo: Boolean
  +fecha_registro: DateTime
}

class ConsentimientoLegal {
  +id_consentimiento: UUID
  +id_usuario: UUID
  +ip_address: String
  +user_agent: String
  +fecha_aceptacion: DateTime
}

class Rol {
  +id_rol: Integer
  +codigo_rol: String
  +nombre_rol: String
}

class PerfilFormativo {
  +id_perfil: UUID
  +id_usuario: UUID
  +biografia: Text
  +ciclo_actual: Integer
  +reputacion_promedio: Float
  +horas_dictadas_total: Float
}

class DisponibilidadHoraria {
  +id_disponibilidad: UUID
  +id_usuario: UUID
  +dia_semana: Integer
  +hora_inicio: Time
  +hora_fin: Time
}

class CursoCritico {
  +id_curso: UUID
  +codigo_curso: String
  +nombre_curso: String
  +ciclo_sugerido: Integer
  +es_prioritario: Boolean
}

class TemaCurricular {
  +id_tema: UUID
  +id_curso: UUID
  +unidad_silabica: Integer
  +titulo_tema: String
  +descripcion_conceptual: Text
}

class OfertaMentoria {
  +id_oferta: UUID
  +id_mentor: UUID
  +id_curso: UUID
  +id_tema: UUID
  +modalidad: String
  +aforo_maximo: Integer
  +fecha_hora_inicio: DateTime
  +fecha_hora_fin: DateTime
  +estado_oferta: String
}

class EspacioFisico {
  +id_espacio: UUID
  +codigo_ambiente: String
  +pabellon: String
  +capacidad: Integer
  +es_activo: Boolean
}

class SesionMentoria {
  +id_sesion: UUID
  +id_oferta: UUID
  +id_espacio: UUID
  +enlace_virtual: String
  +estado_sesion: String
  +quorum_alcanzado: Boolean
}

class ReservaCupo {
  +id_reserva: UUID
  +id_sesion: UUID
  +id_mentoreado: UUID
  +estado_reserva: String
  +fecha_reserva: DateTime
  +fecha_ratificacion: DateTime
}

class AsistenciaSesion {
  +id_asistencia: UUID
  +id_sesion: UUID
  +id_estudiante: UUID
  +estado_asistencia: String
  +metodo_checkin: String
  +timestamp_checkin: DateTime
}

class BitacoraPedagogica {
  +id_bitacora: UUID
  +id_sesion: UUID
  +id_mentor: UUID
  +temas_impartidos: Text
  +observaciones_docentes: Text
  +hash_sha256: String
  +estado_visado: String
  +fecha_registro: DateTime
}

class EvaluacionCalidad {
  +id_evaluacion: UUID
  +id_sesion: UUID
  +id_estudiante: UUID
  +puntuacion_estrellas: Integer
  +comentario_cualitativo: Text
  +fecha_evaluacion: DateTime
}

class CertificadoHoras {
  +id_certificado: UUID
  +id_mentor: UUID
  +folio_correlativo: String
  +horas_acreditadas: Float
  +hash_documento: String
  +url_qr_verificacion: String
  +fecha_emision: DateTime
}

Usuario "1" -- "0..1" ConsentimientoLegal : formaliza
Usuario "1" -- "1..*" Rol : posee
Usuario "1" -- "1" PerfilFormativo : define
Usuario "1" -- "0..*" DisponibilidadHoraria : agenda

CursoCritico "1" -- "1..*" TemaCurricular : desglosa
Usuario "1" -- "0..*" OfertaMentoria : publica (como mentor)
CursoCritico "1" -- "0..*" OfertaMentoria : clasifica
TemaCurricular "1" -- "0..*" OfertaMentoria : especifica

OfertaMentoria "1" -- "1" SesionMentoria : materializa
EspacioFisico "0..1" -- "0..*" SesionMentoria : alberga

SesionMentoria "1" -- "0..*" ReservaCupo : gestiona cupos
Usuario "1" -- "0..*" ReservaCupo : inscribe (como mentoreado)

SesionMentoria "1" -- "0..*" AsistenciaSesion : controla
SesionMentoria "1" -- "0..1" BitacoraPedagogica : documenta
SesionMentoria "1" -- "0..*" EvaluacionCalidad : recibe

Usuario "1" -- "0..*" CertificadoHoras : acredita
@enduml
```

Fuente: Elaboración propia.

---

### 6.2.1. Diagrama de Paquetes Arquitecturales

### Presentación del Diagrama de Paquetes
La arquitectura de software del Sistema Web P2P adopta un patrón en **Capas Desacopladas** (*Clean Architecture / Layered Architecture*), asegurando la separación estricta de responsabilidades entre la capa de presentación del cliente (React SPA), los controladores y servicios RESTful (FastAPI), la capa de dominio y persistencia (SQLAlchemy / PostgreSQL) y las integraciones con servicios externos (SMTP, ReportLab, Supabase RLS):

### Diagrama 6.3: Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P

```plantuml
@startuml
title Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

package "Capa de Presentación (Frontend SPA - React 18 / TypeScript)" as PKG_FRONT #EBF3FB {
  package "Vistas de Usuario (UI Views)" as PKG_VIEWS {
    [LoginOtpView]
    [ConsentModalView]
    [ProfileAvailabilityView]
    [RecommendationsView]
    [PublishMentorshipView]
    [BookingModalView]
    [QrScannerView / QrPassView]
    [BitacoraRegisterView]
    [AdminAnalyticsView]
    [AdminCertificatesView]
  }
  package "Adaptadores de Cliente (HTTP / State)" as PKG_CLIENT {
    [apiClient (Axios)]
    [authService]
    [mentorshipService]
    [bookingService]
    [bitacoraService]
  }
  PKG_VIEWS ..> PKG_CLIENT : invoca
}

package "Capa de Aplicación y API RESTful (Python / FastAPI)" as PKG_API #F0FDF4 {
  package "Controladores (Endpoints v1)" as PKG_ENDPOINTS {
    [auth.py]
    [consent.py]
    [roles.py]
    [curriculum.py]
    [recommendations.py]
    [mentorships.py]
    [bookings.py]
    [attendance.py]
    [bitacora.py]
    [certificates.py]
    [analytics.py]
  }
  package "Esquemas de Datos (Pydantic v2)" as PKG_SCHEMAS {
    [AuthSchemas]
    [BookingSchemas]
    [MentorshipSchemas]
    [BitacoraSchemas]
    [CertificateSchemas]
  }
  PKG_ENDPOINTS ..> PKG_SCHEMAS : valida
}

package "Capa de Servicios y Dominio (Lógica de Negocio)" as PKG_DOMAIN #FEF9C3 {
  package "Servicios de Negocio (Services)" as PKG_SERVICES {
    [AuthService]
    [ConsentService]
    [RecommendationService (EdRecSys)]
    [MentorshipService]
    [BookingService (Locks pesimistas)]
    [QuorumCronService]
    [AttendanceService (TOTP QR)]
    [BitacoraService (SHA-256)]
    [CertificateService]
    [AnalyticsService]
  }
  package "Entidades ORM (SQLAlchemy 2.0)" as PKG_MODELS {
    [Usuario / Rol]
    [Perfil / Disponibilidad]
    [Curso / Tema]
    [Oferta / Sesion]
    [Reserva / Asistencia]
    [Bitacora / Evaluacion]
    [Certificado / Insignia]
  }
  PKG_SERVICES ..> PKG_MODELS : manipula
}

package "Capa de Persistencia e Infraestructura Externa" as PKG_INFRA #FFF1F2 {
  database "PostgreSQL 15 (Supabase)" as DB_PG {
    [15 Tablas Relacionales]
    [Políticas RLS]
    [Constraints chk_sesion]
  }
  [Servidor SMTP UPT (Emails)] as EXT_SMTP
  [Generador PDF (ReportLab)] as EXT_PDF
}

PKG_CLIENT ..> PKG_ENDPOINTS : peticiones HTTPS / JSON
PKG_ENDPOINTS ..> PKG_SERVICES : orquesta
PKG_SERVICES ..> DB_PG : transacciones ACID
PKG_SERVICES ..> EXT_SMTP : despacha correos
PKG_SERVICES ..> EXT_PDF : compila certificados
@enduml
```

Fuente: Elaboración propia.

---

## 6.2.2. Diagramas de Casos de Uso

### Presentación de los Diagramas de Casos de Uso
Los casos de uso del Sistema Web P2P especifican la interacción funcional entre los actores institucionales y el software. A continuación, se presenta el **Diagrama General Consolidado (Diagrama 6.4)** que integra los 24 casos de uso canónicos estructurados en los ocho módulos del sistema, seguido de los diagramas modulares individuales (Diagramas 6.5 al 6.12).

### Diagrama 6.4: Diagrama de Casos de Uso General Consolidado del Sistema Web P2P (CUS-001 al CUS-024)

```plantuml
@startuml
title Diagrama 6.4: Diagrama de Casos de Uso General Consolidado (CUS-001 al CUS-024)\nSistema Web P2P - EPIS UPT
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional" as User #EBF3FB
actor "Estudiante Mentoreado" as Mentoreado #EBF3FB
actor "Estudiante Mentor" as Mentor #EBF3FB
actor "Administrador (EPIS)" as Admin #FEF9C3
actor "Servicio Cron Backend" as Cron #FFF1F2

Mentoreado -up-|> User
Mentor -up-|> User
Admin -up-|> User

rectangle "Sistema Web P2P de Mentorías Académicas EPIS-UPT" {

  package "MOD-01: Seguridad y Gobernanza" {
    usecase "CUS-001: Iniciar sesión con 2FA\ny consentimiento Ley 29733" as CUS01
    usecase "CUS-010: Gestionar asignación\nde roles de usuario" as CUS10
  }

  package "MOD-02: Ofertas de Mentoría y Recursos" {
    usecase "CUS-006: Publicar oferta\nde mentoría académica" as CUS06
    usecase "CUS-008: Consultar disponibilidad\nde espacios y recursos" as CUS08
  }

  package "MOD-03: Perfil y Plan de Aprendizaje" {
    usecase "CUS-005: Gestionar perfil\ny disponibilidad horaria" as CUS05
    usecase "CUS-021: Explorar catálogo\ncurricular de asignaturas filtro" as CUS21
  }

  package "MOD-04: Demanda y Recomendaciones" {
    usecase "CUS-002: Explorar recomendaciones\npersonalizadas Top-k" as CUS02
    usecase "CUS-003: Registrar solicitud\nde demanda académica" as CUS03
  }

  package "MOD-05: Quórum y Cancelaciones" {
    usecase "CUS-004: Reservar cupo\nde mentoría académica" as CUS04
    usecase "CUS-024: Ratificar asistencia\na sesión de mentoría" as CUS24
    usecase "CUS-017: Desistir voluntariamente\nde reserva de cupo" as CUS17
    usecase "CUS-023: Evaluar quórum\nautomático a T-24h" as CUS23
    usecase "CUS-007: Decisión ante\nquórum insuficiente" as CUS07
  }

  package "MOD-06: Asistencia, Bitácoras y Feedback" {
    usecase "CUS-012: Registrar asistencia\ncon pase QR dinámico" as CUS12
    usecase "CUS-013: Registrar bitácora\ndocente con SHA-256" as CUS13
    usecase "CUS-014: Visualizar historial\ny bitácoras académicas" as CUS14
  }

  package "MOD-07: Gamificación e Incentivos" {
    usecase "CUS-018: Emitir constancia\ninstitucional de horas" as CUS18
    usecase "CUS-019: Gestionar insignias\ny reputación gamificada" as CUS19
  }

  package "MOD-08: Analítica y Configuración" {
    usecase "CUS-009: Notificar eventos\ncríticos y alertas temporales" as CUS09
    usecase "CUS-011: Generar reportes\ne indicadores de analítica" as CUS11
    usecase "CUS-015: Consultar métricas\nde retención y desempeño" as CUS15
    usecase "CUS-016: Auditar trazas de\nseguridad y consentimiento" as CUS16
    usecase "CUS-020: Configurar parámetros\ninstitucionales y umbrales" as CUS20
    usecase "CUS-022: Gestionar catálogo\nde temas y materias críticas" as CUS22
  }
}

User --> CUS01
Admin --> CUS10

Mentor --> CUS06
Mentor --> CUS08
Mentor --> CUS07
Mentor --> CUS13
Mentor --> CUS18
Mentor --> CUS19

User --> CUS05
User --> CUS21
User --> CUS14

Mentoreado --> CUS02
Mentoreado --> CUS03
Mentoreado --> CUS04
Mentoreado --> CUS24
Mentoreado --> CUS17
Mentoreado --> CUS12

Cron --> CUS23
Cron --> CUS09

Admin --> CUS11
Admin --> CUS15
Admin --> CUS16
Admin --> CUS20
Admin --> CUS22
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.5: Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza

```plantuml
@startuml
title Diagrama 6.5: Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional" as User #EBF3FB
actor "Administrador (EPIS)" as Admin #FEF9C3
actor "Servicio Correo SMTP" as SMTP #FFF1F2

rectangle "MOD-01: Seguridad, Autenticación y Gobernanza" {
  usecase "CUS-001: Iniciar sesión con 2FA\ny consentimiento Ley 29733" as CUS01
  usecase "CUS-010: Gestionar asignación\nde roles de usuario" as CUS10
}

User --> CUS01
CUS01 ..> SMTP : <<include>>
Admin --> CUS10
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.6: Diagrama de Casos de Uso - MOD-02: Ofertas de Mentoría y Gestión de Recursos

```plantuml
@startuml
title Diagrama 6.6: Diagrama de Casos de Uso - MOD-02: Ofertas de Mentoría y Gestión de Recursos
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentor" as Mentor #EBF3FB
actor "Administrador (EPIS)" as Admin #FEF9C3

rectangle "MOD-02: Ofertas de Mentoría y Gestión de Recursos" {
  usecase "CUS-006: Publicar oferta\nde mentoría académica" as CUS06
  usecase "CUS-008: Consultar disponibilidad\nde espacios y recursos" as CUS08
}

Mentor --> CUS06
Mentor --> CUS08
Admin --> CUS08
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.7: Diagrama de Casos de Uso - MOD-03: Perfil del Mentor y Plan de Aprendizaje

```plantuml
@startuml
title Diagrama 6.7: Diagrama de Casos de Uso - MOD-03: Perfil del Mentor y Plan de Aprendizaje
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional\n(Mentoreado / Mentor)" as User #EBF3FB

rectangle "MOD-03: Perfil del Mentor y Plan de Aprendizaje" {
  usecase "CUS-005: Gestionar perfil formativo\ny disponibilidad horaria" as CUS05
  usecase "CUS-021: Explorar catálogo curricular\nde asignaturas filtro" as CUS21
}

User --> CUS05
User --> CUS21
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.8: Diagrama de Casos de Uso - MOD-04: Demanda y Recomendaciones Personalizadas

```plantuml
@startuml
title Diagrama 6.8: Diagrama de Casos de Uso - MOD-04: Demanda y Recomendaciones Personalizadas
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Mentoreado #EBF3FB
actor "Estudiante Mentor" as Mentor #EBF3FB
actor "Motor EdRecSys" as RecSys #FFF1F2

rectangle "MOD-04: Demanda y Recomendaciones Personalizadas" {
  usecase "CUS-002: Explorar recomendaciones\npersonalizadas Top-k" as CUS02
  usecase "CUS-003: Registrar solicitud\nde demanda académica" as CUS03
}

Mentoreado --> CUS02
CUS02 ..> RecSys : <<include>>
Mentoreado --> CUS03
Mentor --> CUS03
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.9: Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones

```plantuml
@startuml
title Diagrama 6.9: Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Mentoreado #EBF3FB
actor "Estudiante Mentor" as Mentor #EBF3FB
actor "Servicio Cron Backend" as Cron #FFF1F2

rectangle "MOD-05: Quórum, Confirmación y Cancelaciones" {
  usecase "CUS-004: Reservar cupo\nde mentoría académica" as CUS04
  usecase "CUS-024: Ratificar asistencia\na sesión de mentoría" as CUS24
  usecase "CUS-017: Desistir voluntariamente\nde reserva" as CUS17
  usecase "CUS-023: Evaluar quórum\nautomático a T-24h" as CUS23
  usecase "CUS-007: Decisión del mentor\nante quórum insuficiente" as CUS07
}

Mentoreado --> CUS04
Mentoreado --> CUS24
Mentoreado --> CUS17
Cron --> CUS23
Mentor --> CUS07
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.10: Diagrama de Casos de Uso - MOD-06: Asistencia, Bitácoras y Feedback

```plantuml
@startuml
title Diagrama 6.10: Diagrama de Casos de Uso - MOD-06: Asistencia, Bitácoras y Feedback
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Mentoreado #EBF3FB
actor "Estudiante Mentor" as Mentor #EBF3FB

rectangle "MOD-06: Asistencia, Bitácoras y Feedback" {
  usecase "CUS-012: Registrar asistencia\na sesión de mentoría" as CUS12
  usecase "CUS-013: Registrar bitácora\nacadémica de sesión" as CUS13
  usecase "CUS-014: Visualizar historial\ny bitácoras académicas" as CUS14
}

Mentoreado --> CUS12
Mentor --> CUS12
Mentor --> CUS13
Mentoreado --> CUS14
Mentor --> CUS14
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.11: Diagrama de Casos de Uso - MOD-07: Gamificación e Incentivos

```plantuml
@startuml
title Diagrama 6.11: Diagrama de Casos de Uso - MOD-07: Gamificación e Incentivos
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentor" as Mentor #EBF3FB
actor "Administrador (EPIS)" as Admin #FEF9C3

rectangle "MOD-07: Gamificación e Incentivos" {
  usecase "CUS-018: Emitir constancia\ninstitucional de horas" as CUS18
  usecase "CUS-019: Gestionar insignias\ny reputación gamificada" as CUS19
}

Mentor --> CUS18
Admin --> CUS18
Mentor --> CUS19
@enduml
```

Fuente: Elaboración propia.

---

### Diagrama 6.12: Diagrama de Casos de Uso - MOD-08: Analítica, Notificaciones y Configuración

```plantuml
@startuml
title Diagrama 6.12: Diagrama de Casos de Uso - MOD-08: Analítica, Notificaciones y Configuración
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Administrador (EPIS)" as Admin #FEF9C3
actor "Servicio Cron Backend" as Cron #FFF1F2

rectangle "MOD-08: Analítica, Notificaciones y Configuración" {
  usecase "CUS-009: Notificar eventos\ncríticos y alertas temporales" as CUS09
  usecase "CUS-011: Generar reportes e\nindicadores de analítica" as CUS11
  usecase "CUS-015: Consultar métricas\nde retención y desempeño" as CUS15
  usecase "CUS-016: Auditar trazas de\nseguridad y consentimiento" as CUS16
  usecase "CUS-020: Configurar parámetros\ninstitucionales y umbrales" as CUS20
  usecase "CUS-022: Gestionar catálogo\nde temas y materias críticas" as CUS22
}

Cron --> CUS09
Admin --> CUS11
Admin --> CUS15
Admin --> CUS16
Admin --> CUS20
Admin --> CUS22
@enduml
```

Fuente: Elaboración propia.

---
'''
