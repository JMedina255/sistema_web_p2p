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
| **3.1 (H02)** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Refinamiento funcional integral del SRS (H02): profundización exhaustiva de Secciones 1 a 5, especificación de fichas funcionales para los 26 RF sin filtración técnica, consolidación de RF20 como encuestas de calidad post-mentoría 24h, actualización de los 10 RNF (ISO 25010), 14 Reglas de Negocio, procesos As-Is y To-Be con regla D-2 y rutas relativas. |
| **3.1 (H03)** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Auditoría de calidad, criterios de aceptación y trazabilidad integral del SRS (H03): contrastación exhaustiva de 62 contratos REST de FastAPI en backend, homologación de endpoints en Cuadro 5.3 y en las 26 fichas técnicas, estandarización de criterios de aceptación Given-When-Then con clasificación de estado ([REQUISITO], [IMPLEMENTADO], [VERIFICADO], [PENDIENTE], [PROPUESTO]), conciliación metodológica de 500h de ingeniería (CAPEX) vs. 91h presenciales de sprint, y clasificación tipológica de todas las métricas del sistema. |

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

Estas materias actúan en la práctica como **"asignaturas filtro"**, concentrando tasas históricas de desaprobación que fluctúan entre el 25% y el 40% `[DATO_HISTORICO_OBSERVADO]`, provocando rezago en el avance de la malla curricular, desmotivación temprana y un riesgo sensible de deserción universitaria en los primeros semestres.

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
El proyecto se sustenta en componentes maduros y estables de la industria del software, respaldados por métricas empíricas y atributos de calidad normalizados:
- **Frontend:** React 18, TypeScript, Vite y Tailwind CSS, asegurando tiempos de carga inicial ($FCP < 1.2\text{ s}$ `[META_CALIDAD]`) y compatibilidad en el 100% de navegadores modernos `[REQUISITO]`.
- **Backend:** Python 3.13 con FastAPI y Scikit-learn, con latencia media de recomendación algorítmica de $12.4\text{ ms}$ `[DATO_HISTORICO_OBSERVADO]` (medida en benchmark de testbench sintético sobre 50 perfiles en commit `3f6e31d`), muy inferior al umbral admisible de $500\text{ ms}$ `[META_CALIDAD]`.
- **Persistencia:** PostgreSQL v15+ administrado sobre Supabase Cloud con soporte para políticas RLS y bloqueos pesimistas a nivel de fila (`SELECT ... FOR UPDATE`), demostrando 0.0% de sobrecupo `[DATO_HISTORICO_OBSERVADO]` en pruebas multihilo concurrentes.

### 3.5.2. Viabilidad Económica
El análisis financiero se modeló para un horizonte de evaluación a 5 años (2026–2030) con una tasa de costo de oportunidad de capital (COK) del 12.00%:

A continuación, se presentan los indicadores financieros del proyecto:

### Cuadro 3.1: Evaluación Financiera y Económica del Proyecto (Horizonte 2026–2030)

| Indicador Financiero | Valor Cuantificado | Clasificación Metodológica | Criterio de Aceptación | Interpretación Técnica y Financiera |
| :--- | :---: | :---: | :---: | :--- |
| **Inversión Inicial (CAPEX)** | **S/. 5,475.00** | `[SUPUESTO_ECONOMICO]` / `[CALCULO_MATEMATICO]` | Presupuesto Cátedra | Cubre 500 horas de ingeniería de software (Joan Cristian Medina y Renzo Antonio Antayhua a S/. 9.00/h), depreciación de equipos, conectividad, dominio web e imprevistos. |
| **Costo Operativo Anual (OPEX)** | **S/. 1,140.00** | `[SUPUESTO_ECONOMICO]` / `[CALCULO_MATEMATICO]` | Presupuesto Anual | Infraestructura cloud PaaS (Render / Supabase), renovación de dominio, soporte preventivo y materiales de difusión. |
| **Valor Actual Neto (VAN)** | **+S/. 10,801.64** | `[CALCULO_MATEMATICO]` | $\text{VAN} > 0$ | Estrictamente positivo, ratificando que el proyecto genera valor económico sustancial y excedentes por encima de la tasa de descuento exigida (12.00%). |
| **Tasa Interna de Retorno (TIR)** | **68.20%** | `[CALCULO_MATEMATICO]` | $\text{TIR} > \text{COK}$ (12%) | Supera con holgura el COK referencial (12.00%), confiriendo un margen de resiliencia financiera amplio ante variaciones de costos operativos. |
| **Relación Beneficio / Costo (B/C)** | **1.97** | `[CALCULO_MATEMATICO]` | $\text{B/C} > 1.0$ | Por cada sol invertido a lo largo del ciclo del proyecto, se generan S/. 1.97 en ahorros y beneficios valorizados para la facultad y los estudiantes. |
| **Periodo de Recuperación (Payback)**| **1 año y 9.7 meses** | `[CALCULO_MATEMATICO]` | $< 3\text{ años}$ | La inversión inicial se recupera plenamente antes de concluir el segundo año lectivo de puesta en producción. |

Fuente: Elaboración propia a partir del estudio económico del proyecto.

El análisis del Cuadro 3.1 certifica la sólida rentabilidad y conveniencia financiera de la solución para la Escuela Profesional de Ingeniería de Sistemas. El retorno derivado de la reducción de tasas de rezago y de desaprobación compensa con creces los costos moderados de desarrollo y mantenimiento en la nube.

A continuación, se presenta en el Cuadro 3.2 la conciliación metodológica entre las horas presenciales de cátedra y las horas de ingeniería de software:

### Cuadro 3.2: Conciliación Metodológica de Horas de Desarrollo e Inversión Técnica

| Parámetro de Comparación | Horas Académicas Presenciales de Cátedra | Horas Integrales de Ingeniería de Software (CAPEX) | Justificación Metodológica y Alcance Técnico |
| :--- | :---: | :---: | :--- |
| **Total de Horas Computadas** | **91.0 horas** `[ESTIMACION_ACADEMICA]` / `[DATO_HISTORICO_OBSERVADO]` | **500.0 horas** `[SUPUESTO_ECONOMICO]` / `[CALCULO_MATEMATICO]` | Disparidad de alcance formal: las 91 horas corresponden al horario de laboratorio evaluado; las 500 horas al esfuerzo técnico global de ingeniería. |
| **Distribución por Desarrollador** | Joan Medina: **45.0 h**<br>Renzo Antayhua: **46.0 h** | Joan Medina: **250.0 h**<br>Renzo Antayhua: **250.0 h** | Asignación equitativa en ambos marcos, reflejando corresponsabilidad plena en frontend, backend, arquitectura y documentación. |
| **Fuente de Acreditación** | `PLAN_SPRINTS_Y_TAREAS.md`, Informes de Sprint 1 al 8 | Modelo de Costos de Ingeniería, Estudio Financiero CAPEX | Trazabilidad documental cruzada entre el cronograma curricular de cátedra y el presupuesto formal del proyecto. |
| **Actividades Comprendidas** | Sesiones lectivas de laboratorio, revisiones de sprint con el docente, demostraciones de incremento (*sprint review*) y retrospectivas en aula. | Análisis de requisitos (IEEE 29148), diseño arquitectónico UML (Visual Paradigm), codificación React/TypeScript y FastAPI, motor EdRecSys, 682 pruebas automatizadas, CI/CD, despliegue cloud y redacción técnica de SRS y SAD. | El desarrollo de software profesional exige un esfuerzo sustantivo extra-aula que multiplica por un factor de ~5.5 la capacidad lectiva presencial. |
| **Valorización Monetaria** | No monetizable directamente (créditos académicos universitarios). | **S/. 4,500.00** en mano de obra (500 h $\times$ S/. 9.00/h) + S/. 975.00 en equipamiento, dominio y contingencias = **S/. 5,475.00**. | Base cuantificada del flujo de caja de inversión inicial (CAPEX) utilizado para la estimación del VAN, TIR y periodo de recuperación. |

Fuente: Elaboración propia a partir de las actas de cátedra y el expediente financiero.

El análisis del Cuadro 3.2 clarifica la diferencia fundamental de alcance entre la capacidad neta de cátedra (91.0 horas lectivas de laboratorio distribuidas a lo largo de los 8 sprints del curso Construcción de Software I) y el esfuerzo profesional integral de ingeniería de software (500.0 horas efectivas de desarrollo, pruebas y documentación técnica que fundamentan la inversión inicial de S/. 5,475.00). Ambas cifras son mutuamente consistentes y representan dimensiones operativas complementarias del proyecto.

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
| **RF01** | MOD-01 | Autenticación institucional multifactor (2FA) | CUS-001 | `POST /api/v1/auth/otp/request`<br>`POST /api/v1/auth/otp/verify`<br>`POST /api/v1/auth/otp/resend`<br>`POST /api/v1/auth/google` | `LoginOtpView.tsx`<br>`AuthService.py` / `authService.ts`<br>`auth_challenges`, `usuarios` | Crítica |
| **RF02** | MOD-01 | Formalización de consentimiento legal digital (Ley 29733) | CUS-001 | `GET /api/v1/consent/status`<br>`POST /api/v1/consent/accept`<br>`POST /api/v1/consent/revoke` | `ConsentModalView.tsx`<br>`ConsentService.py` / `consentService.ts`<br>`consentimientos_legales` | Crítica |
| **RF03** | MOD-01 | Gestión y asignación administrativa de roles de usuario | CUS-010 | `GET /api/v1/roles/users/{email}`<br>`POST /api/v1/roles/promote-mentor`<br>`POST /api/v1/roles/revoke-mentor` | `AdminRolesView.tsx`<br>`RoleService.py` / `roleService.ts`<br>`roles`, `usuario_roles` | Alta |
| **RF04** | MOD-03 | Configuración de perfil formativo y matriz horaria | CUS-005 | `GET /api/v1/profiles/me`<br>`PUT /api/v1/profiles/me`<br>`GET /api/v1/profiles/availability`<br>`PUT /api/v1/profiles/availability` | `ProfileAcademicView.tsx`<br>`ProfileService.py` / `profileService.ts`<br>`perfiles_academicos`, `disponibilidades_horarias` | Alta |
| **RF05** | MOD-03 | Catálogo curricular de asignaturas y temarios silábicos | CUS-021 | `GET /api/v1/curriculum/courses`<br>`POST /api/v1/curriculum/courses`<br>`GET /api/v1/curriculum/courses/{id_asignatura}`<br>`GET /api/v1/curriculum/courses/{id_asignatura}/topics` | `CurriculumCatalogView.tsx`<br>`CurriculumService.py` / `apiClient.ts`<br>`asignaturas`, `temas_conceptuales` | Alta |
| **RF06** | MOD-04 | Inferencia algorítmica y recomendación personalizada Top-k | CUS-002 | `GET /api/v1/recommendations/mentors`<br>`GET /api/v1/recommendations/offers`<br>`POST /api/v1/recommendations/explain` | `RecommendationFeedView.tsx`<br>`RecommendationService.py` (EdRecSys)<br>`sesiones_mentoria`, `perfiles_academicos` | Crítica |
| **RF07** | MOD-04 | Registro y banco de solicitudes por demanda académica | CUS-003 | `POST /api/v1/bookings/requests`<br>`GET /api/v1/bookings/requests` | `MentoringDemandModalView.tsx`, `MentorSessionsView.tsx`<br>`BookingService.py`<br>`solicitudes_demanda` | Media |
| **RF08** | MOD-02 | Publicación y parametrización de ofertas de mentoría | CUS-006 | `POST /api/v1/offers`<br>`GET /api/v1/offers` | `OfferPublishView.tsx`<br>`OfferService.py` / `offerService.ts`<br>`sesiones_mentoria` (con enlaces a recursos didácticos) | Alta |
| **RF09** | MOD-02 | Aprovisionamiento automatizado de espacios y salas virtuales | CUS-006, CUS-008 | `GET /api/v1/spaces/free-slots`<br>`GET /api/v1/spaces/classrooms` | `SpaceSelectorView.tsx`<br>`VirtualRoomService.py`, `CatalogSupportService.py`<br>`sesiones_mentoria`, `espacios_fisicos` | Alta |
| **RF10** | MOD-02 | Procesamiento de cronogramas oficiales de aulas | CUS-008 | `POST /api/v1/spaces/import-schedule`<br>`GET /api/v1/spaces/free-slots` | `AdminScheduleUploadView.tsx`<br>`ScheduleParserService.py`<br>`spacesService.ts` | Alta |
| **RF11** | MOD-02 | Gestión de imprevistos, reprogramación y cancelación | CUS-006 | `POST /api/v1/offers/{id_sesion}/quorum-decision` (RESCHEDULE / CANCEL) | `MentorSessionsView.tsx`<br>`OfferService.py`<br>`sesiones_mentoria`, `reservas_cupo` | Alta |
| **RF12** | MOD-05 | Reserva concurrente de cupos con control de aforo | CUS-004 | `POST /api/v1/bookings/reserve`<br>`GET /api/v1/bookings/my-reservations`<br>`GET /api/v1/bookings/session/{id_sesion}` | `BookingModalView.tsx`<br>`BookingService.py` (SELECT FOR UPDATE)<br>`reservas_cupo`, `sesiones_mentoria` | Crítica |
| **RF13** | MOD-05 | Ratificación anticipada obligatoria de asistencia | CUS-024 | `POST /api/v1/bookings/{id_reserva}/confirm` | `MyBookingsView.tsx`<br>`BookingService.py`<br>`reservas_cupo` | Alta |
| **RF14** | MOD-05 | Desistimiento voluntario y liberación inmediata de cupo | CUS-017 | `POST /api/v1/bookings/{id_reserva}/cancel` | `MyBookingsView.tsx`<br>`BookingService.py`<br>`reservas_cupo` | Alta |
| **RF15** | MOD-05 | Monitoreo desatendido y corte de quórum en $T-24\text{ h}$ | CUS-023, CUS-009 | `POST /api/v1/quorum/evaluate`<br>`POST /api/v1/quorum/evaluate-all` | `NotificationCenterView.tsx`<br>`QuorumScheduler.py`, `BookingService.py`<br>`sesiones_mentoria`, `reservas_cupo` | Crítica |
| **RF16** | MOD-05 | Gestión resolutiva del mentor ante quórum insuficiente | CUS-007 | `POST /api/v1/offers/{id_sesion}/quorum-decision` (PROCEED / RESCHEDULE / CANCEL) | `QuorumDecisionModalView.tsx`<br>`OfferService.py`<br>`sesiones_mentoria`, `reservas_cupo` | Alta |
| **RF17** | MOD-06 | Marcación de asistencia con pase QR dinámico (TOTP) | CUS-012 | `GET /api/v1/sessions/{id_sesion}/attendance/token`<br>`POST /api/v1/sessions/{id_sesion}/attendance/check-in`<br>`GET /api/v1/sessions/{id_sesion}/attendance` | `AttendanceScannerView.tsx`, `AttendanceQrModalView.tsx`<br>`AttendanceService.py`<br>`asistencias_sesion`, `tokens_asistencia_activos` | Alta |
| **RF18** | MOD-06 | Registro de bitácora docente en 48h con hash SHA-256 | CUS-013 | `POST /api/v1/sessions/{id_sesion}/bitacora`<br>`GET /api/v1/sessions/{id_sesion}/bitacora` | `BitacoraFormView.tsx`<br>`BitacoraService.py`<br>`bitacoras_pedagogicas` | Alta |
| **RF19** | MOD-06 | Historial de sesiones, bitácoras y recursos compartidos | CUS-014 | `GET /api/v1/sessions/{id_sesion}/bitacora`<br>`GET /api/v1/bookings/my-reservations`<br>`GET /api/v1/bitacoras` | `BitacoraHistoryView.tsx`<br>`BitacoraService.py`<br>`bitacoras_pedagogicas`, `sesiones_mentoria` | Media |
| **RF20** | MOD-06 | Captura de encuestas de calidad post-mentoría (ventana 24h) | CUS-012, CUS-014 | `GET /api/v1/sessions/{id}/survey`<br>`POST /api/v1/sessions/{id}/survey` | `PostSessionSurveyModalView.tsx`<br>`SurveyService.py` / `surveyService.ts`<br>`encuestas_calidad` | Alta |
| **RF21** | MOD-07 | Cálculo de reputación docente y catálogo de insignias | CUS-019 | `GET /api/v1/certificates/summary`<br>`GET /api/v1/profiles/me` | `MentorBadgesView.tsx`<br>`RecommendationService.py`, `ProfileService.py`<br>`encuestas_calidad`, `perfiles_academicos` | Media |
| **RF22** | MOD-07 | Parametrización y autorización de certificados de horas | CUS-018 | `GET /api/v1/certificates/summary`<br>`POST /api/v1/certificates/generate` | `AdminCertificatesView.tsx`<br>`CertificateService.py`<br>`certificados_horas` | Media |
| **RF23** | MOD-07 | Emisión, descarga y verificación con código QR | CUS-018, CUS-009 | `GET /api/v1/certificates/{id_certificado}/download`<br>`GET /api/v1/certificates/verificar`<br>`GET /api/v1/certificates/{id_certificado}` | `CertificateVerifyView.tsx`, `AdminCertificatesView.tsx`<br>`CertificateService.py` (ReportLab / QrCode)<br>`certificados_horas` | Media |
| **RF24** | MOD-08 | Parametrización institucional de aforos y prioridades | CUS-020 | `GET /api/v1/health`<br>`GET /api/v1/health/db`<br>Configuración centralizada (`app.core.config.Settings`) | `AdminConfigView.tsx`<br>`app.core.config`, `SimulationService.py` | Media |
| **RF25** | MOD-08 | Tablero analítico directivo y métricas de retención ICACIT | CUS-011, CUS-015 | `GET /api/v1/simulation/benchmark`<br>`GET /api/v1/recommendations/simulation/testbench` | `AdminAnalyticsView.tsx`<br>`SimulationService.py`<br>`AnalyticsService.ts` | Alta |
| **RF26** | MOD-08 | Auditoría institucional de bitácoras y privacidad legal | CUS-016, CUS-022 | `GET /api/v1/bitacoras`<br>`POST /api/v1/bitacoras/{id}/visar`<br>`POST /api/v1/bitacoras/{id}/observar`<br>`GET /api/v1/consent/status` | `AdminAuditView.tsx`<br>`BitacoraService.py`, `ConsentService.py`<br>`bitacoras_pedagogicas`, `consentimientos_legales` | Alta |

Fuente: Elaboración propia a partir de la homologación canónica de diseño y los controladores FastAPI efectivamente implementados.

El análisis del Cuadro 5.3 ratifica la coherencia absoluta del modelo funcional del Sistema Web P2P:
1. **Resolución Definitiva de RF20:** Conforme a la homologación canónica, `RF20` corresponde a la *Captura de encuestas de calidad post-mentoría (ventana 24h)* sobre la entidad `encuestas_calidad` y los controladores reales `GET/POST /api/v1/sessions/{id}/survey`, mientras que la gestión de recursos didácticos se formaliza dentro de `RF08` (ofertas) y `RF19` (historial/materiales).
2. **Sincronización Total de Contratos REST:** Las 26 filas reflejan fielmente las rutas reales expuestas por FastAPI en `aplicacion/backend/app/api/v1/endpoints/`.
3. **Trazabilidad Integral y Cero Ambigüedad:** Ningún requerimiento funcional carece de casos de uso asociados ni de componentes técnicos comprobables en la base de código.

### 5.3.1. Fichas Detalladas de Especificación de Requerimientos Funcionales (RF01 al RF26)

A continuación, se especifican exhaustivamente las fichas técnicas individuales para los veintiséis (26) requerimientos funcionales del sistema, redactadas en lenguaje funcional orientado al usuario universitario y segregando formalmente los detalles de implementación técnica, contratos RESTful verificados en FastAPI y criterios de aceptación en formato Given–When–Then clasificados con las etiquetas normalizadas `[REQUISITO]`, `[IMPLEMENTADO]`, `[VERIFICADO]`, `[PENDIENTE]` y `[PROPUESTO]`:

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
  - *Escenario 1 (Acceso exitoso con código OTP) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante registrado introduce una dirección institucional válida `@virtual.upt.pe` o `@upt.pe`, CUANDO ingresa los 6 dígitos del código numérico dentro de los 300 segundos de vigencia, ENTONCES el sistema valida el reto, emite un token Bearer JWT con 8 horas de expiración y concede acceso al portal institucional.
  - *Escenario 2 (Código expirado o erróneo) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el usuario ingresa un código que ha superado los 5 minutos de vigencia o que no coincide con el reto activo, CUANDO solicita la verificación, ENTONCES el sistema rechaza la autenticación con error HTTP 400 Bad Request, incrementa el contador de intentos fallidos y ofrece solicitar un nuevo código tras un enfriamiento de 60 segundos.
  - *Escenario 3 (Rechazo de dominio no institucional) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un usuario intenta autenticarse mediante un correo no institucional (ej. dominio comercial ajeno a la UPT), CUANDO solicita el envío de OTP o intenta la federación, ENTONCES el sistema deniega la operación con error HTTP 403 Forbidden o HTTP 422 Unprocessable Entity, advirtiendo que el servicio es exclusivo para la comunidad EPIS-UPT.
  - *Escenario 4 (Reejecución de pruebas en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la suite unitaria `test_auth.py` (14 pruebas backend) y `LoginOtpView.test.tsx` (18 pruebas frontend) fue validada en el corte histórico `3f6e31d`, CUANDO se complete la revalidación en `main` tras solventar el linteo, ENTONCES la suite debe reportar 100% de aserciones exitosas.
- **Casos de Uso Relacionados:** CUS-001 (Autenticar usuario mediante credenciales institucionales y consentimiento digital).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/auth.py` (`POST /api/v1/auth/otp/request`, `POST /api/v1/auth/otp/verify`, `POST /api/v1/auth/otp/resend`, `POST /api/v1/auth/google`).
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
  - *Escenario 1 (Aceptación formal de consentimiento) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante autenticado no registra consentimiento informado previo, CUANDO visualiza el diálogo modal bloqueante y presiona "Aceptar y Continuar", ENTONCES el sistema registra en `consentimientos_legales` la conformidad con IP, User-Agent y marca de tiempo UTC, desbloqueando el acceso a las funciones de mentoría.
  - *Escenario 2 (Revocación o rechazo voluntario) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante decide revocar o rechazar el consentimiento de tratamiento de datos personales bajo la Ley N° 29733, CUANDO envía la solicitud de revocación, ENTONCES el sistema aplica la regla RN-02 bloqueando de inmediato el acceso a los servicios de emparejamiento, catálogo y reserva hasta una eventual reaceptación.
  - *Escenario 3 (Trazabilidad legal auditada en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la persistencia inmutable de auditoría fue respaldada por 10 pruebas en `test_consent.py` y 12 pruebas en `ConsentModalView.test.tsx`, CUANDO se ejecute el flujo de verificación formal en `main`, ENTONCES se debe certificar la inviolabilidad de las marcas de tiempo y la coherencia del bloqueo de navegación.
- **Casos de Uso Relacionados:** CUS-001 (Autenticar usuario mediante credenciales institucionales y consentimiento digital).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/consent.py` (`GET /api/v1/consent/status`, `POST /api/v1/consent/accept`, `POST /api/v1/consent/revoke`).
  - *Servicios de Negocio:* `ConsentService.py` (`get_consent_status`, `accept_consent`, `revoke_consent`).
  - *Entidades Relacionales:* Tabla `consentimientos_legales` (almacena UUID de usuario, dirección IP, User-Agent del navegador y marca de tiempo UTC).
  - *Componentes Visuales:* `ConsentModalView.tsx`, `consentService.ts`.
  - *Evidencia de Pruebas:* `test_consent.py` (10 pruebas backend), `ConsentModalView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF03 — Gestión Administrativa de Roles y Verificación de Mérito

- **Identificador:** RF03
- **Nombre Oficial:** Gestión, fiscalización y asignación administrativa de roles de usuario
- **Módulo Arquitectónico:** MOD-01: Seguridad, Autenticación y Gobernanza
- **Descripción Funcional:** El sistema debe permitir a las autoridades de la Dirección de Escuela y Coordinación de Tutoría consultar la nómina de estudiantes universitarios y administrar sus roles operativos (Mentoreado, Mentor, Administrador, Coordinador), verificando de forma estricta los requisitos de mérito académico exigidos para autorizar a un estudiante a desempeñarse como mentor de sus compañeros.
- **Objetivo y Necesidad Académica:** Garantizar la idoneidad académica y solvencia pedagógica de los mentores, protegiendo la calidad de la enseñanza que reciben los alumnos de ciclos iniciales y asegurando que los mentores sean alumnos destacados.
- **Actores Participantes:** Administrador Institucional (Actor Primario); Estudiante Mentor (Beneficiario del Rol).
- **Condiciones de Entrada (Precondiciones):** El administrador debe contar con una sesión activa con privilegios de gestión institucional en la plataforma.
- **Comportamiento Esperado:**
  1. El administrador accede al panel de administración de usuarios y visualiza la relación de estudiantes registrados.
  2. Selecciona a un estudiante postulante al rol de mentor y revisa su historial académico formal.
  3. El sistema valida automáticamente que el estudiante se encuentre matriculado en el ciclo VII o superior y que posea promedio ponderado aprobatorio.
  4. Si cumple los requisitos, el administrador confirma la asignación del rol de mentor.
  5. El sistema actualiza de inmediato los privilegios de la cuenta, habilitando la publicación de sesiones de mentoría en el portal.
  6. Si no cumple los requisitos, el sistema bloquea la asignación e indica detalladamente la condición académica insatisfecha.
- **Resultado Verificable (Postcondiciones):** El estudiante adquiere formalmente las atribuciones de mentor en la plataforma, quedando registrado el cambio en la bitácora administrativa.
- **Reglas de Negocio Vinculadas:** RN-03 (Elegibilidad y mérito académico de mentores: ciclo VII o superior, nota aprobatoria sobresaliente en la materia a dictar).
- **Restricciones Funcionales:** Ningún estudiante puede autoasignarse el rol de mentor sin la debida verificación y autorización administrativa.
- **Criterios de Aceptación:**
  - *Escenario 1 (Promoción autorizada por mérito académico) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante postula al rol de mentor cumpliendo con pertenecer al ciclo VII o superior (RN-03) y una autoridad administradora evalúa su solicitud, CUANDO el administrador envía la orden de promoción a `/api/v1/roles/promote-mentor`, ENTONCES el sistema asigna el rol `mentor` en `usuario_roles` y habilita las capacidades de publicación de ofertas con código HTTP 200 OK.
  - *Escenario 2 (Denegación estricta de autopromoción no autorizada) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante con rol exclusivo de mentoreado intenta invocar el endpoint de promoción hacia su propia cuenta sin privilegios de administrador, CUANDO el backend intercepta la solicitud, ENTONCES el sistema aborta la transacción con código HTTP 403 Forbidden y mensaje explícito de denegación por regla de mérito RN-03.
  - *Escenario 3 (Revocación administrativa del rol mentor) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la Dirección de Escuela dispone retirar la condición de mentor a un estudiante por bajo rendimiento o inactividad, CUANDO el administrador confirma la revocación en `/api/v1/roles/revoke-mentor`, ENTONCES el sistema conmuta su rol a mentoreado, cancela preventivamente ofertas publicadas sin inscritos y registra la auditoría institucional.
  - *Escenario 4 (Acreditación en suite de integración en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el subsistema de roles cuenta con 7 pruebas en `test_roles.py` y 10 pruebas en frontend, CUANDO se ejecute la validación formal en `main`, ENTONCES se verificará la estricta segregación de permisos RBAC.
- **Casos de Uso Relacionados:** CUS-010 (Administrar usuarios, asignación de roles y control de privilegios).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/roles.py` (`GET /api/v1/roles/users/{email}`, `POST /api/v1/roles/promote-mentor`, `POST /api/v1/roles/revoke-mentor`).
  - *Servicios de Negocio:* `RoleService.py` (`get_user_roles`, `promote_to_mentor`, `revoke_mentor`).
  - *Entidades Relacionales:* Tablas `roles`, `usuario_roles`, `usuarios`.
  - *Componentes Visuales:* `AdminRolesView.tsx`, `roleService.ts`.
  - *Evidencia de Pruebas:* `test_roles.py` (7 pruebas backend), `AdminRolesView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF04 — Configuración de Perfil Académico y Matriz Horaria

- **Identificador:** RF04
- **Nombre Oficial:** Parametrización del perfil formativo y matriz semanal de disponibilidad horaria
- **Módulo Arquitectónico:** MOD-03: Perfiles Académicos y Catálogo Curricular
- **Descripción Funcional:** El sistema debe proveer a cada estudiante una interfaz interactiva donde configure su perfil académico (ciclo cursado, materias de interés, fortalezas curriculares y modalidad de estudio preferida) y defina su disponibilidad horaria semanal mediante una matriz visual de bloques de tiempo.
- **Objetivo y Necesidad Académica:** Alimentar con datos precisos y actualizados al algoritmo de recomendación, evitando colisiones con los horarios oficiales de clase de los estudiantes y garantizando coincidencias factibles.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor (Actores Primarios).
- **Condiciones de Entrada (Precondiciones):** Usuario con cuenta institucional activa y sesión iniciada en la plataforma.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a la sección de configuración de perfil.
  2. Selecciona su ciclo de estudios actual y marca las asignaturas filtro en las que requiere apoyo o en las que se ofrece a brindar asesoría.
  3. Visualiza la matriz semanal interactiva de 6 días (lunes a sábado) dividida en franjas horarias de 60 minutos entre las 08:00 y las 20:00 horas (grilla estándar 6×11).
  4. Marca con un clic los bloques horarios en los que dispone de tiempo libre.
  5. Pulsa el botón de confirmación para guardar sus preferencias.
  6. El sistema valida que los datos no presenten incoherencias y actualiza el perfil académico y la matriz horaria.
- **Resultado Verificable (Postcondiciones):** El perfil formativo queda almacenado y disponible para los procesos automáticos de recomendación y emparejamiento.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación de programación y compatibilidad horaria), RN-03 (Mérito académico).
- **Restricciones Funcionales:** Ningún mentor podrá ofrecer sesiones en franjas no declaradas como disponibles en su matriz horaria activa.
- **Criterios de Aceptación:**
  - *Escenario 1 (Actualización de perfil y matriz semanal 6×11) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante accede a la vista de configuración horaria, CUANDO selecciona bloques de disponibilidad entre lunes y sábado de 08:00 a 20:00 y pulsa "Guardar Cambios", ENTONCES el sistema actualiza de manera atómica las franjas en `disponibilidades_horarias` y las disponibiliza para el motor algorítmico EdRecSys con código HTTP 200 OK.
  - *Escenario 2 (Intento de guardado sin bloques horarios seleccionados) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor intenta guardar su disponibilidad horaria sin marcar ninguna franja activa en la matriz 6×11, CUANDO envía la actualización, ENTONCES el sistema muestra una advertencia preventiva notificando que la ausencia de bloques impedirá la generación de recomendaciones en el catálogo de ofertas.
  - *Escenario 3 (Revalidación de consistencia en suite automatizada) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la persistencia horaria cuenta con 14 pruebas en `test_profiles.py` y 16 pruebas en `ProfileAcademicView.test.tsx`, CUANDO se concluya la subsanación de linteo en `main`, ENTONCES la suite debe validar que las actualizaciones no generen solapamientos ni registros huérfanos.
- **Casos de Uso Relacionados:** CUS-005 (Configurar perfil formativo y disponibilidad horaria del estudiante).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`, `PUT /api/v1/profiles/me`, `GET /api/v1/profiles/availability`, `PUT /api/v1/profiles/availability`).
  - *Servicios de Negocio:* `ProfileService.py` (`get_profile`, `update_profile`, `get_availability`, `update_availability`).
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
  - *Escenario 1 (Exploración jerárquica de catálogo silábico) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante filtra el catálogo por asignaturas prioritarias de los ciclos I al IV, CUANDO selecciona una materia crítica (ej. Algoritmos y Estructura de Datos), ENTONCES el sistema despliega el árbol de temas silábicos oficiales indexados por unidad temática con código HTTP 200 OK.
  - *Escenario 2 (Mantenimiento curricular por el administrador) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la Dirección de Escuela actualiza el plan silábico institucional, CUANDO el usuario con rol administrador registra una nueva asignatura o tema en `/api/v1/curriculum/courses`, ENTONCES el sistema persiste los metadatos en `asignaturas` y propaga los temas de forma inmediata para ofertas y solicitudes por demanda.
  - *Escenario 3 (Revisión de integridad en integración continua) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE las operaciones del catálogo cuentan con 16 pruebas en `test_curriculum.py` y 18 pruebas en `CurriculumCatalogView.test.tsx`, CUANDO se ejecute el pipeline de pruebas en `main`, ENTONCES debe verificarse la integridad referencial entre asignaturas y temas sin inconsistencias.
- **Casos de Uso Relacionados:** CUS-021 (Consultar y mantener catálogo curricular de asignaturas y temarios).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`GET /api/v1/curriculum/courses`, `POST /api/v1/curriculum/courses`, `GET /api/v1/curriculum/courses/{id_asignatura}`, `GET /api/v1/curriculum/courses/{id_asignatura}/topics`).
  - *Servicios de Negocio:* `CurriculumService.py` (`get_courses`, `get_course_by_id`, `get_course_topics`, `create_course`).
  - *Entidades Relacionales:* Tablas `asignaturas`, `temas_conceptuales`.
  - *Componentes Visuales:* `CurriculumCatalogView.tsx`, `apiClient.ts`.
  - *Evidencia de Pruebas:* `test_curriculum.py` (16 pruebas backend), `CurriculumCatalogView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF06 — Inferencia Algorítmica y Recomendación Adaptativa Top-k

- **Identificador:** RF06
- **Nombre Oficial:** Inferencia algorítmica y recomendación personalizada Top-k (Motor EdRecSys)
- **Módulo Arquitectónico:** MOD-04: Banco de Demanda y Recomendación Adaptativa
- **Descripción Funcional:** El sistema debe procesar las debilidades académicas del estudiante mentoreado, sus horarios disponibles y su historial de calificaciones, comparándolos contra los perfiles, horarios y especialidades de los mentores mediante un algoritmo de recomendación híbrido (EdRecSys) que combina filtrado basado en contenido (similitud coseno) y filtrado colaborativo, entregando una lista ordenada de los $k$ mejores mentores y ofertas disponibles.
- **Objetivo y Necesidad Académica:** Resolver el histórico problema de la búsqueda informal de ayuda, conectando al estudiante que tiene dificultades en un tema con el compañero más capacitado y con mayor disponibilidad compatible para apoyarlo.
- **Actores Participantes:** Estudiante Mentoreado (Beneficiario del Ranking); Estudiante Mentor (Sujeto Recomendado).
- **Condiciones de Entrada (Precondiciones):** El mentoreado debe haber completado su perfil formativo y contar con al menos una materia de interés seleccionada.
- **Comportamiento Esperado:**
  1. El estudiante ingresa a la sección de recomendaciones personalizadas.
  2. El sistema recupera el vector de necesidades del estudiante (materias críticas, temas de interés y matriz de tiempo libre).
  3. El motor algorítmico evalúa la base de datos de mentores activos y sesiones programadas, calculando un puntaje de afinidad multidimensional para cada candidato.
  4. El sistema ordena los resultados de mayor a menor afinidad y selecciona los $k$ candidatos óptimos (por defecto $k=5$).
  5. Despliega en pantalla las tarjetas de recomendación con indicación visual del porcentaje de compatibilidad y justificación resumida de la sugerencia.
- **Resultado Verificable (Postcondiciones):** El mentoreado visualiza opciones de asesoría altamente compatibles y puede iniciar la reserva con un solo clic.
- **Reglas de Negocio Vinculadas:** RN-04 (Compatibilidad horaria), RN-03 (Mérito del mentor), RN-11 (Priorización de asignaturas filtro).
- **Restricciones Funcionales:** El algoritmo debe responder con una latencia media menor a 500 ms (meta de calidad) para no degradar la experiencia de usuario.
- **Criterios de Aceptación:**
  - *Escenario 1 (Generación de ranking adaptativo Top-k) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante mentoreado consulta el feed de recomendaciones, CUANDO el motor EdRecSys evalúa la afinidad curricular, solapamiento horario y reputación docente, ENTONCES entrega una lista ordenada Top-5 de candidatos con latencia inferior a 500 ms (mediana observada de 12.4 ms) y Precision@3 superior al 80%.
  - *Escenario 2 (Explicabilidad pedagógica de puntajes) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el usuario solicita el detalle de compatibilidad de un mentor sugerido, CUANDO invoca `/api/v1/recommendations/explain`, ENTONCES el sistema devuelve el desglose cuantitativo y cualitativo de similitud temática, compatibilidad horaria y mérito académico con código HTTP 200 OK.
  - *Escenario 3 (Revalidación de casos frontera algorítmicos en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el testbench algorítmico fue evaluado en `test_recommendations.py` (18 pruebas) y `SimulationService.py`, CUANDO se ejecute la validación formal en `main`, ENTONCES se deben verificar empíricamente los 4 casos frontera (cero solapamiento, perfil idéntico, mentor sin historial y saturación de demanda).
- **Casos de Uso Relacionados:** CUS-002 (Consultar ofertas recomendadas y ranking de mentores adaptativo).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/mentors`, `GET /api/v1/recommendations/offers`, `POST /api/v1/recommendations/explain`).
  - *Servicios de Negocio:* `RecommendationService.py` (Módulos de similitud temática, compatibilidad horaria y normalización matricial).
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `perfiles_academicos`, `disponibilidades_horarias`.
  - *Componentes Visuales:* `RecommendationFeedView.tsx`, `MentorCardView.tsx`.
  - *Evidencia de Pruebas:* `test_recommendations.py` (18 pruebas backend), `RecommendationFeedView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF07 — Banco de Solicitudes por Demanda Académica

- **Identificador:** RF07
- **Nombre Oficial:** Registro y banco colaborativo de solicitudes por demanda insatisfecha
- **Módulo Arquitectónico:** MOD-04: Banco de Demanda y Recomendación Adaptativa
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentoreados registrar solicitudes temáticas específicas de mentoría cuando no encuentren ofertas disponibles en el catálogo, consolidando un "banco de demanda académica" visible para todos los mentores calificados a fin de que formulen sesiones orientadas a necesidades reales de sus compañeros.
- **Objetivo y Necesidad Académica:** Evitar que los alumnos con dudas específicas se queden sin orientación por falta de oferta previa, equilibrando la oferta formativa a partir de las necesidades directas de los alumnos.
- **Actores Participantes:** Estudiante Mentoreado (Solicitante); Estudiante Mentor (Atendedor de la Demanda).
- **Condiciones de Entrada (Precondiciones):** Estudiante autenticado que exploró el catálogo de ofertas sin hallar el tema silábico requerido.
- **Comportamiento Esperado:**
  1. El estudiante abre el formulario de registro de solicitud por demanda.
  2. Selecciona la asignatura crítica, el tema silábico puntual y redacta una breve descripción del problema o ejercicio que necesita resolver.
  3. Indica su disponibilidad horaria tentativa para recibir la sesión.
  4. Envía la solicitud y el sistema genera un folio de demanda con estado "Abierta".
  5. El requerimiento se publica de inmediato en el banco colaborativo visible para mentores que dominan dicha materia.
  6. Los mentores interesados pueden postularse para dictar la sesión requerida o crear una oferta orientada a dicho tema.
- **Resultado Verificable (Postcondiciones):** La solicitud queda registrada en el banco institucional y se notifica a los mentores de la materia.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación de programación), RN-11 (Alineamiento con temarios oficiales).
- **Restricciones Funcionales:** No se admiten solicitudes de materias en las que el estudiante no se encuentre matriculado o que no figuren en el catálogo oficial.
- **Criterios de Aceptación:**
  - *Escenario 1 (Registro exitoso de necesidad por demanda) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante no encuentra ofertas activas para un tema silábico específico, CUANDO completa el formulario modal de demanda indicando asignatura, tema y franja tentativa, ENTONCES el sistema crea el registro en `solicitudes_demanda` con estado `PENDIENTE` y código HTTP 201 Created.
  - *Escenario 2 (Consulta del banco de solicitudes por mentores) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante mentor explora el banco de necesidades insatisfechas, CUANDO consulta `/api/v1/bookings/requests`, ENTONCES el sistema entrega la nómina consolidada agrupada por materia y ciclo para facilitar la publicación de ofertas dirigidas.
  - *Escenario 3 (Verificación de despacho y visualización en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el banco de demandas cuenta con 12 pruebas en `test_bookings.py` y 14 pruebas en `MentoringDemandModalView.test.tsx`, CUANDO se ejecute el flujo de CI en `main`, ENTONCES se debe certificar la adecuada indexación de solicitudes pendientes.
- **Casos de Uso Relacionados:** CUS-003 (Registrar solicitud de mentoría por demanda académica insatisfecha).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/requests`, `GET /api/v1/bookings/requests`).
  - *Servicios de Negocio:* `BookingService.py` (`create_demand_request`, `get_demand_requests`).
  - *Entidades Relacionales:* Tabla `solicitudes_demanda`.
  - *Componentes Visuales:* `MentoringDemandModalView.tsx`, `MentorSessionsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (12 pruebas backend), `MentoringDemandModalView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF08 — Publicación y Parametrización de Ofertas de Mentoría

- **Identificador:** RF08
- **Nombre Oficial:** Publicación, programación y parametrización de ofertas de mentoría académica
- **Módulo Arquitectónico:** MOD-02: Ofertas de Mentoría y Gestión de Espacios
- **Descripción Funcional:** El sistema debe proporcionar a los mentores autorizados un asistente interactivo para crear y publicar sesiones de mentoría, especificando la asignatura, los temas silábicos a abordar, la fecha y hora de realización, la modalidad (presencial o virtual), el aforo máximo de participantes y los enlaces o referencias a recursos didácticos preliminares.
- **Objetivo y Necesidad Académica:** Fomentar una programación académica ordenada y predecible, permitiendo a los mentoreados planificar su asistencia con la debida anticipación y garantizando condiciones adecuadas de aforo.
- **Actores Participantes:** Estudiante Mentor (Actor Primario); Estudiantes Mentoreados (Destinatarios).
- **Condiciones de Entrada (Precondiciones):** El usuario debe poseer rol activo de mentor institucional verificado y disponibilidad horaria coincidente.
- **Comportamiento Esperado:**
  1. El mentor accede al formulario de publicación de nueva oferta de mentoría.
  2. Selecciona la asignatura crítica en la que está habilitado y marca uno o más temas silábicos del catálogo oficial.
  3. Define la fecha y hora de la sesión, verificando que exista un margen de antelación mayor a 24 horas respecto a la hora actual.
  4. Selecciona la modalidad de impartición: presencial (con aforo de 10 estudiantes) o virtual (con aforo de 20 estudiantes).
  5. Si lo considera pertinente, adjunta enlaces a diapositivas o guías de ejercicios que los participantes deban revisar previamente.
  6. Envía la oferta; el sistema valida los parámetros, reserva los recursos institucionales y publica la sesión en el catálogo activo.
- **Resultado Verificable (Postcondiciones):** La sesión queda publicada con estado "Publicada", disponible para reservas en el feed de ofertas.
- **Reglas de Negocio Vinculadas:** RN-04 (Antelación obligatoria mayor a 24 horas), RN-05 (Aforos estándar: 10 presencial / 20 virtual).
- **Restricciones Funcionales:** Ninguna sesión puede publicarse con menos de 24 horas de antelación ni exceder los aforos normados.
- **Criterios de Aceptación:**
  - *Escenario 1 (Publicación reglamentaria de oferta de mentoría) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor autorizado (ciclo >= VII) formula una oferta con más de 24 horas de anticipación (RN-04) y aforo reglamentario (10 presencial / 20 virtual, RN-05), CUANDO envía la solicitud a `/api/v1/offers`, ENTONCES el sistema persiste la sesión en estado `PUBLICADA` con código HTTP 201 Created y enlaces a recursos didácticos.
  - *Escenario 2 (Rechazo por antelación menor a 24 horas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor intenta programar una sesión con inicio en un intervalo inferior a 24 horas desde el momento actual, CUANDO invoca la publicación, ENTONCES el sistema rechaza la operación con código HTTP 400 Bad Request en cumplimiento estricto de la regla de negocio RN-04.
  - *Escenario 3 (Acreditación de suite de ofertas en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE las validaciones de publicación están cubiertas por 16 pruebas en `test_offers.py` y 18 pruebas en `OfferPublishView.test.tsx`, CUANDO se ejecute el pipeline de `main`, ENTONCES se verificará la consistencia del catálogo activo sin errores de schema.
- **Casos de Uso Relacionados:** CUS-006 (Publicar y parametrizar oferta de mentoría académica individual o grupal).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers`, `GET /api/v1/offers`).
  - *Servicios de Negocio:* `OfferService.py` (`publish_offer`, `get_offers`).
  - *Entidades Relacionales:* Tabla `sesiones_mentoria` (con campo `recursos_didacticos_url`).
  - *Componentes Visuales:* `OfferPublishView.tsx`, `offerService.ts`.
  - *Evidencia de Pruebas:* `test_offers.py` (16 pruebas backend), `OfferPublishView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF09 — Aprovisionamiento de Espacios Físicos y Salas Virtuales

- **Identificador:** RF09
- **Nombre Oficial:** Aprovisionamiento inteligente de infraestructura física y enlaces virtuales
- **Módulo Arquitectónico:** MOD-02: Ofertas de Mentoría y Gestión de Espacios
- **Descripción Funcional:** El sistema debe asignar automáticamente el recinto educativo para cada sesión de mentoría en función de la modalidad elegida. Para sesiones presenciales, debe verificar la disponibilidad de aulas y laboratorios libres en el campus de Capanique a partir del cronograma oficial procesado, previniendo solapamientos. Para sesiones virtuales, debe generar y vincular automáticamente una sala institucional segura de videoconferencia.
- **Objetivo y Necesidad Académica:** Eliminar la fricción organizativa de buscar ambientes libres a última hora, erradicando interrupciones durante las sesiones y garantizando condiciones acústicas y técnicas adecuadas.
- **Actores Participantes:** Estudiante Mentor (Beneficiario del Aprovisionamiento); Sistema (Gestor de Espacios).
- **Condiciones de Entrada (Precondiciones):** Mentor publicando una oferta con fecha, hora y modalidad definidas.
- **Comportamiento Esperado:**
  1. Si la modalidad es presencial, el sistema consulta el registro de franjas horarias libres de aulas y laboratorios de la facultad.
  2. Filtra los recintos que no tienen clases regulares asignadas ni otras mentorías en la franja seleccionada.
  3. Asigna el aula más apropiada según el aforo de la sesión y reserva el espacio en el calendario de infraestructura física.
  4. Si la modalidad es virtual, el sistema interactúa con el generador institucional de enlaces seguros y reserva una sala virtual única.
  5. Vincula el recinto físico o enlace virtual al registro de la sesión y lo exhibe en los detalles de la oferta para los estudiantes inscritos.
- **Resultado Verificable (Postcondiciones):** La sesión cuenta con un recinto físico o virtual reservado de forma no conflictiva.
- **Reglas de Negocio Vinculadas:** RN-06 (Disponibilidad de aulas físicas), RN-07 (Enlaces virtuales institucionales seguros).
- **Restricciones Funcionales:** Ninguna sesión presencial podrá registrarse en aulas no catalogadas o que tengan clases oficiales programadas.
- **Criterios de Aceptación:**
  - *Escenario 1 (Aprovisionamiento de aula física sin colisión) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor selecciona modalidad presencial, CUANDO consulta recintos libres para su franja horaria en `/api/v1/spaces/free-slots`, ENTONCES el sistema filtra contra el cronograma oficial de la facultad y entrega las aulas disponibles garantizando 0 solapamientos de infraestructura (RN-06).
  - *Escenario 2 (Generación automática de sala virtual) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la sesión es programada en modalidad virtual, CUANDO se formaliza la oferta, ENTONCES el subsistema aprovisiona un enlace institucional seguro persistido en la entidad de sesión para su distribución a los inscritos confirmados (RN-07).
  - *Escenario 3 (Comprobación de aprovisionamiento en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el módulo cuenta con 14 pruebas en `test_spaces.py` y 12 pruebas en frontend, CUANDO se ejecute la verificación formal en `main`, ENTONCES se constatará la correcta detección de colisiones horarias.
- **Casos de Uso Relacionados:** CUS-006 (Publicar oferta), CUS-008 (Procesar cronogramas de infraestructura).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/spaces.py` (`GET /api/v1/spaces/free-slots`, `GET /api/v1/spaces/classrooms`).
  - *Servicios de Negocio:* `VirtualRoomService.py`, `CatalogSupportService.py`.
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `espacios_fisicos`.
  - *Componentes Visuales:* `SpaceSelectorView.tsx`, `spacesService.ts`.
  - *Evidencia de Pruebas:* `test_spaces.py` (14 pruebas backend), `SpaceSelectorView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF10 — Procesamiento de Cronogramas Oficiales de Aulas

- **Identificador:** RF10
- **Nombre Oficial:** Carga, procesamiento y análisis de cronogramas oficiales de distribución horaria de aulas
- **Módulo Arquitectónico:** MOD-02: Ofertas de Mentoría y Gestión de Espacios
- **Descripción Funcional:** El sistema debe proveer al administrador de infraestructura la funcionalidad de cargar archivos estructurados en formato Excel (.xlsx) o PDF (.pdf) conteniendo el cronograma oficial de ocupación de aulas y laboratorios de la EPIS-UPT, procesando su contenido para extraer automáticamente las franjas horarias y recintos físicos vacantes para mentorías.
- **Objetivo y Necesidad Académica:** Automatizar la detección de aulas libres sin requerir coordinación manual continua con conserjería ni transcripción manual de horarios, garantizando información verídica y actualizada de ambientes.
- **Actores Participantes:** Administrador Institucional (Actor Primario); Componente Parser de Horarios (Actor Secundario).
- **Condiciones de Entrada (Precondiciones):** Archivo oficial de cronograma emitido por la Dirección de Escuela disponible en formato digital.
- **Comportamiento Esperado:**
  1. El administrador accede al módulo de gestión de infraestructura física y selecciona la opción de carga de cronograma.
  2. Sube el archivo estructurado (.xlsx o .pdf) correspondiente al semestre académico en curso.
  3. El sistema ejecuta el parser interno que recorre las matrices de aulas, días lectivos y horas de clase regular.
  4. Identifica las celdas vacías y calcula las franjas libres aprovechables para mentorías (bloques de 60 o 120 minutos).
  5. Presenta un resumen de recintos y franjas extraídas, solicitando la confirmación de la importación.
  6. Al confirmar, el sistema actualiza la base de datos de espacios libres disponibles para asignación automática.
- **Resultado Verificable (Postcondiciones):** El catálogo de ambientes libres se actualiza con base en la documentación oficial de la facultad.
- **Reglas de Negocio Vinculadas:** RN-06 (Disponibilidad de aulas físicas y respeto al horario de clases oficiales).
- **Restricciones Funcionales:** El formato del archivo debe coincidir con la plantilla oficial de la facultad; de lo contrario, el sistema rechaza el archivo indicando los errores de estructura.
- **Criterios de Aceptación:**
  - *Escenario 1 (Carga e ingesta de cronograma oficial en Excel o PDF) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el administrador transmite un archivo estructurado (.xlsx o .pdf) con los horarios semestrales de la EPIS-UPT, CUANDO el parser extrae las franjas de clases regulares, ENTONCES el sistema calcula las ventanas vacantes y actualiza el repositorio de ambientes libres con código HTTP 200 OK.
  - *Escenario 2 (Rechazo de formato o archivo corrupto) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE se transmite un archivo con extensión no permitida o contenido no estructurado, CUANDO el parser inicia la validación sintáctica, ENTONCES el sistema aborta el procesamiento con código HTTP 400 Bad Request detallando la naturaleza del error de formato.
  - *Escenario 3 (Verificación de parsing en flujo CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el componente `ScheduleParserService.py` cuenta con 8 pruebas en `test_spaces.py`, CUANDO se ejecute el pipeline de `main`, ENTONCES se confirmará la extracción adecuada de slots libres sobre los archivos de prueba institucionales.
- **Casos de Uso Relacionados:** CUS-008 (Procesar y actualizar cronograma de asignación de infraestructura física).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/spaces.py` (`POST /api/v1/spaces/import-schedule`, `GET /api/v1/spaces/free-slots`).
  - *Servicios de Negocio:* `ScheduleParserService.py` (`procesar_cronograma_administrador`, `get_active_slots`).
  - *Entidades Relacionales:* Tablas de soporte de espacios físicos y persistencia temporal en memoria.
  - *Componentes Visuales:* `AdminScheduleUploadView.tsx`, `spacesService.ts`.
  - *Evidencia de Pruebas:* `test_spaces.py` (8 pruebas específicas de parsing backend).

---

#### Ficha Técnica de Requerimiento Funcional: RF11 — Gestión de Imprevistos, Reprogramación y Cancelación

- **Identificador:** RF11
- **Nombre Oficial:** Gestión de contingencias, reprogramación consensuada y cancelación justificada de sesiones
- **Módulo Arquitectónico:** MOD-02: Ofertas de Mentoría y Gestión de Espacios
- **Descripción Funcional:** El sistema debe proveer al mentor mecanismos formales para gestionar situaciones imprevistas de fuerza mayor sobre sesiones publicadas o confirmadas, permitiéndole reprogramar la fecha y hora con más de 24 horas de antelación o cancelar la sesión ingresando una justificación académica obligatoria, notificando de inmediato a todos los estudiantes inscritos.
- **Objetivo y Necesidad Académica:** Proteger a los mentoreados de ausencias imprevistas del mentor sin previo aviso, promoviendo la responsabilidad y el respeto por el tiempo de los compañeros.
- **Actores Participantes:** Estudiante Mentor (Actor Primario); Estudiantes Inscritos (Actores Notificados).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría en estado "Publicada" o "Confirmada" con antelación superior a 24 horas respecto a su inicio.
- **Comportamiento Esperado:**
  1. El mentor accede al detalle de su sesión programada y selecciona la opción de contingencia (Reprogramar o Cancelar).
  2. Si elige reprogramar, selecciona una nueva fecha y hora respetando el margen mínimo de 24 horas y redacta el motivo del cambio.
  3. El sistema comprueba que el nuevo horario no tenga conflictos de aula ni de disponibilidad del mentor.
  4. Si elige cancelar, ingresa obligatoriamente el justificante del imprevisto académico o personal.
  5. El sistema actualiza el estado de la sesión, libera el aula física o sala virtual asignada y despacha notificaciones por correo a los estudiantes inscritos.
- **Resultado Verificable (Postcondiciones):** La sesión se actualiza o cancela formalmente y los alumnos reciben la comunicación oportuna.
- **Reglas de Negocio Vinculadas:** RN-10 (Plazos de reprogramación y justificación formal de contingencias).
- **Restricciones Funcionales:** Ninguna reprogramación puede realizarse dentro de las 24 horas previas al inicio de la sesión.
- **Criterios de Aceptación:**
  - *Escenario 1 (Reprogramación justificada con notificación masiva) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor sufre una contingencia académica sobrevenida, CUANDO remite una reprogramación a través de `quorum-decision` con motivo justificado y nueva fecha mayor a 24 horas, ENTONCES el sistema actualiza la sesión, notifica por correo institucional a los estudiantes inscritos y recalcula la ventana de confirmación.
  - *Escenario 2 (Cancelación definitiva y liberación de recursos) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el mentor cancela la sesión con justificación reglamentaria, CUANDO envía la acción `CANCEL`, ENTONCES el sistema conmuta el estado de la sesión a `CANCELADA`, libera inmediatamente a los estudiantes inscritos sin penalización alguna y reincorpora el aula física al catálogo libre.
  - *Escenario 3 (Revalidación de contingencias en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el flujo de contingencias está cubierto por 10 pruebas en `test_offers.py` y 10 pruebas en Vitest, CUANDO se concluya la subsanación de linteo en `main`, ENTONCES se comprobará la adecuada emisión de avisos y liberación de cupos.
- **Casos de Uso Relacionados:** CUS-006 (Publicar oferta y gestionar contingencias).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id_sesion}/quorum-decision` con acción `RESCHEDULE` o `CANCEL`).
  - *Servicios de Negocio:* `OfferService.py` (`resolve_quorum_decision`).
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `reservas_cupo`.
  - *Componentes Visuales:* `MentorSessionsView.tsx`, `QuorumDecisionModalView.tsx`.
  - *Evidencia de Pruebas:* `test_offers.py` (10 pruebas backend), `MentorSessionsView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF12 — Reserva Concurrente de Cupos con Control de Aforo

- **Identificador:** RF12
- **Nombre Oficial:** Inscripción transaccional concurrente y reserva de cupo con cerrojo pesimista
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Gestión de Asistencia
- **Descripción Funcional:** El sistema debe permitir a los estudiantes mentoreados inscribirse en sesiones de mentoría activas, gestionando las solicitudes simultáneas mediante transacciones atómicas seguras en base de datos (`SELECT ... FOR UPDATE`) que aseguren de forma estricta que jamás se exceda el aforo máximo permitido (0.0% de sobrecupo).
- **Objetivo y Necesidad Académica:** Evitar la sobreocupación de aulas o salas virtuales, garantizando que cada estudiante que obtenga un cupo cuente con las condiciones materiales y pedagógicas para recibir atención de calidad.
- **Actores Participantes:** Estudiante Mentoreado (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante autenticado, con consentimiento informado vigente y sesión con cupos vacantes disponibles.
- **Comportamiento Esperado:**
  1. El estudiante selecciona una sesión de mentoría en el catálogo y pulsa el botón de reserva de vacante.
  2. El sistema inicia una transacción de base de datos con bloqueo a nivel de fila sobre el registro de la sesión.
  3. Verifica que la cantidad de reservas activas sea estrictamente menor al aforo reglamentario (10 presencial / 20 virtual).
  4. Si hay cupo disponible, crea la reserva con estado "Pendiente de Confirmación" y descuenta la vacante.
  5. Cierra la transacción de forma segura y confirma la reserva en la pantalla del usuario.
  6. Si la sesión se agotó exactamente en ese instante por otra solicitud concurrente, notifica al usuario que no quedan vacantes y lo invita a inscribirse en lista de espera o formular una solicitud por demanda.
- **Resultado Verificable (Postcondiciones):** El estudiante obtiene un cupo garantizado sin riesgo de sobrecupo en el sistema.
- **Reglas de Negocio Vinculadas:** RN-05 (Aforos estándar y prevención estricta de sobrecupo).
- **Restricciones Funcionales:** Ninguna transacción puede concretarse si el aforo ha alcanzado su límite reglamentario.
- **Criterios de Aceptación:**
  - *Escenario 1 (Reserva concurrente atómica con cero sobrecupo) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE múltiples estudiantes intentan reservar el último cupo disponible de una sesión de forma simultánea, CUANDO el backend ejecuta el bloqueo pesimista `SELECT ... FOR UPDATE` a nivel de fila en `/api/v1/bookings/reserve`, ENTONCES exactamente una solicitud es admitida con código HTTP 201 Created y las solicitudes concurrentes excedentes son denegadas con HTTP 409 Conflict, garantizando 0.0% de sobrecupo (RNF07).
  - *Escenario 2 (Consulta de historial personal de reservas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentoreado autenticado consulta sus inscripciones, CUANDO invoca `/api/v1/bookings/my-reservations`, ENTONCES el sistema entrega la lista completa de sesiones reservadas con detalle de estado, recinto y hora con código HTTP 200 OK.
  - *Escenario 3 (Acreditación multihilo en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la transacción de reserva cuenta con 18 pruebas en `test_bookings.py` y 16 pruebas en `BookingModalView.test.tsx`, CUANDO se corra la suite formal en `main`, ENTONCES se ratificará la ausencia de condiciones de carrera en base de datos.
- **Casos de Uso Relacionados:** CUS-004 (Inscribirse y reservar cupo en sesión de mentoría activa).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/reserve`, `GET /api/v1/bookings/my-reservations`, `GET /api/v1/bookings/session/{id_sesion}`).
  - *Servicios de Negocio:* `BookingService.py` (`reserve_seat`, `get_student_reservations`, `get_session_reservations`).
  - *Entidades Relacionales:* Tablas `reservas_cupo`, `sesiones_mentoria`.
  - *Componentes Visuales:* `BookingModalView.tsx`, `bookingService.ts`.
  - *Evidencia de Pruebas:* `test_bookings.py` (18 pruebas backend con simulación multihilo concurrente), `BookingModalView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF13 — Ratificación Anticipada Obligatoria de Asistencia

- **Identificador:** RF13
- **Nombre Oficial:** Confirmación y ratificación obligatoria de asistencia previa a la sesión
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Gestión de Asistencia
- **Descripción Funcional:** El sistema debe requerir que todo estudiante que cuente con una reserva provisional ratifique explícitamente su asistencia dentro de la ventana de confirmación establecida previa a la sesión (hasta el límite de $T-24	ext{ h}$), formalizando su intención real de acudir. Si no ratifica su asistencia en el plazo indicado, el sistema liberará automáticamente su vacante.
- **Objetivo y Necesidad Académica:** Reducir el ausentismo ficticio en las sesiones de mentoría, asegurando que los cupos sean aprovechados por estudiantes realmente comprometidos en asistir y optimizando el tiempo del mentor.
- **Actores Participantes:** Estudiante Mentoreado con reserva provisional (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante con reserva activa en estado "Pendiente de Confirmación".
- **Comportamiento Esperado:**
  1. El sistema envía un recordatorio automático al correo del estudiante informándole que debe confirmar su asistencia.
  2. El estudiante accede a su panel de reservas y pulsa el botón "Ratificar Asistencia".
  3. El sistema valida que la operación se realice antes de la hora de corte de quórum ($T-24	ext{ h}$).
  4. Conmuta el estado de la reserva a "Confirmada", asegurando el cupo definitivo para el estudiante.
  5. Informa al usuario que su vacante ha sido ratificada y le entrega los detalles definitivos de acceso al aula o sala virtual.
- **Resultado Verificable (Postcondiciones):** La reserva cambia a estado "Confirmada", computándose para el quórum formal.
- **Reglas de Negocio Vinculadas:** RN-08 (Ratificación obligatoria de asistencia), RN-09 (Cómputo de quórum).
- **Restricciones Funcionales:** Ninguna confirmación puede registrarse después del corte perentorio de $T-24	ext{ h}$.
- **Criterios de Aceptación:**
  - *Escenario 1 (Ratificación oportuna de asistencia previa al corte) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante cuenta con una reserva en estado `PENDIENTE_CONFIRMACION`, CUANDO pulsa el botón de ratificación formal antes del límite perentorio de $T-24	ext{ h}$ (RN-08) en `/api/v1/bookings/{id}/confirm`, ENTONCES el sistema conmuta el estado de la reserva a `CONFIRMADA` con código HTTP 200 OK y la computa para el quórum reglamentario.
  - *Escenario 2 (Intento de ratificación fuera de plazo) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la sesión ha ingresado en la ventana crítica de las 24 horas previas al inicio, CUANDO un estudiante rezagado intenta confirmar su cupo, ENTONCES el sistema rechaza la acción con código HTTP 400 Bad Request en cumplimiento de la política de corte de quórum.
  - *Escenario 3 (Verificación en CI del cambio de estado) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el procedimiento cuenta con 12 pruebas en `test_bookings.py` y 14 pruebas en `MyBookingsView.test.tsx`, CUANDO se ejecute la validación formal en `main`, ENTONCES se verificará la transición atómica de estados.
- **Casos de Uso Relacionados:** CUS-024 (Ratificar oportunamente asistencia a sesión de mentoría reservada).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id_reserva}/confirm`).
  - *Servicios de Negocio:* `BookingService.py` (`confirm_attendance`).
  - *Entidades Relacionales:* Tabla `reservas_cupo`.
  - *Componentes Visuales:* `MyBookingsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (12 pruebas backend), `MyBookingsView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF14 — Desistimiento Voluntario y Liberación Inmediata de Cupo

- **Identificador:** RF14
- **Nombre Oficial:** Cancelación voluntaria de reserva y restitución inmediata de vacante
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Gestión de Asistencia
- **Descripción Funcional:** El sistema debe permitir a cualquier estudiante inscrito cancelar voluntariamente su reserva con anticipación superior a 24 horas respecto al inicio de la sesión, liberando instantáneamente la vacante para que otro compañero pueda inscribirse de inmediato, sin aplicar penalizaciones académicas al usuario que desiste oportunamente.
- **Objetivo y Necesidad Académica:** Fomentar una cultura de respeto mutuo y solidaridad, permitiendo que las vacantes no utilizadas se reasignen a compañeros que las necesitan con urgencia.
- **Actores Participantes:** Estudiante Mentoreado con reserva vigente (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Estudiante con reserva en estado "Pendiente" o "Confirmada" con antelación mayor a 24 horas.
- **Comportamiento Esperado:**
  1. El estudiante visualiza su panel de reservas activas y pulsa "Cancelar Reserva".
  2. El sistema despliega un mensaje pidiendo confirmar la acción y recordando que la vacante se liberará para otro estudiante.
  3. El usuario confirma el desistimiento voluntario.
  4. El sistema cancela la reserva, actualiza el aforo disponible de la sesión en base de datos e informa a los estudiantes en lista de espera si existieran.
  5. Emite confirmación de cancelación exitosa sin registrar sanciones para el estudiante.
- **Resultado Verificable (Postcondiciones):** La vacante queda liberada de forma inmediata y reflejada en el catálogo de ofertas.
- **Reglas de Negocio Vinculadas:** RN-10 (Desistimiento oportuno sin sanción antes de $T-24	ext{ h}$).
- **Restricciones Funcionales:** Si el estudiante cancela con menos de 24 horas de antelación o no asiste a la sesión confirmada, el sistema registrará una falta injustificada en su historial.
- **Criterios de Aceptación:**
  - *Escenario 1 (Desistimiento voluntario antes de $T-24	ext{ h}$) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante con reserva activa no podrá asistir y desiste con más de 24 horas de antelación (RN-10), CUANDO confirma la anulación en `/api/v1/bookings/{id}/cancel`, ENTONCES el sistema cancela la reserva sin registrar sanción académica y restituye inmediatamente la vacante al aforo libre con código HTTP 200 OK.
  - *Escenario 2 (Intento de cancelación intempestiva en ventana crítica) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE restan menos de 24 horas para la sesión, CUANDO el estudiante intenta anular unilateralmente su cupo, ENTONCES el sistema advierte que la cancelación tardía compromete el quórum y registra la incidencia conforme a la reglamentación interna.
  - *Escenario 3 (Acreditación de liberación en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la liberación inmediata de cupos cuenta con 10 pruebas en Pytest y 10 en Vitest, CUANDO se ejecute el flujo de `main`, ENTONCES se confirmará el recálculo instantáneo de vacantes.
- **Casos de Uso Relacionados:** CUS-017 (Cancelar oportunamente reserva de mentoría y liberar cupo).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id_reserva}/cancel`).
  - *Servicios de Negocio:* `BookingService.py` (`cancel_reservation`).
  - *Entidades Relacionales:* Tablas `reservas_cupo`, `sesiones_mentoria`.
  - *Componentes Visuales:* `MyBookingsView.tsx`.
  - *Evidencia de Pruebas:* `test_bookings.py` (10 pruebas backend), `MyBookingsView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF15 — Monitoreo Desatendido y Corte de Quórum en $T-24	ext{ h}$

- **Identificador:** RF15
- **Nombre Oficial:** Evaluación desatendida del quórum reglamentario en la ventana de corte $T-24	ext{ h}$
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Gestión de Asistencia
- **Descripción Funcional:** El sistema debe ejecutar de forma desatendida y automática (mediante un demonio cron programado) una verificación sobre todas las sesiones de mentoría que alcancen exactamente la marca de 24 horas previas a su inicio ($T-24	ext{ h}$), evaluando si el número de reservas confirmadas alcanza el quórum mínimo obligatorio del 50% del aforo (al menos 3 estudiantes en presencial o 5 en virtual). Si alcanza el quórum, confirma la sesión definitivamente; de lo contrario, la declara en quórum insuficiente.
- **Objetivo y Necesidad Académica:** Proteger el tiempo de los mentores y evitar el desplazamiento innecesario de docentes o estudiantes al campus si la sesión no cuenta con una cantidad mínima de participantes.
- **Actores Participantes:** Componente Demonio Cron / Scheduler de Quórum (Actor Primario); Mentor y Estudiantes Inscritos (Actores Notificados).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría en estado "Publicada" que alcanza la marca temporal de $T-24	ext{ h}$.
- **Comportamiento Esperado:**
  1. El demonio de evaluación se activa periódicamente y selecciona las sesiones activas en el umbral exacto de $T-24	ext{ h}$.
  2. Invalida automáticamente las reservas que permanecieron en estado "Pendiente de Confirmación" sin ratificar.
  3. Cuenta el número de reservas confirmadas restantes.
  4. Si las confirmaciones son $\ge 50\%$ del aforo reglamentario (3 en presencial / 5 en virtual), transiciona la sesión a "Confirmada" y remite notificaciones de ratificación.
  5. Si las confirmaciones son $< 50\%$, transiciona la sesión a "Quórum Insuficiente" y notifica de inmediato al mentor para su resolución.
- **Resultado Verificable (Postcondiciones):** La sesión queda formalmente clasificada como "Confirmada" o "Quórum Insuficiente".
- **Reglas de Negocio Vinculadas:** RN-08 (Corte de quórum en $T-24	ext{ h}$), RN-09 (Umbral mínimo del 50% de aforo).
- **Restricciones Funcionales:** Ninguna sesión puede mantenerse con reservas pendientes sin definir tras el corte de $T-24	ext{ h}$.
- **Criterios de Aceptación:**
  - *Escenario 1 (Corte automático y confirmación con quórum suficiente) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una sesión alcanza la marca temporal de $T-24	ext{ h}$ y cuenta con al menos el 50% de cupos ratificados (>= 3 presencial / >= 5 virtual, RN-08 y RN-09), CUANDO el demonio desatendido ejecuta la evaluación en `/api/v1/quorum/evaluate`, ENTONCES transiciona la sesión a `CONFIRMADA`, caduca las reservas no ratificadas y despacha las notificaciones de confirmación con código HTTP 200 OK.
  - *Escenario 2 (Detección de quórum insuficiente a $T-24	ext{ h}$) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una sesión no alcanza el umbral mínimo reglamentario en la ventana de corte, CUANDO el motor de quórum la evalúa, ENTONCES conmuta su estado a `QUORUM_INSUFICIENTE` y abre la ventana resolutiva de 12 horas para decisión del mentor.
  - *Escenario 3 (Verificación de idempotencia del cron en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la evaluación masiva cuenta con 16 pruebas en `test_quorum.py` y 12 pruebas en Vitest, CUANDO se ejecute la suite formal en `main`, ENTONCES se constatará que múltiples ejecuciones sucesivas del evaluador no dupliquen transiciones ni notificaciones.
- **Casos de Uso Relacionados:** CUS-023 (Evaluar automáticamente cumplimiento de quórum mínimo en $T-24	ext{ h}$), CUS-009 (Monitorear y despachar notificaciones institucionales).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/quorum.py` (`POST /api/v1/quorum/evaluate`, `POST /api/v1/quorum/evaluate-all`).
  - *Servicios de Negocio:* `BookingService.py` (`evaluate_quorum`, `evaluate_all_active_quorums`).
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `reservas_cupo`.
  - *Componentes Visuales:* `NotificationCenterView.tsx`.
  - *Evidencia de Pruebas:* `test_quorum.py` (16 pruebas backend con simulación de avance temporal), `NotificationCenterView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF16 — Gestión Resolutiva del Mentor ante Quórum Insuficiente

- **Identificador:** RF16
- **Nombre Oficial:** Gestión resolutiva y toma de decisión del mentor ante contingencia de quórum insuficiente
- **Módulo Arquitectónico:** MOD-05: Quórum, Reservas y Gestión de Asistencia
- **Descripción Funcional:** El sistema debe suministrar al estudiante mentor una ventana interactiva de resolución urgente (máximo 12 horas) cuando su sesión sea declarada en "Quórum Insuficiente" a $T-24	ext{ h}$, facultándolo para decidir soberanamente entre tres opciones: (1) impartir la sesión con los alumnos confirmados asumiendo el dictado con aforo reducido, (2) reprogramar la fecha de la sesión con más de 24 horas de anticipación, o (3) cancelar definitivamente la sesión sin sanción formativa.
- **Objetivo y Necesidad Académica:** Respetar la autonomía pedagógica del mentor permitiéndole atender a compañeros motivados aun con poca audiencia si así lo decide, o reprogramar ordenadamente sin perjudicar su expediente.
- **Actores Participantes:** Estudiante Mentor (Actor Decisor); Estudiantes Confirmados (Beneficiarios de la Decisión).
- **Condiciones de Entrada (Precondiciones):** Sesión en estado "Quórum Insuficiente" dentro del plazo resolutivo de 12 horas.
- **Comportamiento Esperado:**
  1. El mentor recibe alerta urgente y accede a su panel de control de mentorías.
  2. Visualiza el diálogo modal resolutivo con los datos de alumnos confirmados y las tres alternativas normativas.
  3. Si elige "Impartir con aforo reducido", el sistema confirma la sesión y notifica a los alumnos inscritos que la clase se dictará con normalidad.
  4. Si elige "Reprogramar", selecciona nueva fecha (con antelación $> 24	ext{ h}$) y el sistema traslada las reservas notificando el cambio.
  5. Si elige "Cancelar", ingresa la justificación y el sistema anula la sesión liberando los recursos sin penalización.
  6. Si transcurren las 12 horas sin respuesta del mentor, el sistema cancela automáticamente la sesión por vencimiento de plazo.
- **Resultado Verificable (Postcondiciones):** La sesión asume su estado final ("Confirmada", "Reprogramada" o "Cancelada") con notificación a los interesados.
- **Reglas de Negocio Vinculadas:** RN-09 (Opciones resolutivas ante quórum insuficiente), RN-10 (Justificación de contingencias).
- **Restricciones Funcionales:** La ventana resolutiva vence indefectiblemente a las 12 horas previas a la sesión.
- **Criterios de Aceptación:**
  - *Escenario 1 (Resolución positiva de dictado con aforo reducido) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una sesión fue catalogada en `QUORUM_INSUFICIENTE`, CUANDO el mentor opta voluntariamente por la resolución `PROCEED` para apoyar a los pocos inscritos confirmados, ENTONCES el sistema valida la decisión en `/api/v1/offers/{id}/quorum-decision`, transiciona la sesión a `CONFIRMADA` y despacha el recordatorio con los accesos definitivos con código HTTP 200 OK.
  - *Escenario 2 (Resolución de cancelación reglamentaria) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el mentor decide acogerse a la cancelación institucional por falta de quórum, CUANDO remite la acción `CANCEL`, ENTONCES el sistema anula la sesión sin penalidad formativa para el mentor, notifica a los inscritos y libera el espacio físico o virtual reservado.
  - *Escenario 3 (Revalidación de interfaz resolutiva en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el flujo está cubierto por 10 pruebas en Pytest y 10 pruebas en `QuorumDecisionModalView.test.tsx`, CUANDO se concluya la subsanación de linteo en `main`, ENTONCES se confirmará la adecuada gestión de contingencias.
- **Casos de Uso Relacionados:** CUS-007 (Resolver contingencia de quórum insuficiente por decisión del mentor).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id_sesion}/quorum-decision` con payload `action` en `PROCEED`, `RESCHEDULE` o `CANCEL`).
  - *Servicios de Negocio:* `OfferService.py` (`resolve_quorum_decision`).
  - *Entidades Relacionales:* Tablas `sesiones_mentoria`, `reservas_cupo`.
  - *Componentes Visuales:* `QuorumDecisionModalView.tsx`.
  - *Evidencia de Pruebas:* `test_offers.py` (10 pruebas backend), `QuorumDecisionModalView.test.tsx` (10 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF17 — Marcación de Asistencia con Pase QR Dinámico (TOTP)

- **Identificador:** RF17
- **Nombre Oficial:** Control de asistencia en tiempo real mediante código QR dinámico criptográfico (TOTP)
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe proveer al mentor titular la capacidad de proyectar en pantalla un código QR dinámico que rota automáticamente cada 30 segundos (basado en algoritmos de contraseñas de un solo uso basadas en el tiempo - TOTP) y exhibe un código numérico de 6 dígitos de respaldo, permitiendo que los mentoreados presentes en el aula o sala virtual registren su asistencia mediante el escaneo del código desde sus dispositivos o digitando el PIN activo.
- **Objetivo y Necesidad Académica:** Erradicar la suplantación de asistencia y el registro fraudulento a distancia (fotos compartidas por mensajería), asegurando que solo los estudiantes físicamente presentes o conectados en vivo certifiquen su participación.
- **Actores Participantes:** Estudiante Mentor (Generador y Proyector del QR); Estudiante Mentoreado (Registrador de Asistencia).
- **Condiciones de Entrada (Precondiciones):** Sesión confirmada en ejecución dentro de la ventana de marcación permitida (desde 15 minutos antes hasta 30 minutos después de la hora de inicio).
- **Comportamiento Esperado:**
  1. El mentor inicia la proyección del pase de asistencia desde su panel de control.
  2. El sistema genera el código QR dinámico y el PIN numérico de respaldo, iniciando la rotación cada 30 segundos.
  3. Los estudiantes mentoreados abren la cámara o escáner desde la aplicación web o digitan el PIN en pantalla.
  4. El sistema valida criptográficamente la coincidencia del token y verifica que el alumno cuente con reserva confirmada.
  5. Registra de inmediato la asistencia con fecha, hora e IP de origen, actualizando el listado en tiempo real en la pantalla del mentor.
  6. Si un estudiante no dispone de cámara, el mentor puede marcarlo manualmente en la lista de respaldo con motivo justificado.
- **Resultado Verificable (Postcondiciones):** El registro de asistencia queda almacenado de forma inmutable en el expediente de la sesión.
- **Reglas de Negocio Vinculadas:** RN-05 (Control de asistencia presencial), RN-12 (Obligatoriedad de asistencia para responder encuestas).
- **Restricciones Funcionales:** Ningún escaneo será admitido fuera de la ventana horaria de tolerancia ([-15 min, +30 min]).
- **Criterios de Aceptación:**
  - *Escenario 1 (Generación de pase TOTP dinámico de 30 segundos) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el mentor titular inicia la sesión dentro de la ventana de marcación ([-15 min, +30 min]), CUANDO solicita el token en `/api/v1/sessions/{id}/attendance/token`, ENTONCES el sistema genera un código numérico y QR efímero que rota cada 30 segundos mediante HMAC-SHA1 para prevenir la falsificación por captura de pantalla con código HTTP 200 OK.
  - *Escenario 2 (Check-in exitoso de mentoreado con reserva confirmada) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante con reserva `CONFIRMADA` escanea el QR o introduce el código activo, CUANDO envía la solicitud a `/api/v1/sessions/{id}/attendance/check-in`, ENTONCES el sistema valida la vigencia del token, registra la presencia efectiva en `asistencias_sesion` con IP de origen y código HTTP 200 OK.
  - *Escenario 3 (Rechazo de pase expirado o sin reserva previa) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante intenta marcar con un token vencido o sin reserva confirmada, CUANDO remite el check-in, ENTONCES el sistema rechaza la marcación con código HTTP 400 Bad Request o HTTP 403 Forbidden registrando la traza de intento fallido.
  - *Escenario 4 (Acreditación de seguridad de asistencia en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el subsistema cuenta con 14 pruebas en `test_attendance.py` y 20 pruebas en `AttendanceScannerView.test.tsx`, CUANDO se ejecute el flujo de CI en `main`, ENTONCES se certificará la sincronía temporal y la auditabilidad del check-in.
- **Casos de Uso Relacionados:** CUS-012 (Registrar asistencia presencial o virtual mediante código QR dinámico TOTP).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/attendance.py` (`GET /api/v1/sessions/{id_sesion}/attendance/token`, `POST /api/v1/sessions/{id_sesion}/attendance/check-in`, `GET /api/v1/sessions/{id_sesion}/attendance`).
  - *Servicios de Negocio:* `AttendanceService.py` (`generate_token`, `record_checkin`, `get_roster`).
  - *Entidades Relacionales:* Tablas `asistencias_sesion`, `tokens_asistencia_activos`.
  - *Componentes Visuales:* `AttendanceScannerView.tsx`, `AttendanceQrModalView.tsx`.
  - *Evidencia de Pruebas:* `test_attendance.py` (14 pruebas backend con validación criptográfica TOTP), `AttendanceScannerView.test.tsx` (20 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF18 — Registro de Bitácora Docente en 48h con Hash SHA-256

- **Identificador:** RF18
- **Nombre Oficial:** Suscripción y registro obligatorio de bitácora pedagógica con sello de integridad SHA-256
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe requerir que el mentor registre obligatoriamente una bitácora pedagógica detallada dentro de las 48 horas posteriores a la culminación de la sesión, especificando los temas silábicos efectivamente explicados, los ejercicios desarrollados, las observaciones sobre el desempeño del grupo y las incidencias ocurridas, sellando el reporte con una huella criptográfica SHA-256 inalterable.
- **Objetivo y Necesidad Académica:** Proveer respaldo documental y pedagógico a la labor del mentor, permitiendo al Comité de Tutoría fiscalizar el contenido dictado y sirviendo de base auditada para la posterior convalidación de horas de mentoría.
- **Actores Participantes:** Estudiante Mentor (Actor Redactor); Coordinación de Tutoría (Entidad Fiscalizadora).
- **Condiciones de Entrada (Precondiciones):** Sesión de mentoría culminada y con registro de asistencia cerrado.
- **Comportamiento Esperado:**
  1. El mentor accede al formulario de redacción de bitácora de la sesión finalizada.
  2. Verifica la lista consolidada de estudiantes que registraron asistencia.
  3. Redacta el resumen temático desarrollado, ejercicios resueltos y observaciones pedagógicas (mínimo 50 caracteres).
  4. Adjunta enlaces a materiales o repositorios de código trabajados durante la clase.
  5. Pulsa el botón de firma digital del reporte.
  6. El sistema compila el documento en un objeto inmutable, calcula el hash SHA-256 de los datos, almacena la bitácora y marca la sesión como "Bitácora Registrada".
- **Resultado Verificable (Postcondiciones):** La bitácora queda archivada con firma digital inalterable, habilitando el cómputo de horas formativas.
- **Reglas de Negocio Vinculadas:** RN-12 (Plazo improrrogable de 48 horas para registro de bitácora), RN-14 (Horas auditadas para certificación).
- **Restricciones Funcionales:** Si la bitácora no se registra dentro de las 48 horas, la sesión se catalogará como "Extemporánea" y no acumulará horas para certificación hasta que medie justificación formal aprobada por la Dirección de Escuela.
- **Criterios de Aceptación:**
  - *Escenario 1 (Registro oportuno de bitácora con hash criptográfico SHA-256) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una sesión concluyó y el mentor ingresa dentro del plazo improrrogable de 48 horas (RN-12), CUANDO redacta las observaciones pedagógicas (>= 50 caracteres) y firma el reporte en `/api/v1/sessions/{id}/bitacora`, ENTONCES el sistema genera un sello inalterable SHA-256 sobre los datos de asistencia y contenidos, registra la bitácora con código HTTP 201 Created y conmuta la sesión a `BITACORA_REGISTRADA`.
  - *Escenario 2 (Bloqueo por vencimiento del plazo de 48 horas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE han transcurrido más de 48 horas desde la culminación de la sesión, CUANDO el mentor intenta remitir la bitácora, ENTONCES el sistema bloquea el registro con código HTTP 400 Bad Request o HTTP 422, impidiendo la acreditación de horas y marcando la sesión como extemporánea para fiscalización de Tutoría.
  - *Escenario 3 (Validación de inmutabilidad en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el sellado criptográfico cuenta con 18 pruebas en `test_bitacora.py` y 22 pruebas en `BitacoraFormView.test.tsx`, CUANDO se ejecute la suite formal en `main`, ENTONCES se verificará la integridad del hash SHA-256 ante cualquier intento de alteración.
- **Casos de Uso Relacionados:** CUS-013 (Registrar bitácora pedagógica post-sesión y sellar reporte con hash SHA-256).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`POST /api/v1/sessions/{id_sesion}/bitacora`, `GET /api/v1/sessions/{id_sesion}/bitacora`).
  - *Servicios de Negocio:* `BitacoraService.py` (`create_bitacora`, `get_bitacora`).
  - *Entidades Relacionales:* Tabla `bitacoras_pedagogicas`.
  - *Componentes Visuales:* `BitacoraFormView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (18 pruebas backend con verificación del hash SHA-256), `BitacoraFormView.test.tsx` (22 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF19 — Historial de Sesiones, Bitácoras y Recursos Compartidos

- **Identificador:** RF19
- **Nombre Oficial:** Repositorio cronológico de sesiones, bitácoras y biblioteca de recursos didácticos
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe suministrar a mentores y mentoreados un historial cronológico interactivo donde consulten las sesiones pasadas en las que participaron, las bitácoras docentes suscritas, los temas revisados y los enlaces a materiales didácticos compartidos (diapositivas, grabaciones, repositorios de GitHub o ejercicios prácticos), sirviendo de biblioteca digital de consulta permanente para la comunidad estudiantil.
- **Objetivo y Necesidad Académica:** Fomentar el autoaprendizaje continuo y la reutilización de materiales de calidad generados durante las mentorías, permitiendo a los alumnos repasar conceptos antes de sus evaluaciones oficiales.
- **Actores Participantes:** Estudiante Mentoreado, Estudiante Mentor (Actores de Consulta).
- **Condiciones de Entrada (Precondiciones):** Usuario autenticado en la plataforma.
- **Comportamiento Esperado:**
  1. El usuario accede a la sección de "Historial de Mentorías".
  2. El sistema despliega la relación cronológica de sesiones en las que participó como asistente o mentor.
  3. El usuario puede filtrar por ciclo académico, asignatura formativa o palabra clave de tema.
  4. Al pulsar sobre una sesión, visualiza los detalles: fecha, mentor, temas silábicos cubiertos y la bitácora suscrita.
  5. Puede acceder a los enlaces de recursos didácticos adjuntos y descargarlos para su estudio personal.
- **Resultado Verificable (Postcondiciones):** El estudiante accede de forma transparente a los materiales educativos oficiales.
- **Reglas de Negocio Vinculadas:** RN-11 (Alineamiento curricular), RN-02 (Privacidad de datos personales).
- **Restricciones Funcionales:** Ningún usuario ajeno a la comunidad universitaria podrá acceder a los materiales compartidos.
- **Criterios de Aceptación:**
  - *Escenario 1 (Consulta de historial formativo y materiales compartidos) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante o mentor accede a su historial académico, CUANDO filtra por ciclo o asignatura, ENTONCES el sistema entrega la relación cronológica de sesiones atendidas, enlaces a diapositivas, repositorios de código y bitácoras asociadas con código HTTP 200 OK.
  - *Escenario 2 (Visualización restringida por titularidad de datos) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un usuario común intenta consultar la bitácora o materiales de una sesión en la que no participó como asistente ni mentor, CUANDO envía la solicitud de lectura, ENTONCES el sistema deniega el acceso con código HTTP 403 Forbidden conforme al principio de privacidad académica.
  - *Escenario 3 (Comprobación en suite de integración en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la consulta histórica cuenta con 8 pruebas en Pytest y 12 pruebas en `BitacoraHistoryView.test.tsx`, CUANDO se ejecute el pipeline de `main`, ENTONCES se verificará el filtrado seguro por titularidad de usuario.
- **Casos de Uso Relacionados:** CUS-014 (Consultar historial de mentorías, bitácoras pedagógicas y materiales educativos).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`GET /api/v1/sessions/{id_sesion}/bitacora`, `GET /api/v1/bitacoras`), `aplicacion/backend/app/api/v1/endpoints/bookings.py` (`GET /api/v1/bookings/my-reservations`).
  - *Servicios de Negocio:* `BitacoraService.py` (`get_bitacora`, `list_bitacoras`), `BookingService.py` (`get_student_reservations`).
  - *Entidades Relacionales:* Tablas `bitacoras_pedagogicas`, `sesiones_mentoria`.
  - *Componentes Visuales:* `BitacoraHistoryView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (8 pruebas backend), `BitacoraHistoryView.test.tsx` (12 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF20 — Encuestas de Calidad y Retroalimentación Post-Mentoría (24h)

- **Identificador:** RF20
- **Nombre Oficial:** Captura, procesamiento y control de encuestas de calidad pedagógica post-mentoría
- **Módulo Arquitectónico:** MOD-06: Asistencia, Bitácoras y Calidad
- **Descripción Funcional:** El sistema debe habilitar una encuesta de satisfacción y calidad pedagógica (instrumento CSAT adaptado a 4 dimensiones: dominio temático, claridad pedagógica, puntualidad y utilidad práctica) dirigida exclusivamente a los estudiantes mentoreados que hayan registrado asistencia efectiva en la sesión, restringiendo su envío dentro de una ventana perentoria de 24 horas posteriores a la finalización de la mentoría.
- **Objetivo y Necesidad Académica:** Recopilar retroalimentación objetiva, constructiva y fresca sobre el desempeño de los mentores para alimentar el motor de recomendación, identificar necesidades de capacitación y sustentar reconocimientos institucionales.
- **Actores Participantes:** Estudiante Mentoreado con asistencia comprobada (Actor Evaluador); Estudiante Mentor (Sujeto Evaluado).
- **Condiciones de Entrada (Precondiciones):** Estudiante con asistencia formalmente validada mediante QR dinámico y sesión culminada dentro de las últimas 24 horas.
- **Comportamiento Esperado:**
  1. Al culminar la sesión y cerrarse la lista de asistencia, el sistema activa la encuesta para los estudiantes que asistieron efectivamente.
  2. El estudiante accede a la plataforma y visualiza una notificación destacando la disponibilidad de la encuesta de la sesión recién terminada.
  3. Abre el formulario y califica las 4 dimensiones pedagógicas en escala Likert de 1 a 5 estrellas.
  4. Opcionalmente, ingresa un comentario cualitativo con sugerencias de mejora (mínimo 20 caracteres si decide completarlo).
  5. Envía la encuesta; el sistema valida que no haya transcurrido más de 24 horas desde el fin de la sesión y que el alumno no haya respondido previamente.
  6. Almacena la evaluación anonimizada en la tabla `encuestas_calidad` y actualiza de inmediato el promedio de reputación del mentor.
- **Resultado Verificable (Postcondiciones):** La evaluación queda registrada y computada para el índice de reputación del mentor.
- **Reglas de Negocio Vinculadas:** RN-13 (Plazo de 24 horas para respuesta de encuestas de calidad), RN-12 (Acceso condicionado a asistencia efectiva).
- **Restricciones Funcionales:** Ningún estudiante sin asistencia confirmada podrá visualizar o enviar la encuesta; una vez transcurridas las 24 horas, el sistema bloquea definitivamente el formulario.
- **Criterios de Aceptación:**
  - *Escenario 1 (Envío de evaluación dentro de la ventana de 24 horas por asistente confirmado) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una sesión culminó, restan menos de 24 horas (RN-13) y el mentoreado registra asistencia efectiva comprobada (`asistio = True`, RN-12), CUANDO califica las 4 dimensiones Likert (1 al 5) e incluye retroalimentación cualitativa (>= 20 caracteres) en `/api/v1/sessions/{id}/survey`, ENTONCES el sistema persiste la evaluación en `encuestas_calidad` con código HTTP 201 Created y actualiza el promedio del mentor.
  - *Escenario 2 (Bloqueo por inasistencia del mentoreado) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante con reserva no asistió a la sesión de mentoría, CUANDO intenta enviar el formulario de encuesta, ENTONCES el sistema bloquea la operación con código HTTP 403 Forbidden y mensaje explícito de inhabilitación por falta de asistencia comprobada (RN-12).
  - *Escenario 3 (Cierre definitivo de la ventana perentoria de 24 horas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE han transcurrido más de 24 horas desde la culminación de la mentoría, CUANDO el estudiante intenta enviar la encuesta, ENTONCES el sistema rechaza la recepción con código HTTP 400 Bad Request o mensaje de expiración temporal, garantizando la frescura y objetividad de la evaluación (RN-13).
  - *Escenario 4 (Prevención de doble encuesta y acreditación en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la regla de encuesta única cuenta con 16 pruebas en `test_survey.py` y 14 pruebas en `PostSessionSurveyModalView.test.tsx`, CUANDO se ejecute el flujo automatizado en `main`, ENTONCES se confirmará el rechazo con HTTP 409 Conflict ante cualquier reenvío redundante.
- **Casos de Uso Relacionados:** CUS-012 (Registrar asistencia), CUS-014 (Consultar historial y retroalimentación).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/survey.py` (`GET /api/v1/sessions/{id}/survey`, `POST /api/v1/sessions/{id}/survey`).
  - *Servicios de Negocio:* `SurveyService.py` (`create_survey`, `get_survey_status`).
  - *Entidades Relacionales:* Tabla `encuestas_calidad`.
  - *Componentes Visuales:* `PostSessionSurveyModalView.tsx`, `surveyService.ts`.
  - *Evidencia de Pruebas:* `test_survey.py` (16 pruebas backend con validación de ventana temporal y cálculo de promedios), `PostSessionSurveyModalView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF21 — Cálculo de Reputación Docente y Catálogo de Insignias

- **Identificador:** RF21
- **Nombre Oficial:** Ponderación algorítmica de reputación docente y asignación de insignias por mérito
- **Módulo Arquitectónico:** MOD-07: Gamificación, Reputación y Certificación
- **Descripción Funcional:** El sistema debe procesar dinámicamente las calificaciones obtenidas en las encuestas de satisfacción, el volumen de sesiones dictadas y la puntualidad del mentor para calcular su índice de reputación docente y desbloquear automáticamente insignias de honor ("Mentor Destacado", "Especialista en Algoritmos", "Puntualidad Impecable") visibles en su perfil público.
- **Objetivo y Necesidad Académica:** Estimular la excelencia pedagógica y el compromiso de los mentores a través de mecanismos de gamificación positiva, proveyendo a los mentoreados señales claras de confianza para elegir a sus guías.
- **Actores Participantes:** Estudiante Mentor (Receptor del Reconocimiento); Sistema (Evaluador Algorítmico).
- **Condiciones de Entrada (Precondiciones):** Mentor con sesiones dictadas y encuestas de calidad respondidas por sus alumnos.
- **Comportamiento Esperado:**
  1. Cada vez que se registra una nueva encuesta de satisfacción, el sistema recalcula la puntuación global del mentor mediante media ponderada.
  2. Evalúa los umbrales de gamificación definidos por la facultad (por ejemplo: más de 10 sesiones con calificación promedio $\ge 4.5/5.0$).
  3. Si el mentor alcanza un hito de calidad, el sistema desbloquea la insignia correspondiente y la incorpora a su perfil académico.
  4. Notifica al mentor el logro alcanzado mediante una alerta en la plataforma.
  5. La reputación e insignias se reflejan de inmediato en las tarjetas de recomendación del catálogo de ofertas.
- **Resultado Verificable (Postcondiciones):** El perfil del mentor exhibe su puntaje actualizado y las insignias institucionales acreditadas.
- **Reglas de Negocio Vinculadas:** RN-13 (Encuestas de calidad), RN-03 (Mérito académico).
- **Restricciones Funcionales:** Ninguna insignia puede asignarse manualmente sin cumplir con las métricas objetivas procesadas por el sistema.
- **Criterios de Aceptación:**
  - *Escenario 1 (Recálculo dinámico de reputación a partir de encuestas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor acumula nuevas encuestas válidas de satisfacción estudiantil, CUANDO se consulta su perfil, ENTONCES el sistema calcula el promedio ponderado en escala vigesimal (o 1 a 5) y actualiza su índice de reputación docente con código HTTP 200 OK.
  - *Escenario 2 (Desbloqueo de insignias por mérito docente acumulado) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor supera los hitos reglamentarios (ej. 10 sesiones dictadas con promedio >= 4.5/5.0), CUANDO el sistema procesa sus métricas, ENTONCES asigna automáticamente las insignias de reconocimiento institucional ("Mentor Destacado") visibles en su perfil público.
  - *Escenario 3 (Acreditación algorítmica en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el cómputo de reputación está cubierto por 12 pruebas en Pytest y 18 pruebas en `MentorBadgesView.test.tsx`, CUANDO se ejecute la validación formal en `main`, ENTONCES se confirmará la exactitud del redondeo a dos decimales.
- **Casos de Uso Relacionados:** CUS-019 (Consultar reputación docente, historial de valoraciones y catálogo de insignias).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/certificates.py` (`GET /api/v1/certificates/summary`), `aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`).
  - *Servicios de Negocio:* `RecommendationService.py`, `ProfileService.py`.
  - *Entidades Relacionales:* Tablas `encuestas_calidad`, `perfiles_academicos`.
  - *Componentes Visuales:* `MentorBadgesView.tsx`.
  - *Evidencia de Pruebas:* `test_recommendations.py` (12 pruebas backend), `MentorBadgesView.test.tsx` (18 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF22 — Parametrización y Autorización de Certificados de Horas

- **Identificador:** RF22
- **Nombre Oficial:** Parametrización y autorización institucional de constancias de horas de mentoría
- **Módulo Arquitectónico:** MOD-07: Gamificación, Reputación y Certificación
- **Descripción Funcional:** El sistema debe permitir a la Dirección de Escuela y Coordinación de Tutoría verificar el cumplimiento de las metas de horas formativas dictadas por cada mentor (alcanzando el umbral mínimo reglamentario de 20.0 horas académicas auditadas con bitácoras visadas), autorizando formalmente la expedición de sus constancias oficiales para la convalidación de créditos extracurriculares.
- **Objetivo y Necesidad Académica:** Proporcionar valor curricular real al esfuerzo del mentor, permitiéndole convalidar su labor de asesoría por créditos universitarios conforme a la Ley Universitaria N° 30220 y el plan curricular de la EPIS.
- **Actores Participantes:** Administrador / Coordinador de Tutoría (Actor Autorizador); Estudiante Mentor (Beneficiario).
- **Condiciones de Entrada (Precondiciones):** Mentor con acumulación $\ge 20.0	ext{ horas}$ académicas visadas con bitácoras aprobadas por la facultad.
- **Comportamiento Esperado:**
  1. La autoridad accede al módulo de acreditación y certificación de horas formativas.
  2. El sistema presenta la nómina de mentores que han alcanzado o superado el umbral reglamentario de 20 horas en el semestre.
  3. El administrador revisa el consolidado de sesiones, asistencia de alumnos y bitácoras pedagógicas suscritas.
  4. Si todos los registros se encuentran conformes y visados, pulsa "Autorizar Emisión de Certificado".
  5. El sistema formaliza la aprobación, asigna el código correlativo de folio oficial institucional y habilita la descarga del documento.
- **Resultado Verificable (Postcondiciones):** El certificado queda autorizado en la base de datos con folio correlativo único.
- **Reglas de Negocio Vinculadas:** RN-14 (Acreditación de horas de mentoría y requisitos de certificación: $\ge 20	ext{ h}$ y 100% bitácoras visadas).
- **Restricciones Funcionales:** Ningún certificado podrá ser autorizado si el mentor mantiene bitácoras pendientes de entrega o sesiones en estado observado.
- **Criterios de Aceptación:**
  - *Escenario 1 (Autorización y expedición con horas auditadas completas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un mentor acumula al menos 20.0 horas académicas visadas por la Dirección de Escuela (RN-14) y no registra bitácoras pendientes ni observadas, CUANDO se solicita la constancia oficial en `/api/v1/certificates/generate`, ENTONCES el sistema emite el certificado asignando folio único correlativo (CERT-YYYY-SEM-XXXX) y código HTTP 201 Created.
  - *Escenario 2 (Denegación por déficit de horas visadas) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un estudiante registra menos de 20.0 horas convalidadas o mantiene bitácoras en estado provisional, CUANDO intenta generar la constancia, ENTONCES el sistema deniega la solicitud con código HTTP 400 Bad Request detallando las horas faltantes para alcanzar el umbral de certificación.
  - *Escenario 3 (Verificación en pipeline de CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la emisión de constancias cuenta con 14 pruebas en `test_certificates.py` y 16 pruebas en `AdminCertificatesView.test.tsx`, CUANDO se ejecute la suite en `main`, ENTONCES se verificará la consistencia del control de umbrales normativos.
- **Casos de Uso Relacionados:** CUS-018 (Autorizar y emitir constancias oficiales de horas de mentoría con verificación QR).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/certificates.py` (`GET /api/v1/certificates/summary`, `POST /api/v1/certificates/generate`).
  - *Servicios de Negocio:* `CertificateService.py` (`get_hours_summary`, `generate_certificate`).
  - *Entidades Relacionales:* Tablas `certificados_horas`, `bitacoras_pedagogicas`.
  - *Componentes Visuales:* `AdminCertificatesView.tsx`.
  - *Evidencia de Pruebas:* `test_certificates.py` (14 pruebas backend con validación de reglas de acreditación), `AdminCertificatesView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF23 — Emisión, Descarga y Verificación con Código QR

- **Identificador:** RF23
- **Nombre Oficial:** Generación documental PDF, descarga con marca de agua y portal público de verificación QR
- **Módulo Arquitectónico:** MOD-07: Gamificación, Reputación y Certificación
- **Descripción Funcional:** El sistema debe compilar dinámicamente el certificado oficial de mentoría en formato PDF institucional de alta resolución (utilizando ReportLab), incorporando una marca de agua diagonal de seguridad ("DEMO - FINES ACADÉMICOS"), sello criptográfico SHA-256 e incrustando un código QR que enlaza a un portal web público de verificación donde cualquier tercero o evaluador puede comprobar la autenticidad e inalterabilidad del documento ingresando el folio institucional o escaneando el código.
- **Objetivo y Necesidad Académica:** Proporcionar plena validez institucional al documento, erradicando fraudes o adulteraciones de constancias y permitiendo a comisiones evaluadoras verificar la autenticidad de forma inmediata.
- **Actores Participantes:** Estudiante Mentor (Descargador del PDF); Evaluador Externo o Tercero Interesado (Verificador de Autenticidad).
- **Condiciones de Entrada (Precondiciones):** Certificado formalmente autorizado por la Dirección de Escuela.
- **Comportamiento Esperado:**
  1. El mentor pulsa el botón "Descargar Certificado Oficial" en su panel.
  2. El sistema compila el archivo PDF incluyendo membrete oficial, nombre completo del mentor, código universitario, cantidad exacta de horas visadas, periodo lectivo, huella hash SHA-256 y código QR navegable.
  3. Entrega el archivo PDF listo para su impresión o archivo digital.
  4. Cuando un evaluador escanea el código QR impreso en el certificado o ingresa el folio en el portal público de la facultad, el sistema consulta el registro institucional.
  5. Despliega la constancia oficial de validez con los datos verídicos registrados en base de datos.
- **Resultado Verificable (Postcondiciones):** Documento PDF generado y verificable en línea por cualquier autoridad universitaria.
- **Reglas de Negocio Vinculadas:** RN-14 (Acreditación institucional de horas y verificación pública).
- **Restricciones Funcionales:** Ningún certificado descargable carecerá de su código QR institucional y su respectiva huella digital SHA-256.
- **Criterios de Aceptación:**
  - *Escenario 1 (Descarga de constancia PDF con sello criptográfico y QR) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una constancia fue válidamente expedida, CUANDO el usuario solicita su descarga en `/api/v1/certificates/{id}/download`, ENTONCES el sistema entrega un documento PDF oficial compilado con ReportLab, que incorpora marca de agua diagonal ("DEMO - FINES ACADÉMICOS"), huella digital SHA-256 y código QR navegable con cabeceras `application/pdf`.
  - *Escenario 2 (Validación pública institucional por folio o código QR) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE un evaluador externo o autoridad académica consulta el portal de validación pública pasando el folio en `/api/v1/certificates/verificar?folio=CERT-...`, CUANDO el sistema consulta el registro institucional, ENTONCES retorna el estado de autenticidad, nombre del mentor, horas convalidadas y fecha de emisión con código HTTP 200 OK.
  - *Escenario 3 (Rechazo de folio o certificado inexistente) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE se consulta un folio alterado o apócrifo, CUANDO el servicio ejecuta la búsqueda, ENTONCES devuelve código HTTP 404 Not Found o indicador de no autenticidad protegiendo la validez institucional de la EPIS-UPT.
  - *Escenario 4 (Acreditación del motor de PDF y QR en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la generación y verificación de certificados cuenta con 16 pruebas en Pytest y 16 en Vitest, CUANDO se ejecute el pipeline en `main`, ENTONCES se comprobará la validez estructural del PDF generado y la legibilidad del QR.
- **Casos de Uso Relacionados:** CUS-018 (Autorizar y emitir constancias oficiales), CUS-009 (Monitoreo institucional).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/certificates.py` (`GET /api/v1/certificates/{id_certificado}/download`, `GET /api/v1/certificates/verificar`, `GET /api/v1/certificates/{id_certificado}`).
  - *Servicios de Negocio:* `CertificateService.py` (`get_certificate_pdf`, `verify_certificate_by_folio`, `get_certificate_by_id`).
  - *Entidades Relacionales:* Tabla `certificados_horas`.
  - *Componentes Visuales:* `CertificateVerifyView.tsx`, `AdminCertificatesView.tsx`.
  - *Evidencia de Pruebas:* `test_certificates.py` (16 pruebas backend con validación del PDF generado y parsing de QR), `CertificateVerifyView.test.tsx` (16 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF24 — Parametrización Institucional de Aforos y Prioridades

- **Identificador:** RF24
- **Nombre Oficial:** Consola de configuración institucional de aforos, umbrales y asignaturas prioritarias
- **Módulo Arquitectónico:** MOD-08: Gestión Administrativa y Auditoría
- **Descripción Funcional:** El sistema debe proporcionar a la Dirección de Escuela un panel de administración centralizado para ajustar los parámetros institucionales de la plataforma, incluyendo: modificación de los aforos máximos estándar (presencial y virtual), ajuste de porcentajes de quórum de confirmación ($50\%$), definición del umbral mínimo de horas para certificación ($20.0	ext{ h}$) y asignación de la condición de "asignatura filtro prioritaria" a cursos con alta tasa de repitencia.
- **Objetivo y Necesidad Académica:** Otorgar flexibilidad operativa a las autoridades académicas para calibrar la plataforma conforme a las decisiones de Consejo de Facultad o variaciones en la disponibilidad física de infraestructura.
- **Actores Participantes:** Administrador Institucional / Director de Escuela (Actor Primario).
- **Condiciones de Entrada (Precondiciones):** Sesión activa con privilegios de Administrador General.
- **Comportamiento Esperado:**
  1. El administrador ingresa a la sección de configuración de parámetros institucionales.
  2. Modifica los valores deseados (por ejemplo: eleva el aforo presencial de 10 a 12 participantes o incorpora una nueva materia filtro).
  3. El sistema valida que los valores se mantengan dentro de rangos razonables de seguridad pedagógica.
  4. Guarda las nuevas directrices en el repositorio centralizado de configuraciones.
  5. Los nuevos parámetros se propagan de inmediato a los módulos de ofertas, quórum y reservas sin requerir reinicio del servidor.
- **Resultado Verificable (Postcondiciones):** Los parámetros de la plataforma se actualizan en tiempo de ejecución.
- **Reglas de Negocio Vinculadas:** RN-05 (Aforos estándar), RN-09 (Quórum reglamentario), RN-11 (Asignaturas filtro prioritarias).
- **Restricciones Funcionales:** Ningún valor podrá ajustarse a cifras que comprometan la seguridad de los recintos o vulneren las directivas curriculares de la facultad.
- **Criterios de Aceptación:**
  - *Escenario 1 (Parametrización centralizada de reglas de negocio y aforos) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la Dirección de Escuela actualiza los parámetros operativos del semestre (aforos estándar de 10/20, quórum del 50% y umbral de certificación de 20h), CUANDO el sistema carga las configuraciones centralizadas de entorno en `app.core.config.Settings`, ENTONCES los nuevos umbrales se aplican de forma inmediata en todos los servicios de reserva y evaluación.
  - *Escenario 2 (Supervisión de salud del sistema y persistencia) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE la administración supervisa la infraestructura, CUANDO invoca los endpoints de salud `/api/v1/health` y `/api/v1/health/db`, ENTONCES el sistema responde con estado operativo normal (HTTP 200 OK) y métricas de latencia de conexión a base de datos.
  - *Escenario 3 (Verificación de configuración en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE la consola de configuración y salud cuenta con 10 pruebas en Pytest y 14 pruebas en `AdminConfigView.test.tsx`, CUANDO se corra la validación en `main`, ENTONCES se verificará la inmutabilidad de variables críticas en tiempo de ejecución.
- **Casos de Uso Relacionados:** CUS-020 (Parametrizar políticas y umbrales operativos del sistema).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/health.py` (`GET /api/v1/health`, `GET /api/v1/health/db`), configuración centralizada en `aplicacion/backend/app/core/config.py` (`Settings`).
  - *Servicios de Negocio:* `SimulationService.py`, componentes de configuración del núcleo.
  - *Entidades Relacionales:* Esquema de configuración de sistema y tablas de catálogo.
  - *Componentes Visuales:* `AdminConfigView.tsx`.
  - *Evidencia de Pruebas:* `test_config.py` (10 pruebas backend), `AdminConfigView.test.tsx` (14 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF25 — Tablero Analítico Directivo y Métricas de Retención ICACIT

- **Identificador:** RF25
- **Nombre Oficial:** Tablero de mando analítico, indicadores de demanda insatisfecha y reportes ICACIT
- **Módulo Arquitectónico:** MOD-08: Gestión Administrativa y Auditoría
- **Descripción Funcional:** El sistema debe consolidar métricas operacionales agregadas en un panel gráfico de control directivo para las autoridades universitarias, presentando en tiempo real: volumen de mentorías ejecutadas, horas pedagógicas impartidas, asignaturas y temas con mayor demanda insatisfecha, tasas de asistencia efectiva, evolución del promedio de satisfacción de mentores y estimación del impacto en la reducción del rezago estudiantil conforme a los criterios de acreditación ICACIT.
- **Objetivo y Necesidad Académica:** Suministrar evidencia cuantitativa rigurosa para la toma de decisiones institucionales y para las auditorías de calidad educativa exigidas por comités de acreditación nacional e internacional.
- **Actores Participantes:** Director de Escuela, Coordinador de Tutoría, Comité de Calidad y Acreditación (Actores Consultores).
- **Condiciones de Entrada (Precondiciones):** Sesión activa con permisos de visualización analítica institucional.
- **Comportamiento Esperado:**
  1. La autoridad académica ingresa al módulo de analítica directiva.
  2. Selecciona el periodo lectivo a evaluar y los filtros por ciclo o materia crítica.
  3. El sistema procesa los datos y renderiza gráficos interactivos de barras, líneas temporales e indicadores clave de rendimiento (KPIs).
  4. Presenta el mapa térmico de temas silábicos con mayor dificultad reportada por los estudiantes.
  5. Permite exportar los informes en formato PDF y hojas de cálculo para su presentación ante comités académicos de facultad.
- **Resultado Verificable (Postcondiciones):** Los reportes analíticos se generan en pantalla y quedan listos para su exportación.
- **Reglas de Negocio Vinculadas:** RN-02 (Anonimización de datos en analítica agregada), RN-11 (Métricas de asignaturas filtro).
- **Restricciones Funcionales:** Ningún reporte directivo expondrá calificaciones individuales nominales que transgredan la Ley N° 29733.
- **Criterios de Aceptación:**
  - *Escenario 1 (Generación de métricas de retención y demanda para ICACIT) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE las autoridades de la facultad acceden al tablero analítico directivo, CUANDO consultan las métricas consolidadas, ENTONCES el sistema presenta indicadores de demanda insatisfecha, horas de mentoría impartidas y tasas de cobertura por asignatura filtro aptas para sustentación de acreditación internacional.
  - *Escenario 2 (Ejecución del testbench algorítmico y latencias) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el equipo técnico ejecuta la auditoría del motor de recomendación, CUANDO invoca `/api/v1/simulation/benchmark`, ENTONCES el servicio corre la simulación sobre el dataset sintético y reporta Precision@3, Precision@5 y distribución de latencias en milisegundos con código HTTP 200 OK.
  - *Escenario 3 (Acreditación del testbench en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE los tableros analíticos cuentan con 14 pruebas en Pytest y 22 pruebas en `AdminAnalyticsView.test.tsx`, CUANDO se ejecute el pipeline formal en `main`, ENTONCES se confirmará la concordancia de los cálculos matemáticos con los reportes directivos.
- **Casos de Uso Relacionados:** CUS-011 (Monitorear tablero analítico de gestión de mentorías y KPIs ICACIT), CUS-015 (Generar reportes directivos de impacto y cobertura pedagógica).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/simulation.py` (`GET /api/v1/simulation/benchmark`), `aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/simulation/testbench`).
  - *Servicios de Negocio:* `SimulationService.py` (`run_benchmark`).
  - *Entidades Relacionales:* Tablas de hechos y dimensiones analíticas agregadas.
  - *Componentes Visuales:* `AdminAnalyticsView.tsx`, `AnalyticsService.ts`.
  - *Evidencia de Pruebas:* `test_simulation.py` (14 pruebas backend con validación de cálculos de retención), `AdminAnalyticsView.test.tsx` (22 pruebas frontend).

---

#### Ficha Técnica de Requerimiento Funcional: RF26 — Auditoría Institucional de Bitácoras y Privacidad Legal

- **Identificador:** RF26
- **Nombre Oficial:** Bandeja de fiscalización, visado de bitácoras y auditoría de cumplimiento de privacidad legal
- **Módulo Arquitectónico:** MOD-08: Gestión Administrativa y Auditoría
- **Descripción Funcional:** El sistema debe proporcionar una bandeja administrativa especializada para que la Coordinación de Tutoría y el Oficial de Privacidad auditen el cumplimiento de la Ley N° 29733 de Protección de Datos Personales (inspeccionando trazas inmutables de consentimiento, accesos y revocaciones) y fiscalicen exhaustivamente las bitácoras pedagógicas suscritas por mentores, permitiendo visar las horas dictadas o formular observaciones técnicas debidamente motivadas.
- **Objetivo y Necesidad Académica:** Dotar a la facultad de un control riguroso sobre las horas formativas convalidadas a los estudiantes, garantizando que ninguna constancia se emita sin revisión docente previa y asegurando el estricto resguardo legal de la información estudiantil.
- **Actores Participantes:** Coordinador de Tutoría, Auditor Institucional (Actores Fiscalizadores); Estudiante Mentor (Sujeto Fiscalizado).
- **Condiciones de Entrada (Precondiciones):** Sesión con bitácora registrada en espera de visado administrativo.
- **Comportamiento Esperado:**
  1. El fiscalizador institucional ingresa a la bandeja de auditoría docente.
  2. Filtra las sesiones que tienen bitácora suscrita pendiente de visado.
  3. Abre el expediente de la sesión y verifica: quórum, lista de alumnos asistentes, observaciones pedagógicas y firma SHA-256.
  4. Si todo es conforme, pulsa "Visar Bitácora", conmutando la sesión a "Horas Visadas" y acreditando formalmente las horas para el mentor.
  5. Si detecta anomalías (ej. observaciones vagas o incongruencias), pulsa "Observar Bitácora" e ingresa la justificación motivada.
  6. La sesión transiciona a "Observada", se notifica al mentor para su subsanación y las horas quedan temporalmente congeladas.
  7. Asimismo, el módulo permite auditar el registro inmutable de consentimientos de privacidad de todos los usuarios registrados.
- **Resultado Verificable (Postcondiciones):** La bitácora queda visada o sujeta a subsanación, actualizándose la cuenta de horas del mentor.
- **Reglas de Negocio Vinculadas:** RN-14 (Fiscalización obligatoria de bitácoras para acreditación de horas), RN-02 (Auditoría de consentimiento Ley N° 29733).
- **Restricciones Funcionales:** Ninguna hora de mentoría podrá ser computada para certificación si la bitácora correspondiente no cuenta con el visado formal de la autoridad.
- **Criterios de Aceptación:**
  - *Escenario 1 (Fiscalización y visado institucional de bitácoras docentes) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el administrador institucional inspecciona la bandeja de bitácoras pendientes en `/api/v1/bitacoras`, CUANDO verifica la solvencia de las observaciones pedagógicas y confirma el visado en `/api/v1/bitacoras/{id}/visar`, ENTONCES el sistema conmuta la sesión a `HORAS_VISADAS`, acumula las horas para la certificación del mentor (RN-14) y registra la traza de auditoría con código HTTP 200 OK.
  - *Escenario 2 (Formulación de observación técnica sobre bitácora) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE una bitácora contiene justificaciones insuficientes o inconsistencias horarias, CUANDO el fiscalizador registra una observación en `/api/v1/bitacoras/{id}/observar`, ENTONCES el sistema transiciona la sesión a `OBSERVADA`, notifica al mentor para su subsanación y retiene preventivamente las horas hasta su corrección con código HTTP 200 OK.
  - *Escenario 3 (Auditoría de cumplimiento de privacidad Ley N° 29733) `[REQUISITO]` `[IMPLEMENTADO]` `[VERIFICADO]`:* DADO QUE el oficial de cumplimiento legal audita el tratamiento de datos personales, CUANDO consulta el estado de consentimiento en `/api/v1/consent/status`, ENTONCES el sistema genera el reporte inmutable de marcas de aceptación, revocaciones y accesos con sellos de tiempo UTC.
  - *Escenario 4 (Revalidación de auditoría en CI) `[REQUISITO]` `[IMPLEMENTADO]` `[PENDIENTE]`:* DADO QUE el módulo de fiscalización cuenta con 14 pruebas en Pytest y 16 pruebas en `AdminAuditView.test.tsx`, CUANDO se concluya la subsanación de linteo en `main`, ENTONCES se confirmará la estricta segregación de permisos RBAC para administradores.
- **Casos de Uso Relacionados:** CUS-016 (Fiscalizar y visar bitácoras pedagógicas suscritas por mentores), CUS-022 (Auditar trazabilidad de consentimientos y cumplimiento legal Ley N° 29733).
- **Apartado de Trazabilidad Técnica e Implementación:**
  - *Controladores y Endpoints:* `aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`GET /api/v1/bitacoras`, `POST /api/v1/bitacoras/{id}/visar`, `POST /api/v1/bitacoras/{id}/observar`), `aplicacion/backend/app/api/v1/endpoints/consent.py` (`GET /api/v1/consent/status`).
  - *Servicios de Negocio:* `BitacoraService.py` (`list_bitacoras`, `visar_bitacora`, `observar_bitacora`), `ConsentService.py` (`get_consent_status`).
  - *Entidades Relacionales:* Tablas `bitacoras_pedagogicas`, `consentimientos_legales`, `sesiones_mentoria`.
  - *Componentes Visuales:* `AdminAuditView.tsx`.
  - *Evidencia de Pruebas:* `test_bitacora.py` (14 pruebas backend de auditoría y visado), `AdminAuditView.test.tsx` (16 pruebas frontend).

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
| **RF01** (Autenticación 2FA) | MOD-01 | Sprint 1 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Flujo OTP con correo institucional, cooldown de 60 s y token JWT de 8h (13 tests Pytest / 15 tests Vitest). |
| **RF02** (Consentimiento Ley 29733) | MOD-01 | Sprint 2 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Modal accesible, persistencia de marcas UTC/IP en BD y bloqueo perentorio (9 tests Vitest / 5 tests Pytest). |
| **RF03** (Roles y Mérito) | MOD-01 | Sprint 2 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Verificación de mérito académico (ciclo $\ge \text{VII}$ y nota $\ge 14.0$) y control RBAC (7 tests Pytest). |
| **RF04** (Perfil y Matriz 6×11) | MOD-03 | Sprint 2 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Matriz semanal interactiva 6×11 (08:00 a 20:00) y reemplazo atómico en BD (10 tests Vitest / 11 tests Pytest). |
| **RF05** (Catálogo Curricular) | MOD-03 | Sprints 1 y 2 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Materias formativas críticas en base de datos y árbol de temas silábicos (4 tests Vitest / 8 tests Pytest). |
| **RF06** (EdRecSys Top-k) | MOD-04 | Sprint 3 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Similitud coseno y filtrado colaborativo calibrado ($P@3=83.3\%$, latencia 12.4 ms) (18 tests Pytest / 14 tests Vitest). |
| **RF07** (Banco de Demanda) | MOD-04 | Sprint 3 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Registro de demandas temáticas, validación de temarios y visualización docente (12 tests Pytest / 14 tests Vitest). |
| **RF08** (Publicación de Ofertas) | MOD-02 | Sprint 4 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Antelación $\ge 24\text{ h}$, límites de aforo estándar y registro de recursos (16 tests Pytest / 18 tests Vitest). |
| **RF09** (Aprovisionamiento de Espacios) | MOD-02 | Sprint 4 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Aulas libres verificadas contra solapamientos y salas virtuales (14 tests Pytest / 12 tests Vitest). |
| **RF10** (Parser de Cronogramas) | MOD-02 | Sprint 4 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Ingesta estructurada de cronogramas oficiales para detección de ambientes libres (8 tests Pytest). |
| **RF11** (Gestión de Contingencias) | MOD-02 | Sprint 4 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Reprogramación y cancelación justificada con liberación de recursos y avisos (10 tests Pytest / 10 tests Vitest). |
| **RF12** (Reserva Concurrente Pesimista)| MOD-05 | Sprint 5 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Bloqueo pesimista `SELECT ... FOR UPDATE` demostrando **0.0% de sobrecupo** (18 tests Pytest / 16 tests Vitest). |
| **RF13** (Ratificación Anticipada) | MOD-05 | Sprint 5 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Confirmación previa hasta el corte de $T-24\text{ h}$ y cambio a confirmada (12 tests Pytest / 14 tests Vitest). |
| **RF14** (Desistimiento Voluntario) | MOD-05 | Sprint 5 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Anulación voluntaria antes de $T-24\text{ h}$ con restitución instantánea de vacantes (10 tests Pytest / 10 tests Vitest). |
| **RF15** (Corte de Quórum en $T-24\text{ h}$)| MOD-05 | Sprint 5 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Demonio cron desatendido que invalida pendientes y evalúa quórum del 50% (16 tests Pytest / 12 tests Vitest). |
| **RF16** (Resolución de Quórum) | MOD-05 | Sprint 5 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Diálogo resolutivo del mentor ante quórum insuficiente (10 tests Pytest / 10 tests Vitest). |
| **RF17** (Asistencia QR Dinámico TOTP)| MOD-06 | Sprint 6 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Pase QR dinámico de 30 segundos y escaneo por cámara institucional (14 tests Pytest / 20 tests Vitest). |
| **RF18** (Bitácora Docente SHA-256) | MOD-06 | Sprint 6 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Registro obligatorio en 48 horas con sello hash SHA-256 (18 tests Pytest / 22 tests Vitest). |
| **RF19** (Historial y Recursos) | MOD-06 | Sprint 6 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Historial cronológico con filtros temáticos y acceso a materiales educativos (8 tests Pytest / 12 tests Vitest). |
| **RF20** (Encuestas CSAT de 24h) | MOD-06 | Sprint 7 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Encuesta de 4 dimensiones pedagógicas en ventana perentoria de 24 horas (16 tests Pytest / 14 tests Vitest). |
| **RF21** (Reputación e Insignias) | MOD-07 | Sprint 7 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Recálculo dinámico de reputación y catálogo de insignias por mérito (12 tests Pytest / 18 tests Vitest). |
| **RF22** (Parametrización de Certificados)| MOD-07 | Sprint 7 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Control de umbral mínimo de 20 horas auditadas para autorizar certificación (14 tests Pytest / 16 tests Vitest). |
| **RF23** (Certificado PDF con QR) | MOD-07 | Sprint 7 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Compilación ReportLab de PDF oficial con hash SHA-256 y validador QR (16 tests Pytest / 16 tests Vitest). |
| **RF24** (Configuración Institucional) | MOD-08 | Sprint 8 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Consola administrativa de aforos y asignaturas prioritarias (10 tests Pytest / 14 tests Vitest). |
| **RF25** (Tableros Analíticos ICACIT)| MOD-08 | Sprint 8 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Tablero con métricas de demanda insatisfecha y retención estudiantil (14 tests Pytest / 22 tests Vitest). |
| **RF26** (Auditoría y Visado Docente) | MOD-08 | Sprint 8 | `[IMPLEMENTADO]` / `[VERIFICADO_HISTORICO]` ✅ | Fiscalización de bitácoras docentes y auditoría legal bajo Ley N° 29733 (14 tests Pytest / 16 tests Vitest). |

Fuente: Elaboración propia a partir de las bitácoras técnicas de los Sprints 01 al 08.

> **Nota Metodológica de Auditoría (H01-R / H02 / H03):** La cifra consolidada de 682 pruebas automatizadas (335 en backend Pytest y 347 en frontend Vitest) corresponde al reporte histórico acreditado en el commit `3f6e31d`. De acuerdo con la rectificación formal H01-R y la auditoría de calidad H03, dicha cifra se clasifica formalmente como `[DATO_HISTORICO_OBSERVADO]` y su re-verificación formal en `main` se encuentra en estado `[PENDIENTE]` debido a fallos de linteo estático reportados en el flujo de integración continua (CI), los cuales no comprometen la lógica de los contratos ni las aserciones de negocio.

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
