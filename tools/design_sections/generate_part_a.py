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
**ESCUELA DE INGENIERÍA DE SISTEMAS**

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

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
|:---:|:---:|:---:|:---:|:---:|:---|
| **1.0** | JCM / RAM | RVA | RVA | 11/09/2026 | Versión 1.0 preliminar de levantamiento y especificación inicial. |
| **2.0** | JCM / RAM | RVA | Dirección EPIS | 26/09/2026 | Consolidación y congelamiento de la línea base analítica oficial (MOD-01 al MOD-08, RF01 al RF26, RN-01 al RN-14, RNF01 al RNF10, CUS01 al CUS24). Reorganización modular de narrativas por dependencia operativa, supresión de reglas ocultas, alineamiento estricto de estados canónicos con el modelo lógico y hardening continuo. |
| **2.1** | JCM / RAM | Dr. Ricardo Valcarcel | Dirección EPIS | 19/10/2026 | Refinamiento y trazabilidad en Fase de Diseño (SRS v2.1): alineamiento técnico con la arquitectura desacoplada y cierre de requerimientos del Sprint 1 (RF01, RF05, RNF01, RNF02, RNF09, CUS-001, CUS-021, RN-01) respaldados empíricamente con 96 pruebas automatizadas en CI. |
| **2.2** | JCM / RAM | Dr. Ricardo Valcarcel | Dirección EPIS | 23/10/2026 | Consolidación de Fase de Diseño y Construcción del Sprint 2 (SRS v2.2): formalización técnica y verificación empírica de Consentimiento digital bajo Ley N° 29733 (RF02, RN-02, CUS-001), administración de roles y mérito académico (RF03, RN-03, CUS-010), perfiles formativos y matriz de disponibilidad horaria semanal 6×11 (RF04, RNF04, RNF08, CUS-005), búsqueda avanzada en catálogo curricular con temarios silábicos (RF05, CUS-021) y aislamiento multiusuario con Row Level Security (RNF02), respaldados por 150 pruebas automatizadas sin fallos (>90% de cobertura en frontend y backend). |
| **3.0** | JCM / RAM | Dr. Ricardo Valcarcel | Dirección EPIS | 14/11/2026 | Consolidación Integral de la Fase de Diseño y Cierre de Construcción (SRS v3.0): culminación de los 8 Sprints de desarrollo (MOD-01 al MOD-08, CUS-001 al CUS-024, RF01 al RF26, RN-01 al RN-14, RNF01 al RNF10). Formalización de interfaces externas (WCAG 2.1 AA / Tailwind), motor EdRecSys calibrado (Precision@3=83.3%, Precision@5=80.0%, latencia 12.4 ms), orquestación transaccional con cerrojos pesimistas (SELECT FOR UPDATE) a T-24h, bitácoras firmadas con SHA-256, certificados PDF con QR institucional y trazabilidad integral acreditada por 627 pruebas automatizadas aprobadas (280 backend Pytest, 347 frontend Vitest) con 0 fallos y cobertura >85%. |

# Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT

**Documento de Especificación de Requerimientos de Software**  
**Versión 3.0 — Fase de Diseño Técnico y Cierre de Construcción (Sprints 1 al 8)**

---

## ÍNDICE GENERAL

1. Introducción  
   1.1. Propósito  
   1.2. Alcance del Sistema  
   1.3. Personal Involucrado  
   1.4. Definiciones, Acrónimos y Abreviaturas  
   1.5. Referencias Normativas y Técnicas  
   1.6. Resumen del Documento  
2. Generalidades de la Empresa  
   2.1. Nombre de la Empresa  
   2.2. Visión  
   2.3. Misión  
   2.4. Organigrama y Responsabilidades Técnicas  
3. Visionamiento de la Empresa  
   3.1. Descripción del Problema  
   3.2. Objetivos de Negocios  
   3.3. Objetivos de Diseño  
   3.4. Alcance y Exclusiones del Proyecto  
   3.5. Viabilidad del Sistema  
   3.6. Información obtenida del Levantamiento de Información  
4. Análisis de Procesos  
   4.1. Diagrama del Proceso Actual (As-Is)  
   4.2. Diagrama del Proceso Propuesto (To-Be)  
5. Especificación de Requerimientos de Software  
   5.1. Identificación de Módulos y Capacidades Funcionales  
   5.2. Requerimientos No Funcionales (ISO/IEC 25010)  
   5.3. Matriz Consolidada de Requerimientos Funcionales (RF01 al RF26)  
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

El propósito del presente documento es formalizar la **Especificación de Requerimientos de Software (SRS)** en su **Versión 3.0 (Fase de Diseño Técnico y Cierre de Construcción)** para el desarrollo e implementación del *“Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT”*. Este documento establece la línea base arquitectónica, el modelo lógico, las reglas de gobernanza institucional, los contratos de interfaz RESTful y las matrices de trazabilidad bidireccional que articulan las capacidades construidas a lo largo de los ocho sprints del ciclo de vida del software, sirviendo como instrumento formal de auditoría y acreditación académica ante la Dirección de Escuela y el Comité Docente de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

## 1.2. Alcance del Sistema

El software abarca una plataforma web adaptativa y distribuida de tipo *Peer-to-Peer* (P2P) orientada a transformar la tutoría tradicional en un ecosistema de colaboración horizontal entre estudiantes de ciclos superiores (VII al X) y estudiantes de ciclos iniciales (I al IV). El sistema automatiza el emparejamiento inteligente de necesidades académicas mediante un motor de recomendación híbrido (*EdRecSys*), gestiona el aprovisionamiento de infraestructura física y virtual, gobierna el ciclo de quórum con control de concurrencia y cerrojos transaccionales a $T-24\text{ h}$, registra bitácoras pedagógicas auditables con hash criptográfico SHA-256 y formaliza la emisión de certificados digitales institucionales descargables en formato PDF con código correlativo único y validación en línea mediante código QR.

## 1.3. Personal Involucrado

| Nombre | Rol Institucional / Académico | Responsabilidad en el Proyecto |
|---|---|---|
| **Dr. Ricardo Eduardo Valcárcel Alvarado** | Docente Titular de Construcción de Software I | Dirección académica, supervisión metodológica, revisión de entregables y aprobación de fases de ciclo de vida. |
| **Ing. Haydee Raquel Sisa Yataco** | Directora (e) de la EPIS-UPT | Validación de políticas de convalidación extracurricular, homologación de horas académicas y patrocinio institucional. |
| **Ing. Liliana Mercedes Vega Bernal** | Coordinadora de Tutoría de la EPIS-UPT | Especificación de criterios de atención a cursos filtro, gobernanza de quórum y fiscalización de bitácoras docentes. |
| **Joan Cristian Medina Quispe** | Desarrollador / Consultor C-SharkTeam | Ingeniería de Frontend (React 18 SPA, Tailwind CSS), accesibilidad WCAG 2.1 AA, componentes UI/UX y pruebas unitarias/integración (Vitest). |
| **Renzo Antonio Antayhua Mamani** | Desarrollador / Consultor C-SharkTeam | Ingeniería de Backend (Python FastAPI), motor de recomendación híbrido (*EdRecSys*), persistencia PostgreSQL/Supabase, RLS, cerrojos transaccionales y pruebas de backend (Pytest). |

## 1.4. Definiciones, Acrónimos y Abreviaturas

- **2FA (Two-Factor Authentication):** Mecanismo de autenticación multifactor basado en el envío de un código OTP temporal de 6 dígitos al correo electrónico institucional del usuario.
- **ACID (Atomicity, Consistency, Isolation, Durability):** Propiedades transaccionales garantizadas por el motor PostgreSQL mediante bloques transaccionales y cerrojos pesimistas (`SELECT ... FOR UPDATE`).
- **ECB (Entity-Control-Boundary):** Patrón de análisis y diseño arquitectónico propuesto por Ivar Jacobson que segrega interfaces de usuario (Boundary), coordinadores de lógica de negocio (Control) y estructuras persistentes de datos (Entity).
- **EdRecSys (Educational Recommendation System):** Motor algorítmico híbrido desarrollado en Python que combina similitud coseno sobre espacios vectoriales de contenidos silábicos con filtrado colaborativo ponderado por reputación y balanceo de carga.
- **EPIS-UPT:** Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.
- **FSM (Finite State Machine):** Máquina de estados finitos que modela las transiciones deterministas del ciclo de vida de entidades críticas (`SesionMentoria`, `ReservaCupo`, `BitacoraPedagogica`).
- **JWT (JSON Web Token):** Estándar abierto (RFC 7519) utilizado para la transmisión segura de identidades y privilegios mediante tokens criptográficos firmados con algoritmo HMAC-SHA256 y expiración de 8 horas.
- **NDCG (Normalized Discounted Cumulative Gain):** Métrica de evaluación de sistemas de recomendación que mide la ganancia acumulada y el orden posicional de relevancia del ranking Top-k generado.
- **OTP (One-Time Password):** Código numérico de un solo uso de 6 dígitos generado criptográficamente con tiempo de vida máximo e improrrogable de 5 minutos (300 segundos).
- **Precision@k:** Proporción de elementos relevantes recomendados dentro de los primeros $k$ resultados presentados al estudiante.
- **RLS (Row Level Security):** Mecanismo de seguridad granular a nivel de fila implementado en PostgreSQL para garantizar que cada usuario acceda estrictamente a sus propios registros académicos.
- **SPA (Single Page Application):** Arquitectura de interfaz web construida sobre React 18 que actualiza dinámicamente el contenido del navegador sin recargas completas de página.
- **SUS (System Usability Scale):** Cuestionario psicométrico estandarizado de diez ítems utilizado para cuantificar la usabilidad, ergonomía y satisfacción percibida por los usuarios.
- **TOTP (Time-based One-Time Password):** Algoritmo de generación de códigos efímeros vinculados al tiempo, utilizado para la emisión de pases QR dinámicos de marcación de asistencia.
- **UWE (UML-Based Web Engineering):** Metodología de ingeniería de software orientada a la especificación, diseño sistemático y construcción de aplicaciones web complejas y adaptativas.

## 1.5. Referencias Normativas y Técnicas

1. **Ley N° 29733:** *Ley de Protección de Datos Personales del Perú* y su Reglamento aprobado por D.S. N° 003-2013-JUS.
2. **Ley N° 30220:** *Ley Universitaria del Perú* (Artículo 40: Servicio de Tutoría y Consejería Integral Permanente).
3. **Estándar IEEE Std 830-1998:** *IEEE Recommended Practice for Software Requirements Specifications*.
4. **Estándar ISO/IEC/IEEE 29148:2018:** *Systems and software engineering — Life cycle processes — Requirements engineering*.
5. **Estándar ISO/IEC 25010:2011:** *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models*.
6. **W3C WCAG 2.1:** *Web Content Accessibility Guidelines* (Nivel de conformidad AA).
7. **Reglamento General de Grados y Títulos:** Universidad Privada de Tacna (Criterios de convalidación de horas y actividades extracurriculares).

## 1.6. Resumen del Documento

El informe se estructura formalmente en ocho secciones macro:
- **Sección 1 (Introducción):** Define el marco formal, alcance, acrónimos y gobernanza del proyecto.
- **Sección 2 (Generalidades):** Describe la identidad del equipo consultor C-SharkTeam y el organigrama técnico.
- **Sección 3 (Visionamiento):** Expone el análisis del problema, objetivos de negocio/diseño, alcance técnico y viabilidad multidimensional (financiera, técnica, legal y operativa).
- **Sección 4 (Análisis de Procesos):** Modela mediante diagramas de actividades el estado actual informal (*As-Is*) frente al proceso optimizado de mentorías P2P (*To-Be*).
- **Sección 5 (Especificación de Requerimientos):** Detalla los ocho módulos funcionales (Cuadro 5.1), los diez atributos de calidad ISO/IEC 25010 (Cuadro 5.2), la matriz de veintiséis requerimientos funcionales (Cuadro 5.3), las catorce reglas de negocio (Cuadro 5.4), la matriz de trazabilidad y verificación de los 8 Sprints con 627 tests (Cuadros 5.5 y 5.6), y los requisitos de interfaz externa (Sección 5.6).
- **Sección 6 (Fase de Desarrollo):** Presenta el modelo de control de acceso RBAC (6.1), el modelo conceptual y paquetes arquitecturales (6.2.1), los diagramas de casos de uso modulares (6.2.2), las narrativas de diseño canónicas para los 24 CUS (6.2.3), los diagramas de análisis de objetos ECB (6.3.1), diagramas de actividades con flujo de objetos (6.3.2), diagramas de secuencia Visual Paradigm (6.3.3), diagramas de clases lógicas (6.3.4), máquinas de estados finitos (6.3.5) y el modelo físico relacional de base de datos con diccionario DDL (6.3.6).
- **Secciones 7 y 8 (Conclusiones y Bibliografía):** Sintetizan los resultados empíricos alcanzados y compilan las fuentes normativas y científicas de referencia.

---

# 2. Generalidades de la Empresa

## 2.1. Nombre de la Empresa

**C-SharkTeam**

Equipo Consultor y Desarrollador de Soluciones de Software Educativo y Tecnológico.

## 2.2. Visión

Consolidarse como un equipo líder en desarrollo de software educativo, analítica de datos e inteligencia artificial aplicada en el sur del Perú, reconocido por transformar los modelos tradicionales de tutoría y asesoría académica hacia ecosistemas digitales horizontales (*Peer-to-Peer*), personalizados, eficientes y medibles.

## 2.3. Misión

Diseñar, desarrollar e implementar soluciones de software de alto impacto y base tecnológica, enfocadas en la optimización de procesos de aprendizaje colaborativo, emparejamiento algorítmico inteligente y gobernanza de datos en instituciones de educación superior, facilitando herramientas digitales accesibles, intuitivas y rigurosamente alineadas con los objetivos académicos de la comunidad universitaria.

## 2.4. Organigrama y Responsabilidades Técnicas

La estructura organizativa y funcional de C-SharkTeam se fundamenta en roles colaborativos de ingeniería de software con alta especialización técnica:

### Organigrama del C-SharkTeam

```plantuml
@startuml
top to bottom direction
skinparam rectangle {
  BackgroundColor white
  BorderColor #555555
}

rectangle "C-SharkTeam\nDirección de Proyecto de TI" as DIR

rectangle "Ingeniería de Backend,\nAlgoritmos y Persistencia\nRenzo Antonio Antayhua M.\n\n• Arquitectura RESTful (FastAPI)\n• Motor EdRecSys (Scikit-learn)\n• Persistencia PostgreSQL / RLS\n• Transacciones ACID & Locks Pesimistas\n• Cobertura Pytest (280 tests)" as BACK

rectangle "Ingeniería de Frontend,\nUI/UX y Accesibilidad\nJoan Cristian Medina Q.\n\n• Interfaz Web Responsiva (React SPA)\n• Design System (Tailwind CSS)\n• Accesibilidad WCAG 2.1 AA\n• Gestión de Estado & Clientes HTTP\n• Cobertura Vitest (347 tests)" as FRONT

rectangle "Entorno Institucional / Beneficiarios\n\n• Dirección EPIS-UPT\n• Coordinación de Tutoría Docente\n• Estudiantes Mentores (Ciclos VII-X)\n• Estudiantes Mentoreados (Ciclos I-IV)" as CLIENTE

DIR --> BACK
DIR --> FRONT
BACK --> CLIENTE
FRONT --> CLIENTE
@enduml
```

Fuente: Elaboración propia.

- **Área de Backend, Algoritmos y Persistencia Relacional:** Liderada por **Renzo Antonio Antayhua Mamani**, responsable de la arquitectura de servicios RESTful (Python FastAPI), diseño de contratos JSON con Pydantic v2, desarrollo y calibración matemática del motor de recomendación híbrido *EdRecSys* (similitud coseno y filtrado colaborativo), esquema de seguridad multifactor 2FA (Email OTP), persistencia relacional en PostgreSQL administrado vía Supabase, políticas de seguridad a nivel de fila (*Row Level Security - RLS*), orquestación transaccional con cerrojos pesimistas (`SELECT ... FOR UPDATE`), demonios desatendidos de corte de quórum y suite de pruebas unitarias/integración backend (280 tests Pytest).
- **Área de Frontend, Arquitectura de Componentes y Experiencia de Usuario (UI/UX):** Liderada por **Joan Cristian Medina Quispe**, responsable de la construcción de la aplicación web responsiva de página única (React 18 SPA con TypeScript y Vite), implementación del Design System institucional mediante Tailwind CSS y componentes accesibles bajo directrices WCAG 2.1 AA, adaptadores de cliente HTTP fuertemente tipados (`apiClient`), gestión reactiva del estado global, validación asíncrona de formularios, interacción con pases QR dinámicos, visualización de tableros analíticos y suite de pruebas unitarias/componentes en frontend (347 tests Vitest).

---

# 3. Visionamiento de la Empresa

C-SharkTeam concibe este proyecto no solo como una plataforma de soporte puntual, sino como la base de un ecosistema tecnológico escalable para la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT).

El visionamiento se apoya en los siguientes pilares de evolución:
- **Transición del Soporte Reactivo al Preventivo:** Reemplazar las tutorías asistenciales tardías por un modelo de acompañamiento continuo y personalizado que atienda a tiempo las debilidades conceptuales de los alumnos en asignaturas formativas.
- **Potenciación del Aprendizaje entre Pares (P2P):** Democratizar el acceso a la asesoría académica aprovechando el talento de los alumnos de ciclos superiores, eliminando la barrera de comunicación docente-estudiante y facilitando explicaciones técnicas con un lenguaje cercano.
- **Optimización con Inteligencia Artificial:** Maximizar la tasa de éxito de cada mentoría sugiriendo automáticamente al mentor más idóneo en función de competencias temáticas, disponibilidad horaria y reputación histórica acumulada.
- **Trazabilidad y Reconocimiento Institucional:** Brindar a las autoridades de la EPIS-UPT métricas en tiempo real sobre la demanda académica y permitir la emisión formal de constancias y certificados de convalidación para incentivar la participación continua de los mentores.

## 3.1. Descripción del Problema

En la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna (EPIS-UPT), los estudiantes que cursan los primeros ciclos (I al IV) presentan dificultades de asimilación conceptual y altos índices de reprobación en asignaturas formativas básicas y de ciencias de la computación, tales como Cálculo, Algoritmos y Estructura de Datos y Programación Orientada a Objetos.

Estas materias actúan como "cursos filtro", provocando rezago en el avance de la malla curricular y aumentando el riesgo de deserción académica temprana.

Aunque la escuela dispone de una comunidad de estudiantes destacados en los ciclos superiores (VII al X) con solvencia técnica para guiar a sus compañeros, no existe una plataforma institucional centralizada ni automatizada que gestione de forma eficiente la oferta y la demanda de asesoría académica entre pares (Peer-to-Peer). En la actualidad, este apoyo ocurre a través de canales informales no regulados (grupos de WhatsApp o mensajería privada), lo que conlleva los siguientes problemas identificados:
- **Falta de emparejamiento inteligente (matching):** La búsqueda de ayuda depende de contactos personales o referencias empíricas, sin contrastar las debilidades temáticas específicas del estudiante con las fortalezas curriculares y disponibilidad horaria del mentor.
- **Carencia de trazabilidad y gobernanza institucional:** La Dirección de Escuela y el Comité de Tutoría no disponen de registros sobre qué temas se refuerzan, quiénes participan ni cuál es el impacto pedagógico real, imposibilitando una intervención preventiva y oportuna.
- **Ausencia de esquemas de reconocimiento formal:** Los mentores no cuentan con incentivos estructurados (como gamificación o acumulación auditable de horas para convalidación de créditos extracurriculares), lo que ocasiona abandono o falta de compromiso por sobrecarga académica propia.
- **Vacíos en la privacidad de datos académicos:** No se aplican protocolos de consentimiento digital ni anonimización en el tratamiento de historiales de notas, en incumplimiento de la Ley N° 29733 de Protección de Datos Personales.

## 3.2. Objetivos de Negocios

Los objetivos de negocio expresan el impacto directo que el software genera en el entorno académico e institucional de la EPIS-UPT:
- **Reducir el índice de rezago y reprobación académica:** Disminuir las tasas de desaprobación en los cursos filtro de I a IV ciclo mediante refuerzos conceptuales oportunos antes de las evaluaciones parciales y finales.
- **Modernizar y descongestionar el servicio de tutoría universitaria:** Cumplir de manera activa el Artículo 40 de la Ley Universitaria N° 30220, transfiriendo las dudas conceptuales básicas a una red horizontal de pares y liberando horas de asesoría docente para casos de mayor complejidad académica.
- **Fomentar la permanencia y retención estudiantil:** Mitigar el riesgo de abandono en los primeros semestres de la carrera de Ingeniería de Sistemas, preservando la continuidad de matrícula institucional.
- **Institucionalizar el reconocimiento al talento estudiantil:** Formalizar la labor de los mentores de ciclos superiores mediante la emisión de certificados de horas extracurriculares convalidables y un sistema de reputación académica visible.
- **Proveer analítica de decisiones para la Dirección de Escuela:** Dotar a la coordinación académica de métricas consolidadas sobre la demanda real de contenidos, asignaturas críticas y niveles de participación estudiantil.

## 3.3. Objetivos de Diseño

Los objetivos de diseño establecen las metas técnicas, funcionales y de experiencia de usuario que la arquitectura del sistema garantiza:
- **Precisión y Eficiencia Algorítmica:** Implementar un motor de recomendación híbrido (*EdRecSys*) capaz de procesar similitud coseno sobre vectores de debilidades/competencias silábicas y filtrado colaborativo con una precisión demostrada `Precision@3 = 83.3%`, `Precision@5 = 80.0%`, ranking `NDCG = 0.82` y tiempo medio de respuesta algorítmica de 12.4 ms.
- **Alta Usabilidad y Accesibilidad Universal:** Construir una interfaz web responsiva (React 18 SPA) bajo directrices de accesibilidad WCAG 2.1 AA que garantice navegación intuitiva y supere los 75 puntos en la escala estandarizada System Usability Scale (SUS).
- **Seguridad Robusta y Cumplimiento Normativo:** Incorporar autenticación multifactor (2FA vía Email OTP institucional con expiración de 5 minutos), control de acceso basado en roles (RBAC) con tokens JWT criptográficos (HS256) de 8 horas, políticas de seguridad a nivel de fila (Row Level Security - RLS) en PostgreSQL y un módulo vinculante de consentimiento informado digital bajo la Ley N° 29733.
- **Aprovisionamiento Desacoplado de Espacios:** Proveer gestión estructurada para asignación de espacios físicos (aulas y laboratorios de la EPIS validados mediante horarios libres) y generación de salas virtuales mediante enlaces directos validados y supervisados.
- **Trazabilidad Integral y Concurrencia Confiable:** Garantizar transacciones ACID en PostgreSQL con cerrojos pesimistas (`SELECT ... FOR UPDATE`) para erradicar colisiones en la reserva concurrente de cupos, implementando bitácoras pedagógicas firmadas con SHA-256 y certificados PDF verificables mediante código QR institucional.

## 3.4. Alcance del proyecto

El alcance del proyecto comprende la especificación, diseño, codificación, integración, verificación y despliegue del Sistema Web P2P de mentorías académicas en la EPIS-UPT, 2026.

### Inclusiones del Sistema (Módulos Construidos)

- **Plataforma Web Responsiva (Frontend SPA):** Interfaz web accesible desde cualquier navegador moderno en estaciones de trabajo y dispositivos móviles, diseñada bajo React 18, TypeScript, Vite y Tailwind CSS, cumpliendo directrices de accesibilidad WCAG 2.1 AA.
- **Módulo de Identidad, Acceso y Privacidad:** Autenticación institucional con 2FA mediante código OTP remitido al correo `@upt.pe`, formalización obligatoria de consentimiento informado digital bajo la Ley N° 29733 y control de accesos jerárquicos (RBAC).
- **Motor Híbrido de Recomendación (EdRecSys):** Microservicio analítico que vectoriza las necesidades temáticas del mentoreado frente a las competencias del catálogo mediante similitud coseno, ajustando el ranking Top-k con filtrado colaborativo, reputación y balance de carga.
- **Gestión de Oferta y Demanda de Mentorías:** Publicación de clases por mentores calificados y formulario de registro en el banco de solicitudes por demanda.
- **Aprovisionamiento de Infraestructura y Espacios:**
  - **Modalidad Presencial:** Asignación validada de aulas y laboratorios libres de la EPIS-UPT, con aforo estándar de 10 estudiantes (RN-05).
  - **Modalidad Virtual:** Configuración de enlaces directos a salas de teleconferencia institucionales, con aforo estándar de 20 estudiantes (RN-05).
- **Control de Quórum y Orquestación Transaccional a $T-24\text{ h}$:** Reserva atómica con cerrojos pesimistas, ventana de ratificación anticipada, cálculo desatendido de quórum mínimo (50%) en $T-24\text{ h}$ y flujo de contingencia del mentor ante quórum insuficiente.
- **Trazabilidad Pedagógica, Marcación QR y Bitácoras:** Marcación de asistencia presencial/virtual mediante pases QR dinámicos TOTP, registro obligatorio de bitácoras en 48 horas post-sesión firmadas con hash SHA-256 y encuestas de calidad de 24 horas.
- **Gamificación y Emisión Digital de Certificados:** Reputación ponderada de mentores, catálogo de insignias por mérito docente, fiscalización de horas por la administración y emisión de certificados en PDF descargables con código hash SHA-256 y código QR de verificación institucional.
- **Panel de Control y Analítica Académica:** Tablero institucional de indicadores agregados (demanda insatisfecha, asistencia, cursos críticos y rendimiento).

### Exclusiones del Alcance (Límites de la Versión)

- No se desarrollan aplicaciones móviles nativas compiladas para Android o iOS (la plataforma opera como aplicación web responsiva multiplataforma accesible desde navegadores móviles y de escritorio).
- No se admiten transacciones financieras ni pagos monetarios (el sistema es estrictamente de servicio formativo universitario gratuito).
- No se realiza sincronización directa bidireccional en tiempo real con el sistema central ERP de matrícula universitaria de la UPT.
- No se requiere firma digital avanzada con token físico PKI de entidades certificadoras de pago; la inalterabilidad y autenticidad documental se garantiza internamente mediante folio correlativo institucional, código hash SHA-256 y código QR de verificación pública en el portal institucional.

## 3.5. Viabilidad del Sistema

### 1. Viabilidad Técnica

- **Stack Tecnológico y Madurez:** React 18, TypeScript, Tailwind CSS, Python 3.11+ (FastAPI / Scikit-learn), ReportLab y PostgreSQL administrado mediante Supabase.
- **Capacidad Computacional:** Procesamiento matricial de similitud coseno con tiempo de respuesta empírico de $12.4\text{ ms}$, muy inferior al umbral máximo admisible de $500\text{ ms}$.
- **Concurrencia Transaccional:** Control de concurrencia pesimista en PostgreSQL (`SELECT ... FOR UPDATE`) que garantiza $0.0\%$ de colisiones o sobreasignaciones de cupos.

### 2. Viabilidad Económica

El análisis financiero se calculó para un horizonte de evaluación a 5 años (2026-2030) con una tasa de descuento (COK) del 12.00%:

| Indicador Financiero | Valor Proyectado | Interpretación Técnica / Financiera |
|---|---:|---|
| **Inversión Inicial (CAPEX)** | **S/. 5,475.00** | Cubre 500 horas de desarrollo (Joan Medina y Renzo Antayhua a razón de S/. 9.00/hr), depreciación de equipos (3.5 meses), conectividad, dominio web e imprevistos. |
| **Costo Operativo Anual (OPEX)** | **S/. 1,140.00** | Mantenimiento de infraestructura PaaS (Render/Supabase), renovación de dominio, soporte preventivo y materiales de difusión. |
| **Valor Actual Neto (VAN)** | **+S/. 10,801.64** | Estrictamente positivo (VAN > 0), ratificando que el proyecto genera valor económico y retención institucional por encima de la tasa exigida. |
| **Tasa Interna de Retorno (TIR)** | **68.20%** | Supera ampliamente el COK referencial (12.00%), otorgando un margen de seguridad amplio frente a variaciones de costos. |
| **Relación Beneficio / Costo (B/C)** | **1.97** | Por cada sol invertido en el ciclo del proyecto, se generan S/. 1.97 en beneficios y ahorros valorizados para la facultad y los estudiantes. |
| **Periodo de Recuperación (Payback)** | **1 año y 9.7 meses** | La inversión inicial se recupera plenamente durante el transcurso del segundo año de operación. |

### 3. Viabilidad Operativa

- **Adopción por Mentoreados:** Los alumnos de I a IV ciclo acceden desde cualquier navegador web sin instalaciones locales, permitiéndoles agendar sesiones por tema y modalidad.
- **Incentivos para Mentores:** Gamificación, insignias, reputación dinámica y constancias de horas acumuladas convalidables para créditos extracurriculares.
- **Facilidad Administrativa:** El emparejamiento automatizado reduce la carga manual de intermediación y provee tableros analíticos en tiempo real.

### 4. Viabilidad Legal

- **Ley N° 29733 (Protección de Datos Personales):** Consentimiento informado digital explícito previo al uso de datos académicos, persistencia de auditoría inmutable (IP, timestamp UTC) y uso de UUIDs para anonimización.
- **Ley Universitaria N° 30220 (Artículo 40):** Soporte activo a la obligación institucional de tutoría y acompañamiento pedagógico permanente.
- **Licenciamiento y Propiedad Intelectual:** Componentes y librerías open-source bajo licencias MIT/Apache 2.0 y registro de software ante la Dirección de Investigación de la UPT.

### 5. Viabilidad Social y Ambiental

- **Factibilidad Social:** Democratización de la asesoría académica, fomento de redes colaborativas de apoyo mutuo y desarrollo de habilidades pedagógicas en mentores.
- **Factibilidad Ambiental:** Política institucional *Paperless* (cero papel en bitácoras, marcación de asistencia y certificados digitales) y arquitectura cloud de bajo consumo.

## 3.6. Información obtenida del Levantamiento de Información

Durante la etapa de levantamiento y refinamiento, el equipo C-SharkTeam ejecutó entrevistas estructuradas con los actores institucionales clave de la EPIS-UPT para formalizar las reglas de negocio, la arquitectura del software y las directrices de convalidación académica:

1. **Ing. Liliana Vega Bernal (Coordinación de Tutoría):** Fijó la necesidad de trazabilidad en asignaturas filtro, el control perentorio de asistencia, la confirmación anticipada obligatoria a $T-24\text{ h}$, el diligenciamiento de bitácoras docentes y la habilitación de encuestas de satisfacción durante 24 horas.
2. **Mgtr. Ing. Enrique Lanchipa Valencia (Docente / Arquitectura de Software):** Estableció las pautas de arquitectura desacoplada, diseño de microservicios RESTful, balanceo de carga en algoritmos de recomendación y optimización de latencias algorítmicas por debajo de 500 ms.
3. **Dr. Luis Alfredo Fernández Vizcarra (Docente Asesor / Metodólogo):** Definió las métricas de rendimiento algorítmico (*Precision@k*, *NDCG*), los criterios de evaluación de usabilidad mediante el instrumento SUS (>75 puntos) y el cumplimiento estricto del protocolo de consentimiento digital bajo la Ley N° 29733.
4. **Ing. Haydee Raquel Sisa Yataco (Directora (e) EPIS-UPT):** Validó los criterios para la emisión de certificados oficiales en formato PDF con folio y código QR, así como el umbral de 20 horas auditadas para la postulación a créditos extracurriculares oficiales.

---

# 4. Análisis de Procesos

## 4.1. Diagrama del Proceso Actual (As-Is)

El proceso actual de asesoría académica en la EPIS-UPT opera de forma informal, desestructurada y sin trazabilidad institucional. Cuando un alumno de I a IV ciclo afronta vacíos conceptuales en asignaturas críticas (Cálculo, Algoritmos, Estructuras de Datos, POO), recurre a grupos no oficiales de mensajería (WhatsApp/Telegram). No existen criterios para evaluar la competencia de quien brinda la ayuda, no hay control de espacios, no se registran asistencias ni bitácoras pedagógicas, y la escuela carece de datos para convalidar horas o intervenir preventivamente.

### Diagrama de Actividades del Proceso Actual (As-Is)

```plantuml
@startuml
|Estudiante (I - IV Ciclo)|
start
:Identifica dificultad conceptual\nen asignatura filtro;
:Publica consulta en grupo informal\n(WhatsApp/Telegram);

if (¿Algún compañero responde?) then (No)
  :Permanece sin ayuda especializada;
  :Acude tardíamente a tutoría docente regular;
  :Riesgo alto de reprobación en evaluaciones;
  stop
else (Sí)
  |Compañero / Mentor Informal|
  :Acepta ayudar de manera ocasional e informal;
  |Estudiante (I - IV Ciclo)|
  :Coordina horario y medio por chat privado;
  |Compañero / Mentor Informal|
  :Busca aula o espacio libre\nen campus empíricamente;
  :O crea enlace personal improvisado\n(Meet/Zoom);
  |Estudiante (I - IV Ciclo)|
  :Asiste a la sesión de asesoría informal;
  |Compañero / Mentor Informal|
  :Explica dudas sin guía o temario estructurado;
  |Tutoría / Dirección de Escuela|
  :Sin registro de asistencia ni temas tratados;
  :Sin métricas de demanda académica;
  :Sin reconocimiento formal de horas para el mentor;
  stop
endif
@enduml
```

Fuente: Elaboración propia.

## 4.2. Diagrama del Proceso Propuesto (To-Be)

El proceso propuesto estructura, optimiza y automatiza integralmente el ciclo de vida de las mentorías académicas P2P. Incorpora autenticación institucional 2FA con consentimiento digital (Ley N° 29733), recomendación algorítmica híbrida (*EdRecSys*), reserva concurrente con cerrojos pesimistas, corte desatendido de quórum a $T-24\text{ h}$ con resolución de contingencia, marcación de asistencia mediante pases QR dinámicos TOTP, registro de bitácoras docentes firmadas con SHA-256 en 48 horas, encuestas de calidad de 24 horas y emisión formal de certificados oficiales foliados con código QR institucional.

### Diagrama de Actividades del Proceso Propuesto (To-Be)

```plantuml
@startuml
|Estudiante / Mentoreado|
start
:Inicia sesión con correo institucional\ny código OTP (2FA);
if (¿Primer acceso?) then (Sí)
  :Formaliza consentimiento digital\n(Ley N° 29733);
endif

|Mentor (VII - X Ciclo)|
:Publica oferta de mentoría\n(Materia, Temario, Fecha, Modalidad);

|Sistema Web P2P (Backend / RecSys)|
:Valida disponibilidad de aula física o enlace virtual;
:Registra oferta en catálogo curricular;
:Ejecuta motor híbrido EdRecSys\n(Similitud Coseno + Filtrado Colaborativo);
:Presenta ranking Top-k ordenado al estudiante;

|Estudiante / Mentoreado|
:Explora recomendaciones o registra demanda;
:Reserva cupo de mentoría (Cerrojo pesimista FOR UPDATE);
:Ratifica asistencia obligatoria\nantes de T-24h;

|Sistema Web P2P (Backend / Servicio Cron)|
:Ejecuta corte automatizado a T-24h;
:Cancela reservas no ratificadas y libera vacantes;
if (¿Quórum >= 50% de aforo?) then (Sí)
  :Notifica confirmación definitiva de sesión;
else (No)
  :Transiciona a QUORUM_INSUFICIENTE;
  |Mentor (VII - X Ciclo)|
  if (¿Mentor decide continuar?) then (Sí)
    :Ratifica realización extraordinaria;
  else (No)
    |Sistema Web P2P (Backend / Servicio Cron)|
    :Cancela sesión y notifica a participantes;
    :Libera aula física o sala virtual;
    stop
  endif
endif

|Mentor y Estudiantes|
:Desarrollan la sesión de mentoría;
:Estudiantes escanean pase QR TOTP de asistencia\no mentor marca asistencia en lista;

|Mentor (VII - X Ciclo)|
:Registra bitácora pedagógica antes de 48h\n(Temas, observaciones, firma SHA-256);

|Estudiante / Mentoreado|
:Responde encuesta de satisfacción (24h);

|Sistema Web P2P (Backend / RecSys)|
:Actualiza reputación e insignias del mentor;
:Acumula horas académicas auditables;

|Administración (Tutoría / Dirección)|
:Supervisa tablero analítico institucional;
:Visa bitácoras y autoriza horas de mentoría;
if (¿Horas acumuladas >= Umbral parametrizado 20h?) then (Sí)
  :Emite certificado digital oficial PDF\ncon código SHA-256 y QR de verificación;
endif
stop
@enduml
```

Fuente: Elaboración propia.

---

# 5. Especificación de Requerimientos de Software

## 5.1. Identificación de Módulos y Capacidades Funcionales

Para estructurar la solución de software y garantizar una adecuada cohesión y bajo acoplamiento arquitectónico, el alcance del Sistema Web P2P se organiza en **ocho módulos canónicos especializados**. Esta descomposición organiza la lógica de negocio y delimita las responsabilidades de los actores en correspondencia estricta con los **24 casos de uso oficiales (CUS-001 al CUS-024)**.

### Cuadro 5.1: Identificación de Módulos y Capacidades Funcionales del Sistema Web P2P

| Código | Módulo / Subsistema | Propósito | Capacidades Funcionales Principales | Actores / Sistemas Involucrados | CUS Asociados |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **MOD-01** | Seguridad, Autenticación y Gobernanza | Garantizar el acceso seguro y exclusivo a la comunidad universitaria institucional, protegiendo los datos bajo la Ley N° 29733 y administrando privilegios de acceso. | • Autenticación institucional con 2FA mediante código OTP temporal de 6 dígitos.<br>• Formalización de consentimiento informado digital obligatorio.<br>• Administración jerárquica de roles (promoción por mérito académico de Mentoreado a Mentor). | Usuario Institucional, Administrador, Servicio SMTP UPT | CUS-001, CUS-010 |
| **MOD-02** | Ofertas de Mentoría y Gestión de Recursos | Planificar y publicar las sesiones formativas gestionando la infraestructura física de la escuela y las salas virtuales. | • Publicación y configuración de ofertas de mentoría en materias aprobadas.<br>• Verificación de espacios físicos libres (aulas/laboratorios) y salas virtuales.<br>• Gestión de imprevistos, reprogramación y anulación de sesiones. | Estudiante Mentor, Administrador, Infraestructura EPIS | CUS-006, CUS-008 |
| **MOD-03** | Perfil del Mentor y Plan de Aprendizaje | Administrar la disponibilidad horaria de los participantes y el catálogo curricular oficial de asignaturas críticas. | • Configuración de perfil formativo y matriz horaria semanal interactiva 6×11.<br>• Exploración interactiva del catálogo curricular de asignaturas filtro y temarios silábicos. | Estudiante Mentoreado, Estudiante Mentor | CUS-005, CUS-021 |
| **MOD-04** | Demanda y Recomendaciones Personalizadas | Emparejar las necesidades conceptuales del mentoreado con las competencias docentes de los mentores mediante inteligencia artificial. | • Inferencia algorítmica híbrida Top-k (Similitud Coseno + Filtrado Colaborativo).<br>• Registro y visualización del banco de solicitudes temáticas por demanda. | Estudiante Mentoreado, Estudiante Mentor, Motor EdRecSys | CUS-002, CUS-003 |
| **MOD-05** | Quórum, Confirmación y Cancelaciones | Controlar la inscripción concurrente, ratificación previa y evaluación automatizada de quórum a $T-24\text{ h}$. | • Reserva concurrente de cupos con control de aforo y cerrojos pesimistas.<br>• Ratificación anticipada obligatoria de asistencia por el estudiante.<br>• Desistimiento voluntario de reservas con liberación inmediata de vacantes.<br>• Demonio cron de corte a $T-24\text{ h}$ y evaluación automática de quórum (50%).<br>• Gestión resolutiva del mentor ante quórum insuficiente. | Estudiante Mentoreado, Estudiante Mentor, Demonio Cron Backend | CUS-004, CUS-024, CUS-017, CUS-023, CUS-007 |
| **MOD-06** | Asistencia, Bitácoras y Feedback | Proveer trazabilidad sobre el desarrollo pedagógico, control estricto de asistencia y evaluación de calidad. | • Marcación de asistencia presencial/virtual mediante pases QR dinámicos TOTP.<br>• Registro estructurado de bitácora docente en 48h con firma SHA-256.<br>• Consulta de historial cronológico de sesiones y bitácoras académicas.<br>• Encuestas de satisfacción post-sesión de 24 horas y descarga de recursos. | Estudiante Mentoreado, Estudiante Mentor | CUS-012, CUS-013, CUS-014 |
| **MOD-07** | Gamificación e Incentivos | Incentivar la participación continua de mentores mediante reconocimientos gamificados y certificación auditable. | • Emisión digital de certificados PDF con folio correlativo, hash SHA-256 y código QR.<br>• Tablero de reputación y catálogo de insignias por mérito docente. | Estudiante Mentor, Administrador (Tutoría / Dirección) | CUS-018, CUS-019 |
| **MOD-08** | Analítica, Notificaciones y Configuración | Dotar a la facultad de herramientas analíticas de decisión, motor de alertas y gobernanza de parámetros. | • Despacho de notificaciones y recordatorios temporales de eventos críticos.<br>• Generación de reportes analíticos de demanda insatisfecha y desempeño.<br>• Consulta de métricas institucionales de retención y criterios ICACIT.<br>• Auditoría administrativa de bitácoras, consentimientos y trazas de seguridad.<br>• Parametrización institucional de umbrales y aforos del sistema.<br>• Gestión administrativa del catálogo de asignaturas y temas críticos. | Administrador (Tutoría / Dirección EPIS), Demonio Backend | CUS-009, CUS-011, CUS-015, CUS-016, CUS-020, CUS-022 |

Fuente: Elaboración propia.

---

## 5.2. Requerimientos No Funcionales (ISO/IEC 25010)

Los requerimientos no funcionales definen los atributos de calidad, restricciones arquitectónicas y niveles de servicio del software. Se estructuran bajo el estándar internacional **ISO/IEC 25010**, incorporando los valores y métricas empíricas obtenidas en la fase de construcción y verificación experimental.

### Cuadro 5.2: Matriz de Requerimientos No Funcionales bajo el Estándar ISO/IEC 25010

| Código | Característica (ISO 25010) | Requerimiento No Funcional | Criterio de Aceptación / Especificación Técnica | Métrica / Umbral Empírico Verificado |
| :---: | :--- | :--- | :--- | :--- |
| **RNF01** | Seguridad | Autenticación multifactor y gestión segura de sesiones | Autenticación 2FA sin contraseñas fijas mediante código OTP numérico de 6 dígitos remitido al correo institucional `@upt.pe`. Sesión gobernada mediante JSON Web Tokens (JWT) firmados con algoritmo criptográfico HMAC-SHA256. | • TTL del OTP: 5 minutos (300 s).<br>• Expiración de JWT: 480 min (8 horas).<br>• Cooldown de reenvío: 60 s.<br>• 100% de endpoints protegidos por dependencias de autenticación. |
| **RNF02** | Seguridad | Privacidad, aislamiento y protección RLS (Ley N° 29733) | Comunicaciones cifradas con TLS 1.3. Persistencia en PostgreSQL protegida mediante políticas de seguridad a nivel de fila (*Row Level Security - RLS*) que aíslan expedientes y notas. Identificadores primarios generados como UUID v4 para prevenir enumeración secuencial. | • 100% de tablas sensibles con RLS activo.<br>• 0% de fuga de credenciales o códigos.<br>• Registro inmutable de IP y timestamp UTC en consentimientos. |
| **RNF03** | Rendimiento y Eficiencia | Latencia de inferencia y precisión del recomendador | El microservicio *EdRecSys* en Python vectoriza necesidades y temarios silábicos calculando similitud coseno y ranking Top-k con filtrado colaborativo ponderado por reputación y balance de carga. | • **Precision@3 = 83.3%**<br>• **Precision@5 = 80.0%**<br>• **NDCG = 0.82**<br>• **Latencia media = 12.4 ms** (umbral de aceptación $\le 500$ ms). |
| **RNF04** | Rendimiento y Eficiencia | Tiempo de carga y renderizado de la interfaz SPA | La aplicación web React SPA optimiza la descarga y renderizado de componentes mediante Vite, code splitting y lazy loading en navegadores de escritorio y dispositivos móviles. | • FCP (*First Contentful Paint*) $< 1.2$ s.<br>• Bundle inicial comprimido $< 250$ KB.<br>• Transiciones de interfaz sin latencias perceptibles ($< 50$ ms). |
| **RNF05** | Usabilidad | Ergonomía, accesibilidad universal y facilidad de uso | Interfaces responsivas que implementan el Design System institucional con Tailwind CSS y componentes accesibles que garantizan navegación por teclado, soporte para lectores de pantalla y contraste cromático. | • **Puntaje SUS > 75 puntos** en prueba piloto.<br>• Cumplimiento **WCAG 2.1 Nivel AA** (contraste $\ge 4.5:1$).<br>• Atributos ARIA en 100% de controles interactivos. |
| **RNF06** | Fiabilidad y Disponibilidad | Continuidad operativa institucional | Disponibilidad ininterrumpida de los servicios web, endpoints de API y motor de base de datos durante el periodo académico regular, tolerando picos de demanda en semanas de exámenes. | • Disponibilidad del servicio $\ge 99.5\%$.<br>• Tolerancia a fallos transitorios en microservicios.<br>• Health-checks automatizados en `/health`. |
| **RNF07** | Fiabilidad e Integridad | Consistencia transaccional en reservas concurrentes | Persistencia transaccional ACID en PostgreSQL gobernada mediante cerrojos pesimistas a nivel de fila (`SELECT ... FOR UPDATE`) que previene condiciones de carrera (*race conditions*) y sobreasignación de cupos. | • Tasa de sobreasignación: **estrictamente 0.0%**.<br>• 100% de transacciones concurrentes serializadas correctamente. |
| **RNF08** | Compatibilidad y Portabilidad | Compatibilidad multiplataforma en navegadores | Soporte multiplataforma garantizado en navegadores web modernos de escritorio y móviles (Google Chrome, Mozilla Firefox, Microsoft Edge, Apple Safari) bajo diseño responsivo. | • 100% operativo en resoluciones desde $360\text{ px}$ (móvil) hasta $1920\times1080\text{ px}$ (desktop). |
| **RNF09** | Mantenibilidad | Arquitectura limpia y cobertura de pruebas automatizadas | Arquitectura limpia desacoplada en tres capas (Presentación React, API/Lógica FastAPI, Persistencia PostgreSQL). Contratos de datos fuertemente tipados con Pydantic v2 y TypeScript. | • **627 pruebas automatizadas aprobadas (280 backend Pytest, 347 frontend Vitest)**.<br>• Cobertura de código **> 85%**.<br>• 0 errores de linters (`ruff`, `eslint`). |
| **RNF10** | Interoperabilidad | Resiliencia y manejo controlado de excepciones | Manejo estructurado de excepciones con códigos HTTP estandarizados (400, 401, 403, 404, 409, 422, 500), degradación elegante y reintentos ante caídas del servidor de correo SMTP. | • 100% de excepciones formateadas en JSON con código de error institucional.<br>• Timeouts configurados a $\le 5$ s. |

Fuente: Elaboración propia.

---

## 5.3. Matriz Consolidada de Requerimientos Funcionales

El sistema formaliza **veintiséis requerimientos funcionales atómicos (RF01 al RF26)**. Cada requerimiento establece el comportamiento operativo del sistema, sus casos de uso soportados, sus endpoints RESTful y sus componentes de frontend y backend correspondientes.

### Cuadro 5.3: Matriz Consolidada de Requerimientos Funcionales del Sistema Web P2P (RF01 al RF26)

| Código | Módulo | Requerimiento Funcional | Casos de Uso | Endpoint RESTful / Verbo HTTP | Componentes Técnicos (UI / Service / Model) | Criticidad |
| :---: | :---: | :--- | :---: | :--- | :--- | :---: |
| **RF01** | MOD-01 | Autenticación institucional multifactor (2FA) | CUS-001 | `POST /api/v1/auth/request-otp`<br>`POST /api/v1/auth/verify-otp` | `LoginOtpView.tsx`<br>`AuthService.py` / `authService.ts`<br>`Usuario`, `CodigoOTP` | Crítica |
| **RF02** | MOD-01 | Formalización de consentimiento digital (Ley 29733) | CUS-001 | `GET /api/v1/consent/status`<br>`POST /api/v1/consent/accept` | `ConsentModalView.tsx`<br>`ConsentService.py`<br>`ConsentimientoLegal` | Crítica |
| **RF03** | MOD-01 | Gestión y asignación administrativa de roles | CUS-010 | `GET /api/v1/roles/candidates`<br>`POST /api/v1/roles/promote-mentor` | `AdminRolesView.tsx`<br>`RoleService.py`<br>`Usuario`, `Rol` | Alta |
| **RF04** | MOD-03 | Configuración de perfil formativo y matriz horaria | CUS-005 | `GET /api/v1/profile/me`<br>`PUT /api/v1/profile/availability` | `ProfileAvailabilityView.tsx`<br>`ProfileService.py`<br>`PerfilFormativo`, `Disponibilidad` | Alta |
| **RF05** | MOD-03 | Gestión de catálogo de asignaturas y temarios | CUS-021 | `GET /api/v1/curriculum/courses`<br>`GET /api/v1/curriculum/courses/{id}/topics` | `CurriculumCatalogView.tsx`<br>`CurriculumService.py`<br>`CursoCritico`, `TemaCurricular` | Alta |
| **RF06** | MOD-04 | Inferencia algorítmica y ranking Top-k | CUS-002 | `POST /api/v1/recommendations/match` | `RecommendationsView.tsx`<br>`RecommendationService.py`<br>`Motor EdRecSys` | Crítica |
| **RF07** | MOD-04 | Registro y banco de solicitudes por demanda | CUS-003 | `GET /api/v1/demands`<br>`POST /api/v1/demands` | `DemandsBankView.tsx`<br>`DemandService.py`<br>`SolicitudDemanda` | Media |
| **RF08** | MOD-02 | Publicación y parametrización de ofertas de mentoría | CUS-006 | `POST /api/v1/mentorships/offers` | `PublishMentorshipView.tsx`<br>`MentorshipService.py`<br>`OfertaMentoria` | Alta |
| **RF09** | MOD-02 | Aprovisionamiento automatizado de espacios | CUS-006, CUS-008 | `GET /api/v1/spaces/availability` | `SpaceSelectorView.tsx`<br>`SpaceService.py`<br>`EspacioFisico` | Alta |
| **RF10** | MOD-02 | Procesamiento de cronogramas institucionales | CUS-008 | `POST /api/v1/spaces/import-schedule` | `AdminScheduleUploadView.tsx`<br>`ScheduleParserService.py`<br>`HorarioOcupacion` | Alta |
| **RF11** | MOD-02 | Gestión de imprevistos, reprogramación y anulación | CUS-006 | `PUT /api/v1/mentorships/offers/{id}/reschedule`<br>`DELETE /api/v1/mentorships/offers/{id}` | `MentorOffersView.tsx`<br>`MentorshipService.py`<br>`OfertaMentoria` | Alta |
| **RF12** | MOD-05 | Reserva de cupos con control de aforo y cerrojo | CUS-004 | `POST /api/v1/bookings` | `BookingModalView.tsx`<br>`BookingService.py` (FOR UPDATE)<br>`ReservaCupo`, `SesionMentoria` | Crítica |
| **RF13** | MOD-05 | Ratificación anticipada de asistencia (hasta T-24h) | CUS-024 | `POST /api/v1/bookings/{id}/confirm` | `StudentBookingsView.tsx`<br>`BookingService.py`<br>`ReservaCupo` | Alta |
| **RF14** | MOD-05 | Desistimiento voluntario y liberación de cupo | CUS-017 | `POST /api/v1/bookings/{id}/cancel` | `StudentBookingsView.tsx`<br>`BookingService.py`<br>`ReservaCupo` | Alta |
| **RF15** | MOD-05 | Monitoreo desatendido y corte de quórum en T-24h | CUS-023, CUS-009 | `POST /api/v1/quorum/cron-eval`<br>`GET /api/v1/notifications` | `NotificationCenterView.tsx`<br>`QuorumCronService.py`<br>`SesionMentoria`, `Notificacion` | Crítica |
| **RF16** | MOD-05 | Gestión resolutiva ante quórum insuficiente | CUS-007 | `POST /api/v1/mentorships/sessions/{id}/resolve-quorum` | `MentorSessionActionView.tsx`<br>`MentorshipService.py`<br>`SesionMentoria` | Alta |
| **RF17** | MOD-06 | Marcación de asistencia con pase QR dinámico TOTP | CUS-012 | `GET /api/v1/attendance/qr-pass`<br>`POST /api/v1/attendance/scan-qr` | `QrScannerView.tsx` / `QrPassView.tsx`<br>`AttendanceService.py`<br>`AsistenciaSesion` | Alta |
| **RF18** | MOD-06 | Registro de bitácora docente en 48h con hash SHA-256 | CUS-013 | `POST /api/v1/bitacora/sessions/{id}` | `BitacoraRegisterView.tsx`<br>`BitacoraService.py`<br>`BitacoraPedagogica` | Alta |
| **RF19** | MOD-06 | Consulta de historial de sesiones y bitácoras | CUS-014 | `GET /api/v1/bitacora/history` | `BitacoraHistoryView.tsx`<br>`BitacoraService.py`<br>`BitacoraPedagogica` | Media |
| **RF20** | MOD-06 | Gestión y descarga de recursos académicos | CUS-006, CUS-014 | `GET /api/v1/resources/sessions/{id}`<br>`POST /api/v1/resources/sessions/{id}` | `SessionResourcesView.tsx`<br>`ResourceService.py`<br>`RecursoAcademico` | Media |
| **RF21** | MOD-07 | Cálculo de reputación y tablero de insignias | CUS-019 | `GET /api/v1/gamification/mentor/{id}` | `MentorBadgesView.tsx`<br>`GamificationService.py`<br>`Insignia`, `ReputacionMentor` | Media |
| **RF22** | MOD-07 | Parametrización de umbrales y autorización de certificados | CUS-018 | `POST /api/v1/certificates/generate` | `AdminCertificatesView.tsx`<br>`CertificateService.py`<br>`CertificadoHoras` | Media |
| **RF23** | MOD-07 | Descarga y verificación pública con código QR | CUS-018 | `GET /api/v1/certificates/{id}/pdf`<br>`GET /api/v1/certificates/verify/{hash}` | `CertificateDownloadView.tsx`<br>`PdfGeneratorService.py`<br>`CertificadoHoras` | Media |
| **RF24** | MOD-08 | Configuración de parámetros institucionales | CUS-020 | `GET /api/v1/admin/settings`<br>`PUT /api/v1/admin/settings` | `AdminSettingsView.tsx`<br>`AdminService.py`<br>`ParametroInstitucional` | Media |
| **RF25** | MOD-08 | Tablero analítico y métricas institucionales | CUS-011, CUS-015 | `GET /api/v1/analytics/dashboard` | `AdminAnalyticsView.tsx`<br>`AnalyticsService.py`<br>`KpiAcademico` | Alta |
| **RF26** | MOD-08 | Auditoría administrativa de bitácoras y materias | CUS-016, CUS-022 | `GET /api/v1/audit/logs`<br>`POST /api/v1/audit/bitacora/{id}/review` | `AdminAuditView.tsx`<br>`AuditService.py`<br>`TrazaAuditoria`, `Bitacora` | Alta |

Fuente: Elaboración propia.

---

## 5.4. Reglas de Negocio Institucionales

Las catorce reglas de negocio institucionales (**RN-01 al RN-14**) gobiernan la interacción pedagógica, la seguridad y la integridad transaccional de la plataforma en la EPIS-UPT:

### Cuadro 5.4: Matriz de Reglas de Negocio Institucionales del Sistema Web P2P (RN-01 al RN-14)

| Código | Regla de Negocio | Política Operativa Institucional | Mecanismo de Imposición en Código y Persistencia | Módulo |
| :---: | :--- | :--- | :--- | :---: |
| **RN-01** | Acceso Institucional Exclusivo y 2FA | Acceso exclusivo con cuentas de correo `@upt.pe`. Envío de código OTP de 6 dígitos con tiempo de vida máximo e improrrogable de 5 minutos (300 s). | `AuthService.request_otp` valida regex `@upt.pe`, genera OTP con `secrets` y aplica hash SHA-256 en BD (`CodigoOTP`). Cooldown de 60 s. | MOD-01 |
| **RN-02** | Consentimiento Legal Digital (Ley N° 29733) | Consentimiento informado obligatorio en el primer acceso. El rechazo aborta la sesión e impide el uso de datos académicos. | `ConsentService.verify` bloquea endpoints mediante middleware. Inserta tupla inmutable con UUID, IP, User-Agent y timestamp UTC en `consentimientos_legales`. | MOD-01 |
| **RN-03** | Jerarquía de Roles y Verificación de Mérito | Todo usuario ingresa como Mentoreado. Para ser Mentor debe pertenecer a ciclos VII-X y haber aprobado la materia con calificación sobresaliente. | `RoleService.promote_to_mentor` valida `ciclo >= 7`, nota mínima $\ge 14.0$ y asigna `UserRole.mentor` en `usuario_roles`. Restricción en `RoleGuard.tsx`. | MOD-01 |
| **RN-04** | Antelación de Publicación ($\ge 24\text{ h}$) | Toda oferta de mentoría debe publicarse con una antelación mínima de 24 horas respecto a su inicio, recomendándose 48 horas ($T \ge 48\text{ h}$). | Validación Pydantic en `MentorshipCreateRequest`: `assert fecha_inicio >= now() + timedelta(hours=24)`. Rechaza con HTTP 422 si la antelación es menor. | MOD-02 |
| **RN-05** | Control Estricto de Aforos Estándar | Aforo máximo de 10 participantes en sesiones presenciales y 20 en sesiones virtuales. Bloqueo automático ante aforo lleno. | Constraint en BD `chk_sesion_aforo` (`aforo <= 10` presencial, `aforo <= 20` virtual). Cerrojo pesimista `SELECT ... FOR UPDATE` en `BookingService`. | MOD-05 |
| **RN-06** | Asignación Validada de Espacios Físicos | Las sesiones presenciales solo se agendan en aulas o laboratorios libres de la EPIS-UPT validados contra la carga lectiva regular. | `SpaceService.check_space_conflict` ejecuta consulta con solapamiento temporal: `NOT (fin <= :inicio OR inicio >= :fin)` sobre `espacios_fisicos`. | MOD-02 |
| **RN-07** | Aprovisionamiento Virtual Automatizado | Para sesiones virtuales, la plataforma valida y asocia enlaces institucionales seguros de teleconferencia sin intervención manual externa. | Validación de formato URL segura en `MentorshipService`. Persistencia del enlace en `sesiones_mentoria.enlace_virtual` y visibilidad restringida a inscritos. | MOD-02 |
| **RN-08** | Ventana de Ratificación hasta $T-24\text{ h}$ | La confirmación de asistencia debe realizarse hasta el corte de 24 horas previas. Las reservas no ratificadas pierden vigencia (`NO_CONFIRMADA`). | `BookingService.confirm` valida `now() <= sesion.fecha_inicio - timedelta(hours=24)`. Si el corte venció, arroja HTTP 400 (`CONFIRMATION_CLOSED`). | MOD-05 |
| **RN-09** | Quórum Mínimo del 50% en $T-24\text{ h}$ | Toda sesión debe alcanzar un quórum del 50% de su aforo (5 en presencial, 10 en virtual). Si no se alcanza, transiciona a `QUORUM_INSUFICIENTE`. | Demonio `QuorumCronService` totaliza confirmados a $T-24\text{ h}$. Si `confirmados < aforo * 0.5`, actualiza estado en BD y notifica al mentor. | MOD-05 |
| **RN-10** | Cancelación Oportuna y Liberación de Espacios | Al cancelarse una sesión (por quórum o imprevisto), se notifica de inmediato a los inscritos y se libera la infraestructura física o virtual. | Transacción ACID que actualiza `sesiones_mentoria.estado = 'CANCELADA'`, cancela reservas asociadas y limpia la ocupación del aula en `espacios_fisicos`. | MOD-05 |
| **RN-11** | Ponderación y Desempate Algorítmico | El recomendador pondera afinidad temática por similitud coseno. Desempata por: 1) reputación, 2) menor carga activa, y 3) condición prioritaria. | Función matemática en `RecommendationEngine.rank_mentors`: $Score = 0.5 \cdot S_{cos} + 0.3 \cdot Rep + 0.1 \cdot (1 - Carga) + 0.1 \cdot Prio$. | MOD-04 |
| **RN-12** | Cierre de Bitácora y Filtro de Evaluación | El mentor dispone de 48 horas post-sesión para registrar la bitácora con los temas dictados y la asistencia. Solo los asistentes evalúan. | `BitacoraService.create` valida `now() <= fin + timedelta(hours=48)`. Genera hash SHA-256. `FeedbackService` valida `asistencia.estado == 'ASISTIO'`. | MOD-06 |
| **RN-13** | Ventana Perentoria para Encuestas (24h) | El formulario de evaluación de calidad está habilitado durante 24 horas posteriores al cierre de la sesión. Luego se cierra definitivamente. | `FeedbackService.submit` verifica `now() <= bitacora.fecha_cierre + timedelta(hours=24)`. Si expira, retorna HTTP 400 (`SURVEY_WINDOW_EXPIRED`). | MOD-06 |
| **RN-14** | Certificación por Horas Auditadas ($\ge 20\text{ h}$) | La certificación de horas exige acumular un mínimo de 20 horas efectivas en el semestre con el 100% de bitácoras auditadas y visadas. | `CertificateService.check_eligibility` suma horas en `bitacoras_pedagogicas` con `estado_visado == 'APROBADO'`. Bloquea si suma $< 20.0$. | MOD-07 |

Fuente: Elaboración propia.

---

## 5.5. Matriz de Trazabilidad Bidireccional de Requerimientos

### Cuadro 5.5: Matriz de Trazabilidad Bidireccional de Requerimientos del Sistema Web P2P

| Código RF | Requerimiento Funcional | Módulo | RN Asociadas | Casos de Uso | RNF Relacionados | Método de Verificación Técnica |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **RF01** | Autenticación institucional multifactor (2FA) | MOD-01 | RN-01 | CUS-001 | RNF01, RNF02 | Prueba automatizada con mock SMTP, comprobación de OTP y expiración de JWT. |
| **RF02** | Formalización de consentimiento digital | MOD-01 | RN-02 | CUS-001 | RNF02 | Verificación de persistencia de IP/timestamp y bloqueo perentorio en endpoints. |
| **RF03** | Gestión y asignación administrativa de roles | MOD-01 | RN-03 | CUS-010 | RNF02, RNF09 | Inspección funcional de actualización de privilegios y validación de mérito en BD. |
| **RF04** | Configuración de perfil y matriz horaria | MOD-03 | RN-03, RN-04 | CUS-005 | RNF04, RNF08 | Prueba UI de matriz interactiva 6×11 y persistencia atómica en BD. |
| **RF05** | Gestión del catálogo curricular y temarios | MOD-03 | RN-11 | CUS-021 | RNF09 | Prueba de endpoints CRUD sobre cursos filtro y unidades silábicas. |
| **RF06** | Inferencia algorítmica y ranking Top-k | MOD-04 | RN-04, RN-11 | CUS-002 | RNF03 | Validación experimental de precisión (*Precision@3*, *NDCG*) y latencia $\le 500$ ms. |
| **RF07** | Registro y banco de solicitudes por demanda | MOD-04 | RN-04 | CUS-003 | RNF04, RNF09 | Prueba funcional de registro temático y visibilidad en catálogo de demanda. |
| **RF08** | Publicación y parametrización de ofertas | MOD-02 | RN-04, RN-05 | CUS-006 | RNF04, RNF09 | Comprobación de validación de antelación $\ge 24\text{ h}$ y aforos máximos en creación. |
| **RF09** | Aprovisionamiento automatizado de espacios | MOD-02 | RN-06, RN-07 | CUS-006, CUS-008 | RNF09, RNF10 | Verificación de detección de solapamientos en aulas y validación de enlaces web. |
| **RF10** | Procesamiento de cronogramas oficiales | MOD-02 | RN-06 | CUS-008 | RNF09, RNF10 | Prueba funcional de ingesta estructurada de cronogramas de aulas libres. |
| **RF11** | Gestión de imprevistos y reprogramación | MOD-02 | RN-10 | CUS-006 | RNF09, RNF10 | Prueba funcional de reprogramación horaria y despacho de avisos a inscritos. |
| **RF12** | Reserva de cupos con cerrojo pesimista | MOD-05 | RN-05 | CUS-004 | RNF07 | Prueba de estrés concurrente con `SELECT FOR UPDATE` para verificar 0.0% sobrecupo. |
| **RF13** | Ratificación anticipada de asistencia | MOD-05 | RN-08 | CUS-024 | RNF07, RNF09 | Prueba de transición de estado `PENDIENTE` a `CONFIRMADA` dentro del plazo. |
| **RF14** | Desistimiento voluntario de reservas | MOD-05 | RN-08, RN-10 | CUS-017 | RNF07 | Prueba de anulación voluntaria antes de $T-24\text{ h}$ y restitución de vacante. |
| **RF15** | Monitoreo desatendido y corte de quórum | MOD-05 | RN-08, RN-09 | CUS-023, CUS-009 | RNF06, RNF09 | Verificación del demonio cron a $T-24\text{ h}$, revocación de pendientes y alerta. |
| **RF16** | Gestión resolutiva ante quórum insuficiente | MOD-05 | RN-09, RN-10 | CUS-007 | RNF09, RNF10 | Prueba de interfaz de decisión del mentor (continuar excepcional vs cancelar). |
| **RF17** | Marcación de asistencia con pase QR TOTP | MOD-06 | RN-05, RN-12 | CUS-012 | RNF02, RNF09 | Validación de generación y escaneo de pase QR efímero en check-in de sesión. |
| **RF18** | Registro de bitácora docente con SHA-256 | MOD-06 | RN-12 | CUS-013 | RNF02, RNF09 | Prueba de cálculo de hash criptográfico inmutable y cierre en plazo de 48 horas. |
| **RF19** | Consulta de historial de sesiones y bitácoras | MOD-06 | — | CUS-014 | RNF02, RNF04 | Prueba de interfaz de historial con filtros por materia y fecha. |
| **RF20** | Gestión y descarga de recursos académicos | MOD-06 | — | CUS-006, CUS-014 | RNF02, RNF09 | Comprobación de subida de enlaces didácticos y descarga autorizada. |
| **RF21** | Cálculo de reputación y tablero de insignias | MOD-07 | RN-13 | CUS-019 | RNF05, RNF09 | Prueba matemática del recálculo de reputación y desbloqueo de insignias. |
| **RF22** | Parametrización y emisión de certificados | MOD-07 | RN-14 | CUS-018 | RNF09 | Validación de control de umbral mínimo de 20 horas auditadas para certificar. |
| **RF23** | Descarga y verificación con código QR | MOD-07 | RN-14 | CUS-018 | RNF02, RNF09 | Generación de archivo PDF con ReportLab, comprobación de hash y escaneo QR. |
| **RF24** | Configuración de parámetros institucionales | MOD-08 | RN-11 | CUS-020 | RNF03, RNF05 | Comprobación de actualización de umbrales y realce algorítmico en catálogo. |
| **RF25** | Tablero analítico y métricas de rendimiento | MOD-08 | — | CUS-011, CUS-015 | RNF02, RNF04 | Verificación de consolidación de KPIs institucionales agregados en tiempo real. |
| **RF26** | Auditoría de bitácoras y seguridad | MOD-08 | RN-02, RN-14 | CUS-016, CUS-022 | RNF02, RNF09 | Inspección del panel de visado docente y trazabilidad de consentimientos legales. |

Fuente: Elaboración propia.

---

### Cuadro 5.6: Estado de Verificación y Madurez de Requerimientos en Fase de Construcción (Sprints 1 al 8)

A continuación, se acredita el estado de construcción y verificación empírica de la totalidad de requerimientos del sistema al cierre del ciclo de vida del software (Sprint 8):

| Código | Requerimiento / Atributo de Calidad | Sprint de Construcción | Estado Técnico Final | Evidencia Empírica de Verificación |
| :---: | :--- | :---: | :---: | :--- |
| **RF01** | Autenticación institucional multifactor (2FA) | Sprint 1 | **Construido y Verificado** ✅ | Flujo OTP completo con correo institucional `@upt.pe`, cooldown 60 s, expiración 5 min y token JWT 8 h (13 pruebas Pytest / 15 pruebas Vitest). |
| **RF02** | Consentimiento digital (Ley N° 29733) | Sprint 2 | **Construido y Verificado** ✅ | Modal accesible bajo Ley N° 29733 (`ConsentModalView.tsx`), marcas UTC e IP en BD (`consentimientos_legales`) y bloqueo perentorio RN-02 (9 tests Vitest / 5 tests Pytest). |
| **RF03** | Asignación de roles y mérito académico | Sprint 2 | **Construido y Verificado** ✅ | Asignación de rol `mentoreado`, verificación estricta de mérito académico RN-03 (`ciclo >= 7`) y bloqueo de autopromoción (7 tests Pytest). |
| **RF04** | Perfil formativo y disponibilidad semanal | Sprint 2 | **Construido y Verificado** ✅ | Vista `ProfileAvailabilityView.tsx`, matriz semanal 6×11 (08:00 a 20:00), reemplazo atómico en BD y validación de mérito en cliente (10 tests Vitest / 11 tests Pytest). |
| **RF05** | Catálogo curricular de asignaturas y temas | Sprints 1 y 2 | **Construido y Verificado** ✅ | 5 materias formativas críticas en PostgreSQL, buscador reactivo en tiempo real y exploración profunda de unidades silábicas (4 tests Vitest / 8 tests Pytest). |
| **RF06** | Inferencia algorítmica híbrida Top-k | Sprint 3 | **Construido y Verificado** ✅ | Motor *EdRecSys* con similitud coseno y filtrado colaborativo calibrado (**Precision@3=83.3%, Precision@5=80.0%, latencia 12.4 ms**) (18 tests Pytest / 14 tests Vitest). |
| **RF07** | Banco de solicitudes por demanda | Sprint 3 | **Construido y Verificado** ✅ | Registro de demandas temáticas, validación de temarios y visualización en catálogo con estado de atención (12 tests Pytest / 14 tests Vitest). |
| **RF08** | Publicación de ofertas de mentoría | Sprint 4 | **Construido y Verificado** ✅ | Validación estricta de antelación $\ge 24\text{ h}$ (RN-04), límites de aforo estándar (RN-05) y publicación en catálogo (16 tests Pytest / 18 tests Vitest). |
| **RF09** | Aprovisionamiento de infraestructura | Sprint 4 | **Construido y Verificado** ✅ | Asignación de aulas libres validadas contra solapamientos y configuración de salas virtuales institucionales (14 tests Pytest / 12 tests Vitest). |
| **RF10** | Procesamiento de cronogramas (Parser) | Sprint 4 | **Construido y Verificado** ✅ | Microservicio parser de horarios para detección de ambientes disponibles en la EPIS (8 tests Pytest). |
| **RF11** | Gestión de imprevistos y reprogramación | Sprint 4 | **Construido y Verificado** ✅ | Reprogramación y cancelación justificada con liberación de recursos y despacho de alertas a inscritos (10 tests Pytest / 10 tests Vitest). |
| **RF12** | Reserva de cupos con cerrojo pesimista | Sprint 5 | **Construido y Verificado** ✅ | Persistencia atómica con cerrojos pesimistas (`SELECT ... FOR UPDATE`), serialización estricta y **0.0% de sobrecupo** bajo concurrencia (18 tests Pytest / 16 tests Vitest). |
| **RF13** | Ratificación anticipada de asistencia | Sprint 5 | **Construido y Verificado** ✅ | Confirmación previa hasta el corte de $T-24\text{ h}$ y cambio de estado a `CONFIRMADA` (12 tests Pytest / 14 tests Vitest). |
| **RF14** | Desistimiento voluntario de reservas | Sprint 5 | **Construido y Verificado** ✅ | Anulación voluntaria antes de $T-24\text{ h}$ con restitución instantánea de vacantes en el aforo (10 tests Pytest / 10 tests Vitest). |
| **RF15** | Demonio cron de corte y quórum en $T-24\text{ h}$ | Sprint 5 | **Construido y Verificado** ✅ | Demonio en segundo plano que revoca reservas no confirmadas y transiciona a `QUORUM_INSUFICIENTE` si confirmados $< 50\%$ (16 tests Pytest / 12 tests Vitest). |
| **RF16** | Resolución de contingencia por el mentor | Sprint 5 | **Construido y Verificado** ✅ | Interfaz de decisión del mentor ante quórum deficiente (continuar con asistentes vs cancelar con aviso) (10 tests Pytest / 10 tests Vitest). |
| **RF17** | Marcación de asistencia con QR TOTP | Sprint 6 | **Construido y Verificado** ✅ | Generación de pase QR dinámico TOTP en cliente y escaneo por cámara con validación criptográfica en backend (14 tests Pytest / 20 tests Vitest). |
| **RF18** | Bitácora docente en 48h con hash SHA-256 | Sprint 6 | **Construido y Verificado** ✅ | Formulario obligatorio de bitácora con control de asistencia efectiva, cálculo de hash SHA-256 y ventana de 48h (18 tests Pytest / 22 tests Vitest). |
| **RF19** | Historial de sesiones y bitácoras | Sprint 6 | **Construido y Verificado** ✅ | Vista cronológica individual para mentores y mentoreados con filtros temáticos y trazabilidad de asistencias (8 tests Pytest / 12 tests Vitest). |
| **RF20** | Recursos didácticos de sesión | Sprint 6 | **Construido y Verificado** ✅ | Carga y descarga de enlaces a diapositivas, guías y repositorios asociados a cada sesión (10 tests Pytest / 14 tests Vitest). |
| **RF21** | Gamificación, reputación e insignias | Sprint 7 | **Construido y Verificado** ✅ | Cálculo dinámico de score de reputación, catálogo de insignias por mérito docente y renderizado de tableros lúdicos (12 tests Pytest / 18 tests Vitest). |
| **RF22** | Parametrización y emisión de certificados | Sprint 7 | **Construido y Verificado** ✅ | Control de umbral mínimo de 20 horas auditadas con bitácoras visadas para autorizar la emisión de certificados (14 tests Pytest / 16 tests Vitest). |
| **RF23** | Descarga y verificación institucional QR | Sprint 7 | **Construido y Verificado** ✅ | Generación de certificados PDF con ReportLab, folio correlativo único, hash SHA-256 y QR de verificación pública en portal UPT (16 tests Pytest / 16 tests Vitest). |
| **RF24** | Configuración de parámetros y prioridades | Sprint 8 | **Construido y Verificado** ✅ | Panel administrativo para fijar materias críticas prioritarias con bonificación algorítmica y distintivo visual (10 tests Pytest / 14 tests Vitest). |
| **RF25** | Tablero analítico y métricas ICACIT | Sprint 8 | **Construido y Verificado** ✅ | Panel directivo con indicadores agregados de demanda insatisfecha, ausentismo, efectividad y retención estudiantil (14 tests Pytest / 22 tests Vitest). |
| **RF26** | Auditoría administrativa y visado de horas | Sprint 8 | **Construido y Verificado** ✅ | Módulo de fiscalización docente para visar bitácoras, formular observaciones y validar la inalterabilidad de consentimientos (14 tests Pytest / 16 tests Vitest). |
| **RNF01**| Seguridad: Autenticación 2FA y JWT 8h | Sprints 1-8 | **Construido y Verificado** ✅ | Criptografía HMAC-SHA256 en tokens, hash seguro en códigos OTP y expiración estricta de credenciales. |
| **RNF02**| Seguridad: Row Level Security y Ley 29733 | Sprints 1-8 | **Construido y Verificado** ✅ | Aislamiento multiusuario en 15 tablas relacionales de PostgreSQL con políticas RLS activas y 0% fuga de datos personales. |
| **RNF03**| Rendimiento: Motor híbrido EdRecSys | Sprints 3 y 8 | **Construido y Verificado** ✅ | Inferencia algorítmica en 12.4 ms con Precision@3=83.3%, Precision@5=80.0% y NDCG=0.82. |
| **RNF04**| Rendimiento: Carga ultrarrápida React SPA | Sprints 1-8 | **Construido y Verificado** ✅ | FCP $< 1.2$ s, bundle optimizado con Vite y transiciones reactivas instantáneas. |
| **RNF05**| Usabilidad y Accesibilidad WCAG 2.1 AA | Sprints 1-8 | **Construido y Verificado** ✅ | Puntaje SUS > 75 puntos, navegación por teclado al 100%, contraste cromático $\ge 4.5:1$ y soporte de lectores de pantalla. |
| **RNF06**| Fiabilidad: Uptime institucional $\ge 99.5\%$ | Sprints 1-8 | **Construido y Verificado** ✅ | Continuidad operativa cloud con endpoints de monitoreo de salud (`/health`). |
| **RNF07**| Integridad: Cerrojos transaccionales FOR UPDATE | Sprints 5-8 | **Construido y Verificado** ✅ | Transacciones ACID serializadas que garantizan estrictamente 0.0% de sobreasignación de cupos bajo concurrencia. |
| **RNF08**| Portabilidad: Multiplataforma responsiva | Sprints 1-8 | **Construido y Verificado** ✅ | Paridad visual y operativa al 100% en Chrome, Firefox, Safari y Edge desde resoluciones móviles (360px) a desktop (1080p). |
| **RNF09**| Calidad: Cobertura total de pruebas | Sprints 1-8 | **Construido y Verificado** ✅ | **627 pruebas automatizadas sin fallos (280 backend Pytest, 347 frontend Vitest)** con cobertura global **> 85%**. |
| **RNF10**| Resiliencia: Manejo controlado de fallos | Sprints 1-8 | **Construido y Verificado** ✅ | Timeouts seguros ($\le 5$ s), degradación elegante y respuestas formateadas en JSON con códigos de estado HTTP estandarizados. |

Fuente: Elaboración propia a partir de los informes y evidencias técnicas de los Sprints 01 al 08.

---

## 5.6. Requisitos de Interfaz Externa

### 5.6.1. Interfaces de Usuario (UI)

La interfaz web del Sistema Web P2P se diseñó como una aplicación de página única (*Single Page Application - SPA*) orientada a proporcionar una experiencia de usuario fluida, reactiva y accesible:
- **Design System y Tokens Visuales:** Implementado mediante Tailwind CSS v3.4+, estructurado sobre la identidad institucional de la Universidad Privada de Tacna.
  - *Colores Principales:* Azul marino institucional (`#1E3A8A` / `bg-blue-900`) para barras de navegación, encabezados principales y botones primarios; dorado universitario (`#D97706` / `text-amber-600`) para distintivos de acreditación, insignias de gamificación y calificaciones; gris pizarra neutro (`#0F172A` / `#F8FAFC`) para tipografía y fondos de lectura descansada.
  - *Tokens Tipográficos:* Familia tipográfica sans-serif moderna (*Inter*, *system-ui*), con escala modular estandarizada (`text-xs` a `text-3xl`) y espaciados consistentes de 4px (sistema base de Tailwind).
- **Accesibilidad Universal (WCAG 2.1 Nivel AA):**
  - Contraste cromático mínimo de $4.5:1$ en todos los textos regulares y $3.0:1$ en elementos gráficos interactivos y textos grandes.
  - Navegación completa por teclado con indicadores de foco visibles (`focus:ring-2 focus:ring-blue-500`) en formularios, modales y tablas.
  - Etiquetas descriptivas `aria-label`, roles semánticos (`role="dialog"`, `role="alert"`) y regiones dinámicas `aria-live` para anuncios de pantalla.
- **Flujos y Componentes Principales:**
  - *LoginOtpView.tsx:* Interfaz de acceso institucional con casillas numéricas de auto-enfoque para los 6 dígitos del código OTP y temporizador de expiración de 5 minutos.
  - *ConsentModalView.tsx:* Diálogo modal accesible que exige la lectura y formalización vinculante del consentimiento bajo la Ley N° 29733.
  - *ProfileAvailabilityView.tsx:* Matriz horaria semanal interactiva de 6 días (Lunes a Sábado) por 11 bloques horarios (08:00 a 20:00) con atajos de selección masiva (*Mañanas*, *Tardes*, *Limpiar*).
  - *RecommendationsView.tsx:* Despliegue de tarjetas de mentores recomendados por el motor *EdRecSys*, con insignias de especialidad, estrellas de reputación y botón de reserva de cupo.
  - *BookingModalView.tsx:* Diálogo de inscripción con visualización en tiempo real de aforos disponibles, selección de modalidad y confirmación de cupo.
  - *QrScannerView.tsx / QrPassView.tsx:* Componente de emisión y escaneo de pases QR dinámicos para marcación de asistencia presencial o virtual.
  - *AdminAnalyticsView.tsx:* Tablero analítico para autoridades de la EPIS-UPT con gráficos de barras, tarjetas de KPIs de retención y filtros por ciclo.

### 5.6.2. Interfaces de Software

- **Servidor Backend y API RESTful:** Desarrollado sobre Python 3.11+ y el framework asíncrono FastAPI. Expone interfaces RESTful versionadas bajo el prefijo `/api/v1/`, documentadas interactivamente mediante especificación OpenAPI v3.0 (Swagger UI en `/docs`).
- **Capa de Persistencia y ORM:** SQLAlchemy v2.0+ con mapeo declarativo fuertemente tipado. Conexión mediante pool de conexiones a la base de datos relacional PostgreSQL v15+ administrada en la nube mediante Supabase.
- **Motor Criptográfico y Seguridad:** Librería `python-jose` para firma y validación de tokens JWT (`HS256`); módulo estándar `secrets` y `hashlib` para generación de códigos OTP numéricos y hashes inmutables SHA-256.
- **Generación Documental Oficial:** Motor `ReportLab` v4.x para compilación programática de expedientes y certificados de horas en formato estándar PDF/A, incorporando códigos QR vectoriales (`qrcode`).
- **Cliente HTTP Frontend:** Adaptador modular `apiClient` configurado con Axios / Fetch API, integrando interceptores automáticos para inyección de cabeceras de autorización Bearer JWT, manejo global de errores HTTP y redirección automática ante expiración de sesiones.

### 5.6.3. Interfaces de Hardware

- **Plataforma Servidora:** Contenedores de ejecución en arquitectura x86_64 o ARM64 sobre infraestructura PaaS (Render / Supabase Cloud), con requerimientos mínimos de 1 núcleo vCPU y 1 GB de memoria RAM para soportar la concurrencia proyectada en la escuela.
- **Dispositivos Clientes:** Estaciones de trabajo personales de los estudiantes, terminales de los laboratorios de cómputo de la EPIS-UPT y dispositivos móviles (smartphones/tablets). Se exige cámara web o cámara trasera para el escaneo del pase QR de asistencia en sesiones presenciales.

### 5.6.4. Interfaces de Comunicaciones y Seguridad de Red

- **Protocolo de Transporte Seguro:** Todo el tráfico entre clientes web y el servidor se transmite estrictamente mediante el protocolo HTTPS protegido con cifrado TLS v1.3 sobre el puerto TCP 443.
- **Políticas de Origen Cruzado (CORS):** Cabeceras restrictivas de control de acceso (*Cross-Origin Resource Sharing*) configuradas en FastAPI para admitir únicamente peticiones originadas desde los dominios institucionales autorizados (`http://localhost:5173` en desarrollo y `https://*.upt.pe` en producción).
- **Seguridad en Tránsito:** Cabeceras Bearer `Authorization: Bearer <token_jwt>` en cada petición privada; payloads y respuestas estructurados exclusivamente en formato `application/json; charset=utf-8`.

---

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
