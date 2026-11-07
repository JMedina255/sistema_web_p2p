**FACULTAD DE INGENIERÍA**  
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
| **2.1** | JCM / RAM | Dr. Ricardo Valcarcel | Dirección EPIS | 19/10/2026 | Refinamiento y trazabilidad en Fase de Diseño (SRS v2.1): alineamiento técnico con la arquitectura desacoplada y cierre de requerimientos del Sprint 1 (RF01, RF05, RNF01, RNF02, RNF09, CUS01, CUS21, RN-01) respaldados empíricamente con 96 pruebas automatizadas en CI. |
| **2.2** | JCM / RAM | Dr. Ricardo Valcarcel | Dirección EPIS | 23/10/2026 | Consolidación de Fase de Diseño y Construcción del Sprint 2 (SRS v2.2): formalización técnica y verificación empírica de Consentimiento digital bajo Ley N° 29733 (RF02, RN-02, CUS01), administración de roles y mérito académico (RF03, RN-03, CUS10), perfiles formativos y matriz de disponibilidad horaria semanal 6×11 (RF04, RNF04, RNF08, CUS15), búsqueda avanzada en catálogo curricular con temarios silábicos (RF05, CUS21) y aislamiento multiusuario con Row Level Security (RNF02), respaldados por 150 pruebas automatizadas sin fallos (>90% de cobertura en frontend y backend). |

# Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT

**Documento de Especificación de Requerimientos de Software**  
**Versión 2.2 — Fase de Diseño Técnico y Trazabilidad de Construcción (Cierre Sprint 2)**

---

## ÍNDICE GENERAL

1. Introducción  
2. Generalidades de la Empresa  
   2.1. Nombre de la Empresa  
   2.2. Visión  
   2.3. Misión  
   2.4. Organigrama  
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
6. Fase de Desarrollo  
   6.1. Perfiles de Usuario y Actores del Sistema  
   6.2. Modelo Conceptual  
   6.2.1. Diagrama de Paquetes Arquitecturales  
   6.2.2. Diagramas de Casos de Uso (General Consolidado y Modulares)  
   6.2.3. Escenarios de Casos de Uso (Narrativas por Módulos MOD-01 al MOD-08)  
   6.3. Modelo Lógico  
   6.3.1. Análisis de Objetos (Modelo ECB)  
   6.3.2. Diagrama de Actividades con Flujo de Objetos  
   6.3.3. Diagrama de Secuencia del Ciclo de Reserva y Quórum  
   6.3.4. Diagrama de Clases del Modelo Lógico  
7. Conclusiones  
8. Bibliografía

---

# Informe de Especificación de Requisitos de Software

# 1. Introducción

El presente documento contiene la especificación de requerimientos de software para el desarrollo del Sistema web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT, 2026.

En el ámbito formativo de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna (EPIS-UPT), los estudiantes de los primeros ciclos (I al IV) se enfrentan a asignaturas críticas o "cursos filtro" como Cálculo, Algoritmos y Estructura de Datos y Programación Orientada a Objetos, las cuales concentran índices significativos de dificultad académica y riesgo de rezago. Paralelamente, la escuela cuenta con estudiantes sobresalientes en los ciclos superiores (VII al X) con la capacidad de brindar orientación pedagógica; sin embargo, esta interacción se produce actualmente mediante canales informales no estructurados y sin ningún tipo de trazabilidad institucional.

Para resolver esta brecha, el equipo de desarrollo C-SharkTeam formula este análisis preliminar para especificar una plataforma web centralizada que automatice el emparejamiento (matching) inteligente entre mentores y mentoreados mediante un algoritmo de recomendación híbrido, gestione la disponibilidad de espacios físicos y virtuales, y facilite la trazabilidad de sesiones y convalidación de horas para la comunidad universitaria.

# 2. Generalidades de la Empresa

## 2.1. Nombre de la Empresa

**C-SharkTeam**

Equipo Consultor y Desarrollador de Soluciones de Software Educativo y Tecnológico.

## 2.2. Visión

Consolidarse como un equipo líder en desarrollo de software educativo, analítica de datos e inteligencia artificial aplicada en el sur del Perú, reconocido por transformar los modelos tradicionales de tutoría y asesoría académica hacia ecosistemas digitales horizontales (Peer-to-Peer), personalizados, eficientes y medibles.

## 2.3. Misión

Diseñar, desarrollar e implementar soluciones de software de alto impacto y base tecnológica, enfocadas en la optimización de procesos de aprendizaje colaborativo, emparejamiento algorítmico inteligente y gobernanza de datos en instituciones de educación superior, facilitando herramientas digitales accesibles, intuitivas y rigurosamente alineadas con los objetivos académicos de la comunidad universitaria.

## 2.4. Organigrama

La estructura organizativa y funcional de C-SharkTeam para el ciclo de vida del proyecto se articula en roles colaborativos de ingeniería de software:

### Organigrama del C-SharkTeam

```plantuml
@startuml
top to bottom direction
skinparam rectangle {
  BackgroundColor white
  BorderColor #555555
}

rectangle "C-SharkTeam\nDirección de Proyecto de TI" as DIR

rectangle "Ingeniería de Backend\ny Algoritmos de IA\nJoan Cristian Medina Q.\n\n• Lógica de Negocio (APIs)\n• Algoritmo Híbrido RecSys\n• Seguridad & Auth (2FA)" as BACK

rectangle "Ingeniería de Frontend\ny Modelado de Datos\nRenzo Antonio Antayhua M.\n\n• Interfaz de Usuario (UI)\n• Experiencia de Uso (UX)\n• Persistencia & Supabase" as FRONT

rectangle "Entorno, Cliente / Beneficiario\n\n• EPIS-UPT\n• Dirección de Escuela y Docentes Tutor\n• Estudiantes Mentores (Ciclos VII-X)\n• Estudiantes Mentoreados (Ciclos I-IV)" as CLIENTE

DIR --> BACK
DIR --> FRONT
BACK --> CLIENTE
FRONT --> CLIENTE
@enduml
```

Fuente: Elaboración propia.

**Área de Backend, Algoritmos e Integraciones:** Liderada por Joan Cristian Medina Quispe, responsable de la arquitectura de servicios RESTful (Python FastAPI), desarrollo y calibración del motor de recomendación híbrido (similitud coseno y filtrado colaborativo), esquemas de autenticación institucional de doble factor (2FA) e integraciones con Google Workspace API y Discord Bot.

**Área de Frontend, Arquitectura de Datos y UX:** Liderada por Renzo Antonio Antayhua Mamani, responsable de la construcción de la aplicación web responsiva (React SPA), gestión de bases de datos PostgreSQL en Supabase, políticas de seguridad a nivel de fila (Row Level Security - RLS) y diseño de tableros interactivos para los perfiles de usuario.

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

Los objetivos de negocio expresan el impacto directo que el software generará en el entorno académico e institucional de la EPIS-UPT:

- **Reducir el índice de rezago y reprobación académica:** Disminuir las tasas de desaprobación en los cursos filtro de I a IV ciclo mediante refuerzos conceptuales oportunos antes de las evaluaciones parciales y finales.
- **Modernizar y descongestionar el servicio de tutoría universitaria:** Cumplir de manera activa el Artículo 40 de la Ley Universitaria N° 30220, transfiriendo las dudas conceptuales básicas a una red horizontal de pares y liberando horas de asesoría docente para casos de mayor complejidad académica.
- **Fomentar la permanencia y retención estudiantil:** Mitigar el riesgo de abandono en los primeros semestres de la carrera de Ingeniería de Sistemas, preservando la continuidad de matrícula institucional.
- **Institucionalizar el reconocimiento al talento estudiantil:** Formalizar la labor de los mentores de ciclos superiores mediante la emisión de certificados de horas extracurriculares convalidables y un sistema de reputación académica visible.
- **Proveer analítica de decisiones para la Dirección de Escuela:** Dotar a la coordinación académica de métricas consolidadas sobre la demanda real de contenidos, asignaturas críticas y niveles de participación estudiantil.

## 3.3. Objetivos de Diseño

Los objetivos de diseño establecen las metas técnicas, funcionales y de experiencia de usuario que la arquitectura del sistema debe garantizar:

- **Precisión y Eficiencia Algorítmica:** Diseñar e implementar un motor de recomendación híbrido (FastAPI / Scikit-learn) capaz de procesar similitud coseno sobre vectores de competencias y filtrado colaborativo con una precisión `Precision@k >= 80%`, ranking `NDCG >= 0.80` y tiempo de respuesta inferior a 500 ms.
- **Alta Usabilidad y Facilidad de Uso:** Construir una interfaz web responsiva (React SPA) con navegación intuitiva que alcance una puntuación media superior a los 75 puntos en la escala estandarizada System Usability Scale (SUS).
- **Seguridad Robusta y Cumplimiento Normativo:** Incorporar autenticación de doble factor (2FA vía Email OTP institucional), control de acceso basado en roles con tokens JWT, políticas de seguridad a nivel de fila (Row Level Security - RLS) en PostgreSQL y un módulo de consentimiento informado digital bajo la Ley N° 29733.
- **Automatización de Infraestructura Física y Virtual:** Proveer integración desacoplada para asignación de espacios físicos (a través de un microservicio parser de horarios en PDF/Excel) y generación automática de salas virtuales (Google Meet API y Bot de gestión en Discord).
- **Trazabilidad Integral y Concurrencia Confiable:** Garantizar transacciones ACID en la persistencia de datos (Supabase) para evitar sobreasignación de cupos y solapamientos de horarios, asegurando un registro fidedigno de bitácoras y encuestas de calidad.

## 3.4. Alcance del proyecto

El alcance del proyecto comprende la especificación, diseño, codificación, integración y despliegue del Sistema web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT, 2026. Habiendo concluido el análisis de prefactibilidad (FD01) y la visión del producto (FD02), el sistema se desarrollará a partir de la matriz de requerimientos del presente documento SRS.

### Inclusiones del Sistema (Módulos a Desarrollar)

- **Plataforma Web Responsiva (Frontend SPA):** Interfaz web accesible mediante navegadores de escritorio en computadoras personales y terminales de los laboratorios de la EPIS-UPT, diseñada bajo React y evaluada para superar los 75 puntos en SUS.
- **Módulo de Identidad, Acceso y Privacidad:** Inicio de sesión institucional con 2FA mediante OTP enviado al correo universitario, consentimiento informado digital bajo la Ley N° 29733 y control de accesos jerárquicos.
- **Motor Híbrido de Recomendación (EdRecSys):** Microservicio en Python (FastAPI) que procesa el vector de necesidades conceptuales del mentoreado frente a las competencias en asignaturas filtro mediante similitud coseno, ajustando el ranking Top-k con filtrado colaborativo, reputación histórica y balance de carga.
- **Gestión de Oferta y Demanda de Mentorías:** Publicación de clases por mentores y formularios de solicitud temática por demanda.
- **Aprovisionamiento de Espacios Físicos y Virtuales:**
  - **Modalidad Presencial:** Componente interno de procesamiento (Parser) para analizar archivos de cronogramas oficiales en PDF/Excel provistos por la Dirección de Escuela y asignar aulas o laboratorios libres, con aforo estándar de 10 estudiantes (RN-05).
  - **Modalidad Virtual:** Integración con Google Workspace API (Google Meet) y bot de Discord para salas de teleconferencia supervisadas, con aforo estándar de 20 estudiantes (RN-05).
- **Control de Quórum y Confirmación de Asistencia:** Confirmación obligatoria hasta 24 horas antes ($T-24\text{ h}$); quórum mínimo reglamentario del 50% (5 alumnos en presencial o 10 en virtual).
- **Trazabilidad, Bitácoras y Retroalimentación:** Registro obligatorio de temas silábicos impartidos, marcado de asistencias reales y encuesta de satisfacción habilitada durante 24 horas.
- **Gamificación y Emisión de Certificados:** Reputación ponderada, catálogo de insignias por mérito formativo, umbrales de horas auditadas y constancias oficiales en PDF con código correlativo único, hash SHA-256 de integridad y código QR de verificación en línea.
- **Panel de Control y Analítica Académica:** Métricas de asignaturas críticas, mentores destacados, tasa de asistencia, demanda insatisfecha y priorización de clases.

### Exclusiones del Alcance (Límites de la Versión Inicial)

- No se desarrollarán aplicaciones móviles nativas para Android o iOS (la plataforma opera como aplicación web responsiva accesible desde cualquier navegador).
- No se incluirán pasarelas de pago monetario ni transacciones financieras (el sistema es estrictamente académico y formativo gratuito).
- No se realizará integración directa ni sincronización en tiempo real con las bases de datos transaccionales centrales de matrícula general de la universidad.
- No se integrará firma digital avanzada basada en certificados PKI emitidos por entidades certificadoras externas de pago; la autenticidad e inalterabilidad de los certificados se gestionará internamente mediante código correlativo institucional único, hash SHA-256 de verificación y validación pública en línea mediante código QR en el portal oficial de la UPT.

## 3.5. Viabilidad del Sistema

### 1. Viabilidad Técnica

**Stack Tecnológico y Madurez:** React (SPA), Python (FastAPI / Scikit-learn) y PostgreSQL administrado mediante Supabase.

**Capacidad Computacional:** El procesamiento matricial para similitud coseno y filtrado colaborativo se ejecutará en contenedores cloud de bajo consumo, garantizando tiempos de respuesta algorítmica `<= 500 ms`.

**Integraciones Desacopladas:** Google Workspace (Meet API), bots de Discord y microservicio parser para cronogramas en PDF/Excel mediante APIs RESTful estructuradas en JSON.

### 2. Viabilidad Económica

El análisis financiero se calculó para un horizonte de evaluación a 5 años (2026-2030) con una tasa de descuento (COK) del 12.00%.

| Indicador Financiero | Valor Proyectado | Interpretación Técnica / Financiera |
|---|---:|---|
| **Inversión Inicial (CAPEX)** | **S/. 5,475.00** | Cubre 500 horas de desarrollo (Joan Medina y Renzo Antayhua a razón de S/. 9.00/hr), depreciación de equipos (3.5 meses), conectividad, dominio web e imprevistos. |
| **Costo Operativo Anual (OPEX)** | **S/. 1,140.00** | Mantenimiento de infraestructura PaaS (Render/Supabase), renovación de dominio, soporte preventivo y materiales de difusión. |
| **Valor Actual Neto (VAN)** | **+S/. 10,801.64** | Estrictamente positivo (VAN > 0), ratificando que el proyecto generará valor económico y retención institucional por encima de la tasa exigida. |
| **Tasa Interna de Retorno (TIR)** | **68.20%** | Supera ampliamente el COK referencial (12.00%), otorgando un margen de seguridad amplio frente a variaciones de costos. |
| **Relación Beneficio / Costo (B/C)** | **1.97** | Por cada sol invertido en el ciclo del proyecto, se generarán S/. 1.97 en beneficios y ahorros valorizados para la facultad y los estudiantes. |
| **Periodo de Recuperación (Payback)** | **1 año y 9.7 meses** | La inversión inicial se recuperará plenamente durante el transcurso del segundo año de operación. |

### 3. Viabilidad Operativa

**Adopción por Mentoreados:** Los alumnos de I a IV ciclo accederán desde cualquier navegador web sin instalaciones locales, permitiéndoles agendar sesiones por tema y modalidad.

**Incentivos para Mentores:** Gamificación, insignias, reputación dinámica y constancias de horas acumuladas convalidables.

**Facilidad Administrativa:** El emparejamiento automatizado reducirá la carga manual de intermediación y proveerá tableros analíticos.

### 4. Viabilidad Legal

**Ley N° 29733:** Consentimiento informado digital en el primer inicio de sesión y uso de UUID para seudonimizar la información académica.

**Ley Universitaria N° 30220 (Artículo 40):** Soporte a la obligación institucional de brindar tutoría y consejería permanente.

**Licenciamiento y Propiedad Intelectual:** Librerías de código abierto bajo licencias permisivas (MIT/Apache 2.0) y registro conforme al reglamento de investigación de la UPT.

### 5. Viabilidad Social y Ambiental

**Factibilidad Social:** Fomento del aprendizaje horizontal P2P, acceso gratuito a asesoría y fortalecimiento de habilidades blandas.

**Factibilidad Ambiental:** Política Paperless y despliegue cloud multi-tenant para optimizar consumo energético.

## 3.6. Información obtenida del Levantamiento de Información

Durante la etapa de análisis, el equipo C-SharkTeam llevó a cabo entrevistas semiestructuradas con los principales actores institucionales, docentes especialistas y autoridades de la EPIS-UPT con el fin de definir las reglas de negocio, la arquitectura del software y los mecanismos de reconocimiento formal del sistema.

### Resumen del Levantamiento de Información

```plantuml
@startuml
top to bottom direction
skinparam rectangle {
  BackgroundColor white
  BorderColor #777777
}

rectangle "1. Ing. Liliana Vega Bernal\nCoordinación de Tutoría EPIS-UPT\n• Trazabilidad en cursos filtro y control de quórum de asistencia\n• Cierre de sesiones mediante bitácora y encuesta de 24 horas" as E1

rectangle "2. Mgtr. Ing. Enrique Lanchipa Valencia\nDocente / Mg. Ing. Software\n• Diseño de arquitectura desacoplada y balance de carga\n• Asignación de espacios físicos (parser) y aprovisionamiento nube" as E2

rectangle "3. Dr. Luis Alfredo Fernandez Vizcarra\nAsesor / Metodólogo\n• Métricas del recomendador: Precision@k, NDCG y cálculo de similitud\n• Cumplimiento normativo de Ley N° 29733 / consentimiento digital" as E3

rectangle "4. Ing. Haydee Raquel Sisa Yataco\nDirectora (e) EPIS-UPT\n• Políticas para la convalidación de horas y créditos académicos\n• Criterios de certificación formal para mentores sobresalientes" as E4

E1 --> E2
E2 --> E3
E3 --> E4
@enduml
```

Fuente: Elaboración propia.

### Entrevista N° 1: Coordinación de Tutoría de la EPIS-UPT

**Entrevistada:** Ing. Liliana Mercedes Milagros Vega Bernal (Encargada de Tutoría EPIS-UPT).  
**Objetivo:** Identificar los cuellos de botella en la atención de alumnos en riesgo académico y fijar los parámetros de trazabilidad y asistencia.

**Registro del Diálogo:**

**C-SharkTeam:** Ingeniera Liliana, ¿cuáles son las principales dificultades que afronta el área de tutoría para brindar soporte a los alumnos de los primeros ciclos?

**Ing. Liliana Vega:** El problema radica en que los estudiantes de I a IV ciclo suelen acudir a tutoría de manera tardía, cuando ya tienen notas desaprobatorias en materias formativas como Cálculo o Algoritmos. Muchos buscan ayuda entre compañeros mayores, pero al ser informal no tenemos forma de registrarlo ni medirlo.

**C-SharkTeam:** ¿Qué requisitos operativos considera necesarios para validar formalmente las sesiones de mentoría?

**Ing. Liliana Vega:** El sistema debe exigir que los alumnos confirmen su asistencia con hasta 24 horas de anticipación para asegurar el quórum. Para dar validez a las horas, el mentor debe registrar los temas dictados y los mentoreados deben completar una encuesta de satisfacción posterior. Además, el panel administrativo debe permitirnos destacar clases prioritarias cuando detectemos asignaturas con alta tasa de reprobación.

### Entrevista N° 2: Asesoría en Arquitectura del Sistema e Infraestructura

**Entrevistado:** Mgtr. Ing. Enrique Felix Lanchipa Valencia (Docente y Maestro en Ingeniería de Software - EPIS-UPT).  
**Objetivo:** Definir las directrices arquitectónicas, el desacoplamiento de servicios y los mecanismos de asignación de espacios físicos y virtuales.

**Registro del Diálogo:**

**C-SharkTeam:** Ingeniero Enrique, desde el punto de vista de la arquitectura de software y la infraestructura disponible en la escuela, ¿cómo debe estructurarse el sistema para soportar las mentorías presenciales y virtuales?

**Mgtr. Enrique Lanchipa:** La arquitectura debe ser desacoplada y basada en microservicios ligeros. Para las clases presenciales, los laboratorios están sujetos a los horarios de cátedra; por lo tanto, el sistema debe conectarse a un API o procesador externo que lea los cronogramas oficiales en PDF o Excel subidos por la administración para identificar franjas libres sin solapamientos. Para las virtuales, el backend debe aprovisionar salas de Google Meet mediante la API institucional o coordinar con un bot en Discord para la asignación de canales.

**C-SharkTeam:** ¿Qué consideraciones arquitectónicas debemos contemplar en el motor de recomendación para la carga de trabajo?

**Mgtr. Enrique Lanchipa:** El motor algorítmico en Python debe optimizarse para responder en milisegundos y no limitarse a ordenar por notas. Es fundamental implementar un balanceo de carga en el ranking para evitar sobrecargar a los mismos mentores y distribuir equitativamente las sesiones entre todos los alumnos habilitados de ciclos superiores.

### Entrevista N° 3: Asesoría Metodológica, Algorítmica y Normativa

**Entrevistado:** Dr. Luis Alfredo Fernandez Vizcarra (Docente Asesor del Curso de Tesis / Metodólogo).  
**Objetivo:** Establecer las métricas de rendimiento algorítmico, el marco experimental de la investigación y la gobernanza de datos bajo el marco legal peruano.

**Dr. Luis Fernandez:** El componente central de la investigación es el algoritmo de recomendación híbrido. Deben garantizarse métricas precisas de evaluación como Precision@k >= 80%, y NDCG >= 0.80, combinando similitud coseno sobre vectores temáticos con filtrado colaborativo. En el plano ético y legal, la plataforma debe acogerse rigurosamente a la Ley N° 29733 de Protección de Datos Personales, solicitando un consentimiento informado digital explícito en el primer inicio de sesión antes de procesar el récord académico del estudiante.

**C-SharkTeam:** ¿Cómo debe validarse la usabilidad de la plataforma frente a los usuarios?

**Dr. Luis Fernandez:** Deben estructurar la evaluación de usabilidad mediante el instrumento psicométrico estandarizado SUS (System Usability Scale), apuntando a una media superior a 75 puntos durante la etapa piloto con los estudiantes.

### Entrevista N° 4: Viabilidad Institucional, Certificación y Convalidación de Créditos

**Entrevistada:** Ing. Haydee Raquel Sisa Yataco (Directora (e) de la Escuela Profesional de Ingeniería de Sistemas - EPIS-UPT).  
**Objetivo:** Establecer los criterios institucionales para la emisión de certificaciones oficiales y analizar la viabilidad de otorgar créditos extracurriculares a mentores destacados.

**Ing. Haydee Sisa:** La Dirección de Escuela ve con mucho interés esta iniciativa, ya que fortalece la retención estudiantil y el trabajo colaborativo. Para incentivar la participación continua de los estudiantes destacados de VII a X ciclo, la escuela puede validar estas horas de asesoría como actividades extracurriculares convalidables, siempre y cuando la plataforma garantice que las horas han sido efectivamente dictadas y evaluadas por los alumnos.

**Ing. Haydee Sisa:** El sistema debe permitir al administrador configurar los umbrales de horas requeridas por semestre y emitir certificados digitales en formato PDF descargables que resuman el récord de mentorías, los temas cubiertos y la calificación de desempeño obtenida. Aquellos mentores con un volumen sobresaliente de horas y alta reputación podrán ser postulados ante el Consejo de Facultad para la asignación de créditos extracurriculares oficiales o reconocimientos al mérito académico.

### Síntesis de Decisiones de Diseño y Reglas Funcionales

- **Acceso y Seguridad:** Autenticación institucional universitaria con doble factor (2FA vía Email OTP) y aceptación obligatoria del consentimiento informado digital bajo la Ley N° 29733.
- **Asignación de Roles:** Todos los alumnos ingresan inicialmente con perfil de "Mentoreado"; el Administrador eleva a "Mentor" según su historial académico.
- **Capacidad y Espacios:** Aforos base de 10 estudiantes en modalidad presencial y 20 en virtual.
- **Quórum y Cancelación:** Confirmación de asistencia hasta 24 horas antes con quórum mínimo del 50%.
- **Trazabilidad y Calidad:** Registro de bitácoras de sesión y encuesta de 1 a 5 estrellas disponible durante 24 horas.
- **Incentivos y Certificación Institucional:** Gamificación, parametrización de horas y generación de constancias digitales PDF.

# 4. Análisis de Procesos

## 4.1. Diagrama del Proceso Actual - Diagrama de actividades

El proceso actual de asesoría académica en la EPIS-UPT opera bajo un esquema informal y desarticulado. Cuando un estudiante de los primeros ciclos (I a IV) afronta vacíos conceptuales en asignaturas críticas (Cálculo, Algoritmos, POO), recurre a grupos no oficiales de mensajería (WhatsApp/Telegram) o contactos personales para buscar ayuda empírica. En este flujo no existen criterios objetivos para evaluar la competencia del compañero que brinda el apoyo, la disponibilidad de espacios físicos o virtuales se coordina sin control, no hay registro de asistencia ni bitácoras pedagógicas, y la Dirección de Escuela carece de métricas para convalidar horas o detectar a tiempo el riesgo académico.

### Diagrama de Actividades del Proceso Actual de Asesoría Académica Informal en la EPIS-UPT

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

El diagrama evidencia que el flujo actual depende de la casualidad y de la red de contactos del alumno, careciendo de mecanismos de emparejamiento por competencias, soporte de espacios y trazabilidad institucional. Esto desincentiva la participación continua de los mentores al no existir convalidación de horas y deja a la escuela sin datos para intervenir de forma preventiva en el rendimiento estudiantil.

## 4.2. Diagrama del Proceso Propuesto - Diagrama de actividades Inicial

El proceso propuesto estructura y automatiza la interacción académica entre pares a través de la plataforma web P2P de la EPIS-UPT. El flujo integra el acceso seguro institucional con doble factor (2FA) y consentimiento digital bajo la Ley N° 29733. Incorpora un motor de recomendación híbrido que evalúa vectores de debilidades y fortalezas en asignaturas filtro, asignación automatizada de recursos, control de quórum con corte a 24 horas, bitácoras de sesión, encuestas de calidad de 24 horas y emisión formal de certificados para convalidación de horas extracurriculares.

### Diagrama de Actividades del Proceso Propuesto - Sistema Web de Mentorías P2P EPIS-UPT

```plantuml
@startuml
|Estudiante / Mentoreado|
start
:Inicia sesión con correo institucional\ny código 2FA (OTP);
if (¿Primer acceso?) then (Sí)
  :Acepta consentimiento informado digital\n(Ley N° 29733);
endif

|Mentor (VII - X Ciclo)|
:Publica oferta de mentoría\n(Tema, Fecha, Modalidad);

|Sistema Web P2P (Backend / RecSys)|
:Asigna espacio físico mediante Parser\nPDF/Excel o Meet/Discord;
:Registra oferta en catálogo de mentorías;
:Ejecuta algoritmo híbrido\n(Similitud Coseno + Filtrado Colaborativo);
:Despliega ranking Top-k ponderado\npor reputación y balance de carga;

|Estudiante / Mentoreado|
:Consulta catálogo o registra formulario\nde solicitud temática;
:Selecciona mentoría y reserva cupo;
:Confirma asistencia obligatoria\nhasta 24 horas antes;

|Sistema Web P2P (Backend / RecSys)|
if (¿Alcanza quórum mínimo del 50%?) then (Sí)
  |Mentor (VII - X Ciclo)|
  :Recibe alerta de quórum listo;
  :Ejecuta clase de mentoría\nen el espacio asignado;
  :Registra bitácora pedagógica\ny marca inasistencias;
else (No)
  |Mentor (VII - X Ciclo)|
  if (¿Decide continuar?) then (Sí)
    :Ejecuta la sesión;
  else (Cancelar)
    |Sistema Web P2P (Backend / RecSys)|
    :Cancela sesión y notifica por correo;
    :Libera aula física o sala virtual;
  endif
endif

|Estudiante / Mentoreado|
:Completa encuesta de calidad\npost-mentoría dentro de 24h;

|Sistema Web P2P (Backend / RecSys)|
:Actualiza score de reputación\ne insignias del mentor;
:Acumula horas efectivas auditadas;

|Administración (Tutoría / Dirección)|
:Supervisa tablero analítico de demanda\ny rendimiento;
if (¿Mentor alcanza umbral parametrizado?) then (Sí)
  :Emite certificado digital PDF\ndescargable para convalidación;
endif
stop
@enduml
```

Fuente: Elaboración propia.

El proceso propuesto transforma la asesoría informal en un flujo trazable, transparente y medible. Asegura un emparejamiento adaptativo mediante inteligencia artificial, garantiza el uso ordenado de la infraestructura física y virtual de la facultad, valida el quórum de forma preventiva y proporciona incentivos institucionales tangibles a los mentores mediante la convalidación de horas.

# 5. Especificación de Requerimientos de Software

## 5.1. Identificación de Módulos y Capacidades Funcionales

Para estructurar la solución de software y garantizar una adecuada cohesión y bajo acoplamiento en el diseño del sistema web P2P de mentorías académicas, el alcance funcional se descompone en ocho módulos o subsistemas especializados. Esta modularización permite organizar la lógica de negocio, delimitar las responsabilidades operativas de los actores institucionales y establecer una base sólida para la posterior definición de los requerimientos funcionales y no funcionales. A continuación, se detallan los módulos identificados, su propósito general dentro de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT), sus capacidades funcionales principales, los actores y sistemas participantes, y su correspondencia con la línea base funcional consolidada de casos de uso (CUS01 al CUS24).

### Cuadro 5.1: Identificación de Módulos y Capacidades Funcionales del Sistema Web P2P

| Código | Módulo / Subsistema | Propósito | Capacidades Funcionales Principales | Actores / Sistemas Involucrados | CUS Asociados |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **MOD-01** | Seguridad, Autenticación y Gobernanza | Garantizar el acceso confiable y restringido a la comunidad universitaria institucional, protegiendo los datos personales y académicos bajo la normativa vigente y asignando privilegios según el rol validado. | • Autenticación institucional con doble factor mediante código de verificación temporal.<br>• Formalización del consentimiento informado digital para el tratamiento de datos académicos (Ley N° 29733).<br>• Gestión y asignación administrativa de roles de usuario (promoción de Mentoreado a Mentor). | Usuario Institucional (*Mentoreado, Mentor, Administrador*), Servicio de Correo SMTP / UPT | CUS01, CUS10 |
| **MOD-02** | Gestión Curricular y Perfiles Académicos | Administrar la estructura curricular de las materias críticas de la carrera y gestionar los perfiles formativos y de disponibilidad de los participantes. | • Gestión del catálogo de asignaturas formativas críticas y desglose de unidades temáticas silábicas.<br>• Registro y actualización de disponibilidad horaria semanal de mentores y mentoreados.<br>• Declaración de debilidades y fortalezas conceptuales para la personalización formativa. | Estudiante Mentoreado, Estudiante Mentor, Administrador (*Tutoría / Dirección EPIS*) | CUS21, CUS15 |
| **MOD-03** | Motor de Recomendación Inteligente (*EdRecSys*) | Generar sugerencias personalizadas de mentores idóneos y articular la oferta formativa con la demanda temática insatisfecha mediante técnicas analíticas. | • Procesamiento analítico de similitud curricular temática y patrones de disponibilidad.<br>• Generación y presentación del ranking de mentores recomendados más afines (Top-k).<br>• Registro de solicitudes temáticas por demanda para materias y temas sin oferta activa. | Estudiante Mentoreado, Estudiantes Mentores habilitados | CUS02, CUS03 |
| **MOD-04** | Planificación, Espacios y Agendamiento | Calendarizar las sesiones de mentoría y gestionar la asignación ordenada de la infraestructura física del campus o salas virtuales de teleconferencia. | • Publicación y configuración de ofertas de mentoría académica en materias aprobadas.<br>• Procesamiento de cronogramas institucionales oficiales para identificar aulas y laboratorios libres.<br>• Aprovisionamiento coordinado de espacios físicos o virtuales (enlaces de videoconferencia).<br>• Gestión de imprevistos mediante reprogramación o cancelación justificada por el mentor. | Estudiante Mentor, Administrador, Servicios Externos (*Google Meet, Discord*) | CUS11, CUS06, CUS18 |
| **MOD-05** | Quórum, Confirmación y Cancelaciones | Controlar la inscripción, reconfirmación de asistencia previa y verificación de viabilidad de las sesiones para optimizar el aprovechamiento de recursos. | • Reserva concurrente de cupos limitados por aforos establecidos.<br>• Reconfirmación obligatoria de asistencia por parte de los inscritos previa al evento.<br>• Despacho automático de alertas temporales y cálculo de quórum mínimo en segundo plano.<br>• Gestión operativa de sesiones con quórum insuficiente bajo decisión del mentor.<br>• Desistimiento voluntario y liberación inmediata de plazas reservadas. | Estudiante Mentoreado, Estudiante Mentor, Sistema (*Servicio Cron / Backend*) | CUS04, CUS24, CUS17, CUS23, CUS07 |
| **MOD-06** | Trazabilidad, Bitácoras y Evaluación | Registrar la evidencia del desarrollo pedagógico, controlar la asistencia efectiva, medir la satisfacción del servicio y gestionar material de apoyo. | • Registro de bitácoras pedagógicas con contenidos impartidos y control estricto de asistencia.<br>• Captura de encuestas de calidad y retroalimentación post-sesión por estudiantes asistentes.<br>• Consulta de historial individual de sesiones, asistencias y evaluaciones para los usuarios.<br>• Intercambio, publicación y descarga de recursos académicos vinculados a cada sesión. | Estudiante Mentoreado, Estudiante Mentor | CUS20, CUS08, CUS05, CUS19 |
| **MOD-07** | Gamificación, Reputación y Certificación | Incentivar la participación continua de los mentores mediante reconocimiento lúdico, cálculo de reputación y formalización de constancias de servicio. | • Cálculo continuo de niveles de reputación y visualización del tablero de insignias del mentor.<br>• Parametrización institucional de horas semestrales requeridas para acreditación.<br>• Emisión y generación digital de certificados de mentoría con código de validación.<br>• Descarga de constancias oficiales de horas para convalidación extracurricular. | Estudiante Mentor, Administrador (*Tutoría / Dirección EPIS*) | CUS16, CUS13, CUS09 |
| **MOD-08** | Supervisión y Analítica Institucional | Proveer herramientas de monitoreo analítico, priorización académica y fiscalización docente para las autoridades de la facultad. | • Despliegue de tableros de analíticas con indicadores de demanda, asistencia y deserción.<br>• Identificación y registro de mentorías prioritarias para asignaturas en riesgo académico.<br>• Auditoría de consistencia y completitud de bitácoras pedagógicas, asistencia y horas declaradas. | Administrador (*Tutoría / Dirección EPIS*) | CUS12, CUS14, CUS22 |

Fuente: Elaboración propia.

La estructuración en estos ocho módulos funcionales responde a la necesidad de separar las responsabilidades del sistema en componentes autónomos, coherentes y de alta cohesión. Cada módulo agrupa capacidades técnicas especializadas que acompañan las etapas progresivas del proceso de acompañamiento entre pares: desde el control de acceso y gobierno de datos (MOD-01) y la modelación curricular (MOD-02), pasando por el emparejamiento adaptativo (MOD-03) y la orquestación logística de espacios y quórum (MOD-04 y MOD-05), hasta la documentación pedagógica (MOD-06), el reconocimiento a los tutores (MOD-07) y la supervisión directiva de la escuela (MOD-08).

Esta división modular constituye el marco de referencia que organiza la posterior definición detallada de los requerimientos funcionales y reglas de negocio en este documento. Al vincular explícitamente cada subsistema con los 24 casos de uso de la línea base funcional consolidada, se asegura que las capacidades del sistema web se mantengan coordinadas e integradas a lo largo de todo el ciclo de vida de la mentoría académica en la EPIS-UPT.

## 5.2. Requerimientos No Funcionales (ISO/IEC 25010)

Los requerimientos no funcionales establecen los atributos de calidad, restricciones técnicas y niveles de servicio que la solución de software debe satisfacer para operar de manera óptima dentro de la infraestructura universitaria. Con el propósito de asegurar que el Sistema Web P2P ofrezca una experiencia confiable, segura, escalable y accesible para la comunidad de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT), los requerimientos se clasifican y estructuran bajo el estándar internacional de calidad del producto de software **ISO/IEC 25010**. A continuación, se presenta la especificación detallada de cada requerimiento no funcional, indicando la característica evaluada, su criterio técnico de aceptación y la métrica verificable exigida.

### Cuadro 5.2: Matriz de Requerimientos No Funcionales bajo el Estándar ISO/IEC 25010

| Código | Característica (ISO 25010) | Requerimiento No Funcional | Criterio de Aceptación / Especificación Técnica | Métrica / Umbral Verificable |
| :---: | :--- | :--- | :--- | :--- |
| **RNF01** | Seguridad | Autenticación multifactor y gestión segura de sesiones | El sistema debe implementar autenticación de doble factor mediante un código de un solo uso (OTP) remitido al correo electrónico institucional con dominio `@upt.pe`. Una vez validado el acceso, la sesión debe gobernarse mediante JSON Web Tokens (JWT) firmados criptográficamente con algoritmo HMAC-SHA256. | Validez máxima del OTP: 5 minutos.<br>Expiración del token JWT: 8 horas continuas. |
| **RNF02** | Seguridad | Privacidad, aislamiento y protección de datos académicos | Todas las comunicaciones deben estar protegidas mediante cifrado TLS 1.3 en tránsito. La persistencia en PostgreSQL (Supabase) debe aplicar políticas de seguridad a nivel de fila (Row Level Security - RLS) para aislar expedientes, kardex y calificaciones, garantizando la anonimización de identificadores directos mediante identificadores universales (UUID v4) en estricto cumplimiento de la Ley N° 29733. | 100% de consultas filtradas por RLS.<br>0% de exposición de códigos de estudiante en tráfico público. |
| **RNF03** | Rendimiento y Eficiencia | Latencia de inferencia del motor de recomendación | El microservicio en Python (FastAPI) debe vectorizar el perfil de necesidades y calcular la similitud coseno frente a los mentores candidatos, aplicando el reordenamiento por filtrado colaborativo en un tiempo imperceptible para el usuario. | Tiempo de procesamiento algorítmico $\le 500$ ms bajo carga concurrente de hasta 50 solicitudes por minuto. |
| **RNF04** | Rendimiento y Eficiencia | Tiempo de respuesta y carga de la interfaz de usuario | La interfaz web React (Single Page Application) debe descargar sus componentes estáticos y renderizar el panel principal de navegación de manera fluida en navegadores de escritorio. | Tiempo de primera pintura con contenido (FCP) $< 2.0$ segundos sobre conexiones de red $\ge 2$ Mbps. |
| **RNF05** | Usabilidad | Facilidad de aprendizaje y satisfacción ergonómica | El diseño visual y los flujos de interacción de la plataforma deben ser intuitivos para estudiantes de ciclos iniciales (I a IV) y avanzados (VII a X), minimizando la curva de aprendizaje sin requerir manuales de inducción complejos. | Puntuación promedio $> 75$ puntos en la escala estandarizada System Usability Scale (SUS) al cierre de la prueba piloto. |
| **RNF06** | Fiabilidad y Disponibilidad | Continuidad operativa durante el periodo académico | La plataforma web, el backend analítico y la base de datos cloud deben mantener operación ininterrumpida a lo largo de las 16 semanas del semestre académico 2026-II, tolerando picos de demanda durante los exámenes parciales y finales. | Nivel de disponibilidad del servicio $\ge 99.0\%$ durante el periodo lectivo regular (excluyendo ventanas de mantenimiento programado). |
| **RNF07** | Fiabilidad e Integridad | Consistencia transaccional en reservas de cupos | El subsistema de persistencia debe ejecutar el bloqueo e inscripción de cupos mediante transacciones ACID con bloqueo optimista/pesimista, garantizando que no existan inconsistencias de sobreasignación ni colisiones de plazas concurrentes. | Tasa de sobreasignación de cupos: estrictamente $0\%$ frente a concurrencia simultánea en el aforo máximo. |
| **RNF08** | Compatibilidad y Portabilidad | Soporte multiplataforma en navegadores de escritorio | La interfaz web debe ser responsiva y garantizar paridad visual y funcional en los navegadores web modernos utilizados en terminales personales y laboratorios de cómputo de la EPIS-UPT (Google Chrome, Mozilla Firefox, Microsoft Edge y Apple Safari). | Renderizado visual y operativo correcto al 100% en resoluciones de pantalla iguales o superiores a $1366 \times 768$ píxeles. |
| **RNF09** | Mantenibilidad | Arquitectura desacoplada basada en microservicios RESTful | El código fuente del frontend (React SPA), backend algorítmico (FastAPI) y capa de persistencia (Supabase / PostgreSQL) debe mantener una separación estricta de responsabilidades, comunicándose mediante interfaces de programación RESTful con contratos JSON fuertemente tipados. | Documentación OpenAPI / Swagger al 100% en todos los endpoints expuestos; cobertura de pruebas unitarias $\ge 70\%$. |
| **RNF10** | Interoperabilidad | Resiliencia ante fallos en servicios externos integrados | El sistema debe implementar políticas de reintento exponencial (*exponential backoff*), degradación elegante y gestión controlada de excepciones frente a indisponibilidades temporales de Google Meet API, Discord API o del servidor de correo SMTP institucional. | Manejo controlado del 100% de tiempos de espera (*timeouts* $\le 5$ s), registrando eventos anómalos en bitácoras de auditoría. |

Fuente: Elaboración propia.

Los requerimientos no funcionales expuestos establecen las salvaguardas técnicas necesarias para garantizar la robustez, agilidad y resiliencia de la solución. La fijación de un tiempo máximo de inferencia de 500 ms para el motor de recomendación híbrido (RNF03) asegura una interacción dinámica e inmediata para los estudiantes, mientras que el umbral superior a los 75 puntos en la escala SUS (RNF05) valida la accesibilidad y ergonomía requeridas para un entorno de pares. Asimismo, el blindaje arquitectónico mediante autenticación 2FA, tokens JWT, cifrado TLS 1.3 y políticas RLS (RNF01 y RNF02) asegura el estricto cumplimiento normativo de la Ley N° 29733, garantizando que el expediente y desempeño académico de los estudiantes de la EPIS-UPT permanezcan permanentemente aislados y protegidos contra accesos no autorizados.

## 5.3. Matriz Consolidada de Requerimientos Funcionales

Habiendo formalizado la modularización del sistema en ocho componentes funcionales (MOD-01 al MOD-08) y establecida la línea base de los 24 casos de uso canónicos (CUS01 al CUS24), la presente sección especifica detalladamente los requerimientos funcionales del software. Cada requerimiento formaliza el comportamiento, las condiciones operativas y las capacidades del sistema que permiten a los actores institucionales —estudiantes mentoreados, estudiantes mentores, autoridades administrativas y servicios automatizados de backend— interactuar eficazmente con la plataforma.

En estricta observancia de las buenas prácticas de ingeniería de requisitos (ISO/IEC/IEEE 29148 e IEEE 830), la relación entre los requerimientos funcionales y los casos de uso responde a un principio de **trazabilidad bidireccional** y no a una correspondencia forzada o biunívoca. Como resultado de la auditoría técnica de atomicidad, necesidad, verificabilidad y separación de responsabilidades (aislando métricas de rendimiento que corresponden a RNF y políticas operativas que corresponden a RN), el sistema consolida **26 requerimientos funcionales atómicos** organizados por módulos funcionales. A continuación, se presenta la matriz consolidada de requerimientos funcionales del sistema.

### Cuadro 5.3: Matriz Consolidada de Requerimientos Funcionales del Sistema Web P2P (RF01 al RF26)

| Código | Módulo Principal | Requerimiento Funcional | Descripción Detallada y Criterios Operativos | Casos de Uso Soportados | Criticidad |
| :---: | :--- | :--- | :--- | :---: | :---: |
| **RF01** | MOD-01 Seguridad, Autenticación y Gobernanza | Autenticación institucional multifactor (2FA) | El sistema debe validar la identidad de los usuarios mediante cuentas de correo institucional `@upt.pe` y la comprobación de un código de verificación temporal de un solo uso (OTP) emitido al buzón institucional. Una vez validada la identidad, el sistema debe inicializar y gobernar la sesión de usuario de acuerdo con el perfil asignado. | CUS01 | Crítica |
| **RF02** | MOD-01 Seguridad, Autenticación y Gobernanza | Formalización del consentimiento informado digital | El sistema debe presentar con carácter obligatorio, en el primer inicio de sesión de cualquier usuario, la política institucional de privacidad y tratamiento de datos personales conforme al marco normativo de la Ley N° 29733. El sistema debe registrar digitalmente la fecha, hora y conformidad expresa del titular para habilitar el uso de su expediente académico en los algoritmos de emparejamiento; de ser rechazado, el sistema debe abortar el proceso e impedir el acceso al software. | CUS01 | Crítica |
| **RF03** | MOD-01 Seguridad, Autenticación y Gobernanza | Gestión y asignación administrativa de roles de usuario | El sistema debe facultar a los usuarios con rol de Administrador (Tutoría / Dirección de Escuela) para consultar el padrón estudiantil, verificar el rendimiento académico y calificaciones en los cursos filtro de los estudiantes de ciclos superiores (VII al X), y promover formalmente su rol de Mentoreado al rol de Mentor, así como suspender o revocar privilegios de mentoría ante faltas normativas o solicitud del usuario. | CUS10 | Alta |
| **RF04** | MOD-02 Gestión Curricular y Perfiles Académicos | Configuración de perfil formativo y matriz de disponibilidad horaria | El sistema debe permitir a mentoreados y mentores configurar su perfil académico complementario mediante la selección de asignaturas críticas de interés, dudas conceptuales o fortalezas curriculares, y el registro interactivo de su agenda semanal de disponibilidad horaria en bloques de una hora, sirviendo como insumo indispensable para el motor de recomendación. | CUS15 | Alta |
| **RF05** | MOD-02 Gestión Curricular y Perfiles Académicos | Gestión del catálogo de asignaturas críticas y temarios silábicos | El sistema debe permitir al Administrador registrar, actualizar y mantener el catálogo oficial de materias formativas críticas de I a IV ciclo (Cálculo I/II, Algoritmos, Estructuras de Datos, Programación Orientada a Objetos) junto con la taxonomía jerárquica de sus unidades temáticas silábicas oficiales, actuando como repositorio único de verdad curricular. | CUS21 | Alta |
| **RF06** | MOD-03 Motor de Recomendación Inteligente (*EdRecSys*) | Inferencia de recomendaciones personalizadas y ranking Top-k | El sistema debe procesar el vector de necesidades conceptuales declarado por el mentoreado frente a las competencias de los mentores mediante similitud coseno sobre espacios vectoriales silábicos. El motor híbrido debe reordenar los candidatos combinando filtrado colaborativo ponderado por la reputación histórica del mentor, su carga activa de sesiones y la coincidencia horaria semanal, presentando una lista ordenada de 3 a 5 mentores recomendados (Top-k). | CUS02 | Crítica |
| **RF07** | MOD-03 Motor de Recomendación Inteligente (*EdRecSys*) | Registro y banco de solicitudes temáticas por demanda | El sistema debe permitir a los estudiantes mentoreados registrar requerimientos de asesoría específicos cuando no existan ofertas activas en el catálogo que coincidan con sus dudas temáticas o disponibilidad horaria. La solicitud debe almacenar la asignatura, unidad temática y observaciones pedagógicas, publicándose en el banco de demanda para que los mentores calificados puedan proponer mentorías dirigidas. | CUS03 | Media |
| **RF08** | MOD-04 Planificación, Espacios y Agendamiento | Publicación y parametrización de ofertas de mentoría académica | El sistema debe permitir a los estudiantes con rol de Mentor programar y publicar ofertas de asesoría en asignaturas críticas previamente aprobadas. El mentor debe seleccionar la asignatura, los contenidos temáticos del sílabo, la fecha, franja horaria y la modalidad pedagógica (presencial o virtual). | CUS06 | Alta |
| **RF09** | MOD-04 Planificación, Espacios y Agendamiento | Aprovisionamiento automatizado de infraestructura y espacios | El sistema debe coordinar la asignación de recintos físicos o virtuales para las mentorías programadas o reprogramadas. En modalidad presencial, debe verificar y reservar aulas o laboratorios libres validados contra el cronograma oficial; en modalidad virtual, debe generar de manera automática y desatendida el enlace de Google Meet o el canal supervisado en Discord mediante interfaces de programación externas. | CUS06, CUS18 | Alta |
| **RF10** | MOD-04 Planificación, Espacios y Agendamiento | Procesamiento de cronogramas institucionales oficiales (Parser de horarios) | El sistema debe permitir al Administrador cargar los archivos oficiales de programación académica de aulas y laboratorios de la EPIS-UPT en formatos estructurados (PDF o Excel). Un componente interno de backend (Parser de horarios) debe procesar el documento, extraer las franjas horarias y recintos ocupados por las clases regulares, y actualizar la base de datos de infraestructura física libre para prevenir solapamientos. | CUS11 | Alta |
| **RF11** | MOD-04 Planificación, Espacios y Agendamiento | Gestión de imprevistos, reprogramación y cancelación de ofertas por el mentor | El sistema debe permitir al mentor modificar la fecha u horario de una sesión programada u optar por su cancelación formal por causas de fuerza mayor debidamente justificadas, con anterioridad al inicio del evento. Ante una reprogramación, el sistema revalida la disponibilidad del nuevo espacio, actualiza el cronograma y notifica a los inscritos; ante una cancelación, notifica a los participantes y libera los recintos asignados. | CUS18 | Alta |
| **RF12** | MOD-05 Quórum, Confirmación y Cancelaciones | Reserva de cupos de mentoría con control de aforo | El sistema debe permitir a los estudiantes mentoreados inscribirse en una sesión de mentoría ofertada bloqueando un cupo individual y registrando la reserva en estado preliminar `PENDIENTE_CONFIRMACION`. El sistema debe impedir nuevas inscripciones cuando el número de reservas alcance la capacidad máxima de aforo parametrizada para la modalidad. | CUS04 | Alta |
| **RF13** | MOD-05 Quórum, Confirmación y Cancelaciones | Confirmación anticipada de asistencia a mentoría | El sistema debe habilitar una interfaz para que los estudiantes mentoreados con reserva en estado `PENDIENTE_CONFIRMACION` ratifiquen formalmente su asistencia a la sesión. Esta capacidad debe estar habilitada desde el momento de la reserva hasta el corte perentorio de 24 horas previas al inicio ($T-24\text{ h}$), transicionando la reserva al estado `CONFIRMADA` para su cómputo formal en el quórum. | CUS24 | Alta |
| **RF14** | MOD-05 Quórum, Confirmación y Cancelaciones | Desistimiento voluntario y liberación anticipada de cupos de reserva | El sistema debe permitir al estudiante mentoreado anular voluntariamente su reserva de cupo siempre que dicha acción se efectúe antes del corte perentorio de 24 horas previas ($T-24\text{ h}$). Al confirmarse el desistimiento, el sistema transiciona la reserva a `CANCELADA_USUARIO`, restituye de inmediato la vacante disponible en el aforo de la oferta y notifica al mentor sobre la modificación en la lista. | CUS17 | Alta |
| **RF15** | MOD-05 Quórum, Confirmación y Cancelaciones | Monitoreo desatendido, emisión de recordatorios y evaluación automática de quórum | Un servicio programado en segundo plano (demonio cron de backend) debe ejecutarse periódicamente para despachar notificaciones automáticas de recordatorio a los estudiantes con confirmación pendiente antes del corte. Al cumplirse exactamente el corte de 24 horas previas ($T-24\text{ h}$), el servicio cierra la ventana de confirmación, revoca las reservas no ratificadas (cambiándolas a `NO_CONFIRMADA` y liberando sus plazas), totaliza los alumnos confirmados y, si no se alcanza el quórum mínimo (50%), transiciona la sesión a `QUORUM_INSUFICIENTE` y notifica al mentor. | CUS23 | Crítica |
| **RF16** | MOD-05 Quórum, Confirmación y Cancelaciones | Gestión resolutiva de sesiones ante quórum insuficiente | El sistema debe proveer una interfaz de decisión para que el Mentor determine la continuidad o cancelación de una sesión cuando reciba la notificación del sistema de quórum deficiente emitida al corte de 24 horas. Si el mentor decide continuar, la sesión queda ratificada para dictarse con los asistentes confirmados; si decide cancelar, la sesión transiciona a `CANCELADA_QUORUM`, notificando a los estudiantes y liberando los espacios asignados. | CUS07 | Alta |
| **RF17** | MOD-06 Trazabilidad, Bitácoras y Evaluación | Registro de bitácora pedagógica y control estricto de asistencia efectiva | El sistema debe proporcionar al mentor un formulario obligatorio para el cierre formal de cada sesión de mentoría. En él se deben detallar los contenidos silábicos desarrollados, observaciones metodológicas y el marcado individual de asistencia efectiva o inasistencia de los alumnos que confirmaron su participación. El guardado transiciona la sesión a estado `FINALIZADA`, habilita la evaluación y acumula las horas dictadas del mentor. | CUS08 | Alta |
| **RF18** | MOD-06 Trazabilidad, Bitácoras y Evaluación | Captura y procesamiento de encuestas de calidad post-mentoría | El sistema debe desplegar un instrumento de evaluación de calidad del servicio accesible exclusivamente para aquellos estudiantes cuya asistencia haya sido validada como efectiva en la bitácora de la sesión. El formulario debe capturar una valoración cuantitativa (escala de 1 a 5 estrellas) y comentarios cualitativos, procesando dichos datos para la reputación docente del mentor. | CUS05 | Alta |
| **RF19** | MOD-06 Trazabilidad, Bitácoras y Evaluación | Consulta de historial cronológico individual de sesiones y asistencias | El sistema debe proveer a cada estudiante una interfaz histórica y cronológica con el registro detallado de todas las sesiones de mentoría en las que haya participado como alumno o dictado como mentor. La vista debe mostrar fechas, temarios tratados, modalidad, condición de asistencia final (`ASISTIDA`, `INASISTENCIA`), accesos a encuestas pendientes y enlaces directos para la descarga de materiales pedagógicos compartidos. | CUS19 | Media |
| **RF20** | MOD-06 Trazabilidad, Bitácoras y Evaluación | Gestión, almacenamiento e intercambio de recursos académicos de sesión | El sistema debe permitir al mentor adjuntar y publicar referencias y enlaces a recursos didácticos de soporte (presentaciones de diapositivas, guías prácticas de laboratorio, problemas resueltos o repositorios de código fuente) vinculados a una sesión creada. Los estudiantes con inscripción confirmada deben poder consultar y descargar dichos materiales educativos antes, durante y después del desarrollo de la clase. | CUS20 | Media |
| **RF21** | MOD-07 Gamificación, Reputación y Certificación | Cálculo dinámico de reputación y visualización del tablero de insignias | El sistema debe calcular y mostrar dinámicamente en el perfil público del Mentor su puntaje acumulado de reputación académica en base al promedio ponderado de las evaluaciones post-sesión, su volumen acumulado de horas dictadas y la puntualidad en el cierre de bitácoras, presentando además un tablero de insignias digitales de reconocimiento para incentivar su compromiso. | CUS16 | Media |
| **RF22** | MOD-07 Gamificación, Reputación y Certificación | Parametrización institucional de umbrales y emisión digital de certificados | El sistema debe permitir al Administrador configurar por periodo lectivo el umbral mínimo de horas de mentoría válidas requeridas para la certificación institucional (ej. 20 horas semestrales). Asimismo, debe permitir autorizar la emisión digital de certificados oficiales en formato PDF para aquellos mentores cuyas bitácoras y registros de asistencia hayan sido auditados y aprobados institucionalmente. | CUS13 | Media |
| **RF23** | MOD-07 Gamificación, Reputación y Certificación | Descarga y verificación institucional de certificados de horas de mentoría | El sistema debe permitir a los mentores calificados descargar su certificado digital formal en formato PDF con refrendo de la Dirección de Escuela. Dicho documento debe incorporar un código hash/alfanumérico único con código QR de verificación institucional para validar su autenticidad física o digital ante la Secretaría Académica de la facultad. | CUS09 | Media |
| **RF24** | MOD-08 Supervisión y Analítica Institucional | Priorización institucional y realce algorítmico de mentorías críticas | El sistema debe permitir al Administrador registrar la condición de "prioritaria" sobre aquellas asignaturas o temarios formativos que presenten contingencias de reprobación académica según los reportes semestrales. Al registrarse dicha condición, el motor de recomendación debe aplicar una bonificación en el ranking Top-k a las ofertas afines y la interfaz debe desplegar un distintivo visual destacado en el catálogo general. | CUS12 | Media |
| **RF25** | MOD-08 Supervisión y Analítica Institucional | Tablero analítico y métricas de rendimiento académico institucional | El sistema debe presentar un panel analítico integral para las autoridades de la EPIS-UPT que consolide métricas agregadas en tiempo real sobre: asignaturas con mayor demanda insatisfecha, tasas de asistencia y ausentismo, evolución de satisfacción docente por mentor, distribución de sesiones físicas vs. virtuales, y horas de acompañamiento acumuladas por ciclo académico. | CUS14 | Alta |
| **RF26** | MOD-08 Supervisión y Analítica Institucional | Auditoría administrativa de bitácoras, asistencia y validación de horas | El sistema debe facultar al Administrador para inspeccionar la consistencia y completitud de las bitácoras pedagógicas registradas por los mentores, confrontando los temas reportados, los horarios efectivos y los reportes de asistencia. El administrador debe poder visar y validar las horas acumuladas para declararlas computables hacia la certificación, o dejarlas en observación si detecta discrepancias documentales. | CUS22 | Alta |

Fuente: Elaboración propia.

La matriz consolidada de 26 requerimientos funcionales culmina la especificación atómica del sistema, logrando tres objetivos fundamentales de diseño de software:
1. **Desacoplamiento Funcional Estricto:** Se dividieron capacidades sobrecargadas como la autenticación frente al consentimiento de privacidad (RF01 y RF02) y la publicación de ofertas frente al aprovisionamiento técnico de espacios físicos/virtuales (RF08 y RF09).
2. **Coherencia Temporal en el Ciclo de Quórum:** Se armonizó el flujo operativo entre la reserva inicial (RF12), la ventana de confirmación abierta al estudiante (RF13), el servicio cron desatendido de recordatorios y corte a $T-24\text{ h}$ (RF15), y la posterior decisión humana del mentor ante quórum insuficiente (RF16).
3. **Pureza Metodológica de Requisitos:** Las descripciones funcionales se despojaron de métricas de rendimiento (como los $\le 500$ ms, trasladados íntegramente a RNF03), restricciones de persistencia (como transacciones ACID, trasladadas a RNF07) y parámetros operativos numéricos (aforos y porcentajes, delegados a las Reglas de Negocio).

## 5.4. Reglas de Negocio Institucionales

Las reglas de negocio constituyen las políticas, directrices institucionales, restricciones operativas y normativas legales que gobiernan el funcionamiento del Sistema Web P2P dentro de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT). Estas disposiciones regulan la admisión y promoción de los actores, la gestión de la infraestructura física y virtual, los protocolos de confirmación de quórum y el tratamiento ético y legal de la información académica bajo la legislación peruana. A continuación, se detalla la matriz de reglas de negocio institucionales, indicando su código canónico, descripción política, módulo impactado y los requerimientos funcionales que aseguran su cumplimiento informático.

### Cuadro 5.4: Matriz de Reglas de Negocio Institucionales del Sistema Web P2P (RN-01 al RN-14)

| Código | Regla de Negocio | Descripción Detallada y Política Operativa | Módulo Afectado | Requerimientos Asociados |
| :---: | :--- | :--- | :--- | :---: |
| **RN-01** | Acceso Institucional Exclusivo y 2FA | Todo acceso a la plataforma exige de forma obligatoria credenciales universitarias válidas pertenecientes al dominio oficial `@upt.pe`. El inicio de sesión requiere la verificación de un código temporal de un solo uso (OTP) enviado al correo electrónico institucional con un tiempo de vida máximo e improrrogable de 5 minutos. No se admiten correos personales ni accesos federados externos fuera de la red UPT. | MOD-01 Seguridad y Autenticación | RF01 |
| **RN-02** | Consentimiento Legal Digital (Ley N° 29733) | En el primer inicio de sesión de cualquier usuario, el sistema debe exigir la aceptación expresa del consentimiento informado digital para el tratamiento de sus datos académicos (kardex, calificaciones y registros de asistencia) con fines estrictos de recomendación y tutoría entre pares. Si el usuario no otorga su consentimiento expreso, la sesión se aborta y se bloquea el acceso a todas las funcionalidades del software. | MOD-01 Seguridad y Gobernanza | RF02 |
| **RN-03** | Jerarquía de Roles y Verificación de Mérito | Todo usuario registrado ingresa inicialmente al sistema con el rol básico de Mentoreado. Para ser promovido al rol de Mentor, el estudiante debe pertenecer obligatoriamente a los ciclos formativos avanzados (VII al X) y haber aprobado las asignaturas críticas objeto de asesoría con una calificación mínima institucional satisfactoria, siendo esta promoción una facultad exclusiva del Administrador previa verificación. | MOD-01 Gobernanza y MOD-02 Perfiles | RF03, RF04 |
| **RN-04** | Dinámica de Oferta/Demanda y Antelación de Publicación | El sistema opera bajo un modelo interactivo bidireccional donde los mentores habilitados publican ofertas formativas en el catálogo y los mentoreados registran solicitudes temáticas por demanda. Para garantizar la viabilidad del ciclo de confirmación previa a la sesión ($T-24\text{ h}$ según RN-08), toda oferta debe publicarse con una antelación mínima obligatoria superior a las 24 horas respecto a su inicio, estableciéndose un estándar institucional recomendado de 48 horas ($T \ge 48\text{ h}$) para permitir la adecuada difusión e indexación en el motor de recomendación. | MOD-03 Recomendador y MOD-04 Agendamiento | RF06, RF07, RF08 |
| **RN-05** | Control Estricto de Aforos Estándar | El aforo de las sesiones de mentoría se encuentra estrictamente delimitado por la modalidad pedagógica elegida: un máximo estándar de 10 participantes para sesiones presenciales (en aulas o laboratorios) y un máximo de 20 participantes para sesiones en modalidad virtual, impidiendo reservas adicionales una vez completada la capacidad asignada. | MOD-05 Quórum y Reservas | RF12 |
| **RN-06** | Asignación Validada de Espacios Físicos (Parser API) | Las mentorías en modalidad presencial solo podrán agendarse en recintos académicos (aulas y laboratorios) y franjas horarias que hayan sido validados como plenamente libres respecto de la carga lectiva regular institucional, determinada mediante el procesamiento automático de los cronogramas oficiales en PDF/Excel provistos por la Dirección de Escuela. | MOD-04 Planificación y Espacios | RF08, RF09, RF10 |
| **RN-07** | Aprovisionamiento Virtual Automatizado | Para las sesiones de mentoría en modalidad virtual, la plataforma debe generar de forma desatendida y automática el enlace de teleconferencia mediante la API de Google Meet o el canal de audio/texto supervisado en el servidor oficial de Discord de la escuela, vinculándolo inmediatamente a la ficha de la clase sin intervención manual externa. | MOD-04 Planificación y Espacios | RF08, RF09 |
| **RN-08** | Ventana de Confirmación de Asistencia hasta $T-24$ Horas | La confirmación de asistencia se encuentra abierta e interactiva para el mentoreado desde el momento en que formaliza su reserva de cupo hasta el corte perentorio de 24 horas previas al inicio de la sesión ($T-24\text{ h}$). Al cumplirse dicho plazo, la ventana de confirmación se cierra automáticamente; las reservas que permanezcan sin ratificar pierden su vigencia por expiración, transicionando a `NO_CONFIRMADA` y liberando sus vacantes. | MOD-05 Quórum y Confirmación | RF13, RF15 |
| **RN-09** | Corte Desatendido y Quórum Mínimo del 50% en $T-24$ Horas | Al corte de 24 horas previas ($T-24\text{ h}$), el sistema desatendido computa los estudiantes con confirmación ratificada. Toda sesión debe alcanzar un quórum mínimo equivalente al 50% del aforo establecido (mínimo 5 confirmados en presencial o 10 en virtual). Si no se alcanza dicho umbral, la sesión transiciona al estado `QUORUM_INSUFICIENTE` y se notifica de inmediato al Mentor, quien posee la atribución exclusiva de continuar excepcionalmente la sesión o proceder a su cancelación formal. | MOD-05 Quórum y Cancelaciones | RF15, RF16 |
| **RN-10** | Cancelación Oportuna y Liberación Inmediata de Recursos | Cuando una sesión es cancelada formalmente (por decisión ante quórum insuficiente, por desistimiento del mentor ante fuerza mayor o por anulación anticipada de cupos), el sistema debe notificar de inmediato a todos los participantes inscritos mediante correo institucional y liberar el aula física o canal virtual reservado para su reasignación inmediata. | MOD-04 Espacios y MOD-05 Cancelaciones | RF11, RF14, RF16 |
| **RN-11** | Criterios de Ponderación y Desempate Algorítmico | El motor de recomendación híbrido (*EdRecSys*) prioriza las coincidencias temáticas mediante el cálculo de similitud coseno vectorial. En caso de empates de afinidad conceptual, el ordenamiento desempata considerando: 1) mayor score de reputación histórica del mentor, 2) menor carga activa de sesiones programadas en la semana, y 3) condición de mentoría prioritaria designada institucionalmente. | MOD-03 Motor de Recomendación | RF06, RF24 |
| **RN-12** | Cierre Formal de Bitácora y Filtro de Evaluación | Al culminar la sesión, el mentor debe diligenciar la bitácora pedagógica reportando los temas silábicos impartidos y registrar obligatoriamente la asistencia efectiva de los confirmados. Aquellos estudiantes que hayan sido marcados como inasistentes quedan inhabilitados de manera definitiva para responder la encuesta de calidad de dicha sesión. | MOD-06 Trazabilidad y Bitácoras | RF17, RF18 |
| **RN-13** | Ventana Temporal Perentoria para Encuestas (24h) | El formulario de evaluación de calidad y satisfacción post-mentoría únicamente se encuentra habilitado para los estudiantes asistentes durante un lapso perentorio de 24 horas posteriores al cierre de la sesión. Una vez transcurrido este tiempo, el sistema cierra la encuesta y procesa las calificaciones recibidas para actualizar la reputación del mentor. | MOD-06 Evaluación y Calidad | RF18, RF21 |
| **RN-14** | Certificación Parametrizada por Horas Auditadas | La emisión de certificados digitales oficiales de horas extracurriculares convalidables para los mentores exige que estos hayan acumulado un número de horas efectivas igual o superior al umbral mínimo semestral configurado por el Administrador (Dirección de Escuela), y que la totalidad de sus bitácoras de sesión hayan sido auditadas y aprobadas institucionalmente. | MOD-07 Certificación y MOD-08 Supervisión | RF22, RF23, RF26 |

Fuente: Elaboración propia.

La formalización de estas catorce reglas de negocio garantiza un marco operativo transparente y riguroso para la comunidad universitaria de la EPIS-UPT:
1. **Seguridad y Garantía de Privacidad:** Las reglas RN-01 y RN-02 establecen barreras estrictas de acceso institucional y cumplimiento normativo vinculante bajo la Ley N° 29733, protegiendo los historiales y el honor académico de los participantes mediante consentimiento informado explícito.
2. **Eficiencia en la Utilización de Recursos:** Las políticas de aforos controlados (RN-05), verificación libre de aulas mediante parser (RN-06), ventana de confirmación cerrada a $T-24\text{ h}$ (RN-08) y umbral de quórum del 50% (RN-09) optimizan la logística universitaria, evitando el bloqueo innecesario de recintos físicos o canales de teleconferencia sin concurrencia real.
3. **Gobernanza Pedagógica y Mérito Estudiantil:** Las directrices sobre el cierre obligatorio de bitácoras (RN-12), la fiscalización administrativa de horas acumuladas (RN-14) y la ponderación algorítmica transparente (RN-11) aseguran que el reconocimiento a los mentores responda a una labor formativa auditable, brindando a la Dirección de Escuela un instrumento fidedigno para la convalidación de créditos extracurriculares.

## 5.5. Matriz de Trazabilidad de Requerimientos

Para garantizar la consistencia global del sistema y verificar que ningún elemento de software quede desarticulado, la presente sección introduce la matriz de trazabilidad bidireccional del Sistema Web P2P. Esta matriz interconecta de manera explícita cada **Requerimiento Funcional (RF)** con su **Módulo de pertenencia**, las **Reglas de Negocio (RN)** que rigen su ejecución, los **Casos de Uso (CUS)** que lo materializan en la interacción de los actores, los **Requerimientos No Funcionales (RNF)** vinculados a su calidad técnica, y el **Método de Verificación Previsto** para su posterior validación en la fase de pruebas del software.

A continuación, se detalla la matriz de trazabilidad multidimensional del sistema.

### Cuadro 5.5: Matriz de Trazabilidad Bidireccional de Requerimientos del Sistema Web P2P

| Código RF | Requerimiento Funcional | Módulo | RN Asociadas | CUS Soportados | RNF Relacionados | Verificación Prevista |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **RF01** | Autenticación institucional multifactor (2FA) | MOD-01 | RN-01 | CUS01 | RNF01, RNF02 | Prueba funcional de autenticación con OTP y expiración de tokens JWT. |
| **RF02** | Formalización del consentimiento informado digital | MOD-01 | RN-02 | CUS01 | RNF02 | Prueba de persistencia legal y bloqueo preventivo ante rechazo de términos. |
| **RF03** | Gestión y asignación administrativa de roles de usuario | MOD-01 | RN-03 | CUS10 | RNF02, RNF09 | Inspección funcional de actualización de privilegios de Mentoreado a Mentor. |
| **RF04** | Configuración de perfil formativo y matriz horaria | MOD-02 | RN-03 | CUS15 | RNF04, RNF08 | Prueba de UI de matriz semanal interactiva y persistencia de competencias. |
| **RF05** | Gestión del catálogo de asignaturas y temarios | MOD-02 | — | CUS21 | RNF09 | Prueba de operaciones CRUD sobre jerarquías de cursos filtro y unidades silábicas. |
| **RF06** | Inferencia de recomendaciones y ranking Top-k | MOD-03 | RN-04, RN-11 | CUS02 | RNF03 | Prueba algorítmica de precisión (`Precision@k`, `NDCG`) y latencia $\le 500$ ms. |
| **RF07** | Registro y banco de solicitudes por demanda | MOD-03 | RN-04 | CUS03 | RNF04, RNF09 | Prueba funcional de registro temático y visibilidad en catálogo de demanda. |
| **RF08** | Publicación y parametrización de ofertas de mentoría | MOD-04 | RN-04, RN-05 | CUS06 | RNF04, RNF09 | Prueba de validación de prerrequisitos docentes y creación de oferta. |
| **RF09** | Aprovisionamiento automatizado de infraestructura | MOD-04 | RN-06, RN-07 | CUS06, CUS18 | RNF10 | Prueba de integración con Meet API, Discord Bot y asignación de aulas. |
| **RF10** | Procesamiento de cronogramas (Parser de horarios) | MOD-04 | RN-06 | CUS11 | RNF09, RNF10 | Prueba de extracción de celdas libres en archivos PDF y hojas Excel. |
| **RF11** | Gestión de imprevistos, reprogramación y cancelación | MOD-04 | RN-10 | CUS18 | RNF09, RNF10 | Prueba funcional de actualización de cronograma y despacho de alertas. |
| **RF12** | Reserva de cupos con control de aforo | MOD-05 | RN-05 | CUS04 | RNF07 | Prueba de concurrencia y estrés para verificar $0\%$ de sobreasignación de cupos. |
| **RF13** | Confirmación anticipada de asistencia (hasta $T-24\text{ h}$) | MOD-05 | RN-08 | CUS24 | RNF07, RNF09 | Prueba de transición de estados `PENDIENTE` a `CONFIRMADA` dentro de la ventana. |
| **RF14** | Desistimiento voluntario y liberación anticipada de cupos | MOD-05 | RN-08, RN-10 | CUS17 | RNF07 | Prueba funcional de anulación previa al corte y restitución en aforo. |
| **RF15** | Monitoreo desatendido, alertas y quórum en $T-24\text{ h}$ | MOD-05 | RN-08, RN-09 | CUS23 | RNF06, RNF09 | Prueba de ejecución programada de servicio cron, corte temporal y cálculo de quórum. |
| **RF16** | Gestión resolutiva ante quórum insuficiente | MOD-05 | RN-09, RN-10 | CUS07 | RNF09, RNF10 | Prueba de interfaz de decisión del mentor (continuar excepcional vs. cancelar). |
| **RF17** | Registro de bitácora y control de asistencia efectiva | MOD-06 | RN-12 | CUS08 | RNF02, RNF09 | Prueba funcional de cierre de sesión y marcado obligatorio de asistencias. |
| **RF18** | Captura de encuestas de calidad post-mentoría | MOD-06 | RN-12, RN-13 | CUS05 | RNF05, RNF09 | Prueba de validación de formulario (1-5 estrellas) y corte temporal a 24 horas. |
| **RF19** | Consulta de historial de sesiones y asistencias | MOD-06 | — | CUS19 | RNF02, RNF04 | Prueba de interfaz con filtros cronológicos y aislamiento de datos por usuario. |
| **RF20** | Gestión e intercambio de recursos académicos | MOD-06 | — | CUS20 | RNF02, RNF09 | Prueba funcional de subida de enlaces y descarga restringida a participantes. |
| **RF21** | Cálculo dinámico de reputación y tablero de insignias | MOD-07 | RN-13 | CUS16 | RNF05, RNF09 | Prueba de recálculo matemático de reputación y renderizado de insignias. |
| **RF22** | Parametrización de umbrales y emisión de certificados | MOD-07 | RN-14 | CUS13 | RNF09 | Prueba de configuración de horas mínimas y generación batch de documentos PDF. |
| **RF23** | Descarga y verificación institucional de certificados | MOD-07 | RN-14 | CUS09 | RNF02, RNF09 | Prueba de validación de código hash criptográfico y escaneo de código QR. |
| **RF24** | Priorización institucional de mentorías críticas | MOD-08 | RN-11 | CUS12 | RNF03, RNF05 | Prueba de bonificación algorítmica y despliegue de distintivo en catálogo. |
| **RF25** | Tablero analítico y métricas de rendimiento | MOD-08 | — | CUS14 | RNF02, RNF04 | Prueba de consolidación de indicadores agregados y anonimización de datos. |
| **RF26** | Auditoría administrativa de bitácoras y horas | MOD-08 | RN-14 | CUS22 | RNF02, RNF09 | Prueba de flujo de visado y formulación de observaciones sobre horas declaradas. |

Fuente: Elaboración propia.

La matriz de trazabilidad bidireccional demuestra que el modelo de requisitos de la EPIS-UPT presenta consistencia lógica y articulación integral:
1. **Ausencia de Requisitos Huérfanos:** Cada uno de los 26 requerimientos funcionales está respaldado por al menos una regla de negocio o caso de uso del sistema, y cuenta con un método de verificación formal explícito para su futura validación en la fase de pruebas (FASE 4).
2. **Cobertura Total de Casos de Uso:** Todos los casos de uso consolidados (CUS01 al CUS24) disponen de las capacidades funcionales necesarias para su ejecución, eliminando vacíos conceptuales que pudieran retrasar la fase de construcción.
3. **Alineamiento con Atributos de Calidad (ISO/IEC 25010):** Se formaliza cómo las políticas de seguridad (RNF01, RNF02), el rendimiento algorítmico (RNF03), la usabilidad ergonómica (RNF05) y la consistencia transaccional (RNF07) impactan de manera directa en cada componente funcional del software.

### Cuadro 5.6: Estado de Verificación y Madurez de Requerimientos en Fase de Diseño y Construcción (Sprints 1 y 2)

A continuación, se documenta el estado de implementación y verificación empírica de los requerimientos abordados al cierre del Sprint 2:

| Código | Requerimiento Funcional / No Funcional | Sprint de Construcción | Estado Técnico Actual | Evidencia Empírica de Verificación |
| :---: | :--- | :---: | :---: | :--- |
| **RF01** | Autenticación institucional multifactor (2FA) | Sprint 1 | **Construido y Verificado** ✅ | Flujo OTP con correo `@upt.pe`, cooldown 60 s, expiración 5 min y token JWT 8 h (13 pruebas Pytest / 15 pruebas Vitest). |
| **RF02** | Formalización del consentimiento informado digital | Sprint 2 | **Construido y Verificado** ✅ | Modal accesible bajo Ley N° 29733 (`ConsentModalView.tsx`), marcas UTC e IP en BD (`consentimientos_legales`) y bloqueo perentorio RN-02 (9 tests Vitest / 5 tests Pytest). |
| **RF03** | Gestión y asignación administrativa de roles de usuario | Sprint 2 | **Construido y Verificado** ✅ | Asignación de rol `mentoreado`, verificación estricta de mérito académico RN-03 (`ciclo >= 7`) y bloqueo de autopromoción (7 tests Pytest). |
| **RF04** | Configuración de perfil formativo y matriz horaria | Sprint 2 | **Construido y Verificado** ✅ | Vista `ProfileAvailabilityView.tsx`, matriz semanal 6×11 (08:00 a 20:00), reemplazo atómico en BD y validación de mérito en cliente (10 tests Vitest / 11 tests Pytest). |
| **RF05** | Gestión del catálogo de asignaturas y temarios | Sprints 1 y 2 | **Construido y Verificado** ✅ | 5 materias filtro formativas en PostgreSQL, buscador reactivo en tiempo real y exploración profunda de unidades silábicas (4 tests Vitest / 8 tests Pytest). |
| **RNF01**| Seguridad: Autenticación multifactor y tokens JWT | Sprint 1 | **Construido y Verificado** ✅ | Tokens JWT HS256 con vigencia de 480 min (8 horas) e invalidación atómica de códigos previos. |
| **RNF02**| Seguridad: Privacidad, aislamiento y protección RLS | Sprints 1 y 2 | **Construido y Verificado** ✅ | Row Level Security activo en 8 tablas PostgreSQL/Supabase, denegación de acceso cruzado (HTTP 403) y 0% fuga de credenciales. |
| **RNF04**| Rendimiento: Granularidad horaria y tiempos de carga | Sprint 2 | **Construido y Verificado** ✅ | Bloques horarios estrictos de 1 hora y renderizado fluido sin latencias perceptibles. |
| **RNF08**| Ergonomía y compatibilidad multiplataforma | Sprint 2 | **Construido y Verificado** ✅ | Atajos de selección masiva en matriz semanal (*Mañanas*, *Tardes*, *Limpiar*), diseño accesible y responsivo. |
| **RNF09**| Calidad y cobertura de pruebas unitarias ($\ge 70\%$) | Sprints 1 y 2 | **Construido y Verificado** ✅ | **150 pruebas automatizadas sin fallos (84 backend / 66 frontend)** con cobertura superior al **90%** en ambas capas. |

Fuente: Elaboración propia a partir de `docs/diseño/INFORME_GENERAL_SPRINT_02.md` y `docs/diseño/EVIDENCIA_PRUEBAS_SPRINT_02.md`.

El Cuadro 5.6 acredita que la línea base de requerimientos de los Módulos MOD-01 y MOD-02 se encuentra plenamente satisfecha en la fase de construcción, proporcionando la base de datos, los roles de usuario y las agendas horarias requeridas para acometer los algoritmos de recomendación del Sprint 3.

# 6. Fase de Desarrollo

El ciclo de vida del proyecto adopta formalmente la metodología UWE (*UML-Based Web Engineering*) orientada a aplicaciones web adaptativas e interactivas. La ejecución se distribuye a lo largo de un periodo intensivo de 15.5 semanas (108 días calendario) correspondientes al semestre académico 2026-II (del 29 de agosto al 14 de diciembre de 2026). La metodología UWE estructura el proceso de desarrollo en cinco fases secuenciales e iterativas que guían desde la formalización rigurosa de los requerimientos y el consentimiento legal, hasta el despliegue cloud y la evaluación empírica de usabilidad y desempeño en la EPIS-UPT.

### Diagrama 6.1: Fases del Ciclo de Vida del Desarrollo de Software (Metodología UWE - Semestre 2026-II)

```plantuml
@startuml
title Fases de Desarrollo del Sistema Web P2P (Metodología UWE - 2026-II)
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
:FASE 1: Especificación de Requisitos y Modelado Inicial\nSemanas 1-3: 29 Ago - 19 Set\n• Levantamiento de información y entrevistas semiestructuradas\n• Definición de requerimientos funcionales (RF01-RF26) y no funcionales (ISO 25010)\n• Protocolo formal de Consentimiento Legal Digital (Ley N° 29733);
:FASE 2: Diseño del Sistema y Modelado de Datos\nSemanas 4-6: 20 Set - 10 Oct\n• Arquitectura en capas desacopladas y diseño modular (MOD-01 al MOD-08)\n• Modelado relacional PostgreSQL (Supabase) y políticas RLS\n• Prototipos de alta fidelidad en React SPA y diseño de navegación UWE;
:FASE 3: Codificación del Software y Motor Algorítmico\nSemanas 7-11: 11 Oct - 14 Nov\n• Microservicios RESTful en Python (FastAPI)\n• Motor híbrido de recomendación (Similitud Coseno + Filtrado Colaborativo)\n• Integraciones de servicios: Google Meet API, Bot Discord y Parser de Horarios;
:FASE 4: Pruebas, Validación y Evaluación de Usabilidad\nSemanas 12-14: 15 Nov - 05 Dic\n• Pruebas unitarias, de integración y pruebas de concurrencia de cupos\n• Calibración analítica algorítmica (Precision@k, NDCG >= 0.80)\n• Evaluación estandarizada de usabilidad mediante escala SUS (> 75 puntos);
:FASE 5: Despliegue Cloud, Piloto Institucional y Cierre\nSemanas 15-16: 06 Dic - 14 Dic\n• Despliegue en producción sobre infraestructura PaaS (Render / Supabase)\n• Ejecución de prueba piloto con estudiantes reales de I a X ciclo de la EPIS\n• Consolidación de métricas finales e informe de investigación aplicada;
:14 Dic 2026;
stop
@enduml
```

Fuente: Elaboración propia.

El enfoque metodológico UWE permite abordar de manera sistemática la complejidad propia de las aplicaciones web educativas y adaptativas. Al articular fases tempranas de requisitos con etapas avanzadas de modelado conceptual, navegacional y algorítmico, permite que la solución responda a las directrices pedagógicas de la universidad y a los estándares de rendimiento técnico requeridos.

---

## 6.1. Perfiles de Usuario

### Presentación de los Perfiles de Usuario
La operación eficiente y ordenada del Sistema Web P2P requiere la definición explícita de los perfiles de usuario y actores que interactúan en la plataforma. En el ecosistema formativo de la Escuela Profesional de Ingeniería de Sistemas (EPIS-UPT), los usuarios desempeñan roles diferenciados según su nivel de avance curricular, su investidura institucional o la naturaleza técnica de sus procesos. Con el fin de gobernar el acceso, garantizar el principio de mínimo privilegio y resguardar la integridad de los datos académicos bajo la Ley N° 29733, se establecen los perfiles de usuario humanos y los actores técnicos automatizados del sistema. A continuación, se presenta la matriz descriptiva de los perfiles identificados.

### Cuadro 6.1: Perfiles de Usuario y Actores del Sistema Web P2P

| Perfil / Actor | Tipo de Actor | Población Objetivo / Componente | Responsabilidades y Actividades Principales | Privilegios y Permisos en el Sistema |
| :--- | :--- | :--- | :--- | :--- |
| **Estudiante Mentoreado** | Humano (Actor Primario) | Estudiantes matriculados de I a IV ciclo con necesidades de reforzamiento académico en materias críticas (*Cálculo I/II, Algoritmos, Estructuras de Datos, POO*). | • Formalizar el consentimiento informado digital (Ley N° 29733).<br>• Declarar áreas de dificultad temática y disponibilidad horaria semanal.<br>• Consultar recomendaciones personalizadas (Top-k) y explorar el catálogo.<br>• Reservar cupos de mentoría y registrar solicitudes por demanda.<br>• Confirmar asistencia obligatoria hasta $T-24\text{ h}$ o desistir oportunamente.<br>• Responder encuestas de satisfacción dentro de las 24 horas posteriores. | • Acceso a vistas de catálogo y recomendador personal.<br>• Gestión de reservas propias (creación, confirmación, cancelación).<br>• Registro en banco de demandas formativas.<br>• Descarga de materiales de sesiones en las que participó.<br>• Diligenciamiento de encuestas de calidad asignadas. |
| **Estudiante Mentor** | Humano (Actor Primario) | Estudiantes de rendimiento sobresaliente de VII a X ciclo promovidos formalmente por la Dirección de Escuela. | • Configurar áreas de dominio curricular y agenda de disponibilidad.<br>• Programar y publicar ofertas de mentoría académica (temario, modalidad).<br>• Resolver la continuidad o cancelación ante alertas de quórum deficiente.<br>• Dictar sesiones y gestionar imprevistos por causa mayor debidamente justificada.<br>• Registrar bitácoras pedagógicas y reporte obligatorio de asistencia efectiva.<br>• Compartir recursos didácticos y monitorear insignias/reputación obtenida.<br>• Descargar certificados oficiales de horas para convalidación extracurricular. | • Creación, edición, reprogramación y anulación de ofertas propias.<br>• Aprovisionamiento guiado de infraestructura física o virtual.<br>• Diligenciamiento y cierre de bitácoras de sesión.<br>• Carga de materiales y enlaces académicos para sus alumnos.<br>• Visualización de métricas personales de reputación y descarga de certificados PDF auditados. |
| **Administrador Institucional** | Humano (Gobernanza y Supervisión) | Comité de Tutoría Docente, Coordinación Académica y Dirección de la EPIS-UPT. | • Auditar expedientes estudiantiles y aprobar la promoción a rol de Mentor.<br>• Mantener actualizado el catálogo de asignaturas críticas y temarios silábicos.<br>• Cargar cronogramas oficiales de aulas/laboratorios para su procesamiento por el parser interno.<br>• Registrar materias y mentorías en condición prioritaria por reprobación.<br>• Fiscalizar bitácoras pedagógicas, asistencias y computabilidad de horas.<br>• Parametrizar umbrales semestrales y emitir certificados oficiales PDF.<br>• Supervisar tableros analíticos de demanda, ausentismo y desempeño docente. | • Control de acceso total y gestión jerárquica de roles.<br>• Operaciones CRUD sobre asignaturas, temarios y prioridades académicas.<br>• Carga e indexación de archivos de horarios institucionales.<br>• Visado, observación y validación de horas de mentoría.<br>• Generación masiva/individual de certificados digitales.<br>• Acceso irrestricto al panel de analítica institucional. |
| **Servicio Cron / Backend** | Técnico (Proceso Desatendido) | Demonio de tareas programadas en el servidor backend FastAPI. | • Inspeccionar periódicamente la base de datos para identificar sesiones próximas.<br>• Despachar notificaciones automáticas y recordatorios a inscritos.<br>• Ejecutar el corte perentorio a $T-24\text{ h}$, revocar cupos no confirmados y computar quórum.<br>• Transicionar el estado de sesiones que no alcancen el 50% de aforo y alertar al Mentor. | • Ejecución en segundo plano con privilegios a nivel de servicio de sistema.<br>• Modificación automatizada de estados en tablas de reservas y sesiones.<br>• Invocación de microservicios de mensajería y correo SMTP institucional. |
| **Servicios Externos** | Técnico (Sistemas Colaboradores) | Plataformas de infraestructura de terceros: Google Meet API, Bot de Discord y Servidor de Correo SMTP UPT. | • Recibir solicitudes de aprovisionamiento de videollamadas y canales de voz.<br>• Retornar credenciales de acceso, enlaces dinámicos y confirmaciones de sala.<br>• Despachar notificaciones y códigos de verificación OTP mediante la infraestructura de correo de la UPT. | • Respuestas seguras a endpoints REST autenticados mediante tokens de servicio.<br>• Sin acceso directo a datos académicos sensibles de estudiantes. |

Fuente: Elaboración propia.

La estructuración de perfiles y actores formalizada en el cuadro anterior consolida una clara separación de responsabilidades operativas. Los mentoreados y mentores constituyen los agentes esenciales del aprendizaje colaborativo horizontal, disponiendo de herramientas diseñadas para agilizar la interacción académica sin fricciones burocráticas. Por su parte, el rol de Administrador centraliza la supervisión institucional y la salvaguarda de la calidad pedagógica, asegurando que la acumulación de horas responda a sesiones auditadas. Finalmente, la formalización del Servicio Cron y los Servicios Externos como actores técnicos permite que los procesos temporales y las integraciones de infraestructura operen con autonomía y alta disponibilidad.

---

## 6.2. Modelo Conceptual

### Presentación del Modelo Conceptual
El modelo conceptual formaliza las entidades fundamentales del dominio del problema, capturando sus atributos esenciales, estados operacionales y las relaciones semánticas que sustentan el ecosistema de mentorías académicas en la EPIS-UPT. Este modelo traduce las reglas de negocio institucionales (aforos máximos, consentimiento de privacidad bajo la Ley N° 29733, estados de reserva, bitácoras de cumplimiento y certificación) en una estructura ontológica coherente y extensible, orientada a guiar el posterior diseño de bases de datos relacionales en PostgreSQL (Supabase). A continuación, se presenta el diagrama de clases conceptuales del dominio.

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
  +consentimiento_ley29733: Boolean
  +fecha_consentimiento: DateTime
  +estado_activo: Boolean
}

class Rol {
  +id_rol: Integer
  +nombre_rol: String
  +descripcion: String
}

class AsignaturaFiltro {
  +id_asignatura: Integer
  +codigo_curso: String
  +nombre_curso: String
  +ciclo: Integer
  +es_prioritaria: Boolean
}

class TemaConceptual {
  +id_tema: Integer
  +nombre_tema: String
  +descripcion_silabo: String
}

class OfertaMentoria {
  +id_oferta: UUID
  +fecha_sesion: Date
  +hora_inicio: Time
  +hora_fin: Time
  +modalidad: ModalidadEnum
  +aforo_maximo: Integer
  +estado_sesion: EstadoSesionEnum
}

class ReservaCupo {
  +id_reserva: UUID
  +fecha_reserva: DateTime
  +fecha_confirmacion: DateTime
  +estado_reserva: EstadoReservaEnum
  +asistio_efectivamente: Boolean
}

class EspacioFisico {
  +id_espacio: Integer
  +codigo_aula: String
  +pabellon: String
  +capacidad: Integer
}

class EspacioVirtual {
  +id_virtual: Integer
  +plataforma: PlataformaEnum
  +url_reunion_meet: String
  +canal_discord_id: String
}

class BitacoraSesion {
  +id_bitacora: UUID
  +temas_tratados: String
  +observaciones_mentor: String
  +total_asistentes_reales: Integer
  +fecha_cierre: DateTime
  +horas_validadas_admin: Boolean
}

class EncuestaCalificacion {
  +id_encuesta: UUID
  +puntuacion_estrellas: Integer
  +comentario_retroalimentacion: String
  +fecha_envio: DateTime
}

class SolicitudDemanda {
  +id_demanda: UUID
  +descripcion_necesidad: String
  +franja_horaria_preferida: String
  +fecha_registro: DateTime
  +estado_atendida: Boolean
}

class ReputacionGamificacion {
  +id_reputacion: UUID
  +score_promedio: Float
  +total_horas_auditadas: Integer
  +nivel_insignia: String
}

class CertificadoMentor {
  +id_certificado: UUID
  +codigo_verificacion: String
  +total_horas_validadas: Integer
  +fecha_emision: Date
  +ruta_pdf: String
}

' Relaciones y Multiplicidades
Usuario "1" -- "1..*" Rol : asignado a
Usuario "1" -- "0..*" OfertaMentoria : publica como Mentor
Usuario "1" -- "0..*" ReservaCupo : inscribe como Mentoreado
OfertaMentoria "1" -- "0..*" ReservaCupo : contiene participantes
OfertaMentoria "0..1" -- "1" EspacioVirtual : aprovisiona Meet/Discord
OfertaMentoria "0..1" -- "1" EspacioFisico : asigna mediante Parser
OfertaMentoria "1" -- "1" AsignaturaFiltro : pertenece a
OfertaMentoria "1" -- "0..1" BitacoraSesion : documenta cierre
AsignaturaFiltro "1" -- "1..*" TemaConceptual : desglosa en
ReservaCupo "1" -- "0..1" EncuestaCalificacion : evalúa calidad (24h)
EncuestaCalificacion "1..*" -- "1" ReputacionGamificacion : recalcula score
Usuario "1" -- "0..*" SolicitudDemanda : formula necesidad
AsignaturaFiltro "1" -- "0..*" SolicitudDemanda : clasifica demanda
Usuario "1" -- "0..1" ReputacionGamificacion : acumula progreso
Usuario "1" -- "0..*" CertificadoMentor : emite y recibe
@enduml
```

Fuente: Elaboración propia.

El análisis del modelo conceptual pone de relieve la integridad estructural del dominio académico de la EPIS-UPT:
1. **Desacoplamiento Espacial:** Se modelan de manera diferenciada las clases `EspacioFisico` y `EspacioVirtual`, permitiendo que la clase `OfertaMentoria` asocie dinámicamente un aula validada mediante el parser institucional o un enlace de teleconferencia provisto por APIs externas.
2. **Ciclo de Vida de Reservas y Quórum:** La entidad `ReservaCupo` encapsula estados explícitos (`PENDIENTE_CONFIRMACION`, `CONFIRMADA`, `CANCELADA_USUARIO`, `NO_CONFIRMADA`) que permiten gobernar con precisión matemática el cómputo del 50% de quórum previo al inicio de la sesión.
3. **Trazabilidad Pedagógica y de Certificación:** La conexión secuencial entre `OfertaMentoria`, `BitacoraSesion`, `EncuestaCalificacion`, `ReputacionGamificacion` y `CertificadoMentor` asegura que ningún crédito ni constancia de horas se emita sin el respaldo verificable de una bitácora auditada y la evaluación efectiva de los participantes.

---

### 6.2.1. Diagrama de Paquetes Arquitecturales

### Presentación del Diagrama de Paquetes
Para asegurar una arquitectura modular, extensible y de bajo acoplamiento conforme a las directrices de ingeniería web UWE, el software se organiza mediante una jerarquía de paquetes estructurada en capas arquitecturales. Esta organización delimita estrictamente la presentación interactiva en el cliente, la orquestación de servicios en el servidor FastAPI, el motor de recomendación matricial, la persistencia protegida bajo políticas de seguridad en Supabase y los adaptadores de integración con sistemas externos. A continuación, se presenta el diagrama de paquetes arquitecturales del sistema.

### Diagrama 6.3: Diagrama de Paquetes Arquitecturales y Subsistemas del Sistema Web P2P

```plantuml
@startuml
title Diagrama de Paquetes Arquitecturales del Sistema Web P2P EPIS-UPT
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam package {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
}

package "Capa de Presentación (Frontend React SPA)" {
  [PKG-UI-01: Autenticación, Acceso & Consentimiento Legal]
  [PKG-UI-02: Perfil Académico & Disponibilidad Horaria]
  [PKG-UI-03: Catálogo, Búsqueda & Recomendaciones Top-k]
  [PKG-UI-04: Planificación, Ofertas & Aprovisionamiento]
  [PKG-UI-05: Reservas, Confirmaciones & Gestión de Quórum]
  [PKG-UI-06: Bitácoras de Sesión, Asistencia & Encuestas]
  [PKG-UI-07: Tablero de Insignias, Reputación & Certificados]
  [PKG-UI-08: Tablero Analítico & Auditoría de Dirección]
}

package "Capa de Negocio y Lógica de Dominio (FastAPI RESTful Backend)" {
  [PKG-SRV-01: Servicio de Seguridad, JWT & Roles]
  [PKG-SRV-02: Servicio Curricular & Temarios]
  [PKG-SRV-03: Motor Recomendador Inteligente (EdRecSys)]
  [PKG-SRV-04: Servicio de Agendamiento, Espacios & Parser Interno]
  [PKG-SRV-05: Servicio de Quórum, Cancelaciones & Cron]
  [PKG-SRV-06: Servicio de Trazabilidad, Bitácoras & Evaluación]
  [PKG-SRV-07: Servicio de Gamificación & Emisión de PDFs]
  [PKG-SRV-08: Servicio de Analítica Académica & Priorización]
}

package "Capa de Persistencia Segura y Almacenamiento (Supabase / PostgreSQL)" {
  database "PostgreSQL Relacional\n(Tablas Maestras, Índices & Vistas)" as DB
  [Módulo de Seguridad RLS\n(Row Level Security - Ley N° 29733)] as RLS
  [Bucket de Almacenamiento Cloud\n(Certificados PDF & Documentos)] as Storage
}

package "Capa de Integración y Servicios Externos" {
  [Adaptador SMTP Institucional\n(Emisor OTP @upt.pe)] as SMTP
  [Adaptador Google Workspace\n(Google Meet API)] as Meet
  [Adaptador Discord Bot\n(Gestión Canales Supervisados)] as Discord
}

' Consumo de Presentación hacia Servicios de Negocio
[PKG-UI-01] --> [PKG-SRV-01] : JSON / REST
[PKG-UI-02] --> [PKG-SRV-02] : JSON / REST
[PKG-UI-03] --> [PKG-SRV-03] : Inferencia Top-k
[PKG-UI-04] --> [PKG-SRV-04] : JSON / REST
[PKG-UI-05] --> [PKG-SRV-05] : JSON / REST
[PKG-UI-06] --> [PKG-SRV-06] : JSON / REST
[PKG-UI-07] --> [PKG-SRV-07] : JSON / REST
[PKG-UI-08] --> [PKG-SRV-08] : JSON / REST

' Interacción entre Servicios y Persistencia
[PKG-SRV-01] --> RLS
[PKG-SRV-02] --> DB
[PKG-SRV-03] --> DB
[PKG-SRV-04] --> DB : Persistencia de aulas libres
[PKG-SRV-05] --> DB
[PKG-SRV-06] --> DB
[PKG-SRV-07] --> Storage
[PKG-SRV-07] --> DB
[PKG-SRV-08] --> DB
RLS --> DB : Aislamiento granular

' Interacción con Adaptadores Externos
[PKG-SRV-01] --> SMTP : Envío de códigos OTP
[PKG-SRV-04] --> Meet : Generación dinámica de salas
[PKG-SRV-04] --> Discord : Aprovisionamiento de canales
@enduml
```

Fuente: Elaboración propia.

El diagrama de paquetes arquitecturales ratifica una estructuración modular que contribuye a la mantenibilidad (RNF09), la seguridad de datos (RNF02) y la interoperabilidad (RNF10) de la solución. Cada paquete de interfaz web se comunica con su servicio de backend correspondiente a través de contratos RESTful fuertemente tipados. Asimismo, el acceso a la persistencia se encuentra protegido por políticas RLS nativas en la base de datos, y los subsistemas de integración externa se encapsulan en adaptadores independientes, desacoplando la lógica de negocio frente a contingencias en plataformas de terceros.

## 6.2.2. Diagramas de Casos de Uso

### Presentación de los Diagramas de Casos de Uso
El modelo de casos de uso constituye el pilar fundamental del análisis orientado a objetos bajo la metodología UWE, formalizando los límites del sistema web, las interacciones funcionales de los actores humanos y técnicos, y la descomposición del alcance en componentes altamente cohesivos. Para proporcionar una perspectiva integral y a la vez granular del comportamiento del software en la EPIS-UPT, la presente sección se estructura en dos niveles: en primer lugar, el **Diagrama General Consolidado**, que articula la totalidad de los 24 casos de uso canónicos (CUS01 al CUS24) y sus dependencias formales; y en segundo lugar, una serie de **ocho diagramas modulares especializados** correspondientes a cada uno de los subsistemas arquitecturales (MOD-01 al MOD-08), detallando las asociaciones precisas entre actores, casos de uso y flujos de extensión. A continuación, se presenta la especificación visual y descriptiva de los casos de uso.

### Diagrama 6.4: Diagrama de Casos de Uso General Consolidado del Sistema Web P2P (CUS01 al CUS24)

```plantuml
@startuml
title Diagrama de Casos de Uso General Consolidado (CUS01 - CUS24)\nSistema Web P2P con Recomendador para Mentorías Académicas - EPIS UPT

left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
    FontSize 11
}

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}

' ===================================================
' ACTORES DEL SISTEMA
' ===================================================
actor "Mentoreado\n(I - IV Ciclo)" as Mentoreado
actor "Mentor\n(VII - X Ciclo)" as Mentor
actor "Administrador\n(Tutoría / Dirección)" as Admin
actor "Servicio Cron / Backend" as SysCron <<Sistema>>
actor "Servicios Externos\n(Meet, Discord)" as SysExt <<Sistema Externo>>

' ===================================================
' LÍMITE DEL SISTEMA Y MÓDULOS
' ===================================================
rectangle "Sistema Web de Mentorías P2P EPIS-UPT" {

  package "MOD-01: Seguridad, Autenticación y Gobernanza" {
    usecase "CUS01: Iniciar Sesión Institucional con 2FA" as UC01
    usecase "Aceptar Consentimiento para el\nTratamiento de Datos (Ley N° 29733)" as UC_Consent
    usecase "CUS10: Gestionar Asignación de Roles de Usuario" as UC10
  }

  package "MOD-02: Gestión Curricular y Perfiles Académicos" {
    usecase "CUS15: Configurar Perfil y Disponibilidad Horaria" as UC15
    usecase "CUS21: Gestionar Catálogo Curricular y Temarios" as UC21
  }

  package "MOD-03: Motor de Recomendación Inteligente (EdRecSys)" {
    usecase "CUS02: Consultar Recomendaciones Personalizadas Top-k" as UC02
    usecase "CUS03: Registrar Solicitud Temática por Demanda" as UC03
  }

  package "MOD-04: Planificación, Espacios y Agendamiento" {
    usecase "CUS06: Publicar Oferta de Mentoría" as UC06
    usecase "CUS11: Cargar Cronograma de Horarios Oficiales" as UC11
    usecase "CUS18: Modificar o Cancelar Oferta por Imprevisto" as UC18
  }

  package "MOD-05: Quórum, Confirmación y Cancelaciones" {
    usecase "CUS04: Reservar Cupo de Mentoría" as UC04
    usecase "CUS24: Confirmar Asistencia a Mentoría" as UC24
    usecase "CUS07: Gestionar Sesión ante Quórum Insuficiente" as UC07
    usecase "CUS17: Cancelar Reserva de Cupo (Desistimiento)" as UC17
    usecase "CUS23: Ejecutar Alertas y Evaluación Automática de Quórum" as UC23
  }

  package "MOD-06: Trazabilidad, Bitácoras y Evaluación" {
    usecase "CUS08: Registrar Bitácora y Control de Asistencia" as UC08
    usecase "CUS05: Responder Encuesta de Calidad Post-Mentoría" as UC05
    usecase "CUS19: Consultar Historial de Sesiones y Asistencia" as UC19
    usecase "CUS20: Gestionar Recursos Académicos de la Mentoría" as UC20
  }

  package "MOD-07: Gamificación, Reputación y Certificación" {
    usecase "CUS16: Consultar Tablero de Insignias y Reputación" as UC16
    usecase "CUS09: Descargar Certificado de Horas de Mentoría" as UC09
    usecase "CUS13: Parametrizar y Emitir Certificados" as UC13
  }

  package "MOD-08: Supervisión y Analítica Institucional" {
    usecase "CUS12: Destacar Mentorías Prioritarias" as UC12
    usecase "CUS14: Visualizar Tablero de Analíticas Institucionales" as UC14
    usecase "CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría" as UC22
  }
}

' ===================================================
' RELACIONES DE INCLUSIÓN Y EXTENSIÓN
' ===================================================
UC01 <.. UC_Consent : <<extend>>\n(Primer Acceso)

' ===================================================
' ASOCIACIONES: SERVICIOS EXTERNOS Y JOBS
' ===================================================
SysExt -- UC06
SysCron -- UC23

' ===================================================
' ASOCIACIONES: ESTUDIANTE MENTOREADO
' ===================================================
Mentoreado -- UC01
Mentoreado -- UC15
Mentoreado -- UC02
Mentoreado -- UC03
Mentoreado -- UC04
Mentoreado -- UC24
Mentoreado -- UC17
Mentoreado -- UC05
Mentoreado -- UC19
Mentoreado -- UC20

' ===================================================
' ASOCIACIONES: ESTUDIANTE MENTOR
' ===================================================
Mentor -- UC01
Mentor -- UC15
Mentor -- UC06
Mentor -- UC18
Mentor -- UC07
Mentor -- UC08
Mentor -- UC16
Mentor -- UC09
Mentor -- UC19
Mentor -- UC20

' ===================================================
' ASOCIACIONES: ADMINISTRADOR (TUTORÍA / DIRECCIÓN)
' ===================================================
Admin -- UC01
Admin -- UC10
Admin -- UC21
Admin -- UC11
Admin -- UC12
Admin -- UC13
Admin -- UC14
Admin -- UC22
@enduml
```

Fuente: Elaboración propia.

El Diagrama General Consolidado sintetiza de forma integral el ecosistema de interacciones del software. Refleja cómo la seguridad y gobernanza (MOD-01) condicionan el ingreso al sistema mediante 2FA y la extensión de consentimiento informado digital. Asimismo, demuestra la independencia entre el ciclo de búsqueda y agendamiento (MOD-02, MOD-03, MOD-04), el ciclo crítico de control de quórum y asistencia a 24 horas (MOD-05), y los procesos posteriores de evaluación pedagógica, reconocimiento al mentor y fiscalización académica (MOD-06, MOD-07, MOD-08).

---

### Diagrama 6.5: Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-01: Seguridad, Autenticación y Gobernanza
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Usuario Institucional\n(Mentoreado / Mentor / Admin)" as User
actor "Administrador\n(Tutoría / Dirección)" as Admin
actor "Servicio SMTP / UPT" as SMTP <<Sistema Externo>>

rectangle "MOD-01: Seguridad, Autenticación y Gobernanza" {
  usecase "CUS01: Iniciar Sesión Institucional con 2FA" as UC01
  usecase "Aceptar Consentimiento para el\nTratamiento de Datos (Ley N° 29733)" as UC_Consent
  usecase "CUS10: Gestionar Asignación de Roles de Usuario" as UC10
}

User -- UC01
Admin -- UC10
UC01 <.. UC_Consent : <<extend>>\n(Primer Acceso)
UC01 -- SMTP : Envía OTP
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-01 gobierna la puerta de entrada a la plataforma. Establece que el acceso al sistema exige la validación de identidad mediante correo institucional `@upt.pe` y código OTP temporal remitido por SMTP. La formalización del consentimiento legal bajo la Ley N° 29733 se desacopla como un flujo de extensión condicional exclusivo para el primer ingreso. Por su parte, la administración jerárquica de roles (CUS10) asegura que la promoción a Mentor responda a una evaluación objetiva del rendimiento académico del estudiante en cursos avanzados.

---

### Diagrama 6.6: Diagrama de Casos de Uso - MOD-02: Gestión Curricular y Perfiles Académicos

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-02: Gestión Curricular y Perfiles Académicos
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentoreado" as Mentee
actor "Estudiante Mentor" as Mentor
actor "Administrador\n(Tutoría / Dirección)" as Admin

rectangle "MOD-02: Gestión Curricular y Perfiles Académicos" {
  usecase "CUS15: Configurar Perfil y Disponibilidad Horaria" as UC15
  usecase "CUS21: Gestionar Catálogo Curricular y Temarios" as UC21
}

Mentee -- UC15
Mentor -- UC15
Admin -- UC21
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-02 gestiona la información formativa indispensable para el funcionamiento algorítmico del sistema. CUS15 permite a mentoreados y mentores actualizar semanalmente su disponibilidad y sus preferencias temáticas en materias críticas. Complementariamente, CUS21 otorga a las autoridades de la EPIS-UPT el control centralizado del catálogo de cursos filtro y la taxonomía de unidades silábicas, asegurando que las ofertas y solicitudes respondan a la malla curricular oficial.

---

### Diagrama 6.7: Diagrama de Casos de Uso - MOD-03: Motor de Recomendación Inteligente (EdRecSys)

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-03: Motor de Recomendación Inteligente (EdRecSys)
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentoreado" as Mentee
actor "Estudiante Mentor" as Mentor

rectangle "MOD-03: Motor de Recomendación Inteligente (EdRecSys)" {
  usecase "CUS02: Consultar Recomendaciones Personalizadas Top-k" as UC02
  usecase "CUS03: Registrar Solicitud Temática por Demanda" as UC03
}

Mentee -- UC02
Mentee -- UC03
UC03 -- Mentor : Notifica demanda
@enduml
```

Fuente: Elaboración propia.

El subsistema MOD-03 materializa el valor central del proyecto al conectar las necesidades de los alumnos con el talento disponible. Mediante CUS02, el mentoreado obtiene un ranking adaptativo Top-k de mentores idóneos (cuyo cálculo de similitud coseno y filtrado colaborativo opera como lógica interna del backend). Cuando no existen ofertas programadas para un tema específico, CUS03 habilita la captura de la demanda formativa, alertando a los mentores para que formulen talleres dirigidos.

---

### Diagrama 6.8: Diagrama de Casos de Uso - MOD-04: Planificación, Espacios y Agendamiento

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-04: Planificación, Espacios y Agendamiento
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentor" as Mentor
actor "Administrador\n(Tutoría / Dirección)" as Admin
actor "Servicios Externos\n(Meet, Discord)" as SysExt <<Sistema Externo>>

rectangle "MOD-04: Planificación, Espacios y Agendamiento" {
  usecase "CUS06: Publicar Oferta de Mentoría" as UC06
  usecase "CUS11: Cargar Cronograma de Horarios Oficiales" as UC11
  usecase "CUS18: Modificar o Cancelar Oferta por Imprevisto" as UC18
}

Mentor -- UC06
Mentor -- UC18
Admin -- UC11
UC06 -- SysExt : Aprovisiona enlace/canal
UC18 -- SysExt : Actualiza/libera sala
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-04 orquesta la logística de infraestructura física y virtual. Permite al mentor crear ofertas (CUS06) y gestionar eventualidades por causa mayor antes del inicio de la sesión (CUS18). Para sesiones presenciales, el sistema valida aulas libres contra la base de datos alimentada por el Administrador mediante el procesamiento de cronogramas en PDF/Excel (CUS11, operado mediante un parser interno). Para sesiones virtuales, la plataforma se integra con Google Meet y Discord para el aprovisionamiento automatizado de salas.

---

### Diagrama 6.9: Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-05: Quórum, Confirmación y Cancelaciones
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentoreado" as Mentee
actor "Estudiante Mentor" as Mentor
actor "Servicio Cron / Backend" as SysCron <<Sistema>>

rectangle "MOD-05: Quórum, Confirmación y Cancelaciones" {
  usecase "CUS04: Reservar Cupo de Mentoría" as UC04
  usecase "CUS24: Confirmar Asistencia a Mentoría" as UC24
  usecase "CUS17: Cancelar Reserva de Cupo (Desistimiento)" as UC17
  usecase "CUS23: Ejecutar Alertas y Evaluación Automática de Quórum" as UC23
  usecase "CUS07: Gestionar Sesión ante Quórum Insuficiente" as UC07
}

Mentee -- UC04
Mentee -- UC24
Mentee -- UC17
SysCron -- UC23
Mentor -- UC07
UC23 ..> UC07 : Habilita ante quórum < 50%
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-05 implementa el protocolo crítico de confirmación temporal y preservación de aforos. Separa estrictamente la inscripción inicial (CUS04) de la confirmación anticipada (CUS24, habilitada hasta $T-24\text{ h}$) y el desistimiento voluntario (CUS17). Al cumplirse exactamente el corte de 24 horas, el demonio cron desatendido (CUS23) computa el quórum mínimo (50%); si el porcentaje es deficiente, notifica de inmediato al Mentor para que ejerza su potestad de decisión humana (CUS07), evitando cancelaciones arbitrarias del sistema.

---

### Diagrama 6.10: Diagrama de Casos de Uso - MOD-06: Trazabilidad, Bitácoras y Evaluación

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-06: Trazabilidad, Bitácoras y Evaluación
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentoreado" as Mentee
actor "Estudiante Mentor" as Mentor

rectangle "MOD-06: Trazabilidad, Bitácoras y Evaluación" {
  usecase "CUS08: Registrar Bitácora y Control de Asistencia" as UC08
  usecase "CUS05: Responder Encuesta de Calidad Post-Mentoría" as UC05
  usecase "CUS19: Consultar Historial de Sesiones y Asistencia" as UC19
  usecase "CUS20: Gestionar Recursos Académicos de la Mentoría" as UC20
}

Mentor -- UC08
Mentee -- UC05
Mentee -- UC19
Mentor -- UC19
Mentor -- UC20
Mentee -- UC20 : Descarga materiales
UC08 ..> UC05 : Habilita para asistentes efectivos
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-06 asegura el registro fehaciente de la actividad pedagógica. El mentor diligencia la bitácora y marca las asistencias reales en CUS08, lo cual transiciona la sesión a completada y abre la ventana perentoria de 24 horas para que los estudiantes asistentes completen la encuesta de calidad (CUS05). Adicionalmente, CUS19 y CUS20 permiten a mentoreados y mentores revisar su récord histórico y acceder a los recursos didácticos compartidos (diapositivas, guías y repositorios de código).

---

### Diagrama 6.11: Diagrama de Casos de Uso - MOD-07: Gamificación, Reputación y Certificación

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-07: Gamificación, Reputación y Certificación
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Estudiante Mentor" as Mentor
actor "Administrador\n(Tutoría / Dirección)" as Admin

rectangle "MOD-07: Gamificación, Reputación y Certificación" {
  usecase "CUS16: Consultar Tablero de Insignias y Reputación" as UC16
  usecase "CUS13: Parametrizar y Emitir Certificados" as UC13
  usecase "CUS09: Descargar Certificado de Horas de Mentoría" as UC09
}

Mentor -- UC16
Admin -- UC13
Mentor -- UC09
UC13 ..> UC09 : Provee certificado emitido
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-07 regula los mecanismos de reconocimiento formal y estímulo para los mentores. A través de CUS16, el mentor monitorea su progreso en insignias y su score docente. En CUS13, la Dirección de Escuela parametriza los umbrales mínimos de horas semestrales requeridos y autoriza la emisión de constancias con código correlativo institucional y hash SHA-256 de validación. Finalmente, CUS09 faculta al mentor calificado a descargar su certificado en formato PDF para la convalidación de créditos extracurriculares.

---

### Diagrama 6.12: Diagrama de Casos de Uso - MOD-08: Supervisión y Analítica Institucional

```plantuml
@startuml
title Diagrama de Casos de Uso - MOD-08: Supervisión y Analítica Institucional
left to right direction
skinparam packageStyle rectangle
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam usecase {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

actor "Administrador\n(Tutoría / Dirección)" as Admin

rectangle "MOD-08: Supervisión y Analítica Institucional" {
  usecase "CUS12: Destacar Mentorías Prioritarias" as UC12
  usecase "CUS14: Visualizar Tablero de Analíticas Institucionales" as UC14
  usecase "CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría" as UC22
}

Admin -- UC12
Admin -- UC14
Admin -- UC22
@enduml
```

Fuente: Elaboración propia.

El módulo MOD-08 proporciona a las autoridades académicas herramientas de analítica y fiscalización docente. CUS12 permite asignar prioridad a asignaturas críticas para darles realce algorítmico y visual en el catálogo. CUS14 consolida indicadores agregados de demanda insatisfecha, ausentismo y satisfacción docente preservando la privacidad estudiantil bajo la Ley N° 29733. Por último, CUS22 provee la interfaz de auditoría para visar o dejar en observación las bitácoras pedagógicas y horas declaradas previo a su certificación oficial.

---

## 6.2.3. Escenarios de Casos de Uso (Fase de Diseño)

### Presentación de los Escenarios de Casos de Uso en Fase de Diseño

En la presente **Fase de Diseño de Software**, los escenarios de casos de uso traducen los requerimientos funcionales del sistema en especificaciones de comportamiento detalladas a nivel de arquitectura y código ejecutable. Cada especificación proporciona trazabilidad completa hacia los componentes de frontend (React 18 con TypeScript y Tailwind CSS), servicios y adaptadores HTTP (`apiClient`), controladores y rutas de FastAPI, esquemas de validación Pydantic, servicios de lógica de negocio, entidades del modelo relacional ORM en SQLAlchemy y transacciones ACID en PostgreSQL bajo control estricto de concurrencia y cerrojos pesimistas.

La estructura de cada caso de uso conserva con rigurosidad la plantilla canónica institucional:
1. **Ficha Técnica Estructurada (13 atributos):** Identificador unívoco (`Id Caso de Uso`), `Nombre`, `Tipo`, `Requisito ID (RF)`, `Versión` (2.0), `Autor`, `Actores` con roles de sistema (`UserRole`), `Interacción`, `Descripción` técnica exhaustiva, `Referencias` normativas y arquitectónicas, `Anexos` de código fuente, `Precondiciones` y `PostCondiciones`.
2. **Flujo Normal de Eventos:** Distribuido en columnas estrictas (**`Usuario`** | **`Sistema`**), subdividido en fases secuenciales de interacción con pasos numerados correlativamente y llamadas explícitas de desvío `(Si [condición], salta a E00X / A00X)`.
3. **Flujos Alternativos (`A00X`) y de Excepción (`E00X`):** Encabezados de bloque específicos, columnas **`Usuario`** | **`Sistema`**, pasos jerárquicos (`E00X-1.1`, `E00X-1.2`) y cláusula formal de retorno al paso correspondiente del Flujo Normal o cierre explícito del caso de uso.
4. **Trazabilidad de Código y Diseño:** Especificación exacta de endpoints RESTful, verbos HTTP, códigos de estado (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, `503 Service Unavailable`), tipos de excepciones y directivas de control de concurrencia (`SELECT ... FOR UPDATE`, locks transaccionales y mecanismos de desempate).

A continuación, se presentan los 24 casos de uso canónicos estructurados en los 8 módulos arquitectónicos del sistema:

---

### MOD-01: Seguridad, Autenticación y Gobernanza

#### CUS-001 - Iniciar sesión institucional con 2FA

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-001** (CUS-001) |
| **Nombre** | Iniciar sesión institucional con 2FA y formalización de consentimiento digital |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-001 (Autenticación multifactor 2FA institucional), RF-002 (Formalización de consentimiento digital Ley 29733); RN-01 (Dominio institucional @upt.pe y OTP con TTL de 5 minutos), RN-02 (Consentimiento informado legal digital) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Usuario Institucional (`UserRole.mentoreado`, `UserRole.mentor`, `UserRole.administrador`), Servicio de Correo SMTP / UPT (`EmailService`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 |
| **Descripción** | Permite autenticar la identidad del usuario universitario mediante flujo 2FA sin contraseñas estáticas, validando la pertenencia al dominio oficial `@upt.pe` a través del controlador `aplicacion/backend/app/api/v1/endpoints/auth.py`. El backend genera un código OTP numérico criptográficamente seguro de 6 dígitos con expiración de 300 segundos persistido con hash en base de datos (`app/models/auth.py`), despacha el correo mediante `auth_service.py` (`AuthService.request_otp`) y valida el ingreso en `POST /api/v1/auth/verify-otp`. Verifica el estado del consentimiento informado en `app/services/consent_service.py` (`ConsentService.get_consent_status`); si es nuevo, despliega `ConsentModalView.tsx` y formaliza la aceptación persistiendo IP, User-Agent y timestamp en `consentimientos_legales` (`app/models/consent.py`). Tras la validación, expide un token JWT criptográfico (`HS256`) con 8 horas de vigencia (`ACCESS_TOKEN_EXPIRE_MINUTES = 480`) y claims de roles (`UserRole`), retornando el payload al frontend `LoginOtpView.tsx` para su almacenamiento seguro en `localStorage`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios de Acreditación ICACIT<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-01: Seguridad, Autenticación y Gobernanza)<br>Ley Nº 29733 de Protección de Datos Personales del Perú y D.S. Nº 003-2013-JUS |
| **Anexos** | `aplicacion/frontend/src/components/LoginOtpView.tsx`<br>`aplicacion/frontend/src/components/ConsentModalView.tsx`<br>`aplicacion/frontend/src/services/authService.ts` (`AuthService`, `apiClient`)<br>`aplicacion/frontend/src/services/consentService.ts` (`ConsentService`)<br>`aplicacion/backend/app/api/v1/endpoints/auth.py` (`POST /api/v1/auth/request-otp`, `POST /api/v1/auth/verify-otp`)<br>`aplicacion/backend/app/api/v1/endpoints/consent.py` (`GET /api/v1/consent/status`, `POST /api/v1/consent/accept`)<br>`aplicacion/backend/app/services/auth_service.py` (`AuthService.request_otp`, `AuthService.verify_otp`)<br>`aplicacion/backend/app/models/auth.py` (`Usuario`, `CodigoOTP`), `app/models/consent.py` (`ConsentimientoLegal`) |
| **Precondiciones** | 1. El usuario posee una cuenta activa perteneciente al dominio oficial `@upt.pe` en la tabla `usuarios`.<br>2. El servicio SMTP institucional se encuentra configurado en `app/core/config.py` con credenciales operativas.<br>3. El usuario no registra suspensión administrativa en `usuarios.activo = true`. |
| **PostCondiciones** | 1. Token JWT institucional (`HS256`) generado y almacenado en `localStorage` con vigencia estricta de 8 horas.<br>2. Traza inmutable de auditoría registrada en la tabla física `consentimientos_legales` con UUID, IP, User-Agent y marca de tiempo UTC.<br>3. Redirección reactiva en cliente al panel principal según el rol asignado (`mentoreado`, `mentor` o `administrador`). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Validación de identidad institucional y solicitud de OTP** | |
| **1.** El usuario accede a la vista de autenticación `LoginOtpView.tsx`, ingresa su dirección de correo institucional en el cuadro de texto `"Correo Institucional"` (`input[type="email"]`) y hace clic en el botón `"Continuar"`. | **2.** En `authService.ts`, la función `requestOtp(email)` despacha una petición `POST /api/v1/auth/request-otp` con payload JSON `{"email": email}` hacia el controlador `auth.py`. El backend valida con Pydantic (`EmailStr`) la sintaxis y comprueba que `email.endswith("@upt.pe")`. Ejecuta `SELECT * FROM usuarios WHERE email = :email AND activo = true`. (Si el dominio es ajeno a la universidad, salta a E001). (Si la cuenta está inactiva o suspendida, salta a E002). |
| **Fase 2: Generación criptográfica, despacho SMTP y verificación de código temporal** | |
| **3.** El usuario revisa en pantalla el correo verificado y presiona el botón `"Solicitar Código de Acceso"`. | **4.** En `auth_service.py`, `AuthService.request_otp()` genera un código numérico aleatorio seguro mediante `secrets.randbelow(900000) + 100000`, calcula su hash SHA-256 y lo almacena en la tabla temporal con expiración `NOW() + INTERVAL '5 MINUTES'` (RN-01). Invoca a `EmailService.send_otp_email()` para despachar el correo SMTP. Retorna HTTP 200 `{"message": "OTP_SENT"}`. En cliente, `LoginOtpView.tsx` despliega el modal con seis casillas individuales numéricas, inicializa el temporizador regresivo de 300 segundos en color azul institucional y enfoca la primera casilla. (Si el usuario no recibe el código en su buzón tras 60 segundos o el temporizador expira, salta a A002). |
| **5.** El usuario consulta su bandeja institucional, copia el código de 6 dígitos, lo ingresa en las casillas del componente y hace clic en `"Verificar e Ingresar"`. | **6.** En `authService.ts`, se despacha `POST /api/v1/auth/verify-otp` con payload `{"email": email, "otp_code": code}`. `auth_service.py` recupera el registro, compara el hash y valida `expira_en > NOW()`. Si coincide, invalida el OTP usado y consulta `ConsentService.get_consent_status(email)`. (Si el código es incorrecto, salta a E003). (Si el código ha expirado, salta a E004). (Si se superan los 3 intentos fallidos consecutivos, salta a E005). (Si el usuario ya cuenta con consentimiento digital previo, salta a A001). |
| **Fase 3: Formalización de consentimiento legal digital y emisión de sesión** | |
| **7.** El cliente renderiza el componente `ConsentModalView.tsx`. El usuario lee los términos de tratamiento de datos personales en el panel con barra de desplazamiento vertical, marca la casilla de verificación `"He leído y acepto los términos de consentimiento informado bajo la Ley Nº 29733"` y presiona el botón `"Aceptar y Continuar"`. (Si el usuario desmarca o rechaza los términos, salta a E006). | **8.** En `consentService.ts`, se invoca `POST /api/v1/consent/accept` enviando el identificador de usuario y la versión de términos. El backend inserta en `consentimientos_legales` el registro inmutable con IP de origen (`client.host`), User-Agent y timestamp UTC. Seguidamente, `security.py` genera el token JWT firmado mediante `create_access_token` incluyendo los claims `sub: email`, `roles: [UserRole]`, `exp: now + 8h`. El backend retorna HTTP 200 con `access_token` y perfil. En `App.tsx`, el token se persiste en `localStorage.setItem('auth_token', token)`, se actualiza el estado global de autenticación y se redirige al panel correspondiente al rol, mostrando una notificación flotante en color verde de éxito: *"¡Sesión institucional iniciada exitosamente! Bienvenido al Sistema de Mentorías EPIS-UPT"*. |

##### Flujos Alternativos

##### Flujo alternativo A001: Acceso recurrente con consentimiento digital previamente formalizado
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario completa satisfactoriamente el paso 5 introduciendo el código OTP válido. | **A001-1.2** En `auth.py`, `ConsentService.get_consent_status` retorna `has_consented = true` tras localizar en `consentimientos_legales` el registro activo sin revocación. |
| **A001-1.3** El usuario visualiza la pantalla de carga con indicador circular de progreso en color azul institucional. | **A001-1.4** El sistema omite la renderización de `ConsentModalView.tsx`, emite directamente el token JWT firmado de sesión con sus roles asignados y retorna al paso 8 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Reenvío de código temporal por retraso en buzón o caducidad
| Usuario | Sistema |
|---|---|
| **A002-1.1** El usuario constata la ausencia del código en su buzón tras 60 segundos o la finalización del temporizador regresivo de 5 minutos, y hace clic en el enlace `"Reenviar código OTP"`. | **A002-1.2** En `LoginOtpView.tsx`, se valida que hayan transcurrido al menos 60 segundos desde la última solicitud. Despacha nuevamente `POST /api/v1/auth/request-otp` hacia el backend. |
| **A002-1.3** El usuario visualiza la actualización del temporizador regresivo reiniciado a 5 minutos en color azul institucional y una alerta en color ámbar: *"Se ha remitido un nuevo código de acceso a su buzón institucional"*. | **A002-1.4** El backend invalida el código anterior, genera una nueva clave aleatoria de 6 dígitos, la despacha vía SMTP y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Dominio de correo no institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `auth.py` comprueba que la cadena ingresada no termina en `@upt.pe`. Lanza `HTTPException(status_code=400, detail="INVALID_DOMAIN: El acceso está reservado exclusivamente a cuentas institucionales @upt.pe.")`.<br><br>En `authService.ts`, captura el error 400 y propaga la excepción hacia el componente. `LoginOtpView.tsx` despliega una etiqueta de advertencia en color rojo: *"Acceso denegado: Ingrese únicamente su correo institucional universitario (@upt.pe)"*. Presenta el botón `<button onClick={handleReset}>Corregir Correo</button>`. |
| **E001-1.2** Hace clic en el botón "Corregir Correo". | **E001-1.3** Limpia el cuadro de texto `"Correo Institucional"`, le asigna el foco automáticamente y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Cuenta institucional inactiva o suspendida
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, `auth.py` ejecuta `SELECT activo FROM usuarios WHERE email = :email` y detecta `activo = false`. Lanza `HTTPException(status_code=403, detail="ACCOUNT_SUSPENDED: Su cuenta institucional registra suspensión administrativa.")`.<br><br>En `LoginOtpView.tsx`, se captura el error 403 y se despliega un cuadro de diálogo modal en color rojo con el mensaje: *"Cuenta inhabilitada. Su registro se encuentra en estado inactivo. Por favor, comuníquese con la Dirección de Escuela EPIS-UPT"*. Presenta el botón `<button onClick={handleCloseModal}>Aceptar</button>`. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Cierra el cuadro modal, restablece el formulario inicial y finaliza la sesión sin generar registros de autenticación. |

##### Flujo de excepción E003: Código temporal OTP incorrecto
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, `auth_service.py` comprueba que el hash del código introducido no coincide con el persistido en base de datos. Incrementa el contador `intentos_fallidos += 1` y lanza `HTTPException(status_code=400, detail="INVALID_OTP: El código ingresado no coincide con el enviado a su buzón.")`.<br><br>En `LoginOtpView.tsx`, se captura el error y se muestra una alerta en color rojo indicando el error y el número de intentos restantes (e.g. *"Código erróneo. Le quedan 2 intentos antes del bloqueo temporal"*). Presenta el botón `<button onClick={handleClearOtp}>Reintentar</button>`. |
| **E003-1.2** Hace clic en el botón "Reintentar". | **E003-1.3** Limpia las seis casillas numéricas, posiciona el cursor en la primera casilla y retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Código temporal OTP expirado
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, `auth_service.py` comprueba que `NOW() > expira_en` (plazo de 5 minutos excedido conforme a RN-01). Lanza `HTTPException(status_code=400, detail="EXPIRED_OTP: El código temporal ha caducado por límite de tiempo de 5 minutos.")`.<br><br>En `LoginOtpView.tsx`, se captura el error y se despliega una alerta en color ámbar: *"El código temporal ha caducado. Por favor, solicite uno nuevo para ingresar"*. Presenta el botón `<button onClick={handleRequestNewOtp}>Solicitar Nuevo Código</button>`. |
| **E004-1.2** Hace clic en el botón "Solicitar Nuevo Código". | **E004-1.3** Restablece las casillas numéricas, reinicia el temporizador regresivo y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Bloqueo temporal por exceso de intentos fallidos
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 6 del Flujo Normal, `auth_service.py` evalúa `intentos_fallidos >= 3`. Invalida inmediatamente el OTP, bloquea temporalmente la emisión para el correo por 15 minutos en memoria/base de datos y lanza `HTTPException(status_code=429, detail="MAX_ATTEMPTS_EXCEEDED: Se ha superado el límite de 3 intentos fallidos consecutivos. Acceso bloqueado por 15 minutos.")`.<br><br>En `LoginOtpView.tsx`, se bloquean todas las casillas de entrada y se despliega un panel de seguridad en color rojo indicando el bloqueo temporal. Presenta el botón `<button onClick={handleResetToLogin}>Volver al Inicio</button>`. |
| **E005-1.2** Hace clic en el botón "Volver al Inicio". | **E005-1.3** Redirige a la vista inicial de autenticación, restablece el formulario y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E006: Rechazo voluntario del consentimiento informado
| Usuario | Sistema |
|---|---|
| | **E006-1.1** En el paso 7 del Flujo Normal, el usuario no marca la casilla de verificación o presiona el botón `"Declinar y Salir"`. `ConsentModalView.tsx` captura la acción sin enviar petición de aceptación.<br><br>Despliega un cuadro de diálogo modal en color ámbar advirtiendo que la formalización del consentimiento legal bajo la Ley Nº 29733 es un requisito obligatorio e indispensable para utilizar los servicios de la plataforma. Presenta el botón `<button onClick={handleConfirmExit}>Confirmar Salida</button>` y el botón `<button onClick={handleReopenTerms}>Revisar Términos</button>`. |
| **E006-1.2** Hace clic en el botón "Confirmar Salida". | **E006-1.3** Destruye la sesión provisional, purga los datos temporales del formulario, emite notificación informativa y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-010 - Gestionar asignación de roles de usuario

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-010** (CUS-010) |
| **Nombre** | Gestionar asignación y revocación de roles institucionales de usuario |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-003 (Gestión y asignación administrativa de roles de usuario); RN-03 (Separación de privilegios y control de acceso RBAC institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 01 - Sprint 02 |
| **Descripción** | Permite a las autoridades institucionales consultar la nómina universitaria de usuarios y administrar sus roles operativos (`UserRole.mentoreado`, `UserRole.mentor`, `UserRole.administrador`, `UserRole.coordinador`) a través del componente `AdminDashboardView.tsx` y el servicio `roleService.ts`. El backend expone los endpoints en `aplicacion/backend/app/api/v1/endpoints/roles.py`, verificando en cada solicitud los privilegios administrativos con `app/core/security.py` (`decode_access_token` comprobando claim `roles` conteniendo `administrador`). El servicio `role_service.py` ejecuta mutaciones transaccionales ACID en las tablas `roles` y `roles_usuarios` (`app/models/roles.py`), garantizando que ningún usuario quede huérfano de roles y que ningún administrador pueda revocar sus propios privilegios. Cada mutación genera una traza en la tabla de auditoría con el UUID del administrador ejecutor, IP de origen y marca de tiempo UTC. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-01: Seguridad, Autenticación y Gobernanza)<br>Modelo de Control de Acceso Basado en Roles (NIST RBAC Standard) |
| **Anexos** | `aplicacion/frontend/src/components/AdminDashboardView.tsx`<br>`aplicacion/frontend/src/services/roleService.ts` (`RoleService`, `ApiRoleAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/roles.py` (`GET /api/v1/roles/users`, `POST /api/v1/roles/assign`, `DELETE /api/v1/roles/revoke`)<br>`aplicacion/backend/app/services/role_service.py` (`RoleService.list_users`, `RoleService.assign_role`, `RoleService.revoke_role`)<br>`aplicacion/backend/app/models/roles.py` (`Rol`, `RolUsuario`, `UserRole`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. El usuario solicitante ha iniciado sesión institucional válida portando un token JWT activo en `localStorage`.<br>2. El claim `roles` dentro del payload JWT contiene el valor `UserRole.administrador`.<br>3. El catálogo institucional de roles base se encuentra inicializado en la tabla física `roles`. |
| **PostCondiciones** | 1. Inserción o eliminación atómica confirmada en la tabla `roles_usuarios` mediante `db.commit()`.<br>2. Registro de auditoría persistido en la base de datos con identificador del operador, usuario modificado y cambio realizado.<br>3. Actualización reactiva del estado del usuario en el componente de gestión de roles de la interfaz administrativa. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel administrativo y consulta de nómina de usuarios** | |
| **1.** El administrador institucional accede al panel de control en `AdminDashboardView.tsx` y hace clic en la pestaña `"Gestión de Roles"`. | **2.** En `roleService.ts`, se despacha la petición `GET /api/v1/roles/users` incluyendo en la cabecera `Authorization: Bearer <token>`. En `roles.py`, la función dependiente `require_admin_role` valida la firma criptográfica y verifica que `UserRole.administrador` esté presente en los claims. `role_service.py` ejecuta una consulta relacional `SELECT u.id, u.email, u.nombres, u.apellidos, array_agg(r.nombre) AS roles FROM usuarios u LEFT JOIN roles_usuarios ru ON u.id = ru.id_usuario LEFT JOIN roles r ON ru.id_rol = r.id GROUP BY u.id`. Retorna HTTP 200 con la nómina paginada. `AdminDashboardView.tsx` renderiza la tabla interactiva de usuarios con filtros de búsqueda y botones de acción. (Si el token no cuenta con privilegios administrativos, salta a E001). (Si la consulta falla por timeout en base de datos, salta a E002). |
| **Fase 2: Búsqueda y selección de usuario para modificación** | |
| **3.** El administrador ingresa el código universitario o correo institucional del estudiante o docente en el cuadro de búsqueda `"Buscar usuario"` y hace clic en el botón `"Buscar"`. | **4.** En `AdminDashboardView.tsx`, se filtra la lista de usuarios en memoria o se despacha `GET /api/v1/roles/users?q=...`. El sistema resalta la fila del usuario localizado. El administrador hace clic en el botón `"Modificar Roles"` en la fila correspondiente. El sistema despliega un cuadro de diálogo modal `"Asignación de Roles Institucionales"` con casillas de verificación para cada rol del sistema (`Mentoreado`, `Mentor`, `Administrador`, `Coordinador`), marcando los roles actualmente asignados. (Si la búsqueda no arroja coincidencias en el padrón, salta a A001). |
| **Fase 3: Modificación atómica de roles y registro de auditoría** | |
| **5.** El administrador marca o desmarca las casillas según corresponda (e.g. asigna el rol `Mentor` a un estudiante habilitado) y hace clic en el botón `"Guardar Asignación"`. | **6.** En `roleService.ts`, se despacha una petición `POST /api/v1/roles/assign` con payload `RoleAssignRequest(user_id=target_user_id, roles=selected_roles)`. `role_service.py` inicia una transacción ACID con `db.begin()`. Verifica que el conjunto de roles resultante no esté vacío y que el administrador no esté revocando su propio rol de administrador. Ejecuta las sentencias `DELETE FROM roles_usuarios WHERE id_usuario = :uid` e `INSERT INTO roles_usuarios (id_usuario, id_rol) VALUES ...`. Inserta la traza de auditoría, ejecuta `db.commit()` y retorna HTTP 200 con el perfil actualizado. `AdminDashboardView.tsx` actualiza reactivamente la tabla de usuarios, cierra la ventana modal y despliega una notificación flotante en color verde de éxito: *"Roles actualizados exitosamente para el usuario"*. (Si intenta revocar todos los roles dejando al usuario sin privilegios, salta a E003). (Si intenta auto-revocarse el rol de Administrador, salta a E004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda sin coincidencias en el padrón institucional
| Usuario | Sistema |
|---|---|
| **A001-1.1** El administrador ingresa un criterio de búsqueda en el paso 3 que no coincide con ningún registro activo. | **A001-1.2** En `AdminDashboardView.tsx`, el filtro retorna una lista vacía. El sistema despliega en la tabla un panel informativo con el mensaje: *"No se encontraron usuarios que coincidan con el criterio ingresado. Verifique el código o correo institucional"*. Presenta el botón `<button onClick={handleClearSearch}>Limpiar Búsqueda</button>`. |
| **A001-1.3** El administrador hace clic en el botón "Limpiar Búsqueda". | **A001-1.4** Restablece el cuadro de búsqueda, recarga la nómina completa de usuarios en la tabla y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Acceso denegado por privilegios administrativos insuficientes
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `roles.py` evalúa el token JWT del usuario y detecta que no incluye el rol `administrador`. Lanza `HTTPException(status_code=403, detail="FORBIDDEN: Se requieren privilegios de Administrador Institucional para acceder a este módulo.")`.<br><br>En `App.tsx`, el interceptor de peticiones captura el código 403 y redirige inmediatamente al usuario a su panel correspondiente según su rol, desplegando un aviso en color rojo: *"Acceso Restringido: No posee autorización para el módulo de administración de roles"*. |
| **E001-1.2** Hace clic en el botón "Entendido" en la alerta de restricción. | **E001-1.3** Cierra el aviso y retorna al paso 1 del Flujo Normal de Eventos en su vista autorizada. |

##### Flujo de excepción E002: Error de conexión o timeout en base de datos
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, la conexión hacia PostgreSQL sufre timeout o interrupción de red. `roles.py` captura la excepción de base de datos y lanza `HTTPException(status_code=503, detail="SERVICE_UNAVAILABLE: No se pudo establecer conexión con el repositorio de usuarios. Reintente en unos instantes.")`.<br><br>En `AdminDashboardView.tsx`, se captura el error 503 y se despliega un panel de advertencia en color ámbar con el mensaje de indisponibilidad. Presenta el botón `<button onClick={fetchUsers}>Reintentar Carga</button>`. |
| **E002-1.2** Hace clic en el botón "Reintentar Carga". | **E002-1.3** Dispara nuevamente la petición `GET /api/v1/roles/users` y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Intento de dejar al usuario sin ningún rol asignado
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, el administrador desmarca todas las casillas de roles. `role_service.py` valida `len(selected_roles) == 0`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="EMPTY_ROLE_SET_PROHIBITED: Todo usuario debe mantener al menos un rol institucional asignado.")`.<br><br>En `AdminDashboardView.tsx`, se despliega un mensaje de error en color rojo dentro del modal indicando la obligatoriedad de al menos un rol institucional. Mantiene el modal abierto sin cerrar la transacción. |
| **E003-1.2** Marca al menos una casilla de rol válida (e.g. `Mentoreado`). | **E003-1.3** Rehabilita el botón `"Guardar Asignación"` y retorna al paso 5 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Intento de auto-revocación del rol Administrador
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, el administrador intenta desmarcar el rol `Administrador` sobre su propia cuenta (`target_user_id == current_user_id`). `role_service.py` detecta la colisión de gobernanza, ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="CANNOT_REVOKE_OWN_ADMIN: Un administrador no puede auto-revocarse sus propios privilegios para evitar la pérdida de gobernanza institucional.")`.<br><br>En `AdminDashboardView.tsx`, se captura el error y se muestra una alerta en color rojo destacada dentro del modal. |
| **E004-1.2** Hace clic en el botón "Restablecer Selección". | **E004-1.3** Vuelve a marcar la casilla de Administrador en el modal y retorna al paso 5 del Flujo Normal de Eventos. |


---

### MOD-02: Ofertas de Mentoría y Gestión de Recursos

#### CUS-006 - Publicar oferta de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-006** (CUS-006) |
| **Nombre** | Publicar oferta de mentoría académica con validación de antelación y aforo |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-008 (Publicación y parametrización de ofertas de mentoría), RF-009 (Aprovisionamiento automatizado de infraestructura); RN-04 (Ventana de antelación mínima de 24 horas a T-24h), RN-05 (Aforo máximo de 10 presencial y 20 virtual), RN-06 (Prevención de colisión horaria de espacios) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentores formalizar la apertura de una sesión de mentoría a través del componente cliente `OfferPublishView.tsx` y el servicio `offerService.ts`, despachando una petición `POST /api/v1/offers/publish` hacia el controlador `aplicacion/backend/app/api/v1/endpoints/offers.py`. El backend valida el token JWT institucional extrayendo el claim del mentor, y ejecuta en `app/services/offer_service.py` (`OfferService.publish_offer`) las validaciones de negocio institucionales: antelación mínima de 24 horas respecto a la fecha y hora actual en UTC (`fecha_inicio > now_utc + 24h`, RN-04), límites de capacidad según modalidad (máximo 10 cupos en presencial y 20 en virtual, RN-05), verificación de ausencia de traslape con otras sesiones activas del mentor, y validación del aula física o enlace institucional de videoconferencia. Persiste la entidad ORM `SesionMentoria` (`app/models/offer.py`) en estado `PUBLICADA`, emite una confirmación con HTTP 201 Created y sincroniza la cartelera institucional. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Reglamento Académico de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService`, `ApiOfferAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/publish`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.publish_offer`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`, `ModalidadSesion`), `app/models/curriculum.py` (`TemaCurricular`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo conteniendo el rol `UserRole.mentor`.<br>2. Perfil de mentor registrado en `perfiles_academicos` con materias y temas habilitados.<br>3. Fecha y hora de inicio fijadas con al menos 24 horas de antelación respecto a la hora UTC actual. |
| **PostCondiciones** | 1. Registro insertado en la tabla `sesiones_mentoria` con `estado = 'PUBLICADA'` y aforo parametrizado.<br>2. Transacción confirmada en PostgreSQL y emisión de evento de invalidación de caché para el motor de recomendación.<br>3. Despliegue de comprobante de publicación en cliente con código identificador de sesión. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Configuración de la sesión y selección curricular** | |
| **1.** El estudiante mentor accede a la vista de publicación en `OfferPublishView.tsx` y selecciona la asignatura curricular en la lista desplegable `"Curso"`. | **2.** En `offerService.ts`, se invoca la carga de temas disponibles. `OfferPublishView.tsx` renderiza los temas silábicos correspondientes, los campos de fecha de inicio, hora de inicio, duración en minutos (60 a 120), modalidad (`Presencial` o `Virtual`), aula asignada o enlace de videoconferencia (`meet.google.com`), y número de cupos máximos. |
| **Fase 2: Ingreso de parámetros, validación de reglas de aforo y antelación** | |
| **3.** El mentor completa la selección de tema, especifica la fecha y hora programada, selecciona la modalidad, ingresa el número de vacantes deseadas y hace clic en el botón `"Verificar y Publicar"`. | **4.** En `OfferPublishView.tsx`, se ejecutan validaciones previas de formulario. En `offerService.ts`, se despacha `POST /api/v1/offers/publish` con el payload `OfferCreateRequest`. En `offers.py`, el controlador recibe la petición y delega a `offer_service.py`. El servicio valida: 1) que todos los campos requeridos estén completos, 2) que `fecha_inicio >= now_utc + timedelta(hours=24)` (RN-04), 3) que `aforo_maximo <= 10` si la modalidad es `PRESENCIAL` o `aforo_maximo <= 20` si es `VIRTUAL` (RN-05). (Si faltan campos obligatorios o la sintaxis es inválida, salta a E001). (Si la fecha es inferior a 24 horas de antelación, salta a E002). (Si el aforo sobrepasa los límites institucionales de 10 o 20 cupos, salta a E003). |
| **Fase 3: Verificación de concurrencia de horarios y persistencia transaccional** | |
| **5.** El mentor espera la confirmación visual en el botón que presenta un indicador circular de procesamiento. | **6.** En `offer_service.py`, se ejecuta una consulta transaccional `SELECT count(*) FROM sesiones_mentoria WHERE id_mentor = :mid AND estado IN ('PUBLICADA', 'CONFIRMADA') AND NOT (fecha_fin <= :inicio OR fecha_inicio >= :fin)`. Si se seleccionó aula presencial, se verifica que no esté ocupada por otra sesión en ese intervalo. Si es virtual, se valida que el enlace pertenezca al dominio universitario. El backend ejecuta `INSERT INTO sesiones_mentoria (...) VALUES (...)`, confirma la transacción con `db.commit()` y retorna HTTP 201 Created con el payload `OfferResponse`. En `OfferPublishView.tsx`, se limpia el formulario, se despliega una tarjeta de confirmación en color verde con el código generado de sesión y el botón `"Ver en Cartelera"`. (Si existe traslape de horario para el mentor o en el aula solicitada, salta a E004). (Si el enlace de videoconferencia es inválido, salta a E005). |

##### Flujos de Excepción

##### Flujo de excepción E001: Campos obligatorios incompletos o inválidos
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador Pydantic `OfferCreateRequest` en `offers.py` detecta omisión de campos requeridos (e.g. tema curricular o modalidad ausente). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Todos los campos de la sesión son obligatorios.")`.<br><br>En `OfferPublishView.tsx`, se capturan los errores de validación y se resaltan los campos observados con un borde en color rojo y texto explicativo. |
| **E001-1.2** Corrige los campos observados completando los datos requeridos. | **E001-1.3** Rehabilita el botón `"Verificar y Publicar"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Incumplimiento de antelación mínima de 24 horas
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `offer_service.py` evalúa `fecha_inicio < now_utc + timedelta(hours=24)` (violación de RN-04). Lanza `HTTPException(status_code=400, detail="INSUFFICIENT_ADVANCE_TIME: Las ofertas de mentoría deben programarse con un mínimo de 24 horas de antelación.")`.<br><br>En `OfferPublishView.tsx`, se despliega un panel de advertencia en color rojo destacando que no se permite publicar sesiones con menos de 24 horas de margen para garantizar la convocatoria de estudiantes. Presenta el botón `<button onClick={handleAdjustDate}>Ajustar Fecha</button>`. |
| **E002-1.2** Hace clic en el botón "Ajustar Fecha". | **E002-1.3** Asigna el foco al selector de fecha y hora, sugiriendo una fecha válida posterior a 24 horas, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Aforo sobrepasa los límites institucionales
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `offer_service.py` detecta que el valor de aforo ingresado excede el límite máximo institucional establecido en RN-05 (aforo > 10 para modalidad presencial o aforo > 20 para virtual). Lanza `HTTPException(status_code=400, detail="CAPACITY_EXCEEDED: El aforo máximo permitido es de 10 estudiantes en modalidad presencial y 20 en modalidad virtual.")`.<br><br>En `OfferPublishView.tsx`, se despliega un mensaje de error en color rojo junto al campo de vacantes indicando el límite reglamentario. |
| **E003-1.2** Ajusta el número de vacantes al rango permitido (1 a 10 en presencial o 1 a 20 en virtual). | **E003-1.3** Actualiza el valor en el estado del componente y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E004: Conflicto de horario o traslape de espacio físico
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 6 del Flujo Normal, la consulta de solapamiento en `offer_service.py` detecta que el mentor ya tiene una sesión programada en ese bloque horario, o que el aula física seleccionada se encuentra reservada. Lanza `HTTPException(status_code=409, detail="SCHEDULE_CONFLICT: Existe un traslape de horario con otra sesión programada del mentor o el aula física ya se encuentra ocupada.")`.<br><br>En `OfferPublishView.tsx`, se captura el error 409 y se despliega una alerta en color ámbar explicando el conflicto de horario. Presenta el botón `<button onClick={handleReschedule}>Cambiar Horario o Aula</button>`. |
| **E004-1.2** Hace clic en el botón "Cambiar Horario o Aula". | **E004-1.3** Habilita nuevamente los selectores de franja horaria y aula, y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Enlace de videoconferencia virtual inválido
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 6 del Flujo Normal, para modalidad virtual, `offer_service.py` valida la URL de reunión contra patrones autorizados institucionales (e.g. `meet.google.com`). Si la URL no coincide con el dominio institucional autorizado, lanza `HTTPException(status_code=400, detail="INVALID_MEETING_URL: El enlace de videoconferencia debe pertenecer a la plataforma institucional Google Meet.")`.<br><br>En `OfferPublishView.tsx`, se resalta el cuadro de texto del enlace en color rojo con el mensaje de dominio no autorizado. |
| **E005-1.2** Ingresa un enlace válido de videoconferencia universitaria. | **E005-1.3** Valida la estructura del enlace en cliente y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-008 - Consultar disponibilidad de espacios y recursos

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-008** (CUS-008) |
| **Nombre** | Consultar disponibilidad de espacios físicos y aulas de la EPIS |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-009 (Aprovisionamiento automatizado de infraestructura), RF-010 (Procesamiento de cronogramas y horarios institucionales); RN-06 (Prevención de colisión horaria de espacios), RN-07 (Horario operativo institucional 08:00 - 20:00) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores y administradores consultar en tiempo real la disponibilidad de aulas físicas, laboratorios y salas de estudio de la EPIS-UPT antes de programar una sesión presencial. El frontend `OfferPublishView.tsx` invoca a `offerService.ts` despachando una petición `GET /api/v1/offers/spaces/availability` con parámetros de fecha y rango horario. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` delega a `app/services/offer_service.py`, el cual valida que la franja horaria se sitúe estrictamente dentro del horario operativo de la universidad (08:00 a 20:00 horas conforme a RN-07) y consulta las sesiones activas en `sesiones_mentoria` junto con el cronograma académico institucional. Retorna un listado de espacios disponibles con aforo y equipamiento, o sugiere alternativas de modalidad virtual si los espacios físicos se encuentran saturados. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-04: Planificación, Espacios y Agendamiento)<br>Manual de Uso de Infraestructura y Laboratorios EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/OfferPublishView.tsx` (Subcomponente de consulta de aulas)<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.checkSpaceAvailability`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`GET /api/v1/offers/spaces/availability`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.check_space_availability`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional activo.<br>2. Catálogo institucional de aulas físicas y laboratorios registrado en el sistema.<br>3. Fecha de consulta fijada en día hábil académico universitario. |
| **PostCondiciones** | 1. Respuesta JSON generada con la nómina de aulas libres, aforos máximos y recursos audiovisuales disponibles.<br>2. Ninguna mutación destructiva o bloqueo persistente generado en base de datos (operación de lectura idempotente).<br>3. Despliegue interactivo en la interfaz cliente para selección de aula por parte del usuario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Definición de criterios temporales y despacho de consulta** | |
| **1.** El mentor selecciona la fecha proyectada y la franja horaria (hora de inicio y hora de fin) en el selector de espacios de `OfferPublishView.tsx` y hace clic en `"Consultar Aulas Disponibles"`. | **2.** En `offerService.ts`, se valida que la franja horaria se encuentre dentro de la jornada universitaria institucional de 08:00 a 20:00 horas (RN-07). Despacha una petición `GET /api/v1/offers/spaces/availability?date=...&start_time=...&end_time=...`. En `offers.py`, el controlador valida los parámetros y delega a `offer_service.py`. (Si el horario ingresado se encuentra fuera del rango institucional de 08:00 a 20:00, salta a E001). |
| **Fase 2: Verificación de ocupación en base de datos y renderización de resultados** | |
| **3.** El mentor espera la respuesta mientras el componente visualiza un indicador de carga en color azul institucional. | **4.** En `offer_service.py`, se ejecuta una consulta para excluir aulas con sesiones activas en ese bloque: `SELECT a.id, a.codigo, a.capacidad, a.equipamiento FROM aulas a WHERE a.activa = true AND a.id NOT IN (SELECT aula_id FROM sesiones_mentoria WHERE fecha = :fecha AND NOT (hora_fin <= :start OR hora_inicio >= :end) AND estado IN ('PUBLICADA', 'CONFIRMADA'))`. Retorna HTTP 200 con la lista de aulas libres. En cliente, `OfferPublishView.tsx` renderiza una cuadrícula de tarjetas de aulas indicando aforo, ubicación y equipamiento. (Si todas las aulas físicas se encuentran ocupadas en ese bloque, salta a A001). (Si el repositorio de infraestructura reporta falla de comunicación, salta a E002). |
| **5.** El mentor hace clic en el aula física deseada y presiona el botón `"Asignar Aula a la Oferta"`. | **6.** El componente asigna el identificador del aula al formulario de publicación, actualiza el indicador visual en color verde con el texto *"Aula reservada provisionalmente"* y habilita el avance del flujo de publicación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Aulas físicas agotadas con sugerencia de modalidad virtual
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, la consulta retorna cero aulas libres para el horario solicitado. | **A001-1.2** En `OfferPublishView.tsx`, se despliega un panel informativo en color ámbar: *"Todas las aulas físicas se encuentran ocupadas en la franja horaria seleccionada. Se sugiere cambiar a Modalidad Virtual o modificar la hora de inicio"*. Presenta el botón `<button onClick={handleSwitchToVirtual}>Cambiar a Modalidad Virtual</button>` y el botón `<button onClick={handleAdjustTime}>Modificar Horario</button>`. |
| **A001-1.3** El mentor hace clic en el botón "Cambiar a Modalidad Virtual". | **A001-1.4** El sistema conmuta la modalidad de la sesión a `VIRTUAL`, habilita el campo para enlace de Google Meet, actualiza el límite de aforo a 20 estudiantes (RN-05) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horario fuera de la jornada institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `offer_service.py` comprueba que la hora de inicio es anterior a las 08:00 o la hora de fin posterior a las 20:00 (infracción de RN-07). Lanza `HTTPException(status_code=400, detail="OPERATIONAL_HOURS_VIOLATION: El servicio de infraestructura opera estrictamente entre las 08:00 y las 20:00 horas.")`.<br><br>En `OfferPublishView.tsx`, se captura el error y se muestra una advertencia en color rojo indicando que la universidad no permite el uso de aulas físicas fuera de la jornada reglamentaria. |
| **E001-1.2** Modifica la franja horaria seleccionando un horario dentro de las 08:00 y 20:00. | **E001-1.3** Actualiza los valores en el selector y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Falla de conexión con el repositorio de infraestructura
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional hacia el catálogo de aulas sufre timeout o interrupción de conexión. Lanza `HTTPException(status_code=503, detail="INFRASTRUCTURE_UNAVAILABLE: No se pudo verificar la disponibilidad de espacios físicos. Intente nuevamente en unos minutos.")`.<br><br>En `OfferPublishView.tsx`, se muestra un mensaje de alerta en color rojo indicando la indisponibilidad temporal del servicio. Presenta el botón `<button onClick={handleRetryCheck}>Reintentar Consulta</button>`. |
| **E002-1.2** Hace clic en el botón "Reintentar Consulta". | **E002-1.3** Dispara nuevamente la petición `GET /api/v1/offers/spaces/availability` y retorna al paso 1 del Flujo Normal de Eventos. |


---

### MOD-03: Perfil del Mentor y Plan de Aprendizaje

#### CUS-005 - Gestionar perfil formativo y disponibilidad horaria

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-005** (CUS-005) |
| **Nombre** | Gestionar perfil académico formativo y matriz de disponibilidad horaria semanal |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-004 (Configuración de perfil formativo y matriz horaria); RN-03 (Requisitos académicos de mentor: ciclo >= V y promedio), RN-04 (Antelación de planificación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador de Carrera |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los mentores configurar su reseña académica, áreas de competencia disciplinar y su matriz semanal de disponibilidad horaria (lunes a sábado de 08:00 a 20:00) a través del componente cliente `ProfileAvailabilityView.tsx` y el servicio `profileService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/profiles.py` y `app/services/profile_service.py` procesan las peticiones `GET /api/v1/profiles/me` y `PUT /api/v1/profiles/me`, validando los datos con Pydantic (`ProfileUpdateRequest`), verificando que el usuario pertenezca al quinto ciclo académico o superior, y persistiendo de forma atómica en las entidades ORM `PerfilAcademico` y `DisponibilidadHoraria` (`app/models/profile.py`). Las franjas horarias registradas son utilizadas posteriormente por el motor de recomendaciones y el validador de ofertas para evitar traslapes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan Curricular de la Carrera Profesional de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/ProfileAvailabilityView.tsx`<br>`aplicacion/frontend/src/services/profileService.ts` (`ProfileService`, `ApiProfileAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/profiles.py` (`GET /api/v1/profiles/me`, `PUT /api/v1/profiles/me`, `POST /api/v1/profiles/availability`)<br>`aplicacion/backend/app/services/profile_service.py` (`ProfileService.get_profile`, `ProfileService.update_profile`, `ProfileService.save_availability`)<br>`aplicacion/backend/app/models/profile.py` (`PerfilAcademico`, `DisponibilidadHoraria`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `UserRole.mentor` verificado en el token JWT.<br>2. El estudiante mentor se encuentra matriculado en el semestre lectivo en curso y cumple el requisito de ciclo >= V.<br>3. Catálogo de cursos y asignaturas filtro activo en base de datos. |
| **PostCondiciones** | 1. Registros actualizados en las tablas físicas `perfiles_academicos` y `disponibilidad_horaria`.<br>2. Transacción confirmada en PostgreSQL y matriz horaria serializada para el motor de recomendación.<br>3. Despliegue de notificación de éxito en la interfaz y actualización del perfil en caché del frontend. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del perfil académico y visualización de la matriz horaria** | |
| **1.** El mentor hace clic en la pestaña `"Mi Perfil y Disponibilidad"` en `ProfileAvailabilityView.tsx`. | **2.** En `profileService.ts`, se despacha la petición `GET /api/v1/profiles/me` con la cabecera `Authorization: Bearer <token>`. En `profiles.py`, se extrae el correo del claim `sub` y `profile_service.py` ejecuta `SELECT p.*, d.* FROM perfiles_academicos p LEFT JOIN disponibilidad_horaria d ON p.id = d.perfil_id WHERE p.usuario_id = :uid`. Retorna HTTP 200 con el perfil, materias de dominio y bloques horarios semanales. `ProfileAvailabilityView.tsx` renderiza el formulario con biografía, materias acreditadas y una matriz interactiva semanal (lunes a sábado, bloques de una hora de 08:00 a 20:00). |
| **Fase 2: Edición de datos formativos y selección de bloques de disponibilidad** | |
| **3.** El mentor actualiza su biografía pedagógica, selecciona o deselecciona las asignaturas que domina, y hace clic sobre los bloques horarios en la cuadrícula semanal para alternar su estado entre disponible (resaltado en color verde) y no disponible (en color neutro). | **4.** En `ProfileAvailabilityView.tsx`, se actualiza el estado local `availabilitySlots`. El mentor presiona el botón `"Guardar Cambios y Disponibilidad"`. El componente valida que la biografía no exceda 500 caracteres y que se haya marcado al menos un bloque horario semanal. (Si no se selecciona ningún bloque de disponibilidad en toda la semana, salta a E001). (Si la biografía excede el límite de caracteres o contiene caracteres inválidos, salta a E002). |
| **Fase 3: Persistencia transaccional de disponibilidad y perfil** | |
| **5.** El mentor espera la confirmación visual mientras el botón muestra un indicador circular de guardado. | **6.** En `profileService.ts`, se despacha `PUT /api/v1/profiles/me` con el payload `ProfileUpdateRequest`. En `profiles.py`, `profile_service.py` inicia una transacción ACID con `db.begin()`. Actualiza `perfiles_academicos`, elimina los bloques horarios previos en `disponibilidad_horaria` para ese perfil e inserta los nuevos registros `(perfil_id, dia_semana, hora_inicio, hora_fin)`. Ejecuta `db.commit()` y retorna HTTP 200 con el perfil actualizado. `ProfileAvailabilityView.tsx` despliega una alerta flotante en color verde: *"Perfil y disponibilidad horaria actualizados exitosamente"*. (Si ocurre un conflicto de concurrencia o violación de clave única en base de datos, salta a E003). |

##### Flujos de Excepción

##### Flujo de excepción E001: Matriz de disponibilidad horaria semanal vacía
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en `ProfileAvailabilityView.tsx` o `profile_service.py` comprueba que el conjunto de bloques horarios seleccionados está vacío (`len(slots) == 0`). Lanza `HTTPException(status_code=400, detail="EMPTY_SCHEDULE: Debe seleccionar al menos un bloque horario semanal de disponibilidad para ofrecer mentorías.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta la cuadrícula horaria con un borde en color rojo y se despliega una advertencia en color ámbar solicitando marcar al menos una hora disponible. |
| **E001-1.2** Hace clic sobre al menos un bloque horario en la cuadrícula interactiva. | **E001-1.3** Conmuta el bloque a disponible (color verde), rehabilita el botón `"Guardar Cambios"` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Biografía o formato de enlaces no válido
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic detecta que el campo biografía excede 500 caracteres o contiene scripts no autorizados. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: La reseña formativa no debe exceder 500 caracteres ni contener etiquetas HTML.")`.<br><br>En `ProfileAvailabilityView.tsx`, se resalta el cuadro de texto de biografía en color rojo indicando el error de validación. |
| **E002-1.2** Modifica el texto ajustándolo al límite permitido de caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Conflicto de concurrencia al actualizar perfil
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 6 del Flujo Normal, una sesión concurrente modifica el mismo perfil provocando un conflicto de versión en base de datos. `profile_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CONCURRENCY_CONFLICT: El perfil fue actualizado desde otra sesión. Se recargarán los datos más recientes.")`.<br><br>En `ProfileAvailabilityView.tsx`, se captura el error 409 y se despliega un aviso en color ámbar. Presenta el botón `<button onClick={fetchProfile}>Recargar Perfil</button>`. |
| **E003-1.2** Hace clic en el botón "Recargar Perfil". | **E003-1.3** Invoca nuevamente `GET /api/v1/profiles/me`, actualiza el formulario con el estado más reciente y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-021 - Explorar catálogo curricular de asignaturas filtro

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-021** (CUS-021) |
| **Nombre** | Explorar catálogo curricular jerárquico de asignaturas y materias críticas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios); RN-11 (Priorización y catálogo oficial de asignaturas filtro EPIS) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado, Estudiante Mentor, Coordinador Curricular |
| **Interacción** | Fase de Construcción / Iteración Sprint 02 - Sprint 03 |
| **Descripción** | Permite a los estudiantes mentoreados y mentores navegar interactivamente por la malla curricular oficial de la EPIS-UPT a través del componente cliente `CurriculumCatalogView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` proporcionan consultas estructuradas por carrera (`Carrera`), ciclo académico (I al X), curso (`Curso`) y temas de aprendizaje silábico (`TemaCurricular`), destacando visualmente las asignaturas identificadas institucionalmente como "materias filtro" (`es_filtro = true`, tales como Algoritmos, Estructuras de Datos, Base de Datos y Programación Orientada a Objetos). Desde cada tema curricular, el mentoreado puede consultar directamente las ofertas de mentoría activas o solicitar la apertura de una sesión por demanda. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Malla Curricular Oficial de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/CurriculumCatalogView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService`, `ApiCurriculumAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`GET /api/v1/curriculum/careers`, `GET /api/v1/curriculum/courses`, `GET /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.get_courses`, `CurriculumService.get_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Usuario con sesión institucional iniciada en la plataforma.<br>2. Malla curricular y temarios silábicos cargados y versionados en la base de datos PostgreSQL.<br>3. Identificación institucional de cursos filtro debidamente clasificada en la columna `es_filtro`. |
| **PostCondiciones** | 1. Despliegue interactivo del catálogo jerárquico de asignaturas y temas silábicos en la interfaz.<br>2. Consulta idempotente de sólo lectura ejecutada sin mutaciones en base de datos.<br>3. Posibilidad de derivación directa hacia la reserva de mentoría (CUS-004) o registro de demanda (CUS-003). |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Navegación por ciclo académico y selección de asignatura** | |
| **1.** El usuario hace clic en el enlace `"Catálogo Curricular"` del menú de navegación principal en `CurriculumCatalogView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` ejecuta `SELECT c.*, count(t.id) as total_temas FROM cursos c LEFT JOIN temas_curriculares t ON c.id = t.curso_id WHERE c.activo = true GROUP BY c.id ORDER BY c.ciclo, c.nombre`. Retorna HTTP 200 con la lista completa de cursos. `CurriculumCatalogView.tsx` renderiza las asignaturas agrupadas por ciclo académico (del ciclo I al X), destacando las asignaturas filtro con una insignia visual en color azul institucional con la leyenda *"Materia Filtro Prioritaria"*. (Si el repositorio curricular sufre indisponibilidad o timeout, salta a E001). |
| **Fase 2: Búsqueda y filtrado interactivo de cursos** | |
| **3.** El usuario introduce el nombre de una materia o código en el cuadro de búsqueda `"Buscar asignatura o tema"` y aplica el filtro por ciclo. | **4.** En `CurriculumCatalogView.tsx`, se filtra reactivamente la nómina de cursos en el estado de la vista. El usuario hace clic en la tarjeta de la asignatura de su interés para inspeccionar su estructura temática. (Si ningún curso coincide con los términos de búsqueda ingresados, salta a A001). |
| **Fase 3: Despliegue de temarios silábicos y vinculación con mentorías** | |
| **5.** El usuario hace clic sobre la tarjeta de un curso específico (e.g. Algoritmos y Estructuras de Datos). | **6.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses/{course_id}/topics`. El backend retorna los temas clasificados por unidad didáctica con número de semana, descripción y cantidad de ofertas activas. `CurriculumCatalogView.tsx` expande un panel acordeón desplegando la lista de temas silábicos, cada uno con el botón `"Ver Ofertas Disponibles"` y el botón `"Solicitar Demanda"`. |

##### Flujos Alternativos

##### Flujo alternativo A001: Búsqueda curricular sin coincidencias
| Usuario | Sistema |
|---|---|
| **A001-1.1** El usuario introduce en el paso 3 un término de búsqueda que no produce coincidencias en el catálogo. | **A001-1.2** En `CurriculumCatalogView.tsx`, se ocultan las tarjetas y se renderiza un panel centrado con un ícono informativo y el texto: *"No se encontraron asignaturas o temas que coincidan con la búsqueda. Intente con otro término o seleccione un ciclo específico"*. Presenta el botón `<button onClick={handleResetFilter}>Restablecer Filtros</button>`. |
| **A001-1.3** Hace clic en el botón "Restablecer Filtros". | **A001-1.4** Limpia el cuadro de búsqueda, muestra nuevamente todas las asignaturas por ciclo y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de conexión con el repositorio curricular
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, la consulta hacia las tablas `cursos` y `temas_curriculares` sufre una pérdida de conexión en PostgreSQL. Lanza `HTTPException(status_code=503, detail="CURRICULUM_SERVICE_UNAVAILABLE: El repositorio curricular no se encuentra disponible temporalmente. Reintente en unos instantes.")`.<br><br>En `CurriculumCatalogView.tsx`, se captura el error 503 y se despliega un panel de alerta en color ámbar indicando la imposibilidad de cargar la malla curricular. Presenta el botón `<button onClick={fetchCurriculum}>Reintentar Carga</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Carga". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/curriculum/courses` y retorna al paso 1 del Flujo Normal de Eventos. |


---

### MOD-04: Demanda y Recomendaciones Personalizadas

#### CUS-002 - Explorar recomendaciones personalizadas Top-k

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-002** (CUS-002) |
| **Nombre** | Explorar cartelera inteligente de recomendaciones de mentoría Top-k |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-006 (Inferencia de recomendaciones y ranking Top-k); RN-04 (Ventana de antelación mínima de 24 horas), RN-11 (Ponderación algorítmica de asignaturas filtro) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite a los estudiantes mentoreados visualizar una cartelera adaptativa de sesiones de mentoría clasificadas según su relevancia académica individual mediante el componente cliente `RecommendationFeedView.tsx` y el servicio `recommendationService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/recommendations.py` procesa la petición `GET /api/v1/recommendations/top-k?limit=6`, delegando al servicio `app/services/recommendation_service.py`. El motor analiza el vector de intereses y asignaturas matriculadas del estudiante extraído de `perfiles_academicos`, computa la similitud de cosenos respecto a las sesiones en estado `PUBLICADA` con antelación mayor a 24 horas (`fecha_inicio > now_utc + 24h`, RN-04), aplica bonificaciones para materias filtro (`es_filtro = true`, RN-11) y penaliza sesiones con aforo próximo a agotarse. Retorna una nómina ordenada de las mejores k recomendaciones serializadas en el modelo Pydantic `TopKRecommendationResponse`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-03: Motor de Recomendación Inteligente EdRecSys)<br>Algoritmos de Recomendación Basados en Contenido y Filtrado Híbrido |
| **Anexos** | `aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/recommendationService.ts` (`RecommendationService`, `ApiRecommendationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`GET /api/v1/recommendations/top-k`)<br>`aplicacion/backend/app/services/recommendation_service.py` (`RecommendationService.get_top_k_recommendations`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/profile.py` (`PerfilAcademico`), `app/models/curriculum.py` (`Curso`, `TemaCurricular`) |
| **Precondiciones** | 1. Estudiante mentoreado autenticado con token JWT institucional activo en `localStorage`.<br>2. Al menos una sesión de mentoría en estado `PUBLICADA` con antelación superior a 24 horas y vacantes disponibles.<br>3. Registro de perfil académico o cursos matriculados en la base de datos. |
| **PostCondiciones** | 1. Payload JSON serializado con las k sesiones más afines y sus puntuaciones de compatibilidad retornadas al frontend.<br>2. Consulta de lectura sin efectos colaterales persistentes ni mutaciones de datos en PostgreSQL.<br>3. Despliegue de la cartelera interactiva con tarjetas informativas y botones de reserva activados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la cartelera y solicitud de recomendaciones Top-k** | |
| **1.** El mentoreado accede a la página principal de la plataforma en `RecommendationFeedView.tsx`. | **2.** En `recommendationService.ts`, se despacha `GET /api/v1/recommendations/top-k?limit=6` incluyendo el token Bearer institucional. En `recommendations.py`, el controlador extrae el UUID del usuario del token JWT y delega a `recommendation_service.py`. El servicio recupera el perfil académico del estudiante y sus materias matriculadas. (Si el estudiante no registra historial ni materias configuradas, salta a A001). (Si el motor de recomendación sufre una excepción de cálculo o timeout, salta a E001). |
| **Fase 2: Ejecución del algoritmo de emparejamiento y ordenamiento de compatibilidad** | |
| **3.** El usuario visualiza un esqueleto animado de tarjetas mientras se calculan las recomendaciones. | **4.** En `recommendation_service.py`, se recuperan las sesiones en estado `PUBLICADA` con `fecha_inicio > now_utc + timedelta(hours=24)` y `occupied_seats < aforo_maximo`. Para cada oferta, se calcula el puntaje ponderado: $Score = 0.5 	imes SimilitudCursos + 0.3 	imes FactorFiltro + 0.2 	imes UrgenciaTemporal$. Se ordenan de forma descendente y se toman las primeras 6 ofertas. Retorna HTTP 200 con el payload `TopKRecommendationResponse`. En cliente, `RecommendationFeedView.tsx` renderiza las tarjetas con: nombre del tema curricular, nombre de la asignatura, fecha y hora de la sesión, modalidad (Presencial/Virtual con aula o enlace), número de vacantes restantes y un distintivo en color azul institucional indicando el porcentaje de compatibilidad (e.g. *"95% de afinidad"*). (Si no existen ofertas activas para sus materias, salta a A002). |
| **Fase 3: Selección de sesión para reserva de cupo** | |
| **5.** El mentoreado revisa las tarjetas de recomendación y hace clic en el botón `"Reservar Cupo"` de la sesión de su preferencia. | **6.** En `RecommendationFeedView.tsx`, se captura el identificador de la sesión seleccionada y se abre el componente modal `BookingModalView.tsx`, transfiriendo el flujo a la especificación técnica de reserva formal de cupo (CUS-004). |

##### Flujos Alternativos

##### Flujo alternativo A001: Estudiante nuevo sin historial académico (Fallback por popularidad)
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, `recommendation_service.py` detecta que el estudiante no tiene historial académico ni materias configuradas en su perfil. | **A001-1.2** El servicio conmuta automáticamente a la estrategia de respaldo ("Cold Start"): ejecuta una consulta para seleccionar las sesiones de mentoría más populares y con mayor demanda en asignaturas filtro generales de los primeros ciclos (`es_filtro = true`). |
| **A001-1.3** El estudiante visualiza las tarjetas de oferta acompañadas de una insignia informativa en color ámbar: *"Ofertas destacadas para estudiantes de primeros ciclos"*. | **A001-1.4** El sistema presenta el botón `<button onClick={handleConfigureProfile}>Configurar Mis Materias</button>` para personalizar futuras recomendaciones y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo alternativo A002: Cartelera vacía por ausencia de sesiones disponibles
| Usuario | Sistema |
|---|---|
| **A002-1.1** En el paso 4 del Flujo Normal, la consulta de sesiones publicadas retorna cero registros con vacantes disponibles. | **A002-1.2** En `RecommendationFeedView.tsx`, se despliega un panel centralizado con un ícono ilustrativo en color azul institucional y el texto: *"No hay sesiones de mentoría programadas actualmente para tus materias. Puedes solicitar la apertura de un tema registrando tu demanda académica"*. Presenta el botón `<button onClick={handleOpenDemandModal}>Registrar Solicitud por Demanda</button>`. |
| **A002-1.3** El estudiante hace clic en el botón "Registrar Solicitud por Demanda". | **A002-1.4** El sistema abre el modal de registro de demanda académica (CUS-003) y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujos de Excepción

##### Flujo de excepción E001: Error de cómputo en el motor de recomendación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el servicio `recommendation_service.py` encuentra una falla de serialización de vectores o un timeout interno en base de datos. Lanza `HTTPException(status_code=500, detail="RECOMMENDER_ENGINE_ERROR: Ocurrió un error al procesar las recomendaciones personalizadas.")`.<br><br>En `RecommendationFeedView.tsx`, se captura el error 500 y se despliega un panel de advertencia en color rojo. Presenta el botón `<button onClick={fetchRecommendations}>Reintentar Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Reintentar Cartelera". | **E001-1.3** Dispara nuevamente la petición `GET /api/v1/recommendations/top-k` y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-003 - Registrar solicitud de demanda académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-003** (CUS-003) |
| **Nombre** | Registrar solicitud de mentoría por demanda académica no atendida |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-007 (Registro y banco de solicitudes por demanda); RN-04 (Antelación de planificación institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 03 - Sprint 04 |
| **Descripción** | Permite a los estudiantes mentoreados expresar una necesidad formativa insatisfecha cuando no existen ofertas disponibles sobre un tema curricular específico a través del formulario modal en `RecommendationFeedView.tsx` y el servicio `recommendationService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/recommendations.py` y `app/services/recommendation_service.py` procesan la petición `POST /api/v1/recommendations/demand`, validando los campos con Pydantic (`DemandCreateRequest`). El sistema verifica que el estudiante no cuente con una solicitud idéntica en estado `PENDIENTE` para el mismo tema, persiste el registro en la tabla `demandas_academicas` e incrementa el contador de demanda agrupada en caché para alertar a los mentores calificados en su panel de publicación (CUS-006). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-03: Motor de Recomendación Inteligente EdRecSys)<br>Gestión de Demanda Académica EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/RecommendationFeedView.tsx` (Subcomponente de Solicitud de Demanda)<br>`aplicacion/frontend/src/services/recommendationService.ts` (`RecommendationService.createDemand`)<br>`aplicacion/backend/app/api/v1/endpoints/recommendations.py` (`POST /api/v1/recommendations/demand`)<br>`aplicacion/backend/app/services/recommendation_service.py` (`RecommendationService.create_demand_request`)<br>`aplicacion/backend/app/models/curriculum.py` (`TemaCurricular`), `app/models/profile.py` (`DemandaAcademica`) |
| **Precondiciones** | 1. Mentoreado autenticado con token JWT institucional activo.<br>2. Tema curricular seleccionado perteneciente a una asignatura vigente en el catálogo oficial.<br>3. Inexistencia de solicitud pendiente previa idéntica del mismo estudiante para dicho tema. |
| **PostCondiciones** | 1. Registro insertado en la tabla `demandas_academicas` con `estado = 'PENDIENTE'` y marca de tiempo UTC.<br>2. Incremento atómico del acumulador de solicitudes del tema para priorización algorítmica.<br>3. Notificación de confirmación en cliente y cierre del modal de demanda. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura del formulario de demanda y selección temática** | |
| **1.** El mentoreado hace clic en el botón `"Registrar Demanda de Tema"` en la cabecera de `RecommendationFeedView.tsx` o en el catálogo curricular. | **2.** El sistema abre una ventana modal `"Solicitud de Mentoría por Demanda"`. Despacha la consulta de asignaturas y temas silábicos para poblar las listas desplegables. Renderiza los campos: selección de curso, tema curricular específico, franja horaria preferida (mañana, tarde o noche), modalidad predilecta (Presencial/Virtual) y un cuadro de texto para comentarios adicionales. |
| **Fase 2: Ingreso de preferencias y despacho de solicitud** | |
| **3.** El mentoreado selecciona la asignatura, el tema silábico específico, marca su franja horaria predilecta y presiona el botón `"Enviar Solicitud"`. | **4.** En `RecommendationFeedView.tsx`, se valida que se hayan seleccionado la materia y el tema. En `recommendationService.ts`, se despacha `POST /api/v1/recommendations/demand` con el payload `DemandCreateRequest`. En `recommendations.py`, `recommendation_service.py` ejecuta una verificación para descartar duplicados activos: `SELECT id FROM demandas_academicas WHERE estudiante_id = :uid AND tema_id = :tid AND estado = 'PENDIENTE'`. (Si faltan campos obligatorios en el formulario, salta a E001). (Si el estudiante ya cuenta con una solicitud pendiente para el mismo tema, salta a E002). |
| **Fase 3: Registro transaccional e indexación de demanda grupal** | |
| **5.** El mentoreado visualiza el indicador de procesamiento en el botón de envío. | **6.** En `recommendation_service.py`, se ejecuta `INSERT INTO demandas_academicas (estudiante_id, tema_id, franja_preferida, modalidad_preferida, estado, fecha_solicitud) VALUES (...)`. Se confirma la transacción con `db.commit()` y se actualiza el agregado de solicitudes por tema en caché. Retorna HTTP 201 Created con el objeto `DemandResponse`. En cliente, `RecommendationFeedView.tsx` cierra el modal y despliega una notificación flotante en color verde de éxito: *"Tu solicitud de demanda ha sido registrada exitosamente. Los mentores habilitados recibirán una alerta sobre la necesidad formativa de este tema."* |

##### Flujos de Excepción

##### Flujo de excepción E001: Formulario de demanda incompleto
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en cliente o Pydantic en `recommendations.py` comprueba que no se ha seleccionado tema o asignatura. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Debe seleccionar obligatoriamente una materia y tema curricular para registrar su demanda.")`.<br><br>En el modal de demanda, se resaltan los campos vacíos con borde en color rojo y texto explicativo. |
| **E001-1.2** Selecciona la asignatura y el tema silábico en los desplegables. | **E001-1.3** Rehabilita el botón `"Enviar Solicitud"` y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Solicitud duplicada de demanda pendiente
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `recommendation_service.py` detecta un registro previo en estado `PENDIENTE` para la misma tupla `(estudiante_id, tema_id)`. Lanza `HTTPException(status_code=409, detail="DUPLICATE_DEMAND: Ya mantienes una solicitud activa registrada para este tema. Los mentores ya pueden visualizar esta necesidad formativa.")`.<br><br>En el modal, se despliega una alerta en color ámbar explicando la existencia previa de la solicitud. Presenta el botón `<button onClick={handleCloseModal}>Entendido</button>`. |
| **E002-1.2** Hace clic en el botón "Entendido". | **E002-1.3** Cierra la ventana modal sin generar registros redundantes y retorna al paso 1 del Flujo Normal de Eventos. |


---

### MOD-05: Quórum, Confirmación y Cancelaciones

#### CUS-004 - Reservar cupo de mentoría académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-004** (CUS-004) |
| **Nombre** | Reservar cupo de mentoría académica con control de aforo y concurrencia |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-012 (Reserva de cupos con control de aforo y concurrencia; trazabilidad técnica hacia RF-002, RF-006, RF-013 y RF-014) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`), Administrador Institucional (`UserRole.administrador`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite formalizar una reserva provisional de cupo en estado `PENDIENTE_CONFIRMACION` mediante una petición `POST /api/v1/bookings/reserve` despachada desde el componente cliente `BookingModalView.tsx` hacia el controlador FastAPI `bookings.py`. El backend ejecuta validaciones de seguridad con `decode_access_token` en `app/core/security.py`, comprueba la vigencia del consentimiento legal con `ConsentService.get_consent_status`, adquiere el cerrojo en memoria `_booking_lock` y ejecuta una transacción en PostgreSQL bajo bloqueo pesimista de fila `SELECT ... FOR UPDATE OF sesiones_mentoria` con `SET LOCAL lock_timeout = '5.0s'`. Comprueba que `occupied_seats < sesion.aforo_maximo` (10 presencial / 20 virtual, RN-05) y la antelación mayor a 24 horas (`sesion.fecha_inicio > now_utc + 24h`, RN-04). Genera la entidad ORM `ReservaCupo` con código alfanuméricamente secuencial y hash criptográfico SHA-256 (`ticket_hash`), confirma la transacción con `db.commit()` y retorna el payload serializado `BookingResponse` (HTTP 201 Created). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Ley Nº 29733 de Protección de Datos Personales del Perú y D.S. Nº 003-2013-JUS |
| **Anexos** | `aplicacion/frontend/src/components/BookingModalView.tsx`<br>`aplicacion/frontend/src/components/RecommendationFeedView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService`, `ApiBookingAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/reserve`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.reserve_seat`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Token JWT institucional activo en `localStorage` firmado criptográficamente con claim `sub` conteniendo un correo institucional `@upt.pe`.<br>2. Registro de consentimiento persistido en la tabla `consentimientos_legales` con campo `revocado = false`.<br>3. Registro en `sesiones_mentoria` con `estado = 'PUBLICADA'` y `fecha_inicio > NOW() + INTERVAL '24 HOURS'`.<br>4. Recuento transaccional en `reservas_cupo` con estado activo menor a `aforo_maximo` (10 presencial / 20 virtual).<br>5. Inexistencia de tupla activa previa `(id_sesion, estudiante_email)` en la tabla `reservas_cupo`. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `reservas_cupo` con `estado = 'PENDIENTE_CONFIRMACION'` y hash SHA-256 (`ticket_hash`).<br>2. Transacción confirmada en PostgreSQL mediante `db.commit()` con actualización atómica de vacantes.<br>3. Notificación flotante de confirmación desplegada en cliente con código de comprobante y persistencia en la vista `"Mis Reservas"`. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Exploración en Cartelera y Apertura del Diálogo Modal** | |
| **1.** El estudiante mentoreado autenticado navega por `RecommendationFeedView.tsx` y pulsa el botón `"Reservar Cupo"` en la tarjeta correspondiente a una sesión de mentoría en estado `PUBLICADA`. | **2.** En `App.tsx`, el evento `onSelectOffer` actualiza el estado `selectedOfferForBooking`. `BookingModalView.tsx` se renderiza recibiendo las propiedades requeridas (`isOpen={true}`, `offer`, `userEmail`, `onClose`, `onSuccess`). Ejecuta el hook `useEffect` validando `offer.available_slots > 0` y la no expiración de la sesión. (Si la tarjeta quedó desfasada y registra 0 cupos, salta a E001). (Si el mentoreado ya cuenta con una reserva activa para esa misma sesión, salta a E002). |
| **Fase 2: Verificación de Precondiciones y Reglas de Negocio en Cliente** | |
| **3.** En `BookingModalView.tsx`, el usuario revisa el panel de detalles de la sesión: título del tema curricular, nombre de la asignatura, fecha y hora programada, modalidad (Presencial con aula física o Virtual con enlace Google Meet) y aforo restante. Lee la advertencia del compromiso de asistencia y pulsa el botón `"Confirmar Reserva"`. | **4.** El componente activa el estado transicional `isSubmitting = true`, deshabilita los controles del modal y muestra un indicador circular animado en color azul institucional. Lee el token Bearer en `localStorage`. Invoca al método `reserveSeat(offer.id, userEmail)` expuesto por `ApiBookingAdapter` en `bookingService.ts`. (Si el token no existe o expiró, salta a E003). (Si el usuario es el propio mentor titular de la sesión, salta a E004). (Si el usuario no ha suscrito el consentimiento legal digital, salta a E005). |
| **Fase 3: Ejecución de Transacción Atómica con Bloqueo Pesimista en Base de Datos** | |
| **5.** El usuario observa en pantalla el progreso de procesamiento seguro. | **6.** En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/reserve` con cabecera `Authorization: Bearer <token>` y cuerpo JSON `{"id_sesion": id, "estudiante_email": email}`. El controlador `bookings.py` recibe la petición, valida el esquema Pydantic `BookingCreate` e invoca `booking_service.reserve_seat(db, session_id, current_user.email)`. `booking_service.py` adquiere el cerrojo global en memoria `_booking_lock.acquire(timeout=5.0)`. Inicia la transacción ACID en PostgreSQL con `db.begin()`. Configura el cerrojo de fila con `db.execute(text("SET LOCAL lock_timeout = '5.0s'"))`. Ejecuta la consulta relacional con bloqueo pesimista exclusivo de fila: `SELECT * FROM sesiones_mentoria WHERE id = :id FOR UPDATE OF sesiones_mentoria`. Verifica que la sesión exista, mantenga el estado `PUBLICADA`, no haya sobrepasado la ventana límite de 24 horas (`sesion.fecha_inicio > now_utc + timedelta(hours=24)`, RN-04), y que el recuento de reservas activas sea menor al aforo permitido (`occupied_seats < sesion.aforo_maximo`, 10 en presencial o 20 en virtual, RN-05). Inserta el nuevo registro en `reservas_cupo` con estado `PENDIENTE_CONFIRMACION` y ticket hash criptográfico SHA-256. Confirma atómicamente la transacción mediante `db.commit()` y libera el cerrojo `_booking_lock`. Retorna HTTP 201 Created con el payload `BookingResponse`. (Si la sesión no existe en base de datos, salta a E006). (Si el estado de la sesión cambió concurrentemente a CANCELADA, salta a E007). (Si la fecha de inicio no cumple la antelación de 24 horas, salta a E008). (Si ocurre timeout en la adquisición del cerrojo, salta a E009). (Si otra transacción concurrente ocupó el último cupo disponible en el mismo milisegundo, salta a E010). |
| **Fase 4: Confirmación y Actualización Reactiva de Estados** | |
| **7.** `bookingService.ts` recibe el código HTTP 201 y deserializa la entidad de respuesta. Transfiere el control a `BookingModalView.tsx`, la cual oculta el indicador de carga y conmuta su interfaz al panel de confirmación en color verde, desplegando el código de reserva, un recordatorio de ratificación obligatoria a T-24h y el botón `"Finalizar y Ver Mis Reservas"`. | **8.** El usuario hace clic en el botón `"Finalizar y Ver Mis Reservas"`. `BookingModalView.tsx` ejecuta el callback `onSuccess()`. En `App.tsx`, se invoca `fetchOffers()` para sincronizar las vacantes en cartelera, se actualiza el estado global de reservas del estudiante y se navega a la vista `StudentBookingsView.tsx`, presentando el registro recién formalizado en estado `PENDIENTE_CONFIRMACION`. |

##### Flujos de Excepción

##### Flujo de excepción E001: Oferta en cartelera sin vacantes disponibles
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `BookingModalView.tsx` detecta `offer.available_slots <= 0`. Modifica inmediatamente su estado interno deshabilitando el botón `"Confirmar Reserva"` y mostrando un aviso en color ámbar: *"Lo sentimos, el aforo para esta sesión se ha completado. No es posible generar nuevas reservas"*. Presenta el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E001-1.2** Hace clic en el botón "Volver a la Cartelera". | **E001-1.3** Invoca el callback `onClose()`, destruye la instancia modal del árbol del DOM y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reserva duplicada activa para el mismo estudiante
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 2 del Flujo Normal, el hook `useEffect` en `BookingModalView.tsx` verifica la existencia previa de una reserva activa en el estado local de reservas del usuario. Alternativamente, en el paso 6, `booking_service.py` ejecuta `SELECT id FROM reservas_cupo WHERE id_sesion = :sid AND estudiante_email = :email AND estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA')`. Al hallar una tupla, lanza `HTTPException(status_code=400, detail="ALREADY_BOOKED: Ya posees una reserva activa registrada para esta sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error 400 con código `'ALREADY_BOOKED'`. En `BookingModalView.tsx`, renderiza una notificación en color rojo con el mensaje de duplicidad y presenta el botón `<button onClick={onClose}>Aceptar</button>`. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Cierra el cuadro modal, retorna el foco a la tarjeta de la sesión y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E003: Sesión institucional no autenticada o token expirado
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, `bookingService.ts` ejecuta `localStorage.getItem('auth_token')` y detecta valor nulo, o el backend responde con HTTP 401 Unauthorized por firma JWT vencida (`TokenExpiredError`).<br><br>En `bookingService.ts`, propaga la excepción hacia el contexto global. En `App.tsx`, el interceptor de seguridad purga el token expirado con `localStorage.removeItem('auth_token')`, conmuta el estado global `user` a `null` y monta el componente `LoginOtpView.tsx`, desplegando una alerta en color rojo: *"Su sesión institucional ha caducado por inactividad. Por favor, ingrese nuevamente mediante código OTP."* |
| **E003-1.2** Ingresa su correo institucional y solicita nuevo código de acceso. | **E003-1.3** Transfiere el control al flujo de autenticación y retorna al paso 1 del Flujo Normal de Eventos de CUS-001. |

##### Flujo de excepción E004: Conflicto de rol de mentor (Autoreserva Prohibida)
| Usuario | Sistema |
|---|---|
| | **E004-1.1** En el paso 4 del Flujo Normal, `BookingModalView.tsx` compara `offer.mentor_email === userEmail`. Alternativamente, en el paso 6, `booking_service.py` valida `sesion.id_mentor == current_user.id`. Lanza `HTTPException(status_code=400, detail="CANNOT_BOOK_OWN_SESSION: Un mentor no puede reservar cupos en su propia sesión de mentoría.")`.<br><br>En `bookingService.ts`, captura el error con código `'CANNOT_BOOK_OWN_SESSION'`. `BookingModalView.tsx` inhabilita el botón de acción y despliega una advertencia en color rojo. Presenta el botón `<button onClick={onClose}>Cerrar</button>`. |
| **E004-1.2** Hace clic en el botón "Cerrar". | **E004-1.3** Cierra el modal sin realizar peticiones de mutación y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E005: Ausencia o revocación de consentimiento legal digital
| Usuario | Sistema |
|---|---|
| | **E005-1.1** En el paso 4 del Flujo Normal, `booking_service.py` invoca a `ConsentService.get_consent_status(current_user.email)` y obtiene `has_consented = false`. Lanza `HTTPException(status_code=403, detail="CONSENT_REQUIRED: Se requiere la formalización del consentimiento legal digital bajo la Ley Nº 29733 para realizar reservas de cupos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CONSENT_REQUIRED', ...)`. En `App.tsx`, captura el error 403, oculta `BookingModalView.tsx` y monta en primer plano `ConsentModalView.tsx`, presentando los términos de tratamiento de datos personales. |
| **E005-1.2** Lee los términos legales, marca la casilla de aceptación y pulsa "Aceptar y Continuar". | **E005-1.3** Despacha `POST /api/v1/consent/accept`, persiste la traza legal, retorna el control al modal de reserva y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E006: Sesión de mentoría inexistente en el catálogo
| Usuario | Sistema |
|---|---|
| | **E006-1.1** En el paso 6 del Flujo Normal, la consulta relacional `SELECT * FROM sesiones_mentoria WHERE id = :id` retorna `None`. `booking_service.py` ejecuta `db.rollback()` y lanza `HTTPException(status_code=404, detail="SESSION_NOT_FOUND: La sesión de mentoría solicitada no existe o fue eliminada del catálogo.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_FOUND', message, 404)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para purgar la sesión obsoleta y muestra una alerta en color rojo. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E006-1.2** Hace clic en el botón "Entendido". | **E006-1.3** Cierra el diálogo modal, actualiza la cartelera eliminando la tarjeta huérfana y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E007: Sesión cancelada concurrentemente por el mentor o administración
| Usuario | Sistema |
|---|---|
| | **E007-1.1** En el paso 6 del Flujo Normal, tras adquirir el bloqueo pesimista de fila, `booking_service.py` evalúa `sesion.estado != EstadoSesion.PUBLICADA`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=400, detail="SESSION_NOT_OPEN: La sesión seleccionada no se encuentra abierta para reservas (Estado actual: CANCELADA).")`.<br><br>En `bookingService.ts`, eleva `new BookingException('SESSION_NOT_OPEN', message, 400)`. En `App.tsx`, el bloque `catch` ejecuta `setFeedRefreshKey((prev) => prev + 1)` para invalidar la oferta obsoleta y muestra una notificación en color rojo. Presenta el botón `<button onClick={onClose}>Actualizar Cartelera</button>`. |
| **E007-1.2** Hace clic en el botón "Actualizar Cartelera". | **E007-1.3** Cierra el modal, remueve la tarjeta obsoleta del DOM mediante `fetchOffers()` y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E008: Ventana de antelación vencida (Regla Institucional RN-04)
| Usuario | Sistema |
|---|---|
| | **E008-1.1** En el paso 6 del Flujo Normal, `booking_service.py` evalúa `sesion.fecha_inicio <= now_utc + timedelta(hours=24)` y lanza `HTTPException(status_code=400, detail="WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.")`.<br><br>En `bookingService.ts`, identifica `'WINDOW_CLOSED_T24H'` y eleva `new BookingException('WINDOW_CLOSED_T24H', message, 400)`. `BookingModalView.tsx` renderiza la advertencia en color rojo indicando que las inscripciones cerraron por límite de 24 horas. Presenta el botón `<button onClick={onClose}>Entendido</button>`. |
| **E008-1.2** Hace clic en el botón "Entendido". | **E008-1.3** Cierra el diálogo modal, actualiza la tarjeta mostrando el botón deshabilitado con el texto "Inscripciones Cerradas" y retorna al paso 1 del Flujo Normal de Eventos. |

##### Flujo de excepción E009: Timeout de concurrencia en adquisición de cerrojo (Database Busy)
| Usuario | Sistema |
|---|---|
| | **E009-1.1** En el paso 6 del Flujo Normal, `_booking_lock.acquire(timeout=5.0)` retorna `False` o PostgreSQL lanza excepción por timeout de cerrojo. `booking_service.py` lanza `HTTPException(status_code=503, detail="DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('DATABASE_BUSY', message, 503)`. En `App.tsx`, el bloque `catch` preserva la intención del usuario sin ejecutar rollback destructivo. `BookingModalView.tsx` rehabilita los botones y muestra un aviso en color ámbar: *"El servicio se encuentra temporalmente con alta concurrencia. No se ha generado ningún cargo. Por favor, pulsa 'Reintentar'"*. Presenta el botón `<button onClick={handleConfirmClick}>Reintentar Reserva</button>`. |
| **E009-1.2** Hace clic en el botón "Reintentar Reserva". | **E009-1.3** Dispara nuevamente la petición `bookingService.reserveSeat` y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E010: Colisión concurrente por aforo agotado en el último milisegundo
| Usuario | Sistema |
|---|---|
| | **E010-1.1** En el paso 6 del Flujo Normal, bajo el cerrojo pesimista `SELECT ... FOR UPDATE OF sesiones_mentoria`, `booking_service.py` evalúa `occupied_seats >= sesion.aforo_maximo`. Ejecuta `db.rollback()` y lanza `HTTPException(status_code=409, detail="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.")`.<br><br>En `bookingService.ts`, eleva `new BookingException('CAPACITY_EXCEEDED', 'Aforo completo o colisión con otra reserva concurrente.', 409)`. En `App.tsx`, el bloque `catch` captura `err.code === 'CAPACITY_EXCEEDED'`, ejecuta `setFeedRefreshKey((prev) => prev + 1)` para sincronizar la cartelera y despliega en `BookingModalView.tsx` un panel en color naranja de alerta indicando que la última vacante fue ocupada simultáneamente por otro usuario. Presenta el botón `<button onClick={handleGoToDemand}>Registrar Demanda de Tema</button>` y el botón `<button onClick={onClose}>Volver a la Cartelera</button>`. |
| **E010-1.2** Hace clic en el botón "Volver a la Cartelera" (o en "Registrar Demanda de Tema"). | **E010-1.3** Cierra `BookingModalView.tsx`, actualiza la tarjeta en la cartelera como "Aforo Completo (0 vacantes)" y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-024 - Ratificar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-024** (CUS-024) |
| **Nombre** | Ratificar asistencia obligatoria a sesión de mentoría académica a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-013 (Confirmación anticipada de asistencia a mentoría); RN-04 (Ventana de ratificación previa entre T-48h y T-24h), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados con reservas provisionales en estado `PENDIENTE_CONFIRMACION` confirmar obligatoriamente su asistencia definitiva dentro de la ventana de ratificación institucional comprendida entre las 48 horas y las 24 horas previas al inicio de la sesión (`sesion.fecha_inicio - 48h <= now_utc <= sesion.fecha_inicio - 24h`). El usuario accede a la vista `StudentBookingsView.tsx` y acciona el botón de confirmación enlazado a `bookingService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/bookings.py` y `app/services/booking_service.py` procesan la petición `POST /api/v1/bookings/{id}/confirm`, verifican la vigencia temporal de la ventana, conmutan el estado de la entidad `ReservaCupo` a `CONFIRMADA`, generan el identificador criptográfico del pase de lista y emiten una respuesta HTTP 200 OK, contribuyendo al cálculo del quórum mínimo (RN-05). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia y Quórum EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.confirmBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/confirm`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.confirm_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con sesión institucional activa y rol `mentoreado` verificado en JWT.<br>2. Reserva en la tabla `reservas_cupo` asociada al estudiante en estado `PENDIENTE_CONFIRMACION`.<br>3. Fecha y hora actual dentro de la ventana temporal de confirmación [T-48h, T-24h]. |
| **PostCondiciones** | 1. Estado de la entidad `ReservaCupo` actualizado atómicamente a `CONFIRMADA` en PostgreSQL.<br>2. Generación del código seguro de verificación de asistencia.<br>3. Actualización reactiva de la tarjeta en la interfaz del estudiante con distintivo verde de confirmación. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de reservas y visualización de ventana de ratificación** | |
| **1.** El estudiante mentoreado accede a `"Mis Reservas"` en `StudentBookingsView.tsx`. | **2.** En `bookingService.ts`, se despacha `GET /api/v1/bookings/my-bookings`. El backend retorna las reservas del estudiante. En `StudentBookingsView.tsx`, para las reservas cuya sesión se encuentra dentro de la ventana de ratificación [T-48h, T-24h], se renderiza un panel de alerta en color ámbar con un temporizador y el botón `"Ratificar Asistencia Obligatoria"`. |
| **Fase 2: Validación de plazos y solicitud de ratificación** | |
| **3.** El estudiante revisa los datos de la sesión y pulsa el botón `"Ratificar Asistencia Obligatoria"`. | **4.** En `StudentBookingsView.tsx`, se abre un cuadro modal de ratificación. El estudiante presiona `"Sí, Confirmo mi Asistencia Definitiva"`. En `bookingService.ts`, se despacha la petición `POST /api/v1/bookings/{booking_id}/confirm`. En `bookings.py`, `booking_service.py` ejecuta `SELECT r.*, s.fecha_inicio FROM reservas_cupo r JOIN sesiones_mentoria s ON r.id_sesion = s.id WHERE r.id = :bid AND r.estudiante_email = :email`. Verifica que `now_utc >= s.fecha_inicio - timedelta(hours=48)` y que `now_utc <= s.fecha_inicio - timedelta(hours=24)`. (Si el estudiante intenta ratificar antes de T-48h, salta a E001). (Si la ventana ya expiró por superar el umbral T-24h, salta a E002). |
| **Fase 3: Transición atómica de estado y emisión de pase de asistencia** | |
| **5.** El estudiante espera la respuesta visual de confirmación. | **6.** En `booking_service.py`, se ejecuta `UPDATE reservas_cupo SET estado = 'CONFIRMADA', fecha_confirmacion = :now WHERE id = :bid`. Confirma la transacción con `db.commit()` y retorna HTTP 200 con el modelo `BookingResponse`. En cliente, `StudentBookingsView.tsx` conmuta el estado de la tarjeta a color verde con la leyenda *"Asistencia Ratificada"*, despliega el código alfanumérico para el pase de lista presencial/virtual y emite una notificación de éxito. |

##### Flujos de Excepción

##### Flujo de excepción E001: Intento de ratificación anticipada fuera de ventana
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc < sesion.fecha_inicio - timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_NOT_OPEN: La ventana de confirmación abre exactamente 48 horas antes del inicio de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un mensaje en color azul institucional indicando la fecha y hora exacta en que se habilitará la ratificación obligatoria. |
| **E001-1.2** Hace clic en el botón "Entendido" en la alerta. | **E001-1.3** Cierra el modal de confirmación y retorna al paso 2 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Ventana de ratificación vencida a T-24h
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, `booking_service.py` evalúa `now_utc > sesion.fecha_inicio - timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="CONFIRMATION_WINDOW_EXPIRED: La ventana de ratificación cerró 24 horas antes del inicio. La reserva no confirmada fue liberada para dar paso al proceso de quórum.")`.<br><br>En `StudentBookingsView.tsx`, se actualiza la tarjeta a estado inactivo con una insignia en color gris indicando que el cupo fue dado de baja por falta de ratificación en plazo. |
| **E002-1.2** Hace clic en el botón "Aceptar". | **E002-1.3** Actualiza la lista de reservas en cliente y retorna al paso 2 del Flujo Normal de Eventos. |

#### CUS-017 - Desistir voluntariamente de reserva

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-017** (CUS-017) |
| **Nombre** | Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-014 (Desistimiento voluntario y liberación anticipada de cupos); RN-04 (Antelación mínima de 24 horas para cancelaciones sin sanción institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite a los estudiantes mentoreados anular voluntariamente una reserva activa en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA` sin incurrir en penalizaciones académicas, siempre que la solicitud se despache con una antelación mayor a 24 horas respecto al inicio de la sesión (`fecha_inicio > now_utc + 24h`, RN-04). El componente `StudentBookingsView.tsx` despacha `POST /api/v1/bookings/{id}/cancel` hacia `bookings.py` y `app/services/booking_service.py`. El backend adquiere el cerrojo pesimista de fila, actualiza el estado de la reserva a `CANCELADA_ESTUDIANTE`, decrementa el contador de cupos ocupados de la sesión y confirma la transacción ACID con `db.commit()`, notificando al motor de recomendaciones sobre la vacante liberada. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Asistencia EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/StudentBookingsView.tsx`<br>`aplicacion/frontend/src/services/bookingService.ts` (`BookingService.cancelBooking`)<br>`aplicacion/backend/app/api/v1/endpoints/bookings.py` (`POST /api/v1/bookings/{id}/cancel`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.cancel_booking`)<br>`aplicacion/backend/app/models/booking.py` (`ReservaCupo`, `EstadoReserva`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario autenticado con token JWT institucional y titularidad sobre la reserva.<br>2. Reserva en estado `PENDIENTE_CONFIRMACION` o `CONFIRMADA`.<br>3. Fecha de inicio de la sesión mayor a la hora actual UTC más 24 horas (`fecha_inicio > now + 24h`). |
| **PostCondiciones** | 1. Estado de `ReservaCupo` actualizado a `CANCELADA_ESTUDIANTE` en PostgreSQL.<br>2. Cupo vacante liberado y disponible nuevamente en la cartelera institucional.<br>3. Despliegue de confirmación en cliente y actualización reactiva de la tarjeta a color neutro. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Solicitud de desistimiento y verificación de plazos** | |
| **1.** El estudiante mentoreado localiza su reserva en `StudentBookingsView.tsx` y hace clic en el botón `"Cancelar Reserva"`. | **2.** En `StudentBookingsView.tsx`, se abre un modal de advertencia indicando que el desistimiento es irrevocable y liberará el cupo para otro compañero. El sistema solicita seleccionar un motivo de cancelación opcional en una lista desplegable. (Si la antelación es inferior a 24 horas respecto al inicio de la sesión, salta a E001). |
| **Fase 2: Confirmación y procesamiento atómico de liberación de cupo** | |
| **3.** El estudiante selecciona el motivo y pulsa el botón `"Confirmar Cancelación"`. | **4.** En `bookingService.ts`, se despacha `POST /api/v1/bookings/{booking_id}/cancel`. En `bookings.py`, `booking_service.py` inicia la transacción con `db.begin()`. Ejecuta bloqueo de fila en `sesiones_mentoria` y `reservas_cupo`. Verifica que `sesion.fecha_inicio > now_utc + timedelta(hours=24)` (RN-04). Actualiza `reservas_cupo.estado = 'CANCELADA_ESTUDIANTE'` y registra `fecha_cancelacion = now_utc`. Ejecuta `db.commit()` y retorna HTTP 200 con `BookingResponse`. |
| **5.** El estudiante visualiza el modal de éxito indicando la liberación correcta del cupo sin penalidad. | **6.** En `StudentBookingsView.tsx`, se cierra el modal, se conmuta el estado de la tarjeta a color gris con la leyenda *"Cancelada por el estudiante"* y se emite un evento de actualización que incrementa las vacantes disponibles en la cartelera. |

##### Flujos de Excepción

##### Flujo de excepción E001: Desistimiento tardío con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `booking_service.py` comprueba que `sesion.fecha_inicio <= now_utc + timedelta(hours=24)`. Lanza `HTTPException(status_code=400, detail="LATE_CANCELLATION_PROHIBITED: No se permite la cancelación voluntaria con menos de 24 horas de antelación para no desestabilizar el quórum de la sesión.")`.<br><br>En `StudentBookingsView.tsx`, se despliega un panel de advertencia en color rojo indicando que la política institucional prohíbe cancelaciones a menos de 24 horas y que la inasistencia injustificada acarreará una penalización temporal en futuras reservas. |
| **E001-1.2** Hace clic en el botón "Entendido". | **E001-1.3** Cierra el cuadro modal manteniendo la reserva en estado activo y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-023 - Evaluar quórum automático a T-24h

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-023** (CUS-023) |
| **Nombre** | Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y evaluación de quórum); RN-05 (Regla de quórum mínimo de 3 estudiantes confirmados), RN-10 (Automatización de eventos temporales a T-24h) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Demonio en Segundo Plano (`SchedulerWorker`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite evaluar de forma automatizada y desatendida el cumplimiento del umbral reglamentario de quórum institucional (mínimo 3 estudiantes con asistencia ratificada, RN-05) exactamente 24 horas antes del inicio programado de cada sesión de mentoría. Un proceso en segundo plano programado mediante APScheduler o endpoint administrativo `POST /api/v1/quorum/evaluate-all` en `aplicacion/backend/app/api/v1/endpoints/quorum.py` invoca al método `evaluate_session_quorum` en `app/services/booking_service.py`. El servicio consulta las sesiones en estado `PUBLICADA` con ventana de antelación alcanzada, cuantifica las reservas en estado `CONFIRMADA`; si se alcanza o supera el quórum, promueve automáticamente la sesión a estado `CONFIRMADA`. Si no se alcanza el quórum reglamentario (menos de 3 confirmados), transiciona la sesión a estado `QUORUM_INSUFICIENTE` y despacha alertas urgentes al mentor para la resolución de contingencia (CUS-007). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Quórum y Viabilidad de Sesiones EPIS-UPT |
| **Anexos** | `aplicacion/backend/app/api/v1/endpoints/quorum.py` (`POST /api/v1/quorum/evaluate-all`, `GET /api/v1/quorum/status/{session_id}`)<br>`aplicacion/backend/app/services/booking_service.py` (`BookingService.evaluate_session_quorum`)<br>`aplicacion/backend/app/services/simulation_service.py`<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`), `app/models/booking.py` (`ReservaCupo`, `EstadoReserva`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `PUBLICADA` en la tabla física `sesiones_mentoria`.<br>2. Fecha y hora actual del servidor en la marca temporal exacta de 24 horas previas al inicio de la sesión (`now_utc >= fecha_inicio - 24h`).<br>3. Proceso planificador o disparador de simulación operativo. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos a `CONFIRMADA` o `QUORUM_INSUFICIENTE`.<br>2. Transacción confirmada en PostgreSQL y generación de registros de auditoría de evaluación.<br>3. Disparo de notificaciones hacia el mentor y los estudiantes inscritos. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Disparo de la tarea programada y localización de sesiones a T-24h** | |
| **1.** El proceso planificador del sistema en segundo plano (`SchedulerWorker`) ejecuta el ciclo de evaluación o el administrador despacha la petición `POST /api/v1/quorum/evaluate-all`. | **2.** En `quorum.py`, el controlador invoca `simulation_service.evaluate_all_active_quorums(db)`. El backend ejecuta `SELECT * FROM sesiones_mentoria WHERE estado = 'PUBLICADA' AND fecha_inicio <= NOW() + INTERVAL '24 HOURS'`. (Si no existen sesiones en la ventana T-24h, el sistema finaliza la ejecución sin mutaciones). |
| **Fase 2: Cuantificación de confirmaciones y verificación de umbral de quórum** | |
| **3.** El sistema procesa cada sesión localizada en un bucle transaccional independiente. | **4.** En `booking_service.py`, para cada sesión se ejecuta `SELECT count(*) FROM reservas_cupo WHERE id_sesion = :sid AND estado = 'CONFIRMADA'`. El servicio evalúa si `confirmed_count >= 3` (RN-05). (Si el recuento es menor a 3 confirmados, salta a A001). |
| **Fase 3: Confirmación oficial de sesión y notificación de viabilidad** | |
| **5.** El sistema constata que la sesión cumple el quórum reglamentario (3 o más estudiantes con asistencia ratificada). | **6.** En `booking_service.py`, se ejecuta `UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :sid`. Se confirma la transacción con `db.commit()`. Se genera la traza en la bitácora de auditoría y se despacha una notificación por correo electrónico y notificación web al mentor y a los estudiantes inscritos con el texto: *"¡Sesión confirmada! Tu sesión de mentoría cuenta con el quórum reglamentario para su realización"*. Retorna HTTP 200 con el resumen de la evaluación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Quórum insuficiente a T-24h con alerta al mentor
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, `booking_service.py` detecta que la sesión tiene menos de 3 estudiantes confirmados (`confirmed_count < 3`). | **A001-1.2** El servicio ejecuta `UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :sid` y confirma con `db.commit()`. |
| **A001-1.3** El mentor titular de la sesión recibe una alerta urgente en su panel de control y correo institucional: *"Alerta de Quórum: Tu sesión programada para mañana no alcanzó el quórum mínimo de 3 estudiantes. Por favor, ingresa para decidir si dictarla, reprogramarla o cancelarla"*. | **A001-1.4** El sistema habilita el componente de resolución de contingencia en la interfaz del mentor y concluye el caso de uso y transfiere el flujo a la toma de decisión del mentor (CUS-007). |

#### CUS-007 - Decisión del mentor ante quórum insuficiente

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-007** (CUS-007) |
| **Nombre** | Gestionar sesión de mentoría y decisión resolutiva ante quórum insuficiente |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-016 (Gestión resolutiva de sesiones ante quórum insuficiente); RN-04 (Antelación mínima de reprogramación), RN-10 (Resolución de contingencia ante quórum) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 04 - Sprint 05 |
| **Descripción** | Permite al estudiante mentor tomar una decisión resolutiva cuando su sesión no alcanza el quórum reglamentario de 3 estudiantes a T-24h (estado `QUORUM_INSUFICIENTE`) a través del componente cliente `MentorSessionsView.tsx` y el servicio `offerService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/offers.py` y `app/services/offer_service.py` procesan la petición `POST /api/v1/offers/{id}/quorum-decision`. El mentor cuenta con tres alternativas reglamentarias: 1) Dictar la sesión de todas formas con los estudiantes confirmados (promoción forzada a `CONFIRMADA`), 2) Reprogramar la sesión para una nueva fecha con antelación mínima de 24 horas, o 3) Cancelar la sesión definitivamente liberando a los inscritos sin penalización alguna. La operación se ejecuta bajo una transacción ACID confirmada con `db.commit()`. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-05: Quórum, Confirmación y Cancelaciones)<br>Reglamento Académico de Contingencia de Mentorías EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/MentorSessionsView.tsx`<br>`aplicacion/frontend/src/services/offerService.ts` (`OfferService.resolveQuorum`)<br>`aplicacion/backend/app/api/v1/endpoints/offers.py` (`POST /api/v1/offers/{id}/quorum-decision`)<br>`aplicacion/backend/app/services/offer_service.py` (`OfferService.resolve_quorum_decision`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`, `EstadoSesion`), `app/models/booking.py` (`ReservaCupo`) |
| **Precondiciones** | 1. Mentor titular autenticado con token JWT institucional activo.<br>2. Sesión en la tabla `sesiones_mentoria` en estado estricto `QUORUM_INSUFICIENTE`.<br>3. Decisión despachada antes del inicio programado de la sesión. |
| **PostCondiciones** | 1. Estado de `SesionMentoria` actualizado en base de datos según la decisión elegida (`CONFIRMADA`, `REPROGRAMADA` o `CANCELADA_QUORUM`).<br>2. Actualización en cascada de los estados de reserva de los estudiantes inscritos.<br>3. Despacho automatizado de notificaciones informativas a los estudiantes afectados. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso a la sesión con quórum insuficiente y visualización de opciones** | |
| **1.** El mentor accede a `"Mis Sesiones"` en `MentorSessionsView.tsx` y visualiza la tarjeta de la sesión resaltada en color ámbar con la etiqueta *"Quórum Insuficiente"*. | **2.** El mentor hace clic en el botón `"Gestionar Sesión"`. En `MentorSessionsView.tsx`, se abre una ventana modal desplegando los estudiantes inscritos confirmados y las tres opciones resolutivas: 1) `"Dictar de Todas Formas"`, 2) `"Reprogramar Sesión"`, 3) `"Cancelar Sesión Definitivamente"`. |
| **Fase 2: Elección de la resolución y verificación de parámetros** | |
| **3.** El mentor selecciona la opción `"Dictar de Todas Formas"` (o `"Reprogramar Sesión"` indicando nueva fecha y hora, o `"Cancelar Sesión"` ingresando un justificativo) y presiona el botón `"Confirmar Decisión"`. | **4.** En `offerService.ts`, se despacha la petición `POST /api/v1/offers/{offer_id}/quorum-decision` con payload JSON `{"decision": "PROCEED" | "RESCHEDULE" | "CANCEL", "new_start_time": ..., "reason": ...}`. En `offers.py`, `offer_service.py` inicia la transacción con `db.begin()`. Valida que la sesión se encuentre en estado `QUORUM_INSUFICIENTE`. Si seleccionó reprogramar, valida que la nueva fecha cumpla con la antelación mayor a 24 horas (RN-04). Si seleccionó cancelar, valida que el justificativo no esté vacío. (Si la fecha de reprogramación es inferior a 24 horas, salta a E001). (Si la justificación de cancelación está vacía, salta a E002). |
| **Fase 3: Persistencia de la resolución y notificación a los estudiantes** | |
| **5.** El mentor observa el indicador de procesamiento seguro en el botón de confirmación. | **6.** En `offer_service.py`, si la decisión es `PROCEED`, actualiza `sesiones_mentoria.estado = 'CONFIRMADA'`. Si es `RESCHEDULE`, actualiza fecha y hora, restablece `estado = 'PUBLICADA'` y notifica a los inscritos. Si es `CANCEL`, actualiza `estado = 'CANCELADA_QUORUM'` y libera a los inscritos. Confirma la transacción con `db.commit()` y retorna HTTP 200. En cliente, `MentorSessionsView.tsx` cierra el modal, actualiza el estado de la tarjeta y despliega una notificación flotante en color verde: *"Decisión registrada exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Fecha de reprogramación con menos de 24 horas de antelación
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el mentor selecciona reprogramar pero ingresa una fecha y hora con antelación menor a 24 horas respecto al tiempo actual. `offer_service.py` valida la regla RN-04 y lanza `HTTPException(status_code=400, detail="INSUFFICIENT_RESCHEDULE_ADVANCE: La nueva fecha de la sesión debe programarse con al menos 24 horas de antelación.")`.<br><br>En `MentorSessionsView.tsx`, se resalta el selector de fecha en color rojo con el mensaje de infracción reglamentaria. |
| **E001-1.2** Selecciona una nueva fecha y hora con un margen superior a 24 horas. | **E001-1.3** Rehabilita el botón de confirmación en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Justificación de cancelación definitiva vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el mentor selecciona cancelar la sesión pero deja en blanco el campo de motivo. `offer_service.py` comprueba que la cadena es nula o vacía y lanza `HTTPException(status_code=422, detail="REASON_REQUIRED: Debe ingresar obligatoriamente un motivo justificado para proceder con la cancelación definitiva.")`.<br><br>En `MentorSessionsView.tsx`, se destaca el área de texto en color rojo solicitando ingresar el motivo para los estudiantes. |
| **E002-1.2** Ingresa una justificación válida en el cuadro de texto. | **E002-1.3** Valida la longitud mínima en cliente y retorna al paso 3 del Flujo Normal de Eventos. |


---

### MOD-06: Asistencia, Bitácoras y Feedback

#### CUS-012 - Registrar asistencia a sesión de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-012** (CUS-012) |
| **Nombre** | Registrar asistencia interactiva a sesión de mentoría mediante código QR dinámico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-05 (Aforo y presencia efectiva), RN-12 (Trazabilidad de asistencia y ventana temporal de check-in) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Estudiante Mentoreado (`UserRole.mentoreado`) |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 - Sprint 06 |
| **Descripción** | Permite registrar la presencia efectiva de los estudiantes durante la ejecución de una sesión de mentoría a través del componente cliente `SessionAttendanceView.tsx` y el servicio `attendanceService.ts`. El mentor proyecta o comparte un código QR dinámico cifrado basado en TOTP que rota cada 30 segundos. El estudiante mentoreado escanea el código o digita el pase numérico de 6 dígitos despachando `POST /api/v1/sessions/{id}/attendance/check-in` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/attendance.py`. El servicio `AttendanceService` valida que la solicitud se produzca dentro de la ventana de la sesión (desde 15 minutos antes del inicio hasta 30 minutos tras el fin), comprueba que el estudiante posea una reserva en estado `CONFIRMADA` y persiste el registro en la tabla `asistencias_sesion` (`app/models/attendance.py`) con timestamp UTC y geolocalización o IP institucional, transmitiendo el evento en tiempo real vía WebSockets al panel del mentor. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Control de Asistencia y Acreditación EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SessionAttendanceView.tsx`<br>`aplicacion/frontend/src/services/attendanceService.ts` (`AttendanceService`, `ApiAttendanceAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/attendance.py` (`POST /api/v1/sessions/{id}/attendance/check-in`, `GET /api/v1/sessions/{id}/attendance`)<br>`aplicacion/backend/app/services/attendance_service.py` (`AttendanceService.record_checkin`, `AttendanceService.get_roster`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/booking.py` (`ReservaCupo`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Sesión de mentoría en estado `CONFIRMADA` o `EN_CURSO` en la base de datos.<br>2. Estudiante mentoreado con reserva en estado `CONFIRMADA` en la tabla `reservas_cupo`.<br>3. Petición ejecutada dentro de la ventana temporal de validez de la sesión [inicio - 15m, fin + 30m]. |
| **PostCondiciones** | 1. Registro insertado o actualizado en la tabla física `asistencias_sesion` con `asistio = true`.<br>2. Transmisión del evento de presencia en tiempo real al panel del mentor.<br>3. Despliegue del comprobante de asistencia en la interfaz del mentoreado y habilitación de encuesta de calidad post-mentoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de sesión y generación de token dinámico de asistencia** | |
| **1.** El mentor accede a la sesión activa en `SessionAttendanceView.tsx` y pulsa el botón `"Iniciar Pase de Asistencia Digital"`. | **2.** En `attendanceService.ts`, se despacha `GET /api/v1/sessions/{id}/attendance/token`. El backend genera un token criptográfico TOTP con ventana de rotación de 30 segundos y lo serializa en un código QR interactivo proyectado en la pantalla del mentor junto con la nómina de estudiantes con reserva confirmada en estado provisional *"Ausente"*. |
| **Fase 2: Escaneo de código QR y validación de reserva y ventana horaria** | |
| **3.** El mentoreado presente en la sesión escanea el código QR desde su dispositivo móvil o ingresa el código numérico de 6 dígitos en su aplicación y pulsa `"Registrar Mi Asistencia"`. | **4.** En `attendanceService.ts`, se despacha `POST /api/v1/sessions/{id}/attendance/check-in` con payload `{"session_id": id, "qr_token": token}`. En `attendance.py`, `AttendanceService.record_checkin` valida: 1) que el token TOTP no haya expirado, 2) que el estudiante mantenga una reserva en estado `CONFIRMADA`, 3) que la hora actual esté dentro del intervalo de la sesión (`fecha_inicio - 15m <= now_utc <= fecha_fin + 30m`). (Si el token TOTP o código numérico ha expirado, salta a E001). (Si el estudiante no cuenta con reserva confirmada en la sesión, salta a E002). (Si el check-in se intenta fuera del intervalo temporal permitido, salta a E003). |
| **Fase 3: Persistencia de asistencia y actualización reactiva en tiempo real** | |
| **5.** El estudiante y el mentor observan la actualización instantánea en pantalla. | **6.** En `attendance_service.py`, se ejecuta `INSERT INTO asistencias_sesion (sesion_id, estudiante_id, fecha_checkin, asistio, ip_origen) VALUES (...) ON CONFLICT (sesion_id, estudiante_id) DO UPDATE SET asistio = true, fecha_checkin = NOW()`. Se confirma la transacción con `db.commit()`. El servidor emite un evento WebSocket hacia el panel del mentor, actualizando la fila del estudiante a estado *"Presente"* con un distintivo en color verde. En el dispositivo del mentoreado, se muestra una notificación de éxito: *"¡Asistencia registrada exitosamente! Gracias por tu puntualidad."* |

##### Flujos de Excepción

##### Flujo de excepción E001: Código QR o token TOTP expirado
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `AttendanceService` comprueba que el token TOTP superó su ciclo de vida de 30 segundos. Lanza `HTTPException(status_code=400, detail="QR_TOKEN_EXPIRED: El código de asistencia ha expirado. Por favor, escanee el código QR actualizado proyectado por el mentor.")`.<br><br>En el cliente del estudiante, se despliega una advertencia en color ámbar solicitando enfocar el nuevo código dinámico. Presenta el botón `<button onClick={handleRetryScan}>Escanear Nuevo Código</button>`. |
| **E001-1.2** Hace clic en el botón "Escanear Nuevo Código" y enfoca la pantalla del mentor. | **E001-1.3** Captura el nuevo token TOTP y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Estudiante sin reserva previa confirmada
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, la consulta relacional detecta que el estudiante no posee una tupla en `reservas_cupo` con `estado = 'CONFIRMADA'`. Lanza `HTTPException(status_code=403, detail="NO_CONFIRMED_BOOKING: No registra una reserva confirmada para esta sesión de mentoría.")`.<br><br>En la interfaz del estudiante, se muestra una alerta en color rojo indicando que solo los estudiantes debidamente inscritos y ratificados a T-24h pueden registrar su asistencia. |
| **E002-1.2** Hace clic en el botón "Entendido" en la alerta de restricción. | **E002-1.3** Cierra el escáner y finaliza la interacción sin registrar presencia. |

##### Flujo de excepción E003: Check-in fuera del intervalo temporal reglamentario
| Usuario | Sistema |
|---|---|
| | **E003-1.1** En el paso 4 del Flujo Normal, el servicio comprueba que la hora actual del servidor se ubica fuera del intervalo de tolerancia reglamentaria (más de 15 minutos antes del inicio o más de 30 minutos después de concluida la sesión). Lanza `HTTPException(status_code=400, detail="CHECKIN_WINDOW_CLOSED: El pase de asistencia sólo está habilitado durante la realización de la sesión.")`.<br><br>En la interfaz del estudiante, se despliega un mensaje en color rojo indicando que el registro de asistencia se encuentra cerrado. |
| **E003-1.2** Hace clic en el botón "Aceptar". | **E003-1.3** Redirige a la vista principal y finaliza el caso de uso sin generar registros en la base de datos. |

#### CUS-013 - Registrar bitácora académica de sesión

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-013** (CUS-013) |
| **Nombre** | Registrar bitácora pedagógica y reporte formativo de sesión de mentoría |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-017 (Registro de bitácora pedagógica y control de asistencia); RN-12 (Plazo máximo de 48 horas post-sesión para registro de bitácora) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Coordinador Académico |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 - Sprint 06 |
| **Descripción** | Permite al estudiante mentor consignar el reporte pedagógico de la sesión de mentoría recién concluida a través del formulario `BitacoraFormView.tsx` y el servicio `bitacoraService.ts`. El mentor detalla los temas específicos del sílabo abordados, el nivel de asimilación conceptual de los participantes, las dificultades pedagógicas observadas y las observaciones institucionales. La petición se despacha mediante `POST /api/v1/sessions/{id}/bitacora` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/bitacora.py`. El servicio `BitacoraService` valida que la sesión se encuentre en estado `CONCLUIDA`, que el plazo transcurrido desde el fin de la sesión no exceda las 48 horas reglamentarias (RN-12) y que el texto pedagógico supere los 50 caracteres mínimos. Persiste la entidad `BitacoraPedagogica` (`app/models/bitacora.py`) vinculada a la sesión y actualiza el estado a `BITACORA_REGISTRADA` para su posterior visado administrativo. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Mentorías y Certificación de Horas EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/BitacoraFormView.tsx`<br>`aplicacion/frontend/src/services/bitacoraService.ts` (`BitacoraService`, `ApiBitacoraAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/bitacora.py` (`POST /api/v1/sessions/{id}/bitacora`, `GET /api/v1/sessions/{id}/bitacora`)<br>`aplicacion/backend/app/services/bitacora_service.py` (`BitacoraService.create_bitacora`)<br>`aplicacion/backend/app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Mentor titular con sesión institucional autenticada.<br>2. Sesión de mentoría en estado `CONCLUIDA` en la base de datos.<br>3. Plazo posterior a la finalización de la sesión menor o igual a 48 horas (`now_utc <= fecha_fin + 48h`). |
| **PostCondiciones** | 1. Registro insertado en la tabla `bitacoras_pedagogicas` con código de firma digital SHA-256.<br>2. Estado de `SesionMentoria` actualizado a `BITACORA_REGISTRADA` en PostgreSQL.<br>3. Despliegue de confirmación en cliente y habilitación de las horas para acreditación institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Apertura de bitácora y verificación de plazo límite** | |
| **1.** El mentor ingresa a la sesión concluida en `BitacoraFormView.tsx` y presiona el botón `"Completar Bitácora Pedagógica"`. | **2.** En `bitacoraService.ts`, se invoca la verificación de estado de la sesión. El backend comprueba que la sesión finalizó y que `now_utc <= fecha_fin + timedelta(hours=48)` (RN-12). En `BitacoraFormView.tsx`, se renderiza el formulario pedagógico: lista de temas silábicos cubiertos con casillas de verificación, selector de nivel de dificultad (Bajo, Medio, Alto), cuadro de texto para observaciones pedagógicas y declaración jurada de veracidad. (Si han transcurrido más de 48 horas desde el cierre de la sesión, salta a E001). |
| **Fase 2: Ingreso de evidencias pedagógicas y validación de contenido** | |
| **3.** El mentor marca los temas curriculares explicados, selecciona el nivel de asimilación, redacta las incidencias pedagógicas y presiona el botón `"Guardar y Firmar Bitácora"`. | **4.** En `BitacoraFormView.tsx`, se valida que las observaciones pedagógicas posean una extensión mínima de 50 caracteres y no contengan scripts. En `bitacoraService.ts`, se despacha `POST /api/v1/sessions/{id}/bitacora` con el payload `BitacoraCreateRequest`. En `bitacora.py`, `BitacoraService.create_bitacora` valida la firma del mentor y el esquema de datos. (Si la descripción pedagógica no alcanza el mínimo de 50 caracteres, salta a E002). |
| **Fase 3: Persistencia transaccional y certificación de horas** | |
| **5.** El mentor observa la barra de progreso mientras se genera el hash de integridad de la bitácora. | **6.** En `bitacora_service.py`, se calcula el hash criptográfico SHA-256 sobre el contenido pedagógico y se ejecuta `INSERT INTO bitacoras_pedagogicas (sesion_id, mentor_id, temas_cubiertos, observaciones, nivel_dificultad, hash_firma, fecha_registro) VALUES (...)`. Se actualiza `sesiones_mentoria.estado = 'BITACORA_REGISTRADA'`. Se confirma la transacción con `db.commit()` y se retorna HTTP 201 Created. En cliente, `BitacoraFormView.tsx` muestra un panel de confirmación en color verde con el código de firma digital y redirige al historial de sesiones. |

##### Flujos de Excepción

##### Flujo de excepción E001: Plazo límite de 48 horas vencido
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `bitacora_service.py` evalúa `now_utc > sesion.fecha_fin + timedelta(hours=48)`. Lanza `HTTPException(status_code=400, detail="DEADLINE_EXCEEDED: El plazo reglamentario de 48 horas para registrar la bitácora ha vencido.")`.<br><br>En `BitacoraFormView.tsx`, se deshabilita la edición del formulario y se muestra una advertencia en color rojo indicando que la bitácora quedó fuera de plazo reglamentario y requiere solicitud de desbloqueo administrativo ante la Dirección de Escuela. |
| **E001-1.2** Hace clic en el botón "Solicitar Desbloqueo a Coordinación". | **E001-1.3** Abre un formulario de solicitud de prórroga y finaliza la interacción sin registrar la bitácora ordinaria. |

##### Flujo de excepción E002: Descripción pedagógica insuficiente o vacía
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, el validador Pydantic en `bitacora.py` comprueba que el campo de observaciones tiene menos de 50 caracteres. Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: Las observaciones pedagógicas deben contener una descripción sustantiva de al menos 50 caracteres.")`.<br><br>En `BitacoraFormView.tsx`, se resalta el cuadro de texto en color rojo y se muestra un contador de caracteres indicando los faltantes. |
| **E002-1.2** Amplía la descripción pedagógica detallando el desarrollo de la sesión hasta superar los 50 caracteres. | **E002-1.3** Actualiza el contador de caracteres en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-014 - Visualizar historial y bitácoras académicas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-014** (CUS-014) |
| **Nombre** | Visualizar historial académico integral de sesiones y bitácoras pedagógicas |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-019 (Consulta de historial cronológico individual de sesiones y asistencias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 05 - Sprint 06 |
| **Descripción** | Permite a los usuarios consultar su trayectoria histórica dentro del programa de mentorías académicas a través del componente cliente `HistorySessionsView.tsx` y el servicio `historyService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/history.py` y `app/services/history_service.py` procesan las peticiones `GET /api/v1/history/sessions` y `GET /api/v1/history/bitacora/{session_id}`. Para los mentoreados, el sistema presenta la relación cronológica de sesiones a las que asistió con sus comprobantes y temas repasados. Para los mentores, despliega las sesiones impartidas, las bitácoras pedagógicas suscritas con su hash de firma digital y el estado de validación de horas ante la Dirección de Escuela. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-06: Trazabilidad, Bitácoras y Evaluación)<br>Reglamento Académico de Seguimiento Estudiantil EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/HistorySessionsView.tsx`<br>`aplicacion/frontend/src/services/historyService.ts` (`HistoryService`, `ApiHistoryAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/history.py` (`GET /api/v1/history/sessions`, `GET /api/v1/history/bitacora/{session_id}`)<br>`aplicacion/backend/app/services/history_service.py` (`HistoryService.get_user_history`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/attendance.py` (`AsistenciaSesion`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Registros históricos persistidos en las tablas de sesiones, bitácoras o asistencias. |
| **PostCondiciones** | 1. Respuesta JSON paginada con el historial cronológico y metadatos pedagógicos retornada al cliente.<br>2. Operación idempotente de lectura sin alteraciones destructivas en la base de datos.<br>3. Renderizado de la línea de tiempo interactiva con opciones de filtrado por ciclo y asignatura. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del historial y aplicación de filtros cronológicos** | |
| **1.** El usuario hace clic en `"Mi Historial"` en el menú lateral de navegación de `HistorySessionsView.tsx`. | **2.** En `historyService.ts`, se despacha `GET /api/v1/history/sessions` enviando el token institucional. En `history.py`, `HistoryService.get_user_history` recupera las sesiones en que el usuario participó (como mentor o mentoreado) ordenadas de forma cronológica descendente. Retorna HTTP 200 con la nómina histórica. `HistorySessionsView.tsx` renderiza las tarjetas de sesiones en una línea de tiempo interactiva con distintivos por estado (`Concluida`, `Bitácora Registrada`, `Visada`). (Si el usuario es nuevo y no registra historial de sesiones, salta a A001). |
| **Fase 2: Búsqueda y filtrado por materia o período académico** | |
| **3.** El usuario filtra por semestre académico o escribe el nombre de una materia en el cuadro de búsqueda. | **4.** En `HistorySessionsView.tsx`, se actualiza reactivamente la lista de tarjetas en pantalla. El usuario hace clic sobre una sesión concluida para consultar el detalle pedagógico. |
| **Fase 3: Visualización de bitácora pedagógica y comprobante de asistencia** | |
| **5.** El usuario presiona el botón `"Ver Bitácora Pedagógica"` en la tarjeta seleccionada. | **6.** En `historyService.ts`, se despacha `GET /api/v1/history/bitacora/{session_id}`. El backend valida los permisos de lectura y retorna el registro de `BitacoraPedagogica` incluyendo los temas abordados, el nivel de dificultad, las observaciones y la firma digital SHA-256. `HistorySessionsView.tsx` despliega una ventana modal con el desglose formal de la bitácora y el botón de exportación en formato legible. |

##### Flujos Alternativos

##### Flujo alternativo A001: Historial académico vacío para usuario nuevo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 2 del Flujo Normal, la consulta histórica retorna cero registros para el usuario. | **A001-1.2** En `HistorySessionsView.tsx`, se despliega un panel amigable en color azul institucional con el mensaje: *"Aún no registras sesiones de mentoría en tu historial. Comienza explorando la cartelera de recomendaciones para inscribirte en un tema"*. Presenta el botón `<button onClick={handleGoToBillboard}>Explorar Cartelera</button>`. |
| **A001-1.3** El usuario hace clic en el botón "Explorar Cartelera". | **A001-1.4** El sistema redirige al componente `RecommendationFeedView.tsx` y retorna al paso 1 del Flujo Normal de Eventos de CUS-002. |


---

### MOD-07: Gamificación e Incentivos

#### CUS-018 - Emitir constancia institucional de horas de mentoría

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-018** (CUS-018) |
| **Nombre** | Emitir constancia oficial de horas de mentoría con firma criptográfica y QR |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-022 (Parametrización institucional de umbrales y emisión de certificados), RF-023 (Descarga y verificación institucional de certificados); RN-14 (Umbral mínimo de 20 horas acreditadas con bitácoras visadas) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor (`UserRole.mentor`), Administrador Institucional, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a los estudiantes mentores solicitar y descargar una constancia institucional de horas de mentoría acreditadas una vez alcanzado el umbral reglamentario de 20 horas efectivas de dictado (RN-14) con bitácoras pedagógicas debidamente registradas y visadas por la administración. El componente `CertificateView.tsx` despacha la solicitud mediante `POST /api/v1/certificates/generate` hacia el backend en `aplicacion/backend/app/api/v1/endpoints/certificates.py`. El servicio `CertificateService` verifica en base de datos la suma de horas dictadas (`SUM(duracion_minutos)/60 >= 20`), genera un código de serie alfanumérico único, calcula el sello criptográfico SHA-256 del documento, genera un código QR de verificación institucional que apunta al validador público de la universidad, y compila el documento en formato PDF. Persiste la entidad `CertificadoHoras` (`app/models/certificate.py`) y retorna el identificador del archivo para su descarga segura. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Reglamento de Prácticas Pre-Profesionales y Responsabilidad Social EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/CertificateView.tsx`<br>`aplicacion/frontend/src/services/certificateService.ts` (`CertificateService`, `ApiCertificateAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/certificates.py` (`POST /api/v1/certificates/generate`, `GET /api/v1/certificates/{id}/download`, `GET /api/v1/certificates/verify/{code}`)<br>`aplicacion/backend/app/services/certificate_service.py` (`CertificateService.generate_certificate`, `CertificateService.verify_code`)<br>`aplicacion/backend/app/models/certificate.py` (`CertificadoHoras`), `app/models/bitacora.py` (`BitacoraPedagogica`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Estudiante mentor autenticado con token JWT institucional activo.<br>2. Suma acumulada de al menos 20 horas de mentoría con bitácoras pedagógicas aprobadas en el semestre.<br>3. Inexistencia de constancia duplicada activa para el mismo período académico. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `certificados_horas` con código de verificación alfanumérico y hash SHA-256.<br>2. Archivo PDF estructurado generado en almacenamiento seguro con código QR embebido.<br>3. Despliegue del botón de descarga directa y registro del evento en la auditoría institucional. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de acumulado de horas y verificación de umbral** | |
| **1.** El estudiante mentor accede a `"Mis Certificados"` en `CertificateView.tsx`. | **2.** En `certificateService.ts`, se despacha `GET /api/v1/certificates/summary`. En `certificates.py`, `CertificateService` ejecuta `SELECT sum(s.duracion_minutos)/60.0 as horas_totales FROM sesiones_mentoria s JOIN bitacoras_pedagogicas b ON s.id = b.sesion_id WHERE s.id_mentor = :mid AND s.estado = 'BITACORA_REGISTRADA'`. Retorna HTTP 200 con el total de horas acumuladas. En `CertificateView.tsx`, se renderiza una barra de progreso porcentual hacia la meta reglamentaria de 20 horas (RN-14) en color azul institucional. Si las horas son iguales o mayores a 20, se habilita el botón `"Emitir Constancia Oficial"`. (Si el total de horas acumuladas es menor a 20, salta a E001). |
| **Fase 2: Solicitud de emisión y previsualización de datos** | |
| **3.** El mentor presiona el botón `"Emitir Constancia Oficial"`. | **4.** En `CertificateView.tsx`, se abre una ventana modal de previsualización que muestra: nombres completos del mentor, código universitario, semestre académico, total de horas acreditadas y una vista preliminar del código QR de validación. El mentor verifica sus datos y presiona el botón `"Confirmar y Generar PDF Cifrado"`. |
| **Fase 3: Generación criptográfica, persistencia y descarga del PDF** | |
| **5.** El mentor observa la animación de compilación segura del documento. | **6.** En `certificateService.ts`, se despacha `POST /api/v1/certificates/generate` con el período semestral. En `certificates.py`, `CertificateService.generate_certificate` inicia una transacción ACID. Genera un identificador alfanumérico único (e.g. `UPT-EPIS-2026-I-0042`), calcula el hash de integridad SHA-256 de los datos y compila el documento PDF oficial incorporando membrete institucional, firma digital del Director de Escuela y código QR de verificación web. Inserta el registro en `certificados_horas`, ejecuta `db.commit()` y retorna HTTP 201 Created con el payload del certificado. En cliente, `CertificateView.tsx` renderiza la vista previa del documento y habilita el botón de descarga directa en formato PDF. |

##### Flujos de Excepción

##### Flujo de excepción E001: Horas acreditadas insuficientes para el umbral institucional
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, `CertificateService` comprueba que el acumulado de horas con bitácoras registradas es menor a 20 (`horas_totales < 20.0`). Lanza `HTTPException(status_code=400, detail="INSUFFICIENT_HOURS: Requiere al menos 20 horas de mentoría con bitácora registrada para emitir la constancia oficial (Horas actuales: {horas_totales}).")`.<br><br>En `CertificateView.tsx`, se mantiene el botón de emisión deshabilitado y se despliega un panel informativo en color ámbar indicando las horas faltantes para alcanzar la certificación. |
| **E001-1.2** Hace clic en el botón "Ver Sesiones Pendientes". | **E001-1.3** Redirige a la vista de sesiones para completar bitácoras pendientes y retorna al paso 1 del Flujo Normal de Eventos. |

#### CUS-019 - Gestionar insignias y reputación gamificada

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-019** (CUS-019) |
| **Nombre** | Gestionar insignias de logro formativo y reputación gamificada de mentores |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-021 (Cálculo dinámico de reputación y visualización de insignias); RN-13 (Gamificación: puntaje por calificaciones, asistencias y puntualidad) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Estudiante Mentor, Estudiante Mentoreado |
| **Interacción** | Fase de Construcción / Iteración Sprint 06 - Sprint 07 |
| **Descripción** | Permite a la comunidad académica visualizar el progreso, insignias de honor alcanzadas y nivel de reputación formativa de los mentores mediante el componente cliente `GamificationView.tsx` y el servicio `gamificationService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/gamification.py` y `app/services/reputation_service.py` expone las consultas de logros `GET /api/v1/gamification/badges` y el cuadro de honor `GET /api/v1/gamification/leaderboard`. El motor de reputación calcula periódicamente el puntaje global $R = 0.5 	imes ValoracionPromedio + 0.3 	imes HorasAcreditadas + 0.2 	imes TasaPuntualidad$ (RN-13), desbloqueando automáticamente insignias de nivel (tales como "Mentor Destacado", "Puntualidad Impecable" y "Especialista en Algoritmos") en la tabla física `insignias_usuarios` (`app/models/gamification.py`), fomentando la participación y el compromiso entre pares. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-07: Gamificación, Reputación y Certificación)<br>Estrategias de Gamificación en la Educación Superior Universitaria |
| **Anexos** | `aplicacion/frontend/src/components/GamificationView.tsx`<br>`aplicacion/frontend/src/services/gamificationService.ts` (`GamificationService`, `ApiGamificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/gamification.py` (`GET /api/v1/gamification/badges`, `GET /api/v1/gamification/leaderboard`)<br>`aplicacion/backend/app/services/reputation_service.py` (`ReputationService.get_user_badges`, `ReputationService.calculate_rank`)<br>`aplicacion/backend/app/models/gamification.py` (`Insignia`, `InsigniaUsuario`, `ReputacionUsuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado en la plataforma.<br>2. Catálogo de insignias y reglas de desbloqueo configuradas en la base de datos.<br>3. Registro de calificaciones de sesiones o asistencias efectivas en el sistema. |
| **PostCondiciones** | 1. Nómina de insignias obtenidas y bloqueadas con porcentaje de avance retornadas en JSON.<br>2. Tabla de clasificación (leaderboard) calculada en tiempo real de sólo lectura.<br>3. Despliegue interactivo en la interfaz con animación de logros y posición en el cuadro de honor. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de insignias personales y progreso de nivel** | |
| **1.** El usuario hace clic en el enlace `"Insignias y Reputación"` en `GamificationView.tsx`. | **2.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/badges`. En `gamification.py`, `ReputationService` consulta la tabla `insignias_usuarios` unida con `insignias` para el usuario y calcula las métricas de avance hacia las insignias bloqueadas. Retorna HTTP 200 con el listado completo. En `GamificationView.tsx`, se renderiza una vitrina virtual: las insignias desbloqueadas se muestran en color dorado con su fecha de concesión, y las bloqueadas en color gris con una barra de progreso que indica el porcentaje completado. |
| **Fase 2: Exploración de criterios de logro y detalle de insignia** | |
| **3.** El usuario hace clic sobre una insignia específica (e.g. "Mentor Destacado"). | **4.** En `GamificationView.tsx`, se despliega un panel lateral interactivo con el nombre de la insignia, descripción pedagógica, icono gráfico y requisitos de desbloqueo (e.g. *"Haber dictado más de 10 sesiones con calificación promedio mayor o igual a 4.8 estrellas"*). |
| **Fase 3: Visualización del cuadro de honor institucional (Leaderboard)** | |
| **5.** El usuario hace clic en la pestaña `"Cuadro de Honor de la Escuela"`. | **6.** En `gamificationService.ts`, se despacha `GET /api/v1/gamification/leaderboard`. El backend recupera el Top-10 de mentores clasificados por puntaje de reputación global calculados bajo RN-13. Retorna HTTP 200 con los nombres, cursos y puntuación. `GamificationView.tsx` renderiza la tabla clasificatoria destacando a los tres primeros lugares con medallas de honor, e indicando la posición del usuario en el ranking general con un marco en color azul institucional. (Si el usuario ha configurado su perfil en modo privado con alias anónimo, salta a A001). |

##### Flujos Alternativos

##### Flujo alternativo A001: Visualización en el cuadro de honor con alias anónimo
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 6 del Flujo Normal, el usuario tiene activada la opción de privacidad en su perfil institucional. | **A001-1.2** En `gamification.py`, `ReputationService` anonimiza los datos personales del usuario reemplazando sus nombres oficiales por un seudónimo aleatorio o su código universitario parcial (e.g. *"Mentor EPIS-742"*). |
| **A001-1.3** El usuario visualiza su puntaje de reputación en el ranking garantizando la confidencialidad de su identidad ante terceros. | **A001-1.4** El sistema muestra el interruptor de visibilidad para permitir conmutar a nombre público en cualquier momento y retorna al paso 6 del Flujo Normal de Eventos. |


---

### MOD-08: Analítica, Notificaciones y Configuración

#### CUS-009 - Notificar eventos críticos y alertas temporales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-009** (CUS-009) |
| **Nombre** | Notificar eventos críticos y alertas de confirmación a T-24h |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-015 (Monitoreo desatendido, emisión de recordatorios y alertas); RN-04 (Antelación de 24 horas), RN-10 (Control de asistencia y quórum institucional) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Proceso Planificador (`SchedulerWorker`), Estudiante Mentor, Estudiante Mentoreado, Administrador Institucional |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite transmitir notificaciones asíncronas y alertas en tiempo real a los usuarios institucionales ante eventos críticos del ciclo de vida de las sesiones de mentoría (tales como recordatorios de ratificación de asistencia a T-24h, confirmación oficial de quórum, reprogramación o cancelación contingente). El frontend gestiona las alertas reactivas a través del componente `NotificationBell.tsx` y el servicio `notificationService.ts`, conectándose al canal de Server-Sent Events (SSE) `/api/v1/notifications/stream`. El backend `aplicacion/backend/app/api/v1/endpoints/notifications.py` y `app/services/notification_service.py` procesan eventos generados por tareas programadas de Celery/APScheduler, persisten la entidad `NotificacionEvento` (`app/models/notification.py`) en PostgreSQL y despachan simultáneamente correos electrónicos de respaldo vía SMTP universitario (`EmailService`), garantizando la notificación oportuna a mentores y estudiantes. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Estándar W3C Server-Sent Events y Protocolo SMTP RFC 5321 |
| **Anexos** | `aplicacion/frontend/src/components/NotificationBell.tsx`<br>`aplicacion/frontend/src/services/notificationService.ts` (`NotificationService`, `ApiNotificationAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/notifications.py` (`GET /api/v1/notifications/unread`, `POST /api/v1/notifications/{id}/mark-read`, `GET /api/v1/notifications/stream`)<br>`aplicacion/backend/app/services/notification_service.py` (`NotificationService.dispatch_event`, `NotificationService.get_unread`)<br>`aplicacion/backend/app/models/notification.py` (`NotificacionEvento`), `app/models/auth.py` (`Usuario`) |
| **Precondiciones** | 1. Usuario institucional autenticado con token JWT activo en la plataforma.<br>2. Evento de dominio generado en backend (e.g. evaluación de quórum, reserva formalizada, cancelación).<br>3. Servicio SMTP institucional o canal SSE operativo en el servidor. |
| **PostCondiciones** | 1. Registro insertado en la tabla física `notificaciones_eventos` con `leida = false` y marca temporal UTC.<br>2. Transmisión reactiva del mensaje a la campana de notificaciones de la interfaz cliente.<br>3. Despacho de correo electrónico de respaldo al buzón universitario del destinatario. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Conexión al canal de notificaciones e inicialización de alertas** | |
| **1.** El usuario inicia sesión en la plataforma y visualiza el componente de campana en la cabecera `NotificationBell.tsx`. | **2.** En `notificationService.ts`, se establece una conexión persistente SSE con `GET /api/v1/notifications/stream` y se despacha `GET /api/v1/notifications/unread`. En `notifications.py`, `NotificationService` consulta `SELECT * FROM notificaciones_eventos WHERE usuario_id = :uid AND leida = false ORDER BY fecha_creacion DESC`. Retorna HTTP 200 con la nómina de alertas pendientes. En `NotificationBell.tsx`, se renderiza una insignia numérica en color rojo sobre la campana indicando las notificaciones no leídas. |
| **Fase 2: Generación asíncrona de evento crítico y despacho multicanal** | |
| **3.** Un proceso del sistema en segundo plano (e.g. evaluación de quórum a T-24h en CUS-023) detecta la necesidad de alertar al usuario. | **4.** En `notification_service.py`, se invoca `dispatch_event(user_id, event_type, message, reference_id)`. Se ejecuta `INSERT INTO notificaciones_eventos (...) VALUES (...)` y se emite el evento al flujo SSE. Simultáneamente, se invoca a `EmailService.send_alert_email()` para despachar el aviso a su correo `@upt.pe`. (Si el servidor SMTP sufre timeout o indisponibilidad de red, salta a E001). |
| **Fase 3: Recepción reactiva en cliente y lectura de notificación** | |
| **5.** El usuario observa la actualización instantánea del contador en la campana y hace clic sobre el icono `NotificationBell.tsx`. | **6.** En `NotificationBell.tsx`, se abre un panel flotante desplegando las alertas ordenadas cronológicamente con distintivos de criticidad (Informativa, Alerta T-24h, Urgente). El usuario hace clic sobre una alerta específica (e.g. *"Tu sesión de mañana ha sido confirmada"*). En `notificationService.ts`, se despacha `POST /api/v1/notifications/{id}/mark-read`. El backend actualiza `leida = true` en base de datos. El sistema disminuye el contador y redirige al usuario a la vista de la sesión referenciada. |

##### Flujos de Excepción

##### Flujo de excepción E001: Falla de despacho en el servicio SMTP de respaldo
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, la pasarela de correo SMTP universitario no responde o rechaza la conexión. `EmailService` captura la excepción `SMTPException`, registra una advertencia en la bitácora de auditoría del servidor (`logger.warning("SMTP dispatch failed, falling back to SSE only")`) y preserva la entrega mediante el canal web en tiempo real sin abortar la transacción de base de datos.<br><br>En `NotificationBell.tsx`, el usuario recibe la notificación instantánea en pantalla de forma normal, manteniendo la continuidad operativa. |
| **E001-1.2** Hace clic en la campana de notificaciones y lee el mensaje directamente en la aplicación. | **E001-1.3** Marca la notificación como leída y retorna al paso 6 del Flujo Normal de Eventos. |

#### CUS-011 - Generar reportes e indicadores de analítica académica

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-011** (CUS-011) |
| **Nombre** | Generar reportes consolidados e indicadores analíticos de gestión de mentorías |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS, Comité de Calidad ICACIT |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades académicas y evaluadores de acreditación generar informes estadísticos agregados sobre la cobertura, demanda y efectividad del programa de mentorías entre pares mediante el componente cliente `AnalyticsDashboardView.tsx` y el servicio `analyticsService.ts`. El backend en `aplicacion/backend/app/api/v1/endpoints/analytics.py` y `app/services/analytics_service.py` procesa las peticiones `GET /api/v1/analytics/reports/kpis` y `GET /api/v1/analytics/export`. El servicio ejecuta consultas analíticas relacionales en PostgreSQL agrupando métricas por asignatura filtro, ciclo y modalidad (horas dictadas, porcentaje de asistencia efectiva, quórum promedio alcanzado y tasa de demanda no atendida). Permite descargar el consolidado en formato de hoja de cálculo estructurada (`.xlsx` o `.csv`) con metadatos de auditoría institucional. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Criterio 4 ICACIT: Evaluación y Mejora Continua |
| **Anexos** | `aplicacion/frontend/src/components/AnalyticsDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService`, `ApiAnalyticsAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/reports/kpis`, `GET /api/v1/analytics/export`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.calculate_kpis`, `AnalyticsService.export_report`)<br>`aplicacion/backend/app/models/offer.py` (`SesionMentoria`), `app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`) |
| **Precondiciones** | 1. Usuario autenticado con rol `UserRole.administrador` o directivo verificado en JWT.<br>2. Datos de sesiones, asistencias y demandas registradas en el semestre académico consultado.<br>3. Parámetros de rango de fechas válidos dentro del calendario lectivo. |
| **PostCondiciones** | 1. Conjunto estructurado de KPIs retornado en JSON y renderizado en gráficos analíticos.<br>2. Flujo binario de hoja de cálculo generado y descargado en el navegador del usuario.<br>3. Registro de auditoría administrativa persistido en el sistema. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al panel analítico y configuración de parámetros** | |
| **1.** El administrador accede al panel de reportes en `AnalyticsDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/reports/kpis?semester=2026-I`. En `analytics.py`, `AnalyticsService.calculate_kpis` ejecuta consultas agregadas: total de sesiones ejecutadas, horas pedagógicas acumuladas, tasa global de asistencia efectiva y distribución porcentual por modalidad (Presencial vs Virtual). Retorna HTTP 200 con el resumen estadístico. En `AnalyticsDashboardView.tsx`, se renderizan tarjetas de indicadores clave y gráficos de barras comparativos en color azul institucional. |
| **Fase 2: Ajuste de filtros temporales y selección de formato de exportación** | |
| **3.** El usuario ajusta el rango de fechas en los selectores de inicio y fin, elige una asignatura filtro específica y selecciona el formato de salida (`Excel .xlsx` o `CSV`). | **4.** En `AnalyticsDashboardView.tsx`, se validan las fechas seleccionadas verificando que la fecha de inicio no sea posterior a la fecha de fin ni exceda la fecha actual. El usuario presiona el botón `"Exportar Informe Consolidado"`. (Si el rango de fechas es inconsistente o futuro, salta a E001). |
| **Fase 3: Generación del documento analítico y descarga segura** | |
| **5.** El usuario observa el indicador circular de compilación del reporte en el botón de exportación. | **6.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/export?format=xlsx&start_date=...&end_date=...`. En `analytics.py`, `AnalyticsService.export_report` compila el libro de cálculo estructurado con pestañas de: 1) Resumen Ejecutivo de KPIs, 2) Detalle de Sesiones Impartidas, 3) Registro Consolidado de Asistencias, y 4) Análisis de Materias Críticas. Retorna la respuesta binaria con cabecera `Content-Disposition: attachment; filename="Reporte_Mentorias_EPIS.xlsx"`. El navegador del usuario inicia la descarga automática del archivo y el sistema registra la traza de auditoría. |

##### Flujos de Excepción

##### Flujo de excepción E001: Rango de fechas inconsistente o futuro
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, el validador en cliente o `analytics.py` comprueba que la fecha inicial es mayor a la final o que se ingresaron fechas futuras no transcurridas. Lanza `HTTPException(status_code=400, detail="INVALID_DATE_RANGE: El rango de fechas seleccionado es inconsistente o corresponde a períodos futuros.")`.<br><br>En `AnalyticsDashboardView.tsx`, se resaltan los campos de fecha en color rojo y se muestra una notificación de advertencia en color ámbar. |
| **E001-1.2** Modifica las fechas seleccionando un período semestral válido. | **E001-1.3** Actualiza los valores en la interfaz y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-015 - Consultar métricas de retención y desempeño

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-015** (CUS-015) |
| **Nombre** | Consultar métricas de correlación de retención estudiantil y desempeño académico |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-025 (Tablero analítico y métricas de rendimiento académico); Criterios ICACIT de retención y graduación oportuna |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional, Comisión de Acreditación ICACIT, Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los comités de calidad educativa evaluar el impacto del programa de mentorías en la retención estudiantil y en la reducción del índice de reprobación en materias filtro a través del componente cliente `RetentionDashboardView.tsx` y el servicio `analyticsService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/analytics.py` procesa las peticiones `GET /api/v1/analytics/retention/cohorts` y `GET /api/v1/analytics/retention/impact`. El servicio analiza estadísticamente las cohortes estudiantiles, calculando la correlación entre la participación recurrente en mentorías (asistencia >= 3 sesiones) y la tasa de aprobación de las asignaturas críticas (Cálculo, Física, Algoritmos, Estructuras de Datos). Presenta comparativas entre grupos de control (estudiantes no asistentes) y grupos participantes para respaldar las auditorías ICACIT. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Modelo de Calidad y Acreditación de Programas de Ingeniería ICACIT |
| **Anexos** | `aplicacion/frontend/src/components/RetentionDashboardView.tsx`<br>`aplicacion/frontend/src/services/analyticsService.ts` (`AnalyticsService.getRetentionMetrics`)<br>`aplicacion/backend/app/api/v1/endpoints/analytics.py` (`GET /api/v1/analytics/retention/cohorts`, `GET /api/v1/analytics/retention/impact`)<br>`aplicacion/backend/app/services/analytics_service.py` (`AnalyticsService.analyze_retention_correlation`)<br>`aplicacion/backend/app/models/attendance.py` (`AsistenciaSesion`), `app/models/curriculum.py` (`Curso`), `app/models/profile.py` (`PerfilAcademico`) |
| **Precondiciones** | 1. Usuario con credenciales administrativas o de evaluador de calidad.<br>2. Registros de calificaciones o actas académicas consolidadas de asignaturas filtro en el semestre.<br>3. Mínimo de registros estadísticos requeridos para inferencia de correlación. |
| **PostCondiciones** | 1. Métricas de retención, tasa de deserción relativa e impacto en aprobación retornadas en JSON.<br>2. Consulta de lectura analítica sin modificación de registros académicos oficiales.<br>3. Visualización de gráficos de dispersión y comparativas de cohortes en la interfaz. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Acceso al módulo de impacto y selección de cohorte** | |
| **1.** El evaluador de calidad accede a `"Impacto y Retención Académica"` en `RetentionDashboardView.tsx`. | **2.** En `analyticsService.ts`, se despacha `GET /api/v1/analytics/retention/impact`. En `analytics.py`, `AnalyticsService.analyze_retention_correlation` ejecuta la consulta de comparación: calcula el porcentaje de aprobación de estudiantes que recibieron mentoría versus el grupo de estudiantes que no participó en el programa. Retorna HTTP 200. En `RetentionDashboardView.tsx`, se renderiza un gráfico comparativo de barras dobles y un panel con la estimación de reducción del riesgo de reprobación en color azul institucional. |
| **Fase 2: Segmentación por asignatura filtro y período lectivo** | |
| **3.** El usuario selecciona una asignatura filtro específica (e.g. Estructuras de Datos) en la lista desplegable de materias y presiona `"Calcular Índice de Impacto"`. | **4.** En `RetentionDashboardView.tsx`, se envía la consulta parametrizada. En `analytics.py`, se evalúa el tamaño muestral de la asignatura. Si el número de estudiantes evaluados es suficiente (al menos 10 registros), se calcula el coeficiente de correlación y la significancia estadística. (Si la muestra disponible es menor a 10 registros estadísticos, salta a A001). |
| **Fase 3: Visualización de indicadores ICACIT y exportación** | |
| **5.** El usuario revisa los indicadores de logro académico y presiona el botón `"Exportar Evidencia ICACIT"`. | **6.** El sistema genera un resumen analítico con la tasa de retención estudiantil, la tabla de frecuencias de asistencia y las firmas de integridad del informe, descargando el archivo en formato PDF oficial para su incorporación en el expediente de acreditación. |

##### Flujos Alternativos

##### Flujo alternativo A001: Muestra insuficiente para análisis estadístico
| Usuario | Sistema |
|---|---|
| **A001-1.1** En el paso 4 del Flujo Normal, el servicio detecta que la asignatura seleccionada cuenta con menos de 10 estudiantes participantes en el semestre analizado. | **A001-1.2** En `RetentionDashboardView.tsx`, se despliega un panel en color ámbar: *"Muestra preliminar insuficiente para inferencia estadística significativa (< 10 registros). Se presentan únicamente métricas descriptivas básicas"*. |
| **A001-1.3** El evaluador visualiza las frecuencias absolutas sin la estimación de correlación inferencial. | **A001-1.4** El sistema ofrece la opción de ampliar el rango temporal a semestres anteriores y retorna al paso 3 del Flujo Normal de Eventos. |

#### CUS-016 - Auditar trazas de seguridad y consentimiento Ley 29733

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-016** (CUS-016) |
| **Nombre** | Auditar trazas inmutables de seguridad y consentimientos legales digitales |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-026 (Auditoría administrativa de bitácoras, accesos y seguridad); RN-02 (Registro inmutable de consentimiento legal digital Ley Nº 29733) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Oficial de Seguridad de la Información (`UserRole.administrador`), Delegado de Protección de Datos |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a los oficiales de seguridad y autoridades universitarias inspeccionar las trazas de auditoría inmutables del sistema y verificar el estricto cumplimiento de la Ley Nº 29733 (Protección de Datos Personales del Perú) mediante el componente `AuditLogView.tsx` y el servicio `auditService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/audit.py` y `app/services/audit_service.py` exponen los endpoints `GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces` y `POST /api/v1/audit/verify-chain`. El sistema verifica la integridad criptográfica de la cadena de bloques o hashes encadenados de auditoría (donde cada registro contiene el SHA-256 del registro anterior), garantizando la no alteración de eventos críticos (inicios de sesión 2FA, modificaciones de roles, aceptaciones y revocaciones de consentimiento legal con direcciones IP y marcas temporales UTC). |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Ley Nº 29733 de Protección de Datos Personales y Estándar ISO/IEC 27001 |
| **Anexos** | `aplicacion/frontend/src/components/AuditLogView.tsx`<br>`aplicacion/frontend/src/services/auditService.ts` (`AuditService`, `ApiAuditAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/audit.py` (`GET /api/v1/audit/logs`, `GET /api/v1/audit/consent-traces`, `POST /api/v1/audit/verify-chain`)<br>`aplicacion/backend/app/services/audit_service.py` (`AuditService.get_logs`, `AuditService.verify_chain_integrity`)<br>`aplicacion/backend/app/models/consent.py` (`ConsentimientoLegal`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Usuario autenticado portando token JWT institucional con privilegios de Oficial de Seguridad o Administrador.<br>2. Registros de auditoría y trazas de consentimiento persistidos en la base de datos PostgreSQL.<br>3. Claves criptográficas institucionales de verificación activas en el servidor. |
| **PostCondiciones** | 1. Verificación de integridad de la cadena de hashes ejecutada sin detectar corrupciones.<br>2. Consulta forense de sólo lectura generada con registros paginados e inmutables.<br>3. Exportación de expediente de trazabilidad bajo la Ley Nº 29733 con firma digital de auditoría. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del registro forense de auditoría** | |
| **1.** El oficial de seguridad accede al módulo `"Auditoría de Seguridad y Ley 29733"` en `AuditLogView.tsx`. | **2.** En `auditService.ts`, se despacha `GET /api/v1/audit/logs?limit=50`. En `audit.py`, se valida el token con `require_security_officer_role`. `AuditService` ejecuta `SELECT l.*, u.email FROM log_auditoria_seguridad l JOIN usuarios u ON l.usuario_id = u.id ORDER BY l.id DESC LIMIT 50`. Retorna HTTP 200 con la nómina paginada. En `AuditLogView.tsx`, se renderiza una tabla con filtros por fecha, tipo de evento (`AUTH_2FA`, `ROLE_CHANGE`, `CONSENT_ACCEPT`, `CONSENT_REVOKE`), IP de origen y hash de bloque. (Si el usuario no cuenta con privilegios de seguridad, salta a E001). |
| **Fase 2: Filtrado por usuario y verificación de traza legal de consentimiento** | |
| **3.** El oficial introduce el correo institucional de un estudiante o docente en el buscador para auditar su historial de consentimiento digital. | **4.** En `auditService.ts`, se despacha `GET /api/v1/audit/consent-traces?email=...`. El backend retorna la secuencia completa de formalización: UUID, versión de términos aceptada, IP de origen, User-Agent, fecha UTC y estado de revocación. `AuditLogView.tsx` despliega el expediente digital del titular de los datos. |
| **Fase 3: Verificación criptográfica de la cadena de auditoría (Hash Chain)** | |
| **5.** El oficial presiona el botón `"Verificar Integridad de Cadena de Logs"`. | **6.** En `auditService.ts`, se despacha `POST /api/v1/audit/verify-chain`. En `audit_service.py`, se itera secuencialmente por la tabla de auditoría recomputando recursivamente `SHA256(registro_anterior_hash + registro_actual_data)` y comparándolo con el valor almacenado en `hash_bloque`. Al comprobar que todas las firmas coinciden, retorna HTTP 200 `{"status": "VALID", "records_verified": count, "tampering_detected": false}`. En `AuditLogView.tsx`, se despliega una insignia destacada en color verde con la leyenda *"Cadena de Auditoría Íntegra y Verificada (0 Alteraciones)"* y se habilita el botón de exportación de expediente legal. (Si el sistema detecta una inconsistencia en la cadena de hashes, salta a E002). |

##### Flujos de Excepción

##### Flujo de excepción E001: Permisos insuficientes para auditoría de seguridad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 2 del Flujo Normal, el interceptor de seguridad en `audit.py` comprueba que el token JWT carece de rol de Oficial de Seguridad o Administrador Institucional. Lanza `HTTPException(status_code=403, detail="FORBIDDEN_AUDIT: Acceso restringido. Se requieren credenciales de Oficial de Seguridad para auditar registros forenses.")`.<br><br>En `App.tsx`, se captura el error 403 y se redirige al panel estándar del usuario desplegando una alerta en color rojo. |
| **E001-1.2** Hace clic en el botón "Aceptar" en la alerta de restricción. | **E001-1.3** Cierra el aviso y retorna al paso 1 del Flujo Normal de Eventos en su vista autorizada. |

##### Flujo de excepción E002: Inconsistencia detectada en la cadena criptográfica de logs
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 6 del Flujo Normal, `AuditService.verify_chain_integrity` detecta una discrepancia entre el hash recalculado y el hash almacenado en un bloque específico (evidencia de manipulación o corrupción de datos). Lanza `HTTPException(status_code=409, detail="AUDIT_TAMPERING_DETECTED: ¡Alerta Crítica! Se detectó una inconsistencia en la cadena de hashes en el registro ID {broken_id}.")`.<br><br>En `AuditLogView.tsx`, la interfaz conmuta inmediatamente a un estado de alarma en color rojo parpadeante, resalta la fila alterada y genera una entrada prioritaria en el sistema de seguridad institucional. |
| **E002-1.2** Presiona el botón "Descargar Informe Forense de Incidencia". | **E002-1.3** Emite el volcado forense de la discrepancia para su remisión a las autoridades universitarias y finaliza el caso de uso registrando el incidente de seguridad institucional. |

#### CUS-020 - Configurar parámetros institucionales y umbrales

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-020** (CUS-020) |
| **Nombre** | Configurar parámetros operativos institucionales y umbrales de gobernanza |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-024 (Priorización institucional y realce algorítmico); RN-04 (Umbral temporal T-24h), RN-05 (Aforos máximos 10 y 20), RN-10 (Quórum mínimo de 3 estudiantes), RN-14 (Horas de acreditación) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a las autoridades de la EPIS-UPT parametrizar y calibrar las reglas de negocio globales y umbrales operacionales del sistema sin requerir modificaciones en el código fuente a través del componente cliente `SystemSettingsView.tsx` y el servicio `configService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/config.py` y `app/services/config_service.py` procesan las peticiones `GET /api/v1/config/parameters` y `PUT /api/v1/config/parameters`. El administrador puede ajustar los aforos máximos presenciales y virtuales (RN-05), la ventana de antelación obligatoria para reservas y cancelaciones (RN-04), el quórum mínimo para confirmación automática de sesiones (RN-10) y el umbral de horas acumuladas para emisión de constancias (RN-14). Los parámetros se persisten en la tabla `parametros_institucionales` (`app/models/config.py`), invalidan la caché global de la aplicación y registran una traza auditada de modificación. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-08: Supervisión y Analítica Institucional)<br>Reglamento General de Mentorías Universitarias EPIS-UPT |
| **Anexos** | `aplicacion/frontend/src/components/SystemSettingsView.tsx`<br>`aplicacion/frontend/src/services/configService.ts` (`ConfigService`, `ApiConfigAdapter`)<br>`aplicacion/backend/app/api/v1/endpoints/config.py` (`GET /api/v1/config/parameters`, `PUT /api/v1/config/parameters`)<br>`aplicacion/backend/app/services/config_service.py` (`ConfigService.get_parameters`, `ConfigService.update_parameters`)<br>`aplicacion/backend/app/models/config.py` (`ParametroInstitucional`), `app/models/auth.py` (`LogAuditoriaSeguridad`) |
| **Precondiciones** | 1. Administrador institucional autenticado con token JWT portando claim `administrador`.<br>2. Catálogo de parámetros base inicializado en la tabla `parametros_institucionales`.<br>3. Autenticación de doble factor reconfirmada para modificaciones críticas de configuración. |
| **PostCondiciones** | 1. Registro actualizado en la tabla física `parametros_institucionales` en PostgreSQL.<br>2. Invalidación atómica de la caché en memoria del servidor de aplicaciones.<br>3. Despliegue de confirmación en cliente y aplicación inmediata de los nuevos umbrales operacionales. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta de parámetros vigentes y despliegue del panel** | |
| **1.** El administrador accede a `"Configuración del Sistema"` en `SystemSettingsView.tsx`. | **2.** En `configService.ts`, se despacha `GET /api/v1/config/parameters`. En `config.py`, se valida el rol administrativo. `ConfigService.get_parameters` ejecuta `SELECT clave, valor, descripcion, tipo_dato, valor_min, valor_max FROM parametros_institucionales WHERE activo = true`. Retorna HTTP 200 con el diccionario de parámetros. En `SystemSettingsView.tsx`, se renderiza un formulario organizado por categorías: 1) Aforos Institucionales (Presencial máx 10, Virtual máx 20), 2) Ventana de Antelación (24 horas), 3) Quórum Mínimo (3 confirmados), y 4) Horas de Certificación (20 horas). |
| **Fase 2: Edición de umbrales y validación de rangos permitidos** | |
| **3.** El administrador modifica uno o más valores numéricos (e.g. ajusta el quórum mínimo a 4 estudiantes para períodos de alta demanda) y presiona el botón `"Guardar Parámetros Institucionales"`. | **4.** En `SystemSettingsView.tsx`, se ejecutan validaciones en cliente comprobando que los nuevos valores se encuentren dentro de los rangos operacionales permitidos (`valor_min <= valor <= valor_max`). En `configService.ts`, se despacha `PUT /api/v1/config/parameters` con el payload `ParameterUpdatePayload`. En `config.py`, el controlador valida el esquema y delega a `config_service.py`. (Si un parámetro numérico excede los límites institucionales de seguridad, salta a E001). (Si la sesión requiere reautenticación administrativa para cambios críticos, salta a E002). |
| **Fase 3: Persistencia transaccional, purga de caché y aplicación en caliente** | |
| **5.** El administrador observa el indicador circular de guardado seguro. | **6.** En `config_service.py`, se inicia una transacción ACID. Se ejecutan las sentencias `UPDATE parametros_institucionales SET valor = :val, fecha_modificacion = NOW(), modificado_por = :uid WHERE clave = :key`. Se inserta el evento en `log_auditoria_seguridad`. Se confirma la transacción con `db.commit()`. El servicio purga la caché interna del servidor para forzar la recarga de los nuevos umbrales en todos los módulos dependientes (ofertas, reservas y quórum). Retorna HTTP 200 con los parámetros actualizados. En cliente, `SystemSettingsView.tsx` despliega una notificación flotante en color verde de éxito: *"Parámetros institucionales actualizados y aplicados en caliente exitosamente"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Parámetro fuera de los rangos institucionales permitidos
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `config_service.py` comprueba que el valor propuesto supera los límites de seguridad institucional (e.g. se intenta fijar un aforo presencial mayor a 30 cupos excediendo la capacidad de los laboratorios). Lanza `HTTPException(status_code=422, detail="PARAMETER_OUT_OF_BOUNDS: El valor ingresado para '{param_key}' excede los límites operacionales autorizados por la Dirección de Escuela.")`.<br><br>En `SystemSettingsView.tsx`, se resalta el campo observado en color rojo y se muestra el rango admisible. |
| **E001-1.2** Corrige el valor ingresando un número dentro del rango permitido. | **E001-1.3** Rehabilita el botón de guardado y retorna al paso 3 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Reautenticación de seguridad requerida
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, al modificar parámetros de gobernanza crítica, el sistema exige reconfirmación de clave o token OTP. Si el administrador no suministra la clave secundaria, `config.py` lanza `HTTPException(status_code=401, detail="REAUTH_REQUIRED: Se requiere confirmación de credenciales para modificar parámetros de gobernanza crítica.")`.<br><br>En `SystemSettingsView.tsx`, se abre una ventana modal solicitando la confirmación de identidad institucional. |
| **E002-1.2** Ingresa su contraseña institucional o código OTP de confirmación y presiona "Verificar". | **E002-1.3** Valida las credenciales secundarias y retorna al paso 4 del Flujo Normal de Eventos. |

#### CUS-022 - Gestionar catálogo de temas y materias críticas

| Atributo | Detalle |
|---|---|
| **Id Caso de Uso** | **UC-022** (CUS-022) |
| **Nombre** | Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial |
| **Tipo** | Obligatorio ( X ) / Opcional (   ) |
| **Requisito ID (RF)** | RF-005 (Gestión del catálogo de asignaturas y temarios), RF-026 (Auditoría administrativa de bitácoras y materias); RN-11 (Asignaturas filtro prioritarias) |
| **Versión** | 2.0 |
| **Autor** | Antayhua Mamani, Renzo Antonio / Medina Quispe, Joan Carlos |
| **Actores** | Administrador Institucional (`UserRole.administrador`), Director de Escuela EPIS |
| **Interacción** | Fase de Construcción / Iteración Sprint 07 - Sprint 08 |
| **Descripción** | Permite a la Dirección de Escuela y a los administradores actualizar la malla curricular de la EPIS-UPT, gestionar las asignaturas designadas como materias filtro (`es_filtro = true`) y dar de alta, modificar o desactivar temas silábicos de aprendizaje a través del componente cliente `AdminCurriculumView.tsx` y el servicio `curriculumService.ts`. El backend `aplicacion/backend/app/api/v1/endpoints/curriculum.py` y `app/services/curriculum_service.py` procesan las peticiones `POST /api/v1/curriculum/courses`, `PUT /api/v1/curriculum/courses/{id}`, `POST /api/v1/curriculum/courses/{id}/topics` y `DELETE /api/v1/curriculum/topics/{id}`. El servicio valida que los temas ingresados correspondan a las unidades didácticas del semestre lectivo vigente (semanas 1 a 17), previene duplicidades conceptuales mediante comprobaciones de unicidad en `temas_curriculares` (`app/models/curriculum.py`) y asegura la consistencia referencial con las ofertas de mentoría y solicitudes de demanda en curso. |
| **Referencias** | Guía SWEBOK v3.0 (Capítulo 1: Requisitos de Software y Capítulo 2: Diseño de Software)<br>Estándar ISO/IEC/IEEE 29148:2018 y Criterios ICACIT 2026<br>Documento de Arquitectura de Software (SAD v2.0 - MOD-02: Gestión Curricular y Perfiles Académicos)<br>Plan de Estudios y Sílabos Oficiales de Ingeniería de Sistemas UPT |
| **Anexos** | `aplicacion/frontend/src/components/AdminCurriculumView.tsx`<br>`aplicacion/frontend/src/services/curriculumService.ts` (`CurriculumService.manageCurriculum`)<br>`aplicacion/backend/app/api/v1/endpoints/curriculum.py` (`POST /api/v1/curriculum/courses`, `POST /api/v1/curriculum/courses/{id}/topics`)<br>`aplicacion/backend/app/services/curriculum_service.py` (`CurriculumService.create_course`, `CurriculumService.manage_topics`)<br>`aplicacion/backend/app/models/curriculum.py` (`Carrera`, `Curso`, `TemaCurricular`), `app/models/offer.py` (`SesionMentoria`) |
| **Precondiciones** | 1. Usuario con credenciales de Administrador Institucional o Director de Escuela.<br>2. Plan de estudios registrado en la tabla `carreras` en la base de datos.<br>3. Número de semana lectiva comprendido entre las semanas 1 y 17 del calendario académico. |
| **PostCondiciones** | 1. Entidad `Curso` o `TemaCurricular` insertada o actualizada en la tabla física de PostgreSQL.<br>2. Transacción ACID confirmada con `db.commit()` e indexación para el motor de búsqueda.<br>3. Actualización reactiva del árbol curricular en la interfaz administrativa. |

##### Flujo Normal de Eventos

| Usuario | Sistema |
|---|---|
| **Fase 1: Consulta del árbol curricular y selección de asignatura** | |
| **1.** El administrador accede a `"Gestión de Malla y Temarios"` en `AdminCurriculumView.tsx`. | **2.** En `curriculumService.ts`, se despacha `GET /api/v1/curriculum/courses`. En `curriculum.py`, `curriculum_service.py` recupera la estructura completa de asignaturas ordenadas por ciclo. En `AdminCurriculumView.tsx`, se renderiza una vista en árbol con las materias clasificadas por ciclo y la etiqueta *"Materia Filtro"* en aquellas con `es_filtro = true`. El administrador hace clic sobre una asignatura específica para desplegar sus temas silábicos. |
| **Fase 2: Ingreso de datos del nuevo tema curricular silábico** | |
| **3.** El administrador presiona el botón `"Agregar Nuevo Tema Curricular"` en el panel de la asignatura. | **4.** En `AdminCurriculumView.tsx`, se abre una ventana modal con los campos: número de unidad didáctica (1 a 4), título descriptivo del tema, semana académica programada (semanas 1 a 17) y descripción conceptual. El administrador completa los campos y pulsa el botón `"Registrar Tema Curricular"`. (Si el título del tema ya existe en esa misma unidad, salta a E001). (Si el número de semana está fuera del calendario lectivo de 1 a 17, salta a E002). |
| **Fase 3: Persistencia transaccional y actualización del catálogo** | |
| **5.** El administrador observa el indicador circular de guardado en el botón del modal. | **6.** En `curriculumService.ts`, se despacha `POST /api/v1/curriculum/courses/{id}/topics` con el payload `TopicCreateRequest`. En `curriculum.py`, `curriculum_service.py` inicia la transacción con `db.begin()`. Valida que el curso exista y que no exista una tupla idéntica `(curso_id, unidad, titulo)`. Inserta en `temas_curriculares`, ejecuta `db.commit()` y retorna HTTP 201 Created. En cliente, `AdminCurriculumView.tsx` cierra el modal, añade el nuevo tema al árbol curricular en pantalla y despliega una notificación flotante en color verde de éxito: *"Tema curricular registrado y disponible para ofertas y demandas académicas"*. |

##### Flujos de Excepción

##### Flujo de excepción E001: Tema curricular duplicado en la misma unidad
| Usuario | Sistema |
|---|---|
| | **E001-1.1** En el paso 4 del Flujo Normal, `curriculum_service.py` detecta que ya existe un tema con el mismo título para la misma unidad didáctica del curso. Lanza `HTTPException(status_code=409, detail="DUPLICATE_TOPIC: Ya existe un tema curricular registrado con ese título para la unidad seleccionada.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el cuadro de texto del título en color rojo con el mensaje de duplicidad. |
| **E001-1.2** Modifica el título del tema especificando con mayor precisión el contenido temático. | **E001-1.3** Rehabilita el botón de guardado en el modal y retorna al paso 4 del Flujo Normal de Eventos. |

##### Flujo de excepción E002: Número de semana lectiva fuera de rango semestral
| Usuario | Sistema |
|---|---|
| | **E002-1.1** En el paso 4 del Flujo Normal, Pydantic en `curriculum.py` comprueba que el campo `semana` es menor a 1 o mayor a 17 (duración máxima del semestre lectivo universitario). Lanza `HTTPException(status_code=422, detail="VALIDATION_ERROR: El número de semana académica debe estar comprendido estrictamente entre 1 y 17.")`.<br><br>En `AdminCurriculumView.tsx`, se resalta el campo numérico de semana en color rojo. |
| **E002-1.2** Ingresa un número de semana válido dentro del intervalo 1 a 17. | **E002-1.3** Actualiza el valor en el estado del formulario y retorna al paso 4 del Flujo Normal de Eventos. |


---

# 6.3. Modelo Lógico

El modelo lógico traduce los requerimientos funcionales y las especificaciones narrativas de los casos de uso en una representación analítica abstracta, orientada a objetos e independiente de la plataforma tecnológica final. Mediante esta modelación, el equipo de ingeniería formaliza las colaboraciones internas, los flujos dinámicos de datos y las responsabilidades operacionales de las entidades del dominio de la EPIS-UPT, asegurando una transición fluida hacia el diseño de software detallado y la implementación bajo el marco metodológico UWE.


---

## 6.3.1. Análisis de Objetos

### Presentación del Análisis de Objetos
Para descomponer las responsabilidades funcionales y aislar la lógica de presentación, de control y de persistencia, se emplea el patrón analítico **Entidad-Control-Frontera (ECB - Entity-Control-Boundary)** propuesto por Ivar Jacobson y adoptado en UWE. El análisis se focaliza en el subsistema neurálgico del proyecto: el ciclo de **Reserva de Cupos, Ratificación y Control de Quórum** (`CUS04`, `CUS24`, `CUS23` y `CUS07`). A través de este modelo, se explicita cómo las interfaces de usuario (Boundary) canalizan las peticiones de los actores hacia controladores especializados (Control), los cuales hacen cumplir las reglas de negocio (RN-05, RN-08, RN-09, RN-10) interactuando con las entidades de dominio persistentes (Entity) y los servicios de infraestructura externa.

A continuación, se presenta el diagrama de robustez y análisis de objetos correspondiente.

### Diagrama 6.13: Diagrama de Análisis de Objetos (Modelo ECB) - Flujo de Reservas y Quórum

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - Gestión de Reservas, Confirmación y Quórum\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

' ===================================================
' ACTORES
' ===================================================
actor "Mentoreado" as ActMentoreado
actor "Mentor" as ActMentor
actor "Servicio Cron\n(Backend)" as ActCron

' ===================================================
' OBJETOS FRONTERA (BOUNDARY)
' ===================================================
boundary "UI_CatalogoRecomendador" as B_Catalogo
boundary "UI_GestionReservas" as B_Reservas
boundary "UI_ResolucionQuorum" as B_Quorum
boundary "AdaptadorNotificacionEmail" as B_EmailService

' ===================================================
' OBJETOS DE CONTROL (CONTROL)
' ===================================================
control "ControladorReservaCupo" as C_Reserva
control "ControladorConfirmacionAsistencia" as C_Confirmacion
control "DemonioEvaluadorQuorum" as C_EvaluadorQuorum
control "ControladorResolucionSesion" as C_Resolucion

' ===================================================
' OBJETOS DE ENTIDAD (ENTITY)
' ===================================================
entity "Usuario" as E_Usuario
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "EspacioFisico" as E_Aula
entity "EspacioVirtual" as E_SalaVirtual

' ===================================================
' RELACIONES Y FLUJOS
' ===================================================
' Flujo de Reserva (CUS04)
ActMentoreado --> B_Catalogo : 1. Solicita reserva cupo
B_Catalogo --> C_Reserva : 1.1. reservarCupo(idSesion, idUsuario)
C_Reserva ..> E_Usuario : 1.2. verificarElegibilidadMentoreado()
C_Reserva ..> E_Sesion : 1.3. validarAforoDisponible(lock=true)
C_Reserva --> E_Reserva : 1.4. crearReserva(estado=PENDIENTE_CONFIRMACION)
C_Reserva ..> B_EmailService : 1.5. enviarAlertaReservaTemporal()

' Flujo de Confirmación (CUS24)
ActMentoreado --> B_Reservas : 2. Ratifica asistencia
B_Reservas --> C_Confirmacion : 2.1. confirmarAsistencia(idReserva)
C_Confirmacion ..> E_Reserva : 2.2. validarVentanaT24h() [T >= 24h]
C_Confirmacion --> E_Reserva : 2.3. actualizarEstado(CONFIRMADA)
C_Confirmacion ..> B_EmailService : 2.4. emitirTicketDigitalQR()

' Flujo de Evaluación de Quórum en T-24h (CUS23)
ActCron --> C_EvaluadorQuorum : 3. Disparo temporizado periódico
C_EvaluadorQuorum ..> E_Sesion : 3.1. buscarSesionesEnVentanaCorte(T=24h)
C_EvaluadorQuorum --> E_Reserva : 3.2. revocarNoConfirmadas(estado=NO_CONFIRMADA)
C_EvaluadorQuorum ..> E_Reserva : 3.3. contarConfirmadas()
C_EvaluadorQuorum --> E_Sesion : 3.4. actualizarEstadoSesion(CONFIRMADA o QUORUM_INSUFICIENTE)
C_EvaluadorQuorum ..> B_EmailService : 3.5. despacharCredencialesOAlertas()

' Flujo de Resolución de Quórum Insuficiente (CUS07)
ActMentor --> B_Quorum : 4. Consulta sesión en alerta
B_Quorum --> C_Resolucion : 4.1. resolverSesion(idSesion, decision)
C_Resolucion --> E_Sesion : 4.2. aplicarTransicion(CONFIRMADA_EXCEPCIONAL o CANCELADA_QUORUM)
C_Resolucion ..> E_Aula : 4.3. liberarRecursoFisico() [si cancela]
C_Resolucion ..> E_SalaVirtual : 4.4. revocarSalaMeet() [si cancela]
C_Resolucion ..> B_EmailService : 4.5. notificarResolucionInscritos()
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos pone de manifiesto la robustez del diseño ante requerimientos concurrentes y temporales:
1. **Desacoplamiento Estricto de Responsabilidades:** Las clases de frontera (`UI_CatalogoRecomendador`, `UI_GestionReservas`, `UI_ResolucionQuorum`) no manipulan el estado persistente directamente; delegan la orquestación en controladores especializados (`ControladorReservaCupo`, `ControladorConfirmacionAsistencia`, `DemonioEvaluadorQuorum`).
2. **Encapsulamiento de Reglas Críticas:** El `ControladorReservaCupo` encapsula la política de aforos máximos (RN-05) y la verificación de elegibilidad institucional del mentoreado, procesando transacciones atómicas orientadas a prevenir la sobreasignación de cupos.
3. **Autonomía del Demonio Cron:** El componente `DemonioEvaluadorQuorum` opera de forma desatendida, asumiendo la depuración de reservas no confirmadas y el cálculo del 50% de quórum (RN-09), liberando de carga computacional a las interacciones de los usuarios finales.

### 6.3.1.1. CUS01 – Análisis de Objetos: Iniciar Sesión Institucional con 2FA

El análisis de objetos para el caso de uso `CUS01` descompone las responsabilidades arquitectónicas de la autenticación institucional con segundo factor de autenticación (2FA). Se identifican los objetos de frontera (*Boundary*) que gestionan la interacción con el usuario en el navegador y con el servidor de correo institucional SMTP de la UPT; los objetos de control (*Control*) encargados de la verificación de claves temporales, la formalización del consentimiento legal obligatorio (Ley N° 29733) y la emisión de tokens criptográficos JWT; y los objetos de entidad (*Entity*) que mantienen el estado persistente de las cuentas universitarias, las credenciales efímeras OTP y el registro auditable de consentimiento.

#### Diagrama 6.13.1: Análisis de Objetos (Modelo ECB) - CUS01: Iniciar Sesión Institucional con 2FA

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS01: Iniciar Sesión Institucional con 2FA\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Usuario Institucional\n(Mentoreado / Mentor / Admin)" as ActUser
actor "Servicio SMTP / UPT" as ActSMTP <<Sistema Externo>>

boundary "UI_LoginInstitucional" as B_Login
boundary "UI_ValidacionOTP" as B_OTP
boundary "UI_ModalConsentimiento" as B_Consent
boundary "AdaptadorEmailSMTP" as B_AdaptadorSMTP

control "ControladorAutenticacion" as C_Auth
control "GestorConsentimientoLegal" as C_Consent
control "GeneradorTokenJWT" as C_JWT

entity "Usuario" as E_User
entity "CredencialOTP" as E_OTP
entity "RegistroConsentimiento" as E_ConsentDoc

ActUser --> B_Login : 1. Ingresa correo @upt.pe
B_Login --> C_Auth : 1.1. solicitarCodigoAcceso(correo)
C_Auth ..> E_User : 1.2. validarPertenenciaYEstado()
C_Auth --> E_OTP : 1.3. generarClaveEfimera(expira=5min)
C_Auth ..> B_AdaptadorSMTP : 1.4. despacharCodigoOTP(correo, otp)
B_AdaptadorSMTP --> ActSMTP : 1.5. remitirMensajeCorreo()

ActUser --> B_OTP : 2. Introduce código OTP de 6 dígitos
B_OTP --> C_Auth : 2.1. verificarCodigoOTP(correo, otp)
C_Auth --> E_OTP : 2.2. validarVigenciaYConsumir()
C_Auth ..> E_User : 2.3. consultarEstadoConsentimiento()

alt Primer Acceso (Sin consentimiento previo)
    C_Auth --> B_Consent : 2.4. requerirAceptacionLey29733()
    ActUser --> B_Consent : 3. Acepta términos y condiciones
    B_Consent --> C_Consent : 3.1. formalizarConsentimiento(idUsuario, ip, timestamp)
    C_Consent --> E_ConsentDoc : 3.2. persistirConsentimiento()
    C_Consent --> C_Auth : 3.3. consentimientoConfirmado()
end

C_Auth --> C_JWT : 4. emitirTokenSesion(idUsuario, rol)
C_JWT --> B_Login : 4.1. retornarTokenAcceso(JWT)
B_Login --> ActUser : 5. Redirige a Dashboard según Rol
@enduml
```

Fuente: Elaboración propia.

El modelo ECB evidencia que la lógica de seguridad y validación de doble factor permanece rigurosamente centralizada en `ControladorAutenticacion`, evitando que las vistas capturen o manipulen directamente los estados de persistencia. La delegación hacia `AdaptadorEmailSMTP` aísla las particularidades de red del servidor SMTP universitario, mientras que la bifurcación condicional de primer acceso asegura que ningún token de sesión JWT sea emitido sin contar con la confirmación previa del objeto `RegistroConsentimiento` respaldado en base de datos bajo la Ley N° 29733 (RN-02).

### 6.3.1.2. CUS04 – Análisis de Objetos: Reservar Cupo de Mentoría

El análisis de objetos para el caso de uso `CUS04` delimita los componentes de frontera, control y entidad que colaboran en la reserva concurrente de cupos para una sesión de mentoría. Se modelan las interfaces de usuario para la exploración de la oferta y la confirmación de la reserva preliminar (`UI_DetalleOferta`, `UI_ModalConfirmacionReserva`); el orquestador transaccional `ControladorReservaCupo` que encapsula la verificación atómica de aforos reglamentarios (RN-05) y delega la validación de elegibilidad en `ValidadorElegibilidadEstudiante`; y las entidades persistentes `Usuario`, `SesionMentoria` y `ReservaCupo` encargadas de registrar la vacante apartada en estado `PENDIENTE_CONFIRMACION`.

#### Diagrama 6.13.2: Análisis de Objetos (Modelo ECB) - CUS04: Reservar Cupo de Mentoría

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS04: Reservar Cupo de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentoreado" as ActMentee

boundary "UI_DetalleOferta" as B_Detalle
boundary "UI_ModalConfirmacionReserva" as B_ModalConfirm

control "ControladorReservaCupo" as C_Reserva
control "ValidadorElegibilidadEstudiante" as C_Elegibilidad

entity "Usuario" as E_User
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva

ActMentee --> B_Detalle : 1. Selecciona sesión y presiona "Reservar Cupo"
B_Detalle --> C_Reserva : 1.1. reservarCupo(idSesion, idUsuario)

C_Reserva ..> C_Elegibilidad : 1.2. verificarElegibilidadYCruces(idUsuario, idSesion)
C_Elegibilidad ..> E_User : 1.3. consultarCicloYEstado()
C_Elegibilidad ..> E_Reserva : 1.4. verificarAusenciaCrucesHorarios()

C_Reserva --> E_Sesion : 1.5. bloquearFilaYVerificarAforo(lock=true) [RN-05]
C_Reserva --> E_Reserva : 1.6. crearReserva(estado=PENDIENTE_CONFIRMACION)
C_Reserva --> E_Sesion : 1.7. incrementarCuposOcupados()

C_Reserva --> B_ModalConfirm : 1.8. notificarReservaExitosa(idReserva, plazoCorteT24)
B_ModalConfirm --> ActMentee : 2. Despliega confirmación y temporizador hacia T-24h
@enduml
```

Fuente: Elaboración propia.

El análisis ECB de CUS04 demuestra la estricta separación de responsabilidades en la reserva concurrente. La interfaz `UI_DetalleOferta` no efectúa cálculos de aforo ni altera directamente los registros; delega en `ControladorReservaCupo`, el cual coordina con `ValidadorElegibilidadEstudiante` la comprobación del ciclo formativo y la prevención de reservas duplicadas o solapadas. La operación sobre `SesionMentoria` se ejecuta bajo un bloqueo a nivel de fila que previene la sobreventa de cupos frente a peticiones simultáneas, instanciando la entidad `ReservaCupo` en estado `PENDIENTE_CONFIRMACION` para su posterior ratificación en CUS24.

### 6.3.1.3. CUS24 – Análisis de Objetos: Confirmar Asistencia a Mentoría

El análisis de objetos para el caso de uso `CUS24` modela los componentes arquitectónicos encargados de procesar la ratificación anticipada y obligatoria de asistencia estudiantil. Se identifican las fronteras de usuario y adaptadores de notificación (`UI_MisReservas`, `UI_VisorTicketQR`, `AdaptadorEmailSMTP`); los componentes de control especializados en validar la ventana temporal perentoria de 24 horas (`ControladorConfirmacionAsistencia`) y en la emisión criptográfica de credenciales (`GeneradorTicketQR`); y las entidades del dominio `Usuario`, `SesionMentoria`, `ReservaCupo` y `TicketAsistencia` que consolidan la confirmación formal del quórum.

#### Diagrama 6.13.3: Análisis de Objetos (Modelo ECB) - CUS24: Confirmar Asistencia a Mentoría

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS24: Confirmar Asistencia a Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentoreado" as ActMentee
actor "Servicio SMTP / UPT" as ActSMTP <<Sistema Externo>>

boundary "UI_MisReservas" as B_MisReservas
boundary "UI_VisorTicketQR" as B_TicketVisor
boundary "AdaptadorEmailSMTP" as B_SMTP

control "ControladorConfirmacionAsistencia" as C_Confirm
control "GeneradorTicketQR" as C_QR

entity "Usuario" as E_User
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "TicketAsistencia" as E_Ticket

ActMentee --> B_MisReservas : 1. Selecciona reserva y pulsa "Confirmar Asistencia"
B_MisReservas --> C_Confirm : 1.1. ratificarAsistencia(idReserva, idUsuario)

C_Confirm ..> E_Reserva : 1.2. consultarEstadoYFechas()
C_Confirm ..> E_Sesion : 1.3. validarVentanaCorteT24h() [RN-08]

alt Plazo vigente (T >= 24h)
    C_Confirm --> E_Reserva : 1.4. actualizarEstado(CONFIRMADA)
    C_Confirm --> C_QR : 1.5. generarTicketDigitalQR(idReserva)
    C_QR --> E_Ticket : 1.6. crearTicket(tokenHash, qrBase64)
    C_Confirm ..> B_SMTP : 1.7. despacharTicketEmail(correo, ticket)
    B_SMTP --> ActSMTP : 1.8. remitirTicketAdjunto()
    C_Confirm --> B_TicketVisor : 1.9. desplegarAccesoDefinitivo(aulaOEnlace, ticket)
    B_TicketVisor --> ActMentee : 2. Muestra ticket QR y datos de acceso
else Plazo cerrado (T < 24h)
    C_Confirm --> B_MisReservas : 1.10. notificarPlazoVencido(E01)
    B_MisReservas --> ActMentee : 3. Alerta de revocación reglamentaria
end
@enduml
```

Fuente: Elaboración propia.

El modelo ECB evidencia que la lógica temporal de ratificación recae en `ControladorConfirmacionAsistencia`, el cual valida que la petición ocurra con una antelación mínima de 24 horas ($T \ge 24\text{ h}$, conforme a RN-08). Al verificarse la condición, la entidad `ReservaCupo` transiciona al estado definitivo `CONFIRMADA`, desencadenando la creación asíncrona del objeto `TicketAsistencia` mediante `GeneradorTicketQR` y liberando la información de infraestructura (aula física en la EPIS o sala virtual de teleconferencia).

### 6.3.1.4. CUS23 – Análisis de Objetos: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

El análisis de objetos para el caso de uso `CUS23` modela los componentes del subsistema desatendido responsable de efectuar el corte reglamentario de asistencia y la evaluación automática de quórum en la ventana perentoria de 24 horas previas al inicio de la sesión. Se identifican las fronteras de ejecución batch y comunicación (`DemonioEvaluadorQuorum`, `AdaptadorEmailSMTP`); el controlador de procesamiento transaccional (`ControladorEvaluacionQuorum`); y las entidades del dominio (`SesionMentoria`, `ReservaCupo`, `Usuario`) que experimentan transiciones de estado irrevocables para garantizar el uso eficiente de los recursos institucionales.

#### Diagrama 6.13.4: Análisis de Objetos (Modelo ECB) - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Demonio Cron / Planificador" as ActCron <<Servicio del Sistema>>
actor "Servicio SMTP / UPT" as ActSMTP <<Sistema Externo>>

boundary "DemonioEvaluadorQuorum" as B_Worker
boundary "AdaptadorEmailSMTP" as B_SMTP

control "ControladorEvaluacionQuorum" as C_Quorum

entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "Usuario" as E_Usuario

ActCron --> B_Worker : 1. Disparo periódico programado (cada 15 min)
B_Worker --> C_Quorum : 1.1. ejecutarCorteQuorumT24()

C_Quorum ..> E_Sesion : 1.2. consultarSesionesEnVentanaCorte(PUBLICADA, T <= 24h)

loop Por cada sesión detectada en T-24h
    C_Quorum --> E_Reserva : 1.3. revocarReservasNoConfirmadas(idSesion) [RN-08]
    note right: PENDIENTE_CONFIRMACION\n-> NO_CONFIRMADA
    
    C_Quorum ..> E_Reserva : 1.4. contarReservasConfirmadas(idSesion)
    C_Quorum ..> E_Sesion : 1.5. verificarAforoMaximo(idSesion)
    
    alt Quórum alcanzado (Confirmadas >= 50% Aforo) [RN-09]
        C_Quorum --> E_Sesion : 1.6. actualizarEstado(CONFIRMADA)
        C_Quorum ..> B_SMTP : 1.7. despacharNotificacionSesionConfirmada(idSesion)
        B_SMTP --> ActSMTP : 1.8. remitirRecordatorioDefinitivo(Mentor y Mentees)
    else Quórum insuficiente (Confirmadas < 50% Aforo) [RN-09]
        C_Quorum --> E_Sesion : 1.9. actualizarEstado(QUORUM_INSUFICIENTE)
        C_Quorum ..> B_SMTP : 1.10. despacharAlertaQuorumInsuficiente(idSesion)
        B_SMTP --> ActSMTP : 1.11. remitirAlertaUrgente(Mentor para CUS07)
    end
end
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS23 demuestra el desacoplamiento entre el temporizador desatendido del sistema y la lógica de negocio del corte de quórum. La entidad `ReservaCupo` sufre una revocación masiva automática de aquellas plazas que permanecieron en `PENDIENTE_CONFIRMACION`, mutando a `NO_CONFIRMADA` sin penalización conforme a RN-08 y RN-10. En función del cómputo estricto del umbral del 50% estipulado en RN-09, `ControladorEvaluacionQuorum` transiciona la entidad `SesionMentoria` hacia `CONFIRMADA` o `QUORUM_INSUFICIENTE`, delegando en `AdaptadorEmailSMTP` las comunicaciones oficiales inmediatas hacia los estudiantes y el mentor académico.

### 6.3.1.5. CUS07 – Análisis de Objetos: Gestionar Sesión ante Quórum Insuficiente

El análisis de objetos para el caso de uso `CUS07` formaliza los componentes que intervienen en la toma de decisión del mentor cuando una sesión no alcanza el 50% de cupos confirmados en la ventana de corte de 24 horas ($T-24\text{ h}$). Se identifican las fronteras de interacción y despacho (`UI_GestionQuorum`, `AdaptadorEmailSMTP`, `AdaptadorReservaAulas`); el componente de control (`ControladorResolucionQuorum`); y las entidades del modelo de dominio (`SesionMentoria`, `ReservaCupo`, `EspacioFisico`, `RegistroAuditoria`) involucradas en la ratificación del dictado excepcional o en la cancelación regulada sin penalidad.

#### Diagrama 6.13.5: Análisis de Objetos (Modelo ECB) - CUS07: Gestionar Sesión ante Quórum Insuficiente

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS07: Gestionar Sesión ante Quórum Insuficiente\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentor" as ActMentor
actor "Servicio SMTP / UPT" as ActSMTP <<Sistema Externo>>

boundary "UI_GestionQuorum" as B_UI
boundary "AdaptadorEmailSMTP" as B_SMTP
boundary "AdaptadorReservaAulas" as B_Aulas

control "ControladorResolucionQuorum" as C_Res

entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "EspacioFisico" as E_Aula
entity "RegistroAuditoria" as E_Audit

ActMentor --> B_UI : 1. Visualiza alerta y opciones de resolución
B_UI --> C_Res : 1.1. resolverSesionQuorum(idSesion, idMentor, decision)

C_Res ..> E_Sesion : 1.2. verificarEstado(QUORUM_INSUFICIENTE)

alt Decisión: Dictado Excepcional (RN-09)
    C_Res --> E_Sesion : 1.3. actualizarEstado(CONFIRMADA_EXCEPCIONAL)
    C_Res ..> B_SMTP : 1.4. despacharAvisoDictadoExcepcional(idSesion)
    B_SMTP --> ActSMTP : 1.5. remitirConfirmacion(Mentees Confirmados)
    C_Res --> B_UI : 1.6. notificarExito("Sesión confirmada excepcionalmente")
    B_UI --> ActMentor : 2. Despliega confirmación de dictado
else Decisión: Cancelación por Falta de Quórum (RN-10)
    C_Res --> E_Sesion : 1.7. actualizarEstado(CANCELADA_QUORUM)
    C_Res --> E_Reserva : 1.8. cancelarReservasConfirmadas(CANCELADA_SISTEMA)
    C_Res ..> B_Aulas : 1.9. desasignarAulaFisica(idAula, horario)
    B_Aulas --> E_Aula : 1.10. marcarDisponible()
    C_Res --> E_Audit : 1.11. registrarCancelacionSinPenalizacion(RN-10)
    C_Res ..> B_SMTP : 1.12. despacharAvisoCancelacionQuorum(idSesion)
    B_SMTP --> ActSMTP : 1.13. remitirAvisoCancelacion(Mentor y Mentees)
    C_Res --> B_UI : 1.14. notificarExito("Sesión cancelada sin penalización")
    B_UI --> ActMentor : 3. Despliega constancia de cancelación formal
end
@enduml
```

Fuente: Elaboración propia.

El análisis ECB para CUS07 expone el mecanismo de resolución ante el quórum insuficiente. `ControladorResolucionQuorum` valida que la sesión se encuentre legítimamente en estado `QUORUM_INSUFICIENTE` antes de aplicar la decisión del mentor. Si el mentor opta por asumir la sesión, `SesionMentoria` muta a `CONFIRMADA_EXCEPCIONAL`, preservando las reservas confirmadas y el aula asignada. Si decide la cancelación, la entidad muta a `CANCELADA_QUORUM`, forzando la liberación atómica de ambientes físicos o salas virtuales mediante `AdaptadorReservaAulas`, transicionando las reservas a `CANCELADA_SISTEMA` y registrando en `RegistroAuditoria` la exención estricta de penalidad según RN-10.

### 6.3.1.6. CUS09 – Análisis de Objetos: Publicar Oferta de Mentoría Individual o Grupal

El análisis de objetos para el caso de uso `CUS09` modela los componentes arquitectónicos encargados de recepcionar, validar y persistir las convocatorias académicas emitidas por los mentores. Se identifican las fronteras de usuario y servicios externos (`UI_PublicacionOferta`, `AdaptadorHorariosEPIS`, `AdaptadorMeetVirtual`); el controlador de negocio (`ControladorPublicacionMentoria`); y las entidades del dominio (`Usuario`, `SesionMentoria`, `Asignatura`, `EspacioFisico`) que encapsulan las reglas de elegibilidad docente (RN-01), anticipación mínima de 48 horas (RN-04) y límites de aforo diferencial (RN-05).

#### Diagrama 6.13.6: Análisis de Objetos (Modelo ECB) - CUS09: Publicar Oferta de Mentoría Individual o Grupal

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS09: Publicar Oferta de Mentoría Individual o Grupal\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentor" as ActMentor
actor "Servicio Google Meet" as ActMeet <<Sistema Externo>>

boundary "UI_PublicacionOferta" as B_UI
boundary "AdaptadorHorariosEPIS" as B_Horarios
boundary "AdaptadorMeetVirtual" as B_Meet

control "ControladorPublicacionMentoria" as C_Pub

entity "Usuario" as E_Mentor
entity "Asignatura" as E_Asignatura
entity "SesionMentoria" as E_Sesion
entity "EspacioFisico" as E_Aula

ActMentor --> B_UI : 1. Completa formulario de publicación (título, curso, fecha, modalidad, aforo)
B_UI --> C_Pub : 1.1. publicarSesion(datosOferta, idMentor)

C_Pub ..> E_Mentor : 1.2. validarElegibilidadMentor(idMentor) [RN-01]
C_Pub ..> E_Sesion : 1.3. validarAnticipacionMinima(fechaHora) [RN-04 >= 48h]
C_Pub ..> E_Sesion : 1.4. validarAforoMaximo(modalidad, aforo) [RN-05]

alt Modalidad Presencial
    C_Pub ..> B_Horarios : 1.5. verificarDisponibilidadAula(fechaHora, duracion)
    B_Horarios ..> E_Aula : 1.6. reservarAmbienteFisico()
    C_Pub --> E_Sesion : 1.7. crearSesion(aulaAsignada, PUBLICADA)
else Modalidad Virtual
    C_Pub ..> B_Meet : 1.8. solicitarEnlaceReunion(titulo, fechaHora)
    B_Meet --> ActMeet : 1.9. generarSalaVirtualAPI()
    ActMeet --> B_Meet : 1.10. enlaceGenerado (meet.google.com/...)
    B_Meet --> C_Pub : 1.11. urlSalaVirtual
    C_Pub --> E_Sesion : 1.12. crearSesion(enlaceVirtual, PUBLICADA)
end

C_Pub --> B_UI : 1.13. confirmarPublicacionExitosa(idSesion)
B_UI --> ActMentor : 2. Notifica publicación activa en el catálogo P2P
@enduml
```

Fuente: Elaboración propia.

El análisis ECB para CUS09 garantiza la integridad operativa de las sesiones desde su origen. `ControladorPublicacionMentoria` intercepta la creación y corrobora de forma estricta las precondiciones normativas: verifica que el estudiante posea el rol de mentor habilitado sin sanciones (RN-01), que la sesión se programe con al menos 48 horas de anticipación reglamentaria (RN-04) y que el aforo respete los topes máximos de 10 alumnos en presencial y 20 en virtual (RN-05). Asimismo, interactúa de forma polimórfica con los adaptadores de infraestructura para reservar físicamente un aula en los pabellones de la EPIS o autogenerar la sala virtual en Google Meet, instanciando la entidad `SesionMentoria` directamente en estado `PUBLICADA`.

### 6.3.1.7. CUS14 – Análisis de Objetos: Consultar Agenda y Horarios de Mentorías

El análisis de objetos para el caso de uso `CUS14` modela los componentes arquitectónicos dedicados a la recuperación, filtrado y renderizado dinámico de la programación académica institucional. Se identifican las fronteras de visualización y aceleración (`UI_AgendaCalendario`, `UI_PanelFiltros`, `CacheAgendaInMemory`); el componente de control (`ControladorConsultaAgenda`); y las entidades del modelo de datos (`SesionMentoria`, `Asignatura`, `Usuario`, `ReservaCupo`) requeridas para calcular el estado de ocupación, la disponibilidad de cupos en tiempo real (RN-05) y la condición de inscripción del estudiante solicitante.

#### Diagrama 6.13.7: Análisis de Objetos (Modelo ECB) - CUS14: Consultar Agenda y Horarios de Mentorías

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS14: Consultar Agenda y Horarios de Mentorías\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante / Mentor" as ActUser

boundary "UI_AgendaCalendario" as B_Calendario
boundary "UI_PanelFiltros" as B_Filtros
boundary "CacheAgendaInMemory" as B_Cache

control "ControladorConsultaAgenda" as C_Agenda

entity "SesionMentoria" as E_Sesion
entity "Asignatura" as E_Asignatura
entity "Usuario" as E_Docente
entity "ReservaCupo" as E_Reserva

ActUser --> B_Filtros : 1. Selecciona parámetros (mes, asignatura, modalidad)
B_Filtros --> B_Calendario : 1.1. dispararBusqueda(criteriosFiltro)
B_Calendario --> C_Agenda : 1.2. obtenerAgendaEventos(filtros, idUsuarioAutenticado)

C_Agenda ..> B_Cache : 1.3. consultarClaveCache(hashFiltros)

alt Caché disponible (Hit)
    B_Cache --> C_Agenda : 1.4. coleccionEventosSerializados
else Caché ausente o invalidada (Miss)
    C_Agenda ..> E_Sesion : 1.5. buscarSesionesPorRangoTemporal(fechaInicio, fechaFin)
    C_Agenda ..> E_Asignatura : 1.6. asociarMetadatosCurso()
    C_Agenda ..> E_Docente : 1.7. obtenerPerfilMentor()
    C_Agenda ..> E_Reserva : 1.8. verificarInscripcionUsuario(idUsuarioAutenticado)
    C_Agenda ..> B_Cache : 1.9. almacenarEnCache(hashFiltros, resultado, ttl=300s)
end

C_Agenda --> B_Calendario : 1.10. consolidarMatrizCalendario(eventosConCupos)
B_Calendario --> ActUser : 2. Renderiza calendario con distintivos de aforo y estado
@enduml
```

Fuente: Elaboración propia.

El análisis ECB para CUS14 demuestra el diseño optimizado para consultas de alta concurrencia (RNF01). `ControladorConsultaAgenda` orquesta la consulta de sesiones aplicando filtros dinámicos y coordinando con `CacheAgendaInMemory` (Redis) para amortiguar la carga transaccional de lectura. Al recuperar las instancias de `SesionMentoria`, el controlador consulta a `ReservaCupo` para determinar de forma reactiva si el usuario en sesión ya cuenta con una reserva activa o si existen cupos libres (`aforo_maximo - cupos_ocupados`), entregando a `UI_AgendaCalendario` un conjunto de datos consolidado para su renderizado mensual o semanal.

### 6.3.1.8. CUS11 – Análisis de Objetos: Registrar Asistencia Mediante Código QR

El análisis de objetos para el caso de uso `CUS11` modela los componentes del subsistema encargado del control y verificación de presencia física o virtual mediante lectura criptográfica de códigos QR. Se identifican las fronteras de captura visual (`UI_EscanerQR`, `UI_VisorTicketQR`); el controlador de procesamiento y validación criptográfica (`ControladorRegistroAsistencia`, `ValidadorTokenQR`); y las entidades del dominio (`SesionMentoria`, `ReservaCupo`, `TicketAsistencia`, `RegistroAsistencia`) que gobiernan la transición de la plaza hacia estado `ASISTIDA` bajo la ventana reglamentaria de tolerancia (RN-11).

#### Diagrama 6.13.8: Análisis de Objetos (Modelo ECB) - CUS11: Registrar Asistencia Mediante Código QR

```plantuml
@startuml
title Diagrama de Análisis de Objetos (Modelo ECB) - CUS11: Registrar Asistencia Mediante Código QR\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #1D2D44
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #0D9488
}

actor "Estudiante Mentor" as ActMentor
actor "Estudiante Mentoreado" as ActMentee

boundary "UI_VisorTicketQR" as B_TicketUI
boundary "UI_EscanerQR" as B_ScannerUI

control "ControladorRegistroAsistencia" as C_Asist
control "ValidadorTokenQR" as C_Token

entity "TicketAsistencia" as E_Ticket
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "RegistroAsistencia" as E_RegAsist

ActMentee --> B_TicketUI : 1. Exhibe ticket digital con código QR
ActMentor --> B_ScannerUI : 2. Enfoca cámara y captura imagen QR
B_ScannerUI --> C_Asist : 2.1. procesarLecturaQR(payloadEscaneado, idSesion)

C_Asist --> C_Token : 2.2. decodificarYVerificarFirma(tokenHash)
C_Token ..> E_Ticket : 2.3. consultarValidezCriptografica()

alt Token QR inválido o firma alterada (E01)
    C_Asist --> B_ScannerUI : 2.4. notificarErrorLectura("Firma digital inválida o adulterada")
    B_ScannerUI --> ActMentor : 3. Alerta de ticket fraudulento
else Token válido
    C_Asist ..> E_Sesion : 2.5. validarVentanaTolerancia(ahora) [RN-11: -15m a +30m]
    C_Asist ..> E_Reserva : 2.6. consultarEstadoReserva(idReserva)
    
    alt Reserva en estado CONFIRMADA y no registrada
        C_Asist --> E_Reserva : 2.7. mutarEstado(ASISTIDA)
        C_Asist --> E_RegAsist : 2.8. crearRegistro(idReserva, idSesion, timestamp, 'VALIDACION_QR')
        C_Asist --> B_ScannerUI : 2.9. confirmarAsistenciaExitosa(nombreEstudiante, codigo)
        B_ScannerUI --> ActMentor : 4. Feedback visual verde y sonido de confirmación
    else Reserva ya registrada o estado no apto (E02)
        C_Asist --> B_ScannerUI : 2.10. notificarRechazo("Ticket ya utilizado o reserva no ratificada")
        B_ScannerUI --> ActMentor : 5. Alerta de registro duplicado / no confirmado
    end
end
@enduml
```

Fuente: Elaboración propia.

El análisis ECB para CUS11 delimita la verificación criptográfica desacoplada de la cámara. `ControladorRegistroAsistencia` delega en `ValidadorTokenQR` la comprobación del hash SHA-256 para prevenir suplantaciones. Posteriormente, interactúa con `SesionMentoria` para comprobar que la lectura ocurra dentro de la ventana de tolerancia oficial fijada en RN-11 (desde 15 minutos antes hasta 30 minutos después del inicio). Superada la verificación, la entidad `ReservaCupo` transiciona irrevocablemente a `ASISTIDA` y se instancia el objeto `RegistroAsistencia`, proporcionando retroalimentación visual en menos de 1 segundo al mentor (RNF02).

### 6.3.1.9. CUS10 - Análisis de Objetos: Registrar Bitácora Pedagógica de Sesión

El análisis de objetos modela la estructura conceptual y la interacción colaborativa entre las interfaces de captura docente, las clases de control de negocio y las entidades de persistencia pedagógica durante el cierre formal de una sesión de mentoría. Se explicitan el actor *Estudiante Mentor*, el límite *UI Formulario Bitácora*, los controladores *Controlador de Bitácora Pedagógica*, *Validador de Plazo (RN-07)*, *Sincronizador de Asistencia (RN-11)* y *Calculador de Horas Formativas (RN-12)*, así como las entidades *SesionMentoria*, *BitacoraSesion*, *ReservaCupo*, *BolsaHorasMentor* y *RegistroAuditoria*.

#### Diagrama 6.13.9: Análisis de Objetos (Modelo ECB) - CUS10: Registrar Bitácora Pedagógica de Sesión

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS10: Registrar Bitácora Pedagógica de Sesión\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam actor {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #10B981
}

actor "Estudiante Mentor" as ActMentor
boundary "UI Formulario Bitácora\n(SPA React)" as B_BitacoraUI
control "Controlador de\nBitácora Pedagógica" as C_Bitacora
control "Validador de Plazo\n(Ventana 24h RN-07)" as C_Plazo
control "Sincronizador de\nAsistencia (RN-11)" as C_Asist
control "Calculador de Horas\nFormativas (RN-12)" as C_Horas
entity "SesionMentoria" as E_Sesion
entity "BitacoraSesion" as E_Bitacora
entity "ReservaCupo" as E_Reserva
entity "BolsaHorasMentor" as E_Bolsa
entity "RegistroAuditoria" as E_Audit

ActMentor --> B_BitacoraUI : 1. Solicita formulario de cierre de sesión
B_BitacoraUI --> C_Bitacora : 1.1. cargarContextoSesion(idSesion)
C_Bitacora ..> E_Sesion : 1.2. consultarEstadoYHorarios(idSesion)
C_Bitacora ..> E_Reserva : 1.3. listarAsistentesConfirmados(idSesion)
C_Bitacora --> B_BitacoraUI : 1.4. retornarDatosSesionYAlumnos()
B_BitacoraUI --> ActMentor : 2. Despliega lista de alumnos y campos estructurados

ActMentor --> B_BitacoraUI : 3. Completa temas (>=30 caracteres), dificultades, acuerdos y envía
B_BitacoraUI --> C_Bitacora : 3.1. registrarBitacora(dtoBitacora)

C_Bitacora --> C_Plazo : 3.2. verificarPlazoVigente(fechaFin, ahora) [RN-07: <= 24 horas]

alt Plazo extemporáneo (> 24 horas tras fin de sesión)
    C_Plazo --> C_Bitacora : 3.3. plazoVencidoError()
    C_Bitacora --> B_BitacoraUI : 3.4. notificarPlazoVencido("Plazo de 24h expirado. Requiere regularización")
    B_BitacoraUI --> ActMentor : 4. Alerta de bloqueo por extemporaneidad
else Plazo conforme (dentro de las 24 horas)
    C_Bitacora --> C_Asist : 3.5. regularizarInasistencias(idSesion) [RN-11]
    C_Asist --> E_Reserva : 3.6. mutarNoMarcados(INASISTENCIA)
    
    C_Bitacora --> E_Bitacora : 3.7. crear(idSesion, temas, dificultades, observaciones, 'REGISTRADA')
    C_Bitacora --> E_Sesion : 3.8. mutarEstado(FINALIZADA)
    
    C_Bitacora --> C_Horas : 3.9. acumularHorasDictadas(idMentor, horas) [RN-12]
    C_Horas --> E_Bolsa : 3.10. incrementarHorasPendientesVisado(horas)
    
    C_Bitacora --> E_Audit : 3.11. registrarEventoAuditoria('REGISTRO_BITACORA', idSesion)
    C_Bitacora --> B_BitacoraUI : 3.12. confirmarRegistroExitoso()
    B_BitacoraUI --> ActMentor : 5. Notificación de cierre formal y horas acumuladas
end
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS10 delimita la orquestación del cierre formativo y administrativo de cada sesión. `ControladorBitacora` interactúa primeramente con `ValidadorPlazo` para garantizar la observancia de la regla RN-07, impidiendo la captura desfasada de información pedagógica si han transcurrido más de 24 horas desde la culminación del evento. La clase de control `SincronizadorAsistencia` ejecuta la transición de las reservas pendientes hacia el estado canónico `INASISTENCIA` conforme a RN-11, mientras que `CalculadorHoras` computa las horas efectivas dictadas y actualiza la entidad `BolsaHorasMentor` en concordancia estricta con RN-12, dejando la sesión en estado `FINALIZADA` e inmutable ante ulteriores ediciones.

### 6.3.1.10. CUS05 - Análisis de Objetos: Responder Encuesta de Calidad Post-Mentoría

El análisis de objetos modela los componentes lógicos participantes en la captura de la retroalimentación formativa y en la gobernanza de la reputación académica. Se representan el actor *Estudiante Mentoreado*, la frontera *UI Encuesta Calidad*, los controladores de negocio *Controlador de Encuestas de Calidad*, *Validador de Elegibilidad y Plazo*, *Motor de Anonimización (Ley N° 29733)* y *Calculador de Reputación (RN-13)*, junto a las entidades *ReservaCupo*, *SesionMentoria*, *BitacoraSesion*, *EncuestaSatisfaccion*, *ReputacionMentor* y *RegistroAuditoria*.

#### Diagrama 6.13.10: Análisis de Objetos (Modelo ECB) - CUS05: Responder Encuesta de Calidad Post-Mentoría

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS05: Responder Encuesta de Calidad Post-Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam actor {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #10B981
}

actor "Estudiante Mentoreado" as ActMentee
boundary "UI Encuesta Calidad\n(SPA React)" as B_EncuestaUI
control "Controlador de\nEncuestas de Calidad" as C_Encuesta
control "Validador de Elegibilidad\ny Plazo (Ventana 24h)" as C_Validador
control "Motor de Anonimización\n(Ley N° 29733)" as C_Anon
control "Calculador de Reputación\n(Media Ponderada RN-13)" as C_Reputacion
entity "ReservaCupo" as E_Reserva
entity "SesionMentoria" as E_Sesion
entity "BitacoraSesion" as E_Bitacora
entity "EncuestaSatisfaccion" as E_Encuesta
entity "ReputacionMentor" as E_Reputacion
entity "RegistroAuditoria" as E_Audit

ActMentee --> B_EncuestaUI : 1. Accede a encuesta de sesión asistida
B_EncuestaUI --> C_Encuesta : 1.1. cargarFormularioEncuesta(idSesion, idUsuario)
C_Encuesta --> C_Validador : 1.2. validarAptitudEvaluacion(idSesion, idUsuario)
C_Validador ..> E_Reserva : 1.3. verificarEstado(ASISTIDA) y flag(no_evaluada)
C_Validador ..> E_Bitacora : 1.4. consultarFechaCierreBitacora()

alt Reserva no asistida o ya evaluada (E02)
    C_Validador --> C_Encuesta : 1.5. denegarAcceso("Solo asistentes confirmados pueden evaluar")
    C_Encuesta --> B_EncuestaUI : 1.6. notificarInadmisibilidad()
    B_EncuestaUI --> ActMentee : 2. Mensaje de error de acceso
else Plazo de 24 horas expirado (E01)
    C_Validador --> C_Encuesta : 1.7. denegarAcceso("Ventana de 24h vencida")
    C_Encuesta --> B_EncuestaUI : 1.8. notificarExpiracion()
    B_EncuestaUI --> ActMentee : 2. Mensaje de encuesta caducada
else Elegible y dentro de plazo legal
    C_Encuesta --> B_EncuestaUI : 1.9. renderizarReactivosLikert(contextoSesion)
    B_EncuestaUI --> ActMentee : 3. Despliega 4 reactivos (1-5 estrellas) y caja de comentarios

    ActMentee --> B_EncuestaUI : 4. Califica dimensiones, ingresa sugerencia opcional y envía
    B_EncuestaUI --> C_Encuesta : 4.1. registrarEvaluacion(dtoEncuesta)
    
    C_Encuesta --> C_Anon : 4.2. disociarIdentidadEstudiante(idUsuario, comentario)
    C_Anon --> E_Encuesta : 4.3. instanciarEncuesta(idSesion, scoresLikert, hashAnonimo, comentarioFiltrado)
    
    C_Encuesta --> E_Reserva : 4.4. marcarEncuestaCompletada(idReserva)
    
    C_Encuesta --> C_Reputacion : 4.5. recalcularScoreMentor(idMentor, scoresLikert) [RN-13]
    C_Reputacion --> E_Reputacion : 4.6. actualizarMediaPonderadaYTotal()
    
    C_Encuesta --> E_Audit : 4.7. registrarEventoAuditoria('ENCUESTA_REGISTRADA', idSesion)
    C_Encuesta --> B_EncuestaUI : 4.8. confirmarRecepcion()
    B_EncuestaUI --> ActMentee : 5. Banner de agradecimiento y confirmación
end
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS05 formaliza el proceso de evaluación de calidad asegurando el anonimato del mentoreado y la legitimidad de las valoraciones. La clase de control `ValidadorElegibilidad` filtra estrictamente que solo aquellos estudiantes cuya reserva transicionó a `ASISTIDA` y que se encuentren dentro de la ventana de 24 horas posteriores al cierre de bitácora puedan emitir opinión. `MotorAnonimizacion` disocia los datos personales del alumno antes de instanciar `EncuestaSatisfaccion` en cumplimiento de la Ley N° 29733, mientras que `CalculadorReputacion` procesa las cuatro dimensiones Likert actualizando de forma ponderada la entidad `ReputacionMentor` conforme a la regla de negocio RN-13.

### 6.3.1.11. CUS19 - Análisis de Objetos: Consultar Historial de Sesiones y Asistencia

El análisis de objetos modela la estructura lógica orientada a la provisión de información histórica y rendición de cuentas académica para estudiantes y mentores. Se especifican el actor *Usuario Institucional*, las fronteras *UI Tablero Historial* y *Panel Lateral Detalle (Drawer)*, las clases de control *Controlador de Historial Pedagógico*, *Validador de Contexto y RLS* y *Motor de Filtrado y Métricas Agregadas*, en vinculación directa con las entidades de persistencia *SesionMentoria*, *ReservaCupo*, *BitacoraSesion*, *BolsaHorasMentor* y *Asignatura*.

#### Diagrama 6.13.11: Análisis de Objetos (Modelo ECB) - CUS19: Consultar Historial de Sesiones y Asistencia

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS19: Consultar Historial de Sesiones y Asistencia\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam actor {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
}
skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}
skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}
skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #10B981
}

actor "Usuario Institucional\n(Mentor / Mentoreado)" as ActUser
boundary "UI Tablero Historial\n(SPA React)" as B_HistorialUI
boundary "Panel Lateral Detalle\n(Drawer Bitácora)" as B_DrawerUI
control "Controlador de Historial\nPedagógico" as C_Historial
control "Validador de Contexto\ny RLS (Supabase)" as C_RLS
control "Motor de Filtrado y\nMétricas Agregadas" as C_Filtro
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "BitacoraSesion" as E_Bitacora
entity "BolsaHorasMentor" as E_Bolsa
entity "Asignatura" as E_Asignatura

ActUser --> B_HistorialUI : 1. Solicita historial académico consolidado
B_HistorialUI --> C_Historial : 1.1. obtenerHistorialUsuario(filtros, idUsuarioAuth)
C_Historial --> C_RLS : 1.2. verificarAislamientoFilas(idUsuarioAuth)

C_RLS ..> E_Reserva : 1.3. consultarReservasPorUsuario(idUsuarioAuth)
C_RLS ..> E_Sesion : 1.4. consultarSesionesDictadasPorMentor(idUsuarioAuth)
C_Historial ..> E_Asignatura : 1.5. resolverNombresYCodigos()

C_Historial --> C_Filtro : 1.6. procesarMetricasYFiltros(semestre, materia)
C_Filtro --> B_HistorialUI : 1.7. renderizarTablaHistorial(resumenMétricas, listaItems)

alt Historial sin participaciones registradas (E01)
    B_HistorialUI --> ActUser : 2. Despliega estado vacío ("Sin registros de mentoría")
else Historial con eventos encontrados
    B_HistorialUI --> ActUser : 3. Despliega tabla con sesiones, roles, asistencias y métricas
    
    ActUser --> B_HistorialUI : 4. Clic en fila para inspeccionar detalle de bitácora
    B_HistorialUI --> C_Historial : 4.1. obtenerDetalleSesion(idSesion)
    C_Historial ..> E_Bitacora : 4.2. recuperarBitacora(idSesion)
    C_Historial ..> E_Bolsa : 4.3. recuperarHorasAcreditadas(idMentor)
    C_Historial --> B_DrawerUI : 4.4. cargarDetalleBitacoraYRecursos()
    B_DrawerUI --> ActUser : 5. Visualiza temas tratados, acuerdos y recursos compartidos
end
@enduml
```

Fuente: Elaboración propia.

El análisis ECB para CUS19 estructura un acceso seguro y unificado a la trayectoria formativa de los miembros de la comunidad universitaria. `ControladorHistorial` articula con `ValidadorContextoRLS` la aplicación imperativa de directivas de seguridad en la base de datos (PostgreSQL RLS), garantizando que ningún usuario acceda a asistencias de terceros ajenos a su esfera. La clase de control `MotorFiltradoMetricas` agiliza la agregación estadística (tasa de asistencia efectiva y horas dictadas), permitiendo que `UI Tablero Historial` presente un resumen cuantitativo fidedigno y despliegue el contenido temático de la bitácora docente sin fisuras de privacidad.

### 6.3.1.12. CUS16 - Análisis de Objetos: Consultar Tablero de Insignias y Reputación

El análisis de objetos para `CUS16` modela la arquitectura lógica requerida para la cuantificación del prestigio pedagógico y la gamificación formativa en la EPIS-UPT. Se delimitan los actores *Mentor Académico* (beneficiario y consultor principal) y *Mentoreado* (consumidor de la reputación pública), las interfaces *UI Tablero Reputación e Insignias* y *UI Perfil Público Mentor*, los controladores *Controlador de Gamificación*, *Motor de Reputación Ponderada* y *Motor de Reglas de Insignias*, vinculados a las entidades *ReputacionMentor*, *Insignia*, *InsigniaOtorgada*, *EncuestaSatisfaccion*, *BitacoraSesion* y *SesionMentoria*.

#### Diagrama 6.13.12: Análisis de Objetos (Modelo ECB) - CUS16: Consultar Tablero de Insignias y Reputación

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS16: Consultar Tablero de Insignias y Reputación\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Mentor Académico\n(Usuario Autenticado)" as ActMentor
actor "Mentoreado\n(Estudiante Consultor)" as ActEstudiante

boundary "UI Tablero Reputación\ne Insignias (Privado)" as B_TableroUI
boundary "UI Perfil Público\nMentor (Resumido)" as B_PerfilPublicoUI

control "Controlador de\nGamificación y Reputación" as C_Gamificacion
control "Motor de Reputación\nPonderada (RN-13)" as C_MotorReputacion
control "Motor de Reglas\nde Insignias" as C_MotorInsignias

entity "ReputacionMentor" as E_Reputacion
entity "Insignia" as E_Insignia
entity "InsigniaOtorgada" as E_InsigniaOtorgada
entity "EncuestaSatisfaccion" as E_Encuesta
entity "BitacoraSesion" as E_Bitacora
entity "SesionMentoria" as E_Sesion

' Relaciones para flujo privado del Mentor
ActMentor --> B_TableroUI : 1. Accede a "Mi Reputación & Reconocimientos"
B_TableroUI --> C_Gamificacion : 1.1. obtenerTableroMentor(idMentor)
C_Gamificacion --> C_MotorReputacion : 1.2. calcularScoreCompuesto(idMentor)

C_MotorReputacion ..> E_Encuesta : 1.2.1. leerPromediosLikert(idMentor)
C_MotorReputacion ..> E_Sesion : 1.2.2. calcularTasaCumplimiento(idMentor)
C_MotorReputacion ..> E_Bitacora : 1.2.3. calcularPuntualidadEntrega(idMentor)
C_MotorReputacion --> E_Reputacion : 1.2.4. sincronizarReputacion(score, nivel)

C_Gamificacion --> C_MotorInsignias : 1.3. evaluarDesbloqueoInsignias(idMentor)
C_MotorInsignias ..> E_Insignia : 1.3.1. consultarCatalogoVigente()
C_MotorInsignias ..> E_InsigniaOtorgada : 1.3.2. consultarInsigniasPoseidas(idMentor)
C_MotorInsignias --> E_InsigniaOtorgada : 1.3.3. registrarNuevaInsignia(idMentor, idInsignia)

C_Gamificacion --> B_TableroUI : 1.4. consolidarTableroCompleto(score, insignias, progreso, comentarios)
B_TableroUI --> ActMentor : 2. Despliega velocímetro, badges, barras de progreso y comentarios

' Relaciones para flujo público de consulta por Mentoreado
ActEstudiante --> B_PerfilPublicoUI : 3. Visualiza perfil del mentor al reservar
B_PerfilPublicoUI --> C_Gamificacion : 3.1. obtenerResumenPublico(idMentor)
C_Gamificacion ..> E_Reputacion : 3.2. leerScoreYNivelPublico(idMentor)
C_Gamificacion ..> E_InsigniaOtorgada : 3.3. leerInsigniasPublicas(idMentor)
C_Gamificacion --> B_PerfilPublicoUI : 3.4. entregarResumenSanitizado()
B_PerfilPublicoUI --> ActEstudiante : 4. Presenta estrellas, nivel y medallas destacadas
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS16 implementa una arquitectura modular que separa el cómputo analítico privado de la proyección pública de reputación. `ControladorGamificacion` articula dos motores especializados: `MotorReputacionPonderada`, que sintetiza la ecuación estipulada en la regla de negocio RN-13 ($70\%$ de satisfacción en encuestas, $20\%$ de cumplimiento de sesiones convocadas y $10\%$ de puntualidad en bitácoras $\le 24\text{ h}$), y `MotorReglasInsignias`, encargado de auditar de forma determinística los umbrales de desbloqueo normativos. Las entidades persistentes salvaguardan la trazabilidad histórica de los reconocimientos, garantizando que la interfaz renderice proyecciones lúdicas de alto rendimiento sin comprometer la privacidad docente ni los datos sensibles de los estudiantes evaluadores.

### 6.3.1.13. CUS13 - Análisis de Objetos: Parametrizar y Emitir Certificados

El análisis de objetos para `CUS13` formaliza la arquitectura lógica del proceso de acreditación académica y fe pública digital en la EPIS-UPT. Modela la interacción entre el actor *Administrador Institucional*, las fronteras *UI Parametrización y Emisión de Certificados* y *UI Modal Confirmación Batch*, las clases de control *Controlador de Certificación*, *Motor de Elegibilidad Normativa (RN-14)*, *Generador Criptográfico PDF/A y QR* y *Servicio de Notificación SMTP*, en relación con las entidades *ParametroCertificacion*, *Certificado*, *BitacoraSesion*, *BolsaHorasMentor* y *Usuario*.

#### Diagrama 6.13.13: Análisis de Objetos (Modelo ECB) - CUS13: Parametrizar y Emitir Certificados

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS13: Parametrizar y Emitir Certificados\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Administrador Institucional\n(Comité de Tutoría / Dirección)" as ActAdmin

boundary "UI Parametrización y\nEmisión de Certificados" as B_CertUI
boundary "UI Modal Confirmación\nBatch Institucional" as B_ModalUI

control "Controlador de\nCertificación Institucional" as C_Certificacion
control "Motor de Elegibilidad\nNormativa (RN-14)" as C_MotorElegibilidad
control "Generador Criptográfico\nPDF/A y Código QR" as C_GeneradorPDF
control "Servicio de Notificación\nSMTP Institucional" as C_Notificador

entity "ParametroCertificacion" as E_Parametro
entity "Certificado" as E_Certificado
entity "BitacoraSesion" as E_Bitacora
entity "BolsaHorasMentor" as E_Bolsa
entity "Usuario" as E_Usuario

' Flujo de Parametrización y Consulta de Elegibles
ActAdmin --> B_CertUI : 1. Configura umbrales (Semestre, horas mínimas, score mínimo)
B_CertUI --> C_Certificacion : 1.1. registrarParametros(dto)
C_Certificacion --> E_Parametro : 1.2. guardarParametrizacion(semestre, horasMin, scoreMin)

ActAdmin --> B_CertUI : 2. Clic en "Consultar Mentores Elegibles"
B_CertUI --> C_Certificacion : 2.1. obtenerCandidatosCertificacion(idParametro)
C_Certificacion --> C_MotorElegibilidad : 2.2. auditarPadrónMentores(idParametro)

C_MotorElegibilidad ..> E_Bitacora : 2.2.1. verificarHorasVisadas(idMentor, 'VISADA')
C_MotorElegibilidad ..> E_Bolsa : 2.2.2. validarSaldoHoras(idMentor)
C_MotorElegibilidad ..> E_Usuario : 2.2.3. constatarVigenciaAcademica(idMentor)
C_MotorElegibilidad --> C_Certificacion : 2.3. entregarNominaElegibles(candidatos)
C_Certificacion --> B_CertUI : 2.4. renderizarGrillaElegibles(candidatos)
B_CertUI --> ActAdmin : 3. Visualiza padrón con checkboxes de selección

' Flujo de Emisión Batch y Sellado Criptográfico
ActAdmin --> B_CertUI : 4. Selecciona mentores y presiona "Proceder a la Emisión"
B_CertUI --> B_ModalUI : 4.1. abrirModalConfirmacion(totalSeleccionados)
ActAdmin --> B_ModalUI : 5. Confirma emisión institucional definitiva

B_ModalUI --> C_Certificacion : 5.1. ejecutarEmisionLote(listaMentoresIds, idParametro)
loop Para cada mentor aprobado
    C_Certificacion --> C_GeneradorPDF : 5.2. generarDocumentoOficial(idMentor, horas, correlativo)
    C_GeneradorPDF --> C_GeneradorPDF : 5.2.1. calcularHashSHA256(bytesPDF)
    C_GeneradorPDF --> C_GeneradorPDF : 5.2.2. estamparCodigoQRVerificacion(urlPublica)
    C_GeneradorPDF --> E_Certificado : 5.2.3. persistirCertificado(hash, correlativo, 'EMITIDO')
    C_GeneradorPDF --> E_Bolsa : 5.2.4. marcarHorasComoCertificadas(horas)
    
    C_Certificacion --> C_Notificador : 5.3. despacharAvisoCertificado(correoInstitucional, idCertificado)
end

C_Certificacion --> B_CertUI : 6. notificarResultadoBatch(exitosos, errores)
B_CertUI --> ActAdmin : 7. Despliega confirmación final de emisión institucional
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS13 modela la cadena transaccional y de fe pública requerida para la acreditación oficial de horas de mentoría. `ControladorCertificacion` delega en `MotorElegibilidadNormativa` el filtrado determinístico basado en la regla RN-14 (umbral mínimo de horas en bitácoras visadas y ausencia de observaciones éticas). La clase de control `GeneradorCriptograficoPDFA` ejecuta de forma aislada la conformación del documento PDF/A inalterable, el cómputo del hash SHA-256 y la inyección del código QR para verificación externa. La entidad `Certificado` almacena los metadatos de integridad sin redundancia, garantizando que las constancias emitidas sean legalmente auditables ante la Dirección de Escuela y la Secretaría Académica de la EPIS-UPT.

### 6.3.1.14. CUS09 - Análisis de Objetos: Descargar Certificado de Horas de Mentoría

El análisis de objetos para `CUS09` delimita la estructura de componentes requerida para la visualización, descarga segura y validación abierta de constancias institucionales en la EPIS-UPT. Se modelan los actores *Mentor Académico* y *Tercero Verificador*, las interfaces *UI Mis Certificados Oficiales* y *UI Portal Público de Verificación*, los controladores *Controlador de Descarga y Verificación*, *Validador Criptográfico Hash SHA-256*, *Gestor de Almacenamiento Seguro (Bucket)* y *Servicio de Correo*, en vinculación directa con las entidades *Certificado*, *Usuario* y *RegistroAuditoriaVerificacion*.

#### Diagrama 6.13.14: Análisis de Objetos (Modelo ECB) - CUS09: Descargar Certificado de Horas de Mentoría

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS09: Descargar Certificado de Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Mentor Académico\n(Usuario Autenticado)" as ActMentor
actor "Tercero Verificador\n(Empleador / Secretaría vía QR)" as ActVerificador

boundary "UI Mis Certificados\nOficiales (Privado)" as B_MisCertificadosUI
boundary "UI Portal Público de\nVerificación (Abierto)" as B_PortalPublicoUI

control "Controlador de Descarga\ny Verificación" as C_DescargaVerif
control "Validador Criptográfico\nHash SHA-256" as C_ValidadorHash
control "Gestor de Almacenamiento\nSeguro (Bucket Storage)" as C_Storage
control "Servicio de Correo\nInstitucional (SMTP)" as C_Correo

entity "Certificado" as E_Certificado
entity "Usuario" as E_Usuario
entity "RegistroAuditoriaVerificacion" as E_Auditoria

' Flujo de Consulta y Descarga Privada del Mentor
ActMentor --> B_MisCertificadosUI : 1. Accede a "Mis Certificados"
B_MisCertificadosUI --> C_DescargaVerif : 1.1. listarCertificadosUsuario(idMentor)
C_DescargaVerif ..> E_Certificado : 1.2. buscarPorMentor(idMentor)
C_DescargaVerif --> B_MisCertificadosUI : 1.3. entregarListadoEmitidos(certificados)
B_MisCertificadosUI --> ActMentor : 2. Despliega cards de certificados con previsualización

ActMentor --> B_MisCertificadosUI : 3. Presiona "Descargar Certificado Oficial en PDF"
B_MisCertificadosUI --> C_DescargaVerif : 3.1. solicitarStreamPDF(idCertificado)
C_DescargaVerif ..> E_Certificado : 3.2. obtenerRutaYHash(idCertificado)
C_DescargaVerif --> C_Storage : 3.3. recuperarBinarioPDF(rutaStorage)
C_Storage --> C_ValidadorHash : 3.4. verificarChecksumIntegridad(bytesPDF, hashEsperado)
C_ValidadorHash --> C_DescargaVerif : 3.5. confirmacionIntegridadValida()
C_DescargaVerif --> B_MisCertificadosUI : 3.6. transmitirArchivoAdjunto(stream, headersSeguridad)
B_MisCertificadosUI --> ActMentor : 4. Descarga documento oficial inalterable en el dispositivo

' Flujo Alterno FA01: Verificación Pública por Tercero Verificador
ActVerificador --> B_PortalPublicoUI : 5. Escanea código QR del certificado
B_PortalPublicoUI --> C_DescargaVerif : 5.1. verificarPorHash(hashSha256)
C_DescargaVerif ..> E_Certificado : 5.2. consultarPorHash(hashSha256)
C_DescargaVerif ..> E_Usuario : 5.3. consultarDatosMentor(idMentor)
C_DescargaVerif --> E_Auditoria : 5.4. registrarConsultaVerificacion(ip, fecha, hash)
C_DescargaVerif --> B_PortalPublicoUI : 5.5. presentarFichaValidacion(correlativo, horas, estado, mentor)
B_PortalPublicoUI --> ActVerificador : 6. Visualiza sello verde de autenticidad institucional UPT
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS09 establece una estricta separación de responsabilidades entre el acceso privado del mentor y la verificación abierta de fe pública. `ControladorDescargaVerif` orquesta con `ValidadorCriptograficoHash` la verificación obligatoria del *checksum* SHA-256 antes de transmitir el flujo binario desde `Bucket Storage`, impidiendo cualquier alteración documental o distribución de archivos corruptos (RNF09). Paralelamente, la frontera pública `PortalPublicoVerificacion` atiende las consultas generadas por el escaneo de códigos QR sin requerir inicio de sesión, auditando cada verificación en `RegistroAuditoriaVerificacion` y proyectando fe pública digital con validez institucional.

### 6.3.1.15. CUS22 - Análisis de Objetos: Auditar Bitácoras, Asistencia y Horas de Mentoría

El análisis de objetos para `CUS22` modela la arquitectura de fiscalización académica y control de calidad formativa a cargo del Comité de Tutoría de la EPIS-UPT. Se especifican los actores *Administrador Institucional* (auditor) y *Mentor Académico* (fiscalizado), las interfaces *UI Bandeja Auditoría Bitácoras*, *UI Expediente Auditoría Sesión* y *UI Modal Observación Bitácora*, las clases de control *Controlador de Auditoría Docente*, *Motor de Fiscalización Académica (RN-12, RN-14)* y *Servicio de Notificación SMTP*, en interacción directa con las entidades *BitacoraSesion*, *SesionMentoria*, *ReservaCupo*, *BolsaHorasMentor*, *ObservacionBitacora* y *RegistroAuditoriaAdmin*.

#### Diagrama 6.13.15: Análisis de Objetos (Modelo ECB) - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Administrador Institucional\n(Comité de Tutoría / Auditor)" as ActAdmin
actor "Mentor Académico\n(Usuario Fiscalizado)" as ActMentor

boundary "UI Bandeja Auditoría\nBitácoras Pendientes" as B_BandejaUI
boundary "UI Expediente Auditoría\nSesión y Asistencia" as B_ExpedienteUI
boundary "UI Modal Observación\ny Pliego de Cargos" as B_ModalObsUI

control "Controlador de\nAuditoría Docente" as C_Auditoria
control "Motor de Fiscalización\nAcadémica (RN-12/14)" as C_MotorFiscalizacion
control "Servicio de Notificación\nSMTP Institucional" as C_Notificador

entity "BitacoraSesion" as E_Bitacora
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "BolsaHorasMentor" as E_Bolsa
entity "ObservacionBitacora" as E_Observacion
entity "RegistroAuditoriaAdmin" as E_AuditoriaLog

' Flujo de Consulta de Bandeja de Pendientes
ActAdmin --> B_BandejaUI : 1. Accede a "Auditoría de Bitácoras Pendientes"
B_BandejaUI --> C_Auditoria : 1.1. listarSesionesPendientesVisado()
C_Auditoria --> C_MotorFiscalizacion : 1.2. recuperarBandejaAuditoria()
C_MotorFiscalizacion ..> E_Bitacora : 1.2.1. filtrarPorEstado('REGISTRADA')
C_MotorFiscalizacion ..> E_Sesion : 1.2.2. unirDatosSesionYMentor()
C_MotorFiscalizacion --> C_Auditoria : 1.3. entregarBandejaPendientes(lista)
C_Auditoria --> B_BandejaUI : 1.4. renderizarGrillaPendientes(lista)
B_BandejaUI --> ActAdmin : 2. Despliega sesiones finalizadas ordenadas cronológicamente

' Flujo de Examen del Expediente
ActAdmin --> B_BandejaUI : 3. Selecciona una sesión para auditar
B_BandejaUI --> B_ExpedienteUI : 3.1. abrirExpediente(idSesion)
B_ExpedienteUI --> C_Auditoria : 3.2. obtenerExpedienteDetallado(idSesion)
C_Auditoria ..> E_Bitacora : 3.2.1. leerContenidoPedagogico(idSesion)
C_Auditoria ..> E_Reserva : 3.2.2. listarAsistenciasNominales(idSesion)
C_Auditoria --> B_ExpedienteUI : 3.3. presentarExpedienteCompleto(expediente)
B_ExpedienteUI --> ActAdmin : 4. Examina temas, dificultades, nómina de alumnos y recursos

' Subflujo A: Visado y Aprobación Oficial de Horas
ActAdmin --> B_ExpedienteUI : 5a. Presiona "Visar y Aprobar Horas"
B_ExpedienteUI --> C_Auditoria : 5a.1. visarSesion(idBitacora, idAuditor)
C_Auditoria --> E_Bitacora : 5a.2. mutarEstado('VISADA')
C_Auditoria --> E_Bolsa : 5a.3. consolidarHorasOficiales(idMentor, horas)
C_Auditoria --> E_AuditoriaLog : 5a.4. registrarDictamen('VISADO_APROBADO', idAuditor)
C_Auditoria --> B_ExpedienteUI : 5a.5. confirmarVisadoExitoso()
B_ExpedienteUI --> ActAdmin : 6a. Muestra distintivo verde de aprobación oficial

' Subflujo B: Observación Formal por Inconsistencias (FA01)
ActAdmin --> B_ExpedienteUI : 5b. Presiona "Observar Bitácora"
B_ExpedienteUI --> B_ModalObsUI : 5b.1. abrirModalPliegoCargos()
ActAdmin --> B_ModalObsUI : 5b.2. Redacta observaciones y confirma plazo 48h
B_ModalObsUI --> C_Auditoria : 5b.3. emitirObservacion(idBitacora, pliego, plazo)
C_Auditoria --> E_Bitacora : 5b.4. mutarEstado('OBSERVADA')
C_Auditoria --> E_Observacion : 5b.5. registrarPliegoObservacion(pliego, 48h)
C_Auditoria --> E_AuditoriaLog : 5b.6. registrarDictamen('OBSERVACION_EMITIDA', idAuditor)
C_Auditoria --> C_Notificador : 5b.7. despacharAlertaSubsanacion(correoMentor, pliego)
C_Notificador --> ActMentor : 5b.8. Notificación urgente con plazo de 48 horas
C_Auditoria --> B_ExpedienteUI : 5b.9. actualizarVistaObservada()
B_ExpedienteUI --> ActAdmin : 6b. Confirma pase a pliego de observaciones
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS22 formaliza el control institucional de la labor docente entre pares. `ControladorAuditoriaDocente` actúa como barrera evaluadora antes de que las horas declaradas por el mentor adquieran validez jurídica en `BolsaHorasMentor`. La bifurcación de control segrega el visado regular (`VISADA`), que consolida las horas para la certificación semestral (RN-14), de la emisión formal de pliegos de cargo (`OBSERVADA`), la cual congela transaccionalmente los créditos docentes y activa el protocolo de subsanación dentro de una ventana máxima de 48 horas mediante `ServicioNotificacionSMTP`, resguardando la calidad formativa de la EPIS-UPT.

### 6.3.1.16. CUS12 - Análisis de Objetos: Destacar Mentorías Prioritarias

El análisis de objetos para `CUS12` modela la arquitectura de priorización académica institucional orientada a reforzar asignaturas críticas con alta tasa de reprobación o deserción curricular, en cumplimiento estricto del requerimiento funcional `RF24` y la regla de negocio `RN-11`. Se especifican los actores *Administrador Institucional* (Dirección EPIS / Comité de Tutoría) y *Estudiante Mentoreado* (destinatario del estímulo), las interfaces *UI Gestión de Prioridades Académicas*, *UI Modal Campaña de Refuerzo Curricular* y *UI Catálogo Público de Mentorías*, las clases de control *Controlador de Políticas de Priorización Curricular*, *Motor Algorítmico de Recomendación (RN-11)* y *Gestor de Invalidación y Caché (Redis)*, junto con las entidades *PoliticaPrioridadCurricular*, *Asignatura*, *TemaSilabico*, *OfertaMentoria* y *RegistroAuditoriaAdmin*.

#### Diagrama 6.13.16: Análisis de Objetos (Modelo ECB) - CUS12: Destacar Mentorías Prioritarias

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS12: Destacar Mentorías Prioritarias\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Administrador Institucional\n(Comité de Tutoría / Dirección)" as ActAdmin
actor "Estudiante Mentoreado\n(Consumidor del Catálogo)" as ActMentoreado

boundary "UI Gestión de Prioridades\nAcadémicas" as B_PrioridadesUI
boundary "UI Modal Campaña de\nRefuerzo Curricular" as B_ModalCampanaUI
boundary "UI Catálogo Público\nde Mentorías" as B_CatalogoUI

control "Controlador de Políticas\nde Priorización Curricular" as C_Politicas
control "Motor Algorítmico de\nRecomendación (RN-11)" as C_MotorRecomendador
control "Gestor de Invalidación\ny Caché (Redis)" as C_CacheManager

entity "PoliticaPrioridadCurricular" as E_Politica
entity "Asignatura" as E_Asignatura
entity "TemaSilabico" as E_Tema
entity "OfertaMentoria" as E_Oferta
entity "RegistroAuditoriaAdmin" as E_AuditoriaLog

' 1. Consulta de estadísticas y asignaturas
ActAdmin --> B_PrioridadesUI : 1. Accede a "Gestión de Prioridades Académicas"
B_PrioridadesUI --> C_Politicas : 1.1. listarAsignaturasConEstadisticas()
C_Politicas ..> E_Asignatura : 1.2. consultarCatalogo()
C_Politicas ..> E_Politica : 1.3. obtenerPoliticasActivas()
C_Politicas --> B_PrioridadesUI : 1.4. presentarGrillaRendimiento(lista)
B_PrioridadesUI --> ActAdmin : 2. Visualiza asignaturas con tasas de reprobación y estado prioritario

' 2. Configuración y activación de campaña prioritaria
ActAdmin --> B_PrioridadesUI : 3. Selecciona asignatura crítica (ej. Cálculo II)
B_PrioridadesUI --> B_ModalCampanaUI : 3.1. abrirModalConfiguracion(idAsignatura)
ActAdmin --> B_ModalCampanaUI : 4. Ingresa fechas de vigencia, factor alfa (1.25) y resolución
B_ModalCampanaUI --> C_Politicas : 4.1. activarPoliticaPrioridad(idAsignatura, vigencia, alfa=1.25, resolucion)
C_Politicas --> E_Politica : 4.2. crearOModificarPolitica('ACTIVA', alfa, vigencia)
C_Politicas --> E_Asignatura : 4.3. mutarIndicadorPrioritario(TRUE)
C_Politicas --> E_AuditoriaLog : 4.4. registrarAccionResolutiva('ACTIVACION_PRIORIDAD', idAdmin)
C_Politicas --> C_CacheManager : 4.5. purgarCacheRecomendaciones()
C_CacheManager ..> C_MotorRecomendador : 4.6. invalidarScoresPrecalculados()
C_Politicas --> B_ModalCampanaUI : 4.7. confirmarActivacionExitosa()
B_ModalCampanaUI --> ActAdmin : 5. Notifica activación formal de la campaña institucional

' 3. Reflejo algorítmico y visual para mentoreados
ActMentoreado --> B_CatalogoUI : 6. Consulta catálogo o feed de recomendaciones Top-k
B_CatalogoUI --> C_MotorRecomendador : 6.1. obtenerRecomendacionesTopK(idEstudiante)
C_MotorRecomendador ..> E_Politica : 6.2. leerFactorBonificacionAlfa(1.25)
C_MotorRecomendador ..> E_Oferta : 6.3. bonificarScoresOfertasPrioritarias(alfa)
C_MotorRecomendador --> B_CatalogoUI : 6.4. entregarRankingConBadgeDorado()
B_CatalogoUI --> ActMentoreado : 7. Despliega ofertas con distintivo dorado "Prioridad Institucional EPIS"
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS12 formaliza la convergencia entre la gestión directiva institucional y la optimización del aprendizaje asistido por algoritmos. A través de `ControladorPoliticasPriorizacionCurricular`, la Dirección de Escuela y el Comité de Tutoría canalizan intervenciones focalizadas en cursos neurálgicos, modificando los parámetros operativos de `PoliticaPrioridadCurricular`. El motor `MotorAlgoritmicoRecomendacion` consume el coeficiente multiplicador $\alpha$ estipulado en `RN-11`, logrando que las asignaturas críticas alcancen mayor notoriedad tanto en el ranking personalizado de los estudiantes vulnerables como en la interfaz visual con distintivo de fe pública institucional.

### 6.3.1.17. CUS14 - Análisis de Objetos: Visualizar Tablero de Analíticas Institucionales

El análisis de objetos para `CUS14` modela la arquitectura analítica orientada a la inteligencia institucional y gobernanza académica en la EPIS-UPT, en conformidad con el requerimiento funcional `RF25` y la regla de negocio `RN-13` (protección de datos bajo la Ley N° 29733). Se especifican los actores *Administrador Institucional* (Dirección EPIS / Comité de Tutoría) y *Docente Investigador* (analista curricular), las interfaces *UI Tablero Ejecutivo Analítica Institucional* y *UI Modal Filtros y Exportación*, las clases de control *Controlador de Analítica Institucional*, *Motor de Agregación OLAP y Métricas*, *Servicio de Anonimización y Privacidad* y *Generador de Reportes Ejecutivos*, en colaboración con las entidades *KpiInstitucionalAcademico*, *SesionMentoria*, *ReservaCupo*, *EncuestaCalidad*, *SolicitudTematica* y *RegistroAuditoriaAdmin*.

#### Diagrama 6.13.17: Análisis de Objetos (Modelo ECB) - CUS14: Visualizar Tablero de Analíticas Institucionales

```plantuml
@startuml
title Análisis de Objetos (Modelo ECB) - CUS14: Visualizar Tablero de Analíticas Institucionales\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

skinparam actor {
    BackgroundColor #E9ECEF
    BorderColor #2B3A42
}

skinparam boundary {
    BackgroundColor #E8F4F8
    BorderColor #2B3A42
}

skinparam control {
    BackgroundColor #FFF2DF
    BorderColor #2B3A42
}

skinparam entity {
    BackgroundColor #E8F8F5
    BorderColor #2B3A42
}

actor "Administrador Institucional\n(Dirección EPIS / Tutoría)" as ActAdmin
actor "Docente Investigador\n(Analista Curricular)" as ActInvestigador

boundary "UI Tablero Ejecutivo\nAnalítica Institucional" as B_TableroUI
boundary "UI Modal Filtros\ny Exportación" as B_ModalExportUI

control "Controlador de Analítica\nInstitucional (RF25)" as C_AnaliticaCtrl
control "Motor de Agregación OLAP\ny Métricas Cuantitativas" as C_MotorOlap
control "Servicio de Anonimización\n(Ley N° 29733 / RN-13)" as C_Anonimizador
control "Generador de Reportes\nEjecutivos (PDF/CSV)" as C_ReporteGen

entity "KpiInstitucionalAcademico" as E_Kpi
entity "SesionMentoria" as E_Sesion
entity "ReservaCupo" as E_Reserva
entity "EncuestaCalidad" as E_Encuesta
entity "SolicitudTematica" as E_Demanda
entity "RegistroAuditoriaAdmin" as E_AuditoriaLog

' 1. Consulta y agregación de indicadores para el cuadro de mando
ActAdmin --> B_TableroUI : 1. Accede a "Tablero de Analítica Institucional"
B_TableroUI --> C_AnaliticaCtrl : 1.1. cargarCuadroMando(semestreActivo)
C_AnaliticaCtrl --> C_MotorOlap : 1.2. consolidarMetricasSemestrales(semestre)
C_MotorOlap ..> E_Sesion : 1.2.1. computarTasaQuorumYCancelaciones()
C_MotorOlap ..> E_Reserva : 1.2.2. calcularRatioAsistenciaRealVsConfirmada()
C_MotorOlap ..> E_Encuesta : 1.2.3. agregarPuntajesSatisfaccionNeta()
C_MotorOlap ..> E_Demanda : 1.2.4. mapearDemandaInsatisfechaPorCurso()
C_MotorOlap --> E_Kpi : 1.2.5. almacenarInstantaneaMando()
C_MotorOlap --> C_AnaliticaCtrl : 1.3. entregarMetricasAgregadas(kpis)
C_AnaliticaCtrl --> B_TableroUI : 1.4. renderizarWidgetsYGraficos(kpis)
B_TableroUI --> ActAdmin : 2. Despliega KPIs (% quórum, ausentismo, vacíos temáticos, CSAT)

' 2. Filtrado y exportación de informe ejecutivo en PDF
ActAdmin --> B_TableroUI : 3. Aplica filtros por cohorte / rango de fechas
B_TableroUI --> B_ModalExportUI : 3.1. abrirOpcionesExportacion()
ActAdmin --> B_ModalExportUI : 4. Solicita "Exportar Informe Ejecutivo (PDF)"
B_ModalExportUI --> C_AnaliticaCtrl : 4.1. exportarDossierEjecutivo(filtros)
C_AnaliticaCtrl --> C_ReporteGen : 4.2. compilarDocumentoPDF(kpisFiltrados)
C_ReporteGen --> B_ModalExportUI : 4.3. entregarStreamPDF(binario)
B_ModalExportUI --> ActAdmin : 5. Descarga informe gerencial para Consejo de Facultad

' 3. Exportación de dataset anonimizado para investigación (FA02 / RN-13)
ActInvestigador --> B_ModalExportUI : 6. Solicita dataset para estudio de retención
B_ModalExportUI --> C_AnaliticaCtrl : 6.1. exportarDatasetInvestigacion(semestres)
C_AnaliticaCtrl --> C_Anonimizador : 6.2. procesarAnonimizacionDatos(Ley N° 29733)
C_Anonimizador ..> E_Encuesta : 6.2.1. disociarIdEstudiante(hashSha256)
C_Anonimizador ..> E_Reserva : 6.2.2. enmascararCodigosMatricula()
C_Anonimizador --> C_ReporteGen : 6.3. generarArchivoCSV(datasetAnonimizado)
C_ReporteGen --> E_AuditoriaLog : 6.4. registrarDescargaDataset('DATASET_ANONIMIZADO', idUsuario)
C_ReporteGen --> B_ModalExportUI : 6.5. entregarArchivoCSV(dataset)
B_ModalExportUI --> ActInvestigador : 7. Descarga CSV con registros pseudoanonimizados
@enduml
```

Fuente: Elaboración propia.

El análisis de objetos para CUS14 formaliza el subsistema de inteligencia académica de la EPIS-UPT. La interacción entre `ControladorAnaliticaInstitucional` y `MotorAgregacionOlap` desacopla el cálculo pesado de indicadores respecto al esquema transaccional, optimizando las consultas mediante vistas agregadas. En adición, el componente `ServicioAnonimizacion` implementa una salvaguarda de cumplimiento normativo conforme a `RN-13` y a la Ley N° 29733, garantizando que cualquier exportación científica o institucional disocie irreversiblemente la identidad de los estudiantes mediante algoritmos hash, conciliando la transparencia analítica con el derecho irrenunciable a la privacidad de los mentoreados.

---

## 6.3.2. Diagrama de Actividades con objetos

### Presentación del Diagrama de Actividades
El diagrama de actividades con flujo de objetos modela la dimensión temporal, las ramificaciones de control y las transformaciones de estado de los artefactos del sistema a lo largo del ciclo formativo de una mentoría académica en la EPIS-UPT. La representación se estructura en cuatro carriles (*swimlanes*) que delimitan las funciones de los actores primarios (*Mentoreado* y *Mentor*), el proceso automatizado (*Servicio Cron Backend*) y el núcleo transaccional (*Sistema Web P2P*). En el flujo se destacan explícitamente los objetos de negocio entre corchetes, explicitando las transiciones de estado de `OfertaMentoria`, `ReservaCupo`, `Bitacora` y `EncuestaCalidad`.

A continuación, se presenta el diagrama de actividades con objetos.

### Diagrama 6.14: Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos del Ciclo de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Mentor|
|#E8F4F8|Mentoreado|
|#FFF2DF|Servicio Cron Backend|
|#E8F8F5|Sistema Web P2P|

|Mentor|
start
:Selecciona asignatura formativa,
tema silábico y horario (T >= 48h);
:Define modalidad (Presencial/Virtual);

|Sistema Web P2P|
:Valida disponibilidad de aula (Parser)
o aprovisiona sala Meet/Discord;
:Publica oferta académica;
note right: **Objeto: SesionMentoria**\n[Estado: PUBLICADA]

|Mentoreado|
:Explora recomendaciones Top-k;
:Selecciona sesión y solicita cupo;

|Sistema Web P2P|
:Verifica elegibilidad del alumno y aforo libre;
:Genera reserva provisional;
note right: **Objeto: ReservaCupo**\n[Estado: PENDIENTE_CONFIRMACION]

|Mentoreado|
if (¿Ratifica asistencia antes de T-24h?) then (Sí)
    :Presiona "Confirmar Asistencia";
    |Sistema Web P2P|
    :Actualiza reserva y genera ticket QR;
    note right: **Objeto: ReservaCupo**\n[Estado: CONFIRMADA]
else (No)
    |Servicio Cron Backend|
    :Detecta corte perentorio en T-24h;
    |Sistema Web P2P|
    :Revoca reserva por morosidad;
    note right: **Objeto: ReservaCupo**\n[Estado: NO_CONFIRMADA]
endif

|Servicio Cron Backend|
:Calcula quórum en T-24h
(Confirmadas >= 50% Aforo);

|Sistema Web P2P|
if (¿Alcanzó el 50% de quórum?) then (Sí)
    :Confirma realización de sesión;
    note right: **Objeto: SesionMentoria**\n[Estado: CONFIRMADA]
    :Despacha credenciales y accesos finales;
else (No)
    :Congela sesión por quórum insuficiente;
    note right: **Objeto: SesionMentoria**\n[Estado: QUORUM_INSUFICIENTE]
    |Mentor|
    :Recibe alerta y decide acción;
    if (¿Acepta dictar en modalidad excepcional?) then (Sí)
        :Selecciona "Dictado Excepcional";
        |Sistema Web P2P|
        :Ratifica sesión con grupo reducido;
        note right: **Objeto: SesionMentoria**\n[Estado: CONFIRMADA_EXCEPCIONAL]
    else (No)
        :Selecciona "Cancelar sin Penalización";
        |Sistema Web P2P|
        :Cancela sesión y libera infraestructura;
        note right: **Objeto: SesionMentoria**\n[Estado: CANCELADA_QUORUM]
        stop
    endif
endif

|Mentor|
:Dicta la sesión de mentoría
(física en laboratorio o virtual);

|Mentor|
:Cierra sesión, marca asistencias
y redacta bitácora pedagógica;

|Sistema Web P2P|
:Registra bitácora y acumula horas;
note right: **Objeto: Bitacora**\n[Estado: REGISTRADA]\n**Objeto: SesionMentoria**\n[Estado: FINALIZADA]

|Mentoreado|
if (¿Asistió efectivamente a la sesión?) then (Sí)
    :Accede a encuesta dentro de las 24h;
    :Califica las 4 dimensiones (1-5 estrellas);
    |Sistema Web P2P|
    :Persiste evaluación y recalcula reputación;
    note right: **Objeto: EncuestaCalidad**\n[Estado: EVALUADA]
else (No)
    |Sistema Web P2P|
    :Asienta inasistencia en historial;
endif

stop
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades formaliza con precisión las sincronizaciones temporales y los puntos de bifurcación operativa:
1. **Punto de Decisión Crítico en $T-24\text{ h}$:** El diagrama evidencia la bifurcación obligatoria en la ventana de 24 horas, donde las reservas morosas son revocadas a `NO_CONFIRMADA` antes de que el proceso determine si la sesión cuenta con el respaldo numérico necesario para llevarse a cabo.
2. **Gobernanza Humanizada de Excepciones:** Frente a la falta de quórum, el flujo no cancela unilateralmente el evento de forma ciega; transfiere la gobernanza al Mentor para que evalúe si el valor pedagógico del grupo amerita un `Dictado Excepcional` sin menoscabar el tiempo de los alumnos confirmados.
3. **Cierre Transaccional Pedagógico:** La ejecución concluye únicamente cuando la bitácora es asentada por el mentor (`Bitacora [REGISTRADA]`) y los estudiantes efectivos retroalimentan el sistema (`EncuestaCalidad [EVALUADA]`), cerrando el ciclo de mejora continua de la enseñanza.

### 6.3.2.1. CUS01 – Actividades con Objetos: Iniciar Sesión Institucional con 2FA

El diagrama de actividades con flujo de objetos modela la secuencia lógica, las evaluaciones de bifurcación y las transiciones de estado de los artefactos informáticos durante el ingreso seguro a la plataforma. Se organiza en tres carriles de ejecución (*swimlanes*): el *Usuario Institucional*, el *Sistema Web P2P (Backend)* y el *Servicio SMTP UPT*. Durante el flujo se destacan los cambios de estado en las entidades del dominio: `CredencialOTP` (desde su estado inicial `EMITIDO` hasta `VALIDADO`), `RegistroConsentimiento` (formalizado en estado `REGISTRADO` bajo la Ley N° 29733) y el artefacto de autorización `TokenSesionJWT` (transicionado a estado `ACTIVO`).

#### Diagrama 6.14.1: Diagrama de Actividades con Flujo de Objetos - CUS01: Iniciar Sesión Institucional con 2FA

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS01: Iniciar Sesión Institucional con 2FA\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Usuario Institucional|
|#E8F8F5|Sistema Web P2P (Backend)|
|#FFF2DF|Servicio SMTP UPT|

|Usuario Institucional|
start
:Ingresa dirección de correo institucional;

|Sistema Web P2P (Backend)|
if (¿Dominio oficial @upt.pe y cuenta activa?) then (No)
    :Muestra error de acceso no autorizado;
    note right: **Evento E01/E02**\nAcceso bloqueado
    |Usuario Institucional|
    stop
else (Sí)
    |Sistema Web P2P (Backend)|
    :Genera código numérico aleatorio (6 dígitos);
    :Registra credencial temporal con vigencia de 5 min;
    note right: **Objeto: CredencialOTP**\n[Estado: EMITIDO]
    
    |Servicio SMTP UPT|
    :Despacha correo electrónico con clave OTP;
    
    |Usuario Institucional|
    :Revisa bandeja universitaria y copia OTP;
    :Introduce código OTP en el formulario web;
    
    |Sistema Web P2P (Backend)|
    if (¿Código OTP coincide y tiempo < 5 min?) then (No)
        :Registra intento fallido y evalúa tasa de abusos;
        note right: **Evento E03/E04**\nCódigo inválido o expirado
        |Usuario Institucional|
        stop
    else (Sí)
        |Sistema Web P2P (Backend)|
        :Marca credencial temporal como consumida;
        note right: **Objeto: CredencialOTP**\n[Estado: VALIDADO]
        
        if (¿Cuenta con consentimiento previo Ley N° 29733?) then (Sí)
            ' Flujo alternativo FA01: Omisión de modal
        else (No)
            |Usuario Institucional|
            :Lee términos y condiciones de datos personales;
            if (¿Acepta cláusulas de consentimiento?) then (Sí)
                |Sistema Web P2P (Backend)|
                :Persiste registro legal (UUID, IP, Timestamp);
                note right: **Objeto: RegistroConsentimiento**\n[Estado: REGISTRADO]
            else (No)
                |Sistema Web P2P (Backend)|
                :Cancela sesión temporal por rechazo legal;
                note right: **Evento E06**\nInfracción RN-02
                |Usuario Institucional|
                stop
            endif
        endif
        
        |Sistema Web P2P (Backend)|
        :Genera token de autorización criptográfico (JWT);
        note right: **Objeto: TokenSesionJWT**\n[Estado: ACTIVO]
        :Redirige a la vista principal según el rol asignado;
        
        |Usuario Institucional|
        :Accede al Dashboard de la plataforma;
        stop
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos explicita los puntos críticos de control de acceso: la verificación temprana del dominio `@upt.pe` previa a cualquier llamada de red SMTP, el control perentorio de expiración de 5 minutos sobre `CredencialOTP` (RN-01) y la compuerta de decisión sobre la formalización del consentimiento legal (RN-02). Asimismo, demuestra cómo el sistema preserva la integridad del proceso impidiendo la generación de `TokenSesionJWT` si el estudiante desiste de aceptar los términos de privacidad.

### 6.3.2.2. CUS04 – Actividades con Objetos: Reservar Cupo de Mentoría

El diagrama de actividades con flujo de objetos modela el comportamiento transaccional del proceso de reserva de cupos bajo condiciones de concurrencia. La ejecución se distribuye en tres carriles (*swimlanes*): el *Estudiante Mentoreado*, el *Sistema Web P2P (Backend)* y la *Base de Datos PostgreSQL (Supabase)*. El flujo explicita el bloqueo pesimista de fila sobre la entidad `SesionMentoria`, las evaluaciones de guarda para aforos máximos (RN-05) y elegibilidad académica, y la instanciación de `ReservaCupo` en estado `PENDIENTE_CONFIRMACION` con su correspondiente ventana de caducidad perentoria fijada en $T-24\text{ h}$ (RN-08).

#### Diagrama 6.14.2: Diagrama de Actividades con Flujo de Objetos - CUS04: Reservar Cupo de Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS04: Reservar Cupo de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Estudiante Mentoreado|
|#E8F8F5|Sistema Web P2P (Backend)|
|#FFF2DF|Base de Datos PostgreSQL (Supabase)|

|Estudiante Mentoreado|
start
:Explora catálogo de ofertas o recomendación Top-k;
:Selecciona sesión y presiona "Reservar Cupo";

|Sistema Web P2P (Backend)|
:Inicia transacción atómica ACID;
:Solicita bloqueo pesimista de la oferta;

|Base de Datos PostgreSQL (Supabase)|
:Ejecuta SELECT ... FOR UPDATE sobre la sesión;
note right: **Objeto: SesionMentoria**\n[Fila bloqueada contra carreras]

|Sistema Web P2P (Backend)|
if (¿Cupos ocupados < Aforo máximo y Estado = PUBLICADA?) then (No)
    |Base de Datos PostgreSQL (Supabase)|
    :Ejecuta ROLLBACK de transacción;
    |Sistema Web P2P (Backend)|
    :Genera alerta de vacantes agotadas;
    note right: **Evento E01**\nColisión de aforo
    |Estudiante Mentoreado|
    :Visualiza sugerencia de registrar Demanda (CUS03);
    stop
else (Sí)
    |Sistema Web P2P (Backend)|
    :Valida ciclo formativo y ausencia de cruces horarios;
    if (¿Cumple elegibilidad académica y sin cruces?) then (No)
        |Base de Datos PostgreSQL (Supabase)|
        :Ejecuta ROLLBACK de transacción;
        |Sistema Web P2P (Backend)|
        :Notifica causa de rechazo de reserva;
        note right: **Evento E02/E03**\nCruce de agenda o duplicidad
        |Estudiante Mentoreado|
        stop
    else (Sí)
        |Base de Datos PostgreSQL (Supabase)|
        :Inserta nuevo registro de reserva;
        note right: **Objeto: ReservaCupo**\n[Estado: PENDIENTE_CONFIRMACION]
        :Incrementa contador de cupos ocupados;
        note right: **Objeto: SesionMentoria**\n[cupos_ocupados++]
        :Ejecuta COMMIT transaccional;
        
        |Sistema Web P2P (Backend)|
        :Calcula plazo perentorio de confirmación (T-24h);
        :Prepara modal con temporizador regresivo;
        
        |Estudiante Mentoreado|
        :Recibe acuse de reserva exitosa;
        :Visualiza compromiso de ratificación antes de T-24h;
        stop
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades evidencia cómo la arquitectura previene la sobreventa de cupos ante accesos concurrentes de múltiples estudiantes. Mediante el bloqueo pesimista en PostgreSQL, la comprobación del aforo (10 presencial / 20 virtual, según RN-05) y la verificación de solapamientos horarios se efectúan dentro de una transacción indivisible, asegurando que el objeto `ReservaCupo` adquiera el estado `PENDIENTE_CONFIRMACION` únicamente cuando existe una vacante legítimamente asegurada para el mentoreado.

### 6.3.2.3. CUS24 – Actividades con Objetos: Confirmar Asistencia a Mentoría

El diagrama de actividades con flujo de objetos modela la dinámica operativa de la ratificación de asistencia. La lógica se representa a través de tres carriles (*swimlanes*): el *Estudiante Mentoreado*, el *Sistema Web P2P (Backend)* y el *Servicio SMTP UPT*. Se explicitan la captura del tiempo del servidor para la validación de la ventana de 24 horas (RN-08), la transición de estado del objeto `ReservaCupo` desde `PENDIENTE_CONFIRMACION` hacia `CONFIRMADA`, la instanciación de `TicketAsistencia` en estado `EMITIDO` y la habilitación de los detalles de infraestructura.

#### Diagrama 6.14.3: Diagrama de Actividades con Flujo de Objetos - CUS24: Confirmar Asistencia a Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS24: Confirmar Asistencia a Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

|#F8F9FA|Estudiante Mentoreado|
|#E8F8F5|Sistema Web P2P (Backend)|
|#FFF2DF|Servicio SMTP UPT|

|Estudiante Mentoreado|
start
:Ingresa a "Mis Reservas" o pulsa enlace del correo;
:Localiza reserva en PENDIENTE_CONFIRMACION;
:Presiona "Confirmar Asistencia";

|Sistema Web P2P (Backend)|
:Captura estampa de tiempo del servidor;
:Calcula ventana temporal restante: T = (T_inicio - T_actual);

if (¿T >= 24 horas?) then (No)
    :Bloquea la confirmación extemporánea;
    note right: **Evento E01**\nInfracción RN-08 (Ventana expirada)
    :Notifica revocación y liberación de cupo;
    |Estudiante Mentoreado|
    stop
else (Sí)
    |Sistema Web P2P (Backend)|
    :Actualiza entidad ReservaCupo;
    note right: **Objeto: ReservaCupo**\n[Estado: CONFIRMADA]
    
    :Genera token criptográfico de asistencia y QR;
    note right: **Objeto: TicketAsistencia**\n[Estado: EMITIDO]
    
    |Servicio SMTP UPT|
    :Despacha ticket digital con QR al correo institucional;
    
    |Sistema Web P2P (Backend)|
    :Habilita credenciales definitivas en pantalla\n(Aula en EPIS o enlace Google Meet);
    
    |Estudiante Mentoreado|
    :Visualiza código QR de ingreso y detalles de aula;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades formaliza el punto de control normativo de la regla RN-08: la ratificación únicamente se autoriza si dista al menos 24 horas del inicio de la mentoría. Esto garantiza que las reservas no ratificadas sean interceptadas posteriormente por el demonio cron en CUS23, permitiendo que el objeto `ReservaCupo` consolidado en `CONFIRMADA` participe legítimamente en la contabilización del quórum regulatorio.

### 6.3.2.4. CUS23 – Actividades con Objetos: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

El diagrama de actividades con flujo de objetos modela el procesamiento por lotes ejecutado por el demonio cron del backend en la ventana perentoria de corte temporal ($T-24\text{ h}$). Se distribuye en cuatro carriles (*swimlanes*): *Demonio Cron Backend*, *Controlador de Quórum*, *Base de Datos PostgreSQL* y *Servicio SMTP UPT*. Durante el procesamiento se explicitan los cambios de estado sobre las entidades `ReservaCupo` (de `PENDIENTE_CONFIRMACION` a `NO_CONFIRMADA`) y `SesionMentoria` (bifurcando hacia `CONFIRMADA` si se cumple la regla RN-09 de al menos 50% de aforo ratificado, o hacia `QUORUM_INSUFICIENTE` en caso de déficit de confirmaciones).

#### Diagrama 6.14.4: Diagrama de Actividades con Flujo de Objetos - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Demonio Cron Backend|
start
:Disparo temporizado periódico (cada 15 min);
:Invoca evaluación de corte T-24h;

|#FFF2DF|Controlador de Quórum|
:Consulta sesiones en estado PUBLICADA\ncon inicio en ventana (ahora <= T_inicio <= ahora + 24h);

|#E8F8F5|Base de Datos PostgreSQL|
:Inicia transacción ACID;
:Identifica reservas no ratificadas en la sesión;
:Actualiza reservas morosas masivamente;
note right: **Objeto: ReservaCupo**\n[Estado anterior: PENDIENTE_CONFIRMACION]\n[Estado nuevo: NO_CONFIRMADA]

:Contabiliza reservas con estado CONFIRMADA;

|#FFF2DF|Controlador de Quórum|
if (¿Confirmadas >= 50% de Aforo Máximo? [RN-09]) then (Sí: Quórum Alcanzado)
    |#E8F8F5|Base de Datos PostgreSQL|
    :Actualiza estado de la sesión;
    note right: **Objeto: SesionMentoria**\n[Estado: CONFIRMADA]
    :Confirma transacción (COMMIT);
    
    |#E8F4F8|Servicio SMTP UPT|
    :Despacha confirmación definitiva y datos de acceso\na mentor y mentoreados confirmados;
    
    |Demonio Cron Backend|
    :Registra éxito de confirmación en log;
    stop
else (No: Quórum Insuficiente)
    |#E8F8F5|Base de Datos PostgreSQL|
    :Actualiza estado de la sesión;
    note right: **Objeto: SesionMentoria**\n[Estado: QUORUM_INSUFICIENTE]
    :Confirma transacción (COMMIT);
    
    |#E8F4F8|Servicio SMTP UPT|
    :Despacha alerta urgente a Mentor indicando\nfalta de quórum y necesidad de resolución (CUS07);
    
    |Demonio Cron Backend|
    :Registra evento de quórum insuficiente en log;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades automatizado formaliza la ejecución desatendida del corte reglamentario sin intervención manual. La revocación forzosa de reservas no confirmadas muta el estado del objeto `ReservaCupo` a `NO_CONFIRMADA`, garantizando que solo los estudiantes debidamente ratificados sean computados para el umbral mínimo del 50% del aforo (RN-09). La bifurcación resultante actualiza de forma atómica la `SesionMentoria` hacia `CONFIRMADA` (habilitando la ejecución) o hacia `QUORUM_INSUFICIENTE`, disparando en este último caso las alertas asíncronas para que el mentor proceda a su resolución mediante dictado excepcional o cancelación (CUS07).

### 6.3.2.5. CUS07 – Actividades con Objetos: Gestionar Sesión ante Quórum Insuficiente

El diagrama de actividades con flujo de objetos modela las ramificaciones de control, decisiones y mutaciones de estado de los artefactos informáticos durante la resolución de una sesión declarada en quórum insuficiente. Se organiza en cinco carriles (*swimlanes*): *Estudiante Mentor*, *UI Resolución Quórum*, *Controlador de Quórum*, *Base de Datos PostgreSQL* y *Servicio SMTP UPT*. Durante el flujo se destacan las transiciones de estado de `SesionMentoria` (bifurcando a `CONFIRMADA_EXCEPCIONAL` o `CANCELADA_QUORUM`), `ReservaCupo` (mutando a `CANCELADA_SISTEMA` en caso de cancelación), `EspacioFisico` (liberado en estado `DISPONIBLE`) y `RegistroAuditoria` (asentado en estado `SIN_PENALIZACION` bajo la regla RN-10).

#### Diagrama 6.14.5: Diagrama de Actividades con Flujo de Objetos - CUS07: Gestionar Sesión ante Quórum Insuficiente

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS07: Gestionar Sesión ante Quórum Insuficiente\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Estudiante Mentor|
start
:Recibe notificación de quórum insuficiente;
:Accede a pantalla de gestión de quórum;

|#E8F4F8|UI Resolución Quórum|
:Muestra balance de sesión: aforo, confirmados y déficit;
:Presenta alternativas: Dictado Excepcional o Cancelación;

|#E9ECEF|Estudiante Mentor|
if (¿Desea dictar la mentoría con los alumnos confirmados? [RN-09]) then (Sí: Dictado Excepcional)
    :Selecciona "Confirmar Dictado Excepcional";
    |#FFF2DF|Controlador de Quórum|
    :Procesa resolución de dictado excepcional;
    
    |#E8F8F5|Base de Datos PostgreSQL|
    :Actualiza estado de la sesión;
    note right: **Objeto: SesionMentoria**\n[Estado anterior: QUORUM_INSUFICIENTE]\n[Estado nuevo: CONFIRMADA_EXCEPCIONAL]
    :Mantiene reservas confirmadas intactas;
    
    |#E8F4F8|Servicio SMTP UPT|
    :Despacha ratificación definitiva de dictado\na estudiantes confirmados y al mentor;
    
    |UI Resolución Quórum|
    :Despliega confirmación de sesión activa;
    stop
else (No: Cancelación por Falta de Quórum)
    :Selecciona "Cancelar Sesión por Quórum";
    |#FFF2DF|Controlador de Quórum|
    :Inicia transacción de cancelación sin penalidad;
    
    |#E8F8F5|Base de Datos PostgreSQL|
    :Actualiza estado de la sesión;
    note right: **Objeto: SesionMentoria**\n[Estado: CANCELADA_QUORUM]
    
    :Actualiza reservas confirmadas a canceladas;
    note right: **Objeto: ReservaCupo**\n[Estado anterior: CONFIRMADA]\n[Estado nuevo: CANCELADA_SISTEMA]
    
    :Libera aula física o sala virtual;
    note right: **Objeto: EspacioFisico**\n[Estado: DISPONIBLE]
    
    :Registra constancia de auditoría;
    note right: **Objeto: RegistroAuditoria**\n[Estado: SIN_PENALIZACION]\n[Regla: RN-10]
    
    |#E8F4F8|Servicio SMTP UPT|
    :Despacha notificación formal de cancelación\neximiendo de culpa a los alumnos y al mentor;
    
    |UI Resolución Quórum|
    :Muestra comprobante de cancelación registrada;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades formaliza la soberanía del mentor frente a la contingencia de quórum deficitario, evitando la rigidez de cancelaciones automáticas lesivas. La alternativa de `Dictado Excepcional` rescata el compromiso formativo con los estudiantes que sí ratificaron a tiempo, mutando `SesionMentoria` a `CONFIRMADA_EXCEPCIONAL`. Por el contrario, la `Cancelación por Quórum` resguarda a los estudiantes confirmados de sanciones mutando sus registros a `CANCELADA_SISTEMA`, devuelve el ambiente físico o virtual al inventario universitario (`EspacioFisico [DISPONIBLE]`) y genera un asiento inmutable de exención en `RegistroAuditoria` según lo prescrito en la regla RN-10.

### 6.3.2.6. CUS09 – Actividades con Objetos: Publicar Oferta de Mentoría Individual o Grupal

El diagrama de actividades con flujo de objetos modela la secuencia lógica, las reglas de validación y las mutaciones de estado requeridas para publicar una oferta de mentoría en el sistema. Se organiza en cinco carriles (*swimlanes*): *Estudiante Mentor*, *UI Publicación Oferta*, *Controlador de Publicación*, *Base de Datos PostgreSQL* y *Servicio de Infraestructura*. Durante la ejecución se destacan las transiciones de estado sobre la entidad `SesionMentoria` (iniciando en `BORRADOR` y transicionando a `PUBLICADA`) y la entidad `EspacioFisico` (asignada en estado `RESERVADO` en modalidad presencial).

#### Diagrama 6.14.6: Diagrama de Actividades con Flujo de Objetos - CUS09: Publicar Oferta de Mentoría Individual o Grupal

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS09: Publicar Oferta de Mentoría Individual o Grupal\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Estudiante Mentor|
start
:Ingresa a "Publicar Nueva Mentoría";
:Ingresa datos: asignatura, título, descripción,\nfecha/hora inicio, modalidad y aforo;

|#E8F4F8|UI Publicación Oferta|
:Envía formulario de creación;

|#FFF2DF|Controlador de Publicación|
if (¿Anticipación >= 48h? [RN-04]) then (No)
    |UI Publicación Oferta|
    :Muestra error "La sesión debe publicarse con\nal menos 48h de anticipación";
    stop
else (Sí)
    |Controlador de Publicación|
    if (¿Aforo respeta límites según modalidad? [RN-05]) then (No)
        |UI Publicación Oferta|
        :Muestra error "Aforo supera límite reglamentario\n(Presencial <= 10, Virtual <= 20)";
        stop
    else (Sí)
        |#E8F8F5|Base de Datos PostgreSQL|
        :Inicia transacción ACID;
        :Instancia borrador de sesión;
        note right: **Objeto: SesionMentoria**\n[Estado inicial: BORRADOR]
        
        |#FFF2DF|Controlador de Publicación|
        if (¿Modalidad seleccionada?) then (Presencial)
            |#E8F4F8|Servicio de Infraestructura|
            :Consulta disponibilidad de aula en EPIS;
            :Asigna aula física para el horario solicitado;
            note right: **Objeto: EspacioFisico**\n[Estado: RESERVADO]
            
            |#E8F8F5|Base de Datos PostgreSQL|
            :Asocia id_aula a la sesión;
        else (Virtual)
            |#E8F4F8|Servicio de Infraestructura|
            :Genera enlace dinámico de reunión Google Meet;
            
            |#E8F8F5|Base de Datos PostgreSQL|
            :Registra URL de sala virtual en la sesión;
        endif
        
        :Actualiza sesión a estado público;
        note right: **Objeto: SesionMentoria**\n[Estado nuevo: PUBLICADA]
        :Confirma transacción (COMMIT);
        
        |UI Publicación Oferta|
        :Despliega confirmación de publicación exitosa\ny visualiza sesión en el catálogo de ofertas;
        stop
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades asegura que ninguna oferta académica sea expuesta en el catálogo estudiantil sin validar previamente los criterios pedagógicos y logísticos de la EPIS. La bifurcación inicial aborta la publicación si no se respeta la antelación mínima de 48 horas (RN-04) o si los cupos propuestos desbordan las capacidades máximas normadas (RN-05). Una vez superadas las validaciones, el objeto `SesionMentoria` se crea transaccionalmente en `BORRADOR`, coordina con la infraestructura para asegurar el espacio (`EspacioFisico [RESERVADO]` o enlace Meet) y culmina mutando formalmente a `PUBLICADA`, habilitando el proceso concurrente de inscripciones (CUS04).

### 6.3.2.7. CUS14 – Actividades con Objetos: Consultar Agenda y Horarios de Mentorías

El diagrama de actividades con flujo de objetos modela el procesamiento analítico y la transformación de datos requerida para responder a las consultas de agenda estudiantil y docente. Se distribuye en cuatro carriles (*swimlanes*): *Usuario Institucional*, *UI Agenda Calendario*, *Controlador de Agenda* y *Base de Datos / Caché*. Durante el flujo se destacan los objetos de negocio: `FiltroBusquedaDTO` (aplicado sobre los parámetros de búsqueda), `SesionMentoria` (recuperada en estados vigentes `PUBLICADA` o `CONFIRMADA`), y el artefacto de visualización `MatrizCalendarioDTO` (renderizado con métricas de aforo en tiempo real).

#### Diagrama 6.14.7: Diagrama de Actividades con Flujo de Objetos - CUS14: Consultar Agenda y Horarios de Mentorías

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS14: Consultar Agenda y Horarios de Mentorías\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Usuario Institucional|
start
:Accede a la sección "Agenda de Mentorías";
:Define filtros opcionales (asignatura, fecha, modalidad);

|#E8F4F8|UI Agenda Calendario|
:Genera solicitud de consulta con parámetros;
note right: **Objeto: FiltroBusquedaDTO**\n[Estado: APLICADO]

|#FFF2DF|Controlador de Agenda|
:Verifica existencia de resultado en caché Redis;

if (¿Existe clave en Caché?) then (Sí: Cache Hit)
    :Recupera colección serializada;
else (No: Cache Miss)
    |#E8F8F5|Base de Datos / Caché|
    :Ejecuta consulta relacional indexada;
    :Filtra sesiones vigentes (PUBLICADA, CONFIRMADA);
    note right: **Objeto: SesionMentoria**\n[Estados: PUBLICADA / CONFIRMADA]
    
    :Calcula disponibilidad de cupos en tiempo real\n(cupos_disponibles = aforo - cupos_ocupados);
    :Cruza con reservas del usuario autenticado;
    :Almacena resultado en caché con TTL de 300s;
endif

|#FFF2DF|Controlador de Agenda|
:Consolida colección de eventos con estado de cupos;

|#E8F4F8|UI Agenda Calendario|
:Construye matriz de eventos mensual/semanal;
note right: **Objeto: MatrizCalendarioDTO**\n[Estado: RENDERIZADO]

:Despliega cuadrícula interactiva con badges:\n- Vacantes Disponibles\n- Aforo Completo\n- Inscripción Activa;

|Usuario Institucional|
:Visualiza agenda consolidada y selecciona sesión;
stop
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades formaliza la estrategia de alta eficiencia estipulada en RNF01 para el catálogo interactivo. La evaluación condicional de la caché en memoria amortigua la demanda sobre la base de datos PostgreSQL frente a ráfagas de consultas recurrentes. El cómputo dinámico de vacantes libres garantiza la transparencia estipulada en RN-05, permitiendo que el objeto `MatrizCalendarioDTO` provea información fidedigna e inmediata al usuario institucional respecto a qué eventos disponen aún de plazas y cuáles registran aforo completo.

### 6.3.2.8. CUS11 – Actividades con Objetos: Registrar Asistencia Mediante Código QR

El diagrama de actividades con flujo de objetos modela el procesamiento dinámico y las bifurcaciones de control durante la lectura óptica de tickets en el aula o sala virtual. Se estructura en cuatro carriles (*swimlanes*): *Estudiante Mentoreado*, *UI Escáner Mentor*, *Controlador de Asistencia* y *Base de Datos PostgreSQL*. Se destacan las mutaciones de estado sobre la entidad `TicketAsistencia` (verificada en estado `CONSUMIDO`), `ReservaCupo` (de `CONFIRMADA` a `ASISTIDA`) y la instanciación de `RegistroAsistencia` (en estado `REGISTRADO`).

#### Diagrama 6.14.8: Diagrama de Actividades con Flujo de Objetos - CUS11: Registrar Asistencia Mediante Código QR

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS11: Registrar Asistencia Mediante Código QR\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Estudiante Mentoreado|
start
:Abre la aplicación móvil / web;
:Presenta en pantalla el ticket con código QR;

|#E8F4F8|UI Escáner Mentor|
:Apunta la cámara del dispositivo hacia el código QR;
:Captura payload visual y transmite hash;

|#FFF2DF|Controlador de Asistencia|
:Verifica firma criptográfica SHA-256 del ticket;

if (¿Firma válida y no alterada?) then (No)
    |UI Escáner Mentor|
    :Despliega error "Ticket inválido o alterado";
    stop
else (Sí)
    |Controlador de Asistencia|
    if (¿Dentro de ventana de tolerancia? [RN-11: -15m a +30m]) then (No)
        |UI Escáner Mentor|
        :Muestra alerta "Fuera de hora reglamentaria.\nRequiere registro manual en bitácora";
        stop
    else (Sí)
        |#E8F8F5|Base de Datos PostgreSQL|
        :Inicia transacción ACID;
        :Verifica estado de reserva y ticket;
        
        |#FFF2DF|Controlador de Asistencia|
        if (¿Reserva en estado CONFIRMADA y ticket no consumido?) then (No: Ya asistió o cancelada)
            |UI Escáner Mentor|
            :Muestra alerta "Ticket ya consumido o reserva no ratificada";
            stop
        else (Sí: Apto para registrar)
            |#E8F8F5|Base de Datos PostgreSQL|
            :Actualiza estado de la reserva;
            note right: **Objeto: ReservaCupo**\n[Estado anterior: CONFIRMADA]\n[Estado nuevo: ASISTIDA]
            
            :Invalida reutilización del ticket;
            note right: **Objeto: TicketAsistencia**\n[Estado: CONSUMIDO]
            
            :Inserta registro de auditoría de asistencia;
            note right: **Objeto: RegistroAsistencia**\n[Estado: REGISTRADO]\n[Método: ESCANEO_QR]
            
            :Confirma transacción (COMMIT);
            
            |UI Escáner Mentor|
            :Emite pitido de confirmación y banner verde:\n"Asistencia registrada: [Nombre del Alumno]";
            stop
        endif
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos formaliza el protocolo estricto de control de presencia física o remota. La comprobación temprana del hash criptográfico mitiga ataques de falsificación de credenciales, mientras que la bifurcación temporal impone la observancia de la regla RN-11 (-15 min a +30 min desde el inicio). La mutación atómica de `ReservaCupo` hacia `ASISTIDA` y la deshabilitación del objeto `TicketAsistencia` impiden de forma concluyente el doble registro con un mismo código, asegurando la veracidad de las métricas que respaldarán el visado de bitácora y la certificación de horas.

### 6.3.2.9. CUS10 - Actividades con Objetos: Registrar Bitácora Pedagógica de Sesión

El diagrama de actividades con flujo de objetos modela el comportamiento secuencial, las validaciones temporales y las mutaciones de estado de los artefactos informáticos durante el asentamiento de la bitácora docente. Se organiza en cuatro carriles (*swimlanes*): el *Estudiante Mentor*, la *UI Formulario Bitácora*, el *Controlador de Bitácora* y la *Base de Datos PostgreSQL*. Se destacan los cambios de estado en las entidades del dominio: `ReservaCupo` (transicionada a `INASISTENCIA` para cupos no marcados según RN-11), `BitacoraSesion` (creada en estado `REGISTRADA`), `SesionMentoria` (mutada a `FINALIZADA`) y `BolsaHorasMentor` (actualizada para la acumulación formativa según RN-12).

#### Diagrama 6.14.9: Diagrama de Actividades con Flujo de Objetos - CUS10: Registrar Bitácora Pedagógica de Sesión

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS10: Registrar Bitácora Pedagógica de Sesión\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Estudiante Mentor|
start
:Accede a la sesión culminada en su panel docente;
:Solicita apertura del formulario de bitácora;

|#E8F4F8|UI Formulario Bitácora|
:Solicita contexto de la sesión y relación de reservas;

|#FFF2DF|Controlador de Bitácora|
:Verifica temporizador de corte [RN-07];

if (¿Tiempo transcurrido desde fin de sesión > 24 horas?) then (Sí: Plazo vencido)
    |UI Formulario Bitácora|
    :Despliega bloqueo de interfaz:\n"Plazo de 24h perimido. Solicite regularización a Tutoría";
    stop
else (No: Dentro de plazo legal)
    |UI Formulario Bitácora|
    :Renderiza formulario estructurado y nómina de inscritos\ncon marcas de asistencia QR previas;
    
    |#E9ECEF|Estudiante Mentor|
    :Ingresa desarrollo de temas silábicos (mínimo 30 caracteres);
    :Registra dificultades académicas observadas y recomendaciones;
    :Revisa estatus final de alumnos y pulsa "Registrar Bitácora";
    
    |#FFF2DF|Controlador de Bitácora|
    :Valida sintaxis, longitud mínima y parámetros pedagógicos;
    
    if (¿Campos válidos y completos?) then (No)
        |UI Formulario Bitácora|
        :Muestra mensajes de error en campos requeridos;
        stop
    else (Sí)
        |#E8F8F5|Base de Datos PostgreSQL|
        :Inicia transacción ACID;
        
        :Actualiza reservas no validadas por QR;
        note right: **Objeto: ReservaCupo**\n[Estado anterior: CONFIRMADA]\n[Estado nuevo: INASISTENCIA]\n*(RN-11: Cierre de listas)*
        
        :Inserta entidad de bitácora formal;
        note right: **Objeto: BitacoraSesion**\n[Estado: REGISTRADA]\n[Contenido: Temas, Dificultades, Acuerdos]
        
        :Transiciona el estado de la mentoría;
        note right: **Objeto: SesionMentoria**\n[Estado anterior: EN_CURSO]\n[Estado nuevo: FINALIZADA]
        
        :Acumula horas formativas del mentor;
        note right: **Objeto: BolsaHorasMentor**\n[Estado: ACTUALIZADA]\n*(RN-12: Horas computables)*
        
        :Inserta traza de auditoría inmutable;
        :Confirma transacción (COMMIT);
        
        |UI Formulario Bitácora|
        :Despliega confirmación de éxito y acuse foliado:\n"Bitácora asentada y horas acreditadas con éxito";
        stop
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos formaliza el cierre operativo inalterable de cada sesión de mentoría. La verificación temprana de la ventana de 24 horas (RN-07) salvaguarda la frescura y fidelidad de los datos pedagógicos. La ejecución transaccional garantiza la sincronización atómica entre el cierre definitivo de asistencias (pasando a `INASISTENCIA` las no confirmadas presencialmente según RN-11), el estado `FINALIZADA` de la sesión y la acumulación fehaciente de horas formativas en la bolsa del mentor (RN-12), sentando las bases probatorias requeridas para el visado de la Comisión de Tutoría.

### 6.3.2.10. CUS05 - Actividades con Objetos: Responder Encuesta de Calidad Post-Mentoría

El diagrama de actividades con flujo de objetos modela la secuencia lógica, las condiciones de admisibilidad temporal y las transformaciones de estado de los artefactos informáticos durante la captura de retroalimentación cualitativa y cuantitativa. Se estructura en cuatro carriles (*swimlanes*): el *Estudiante Mentoreado*, la *UI Encuesta Calidad*, el *Controlador de Encuestas* y la *Base de Datos PostgreSQL*. Se destacan los cambios de estado en las entidades del dominio: `ReservaCupo` (marcada como evaluada con flag `encuesta_completada = TRUE`), `EncuestaSatisfaccion` (instanciada en estado `REGISTRADA` con identificador disociado) y `ReputacionMentor` (recalculada y transicionada a estado `ACTUALIZADA` bajo RN-13).

#### Diagrama 6.14.10: Diagrama de Actividades con Flujo de Objetos - CUS05: Responder Encuesta de Calidad Post-Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS05: Responder Encuesta de Calidad Post-Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Estudiante Mentoreado|
start
:Ingresa a la sección "Encuestas Pendientes";
:Selecciona la sesión de mentoría a evaluar;

|#E8F4F8|UI Encuesta Calidad|
:Solicita verificación de aptitud y formulario de reactivos;

|#FFF2DF|Controlador de Encuestas|
:Evalúa condiciones de admisibilidad;

if (¿Reserva en estado ASISTIDA y sin evaluación previa?) then (No)
    |UI Encuesta Calidad|
    :Despliega error:\n"Solo estudiantes con asistencia efectiva pueden evaluar";
    stop
else (Sí)
    if (¿Dentro de ventana de 24h tras cierre de bitácora?) then (No)
        |UI Encuesta Calidad|
        :Despliega aviso de caducidad:\n"La ventana de evaluación de 24h ha vencido";
        stop
    else (Sí)
        |UI Encuesta Calidad|
        :Renderiza formulario interactivo con 4 dimensiones Likert (1 a 5)\ny cuadro de texto cualitativo opcional;
        
        |#E9ECEF|Estudiante Mentoreado|
        :Asigna puntuación de 1 a 5 a los 4 reactivos obligatorios;
        :Ingresa retroalimentación cualitativa constructiva (opcional);
        :Presiona "Enviar Evaluación de Calidad";
        
        |#FFF2DF|Controlador de Encuestas|
        :Valida completitud de reactivos cuantitativos;
        :Aplica disociación criptográfica de identidad [Ley N° 29733];
        
        |#E8F8F5|Base de Datos PostgreSQL|
        :Inicia transacción ACID;
        
        :Marca cupo como evaluado;
        note right: **Objeto: ReservaCupo**\n[Flag: encuesta_completada = TRUE]
        
        :Persiste la evaluación anonimizada;
        note right: **Objeto: EncuestaSatisfaccion**\n[Estado: REGISTRADA]\n[Identificador: HASH_ANONIMO]
        
        :Recalcula indicador de calidad del mentor [RN-13];
        note right: **Objeto: ReputacionMentor**\n[Estado: ACTUALIZADA]\n[Métrica: Media Móvil Ponderada]
        
        :Registra traza inmutable en bitácora de auditoría;
        :Confirma transacción (COMMIT);
        
        |UI Encuesta Calidad|
        :Despliega mensaje institucional de agradecimiento:\n"¡Gracias por tu retroalimentación! Calidad registrada";
        stop
    endif
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos formaliza el mecanismo de retroalimentación protegiendo la imparcialidad del proceso. La evaluación condicional inicial restringe el llenado exclusivamente a reservas `ASISTIDA` dentro de la ventana de 24 horas, descartando opiniones de alumnos no asistentes (E02) o extemporáneas (E01). La anonimización automática disocia el nombre y código del estudiante conforme a la Ley N° 29733 antes de asentar `EncuestaSatisfaccion`, permitiendo que el objeto `ReputacionMentor` evolucione de forma transparente mediante la media ponderada de las dimensiones pedagógicas evaluadas (RN-13).

### 6.3.2.11. CUS19 - Actividades con Objetos: Consultar Historial de Sesiones y Asistencia

El diagrama de actividades con flujo de objetos modela el procesamiento dinámico, la segregación de seguridad por políticas RLS y la composición de vistas durante la consulta del expediente de mentorías. Se estructura en cuatro carriles (*swimlanes*): el *Usuario Institucional*, la *UI Tablero Historial*, el *Controlador de Historial* y la *Base de Datos PostgreSQL (RLS)*. Se explicitan los objetos de transferencia instanciados en tiempo de ejecución: `PantallaEstadoVacioDTO` (renderizado ante ausencia de eventos históricos), `ColeccionHistorialDTO` (estructurado con métricas de asistencia y horas) y `DetalleBitacoraDTO` (cargado a demanda en el panel lateral).

#### Diagrama 6.14.11: Diagrama de Actividades con Flujo de Objetos - CUS19: Consultar Historial de Sesiones y Asistencia

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS19: Consultar Historial de Sesiones y Asistencia\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam activity {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam note {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

|#E9ECEF|Usuario Institucional|
start
:Selecciona "Mi Historial Académico" en el menú principal;

|#E8F4F8|UI Tablero Historial|
:Captura token de sesión y parámetros iniciales (semestre activo);
:Emite petición de consulta histórica consolidada;

|#FFF2DF|Controlador de Historial|
:Inyecta identificador de usuario y contexto de autorización;

|#E8F8F5|Base de Datos PostgreSQL (RLS)|
:Ejecuta consulta filtrada por Row Level Security (auth.uid());
note right: **Filtro RLS Activo:**\nSolo registros vinculados\nal usuario autenticado

if (¿Existen registros históricos asociados?) then (No: Primer ingreso)
    |UI Tablero Historial|
    :Renderiza vista de estado vacío (*Empty State*);
    note right: **Objeto: PantallaEstadoVacioDTO**\n[Estado: RENDERIZADO]
    stop
else (Sí: Datos encontrados)
    |#FFF2DF|Controlador de Historial|
    :Agrupa registros por semestre y calcula indicadores:\n- Total sesiones cursadas\n- Horas pedagógicas acumuladas\n- Tasa porcentual de asistencia efectiva;
    
    |#E8F4F8|UI Tablero Historial|
    :Construye matriz de datos con badges de estado;
    note right: **Objeto: ColeccionHistorialDTO**\n[Estado: ESTRUCTURADO]
    
    :Despliega tabla paginada con filtros por ciclo y materia;
    
    |#E9ECEF|Usuario Institucional|
    :Aplica filtro por asignatura o semestre lectivo;
    :Selecciona una sesión específica para examinar;
    
    |#FFF2DF|Controlador de Historial|
    :Recupera bitácora pedagógica y enlaces de materiales;
    
    |#E8F4F8|UI Tablero Historial|
    :Despliega panel lateral (*Drawer*) con contenido temático;
    note right: **Objeto: DetalleBitacoraDTO**\n[Estado: CARGADO]
    
    |#E9ECEF|Usuario Institucional|
    :Visualiza temas silábicos cubiertos y acuerdos pedagógicos;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos formaliza la trazabilidad del expediente pedagógico individual. La interposición de directivas RLS a nivel de motor de datos garantiza que el objeto `ColeccionHistorialDTO` solo incorpore participaciones atribuibles al usuario en sesión, impidiendo fugas de datos de asistencia de otros alumnos (Ley N° 29733). La bifurcación hacia `PantallaEstadoVacioDTO` guía amigablemente a los estudiantes nóveles, mientras que la recuperación desacoplada de `DetalleBitacoraDTO` provee una navegación fluida que optimiza el consumo de memoria en la interfaz SPA.

### 6.3.2.12. CUS16 - Actividades con Objetos: Consultar Tablero de Insignias y Reputación

El diagrama de actividades con flujo de objetos detalla el procesamiento analítico, el cálculo algorítmico de la reputación docente según la regla RN-13 y la auditoría automática de insignias formativas. Se modelan cuatro carriles (*swimlanes*): el *Mentor Académico / Mentoreado*, la *UI Tablero Gamificación*, el *Controlador de Gamificación* y la *Base de Datos PostgreSQL (RLS)*. En el flujo se explicitan los objetos instanciados en tiempo de ejecución: `TableroCalibracionDTO` (para mentores iniciales sin evaluaciones), `EvaluacionesConsolidadasDTO` (con el score ponderado computado), `InsigniaOtorgada` (persistida ante el cumplimiento de nuevos umbrales), `TableroGamificacionDTO` (objeto compuesto de visualización) y `CredencialInsigniaDTO` (generado al compartir insignias externamente).

#### Diagrama 6.14.12: Diagrama de Actividades con Flujo de Objetos - CUS16: Consultar Tablero de Insignias y Reputación

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS16: Consultar Tablero de Insignias y Reputación\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Mentor Académico / Mentoreado|
|#E8F4F8|UI Tablero Gamificación|
|#FFF2DF|Controlador de Gamificación|
|#E8F8F5|Base de Datos PostgreSQL (RLS)|

|#E9ECEF|Mentor Académico / Mentoreado|
start
:Selecciona sección "Mi Reputación & Reconocimientos"\n(o visualiza ficha pública del mentor al reservar);

|#E8F4F8|UI Tablero Gamificación|
:Emite solicitud HTTP GET /gamificacion/tablero/{idMentor}\nadjuntando Bearer Token JWT institucional;

|#FFF2DF|Controlador de Gamificación|
:Verifica alcance de la consulta\n(Ámbito privado de mentor vs. Vista pública resumida);

|#E8F8F5|Base de Datos PostgreSQL (RLS)|
:Ejecuta consulta consolidada:\n- Promedios de encuestas Likert (CUS05)\n- Tasa de cumplimiento de sesiones (CUS09/CUS07)\n- Auditoría de puntualidad de bitácoras (CUS10)\n- Historial de insignias otorgadas;
:Retorna filas agregadas y métricas del mentor;

|#FFF2DF|Controlador de Gamificación|
if (¿Cuenta con evaluaciones históricas registradas?) then (No: Mentor novel / E01)
    :Genera estado preliminar de calibración docente;
    
    |#E8F4F8|UI Tablero Gamificación|
    :Despliega banner motivacional: "Score en Calibración";
    note right: **Objeto: TableroCalibracionDTO**\n[Estado: EN_CALIBRACION]
    
    |#E9ECEF|Mentor Académico / Mentoreado|
    :Visualiza mensaje formativo y metas para activación;
    stop
else (Sí: Datos evaluativos disponibles)
    |#FFF2DF|Controlador de Gamificación|
    :Aplica fórmula de reputación ponderada (RN-13):\nScore = 70% Encuestas + 20% Cumplimiento + 10% Puntualidad;
    note right: **Objeto: EvaluacionesConsolidadasDTO**\n[Estado: COMPUTADO]
    
    :Evalúa reglas y umbrales de desbloqueo de insignias\n(Hito horas dictadas, racha 5 estrellas, quórum pleno);
    
    if (¿Supera nuevos umbrales normativos?) then (Sí)
        |#E8F8F5|Base de Datos PostgreSQL (RLS)|
        :Inserta nuevo registro con hash de integridad;
        note right: **Objeto: InsigniaOtorgada**\n[Estado: RECIEN_DESBLOQUEADA]
    else (No)
        |#FFF2DF|Controlador de Gamificación|
        :Calcula porcentaje de avance restante hacia próximas metas;
    endif
    
    |#FFF2DF|Controlador de Gamificación|
    if (¿Es consulta de perfil público por alumno? / FA01) then (Sí)
        :Sintetiza vista pública: filtra analíticas privadas de horas;
    else (No: Vista privada del mentor)
        :Incorpora comentarios estudiantiles anonimizados (Ley 29733);
    endif
    
    :Compone estructura completa para la vista;
    
    |#E8F4F8|UI Tablero Gamificación|
    :Renderiza tablero interactivo:\n- Velocímetro de score global y nivel (Destacado/Senior)\n- Radar de satisfacción por reactivo Likert\n- Cards de insignias activas y barras de progreso\n- Feed de comentarios formativos disociados;
    note right: **Objeto: TableroGamificacionDTO**\n[Estado: RENDERIZADO_CONSOLIDADO]
    
    |#E9ECEF|Mentor Académico / Mentoreado|
    if (¿Desea compartir insignia en red externa? / FA02) then (Sí)
        :Hace clic en "Compartir Insignia" en una card;
        
        |#FFF2DF|Controlador de Gamificación|
        :Genera URL pública firmada con hash criptográfico SHA-256;
        
        |#E8F4F8|UI Tablero Gamificación|
        :Presenta modal con enlace verificable y código QR;
        note right: **Objeto: CredencialInsigniaDTO**\n[Estado: FIRMADA_SHA256]
        
        |#E9ECEF|Mentor Académico / Mentoreado|
        :Copia enlace para portafolio profesional;
    else (No)
    endif
    
    :Concluye navegación del tablero;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos de CUS16 modela con exactitud la lógica lúdica y meritocrática de la EPIS-UPT. La evaluación condicional inicial segrega a los mentores noveles mediante `TableroCalibracionDTO`, evitando penalizaciones tempranas artificiales. La orquestación del cálculo de la regla RN-13 se articula transparentemente con el motor de insignias, permitiendo que la transición a `InsigniaOtorgada` ocurra de manera determinística y atómica. Finalmente, la bifurcación hacia `CredencialInsigniaDTO` asegura que los logros académicos gocen de fe pública digital externa respaldada por firmas hash SHA-256 sin comprometer el aislamiento de las métricas privadas.

### 6.3.2.13. CUS13 - Actividades con Objetos: Parametrizar y Emitir Certificados

El diagrama de actividades con flujo de objetos modela el procedimiento administrativo, la verificación de suficiencia pedagógica y la generación criptográfica de certificados de mentoría. Se estructuran cinco carriles (*swimlanes*): el *Administrador Institucional*, la *UI Gestión Certificados*, el *Controlador de Certificación*, la *Base de Datos PostgreSQL (RLS)* y el *Servicio Criptográfico PDF y SMTP*. Se destacan las transformaciones de estado de los artefactos: `ParametrosAcreditacionDTO` (definido por el usuario gestor), `NominaElegiblesDTO` (filtrado tras la auditoría relacional de bitácoras visadas), `OrdenEmisionBatchDTO` (aprobado en el modal ejecutivo), `DocumentoCertificadoPDFA` (sellado con hash SHA-256 y código QR) y `NotificacionAcreditacionDTO` (despachada al buzón institucional).

#### Diagrama 6.14.13: Diagrama de Actividades con Flujo de Objetos - CUS13: Parametrizar y Emitir Certificados

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS13: Parametrizar y Emitir Certificados\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Administrador Institucional|
|#E8F4F8|UI Gestión Certificados|
|#FFF2DF|Controlador de Certificación|
|#E8F8F5|Base de Datos PostgreSQL (RLS)|
|#F4ECF7|Servicio Criptográfico PDF y SMTP|

|#E9ECEF|Administrador Institucional|
start
:Accede a "Certificación Académica de Mentores";
:Configura parámetros semestrales:\n- Semestre activo (ej. 2026-I)\n- Umbral de horas mínimas (RN-14: $\ge 30\text{ h}$)\n- Calificación mínima de reputación ($\ge 4.0$);

|#E8F4F8|UI Gestión Certificados|
:Captura formulario institucional;
note right: **Objeto: ParametrosAcreditacionDTO**\n[Estado: REGISTRADO]

:Emite solicitud de auditoría de candidatos\nPOST /certificados/parametros/evaluar-elegibles;

|#FFF2DF|Controlador de Certificación|
:Valida consistencia de los umbrales configurados;

|#E8F8F5|Base de Datos PostgreSQL (RLS)|
:Ejecuta consulta analítica con agregación:\n- Sumatoria de horas en bitácoras con estado 'VISADA'\n- Score consolidado en reputacion_mentores\n- Historial de sanciones o amonestaciones;
:Retorna consolidado de mentores calificados;

|#FFF2DF|Controlador de Certificación|
if (¿Existen mentores que cumplan los criterios?) then (No / E01)
    |#E8F4F8|UI Gestión Certificados|
    :Muestra alerta: "No se encontraron candidatos que cumplan el umbral";
    
    |#E9ECEF|Administrador Institucional|
    :Reevalúa parámetros o reprograma emisión;
    stop
else (Sí: Candidatos identificados)
    |#FFF2DF|Controlador de Certificación|
    :Estructura padrón con horas acreditadas y materias;
    
    |#E8F4F8|UI Gestión Certificados|
    :Renderiza grilla de candidatos con checkboxes de selección;
    note right: **Objeto: NominaElegiblesDTO**\n[Estado: FILTRADO_RN14]
    
    |#E9ECEF|Administrador Institucional|
    :Revisa nómina y desmarca casos con observación administrativa;
    :Presiona "Proceder a la Emisión de Certificados";
    
    |#E8F4F8|UI Gestión Certificados|
    :Abre modal de confirmación indicando cantidad de lotes;
    
    |#E9ECEF|Administrador Institucional|
    :Ratifica orden de emisión institucional;
    
    |#E8F4F8|UI Gestión Certificados|
    :Envía orden batch definitiva;
    note right: **Objeto: OrdenEmisionBatchDTO**\n[Estado: RATIFICADO]
    
    |#FFF2DF|Controlador de Certificación|
    :Inicia ciclo de generación batch transaccional;
    
    while (¿Quedan mentores pendientes en la nómina?) is (Sí)
        |#FFF2DF|Controlador de Certificación|
        :Genera correlativo institucional único (CERT-EPIS-2026-I-XXXX);
        :Construye URL de validación pública institucional;
        
        |#F4ECF7|Servicio Criptográfico PDF y SMTP|
        :Renderiza documento oficial PDF/A con membrete UPT;
        :Inserta código QR dinámico que apunta al portal;
        :Computa huella criptográfica SHA-256 del documento;
        note right: **Objeto: DocumentoCertificadoPDFA**\n[Estado: SELLADO_SHA256]
        
        if (¿Renderizado y almacenamiento exitoso?) then (Sí)
            |#E8F8F5|Base de Datos PostgreSQL (RLS)|
            :Registra fila en tabla certificados con estado 'EMITIDO';
            :Actualiza bolsa_horas_mentor marcando horas certificadas;
            
            |#F4ECF7|Servicio Criptográfico PDF y SMTP|
            :Despacha notificación con aviso de acreditación al correo institucional;
            note right: **Objeto: NotificacionAcreditacionDTO**\n[Estado: DESPACHADA]
        else (No / E02)
            |#FFF2DF|Controlador de Certificación|
            :Registra error técnico en log de auditoría y continúa lote;
        endif
    endwhile (No: Fin de nómina)
    
    |#FFF2DF|Controlador de Certificación|
    :Consolida reporte de ejecución (exitosos vs. fallidos);
    
    |#E8F4F8|UI Gestión Certificados|
    :Despliega resumen: "Emisión completada con éxito";
    
    |#E9ECEF|Administrador Institucional|
    :Visualiza reporte ejecutivo y cierra sesión administrativa;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades de CUS13 modela la rigurosidad administrativa en la acreditación de mérito formativo. La consulta analítica preliminar vincula estrictamente las horas certificadas con bitácoras en estado `VISADA`, garantizando que ninguna sesión carente de visado por la Comisión de Tutoría compute para créditos extracurriculares (RN-12 y RN-14). El desacoplamiento del `Servicio Criptografico PDF y SMTP` permite que la inyección del código QR y el cálculo del hash SHA-256 se efectúen de manera aislada y resiliente ante posibles excepciones de red, persistiendo el certificado con fe pública institucional inalterable.

### 6.3.2.14. CUS09 - Actividades con Objetos: Descargar Certificado de Horas de Mentoría

El diagrama de actividades con flujo de objetos formaliza la navegación interactiva, la validación de integridad criptográfica y los canales de consulta de fe pública correspondientes a las certificaciones institucionales de la EPIS-UPT. Se distribuyen las responsabilidades en cinco carriles (*swimlanes*): el *Mentor Académico / Verificador*, la *UI Portal P2P (Privado/Público)*, el *Controlador de Certificados*, la *Base de Datos PostgreSQL (RLS)* y el *Almacenamiento Seguro (Bucket Storage)*. Se destacan los artefactos y sus transiciones de estado: `ListaCertificadosMentorDTO` (expedientes disponibles), `AlertaSinCertificadoDTO` (notificación de avance de horas en curso), `StreamBinarioPDFA` (documento inalterable transmitido) y `FichaVerificacionPublicaDTO` (sello verde de autenticidad emitido ante el escaneo de código QR).

#### Diagrama 6.14.14: Diagrama de Actividades con Flujo de Objetos - CUS09: Descargar Certificado de Horas de Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS09: Descargar Certificado de Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Mentor Académico / Verificador|
|#E8F4F8|UI Portal P2P (Privado/Público)|
|#FFF2DF|Controlador de Certificados|
|#E8F8F5|Base de Datos PostgreSQL (RLS)|
|#F4ECF7|Almacenamiento Seguro (Bucket Storage)|

|#E9ECEF|Mentor Académico / Verificador|
start
if (¿Canal de interacción del actor?) then (Mentor: Descarga de constancia privada)
    :Accede a la sección "Mis Certificados Oficiales";
    
    |#E8F4F8|UI Portal P2P (Privado/Público)|
    :Emite solicitud HTTP GET /api/v1/certificados/mis-certificados\ncon Bearer Token JWT;
    
    |#FFF2DF|Controlador de Certificados|
    :Aplica directiva de seguridad por usuario autenticado;
    
    |#E8F8F5|Base de Datos PostgreSQL (RLS)|
    :SELECT * FROM certificados WHERE id_mentor = auth.uid();
    :Retorna registros de certificados emitidos;
    
    |#FFF2DF|Controlador de Certificados|
    if (¿Cuenta con certificados emitidos en el ciclo?) then (No / E01)
        :Construye estado de progreso con saldo de horas auditadas;
        
        |#E8F4F8|UI Portal P2P (Privado/Público)|
        :Despliega banner: "Certificado en trámite: Horas auditadas X / 30";
        note right: **Objeto: AlertaSinCertificadoDTO**\n[Estado: EN_CURSO]
        
        |#E9ECEF|Mentor Académico / Verificador|
        :Toma conocimiento de las horas faltantes;
        stop
    else (Sí: Certificados registrados)
        :Estructura catálogo de constancias con correlativos y metadatos;
        
        |#E8F4F8|UI Portal P2P (Privado/Público)|
        :Renderiza tarjetas de certificados con previsualización;
        note right: **Objeto: ListaCertificadosMentorDTO**\n[Estado: CARGADO]
        
        |#E9ECEF|Mentor Académico / Verificador|
        :Selecciona certificado semestral y pulsa "Descargar PDF";
        
        |#E8F4F8|UI Portal P2P (Privado/Público)|
        :Solicita stream binario GET /certificados/{id}/descargar;
        
        |#FFF2DF|Controlador de Certificados|
        :Recupera ruta de almacenamiento y hash SHA-256 esperado;
        
        |#F4ECF7|Almacenamiento Seguro (Bucket Storage)|
        :Lee binario de archivo oficial PDF/A;
        :Transmite bytes al controlador;
        
        |#FFF2DF|Controlador de Certificados|
        :Recalcula SHA-256 sobre los bytes y coteja con base de datos;
        
        if (¿Hash coincide exactamente?) then (Sí: Integridad confirmada)
            |#E8F4F8|UI Portal P2P (Privado/Público)|
            :Descarga documento en el navegador del estudiante;
            note right: **Objeto: StreamBinarioPDFA**\n[Estado: DESCARGADO_INALTERABLE]
            
            |#E9ECEF|Mentor Académico / Verificador|
            :Abre y valida su certificado foliado para créditos;
            stop
        else (No / E02: Inconsistencia o archivo dañado)
            |#E8F4F8|UI Portal P2P (Privado/Público)|
            :Bloquea transmisión y notifica error de integridad documental;
            stop
        endif
    endif

else (Tercero: Validación pública vía QR / FA01)
    |#E9ECEF|Mentor Académico / Verificador|
    :Escanea código QR impreso en el documento PDF/A;
    
    |#E8F4F8|UI Portal P2P (Privado/Público)|
    :Abre navegador en URL pública: /verificar/cert/{hashSha256};
    :Solicita ficha de validación institucional (sin login requerido);
    
    |#FFF2DF|Controlador de Certificados|
    :Consulta datos públicos del certificado por hash único;
    
    |#E8F8F5|Base de Datos PostgreSQL (RLS)|
    :SELECT c.codigo_correlativo, c.semestre, c.horas_totales,\n       c.fecha_emision, c.estado, u.nombres, u.apellidos\nFROM certificados c JOIN usuarios u ON c.id_mentor = u.id\nWHERE c.hash_sha256 = :hash;
    :Retorna registro oficial fidedigno;
    
    |#FFF2DF|Controlador de Certificados|
    :Compone respuesta con sello de fe pública institucional;
    
    |#E8F4F8|UI Portal P2P (Privado/Público)|
    :Presenta ficha con sello verde "DOCUMENTO AUTÉNTICO UPT";
    note right: **Objeto: FichaVerificacionPublicaDTO**\n[Estado: VERIFICADO_AUTENTICO]
    
    |#E9ECEF|Mentor Académico / Verificador|
    :Corrobora identidad del mentor y validez de las horas reconocidas;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos para CUS09 modela la convergencia entre la gestión documental privada y el servicio de fe pública digital. En el carril del mentor, la verificación del hash SHA-256 previa a la entrega de `StreamBinarioPDFA` garantiza que ningún documento comprometido o desactualizado sea descargado, blindando la integridad probatoria exigida por Sunedu y la UPT. En el carril de terceros, la atención desatendida mediante el código QR proyecta `FichaVerificacionPublicaDTO` sin fricciones de autenticación, permitiendo a empleadores y comisiones evaluadoras cotejar la autenticidad del documento en tiempo real y con costo de procesamiento mínimo.

### 6.3.2.15. CUS22 - Actividades con Objetos: Auditar Bitácoras, Asistencia y Horas de Mentoría

El diagrama de actividades con flujo de objetos modela el procedimiento riguroso de fiscalización académica a cargo del Comité de Tutoría de la EPIS-UPT sobre las sesiones finalizadas. Se delimita la transición de estados de la bitácora docente (`REGISTRADA` -> `VISADA` u `OBSERVADA`), el cotejo inmutable de las firmas biométricas o asistencias validadas mediante QR, y el impacto transaccional en la bolsa de horas acumuladas del mentor académico conforme a las reglas `RN-12` (cómputo provisional supeditado al visado) y `RN-14` (requisito de visado oficial para certificación semestral).

#### Diagrama 6.14.15: Diagrama de Actividades con Flujo de Objetos - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
|#E8F4F8|UI Auditoría Docente\n(React SPA)|
|#FFF2DF|Controlador de Auditoría\ny Fiscalización|
|#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
|#FEF9E7|Servicio Notificaciones\nSMTP Institucional|

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
start
:Accede al módulo "Auditoría de Sesiones y Bitácoras";

|#E8F4F8|UI Auditoría Docente\n(React SPA)|
:Solicita bandeja de sesiones finalizadas pendientes de revisión;

|#FFF2DF|Controlador de Auditoría\ny Fiscalización|
:invocar listarSesionesPendientesVisado();

|#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
:SELECT b.*, s.tema, s.fecha_hora_inicio, u.nombres, u.apellidos\nFROM bitacoras_sesion b\nJOIN sesiones_mentoria s ON b.id_sesion = s.id\nJOIN usuarios u ON s.id_mentor = u.id\nWHERE b.estado = 'REGISTRADA' AND s.estado = 'FINALIZADA'\nORDER BY s.fecha_hora_fin ASC;
:Retorna filas de sesiones pendientes;

|#FFF2DF|Controlador de Auditoría\ny Fiscalización|
:Estructura lista y calcula métricas de quórum asistencial;

|#E8F4F8|UI Auditoría Docente\n(React SPA)|
:Renderiza grilla cronológica de auditoría;
note right: **Objeto: ListaBitacorasPendientesDTO**\n[Estado: PENDIENTE_AUDITORIA]

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
:Selecciona una sesión específica para auditar expediente;

|#E8F4F8|UI Auditoría Docente\n(React SPA)|
:Dispara solicitud de expediente completo (idSesion);

|#FFF2DF|Controlador de Auditoría\ny Fiscalización|
:obtenerExpedienteDetallado(idSesion);

|#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
:SELECT * FROM bitacoras_sesion WHERE id_sesion = :idSesion;\nSELECT r.*, u.codigo_estudiante, u.nombres\nFROM reservas_cupo r JOIN usuarios u ON r.id_estudiante = u.id\nWHERE r.id_sesion = :idSesion AND r.asistio = TRUE;
:Entrega metadatos pedagógicos, evidencias y nómina QR;

|#FFF2DF|Controlador de Auditoría\ny Fiscalización|
:Valida consistencia entre aforo ratificado y firmas QR;
note right: **Objeto: ExpedienteAuditoriaDTO**\n[Estado: EN_EVALUACION_DOCENTE]

|#E8F4F8|UI Auditoría Docente\n(React SPA)|
:Despliega expediente analítico con visor de temas, evidencias y nómina;

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
:Examina contenidos, dificultades formativas y reporte de horas;

if (¿El contenido pedagógico y la nómina de asistencia cumplen los estándares normativos?) then (Sí: Dictamen Conforme)
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
    :Presiona botón "Visar y Aprobar Horas";
    
    |#E8F4F8|UI Auditoría Docente\n(React SPA)|
    :Envía solicitud POST /api/v1/auditoria/bitacoras/{id}/visar;
    
    |#FFF2DF|Controlador de Auditoría\ny Fiscalización|
    :procesarVisadoBitacora(idBitacora, idAuditor);
    
    |#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
    :BEGIN TRANSACTION;\nUPDATE bitacoras_sesion SET estado = 'VISADA',\n  id_auditor_visador = :idAuditor, fecha_visado = NOW()\nWHERE id = :idBitacora;\nUPDATE bolsas_horas_mentor\nSET horas_oficiales = horas_oficiales + :horasSesion,\n    horas_provisionales = horas_provisionales - :horasSesion\nWHERE id_mentor = :idMentor;\nINSERT INTO registros_auditoria_admin (accion, dictamen, id_entidad)\nVALUES ('VISADO_BITACORA', 'VISADO_APROBADO', :idBitacora);\nCOMMIT;
    note right: **Objeto: BitacoraSesion**\n[Estado: VISADA]\n**Objeto: BolsaHorasMentor**\n[Estado: HORAS_OFICIALES_ACREDITADAS]
    
    |#FFF2DF|Controlador de Auditoría\ny Fiscalización|
    :Retorna confirmación de visado oficial;
    
    |#E8F4F8|UI Auditoría Docente\n(React SPA)|
    :Presenta distintivo verde "SESIÓN VISADA Y HORAS OFICIALIZADAS";
    :Actualiza lista removiendo ítem auditado;
    
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
    :Verifica acreditación exitosa en el libro de horas docentes;
    stop
else (No: Inconsistencia Detectada - FA01)
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
    :Presiona "Observar Bitácora por Inconsistencia";
    
    |#E8F4F8|UI Auditoría Docente\n(React SPA)|
    :Despliega modal interactivo de emisión de pliego de cargos;
    
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
    :Tipifica motivo (asistencia no fehaciente, falta evidencia);\nRedacta pliego detallado de observaciones y confirma plazo 48h;
    
    |#E8F4F8|UI Auditoría Docente\n(React SPA)|
    :Envía POST /api/v1/auditoria/bitacoras/{id}/observar con pliego;
    
    |#FFF2DF|Controlador de Auditoría\ny Fiscalización|
    :registrarObservacionBitacora(idBitacora, pliego, 48h);
    
    |#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
    :BEGIN TRANSACTION;\nUPDATE bitacoras_sesion SET estado = 'OBSERVADA',\n  fecha_observacion = NOW() WHERE id = :idBitacora;\nINSERT INTO observaciones_bitacora (id_bitacora, pliego, limite_48h)\nVALUES (:idBitacora, :pliego, NOW() + INTERVAL '48 HOURS');\nINSERT INTO registros_auditoria_admin (accion, dictamen, id_entidad)\nVALUES ('OBSERVACION_BITACORA', 'OBSERVACION_EMITIDA', :idBitacora);\nCOMMIT;
    note right: **Objeto: BitacoraSesion**\n[Estado: OBSERVADA]\n**Objeto: ObservacionBitacora**\n[Estado: EMITIDA_PENDIENTE_SUBSANACION]
    
    |#FFF2DF|Controlador de Auditoría\ny Fiscalización|
    :Dispara evento asíncrono de alerta urgente docente;
    
    |#FEF9E7|Servicio Notificaciones\nSMTP Institucional|
    :Despacha correo institucional al mentor con pliego de cargos\ny cuenta regresiva perentoria de 48 horas;
    note right: **Objeto: NotificacionDocenteDTO**\n[Estado: NOTIFICACION_DESPACHADA]
    
    |#E8F4F8|UI Auditoría Docente\n(React SPA)|
    :Despliega ficha de sesión con sello ámbar "EN OBSERVACIÓN (48H)";
    :Informa remisión formal del pliego de cargos;
    
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Auditor)|
    :Constata pase a custodia temporal y espera de descargos;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El diagrama de actividades con flujo de objetos de CUS22 formaliza el rigor de control administrativo y metodológico en la EPIS-UPT. La evaluación por el Comité de Tutoría garantiza que ninguna hora sea computada hacia la certificación final sin superar el filtro del expediente completo (`ExpedienteAuditoriaDTO`). La bifurcación transaccional asegura el cumplimiento de `RN-12` y `RN-14`: el visado promueve las horas a la categoría oficial de manera atómica, mientras que la emisión de observaciones congela provisionalmente el saldo docente y activa el protocolo de subsanación con plazo perentorio de 48 horas mediante correo institucional SMTP, salvaguardando la fe pública universitaria.

### 6.3.2.16. CUS12 - Actividades con Objetos: Destacar Mentorías Prioritarias

El diagrama de actividades con flujo de objetos modela el procedimiento operacional de priorización académica institucional a cargo de la Dirección EPIS y el Comité de Tutoría (`RF24`, `RN-11`). Se representa la evaluación de métricas de reprobación, la parametrización de campañas de refuerzo pedagógico con validación de factores multiplicadores algorítmicos ($\alpha \in [1.05, 1.50]$), la actualización atómica del estado curricular en base de datos, la purga de caché en Redis y la consecuente reponderación de ofertas con distintivo de fe pública en el motor de recomendación.

#### Diagrama 6.14.16: Diagrama de Actividades con Flujo de Objetos - CUS12: Destacar Mentorías Prioritarias

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS12: Destacar Mentorías Prioritarias\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
|#E8F4F8|UI Gestión Prioridades\n(React SPA)|
|#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
|#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
|#FEF9E7|Motor Recomendación\ny Caché Redis (RN-11)|

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
start
:Accede a "Gestión de Prioridades Académicas";

|#E8F4F8|UI Gestión Prioridades\n(React SPA)|
:Solicita asignaturas con índices de reprobación y demanda formativa;

|#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
:invocar obtenerEstadisticasRendimientoCurricular();

|#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
:SELECT a.id, a.codigo, a.nombre, a.ciclo,\n       m.tasa_reprobacion, m.total_estudiantes_en_riesgo,\n       p.id AS id_politica, p.estado AS estado_prioridad\nFROM asignaturas a\nLEFT JOIN metricas_rendimiento_academico m ON a.id = m.id_asignatura\nLEFT JOIN politicas_prioridad_asignatura p ON a.id = p.id_asignatura AND p.estado = 'ACTIVA';
:Retorna consolidado académico;

|#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
:Estructura semáforo de riesgo formativo (>30% crítico);

|#E8F4F8|UI Gestión Prioridades\n(React SPA)|
:Renderiza tablero analítico de priorización;
note right: **Objeto: ListaAsignaturasRendimientoDTO**\n[Estado: CARGADA_CON_ESTADISTICAS]

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
:Selecciona asignatura neurálgica (ej. Cálculo II / Algoritmos);\nAbre modal "Configurar Campaña de Refuerzo Prioritario";

|#E8F4F8|UI Gestión Prioridades\n(React SPA)|
:Despliega formulario de parametrización institucional;

|#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
:Define vigencia (fechaInicio, fechaFin);\nIngresa factor de bonificación algorítmica alfa (ej. 1.25, RN-11);\nRedacta resolución y motivo institucional;

if (¿Parámetros válidos? (fechas coherentes y 1.05 <= alfa <= 1.50)) then (No: Error de Validación - E01/E02)
    |#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
    :Rechaza solicitud con código de error de negocio;
    
    |#E8F4F8|UI Gestión Prioridades\n(React SPA)|
    :Resalta campos observados y alerta: "El factor debe estar entre 1.05 y 1.50";
    
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
    :Corrige valores en el formulario;
    stop
else (Sí: Conforme a Directiva RN-11)
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
    :Presiona "Guardar y Activar Prioridad Institucional";
    
    |#E8F4F8|UI Gestión Prioridades\n(React SPA)|
    :Envía POST /api/v1/prioridades/activar {idAsignatura, vigencia, alfa=1.25};
    
    |#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
    :procesarActivacionPolitica(idAsignatura, payload, idAdmin);
    
    |#E8F8F5|Base de Datos PostgreSQL\n(RLS / ACID)|
    :BEGIN TRANSACTION;\nINSERT INTO politicas_prioridad_asignatura\n  (id_asignatura, factor_alfa, fecha_inicio, fecha_fin, resolucion, estado)\nVALUES (:idAsignatura, :alfa, :inicio, :fin, :resolucion, 'ACTIVA');\nUPDATE asignaturas SET es_prioritaria = TRUE WHERE id = :idAsignatura;\nINSERT INTO registros_auditoria_admin (accion, entidad, detalle)\nVALUES ('ACTIVAR_PRIORIDAD', 'asignaturas', :auditInfo);\nCOMMIT;
    note right: **Objeto: PoliticaPrioridadCurricular**\n[Estado: ACTIVA_VIGENTE]\n**Objeto: Asignatura**\n[Estado: PRIORITARIA_EPIS]
    
    |#FFF2DF|Controlador de Prioridades\ny Políticas Curriculares|
    :Emite orden de purga de caché y reponderación;
    
    |#FEF9E7|Motor Recomendación\ny Caché Redis (RN-11)|
    :Elimina claves precalculadas: DEL cache:recomendaciones:*;\nInvalida matrices de afinidad;\nAplica multiplicador alfa = 1.25 a las ofertas de la materia;
    note right: **Objeto: CatalogoOfertas**\n[Estado: REORDENADO_CON_BADGES_DORADOS]
    
    |#E8F4F8|UI Gestión Prioridades\n(React SPA)|
    :Presenta insignia dorada "PRIORIDAD EPIS ACTIVADA";
    :Actualiza estado en la grilla directiva;
    
    |#E9ECEF|Administrador Institucional\n(Comité de Tutoría / Dirección)|
    :Verifica despliegue exitoso de la campaña de refuerzo;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El flujo de actividades con objetos para CUS12 articula la intervención directiva sobre el ecosistema formativo entre pares. Al condicionar la persistencia de `PoliticaPrioridadCurricular` a los márgenes normativos de `RN-11` ($1.05 \le \alpha \le 1.50$), el sistema previene distorsiones algorítmicas extremas en las recomendaciones personalizadas. La invalidación inmediata de caché en Redis garantiza que las ofertas asociadas adquieran prelación en el ranking y ostenten el distintivo institucional en tiempo real, maximizando la captación de mentoreados en las materias con mayores brechas de aprobación.

### 6.3.2.17. CUS14 - Actividades con Objetos: Visualizar Tablero de Analíticas Institucionales

El diagrama de actividades con flujo de objetos modela el procesamiento analítico y la gobernanza de datos académicos en la EPIS-UPT (`RF25`). Se representa la agregación de indicadores clave de rendimiento (KPIs), la proyección interactiva del cuadro de mando gerencial, y la ramificación de exportación documental que segrega la generación ejecutiva de informes foliados en PDF de la disociación criptográfica de identidades en datasets CSV para investigación educativa, garantizando el cumplimiento de `RN-13` y la Ley N° 29733.

#### Diagrama 6.14.17: Diagrama de Actividades con Flujo de Objetos - CUS14: Visualizar Tablero de Analíticas Institucionales

```plantuml
@startuml
title Diagrama de Actividades con Flujo de Objetos - CUS14: Visualizar Tablero de Analíticas Institucionales\nSistema Web P2P - EPIS UPT

skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

|#E9ECEF|Administrador Institucional / Investigador|
|#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
|#FFF2DF|Controlador de Analítica\ny Reportes|
|#E8F8F5|Base de Datos PostgreSQL\n(OLAP / RLS)|
|#FEF9E7|Servicio Anonimización\ny Exportación|

|#E9ECEF|Administrador Institucional / Investigador|
start
:Accede a "Tablero de Analítica Institucional";

|#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
:Solicita consolidado semestral de rendimiento y tutorías;

|#FFF2DF|Controlador de Analítica\ny Reportes|
:invocar obtenerCuadroMandoIntegral(semestreActivo);

|#E8F8F5|Base de Datos PostgreSQL\n(OLAP / RLS)|
:SELECT COUNT(DISTINCT s.id) AS total_sesiones,\n       ROUND(AVG(CASE WHEN s.estado = 'CONFIRMADA' THEN 1 ELSE 0 END)*100, 2) AS tasa_quorum,\n       ROUND(AVG(CASE WHEN r.asistio = TRUE THEN 1 ELSE 0 END)*100, 2) AS tasa_asistencia_real,\n       ROUND(AVG(e.puntaje_general), 2) AS satisfaccion_promedio\nFROM sesiones_mentoria s\nLEFT JOIN reservas_cupo r ON s.id = r.id_sesion\nLEFT JOIN encuestas_calidad e ON s.id = e.id_sesion;
:Retorna cubos agregados de métricas formativas;

|#FFF2DF|Controlador de Analítica\ny Reportes|
:Calcula mapas de calor de demanda insatisfecha por materia;
note right: **Objeto: KpiInstitucionalAcademico**\n[Estado: CALCULADO_CICLO_ACTIVO]

|#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
:Renderiza widgets dinámicos, gráficos de dispersión y KPIs;\nDespliega botones de filtrado y exportación institucional;
note right: **Objeto: TableroMandoDTO**\n[Estado: PROYECTADO_EN_PANTALLA]

|#E9ECEF|Administrador Institucional / Investigador|
:Aplica filtros analíticos y selecciona opción de exportación;

if (¿Modalidad de exportación requerida?) then (Informe Ejecutivo para Consejo de Facultad)
    |#E9ECEF|Administrador Institucional / Investigador|
    :Presiona botón "Exportar Informe Ejecutivo (PDF)";
    
    |#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
    :Envía solicitud GET /api/v1/analitica/exportar/pdf?semestre=2026-I;
    
    |#FFF2DF|Controlador de Analítica\ny Reportes|
    :compilarDossierEjecutivo(kpisFiltrados);
    
    |#FEF9E7|Servicio Anonimización\ny Exportación|
    :Ensambla documento formal PDF con membrete EPIS,\ngráficos de alta resolución y resumen ejecutivo;
    note right: **Objeto: DossierEjecutivoPDF**\n[Estado: GENERADO_ALTA_RESOLUCION]
    
    |#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
    :Dispara descarga directa del archivo PDF;
    
    |#E9ECEF|Administrador Institucional / Investigador|
    :Guarda dossier para sustentación ante Consejo de Facultad;
    stop
else (Dataset de Investigación - FA02 / RN-13)
    |#E9ECEF|Administrador Institucional / Investigador|
    :Presiona "Exportar Dataset Anonimizado (CSV)";
    
    |#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
    :Envía solicitud GET /api/v1/analitica/exportar/dataset-investigacion;
    
    |#FFF2DF|Controlador de Analítica\ny Reportes|
    :extraerRegistrosHistoricosCrudos();
    
    |#FEF9E7|Servicio Anonimización\ny Exportación|
    :Aplica hash SHA-256 irreversible sobre identidades de usuarios;\nEnmascara códigos de matrícula y suprime datos sensibles (Ley N° 29733);\nGenera estructura tabular CSV con identificadores seudoanonimizados;
    note right: **Objeto: DatasetMentoriasAnonimizadoCSV**\n[Estado: PSEUDOANONIMIZADO_SEGURO]
    
    |#E8F8F5|Base de Datos PostgreSQL\n(OLAP / RLS)|
    :INSERT INTO registros_auditoria_admin (accion, entidad, detalle)\nVALUES ('EXPORTAR_DATASET_ANONIMO', 'analitica', :metaAudit);
    
    |#E8F4F8|UI Tablero Ejecutivo\n(React SPA)|
    :Entrega archivo comprimido CSV para descarga;
    
    |#E9ECEF|Administrador Institucional / Investigador|
    :Almacena dataset protegido para minería de datos académicos;
    stop
endif
@enduml
```

Fuente: Elaboración propia.

El diagrama de actividades con flujo de objetos de CUS14 formaliza el ecosistema de inteligencia de negocios de la EPIS-UPT. La derivación hacia vistas analíticas agregadas protege el rendimiento transaccional del motor relacional PostgreSQL, permitiendo a la Dirección monitorear en tiempo real el impacto de las mentorías y los cuellos de botella formativos (`TableroMandoDTO`). La segregación entre reportes ejecutivos consolidados y datasets de investigación disociados garantiza el estricto cumplimiento de `RN-13`, asegurando que la analítica descriptiva y predictiva de la facultad se desarrolle bajo los más elevados estándares de privacidad y ética en el tratamiento de datos estudiantiles.

---

## 6.3.3. Diagrama de Secuencia

### Presentación del Diagrama de Secuencia
El diagrama de secuencia describe el orden cronológico estricto de los mensajes, llamadas de métodos e interacciones asíncronas entre los componentes del sistema para ejecutar el proceso más complejo de la plataforma: la **orquestación concurrente de Reserva de Cupos, Ratificación y Corte Automatizado de Quórum con Notificación**. Se representan los participantes distribuidos: el *Mentoreado*, el *Frontend SPA*, la *API Backend FastAPI*, la *Base de Datos PostgreSQL (Supabase)*, el *Demonio Cron Backend*, el *Servicio de Correo SMTP* y el *Mentor*.

A continuación, se detalla el diagrama de secuencia analítico.

### Diagrama 6.15: Diagrama de Secuencia del Ciclo de Reserva, Ratificación y Quórum

```plantuml
@startuml
title Diagrama de Secuencia: Reserva, Ratificación y Evaluación de Quórum en T-24h\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Mentoreado" as User
participant "Frontend SPA\n(React/TypeScript)" as UI
participant "API Backend\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Demonio Cron\n(Celery/APScheduler)" as Cron
participant "Servicio Email\n(SMTP UPT)" as Mail
actor "Mentor" as Mentor

== 1. Reserva de Cupo (CUS04) ==
User -> UI: Clic en "Reservar Cupo" (idSesion)
UI -> API: POST /api/v1/reservas {idSesion} [Bearer JWT]
activate API
API -> DB: BEGIN TRANSACTION
API -> DB: SELECT * FROM sesion_mentoria WHERE id = idSesion FOR UPDATE
DB --> API: Registro Sesion (aforo, cupos_ocupados)
alt Cupos disponibles > 0 y ElegibilidadValidada
    API -> DB: INSERT INTO reserva (id_usuario, id_sesion, estado='PENDIENTE_CONFIRMACION')
    API -> DB: UPDATE sesion_mentoria SET cupos_ocupados = cupos_ocupados + 1
    API -> DB: COMMIT
    API --> UI: HTTP 201 Created {idReserva, estado: 'PENDIENTE_CONFIRMACION'}
    UI --> User: Muestra confirmación y plazo hasta T-24h
else Conflicto de aforo o estudiante no elegible
    API -> DB: ROLLBACK
    API --> UI: HTTP 409 Conflict {error: "Aforo agotado o no cumple elegibilidad"}
    UI --> User: Alerta de denegación de reserva
end
deactivate API

== 2. Ratificación de Asistencia antes de T-24h (CUS24) ==
User -> UI: Clic en "Confirmar Asistencia" (idReserva)
UI -> API: PATCH /api/v1/reservas/{idReserva}/confirmar [Bearer JWT]
activate API
API -> DB: SELECT * FROM reserva r JOIN sesion_mentoria s ON r.id_sesion = s.id WHERE r.id = idReserva
DB --> API: Datos Reserva y Sesión
alt Tiempo restante >= 24 horas (T >= 24h)
    API -> DB: UPDATE reserva SET estado = 'CONFIRMADA', fecha_confirmacion = NOW() WHERE id = idReserva
    API -> Mail: Despacha ticket digital con código QR de asistencia
    API --> UI: HTTP 200 OK {estado: 'CONFIRMADA', aula_o_link: 'Lab-01 / meet.google.com/...'}
    UI --> User: Despliega ticket digital y acceso formal
else Plazo cerrado (T < 24h)
    API --> UI: HTTP 400 Bad Request {error: "Plazo de confirmación vencido"}
    UI --> User: Informa revocación reglamentaria
end
deactivate API

== 3. Corte Automatizado y Cómputo de Quórum en T-24h (CUS23) ==
Cron -> API: Disparo automático de corte de quórum (sesiones a T=24h)
activate API
API -> DB: BEGIN TRANSACTION
API -> DB: UPDATE reserva SET estado = 'NO_CONFIRMADA' WHERE id_sesion = idSesion AND estado = 'PENDIENTE_CONFIRMACION'
API -> DB: SELECT COUNT(*) FROM reserva WHERE id_sesion = idSesion AND estado = 'CONFIRMADA'
DB --> API: N_confirmadas (ej. 6)
API -> DB: SELECT aforo_maximo FROM sesion_mentoria WHERE id = idSesion
DB --> API: Aforo_maximo (ej. 10)

alt N_confirmadas / Aforo_maximo >= 0.50 (Quórum >= 50%)
    API -> DB: UPDATE sesion_mentoria SET estado = 'CONFIRMADA' WHERE id = idSesion
    API -> DB: COMMIT
    API -> Mail: Notifica realización confirmada al Mentor y a Mentoreados
else Quórum < 50%
    API -> DB: UPDATE sesion_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = idSesion
    API -> DB: COMMIT
    API -> Mail: Envía alerta urgente de resolución a Mentor (CUS07)
    Mentor -> UI: Accede a panel de contingencia de sesión
    alt Mentor selecciona "Dictado Excepcional"
        Mentor -> UI: Clic "Aceptar Dictado Excepcional"
        UI -> API: PATCH /api/v1/sesiones/{idSesion}/resolver {accion: 'ACEPTAR_EXCEPCIONAL'}
        API -> DB: UPDATE sesion_mentoria SET estado = 'CONFIRMADA_EXCEPCIONAL'
        API -> Mail: Confirma dictado a los inscritos
    else Mentor selecciona "Cancelar por Quórum"
        Mentor -> UI: Clic "Cancelar sin Penalización"
        UI -> API: PATCH /api/v1/sesiones/{idSesion}/resolver {accion: 'CANCELAR'}
        API -> DB: UPDATE sesion_mentoria SET estado = 'CANCELADA_QUORUM'
        API -> Mail: Informa anulación solidaria a confirmados
    end
end
deactivate API
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia confirma la robustez técnica de la arquitectura de servicios:
1. **Garantía Transaccional ACID en Reservas:** El bloqueo pesimista `SELECT ... FOR UPDATE` sobre la fila de la oferta en PostgreSQL previene condiciones de carrera (*race conditions*) durante la reserva concurrente de los últimos cupos disponibles.
2. **Corte Perentorio Atómico:** El demonio programado actualiza a `NO_CONFIRMADA` las reservas omisas antes de evaluar el ratio matemático del 50%, asegurando que ningún participante sin ratificar sea contabilizado para el quórum.
3. **Asincronía en las Notificaciones:** Los despachos de correos electrónicos institucionales y generación de tickets QR se ejecutan de manera desacoplada, permitiendo que los tiempos de respuesta HTTP hacia la SPA se mantengan en el orden de los cientos de milisegundos.

### 6.3.3.1. CUS01 – Diagrama de Secuencia: Iniciar Sesión Institucional con 2FA

El diagrama de secuencia especifica la interacción temporal y el intercambio de mensajes sincrónicos y asíncronos entre los componentes distribuidos de la arquitectura para el caso de uso `CUS01`. Modela dos fases operativas rigurosas: la solicitud inicial de acceso y emisión del código de verificación temporal despachado vía SMTP (`Fase 1`); y la validación de la credencial efímera, la verificación y captura del consentimiento informado bajo la Ley N° 29733 y la entrega del token firmado JWT (`Fase 2`).

#### Diagrama 6.15.1: Diagrama de Secuencia - CUS01: Iniciar Sesión Institucional con 2FA

```plantuml
@startuml
title Diagrama de Secuencia - CUS01: Iniciar Sesión Institucional con 2FA\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional" as User
participant "Frontend SPA\n(React / Vite)" as UI
participant "API Gateway / Auth\n(FastAPI)" as API
participant "Servicio OTP" as OTP
participant "Servicio SMTP UPT" as SMTP
database "PostgreSQL DB\n(Supabase)" as DB
participant "Servicio JWT" as JWT

== Fase 1: Solicitud de Código de Acceso (OTP) ==
User -> UI: Ingresa correo institucional (@upt.pe)
UI -> API: POST /api/v1/auth/solicitar-otp {correo}
activate API

API -> DB: SELECT id, rol, activo, consentimiento FROM usuarios WHERE correo = :correo
activate DB
DB --> API: Registro de usuario (activo=true)
deactivate DB

alt Cuenta activa y dominio institucional válido
    API -> OTP: generarOTP(id_usuario)
    activate OTP
    OTP -> DB: INSERT INTO credenciales_otp (id_usuario, codigo_hash, expira_en) VALUES (...)
    OTP --> API: CodigoOTP_Plano (6 dígitos)
    deactivate OTP
    
    API -> SMTP: enviarCorreoOTP(correo, CodigoOTP_Plano)
    activate SMTP
    SMTP --> API: Despacho exitoso (HTTP 200 / SMTP OK)
    deactivate SMTP
    
    API --> UI: HTTP 200 OK {mensaje: "OTP despachado", expira_segundos: 300}
    UI --> User: Despliega formulario de ingreso con contador (5 min)
else Cuenta suspendida o dominio inválido
    API --> UI: HTTP 403 Forbidden {error: "Acceso no autorizado"}
    UI --> User: Muestra alerta de denegación institucional
end
deactivate API

== Fase 2: Validación de OTP y Consentimiento Legal ==
User -> UI: Ingresa código OTP de 6 dígitos
UI -> API: POST /api/v1/auth/verificar-otp {correo, codigo}
activate API

API -> OTP: validarCodigo(id_usuario, codigo)
activate OTP
OTP -> DB: SELECT * FROM credenciales_otp WHERE id_usuario = :id AND consumido = false
DB --> OTP: Registro OTP
OTP --> API: ValidacionExitosa (vigente < 5 min)
deactivate OTP

API -> DB: UPDATE credenciales_otp SET consumido = true WHERE id = :id_otp

alt Usuario no registra consentimiento (Primer Ingreso)
    API --> UI: HTTP 200 OK {requiere_consentimiento: true, token_temporal}
    UI --> User: Muestra modal obligatorio Ley N° 29733
    User -> UI: Marca casilla de aceptación y confirma
    UI -> API: POST /api/v1/auth/formalizar-consentimiento {token_temporal, aceptado: true}
    API -> DB: UPDATE usuarios SET consentimiento = true, fecha_consentimiento = NOW()
    API -> DB: INSERT INTO auditoria_consentimiento (id_usuario, ip, user_agent, timestamp) VALUES (...)
end

API -> JWT: generarTokenSesion(id_usuario, rol, expira=8h)
activate JWT
JWT --> API: TokenJWT_Firmado
deactivate JWT

API --> UI: HTTP 200 OK {access_token, token_type: "Bearer", rol}
deactivate API

UI --> User: Almacena sesión segura y redirige al Dashboard según Rol
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia confirma la segregación estricta de las fases de seguridad. En la Fase 1, la clave OTP generada aleatoriamente se transmite únicamente mediante el canal seguro SMTP institucional, persistiendo en base de datos únicamente su valor derivado mediante hash para neutralizar vectores de exposición por volcados de memoria. En la Fase 2, la invalidación inmediata de la credencial (`consumido = true`) mitiga ataques de reutilización (*replay attacks*), garantizando que la emisión del token JWT final ocurra exclusivamente tras validar la vigencia de la clave temporal y formalizar el consentimiento exigido por la Ley N° 29733.

### 6.3.3.2. CUS04 – Diagrama de Secuencia: Reservar Cupo de Mentoría

El diagrama de secuencia especifica la interacción cronológica y el intercambio de mensajes entre el navegador del estudiante (*Frontend SPA*), la capa de servicios (*API Gateway / Controller*), el validador de reglas académicas y la base de datos relacional (*PostgreSQL DB*) para procesar la reserva concurrente de vacantes. Se detallan las consultas de validación de perfil, la adquisición del bloqueo pesimista a nivel de fila (`SELECT ... FOR UPDATE`), la inserción atómica de la reserva en estado `PENDIENTE_CONFIRMACION` y la gestión de contingencias por aforo agotado o conflictos de agenda.

#### Diagrama 6.15.2: Diagrama de Secuencia - CUS04: Reservar Cupo de Mentoría

```plantuml
@startuml
title Diagrama de Secuencia - CUS04: Reservar Cupo de Mentoría\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as User
participant "Frontend SPA\n(React / Vite)" as UI
participant "API Gateway / Reservas\n(FastAPI)" as API
participant "Validador Elegibilidad\n(Service)" as Validador
database "PostgreSQL DB\n(Supabase / RLS)" as DB

== 1. Solicitud de Reserva y Validación de Elegibilidad ==
User -> UI: Clic en "Reservar Cupo" (idSesion)
UI -> API: POST /api/v1/reservas {idSesion} [Bearer JWT]
activate API

API -> Validador: verificarElegibilidad(idUsuario, idSesion)
activate Validador

Validador -> DB: SELECT ciclo_actual, activo FROM usuarios WHERE id = :idUsuario
activate DB
DB --> Validador: PerfilEstudiante (activo=true, ciclo=III)
deactivate DB

Validador -> DB: SELECT r.id FROM reservas r JOIN sesiones s ON r.id_sesion = s.id\nWHERE r.id_usuario = :idUsuario AND s.fecha_hora = :fechaSesion\nAND r.estado IN ('PENDIENTE_CONFIRMACION', 'CONFIRMADA')
activate DB
DB --> Validador: CrucesExistentes (0 registros)
deactivate DB

Validador --> API: ElegibilidadConfirmada
deactivate Validador

== 2. Transacción Atómica de Reserva con Bloqueo Pesimista ==
API -> DB: BEGIN TRANSACTION
activate DB
API -> DB: SELECT aforo_maximo, cupos_ocupados, estado FROM sesion_mentoria\nWHERE id = :idSesion FOR UPDATE
DB --> API: FilaSesionBloqueada (cupos_ocupados=7, aforo=10, estado='PUBLICADA')

alt Cupos disponibles (cupos_ocupados < aforo_maximo) [RN-05]
    API -> DB: INSERT INTO reservas (id_usuario, id_sesion, estado, fecha_reserva)\nVALUES (:idUsuario, :idSesion, 'PENDIENTE_CONFIRMACION', NOW())\nRETURNING id, fecha_reserva
    DB --> API: idReservaCreada (UUID)
    
    API -> DB: UPDATE sesion_mentoria SET cupos_ocupados = cupos_ocupados + 1\nWHERE id = :idSesion
    API -> DB: COMMIT
    deactivate DB
    
    API --> UI: HTTP 201 Created {idReserva, estado: 'PENDIENTE_CONFIRMACION', limite_t24}
    UI --> User: Despliega acuse de reserva exitosa y plazo de confirmación
else Aforo agotado en concurrencia (E01)
    activate DB
    API -> DB: ROLLBACK
    deactivate DB
    API --> UI: HTTP 409 Conflict {error: "Aforo agotado. No quedan cupos libres"}
    UI --> User: Alerta de aforo completo y opción de solicitud por demanda (CUS03)
end
deactivate API
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia confirma la solidez transaccional del proceso de reserva frente a escenarios de alta concurrencia. La consulta previa de elegibilidad verifica que el estudiante no mantenga inscripciones duplicadas ni solapamientos horarios en su agenda académica. Posteriormente, la ejecución de `BEGIN TRANSACTION` con `SELECT ... FOR UPDATE` sobre la fila de la sesión en PostgreSQL asegura la exclusión mutua, garantizando que el incremento de cupos y la creación de `ReservaCupo` ocurran de forma atómica sin riesgos de sobrecupo (RN-05).

### 6.3.3.3. CUS24 – Diagrama de Secuencia: Confirmar Asistencia a Mentoría

El diagrama de secuencia especifica la interacción cronológica y el intercambio de mensajes distribuido para ratificar formalmente la asistencia a una mentoría. Modela la recepción de la petición desde la SPA web, la comprobación matemática de la ventana perentoria de 24 horas en la base de datos (RN-08), la actualización atómica del estado a `CONFIRMADA`, la invocación al servicio criptográfico para construir el comprobante con código QR y el despacho asíncrono hacia el servidor SMTP de la UPT.

#### Diagrama 6.15.3: Diagrama de Secuencia - CUS24: Confirmar Asistencia a Mentoría

```plantuml
@startuml
title Diagrama de Secuencia - CUS24: Confirmar Asistencia a Mentoría\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as User
participant "Frontend SPA\n(React / Vite)" as UI
participant "API Gateway / Reservas\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Servicio Criptográfico QR" as QR
participant "Servicio SMTP UPT" as SMTP

User -> UI: Clic en "Confirmar Asistencia" (idReserva)
UI -> API: PATCH /api/v1/reservas/{idReserva}/confirmar [Bearer JWT]
activate API

API -> DB: SELECT r.id, r.estado, s.fecha_hora_inicio, s.modalidad, s.id_aula, s.enlace_virtual\nFROM reservas r JOIN sesiones_mentoria s ON r.id_sesion = s.id\nWHERE r.id = :idReserva AND r.id_usuario = :idUsuario
activate DB
DB --> API: DatosReservaYSesion (estado='PENDIENTE_CONFIRMACION')
deactivate DB

alt Tiempo restante >= 24 horas (T >= 24h) [RN-08]
    API -> DB: UPDATE reservas SET estado = 'CONFIRMADA', fecha_confirmacion = NOW()\nWHERE id = :idReserva
    activate DB
    DB --> API: UpdateOK
    deactivate DB
    
    API -> QR: generarTicketQR(idReserva, idUsuario, fechaSesion)
    activate QR
    QR --> API: PayloadTicket {codigo_hash, qr_base64}
    deactivate QR
    
    API -> SMTP: enviarCorreoTicket(correoUsuario, PayloadTicket)
    activate SMTP
    SMTP --> API: DespachoExitoso
    deactivate SMTP
    
    API --> UI: HTTP 200 OK {estado: 'CONFIRMADA', ticket: PayloadTicket, acceso: 'Lab-02 / meet.google.com/...'}
    UI --> User: Muestra ticket con código QR y detalles de infraestructura
else Plazo cerrado (T < 24h) [E01]
    API --> UI: HTTP 400 Bad Request {error: "Infracción RN-08: Plazo de confirmación vencido"}
    UI --> User: Notifica expiración de plazo y pérdida de la vacante
end
deactivate API
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza que la ratificación sea una operación atómica y estrictamente auditada. La verificación temporal contra el reloj del servidor descarta manipulaciones locales en el cliente, asegurando que la reserva solo transicione a `CONFIRMADA` si se cumple la antelación reglamentaria de 24 horas. La emisión del ticket con código QR y el despacho por correo institucional consolidan el medio probatorio digital para el posterior control de asistencia en la bitácora docente (CUS08).

### 6.3.3.4. CUS23 – Diagrama de Secuencia: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

El diagrama de secuencia detalla el intercambio cronológico y atómico de mensajes durante la ejecución desatendida del corte reglamentario en la ventana de 24 horas previas al inicio de la sesión. Modela el ciclo orquestado por el demonio cron (`Cron`), el servicio de evaluación de quórum (`Worker`), la base de datos relacional PostgreSQL con transacciones ACID, y el adaptador de mensajería SMTP institucional hacia el mentor y los estudiantes inscritos.

#### Diagrama 6.15.4: Diagrama de Secuencia - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

```plantuml
@startuml
title Diagrama de Secuencia - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

participant "Demonio Cron\n(Celery/APScheduler)" as Cron
participant "EvaluadorQuorumWorker\n(FastAPI Service)" as Worker
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Adaptador Email SMTP\n(UPT Mail)" as SMTP
actor "Mentor Asignado" as Mentor
actor "Mentoreado Confirmado" as Mentee

Cron -> Worker: ejecutarCorteQuorumT24()
activate Worker

Worker -> DB: BEGIN TRANSACTION
activate DB

Worker -> DB: SELECT id, id_mentor, aforo_maximo, modalidad, aula_o_enlace\nFROM sesiones_mentoria\nWHERE estado = 'PUBLICADA' AND fecha_hora_inicio <= NOW() + INTERVAL '24 hours' FOR UPDATE
DB --> Worker: ListaSesionesPorEvaluar

loop Por cada sesión pendiente de corte (idSesion)
    Worker -> DB: UPDATE reservas SET estado = 'NO_CONFIRMADA'\nWHERE id_sesion = :idSesion AND estado = 'PENDIENTE_CONFIRMACION'
    DB --> Worker: TotalRevocadas

    Worker -> DB: SELECT COUNT(*) FROM reservas\nWHERE id_sesion = :idSesion AND estado = 'CONFIRMADA'
    DB --> Worker: countConfirmadas

    alt Quórum alcanzado (countConfirmadas >= aforo_maximo * 0.5) [RN-09]
        Worker -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA' WHERE id = :idSesion
        Worker -> DB: COMMIT
        
        Worker -> SMTP: despacharConfirmacionDefinitiva(idSesion, correosConfirmados, correoMentor)
        activate SMTP
        SMTP --> Mentee: Notifica sesión CONFIRMADA con credenciales de acceso
        SMTP --> Mentor: Notifica quórum alcanzado y sesión confirmada
        deactivate SMTP
    else Quórum insuficiente (countConfirmadas < aforo_maximo * 0.5) [RN-09]
        Worker -> DB: UPDATE sesiones_mentoria SET estado = 'QUORUM_INSUFICIENTE' WHERE id = :idSesion
        Worker -> DB: COMMIT
        
        Worker -> SMTP: despacharAlertaQuorumInsuficiente(idSesion, correoMentor)
        activate SMTP
        SMTP --> Mentor: Alerta urgente: Quórum insuficiente (requiere resolución CUS07)
        deactivate SMTP
    end
end
deactivate DB

Worker --> Cron: ResumenEjecucionOK {procesadas, confirmadas, quorum_insuficiente}
deactivate Worker
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia refleja la estricta garantía transaccional ACID de la evaluación de quórum. La adquisición del bloqueo sobre la sesión (`FOR UPDATE`) impide que peticiones concurrentes de reserva o confirmación alteren el cómputo durante la ventana crítica. La mutación en bloque de las reservas pendientes a `NO_CONFIRMADA` sella el corte definitivo, permitiendo contrastar de forma confiable las confirmaciones efectivas contra el aforo máximo de la sesión según RN-09. La bifurcación emite resoluciones deterministas (`CONFIRMADA` o `QUORUM_INSUFICIENTE`) y desencadena los despachos SMTP correspondientes para mantener informados a todos los involucrados sin intervención humana en la capa de datos.

### 6.3.3.5. CUS07 – Diagrama de Secuencia: Gestionar Sesión ante Quórum Insuficiente

El diagrama de secuencia describe el orden cronológico de los mensajes e interacciones síncronas y asíncronas entre los componentes del sistema para ejecutar la resolución por quórum insuficiente. Modela las peticiones enviadas por el *Mentor Académico* a través de la SPA web hacia la *API Gateway (FastAPI)*, el control de concurrencia y mutación transaccional sobre la base de datos *PostgreSQL*, la desasignación de espacios mediante el subsistema de aulas de la EPIS, y el despacho de notificaciones SMTP institucionales.

#### Diagrama 6.15.5: Diagrama de Secuencia - CUS07: Gestionar Sesión ante Quórum Insuficiente

```plantuml
@startuml
title Diagrama de Secuencia - CUS07: Gestionar Sesión ante Quórum Insuficiente\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Mentor Académico" as Mentor
participant "Frontend SPA\n(React / Vite)" as UI
participant "API Gateway / Sesiones\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Servicio Aulas EPIS\n(Gestor Ambientes)" as Aulas
participant "Adaptador Email SMTP\n(UPT Mail)" as SMTP
actor "Mentoreado Confirmado" as Mentee

Mentor -> UI: Visualiza panel de alerta y pulsa opción de resolución
activate UI

alt Caso A: Dictado Excepcional (RN-09)
    UI -> API: PATCH /api/v1/sesiones/{idSesion}/resolver-quorum\n{decision: "DICTADO_EXCEPCIONAL"} [Bearer JWT]
    activate API
    API -> DB: BEGIN TRANSACTION
    activate DB
    API -> DB: UPDATE sesiones_mentoria SET estado = 'CONFIRMADA_EXCEPCIONAL'\nWHERE id = :idSesion AND estado = 'QUORUM_INSUFICIENTE'
    DB --> API: UpdateOK
    API -> DB: COMMIT
    deactivate DB
    
    API -> SMTP: notificarDictadoExcepcional(idSesion, correosMentees)
    activate SMTP
    SMTP --> Mentee: Notifica sesión CONFIRMADA EXCEPCIONALMENTE (se mantiene fecha y aula)
    deactivate SMTP
    
    API --> UI: HTTP 200 OK {estado: "CONFIRMADA_EXCEPCIONAL"}
    UI --> Mentor: Confirma dictado programado en agenda
else Caso B: Cancelación por Falta de Quórum (RN-10)
    UI -> API: PATCH /api/v1/sesiones/{idSesion}/resolver-quorum\n{decision: "CANCELAR_SESION"} [Bearer JWT]
    API -> DB: BEGIN TRANSACTION
    activate DB
    
    API -> DB: UPDATE sesiones_mentoria SET estado = 'CANCELADA_QUORUM'\nWHERE id = :idSesion AND estado = 'QUORUM_INSUFICIENTE'
    DB --> API: SesionCancelada
    
    API -> DB: UPDATE reservas SET estado = 'CANCELADA_SISTEMA'\nWHERE id_sesion = :idSesion AND estado = 'CONFIRMADA'
    DB --> API: ReservasLiberadas
    
    API -> Aulas: liberarAmbiente(idAula, fechaHoraInicio, fechaHoraFin)
    activate Aulas
    Aulas --> API: AmbienteLiberadoOK
    deactivate Aulas
    
    API -> DB: INSERT INTO auditoria_academica (id_sesion, tipo_evento, penalizacion, regla)\nVALUES (:idSesion, 'CANCELACION_QUORUM', false, 'RN-10')
    DB --> API: AuditoriaAsentada
    
    API -> DB: COMMIT
    deactivate DB
    
    API -> SMTP: notificarCancelacionQuorum(idSesion, correoMentor, correosMentees)
    activate SMTP
    SMTP --> Mentee: Notifica cancelación de sesión por falta de quórum (sin demérito)
    SMTP --> Mentor: Notifica constancia de cancelación sin penalización (RN-10)
    deactivate SMTP
    
    API --> UI: HTTP 200 OK {estado: "CANCELADA_QUORUM", penalizacion: false}
    UI --> Mentor: Despliega confirmación de cancelación formal sin penalización
end
deactivate API
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza la coherencia transaccional y la trazabilidad institucional ante un quórum insuficiente. Para el dictado excepcional, la operación confirma la sesión sin alterar la reserva previa de aulas ni los boletos emitidos. En el escenario de cancelación, la API encapsula dentro de una transacción ACID la transición de la sesión a `CANCELADA_QUORUM`, la mutación de las reservas confirmadas a `CANCELADA_SISTEMA`, la devolución inmediata del aula a la infraestructura de la facultad y el asentamiento en la bitácora de auditoría de la no-penalización para el mentor conforme a la regla RN-10, protegiendo su estatus académico en el programa P2P.

### 6.3.3.6. CUS09 – Diagrama de Secuencia: Publicar Oferta de Mentoría Individual o Grupal

El diagrama de secuencia describe el orden cronológico de los mensajes y validaciones que se ejecutan durante la publicación de una nueva oferta formativa. Modela la interacción entre el *Estudiante Mentor*, el *Frontend SPA*, el *API Gateway (FastAPI)*, el motor de persistencia *PostgreSQL (Supabase)* y los servicios de infraestructura (*Servicio Aulas EPIS* y *Google Meet API*).

#### Diagrama 6.15.6: Diagrama de Secuencia - CUS09: Publicar Oferta de Mentoría Individual o Grupal

```plantuml
@startuml
title Diagrama de Secuencia - CUS09: Publicar Oferta de Mentoría Individual o Grupal\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentor" as Mentor
participant "Frontend SPA\n(React / Vite)" as UI
participant "API Gateway / Sesiones\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Servicio Aulas EPIS\n(Gestor Ambientes)" as Aulas
participant "Google Meet API\n(Servicio Virtual)" as Meet

Mentor -> UI: Diligencia formulario de oferta y pulsa "Publicar Mentoría"
activate UI

UI -> API: POST /api/v1/sesiones {idAsignatura, titulo, fechaHora, modalidad, aforo} [Bearer JWT]
activate API

API -> DB: SELECT rol_activo, estado_activo, ciclo_actual\nFROM usuarios WHERE id = :idMentor
activate DB
DB --> API: MentorValido (rol='MENTOR', estado=activo, ciclo >= 7) [RN-01]
deactivate DB

alt Anticipación insuficiente (< 48h) [RN-04] o Aforo excedido [RN-05]
    API --> UI: HTTP 422 Unprocessable Entity {error: "Infracción RN-04 / RN-05: Parámetros inválidos"}
    UI --> Mentor: Alerta en pantalla con motivos de rechazo normativo
else Precondiciones reglamentarias válidas
    API -> DB: BEGIN TRANSACTION
    activate DB
    
    alt Modalidad Presencial (Aforo <= 10)
        API -> Aulas: verificarYBloquearAula(fechaHoraInicio, fechaHoraFin)
        activate Aulas
        Aulas --> API: AulaConfirmada {idAula: "Lab-03"}
        deactivate Aulas
        
        API -> DB: INSERT INTO sesiones_mentoria (id_mentor, id_asignatura, titulo, modalidad,\naforo_maximo, cupos_ocupados, fecha_hora_inicio, id_aula, estado)\nVALUES (:idMentor, :idAsig, :titulo, 'PRESENCIAL', :aforo, 0, :fecha, 'Lab-03', 'PUBLICADA')\nRETURNING id, estado
        DB --> API: idSesionCreada, estado='PUBLICADA'
    else Modalidad Virtual (Aforo <= 20)
        API -> Meet: generarEnlaceReunion(titulo, fechaHoraInicio)
        activate Meet
        Meet --> API: urlMeet ("https://meet.google.com/xyz-abcd-uvw")
        deactivate Meet
        
        API -> DB: INSERT INTO sesiones_mentoria (id_mentor, id_asignatura, titulo, modalidad,\naforo_maximo, cupos_ocupados, fecha_hora_inicio, enlace_virtual, estado)\nVALUES (:idMentor, :idAsig, :titulo, 'VIRTUAL', :aforo, 0, :fecha, :urlMeet, 'PUBLICADA')\nRETURNING id, estado
        DB --> API: idSesionCreada, estado='PUBLICADA'
    end
    
    API -> DB: COMMIT
    deactivate DB
    
    API --> UI: HTTP 201 Created {idSesion, estado: 'PUBLICADA', recursoAsignado}
    UI --> Mentor: Despliega acuse de publicación y tarjeta en el catálogo activo
end
deactivate API
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza que la publicación de una sesión cumpla con las salvaguardas arquitectónicas institucionales. Antes de iniciar la transacción en la base de datos, el backend verifica los privilegios y el récord académico del mentor (RN-01), descartando peticiones extemporáneas ($< 48\text{ h}$, RN-04) o con aforos desmedidos (RN-05). En caso exitoso, orquesta en una transacción atómica la reserva del ambiente físico o la provisión del enlace de videoconferencia con la inserción de la fila en `sesiones_mentoria`, devolviendo el estado `PUBLICADA` con tiempo de respuesta inferior a 2 segundos conforme a RNF02.

### 6.3.3.7. CUS14 – Diagrama de Secuencia: Consultar Agenda y Horarios de Mentorías

El diagrama de secuencia describe el orden cronológico de las invocaciones y el flujo de datos distribuido durante la consulta interactiva de la agenda universitaria. Modela la interacción entre el *Usuario Institucional*, la interfaz *Frontend SPA (React / FullCalendar)*, el *API Gateway (FastAPI)*, la capa de aceleración *Redis Cache* y la réplica de lectura de *PostgreSQL*.

#### Diagrama 6.15.7: Diagrama de Secuencia - CUS14: Consultar Agenda y Horarios de Mentorías

```plantuml
@startuml
title Diagrama de Secuencia - CUS14: Consultar Agenda y Horarios de Mentorías\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional" as User
participant "Frontend SPA\n(React / FullCalendar)" as UI
participant "API Gateway / Agenda\n(FastAPI)" as API
participant "Cache Layer\n(Redis InMemory)" as Cache
database "PostgreSQL DB\n(Read Replica / RLS)" as DB

User -> UI: Abre vista Agenda y selecciona mes/filtros
activate UI

UI -> API: GET /api/v1/agenda?mes=10&anio=2026&asignaturaId=4&modalidad=ALL [Bearer JWT]
activate API

API -> Cache: GET agenda:2026-10:asig-4:mod-ALL
activate Cache

alt Cache Hit (Datos en memoria vigentes)
    Cache --> API: JSONPayloadEventos (TTL restante > 0)
else Cache Miss (Consulta primaria o clave expirada)
    Cache --> API: null (No encontrado)
    deactivate Cache
    
    API -> DB: SELECT s.id, s.titulo, s.fecha_hora_inicio, s.modalidad, s.aforo_maximo,\n       s.cupos_ocupados, s.estado, a.nombre as asignatura, u.nombres as mentor,\n       EXISTS (SELECT 1 FROM reservas r WHERE r.id_sesion = s.id AND r.id_usuario = :idUser AND r.estado IN ('PENDIENTE_CONFIRMACION','CONFIRMADA')) as inscrito\nFROM sesiones_mentoria s\nJOIN asignaturas a ON s.id_asignatura = a.id\nJOIN usuarios u ON s.id_mentor = u.id\nWHERE s.fecha_hora_inicio BETWEEN :inicioMes AND :finMes\n  AND s.estado IN ('PUBLICADA', 'CONFIRMADA', 'CONFIRMADA_EXCEPCIONAL')\nORDER BY s.fecha_hora_inicio ASC
    activate DB
    DB --> API: FilasSesiones (conjunto estructurado)
    deactivate DB
    
    API -> Cache: SETEX agenda:2026-10:asig-4:mod-ALL 300 JSONPayload
    activate Cache
    Cache --> API: OK (Guardado en caché)
    deactivate Cache
end

API --> UI: HTTP 200 OK [Array de Eventos con aforo, cupos libres y flag 'inscrito']
deactivate API

UI --> User: Renderiza eventos en cuadrícula de calendario y barra lateral de detalles
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza un patrón de lectura altamente optimizado y escalable. La interposición de Redis actúa como caché de paso (*cache-aside*), reduciendo drásticamente la latencia de respuesta frente a consultas concurrentes de cientos de estudiantes durante el periodo de inscripciones (RNF01). La consulta SQL subyacente calcula en una sola pasada relacional el diferencial de vacantes (`RN-05`) y la existencia de reservas previas por parte del usuario autenticado, asegurando la consistencia visual sin sobrecarga computacional.

### 6.3.3.8. CUS11 - Diagrama de Secuencia: Registrar Asistencia Mediante Código QR

El diagrama de secuencia describe el orden cronológico de las invocaciones, verificaciones de seguridad criptográfica y mutaciones transaccionales para el registro de presencia de estudiantes mediante códigos QR ópticos. Modela la interacción entre el *Estudiante Mentoreado*, el *Mentor Académico*, la interfaz del escáner en el frontend SPA (*UI Escáner Mentor*), el *API Gateway / Asistencia (FastAPI)*, el *Servicio Criptográfico (HMAC / SHA-256)* y la base de datos *PostgreSQL (Supabase)* con aislamiento transaccional.

#### Diagrama 6.15.8: Diagrama de Secuencia - CUS11: Registrar Asistencia Mediante Código QR

```plantuml
@startuml
title Diagrama de Secuencia - CUS11: Registrar Asistencia Mediante Código QR\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Alumno
actor "Mentor Académico" as Mentor
participant "UI Escáner Mentor\n(React / HTML5-QRCode)" as UI
participant "API Asistencia\n(FastAPI Gateway)" as API
participant "Servicio Criptográfico\n(HMAC-SHA256)" as Crypto
database "PostgreSQL DB\n(Supabase / Transacción ACID)" as DB

Alumno -> Alumno: Abre ticket digital en dispositivo móvil
Alumno -> Mentor: Presenta código QR en pantalla
Mentor -> UI: Abre escáner y enfoca la cámara al código QR
activate UI

UI -> UI: Decodifica payload óptico:\n{idTicket, idReserva, tokenFirma, timestamp}
UI -> API: POST /api/v1/asistencia/escanear-qr {idTicket, idReserva, tokenFirma} [Bearer JWT Mentor]
activate API

API -> Crypto: validarFirmaTicket(idTicket, idReserva, tokenFirma)
activate Crypto
Crypto --> API: firmaValida (Boolean)
deactivate Crypto

alt Firma inválida o ticket adulterado
    API --> UI: HTTP 400 Bad Request {codigo: "FIRMA_INVALIDA", mensaje: "Código QR adulterado o ilegítimo"}
    UI --> Mentor: Alerta visual roja y tono de error ("Ticket no auténtico")
else Firma íntegra y auténtica
    API -> DB: SELECT s.fecha_hora_inicio, s.estado, r.estado as estado_reserva, t.estado as estado_ticket\nFROM tickets_asistencia t\nJOIN reservas r ON t.id_reserva = r.id\nJOIN sesiones_mentoria s ON r.id_sesion = s.id\nWHERE t.id = :idTicket AND r.id_mentor = :idMentorSesion
    activate DB
    DB --> API: RegistroContextoAsistencia
    deactivate DB
    
    alt Fuera de ventana reglamentaria [RN-11: T_inicio - 15m a T_inicio + 30m]
        API --> UI: HTTP 422 Unprocessable Entity {codigo: "HORA_EXTEMPORANEA", mensaje: "Fuera de tolerancia reglamentaria"}
        UI --> Mentor: Despliega aviso amarillo ("Registro manual requerido en bitácora")
    else Dentro de ventana reglamentaria
        API -> DB: BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE
        activate DB
        
        API -> DB: SELECT * FROM reservas WHERE id = :idReserva FOR UPDATE
        API -> DB: SELECT * FROM tickets_asistencia WHERE id = :idTicket FOR UPDATE
        
        alt Reserva no en estado CONFIRMADA o Ticket ya CONSUMIDO
            API -> DB: ROLLBACK
            API --> UI: HTTP 409 Conflict {codigo: "TICKET_YA_UTILIZADO", mensaje: "El cupo no está confirmado o el ticket ya fue validado"}
            UI --> Mentor: Despliega advertencia ("Asistencia previa ya registrada")
        else Cupo apto para marcación
            API -> DB: UPDATE reservas SET estado = 'ASISTIDA', actualizado_en = NOW() WHERE id = :idReserva
            API -> DB: UPDATE tickets_asistencia SET estado = 'CONSUMIDO', consumido_en = NOW() WHERE id = :idTicket
            API -> DB: INSERT INTO registros_asistencia (id_reserva, id_usuario, registrado_por, metodo, fecha_hora)\nVALUES (:idReserva, :idAlumno, :idMentor, 'ESCANEO_QR', NOW())
            API -> DB: COMMIT
            deactivate DB
            
            API --> UI: HTTP 200 OK {estado: "REGISTRADO", alumno: "Juan Pérez", hora: "14:05"}
            UI --> Mentor: Emite pitido de confirmación, borde verde y actualiza contador de asistencia en vivo
        end
    end
end

deactivate API
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza la inviolabilidad del control de presencia en la plataforma. La arquitectura desacopla en primer orden la verificación criptográfica mediante HMAC-SHA256, repeliendo intentos de inyección o duplicación de códigos QR sin sobrecargar la persistencia. Ante firmas legítimas, se somete la petición a la regla temporal RN-11 (-15 min a +30 min); de superarse favorablemente, se ejecuta una transacción relacional serializable con bloqueo pesimista `FOR UPDATE` que actualiza atómicamente la reserva a `ASISTIDA`, inhabilita el ticket (`CONSUMIDO`) y asienta el registro de auditoría, impidiendo ataques de concurrencia y garantizando fe pública para el cómputo de horas formativas.

### 6.3.3.9. CUS10 - Diagrama de Secuencia: Registrar Bitácora Pedagógica de Sesión

El diagrama de secuencia describe el orden cronológico de las invocaciones y mutaciones transaccionales para el cierre pedagógico de la mentoría. Modela las peticiones enviadas por el *Estudiante Mentor* a través de la SPA web hacia la *API Gateway (FastAPI)*, el control de la ventana reglamentaria de 24 horas (RN-07), la mutación atómica de reservas huérfanas hacia `INASISTENCIA` (RN-11), el asentamiento de la bitácora y la acreditación de horas en la bolsa del mentor (RN-12) sobre *PostgreSQL (Supabase)* con aislamiento transaccional, concluyendo con el despacho de eventos de notificación mediante *SMTP UPT*.

#### Diagrama 6.15.9: Diagrama de Secuencia - CUS10: Registrar Bitácora Pedagógica de Sesión

```plantuml
@startuml
title Diagrama de Secuencia - CUS10: Registrar Bitácora Pedagógica de Sesión\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentor" as Mentor
participant "Frontend SPA\n(React / FormBitacora)" as UI
participant "API Bitácora\n(FastAPI Gateway)" as API
database "PostgreSQL DB\n(Supabase / RLS Transaccional)" as DB
participant "Servicio Email / Eventos\n(SMTP UPT & Webhooks)" as Mail

Mentor -> UI: Abre formulario de bitácora para la sesión finalizada
activate UI

UI -> API: GET /api/v1/sesiones/{idSesion}/contexto-bitacora [Bearer JWT]
activate API
API -> DB: SELECT s.*, r.id as id_reserva, r.id_usuario, r.estado as estado_reserva, u.nombres\nFROM sesiones_mentoria s\nJOIN reservas r ON s.id = r.id_sesion\nJOIN usuarios u ON r.id_usuario = u.id\nWHERE s.id = :idSesion AND s.id_mentor = :idMentorAuth
activate DB
DB --> API: FilaSesionYAlumnos (estado='EN_CURSO'|'FINALIZADA', reservas=[...])
deactivate DB

API --> UI: HTTP 200 OK {sesion, alumnosInscritos, horasComputables}
deactivate API

UI --> Mentor: Despliega formulario con nómina de asistencia previa
deactivate UI

Mentor -> UI: Ingresa temas (>=30 chars), dificultades, acuerdos y pulsa "Enviar Bitácora"
activate UI

UI -> API: POST /api/v1/sesiones/{idSesion}/bitacora {temas, dificultades, acuerdos} [Bearer JWT]
activate API

API -> DB: SELECT fecha_hora_fin, estado FROM sesiones_mentoria WHERE id = :idSesion
activate DB
DB --> API: {fecha_hora_fin, estado}
deactivate DB

alt Fuera de plazo reglamentario [RN-07: ahora > fecha_hora_fin + 24 horas]
    API --> UI: HTTP 422 Unprocessable Entity {codigo: "PLAZO_24H_EXPIRADO", mensaje: "El plazo legal de 24h ha vencido"}
    UI --> Mentor: Alerta en pantalla ("Bloqueado por extemporaneidad. Solicitar desbloqueo a Tutoría")
else Dentro de plazo reglamentario (<= 24 horas)
    API -> DB: BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED
    activate DB
    
    API -> DB: SELECT id, estado FROM sesiones_mentoria WHERE id = :idSesion FOR UPDATE
    
    API -> DB: UPDATE reservas SET estado = 'INASISTENCIA', actualizado_en = NOW()\nWHERE id_sesion = :idSesion AND estado = 'CONFIRMADA'
    
    API -> DB: INSERT INTO bitacoras_sesion (id, id_sesion, id_mentor, temas_tratados, dificultades, acuerdos, horas_dictadas, estado, creado_en)\nVALUES (gen_random_uuid(), :idSesion, :idMentor, :temas, :dificultades, :acuerdos, :horas, 'REGISTRADA', NOW())\nRETURNING id
    
    API -> DB: UPDATE sesiones_mentoria SET estado = 'FINALIZADA', actualizado_en = NOW() WHERE id = :idSesion
    
    API -> DB: UPDATE bolsas_horas_mentor SET horas_acumuladas = horas_acumuladas + :horas,\nactualizado_en = NOW() WHERE id_mentor = :idMentor
    
    API -> DB: INSERT INTO registros_auditoria (id_usuario, accion, entidad, detalle, fecha_hora)\nVALUES (:idMentor, 'REGISTRO_BITACORA', 'sesiones_mentoria', :idSesion, NOW())
    
    API -> DB: COMMIT
    deactivate DB
    
    API -> Mail: dispararNotificacionesYCierre(idSesion, idMentor)
    activate Mail
    Mail --> Mentor: Email comprobante: "Bitácora registrada satisfactoriamente"
    Mail --> API: OK (Eventos encolados para encuestas a estudiantes ASISTIDA)
    deactivate Mail
    
    API --> UI: HTTP 201 Created {idBitacora, estado: "REGISTRADA", horasAcreditadas: 2}
    deactivate API
    UI --> Mentor: Despliega acuse formal, insignias potenciales y actualiza estado a FINALIZADA
    deactivate UI
end
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza la coherencia transaccional y la completitud del ciclo pedagógico de mentoría. La verificación previa del límite temporal de 24 horas (`RN-07`) protege la integridad de los informes curriculares frente a registros tardíos. La transacción encapsulada en PostgreSQL sincroniza la regularización masiva de inasistencias (`RN-11`), la persistencia inmutable de la bitácora con sus contenidos formativos, la clausura definitiva de la sesión en estado `FINALIZADA` y la adición inmediata de las horas dictadas a la bolsa del mentor (`RN-12`), disparando de manera desacoplada los eventos para la posterior habilitación de encuestas de calidad.

### 6.3.3.10. CUS05 - Diagrama de Secuencia: Responder Encuesta de Calidad Post-Mentoría

El diagrama de secuencia describe el orden cronológico de las invocaciones, validaciones de seguridad de acceso y mutaciones transaccionales para la captura y anonimización de la encuesta de calidad docente. Modela las peticiones enviadas por el *Estudiante Mentoreado* desde la interfaz SPA, la validación de elegibilidad en la *API Gateway (FastAPI)*, el control de la ventana perentoria de 24 horas posteriores al cierre de bitácora, la disociación criptográfica de identidad bajo la Ley N° 29733, y la actualización concurrente del score de reputación del mentor en la base de datos *PostgreSQL (Supabase)* con aislamiento transaccional.

#### Diagrama 6.15.10: Diagrama de Secuencia - CUS05: Responder Encuesta de Calidad Post-Mentoría

```plantuml
@startuml
title Diagrama de Secuencia - CUS05: Responder Encuesta de Calidad Post-Mentoría\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Estudiante Mentoreado" as Mentee
participant "Frontend SPA\n(React / FormEncuesta)" as UI
participant "API Gateway / Calidad\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS Transaccional)" as DB

Mentee -> UI: Abre pestaña "Encuestas Pendientes"
activate UI

UI -> API: GET /api/v1/encuestas/pendientes [Bearer JWT Mentee]
activate API
API -> DB: SELECT s.id, s.titulo, b.fecha_registro as fecha_cierre, r.id as id_reserva\nFROM reservas r\nJOIN sesiones_mentoria s ON r.id_sesion = s.id\nJOIN bitacoras_sesion b ON s.id = b.id_sesion\nWHERE r.id_usuario = :idMentee AND r.estado = 'ASISTIDA' AND r.encuesta_completada = FALSE\n  AND NOW() <= b.fecha_registro + INTERVAL '24 HOURS'
activate DB
DB --> API: ListaSesionesPendientes
deactivate DB

API --> UI: HTTP 200 OK [Sesiones con ventana de 24h activa]
deactivate API

UI --> Mentee: Renderiza tarjeta con temporizador de cuenta regresiva
deactivate UI

Mentee -> UI: Selecciona sesión y completa 4 escalas Likert + comentario
activate UI
Mentee -> UI: Clic en "Enviar Evaluación de Calidad"

UI -> API: POST /api/v1/sesiones/{idSesion}/encuesta\n{dominio: 5, claridad: 5, puntualidad: 4, recursos: 5, comentario: "Excelente"} [Bearer JWT]
activate API

API -> DB: SELECT r.id, r.estado, r.encuesta_completada, b.fecha_registro as cierre_bitacora, s.id_mentor\nFROM reservas r\nJOIN sesiones_mentoria s ON r.id_sesion = s.id\nJOIN bitacoras_sesion b ON s.id = b.id_sesion\nWHERE r.id_sesion = :idSesion AND r.id_usuario = :idMentee
activate DB
DB --> API: FilaValidacion
deactivate DB

alt Reserva no en estado ASISTIDA o ya evaluada
    API --> UI: HTTP 403 Forbidden {codigo: "RESERVA_NO_APTA", mensaje: "No cuenta con asistencia efectiva acreditada"}
    UI --> Mentee: Alerta de bloqueo ("Acceso denegado: Asistencia no registrada")
else Fuera de ventana reglamentaria (ahora > cierre_bitacora + 24 horas)
    API --> UI: HTTP 422 Unprocessable Entity {codigo: "VENTANA_24H_EXPIRADA", mensaje: "La ventana para evaluar ha caducado"}
    UI --> Mentee: Alerta amarilla ("El plazo de 24 horas para evaluar ha vencido")
else Apto y dentro de plazo
    API -> DB: BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED
    activate DB
    
    API -> DB: UPDATE reservas SET encuesta_completada = TRUE, actualizado_en = NOW() WHERE id = :idReserva
    
    API -> API: anonimizarPayload(idMentee, comentario)
    
    API -> DB: INSERT INTO encuestas_satisfaccion (id_sesion, id_mentor, hash_estudiante_anonimo,\npuntuacion_dominio, puntuacion_claridad, puntuacion_puntualidad, puntuacion_recursos,\npromedio_sesion, comentario_cualitativo, creado_en)\nVALUES (:idSesion, :idMentor, :hashAnonimo, 5, 5, 4, 5, 4.75, :comentario, NOW())
    
    API -> DB: SELECT score_promedio, total_evaluaciones FROM reputacion_mentores WHERE id_mentor = :idMentor FOR UPDATE
    DB --> API: {score_actual: 4.80, total: 10}
    
    API -> DB: UPDATE reputacion_mentores\nSET score_promedio = ((4.80 * 10) + 4.75) / 11,\n    total_evaluaciones = 11, actualizado_en = NOW()\nWHERE id_mentor = :idMentor
    
    API -> DB: INSERT INTO registros_auditoria (id_usuario, accion, entidad, detalle, fecha_hora)\nVALUES (:idMentee, 'REGISTRO_ENCUESTA_CALIDAD', 'encuestas_satisfaccion', :idSesion, NOW())
    
    API -> DB: COMMIT
    deactivate DB
    
    API --> UI: HTTP 201 Created {estado: "REGISTRADO", mensaje: "Evaluación procesada exitosamente"}
    deactivate API
    
    UI --> Mentee: Despliega notificación verde de agradecimiento y remueve sesión de la lista pendiente
    deactivate UI
end
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza el blindaje de la retroalimentación cualitativa estudiantil. Al condicionar la inserción a la verificación relacional previa de asistencia efectiva (`ASISTIDA`) y vigencia horaria ($T \le 24\text{ h}$ post-bitácora), se evitan manipulaciones o evaluaciones maliciosas. La fase intermedia de disociación criptográfica garantiza el cumplimiento incondicional de la Ley N° 29733 sobre protección de identidad, permitiendo que la posterior actualización con bloqueo pesimista en `reputacion_mentores` refleje con total exactitud matemática la media ponderada del docente (RN-13) con latencia menor a 500 ms (RNF02).

### 6.3.3.11. CUS19 - Diagrama de Secuencia: Consultar Historial de Sesiones y Asistencia

El diagrama de secuencia describe el orden cronológico de las invocaciones y el flujo de datos distribuido durante la consulta paginada y filtrada del expediente académico. Modela la interacción entre el *Usuario Institucional*, la interfaz *Frontend SPA (TanStack Table)*, el *API Gateway / Historial (FastAPI)* y la base de datos *PostgreSQL (Supabase)* con políticas de seguridad *Row Level Security (RLS)* activas, detallando tanto la agregación estadística inicial como la recuperación a demanda del contenido temático de la bitácora docente.

#### Diagrama 6.15.11: Diagrama de Secuencia - CUS19: Consultar Historial de Sesiones y Asistencia

```plantuml
@startuml
title Diagrama de Secuencia - CUS19: Consultar Historial de Sesiones y Asistencia\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 11

actor "Usuario Institucional" as User
participant "Frontend SPA\n(React / TanStack Table)" as UI
participant "API Gateway / Historial\n(FastAPI)" as API
database "PostgreSQL DB\n(Supabase / RLS Activo)" as DB

User -> UI: Clic en "Mi Historial Académico"
activate UI

UI -> API: GET /api/v1/historial?semestre=2026-I&page=1&limit=10 [Bearer JWT]
activate API

API -> DB: SET LOCAL rls.user_id = :idUsuarioAuth
activate DB

API -> DB: SELECT s.id, s.titulo, a.nombre as asignatura, s.modalidad, s.fecha_hora_inicio,\n       CASE WHEN s.id_mentor = :idUser THEN 'MENTOR' ELSE 'MENTOREADO' END as rol_usuario,\n       COALESCE(r.estado, 'NO_APLICA') as estado_asistencia, s.estado as estado_sesion,\n       b.id IS NOT NULL as tiene_bitacora\nFROM sesiones_mentoria s\nJOIN asignaturas a ON s.id_asignatura = a.id\nLEFT JOIN reservas r ON s.id = r.id_sesion AND r.id_usuario = :idUser\nLEFT JOIN bitacoras_sesion b ON s.id = b.id_sesion\nWHERE (r.id_usuario = :idUser OR s.id_mentor = :idUser)\n  AND s.estado IN ('FINALIZADA', 'CANCELADA_MENTOR', 'CANCELADA_QUORUM')\nORDER BY s.fecha_hora_inicio DESC LIMIT 10 OFFSET 0
DB --> API: FilasHistorial (colección de registros con rol y asistencia)

API -> DB: SELECT COUNT(DISTINCT s.id) as total_sesiones,\n       COALESCE(SUM(CASE WHEN r.estado = 'ASISTIDA' THEN 1 ELSE 0 END), 0) as asistencias_efectivas,\n       COALESCE(SUM(CASE WHEN s.id_mentor = :idUser AND b.estado = 'REGISTRADA' THEN s.duracion_horas ELSE 0 END), 0) as horas_dictadas\nFROM sesiones_mentoria s\nLEFT JOIN reservas r ON s.id = r.id_sesion AND r.id_usuario = :idUser\nLEFT JOIN bitacoras_sesion b ON s.id = b.id_sesion\nWHERE (r.id_usuario = :idUser OR s.id_mentor = :idUser)
DB --> API: MetricasConsolidadas
deactivate DB

API --> UI: HTTP 200 OK {items: [...], totalRegistros: 18, metricas: {totalSesiones: 18, porcentajeAsistencia: 94.4, horasDictadas: 12}}
deactivate API

UI --> User: Despliega cuadrícula de historial con tarjetas de resumen y paginador
deactivate UI

User -> UI: Clic en fila de sesión para ver bitácora pedagógica
activate UI

UI -> API: GET /api/v1/sesiones/{idSesion}/bitacora-detalle [Bearer JWT]
activate API

API -> DB: SELECT b.temas_tratados, b.dificultades_detectadas, b.observaciones_pedagogicas,\n       b.horas_dictadas, s.enlace_recursos\nFROM bitacoras_sesion b\nJOIN sesiones_mentoria s ON b.id_sesion = s.id\nWHERE b.id_sesion = :idSesion
activate DB
DB --> API: FilaBitacoraYRecursos
deactivate DB

API --> UI: HTTP 200 OK {bitacora: {temas, dificultades, observaciones}, recursosUrl: "..."}
deactivate API

UI --> User: Abre panel lateral con el contenido formativo completo de la sesión
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia garantiza una arquitectura de consulta de alto desempeño y estricta privacidad. La inyección de la variable de sesión `rls.user_id` activa las reglas de seguridad a nivel de fila en PostgreSQL, restringiendo los registros visibles sin depender de filtros arbitrarios en la capa de presentación. La partición analítica entre la recuperación paginada de eventos y la carga bajo demanda de la bitácora pedagógica previene transferencias de carga útil innecesarias, permitiendo tiempos de respuesta de consulta inferiores a 300 ms en concordancia con RNF01.

### 6.3.3.12. CUS16 - Diagrama de Secuencia: Consultar Tablero de Insignias y Reputación

El diagrama de secuencia especifica el intercambio cronológico de mensajes, cómputo algorítmico y persistencia transaccional durante la visualización del tablero lúdico y de reputación. Se articulan el *Mentor Académico*, la interfaz *UI TableroReputacionComponent (React / Recharts)*, el servicio backend *API GamificationRouter (FastAPI)*, los módulos de lógica de dominio *ReputationCalculator (RN-13)* y *BadgeRuleEngine*, y la base de datos *PostgreSQL (Supabase)*. Se integran los fragmentos de interacción condicional para el estado de calibración inicial (E01), la verificación automática de umbrales con persistencia de nuevas medallas y la emisión de credenciales públicas verificables con firma SHA-256 (FA02).

#### Diagrama 6.15.12: Diagrama de Secuencia - CUS16: Consultar Tablero de Insignias y Reputación

```plantuml
@startuml
title Diagrama de Secuencia - CUS16: Consultar Tablero de Insignias y Reputación\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Mentor Académico" as Mentor
participant "UI TableroReputacion\n(React / Recharts)" as UI
participant "API GamificationRouter\n(FastAPI / Pydantic)" as API
participant "Domain: ReputationEngine\n(Regla RN-13)" as RepEngine
participant "Domain: BadgeRuleEngine\n(Auditor de Logros)" as BadgeEngine
database "PostgreSQL DB\n(Supabase / RLS)" as DB

== 1. Carga del Tablero de Gamificación y Reputación ==
Mentor -> UI: Clic en "Mi Reputación & Reconocimientos"
activate UI

UI -> API: GET /api/v1/gamificacion/mentores/{idMentor}/tablero\n[Headers: Authorization Bearer JWT]
activate API

API -> DB: SELECT COUNT(*), AVG(promedio_sesion),\n       AVG(puntuacion_dominio), AVG(puntuacion_claridad),\n       AVG(puntuacion_puntualidad), AVG(puntuacion_recursos)\nFROM encuestas_satisfaccion WHERE id_mentor = :idMentor
activate DB
DB --> API: MetricasEncuestas {totalEvaluaciones, avgGlobal, avgDominio, ...}
deactivate DB

API -> DB: SELECT COUNT(*) FILTER (WHERE estado = 'FINALIZADA') AS sesiones_completadas,\n       COUNT(*) FILTER (WHERE estado IN ('CANCELADA_MENTOR')) AS canceladas_mentor,\n       COUNT(*) AS total_convocadas\nFROM sesiones_mentoria WHERE id_mentor = :idMentor
activate DB
DB --> API: MetricasSesiones {sesiones_completadas, canceladas_mentor, total_convocadas}
deactivate DB

API -> DB: SELECT COUNT(*) FILTER (WHERE creado_en <= fecha_hora_fin + INTERVAL '24 hours') AS a_tiempo,\n       COUNT(*) AS total_bitacoras\nFROM bitacoras_sesion b JOIN sesiones_mentoria s ON b.id_sesion = s.id\nWHERE s.id_mentor = :idMentor
activate DB
DB --> API: MetricasBitacoras {a_tiempo, total_bitacoras}
deactivate DB

alt Mentor sin evaluaciones suficientes (E01: En Calibración)
    API --> UI: HTTP 200 OK {\n  enCalibracion: true,\n  mensaje: "Score en proceso de calibración inicial",\n  sesionesDictadas: total_convocadas,\n  insigniasObtenidas: [...]\n}
    UI --> Mentor: Despliega banner informativo de calibración y metas próximas
else Evaluaciones históricas activas (totalEvaluaciones > 0)
    API -> RepEngine: calcularScoreCompuesto(MetricasEncuestas, MetricasSesiones, MetricasBitacoras)
    activate RepEngine
    note right of RepEngine
      Fórmula RN-13:
      Score = (0.70 * avgGlobal)
            + (0.20 * (completadas / total_convocadas) * 5)
            + (0.10 * (a_tiempo / total_bitacoras) * 5)
    end note
    RepEngine --> API: ScoreCalculadoDTO {scoreCompuesto: 4.88, nivel: "MENTOR_DESTACADO"}
    deactivate RepEngine
    
    API -> DB: UPDATE reputacion_mentores\nSET score_promedio = 4.88, nivel_reputacion = 'MENTOR_DESTACADO',\n    fecha_actualizacion = NOW()\nWHERE id_mentor = :idMentor
    activate DB
    DB --> API: RegistroActualizado
    deactivate DB
    
    API -> BadgeEngine: evaluarNuevosLogros(idMentor, horasAcumuladas, scoreCompuesto)
    activate BadgeEngine
    BadgeEngine -> DB: SELECT id_insignia FROM insignias_otorgadas WHERE id_mentor = :idMentor
    activate DB
    DB --> BadgeEngine: IdsInsigniasPoseidas
    deactivate DB
    
    opt Supera nuevos umbrales normativos de insignias
        BadgeEngine -> DB: INSERT INTO insignias_otorgadas (id_mentor, id_insignia, fecha_otorgamiento, hash_verificacion)\nVALUES (:idMentor, :idInsigniaNueva, NOW(), SHA256(...))
        activate DB
        DB --> BadgeEngine: ConfirmacionInsersion
        deactivate DB
    end
    BadgeEngine --> API: CatalogoInsigniasProgresoDTO {activas: [...], enProgreso: [...]}
    deactivate BadgeEngine
    
    API -> DB: SELECT comentario_cualitativo, creado_en\nFROM encuestas_satisfaccion\nWHERE id_mentor = :idMentor AND comentario_cualitativo IS NOT NULL\nORDER BY creado_en DESC LIMIT 10
    activate DB
    note right of DB: Anonimización estricta Ley N° 29733\n(Sin referencias al id_estudiante)
    DB --> API: ComentariosAnonimos
    deactivate DB
    
    API --> UI: HTTP 200 OK TableroGamificacionDTO {\n  scoreGlobal: 4.88, nivel: "Destacado",\n  dimensiones: {dominio: 4.9, claridad: 4.8, puntualidad: 4.9, recursos: 4.9},\n  insignias: CatalogoInsigniasProgresoDTO,\n  feedComentarios: ComentariosAnonimos\n}
    deactivate API
    
    UI --> Mentor: Renderiza velocímetro animado, gráfica radar Likert, cards de insignias y comentarios
    deactivate UI
end

== 2. Compartir Insignia Oficial en Portafolio Externo (FA02) ==
Mentor -> UI: Clic en botón "Compartir Insignia" en tarjeta de medalla
activate UI

UI -> API: POST /api/v1/gamificacion/insignias/{idOtorgamiento}/compartir\n[Headers: Authorization Bearer JWT]
activate API

API -> DB: SELECT io.hash_verificacion, io.fecha_otorgamiento, i.nombre, u.nombres, u.apellidos\nFROM insignias_otorgadas io\nJOIN insignias i ON io.id_insignia = i.id\nJOIN usuarios u ON io.id_mentor = u.id\nWHERE io.id = :idOtorgamiento
activate DB
DB --> API: FilaInsigniaVerificable
deactivate DB

API --> UI: HTTP 200 OK {\n  urlPublica: "https://p2p.epis.upt.edu.pe/verificar/insignia/" + hash,\n  hashSha256: hash,\n  codigoQrSvg: "<svg>...</svg>"\n}
deactivate API

UI --> Mentor: Despliega modal con enlace permanente de fe pública y botón de copia directa
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS16 articula una comunicación desacoplada y eficiente entre el frontend interactivo y el motor de gamificación. Las invocaciones concurrentes iniciales recuperan de forma atómica los datos evaluativos, operativos y temporales requeridos por la ecuación RN-13. El cómputo en el dominio (`ReputationCalculator`) actualiza el estado de la entidad persistente sin bloquear transacciones de reserva concurrentes. Asimismo, el subsistema `BadgeRuleEngine` verifica el cumplimiento de hitos y asienta los otorgamientos respaldados con un hash criptográfico SHA-256, facilitando su posterior verificación externa y garantizando el cumplimiento de RNF02 (latencia < 500 ms) y RNF09 (trazabilidad y fe pública digital).

### 6.3.3.13. CUS13 - Diagrama de Secuencia: Parametrizar y Emitir Certificados

El diagrama de secuencia describe el orden cronológico de las invocaciones, el procesamiento algorítmico distribuido y la persistencia transaccional durante la parametrización de umbrales y la emisión por lotes (*batch*) de certificaciones formativas. Modela la interacción entre el *Administrador Institucional*, la interfaz *UI CertificadosView (React SPA)*, el servicio backend *API CertificadosRouter (FastAPI)*, el componente de dominio *CertificacionService (RN-14)*, el generador documental *PDFWorker (Motor PDF/A + Hash)*, la base de datos *PostgreSQL (Supabase)* y el *Servicio SMTP UPT*.

#### Diagrama 6.15.13: Diagrama de Secuencia - CUS13: Parametrizar y Emitir Certificados

```plantuml
@startuml
title Diagrama de Secuencia - CUS13: Parametrizar y Emitir Certificados\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Administrador\n(Comité Tutoría)" as Admin
participant "UI CertificadosView\n(React / TanStack)" as UI
participant "API CertificadosRouter\n(FastAPI / Pydantic)" as API
participant "Service: CertificacionService\n(RN-14 Engine)" as CertService
participant "Worker: PDFGenerator\n(PDF/A & Hash SHA-256)" as PDFWorker
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Servicio Email\n(SMTP UPT)" as Mail

== 1. Parametrización y Auditoría de Mentores Elegibles ==
Admin -> UI: Configura umbrales (Semestre "2026-I", horasMin: 30, scoreMin: 4.0)\ny presiona "Consultar Mentores Elegibles"
activate UI

UI -> API: POST /api/v1/certificados/parametros/evaluar-elegibles\n{\n  "semestre": "2026-I",\n  "horasMinimas": 30,\n  "scoreMinimo": 4.0\n} [Bearer JWT]
activate API

API -> CertService: consultarCandidatosAcreditacion(dto)
activate CertService

CertService -> DB: SELECT u.id, u.codigo, u.nombres, u.apellidos, u.correo,\n       SUM(b.horas_dictadas) AS horas_visadas,\n       rm.score_promedio\nFROM usuarios u\nJOIN sesiones_mentoria s ON s.id_mentor = u.id\nJOIN bitacoras_sesion b ON b.id_sesion = s.id\nJOIN reputacion_mentores rm ON rm.id_mentor = u.id\nWHERE s.semestre = :semestre AND b.estado = 'VISADA'\nGROUP BY u.id, u.codigo, u.nombres, u.apellidos, u.correo, rm.score_promedio\nHAVING SUM(b.horas_dictadas) >= :horasMin AND rm.score_promedio >= :scoreMin
activate DB
DB --> CertService: ListaCandidatosAuditoría
deactivate DB

alt Sin postulantes que cumplan el umbral (E01)
    CertService --> API: {totalElegibles: 0, candidatos: []}
    API --> UI: HTTP 200 OK {totalElegibles: 0, mensaje: "Sin mentores elegibles para el umbral fijado"}
    UI --> Admin: Despliega alerta informativa de umbrales no alcanzados
else Postulantes calificados encontrados (> 0)
    CertService --> API: NominaElegiblesDTO {candidatos: [...], total: 18}
    deactivate CertService
    
    API --> UI: HTTP 200 OK NominaElegiblesDTO
    deactivate API
    
    UI --> Admin: Presenta grilla interactiva con postulantes, horas auditadas y checkboxes
    deactivate UI
end

== 2. Orden Batch y Emisión Institucional Criptográfica ==
Admin -> UI: Revisa padrón, ratifica exclusiones y confirma modal de emisión
activate UI

UI -> API: POST /api/v1/certificados/lote/emitir\n{\n  "semestre": "2026-I",\n  "mentoresSeleccionados": ["uuid-1", "uuid-2", ...]\n} [Bearer JWT]
activate API

API -> CertService: ejecutarEmisionLote(dto)
activate CertService

CertService -> DB: BEGIN TRANSACTION
activate DB

loop Para cada mentorId en mentoresSeleccionados
    CertService -> DB: SELECT NEXTVAL('seq_correlativo_certificados')
    DB --> CertService: numCorrelativo (ej. 42)
    
    CertService -> PDFWorker: componerCertificadoPDFA(mentorId, horas, "CERT-EPIS-2026-I-0042")
    activate PDFWorker
    PDFWorker -> PDFWorker: renderizarPlantillaOficial(membrete, firmas, sellos)
    PDFWorker -> PDFWorker: generarCodigoQR("https://p2p.epis.upt.edu.pe/verificar/cert/" + correlativo)
    PDFWorker -> PDFWorker: computarHashSHA256(bytesPDF)
    
    PDFWorker -> DB: Almacenar binario en Supabase Storage (bucket 'certificados')
    DB --> PDFWorker: storagePath
    
    PDFWorker --> CertService: MetaCertificadoDTO {hashSha256, storagePath, qrUrl}
    deactivate PDFWorker
    
    CertService -> DB: INSERT INTO certificados (id_mentor, semestre, codigo_correlativo, horas_totales,\n                           promedio_reputacion, hash_sha256, ruta_pdf, qr_url, estado, fecha_emision)\nVALUES (:mentorId, :semestre, 'CERT-EPIS-2026-I-0042', :horas, :score, :hash, :ruta, :qr, 'EMITIDO', NOW())
    
    CertService -> DB: UPDATE bolsa_horas_mentor\nSET horas_certificadas = horas_certificadas + :horas\nWHERE id_mentor = :mentorId
    
    CertService -> Mail: despacharNotificacionCertificado(correoInstitucional, correlativo, qrUrl)
    activate Mail
    Mail --> CertService: ConfirmaciónEnvioSMTP
    deactivate Mail
end

CertService -> DB: COMMIT TRANSACTION
deactivate DB

CertService --> API: ResumenEmisionLoteDTO {totalProcesados: 18, emitidos: 18, errores: 0}
deactivate CertService

API --> UI: HTTP 201 Created ResumenEmisionLoteDTO
deactivate API

UI --> Admin: Despliega notificación de éxito: "Se han emitido 18 certificados con éxito"
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS13 formaliza una rigurosa arquitectura de fe pública universitaria. La fase inicial de filtrado garantiza la aplicación irrestricta de la regla RN-14, verificando que únicamente las horas con bitácoras en estado `VISADA` sean consolidadas para la certificación semestral. La fase de emisión por lotes modela una transacción atómica encapsulada en PostgreSQL, asegurando que la asignación del correlativo oficial, el cómputo del hash criptográfico SHA-256 sobre el archivo PDF/A y la actualización de la `BolsaHorasMentor` se ejecuten de manera íntegra, mitigando cualquier riesgo de inconsistencia documental o duplicidad de horas acreditadas.

### 6.3.3.14. CUS09 - Diagrama de Secuencia: Descargar Certificado de Horas de Mentoría

El diagrama de secuencia describe el orden cronológico de las invocaciones, los intercambios de datos binarios y la verificación criptográfica durante la descarga privada del certificado y su posterior validación pública ante terceros. Se detallan tres fases: (1) la recuperación paginada de constancias emitidas para el mentor autenticado, (2) la descarga segura con comprobación matemática del *checksum* SHA-256 en memoria antes del despacho HTTP, y (3) la verificación abierta y desatendida mediante escaneo de código QR (FA01) con registro de auditoría institucional.

#### Diagrama 6.15.14: Diagrama de Secuencia - CUS09: Descargar Certificado de Horas de Mentoría

```plantuml
@startuml
title Diagrama de Secuencia - CUS09: Descargar Certificado de Horas de Mentoría\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Mentor Académico" as Mentor
actor "Tercero Verificador\n(Empleador / Secretaría)" as Verificador
participant "UI Portal P2P\n(React Frontend)" as UI
participant "API: CertificadosRouter\n(FastAPI / Pydantic)" as API
participant "Service: VerificationService\n(Motor Criptográfico)" as VerifService
database "PostgreSQL DB\n(Supabase / RLS)" as DB
participant "Storage: ObjectBucket\n(Supabase Storage)" as Bucket

== 1. Listado y Previsualización de Certificados Oficiales ==
Mentor -> UI: Accede a "Mis Certificados"
activate UI

UI -> API: GET /api/v1/certificados/mis-certificados\n[Headers: Authorization Bearer JWT]
activate API

API -> DB: SELECT id, semestre, codigo_correlativo, horas_totales,\n       promedio_reputacion, fecha_emision, hash_sha256, qr_url, estado\nFROM certificados WHERE id_mentor = auth.uid()\nORDER BY fecha_emision DESC
activate DB
DB --> API: FilasCertificados
deactivate DB

API --> UI: HTTP 200 OK List<CertificadoResumenDTO>
deactivate API

UI --> Mentor: Presenta tarjetas de certificados con previsualización y botón de descarga
deactivate UI

== 2. Descarga Segura con Verificación de Checksum SHA-256 ==
Mentor -> UI: Clic en "Descargar Certificado Oficial en PDF" (idCertificado)
activate UI

UI -> API: GET /api/v1/certificados/{idCertificado}/descargar\n[Headers: Authorization Bearer JWT]
activate API

API -> DB: SELECT ruta_almacenamiento_pdf, hash_sha256, codigo_correlativo\nFROM certificados WHERE id = :idCertificado AND id_mentor = auth.uid()
activate DB
DB --> API: MetaCertificado {ruta_pdf, hash_sha256, codigo_correlativo}
deactivate DB

API -> Bucket: descargarObjetoBinario(ruta_pdf)
activate Bucket
Bucket --> API: bytesArchivoPDF
deactivate Bucket

API -> VerifService: calcularHashSHA256(bytesArchivoPDF)
activate VerifService
VerifService --> API: hashCalculado
deactivate VerifService

alt Checksum íntegro (hashCalculado == hash_sha256)
    API --> UI: HTTP 200 OK [Content-Type: application/pdf,\nContent-Disposition: attachment; filename="CERT-EPIS-2026-I-0042.pdf",\nETag: hash_sha256]\nStreamBinarioPDFA
    
    UI --> Mentor: Inicia descarga del archivo oficial sellado e inalterable
else Inconsistencia criptográfica (E02)
    API --> UI: HTTP 500 Internal Server Error {\n  error: "INTEGRIDAD_COMPROMETIDA",\n  mensaje: "El documento almacenado no coincide con el hash oficial registrado"\n}
    UI --> Mentor: Alerta roja de error de integridad y contacto con secretaría
end
deactivate API
deactivate UI

== 3. Verificación Pública Abierta vía Escaneo QR (FA01) ==
Verificador -> UI: Escanea código QR del documento (URL pública: /verificar/cert/{hashSha256})
activate UI

UI -> API: GET /api/v1/certificados/publico/verificar/{hashSha256}\n[Sin credenciales / Abierto]
activate API

API -> DB: SELECT c.codigo_correlativo, c.semestre, c.horas_totales, c.promedio_reputacion,\n       c.fecha_emision, c.estado, c.hash_sha256,\n       u.nombres, u.apellidos, u.codigo_estudiante\nFROM certificados c\nJOIN usuarios u ON c.id_mentor = u.id\nWHERE c.hash_sha256 = :hashSha256
activate DB
DB --> API: FilaVerificacionOficial
deactivate DB

API -> DB: INSERT INTO registros_auditoria_verificacion (hash_consultado, ip_origen, user_agent, fecha_hora)\nVALUES (:hashSha256, :ipClient, :userAgent, NOW())

API --> UI: HTTP 200 OK FichaVerificacionPublicaDTO {\n  autentico: true,\n  correlativo: "CERT-EPIS-2026-I-0042",\n  mentor: "Juan Pérez Quispe",\n  codigoEstudiante: "2021070123",\n  horasAcreditadas: 32,\n  semestre: "2026-I",\n  fechaEmision: "2026-07-15",\n  estado: "EMITIDO_VIGENTE"\n}
deactivate API

UI --> Verificador: Despliega ficha oficial con distintivo verde de Fe Pública EPIS-UPT
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS09 formaliza la rigurosidad técnica en la custodia y validación de la certificación académica. Al incorporar la verificación en memoria del hash SHA-256 previa al despacho del binario, el sistema asegura que ningún archivo manipulado en el bucket de almacenamiento sea entregado como constancia válida. La fase de validación pública mediante código QR resuelve la verificación de fe pública de forma desatendida y sin fricciones de autenticación, preservando la trazabilidad de cada inspección externa en la tabla de auditoría para salvaguardar la reputación académica de la EPIS-UPT.

### 6.3.3.15. CUS22 - Diagrama de Secuencia: Auditar Bitácoras, Asistencia y Horas de Mentoría

El diagrama de secuencia especifica la interacción temporal y el flujo de mensajes sincrónicos y asíncronos para la auditoría y visado docente de las sesiones de mentoría en `CUS22`. Describe dos etapas principales: (1) la recuperación y examen exhaustivo del expediente docente (bitácora pedagógica, evidencias digitales y nómina de firmas QR); y (2) la resolución del dictamen evaluativo por parte del auditor del Comité de Tutoría, modelando la bifurcación transaccional entre el visado oficial que consolida las horas docentes (`RN-12`, `RN-14`) y la emisión de pliegos de cargo con notificación de alerta y plazo perentorio de 48 horas (`FA01`).

#### Diagrama 6.15.15: Diagrama de Secuencia - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría

```plantuml
@startuml
title Diagrama de Secuencia - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Auditor Docente\n(Comité Tutoría)" as Auditor
participant "UI Auditoría Docente\n(React SPA)" as UI
participant "API: AuditoriaController\n(FastAPI / JWT)" as API
participant "Service: FiscalizacionService\n(Reglas RN-12/14)" as Svc
database "PostgreSQL DB\n(Supabase / ACID)" as DB
participant "Servicio Notificaciones\n(SMTP Institucional)" as Mail
actor "Mentor Académico\n(Fiscalizado)" as Mentor

== 1. Consulta de Bandeja y Apertura de Expediente de Fiscalización ==
Auditor -> UI: Accede a panel "Auditoría de Bitácoras Pendientes"
activate UI

UI -> API: GET /api/v1/auditoria/bitacoras/pendientes [Bearer JWT Admin]
activate API

API -> DB: SELECT b.id, b.id_sesion, s.tema, s.fecha_hora_fin, u.nombres, u.apellidos\nFROM bitacoras_sesion b\nJOIN sesiones_mentoria s ON b.id_sesion = s.id\nJOIN usuarios u ON s.id_mentor = u.id\nWHERE b.estado = 'REGISTRADA' AND s.estado = 'FINALIZADA'\nORDER BY s.fecha_hora_fin ASC
activate DB
DB --> API: FilasBitacorasPendientes
deactivate DB

API --> UI: HTTP 200 OK List<BandejaAuditoriaItemDTO>
UI --> Auditor: Renderiza bandeja cronológica con filtros por asignatura y mentor

Auditor -> UI: Selecciona sesión específica para auditar expediente
UI -> API: GET /api/v1/auditoria/sesiones/{idSesion}/expediente [Bearer JWT Admin]

API -> Svc: obtenerExpedienteCompleto(idSesion)
activate Svc

Svc -> DB: SELECT * FROM bitacoras_sesion WHERE id_sesion = :idSesion
activate DB
DB --> Svc: DatosBitacora (temas, dificultades, horas, urlEvidencia)

Svc -> DB: SELECT r.id, r.id_estudiante, u.codigo_estudiante, u.nombres, u.apellidos,\n       r.asistio, r.fecha_hora_firma_qr\nFROM reservas_cupo r\nJOIN usuarios u ON r.id_estudiante = u.id\nWHERE r.id_sesion = :idSesion\nORDER BY u.apellidos ASC
DB --> Svc: FilaNominaAsistenciaQR[]
deactivate DB

Svc --> API: ExpedienteAuditoriaCompletoDTO
deactivate Svc

API --> UI: HTTP 200 OK ExpedienteAuditoriaCompletoDTO
deactivate API

UI --> Auditor: Despliega visor con temas dictados, nómina validada por QR y evidencias adjuntas
deactivate UI

== 2. Dictamen de Fiscalización Académica ==
alt Dictamen A: Visado Favorable y Consolidación de Horas (RN-12 / RN-14)
    Auditor -> UI: Clic en botón "Visar y Aprobar Horas"
    activate UI
    
    UI -> API: POST /api/v1/auditoria/bitacoras/{idBitacora}/visar\n{dictamen: 'VISADO_APROBADO', comentarios: 'Contenido y asistencia conformes'}
    activate API
    
    API -> Svc: procesarVisadoBitacora(idBitacora, idAuditor)
    activate Svc
    
    Svc -> DB: BEGIN TRANSACTION
    activate DB
    
    Svc -> DB: UPDATE bitacoras_sesion\nSET estado = 'VISADA', id_auditor_visador = :idAuditor, fecha_visado = NOW()\nWHERE id = :idBitacora AND estado = 'REGISTRADA'
    
    Svc -> DB: UPDATE bolsas_horas_mentor\nSET horas_oficiales = horas_oficiales + :horasSesion,\n    horas_provisionales = horas_provisionales - :horasSesion\nWHERE id_mentor = :idMentor
    
    Svc -> DB: INSERT INTO registros_auditoria_admin (id_usuario_admin, accion, entidad, id_entidad, detalle)\nVALUES (:idAuditor, 'VISADO_BITACORA', 'bitacoras_sesion', :idBitacora, :detalleAudit)
    
    Svc -> DB: COMMIT
    DB --> Svc: Transacción Confirmada (ACID)
    deactivate DB
    
    Svc --> API: VisadoExitosoDTO {estado: 'VISADA', horasOficialesConsolidadas: :horasSesion}
    deactivate Svc
    
    API --> UI: HTTP 200 OK VisadoExitosoDTO
    deactivate API
    
    UI --> Auditor: Muestra distintivo verde de aprobación oficial y retira ítem de bandeja
    deactivate UI

else Dictamen B: Emisión Formal de Pliego de Observación (FA01)
    Auditor -> UI: Clic en botón "Observar Bitácora por Inconsistencia"
    activate UI
    
    UI --> Auditor: Despliega modal interactivo de emisión de pliego de cargos
    Auditor -> UI: Tipifica falta ('EVIDENCIA_INSUFICIENTE'), redacta observaciones y fija plazo 48h
    
    UI -> API: POST /api/v1/auditoria/bitacoras/{idBitacora}/observar\n{tipoFalta: 'EVIDENCIA_INSUFICIENTE', pliego: 'Discrepancia entre tema reportado y evidencias...', plazoHoras: 48}
    activate API
    
    API -> Svc: registrarObservacionBitacora(idBitacora, idAuditor, req)
    activate Svc
    
    Svc -> DB: BEGIN TRANSACTION
    activate DB
    
    Svc -> DB: UPDATE bitacoras_sesion\nSET estado = 'OBSERVADA', fecha_observacion = NOW()\nWHERE id = :idBitacora
    
    Svc -> DB: INSERT INTO observaciones_bitacora\n  (id_bitacora, id_auditor, tipo_falta, pliego, fecha_limite_subsanacion, estado)\nVALUES (:idBitacora, :idAuditor, :tipoFalta, :pliego, NOW() + INTERVAL '48 HOURS', 'EMITIDA_PENDIENTE')
    
    Svc -> DB: INSERT INTO registros_auditoria_admin (id_usuario_admin, accion, entidad, id_entidad, detalle)\nVALUES (:idAuditor, 'OBSERVACION_BITACORA', 'bitacoras_sesion', :idBitacora, :detalleObs)
    
    Svc -> DB: COMMIT
    DB --> Svc: Transacción Confirmada
    deactivate DB
    
    Svc -> Mail: despacharAlertaSubsanacionMentor(idMentor, pliego, fechaLimite)
    activate Mail
    Mail --> Mentor: Email UPT URGENTE: "Observación de Bitácora - Plazo 48h para subsanación"
    deactivate Mail
    
    Svc --> API: ObservacionRegistradaDTO {estado: 'OBSERVADA', limiteSubsanacion: :fechaLimite}
    deactivate Svc
    
    API --> UI: HTTP 200 OK ObservacionRegistradaDTO
    deactivate API
    
    UI --> Auditor: Presenta estado OBSERVADA con cuenta regresiva de 48 horas en curso
    deactivate UI
end
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS22 formaliza la orquestación transaccional y el cumplimiento normativo en la fiscalización de mentorías. El aislamiento ACID garantiza que la promoción de horas pedagógicas hacia la acreditación oficial ocurra de forma indivisible respecto al estado de la bitácora (`RN-12`), impidiendo la acumulación indebida de horas no verificadas. En caso de discrepancias metodológicas (`FA01`), el protocolo de observación congela preventivamente los créditos formativos y despacha automáticamente una notificación formal con plazo perentorio de 48 horas, preservando las garantías del debido proceso y la integridad del programa en la EPIS-UPT.

### 6.3.3.16. CUS12 - Diagrama de Secuencia: Destacar Mentorías Prioritarias

El diagrama de secuencia especifica la interacción temporal y el flujo sincrónico y asíncrono de mensajes para la activación de políticas de prioridad académica (`RF24`) y su efecto directo en el motor de recomendación personalizada (`RN-11`). Modela tres etapas coordinadas: (1) la consulta de asignaturas con índices críticos de reprobación, (2) la activación transaccional de la campaña con validación del factor de bonificación $\alpha \in [1.05, 1.50]$ e invalidación de caché distribuida en Redis, y (3) la inferencia en tiempo de ejecución del ranking *Top-k* (`CUS02`) con ponderación multiplicativa y proyección del distintivo dorado en la interfaz del estudiante mentoreado.

#### Diagrama 6.15.16: Diagrama de Secuencia - CUS12: Destacar Mentorías Prioritarias

```plantuml
@startuml
title Diagrama de Secuencia - CUS12: Destacar Mentorías Prioritarias\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Administrador Institucional\n(Comité Tutoría / Dirección)" as Admin
participant "UI Prioridades\n(React SPA)" as UI
participant "API: PrioridadesController\n(FastAPI / JWT)" as API
participant "Service: PriorizacionCurricularService\n(Lógica de Negocio RN-11)" as Svc
database "PostgreSQL DB\n(Supabase / ACID)" as DB
participant "Cache: RedisCluster\n(Key-Value Store)" as Redis
participant "Engine: RecommendationEngine\n(Inferencia Top-k)" as Engine
actor "Estudiante Mentoreado\n(Consumidor Feed)" as Alumno

== 1. Consulta y Evaluación de Asignaturas en Riesgo ==
Admin -> UI: Accede a panel "Gestión de Prioridades Académicas"
activate UI

UI -> API: GET /api/v1/prioridades/rendimiento [Bearer JWT Admin]
activate API

API -> DB: SELECT a.id, a.codigo, a.nombre, a.ciclo, m.tasa_reprobacion,\n       m.total_en_riesgo, p.estado AS estado_prioridad\nFROM asignaturas a\nLEFT JOIN metricas_rendimiento_academico m ON a.id = m.id_asignatura\nLEFT JOIN politicas_prioridad_asignatura p ON a.id = p.id_asignatura AND p.estado = 'ACTIVA'
activate DB
DB --> API: FilaAsignaturasCriticas[]
deactivate DB

API --> UI: HTTP 200 OK List<AsignaturaRendimientoDTO>
deactivate API

UI --> Admin: Despliega semáforo analítico de cursos con alta tasa de reprobación
deactivate UI

== 2. Configuración y Activación Transaccional de Campaña (RN-11) ==
Admin -> UI: Selecciona asignatura (ej. Cálculo II), ingresa vigencia y factor alfa=1.25
activate UI

UI -> API: POST /api/v1/prioridades/activar\n{idAsignatura: 'c2-uuid', factorAlfa: 1.25, inicio: '2026-05-01', fin: '2026-06-15', resolucion: 'RES-EPIS-014-2026'}
activate API

API -> Svc: activarPrioridadInstitucional(payload, idAdmin)
activate Svc

Svc -> Svc: validarParametros(1.05 <= alfa <= 1.50 && fin > inicio)

alt Parámetros fuera de rango (E01 / E02)
    Svc --> API: throw ValidationException("El factor alfa debe estar entre 1.05 y 1.50")
    API --> UI: HTTP 422 Unprocessable Entity {error: "Factor alfa fuera del rango reglamentario RN-11"}
    UI --> Admin: Resalta error en rojo y bloquea persistencia
else Parámetros conformes a normativa institucional
    Svc -> DB: BEGIN TRANSACTION
    activate DB
    
    Svc -> DB: INSERT INTO politicas_prioridad_asignatura\n  (id_asignatura, factor_alfa, fecha_inicio, fecha_fin, resolucion, id_admin, estado)\nVALUES (:idAsignatura, 1.25, :inicio, :fin, :resolucion, :idAdmin, 'ACTIVA')
    
    Svc -> DB: UPDATE asignaturas SET es_prioritaria = TRUE WHERE id = :idAsignatura
    
    Svc -> DB: INSERT INTO registros_auditoria_admin (id_usuario_admin, accion, entidad, detalle)\nVALUES (:idAdmin, 'ACTIVACION_PRIORIDAD', 'asignaturas', :detalleJson)
    
    Svc -> DB: COMMIT
    DB --> Svc: Transacción Confirmada (ACID)
    deactivate DB
    
    Svc -> Redis: DEL cache:recomendaciones:*
    activate Redis
    Redis --> Svc: OK (Claves purgadas)
    deactivate Redis
    
    Svc --> API: PrioridadActivadaDTO {idPolitica: 'pol-uuid', estado: 'ACTIVA', factorAlfa: 1.25}
    deactivate Svc
    
    API --> UI: HTTP 200 OK PrioridadActivadaDTO
    deactivate API
    
    UI --> Admin: Notifica confirmación con sello verde "Campaña Institucional Activa"
    deactivate UI
end

== 3. Consumo y Proyección Bonificada en el Feed del Mentoreado (CUS02) ==
Alumno -> UI: Ingresa al catálogo o feed de recomendaciones
activate UI

UI -> API: GET /api/v1/recomendaciones/feed?top=5 [Bearer JWT Alumno]
activate API

API -> Engine: inferirRecomendacionesTopK(idAlumno, top=5)
activate Engine

Engine -> DB: SELECT o.*, a.es_prioritaria, p.factor_alfa\nFROM ofertas_mentoria o\nJOIN asignaturas a ON o.id_asignatura = a.id\nLEFT JOIN politicas_prioridad_asignatura p ON a.id = p.id_asignatura AND p.estado = 'ACTIVA'\nWHERE o.estado = 'PUBLICADA'
activate DB
DB --> Engine: OfertasCandidatas[]
deactivate DB

loop Para cada oferta candidata
    Engine -> Engine: scoreFinal = scoreBase * (es_prioritaria ? factor_alfa : 1.0)
    Engine -> Engine: adjuntarBadge = es_prioritaria ? "Prioridad Institucional EPIS" : null
end

Engine -> Engine: ordenarPorScoreDescendente() y seleccionarTop(5)
Engine --> API: List<OfertaRecomendadaDTO>
deactivate Engine

API --> UI: HTTP 200 OK List<OfertaRecomendadaDTO>
deactivate API

UI --> Alumno: Despliega tarjetas con distintivo dorado "Prioridad Institucional EPIS" en primeras posiciones
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS12 evidencia la sincronización entre la decisión directiva y la experiencia del usuario final. La validación matemática de $\alpha$ en la capa de servicio garantiza la observancia estricta de `RN-11`, evitando monopolios algorítmicos. La purga inmediata de la caché de recomendaciones en Redis destruye matrices obsoletas, provocando que la siguiente consulta de los estudiantes mentoreados (`CUS02`) invoque al motor de inferencia con los nuevos ponderadores, asegurando que las asignaturas críticas reciban visibilidad preferencial inmediata sin requerir reinicios de servicio.

### 6.3.3.17. CUS14 - Diagrama de Secuencia: Visualizar Tablero de Analíticas Institucionales

El diagrama de secuencia especifica la interacción temporal y el flujo sincrónico de mensajes para la generación del cuadro de mando gerencial y el despacho de reportes en `CUS14` (`RF25`). Modela tres etapas analíticas: (1) la agregación de indicadores multidimensionales sobre réplicas de lectura optimizadas OLAP, (2) la compilación de dossiers ejecutivos foliados en formato PDF para el Consejo de Facultad, y (3) la extracción y disociación criptográfica unidireccional de datasets para investigación científica conforme a la regla de negocio `RN-13` y los mandatos de la Ley N° 29733.

#### Diagrama 6.15.17: Diagrama de Secuencia - CUS14: Visualizar Tablero de Analíticas Institucionales

```plantuml
@startuml
title Diagrama de Secuencia - CUS14: Visualizar Tablero de Analíticas Institucionales\nSistema Web P2P - EPIS UPT

autonumber
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

actor "Administrador / Investigador" as User
participant "UI Analítica Docente\n(React SPA)" as UI
participant "API: AnaliticaController\n(FastAPI / JWT)" as API
participant "Service: AnalyticsService\n(Motor OLAP / Agregación)" as Svc
database "PostgreSQL DB\n(Read Replica / OLAP)" as DB
participant "Security: AnonimizationService\n(Ley N° 29733 / RN-13)" as AnonSvc
participant "Compiler: ReportCompiler\n(PDF / CSV Engine)" as Compiler

== 1. Carga y Agregación del Cuadro de Mando Ejecutivo ==
User -> UI: Accede a panel "Analítica Institucional & Métricas"
activate UI

UI -> API: GET /api/v1/analitica/tablero?semestre=2026-I [Bearer JWT Admin]
activate API

API -> Svc: compilarMetricasTablero(semestre='2026-I')
activate Svc

Svc -> DB: SELECT COUNT(DISTINCT s.id) as total_sesiones,\n       ROUND(AVG(CASE WHEN s.estado = 'CONFIRMADA' THEN 1 ELSE 0 END)*100, 2) as tasa_quorum,\n       ROUND(AVG(CASE WHEN r.asistio = TRUE THEN 1 ELSE 0 END)*100, 2) as tasa_asistencia,\n       ROUND(AVG(e.puntaje_general), 2) as csat_global\nFROM sesiones_mentoria s\nLEFT JOIN reservas_cupo r ON s.id = r.id_sesion\nLEFT JOIN encuestas_calidad e ON s.id = e.id_sesion\nWHERE s.semestre = '2026-I'
activate DB
DB --> Svc: MetricasGeneralesAgregadas

Svc -> DB: SELECT a.nombre, COUNT(st.id) as total_demandas_vacias\nFROM solicitudes_tematicas st\nJOIN asignaturas a ON st.id_asignatura = a.id\nWHERE st.estado = 'PENDIENTE_ATENCION'\nGROUP BY a.nombre ORDER BY total_demandas_vacias DESC LIMIT 5
DB --> Svc: MapaCalorDemandaInsatisfecha[]
deactivate DB

Svc --> API: TableroAnaliticoDTO {metricas, mapaDemanda, tasaQuorum, csat}
deactivate Svc

API --> UI: HTTP 200 OK TableroAnaliticoDTO
deactivate API

UI --> User: Renderiza KPIs (quórum 84%, ausentismo 12%, satisfacción 4.7/5 y gráficas)
deactivate UI

== 2. Exportación de Informe Ejecutivo en PDF para Consejo Directivo ==
User -> UI: Clic en "Exportar Informe Ejecutivo (PDF)"
activate UI

UI -> API: POST /api/v1/analitica/exportar/pdf\n{semestre: '2026-I', incluirGraficos: true, formato: 'OFICIAL_EPIS'}
activate API

API -> Svc: compilarDossierEjecutivo(semestre, payload)
activate Svc

Svc -> Compiler: generarDocumentoPDF(datosConsolidados)
activate Compiler
Compiler --> Svc: StreamBinarioPDF (Documento foliado en alta resolución)
deactivate Compiler

Svc --> API: ResponseStream(application/pdf, filename="INFORME-ANALITICA-EPIS-2026-I.pdf")
deactivate Svc

API --> UI: HTTP 200 OK (Stream Binario PDF)
deactivate API

UI --> User: Descarga directa del dossier analítico formal
deactivate UI

== 3. Exportación de Dataset Anonimizado para Investigación (FA02 / RN-13) ==
User -> UI: Clic en "Exportar Dataset Anonimizado (CSV)"
activate UI

UI -> API: GET /api/v1/analitica/exportar/dataset-investigacion?semestre=2026-I [Bearer JWT]
activate API

API -> Svc: generarDatasetAnonimizado('2026-I', idUsuario)
activate Svc

Svc -> DB: SELECT e.id_sesion, e.id_estudiante, u.codigo_estudiante, e.puntaje_general,\n       e.comentarios, s.id_asignatura, s.modalidad\nFROM encuestas_calidad e\nJOIN usuarios u ON e.id_estudiante = u.id\nJOIN sesiones_mentoria s ON e.id_sesion = s.id\nWHERE s.semestre = '2026-I'
activate DB
DB --> Svc: FilasTransaccionalesSinAnonimizar[]

Svc -> AnonSvc: procesarDisociacionCriptografica(filas, saltSecreto)
activate AnonSvc
loop Para cada registro de estudiante
    AnonSvc -> AnonSvc: hashEstudiante = SHA256(id_estudiante + salt)
    AnonSvc -> AnonSvc: suprimir(codigo_estudiante, nombres)
    AnonSvc -> AnonSvc: anonimizarComentariosSensibles()
end
AnonSvc --> Svc: DatasetAnonimizadoDTO[] (Ley N° 29733 / RN-13)
deactivate AnonSvc

Svc -> DB: INSERT INTO registros_auditoria_admin (id_usuario_admin, accion, entidad, detalle)\nVALUES (:idUsuario, 'EXPORT_DATASET_ANONIMO', 'analitica', 'Descarga dataset educacional')
DB --> Svc: Auditoría Registrada
deactivate DB

Svc -> Compiler: serializarCSV(DatasetAnonimizadoDTO[])
activate Compiler
Compiler --> Svc: StreamBinarioCSV
deactivate Compiler

Svc --> API: ResponseStream(text/csv, filename="DATASET-MENTORIAS-2026-I-ANON.csv")
deactivate Svc

API --> UI: HTTP 200 OK (Stream CSV Seguro)
deactivate API

UI --> User: Descarga archivo tabular sin datos de carácter personal
deactivate UI
@enduml
```

Fuente: Elaboración propia.

El diagrama de secuencia de CUS14 formaliza el equilibrio entre accesibilidad analítica y preservación estricta de la privacidad. Las consultas estadísticas complejas operan sobre réplicas de lectura optimizadas para tareas OLAP, evitando degradar los tiempos de respuesta de los módulos transaccionales de reservas y asistencia. Por su parte, la inclusión del servicio criptográfico `AnonimizationService` garantiza que los microdatos de evaluaciones docentes sean sometidos a un proceso de hash salteado con clave efímera antes de la compilación tabular, blindando la identidad estudiantil conforme a la Ley N° 29733 y a la regla `RN-13`.

---

## 6.3.4. Diagrama de Clases del Modelo Lógico

### Presentación del Diagrama de Clases
El diagrama de clases del modelo lógico formaliza la estructura estática analítica del software, especificando las clases de entidad, sus atributos tipados con visibilidad, sus métodos de negocio representativos y las relaciones de agregación, composición y asociación que rigen el dominio de la EPIS-UPT. A diferencia del modelo conceptual preliminar, este diagrama incorpora las operaciones requeridas para dar soporte a los 26 Requerimientos Funcionales y a las 14 Reglas de Negocio, sirviendo como especificación directa para el modelado relacional en Supabase y los esquemas Pydantic / SQLAlchemy en FastAPI.

A continuación, se presenta el diagrama de clases del modelo lógico.

### Diagrama 6.16: Diagrama de Clases del Modelo Lógico del Sistema Web P2P

```plantuml
@startuml
title Diagrama de Clases del Modelo Lógico - Sistema Web P2P EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

' ===================================================
' ENUMERADOS
' ===================================================
enum RolEnum {
  MENTOREADO
  MENTOR
  ADMINISTRADOR
}

enum ModalidadEnum {
  PRESENCIAL
  VIRTUAL
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

' ===================================================
' CLASES DEL MODELO LÓGICO
' ===================================================
class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
  -hash_contrasena: String
  -consentimiento_ley29733: Boolean
  -fecha_consentimiento: DateTime
  -estado_activo: Boolean
  +validarConsentimientoLey29733(): Boolean
  +autenticar2FA(codigoOTP: String): Boolean
  +actualizarPerfil(datos: PerfilDTO): Void
  +asignarRol(nuevoRol: RolEnum): Void
}

class PerfilAcademico {
  -id_perfil: UUID
  -id_usuario: UUID
  -ciclo_actual: Integer
  -biografia: String
  -telefono_contacto: String
  -enlace_linkedin: String
  -enlace_github: String
  -matriz_disponibilidad_json: JSON
  +actualizarMatrizDisponibilidad(matriz: JSON): Boolean
  +obtenerVectorPreferencia(): Float[]
}

class AsignaturaFiltro {
  -id_asignatura: Integer
  -codigo_curso: String
  -nombre_curso: String
  -ciclo_plan: Integer
  -creditos: Integer
  -es_prioritaria: Boolean
  -factor_ponderacion: Float
  +marcarPrioridad(estado: Boolean, factor: Float): Void
  +obtenerTemasActivos(): TemaConceptual[]
}

class TemaConceptual {
  -id_tema: Integer
  -id_asignatura: Integer
  -nombre_tema: String
  -descripcion_silabo: String
  -estado_activo: Boolean
  +actualizarDescripcion(nuevaDesc: String): Void
}

class OfertaMentoria {
  -id_oferta: UUID
  -id_mentor: UUID
  -id_asignatura: Integer
  -id_tema: Integer
  -fecha_sesion: Date
  -hora_inicio: Time
  -hora_fin: Time
  -modalidad: ModalidadEnum
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -estado: EstadoSesionEnum
  -id_espacio_fisico: Integer
  -id_espacio_virtual: Integer
  +publicarOferta(): Boolean
  +verificarAntelacion48h(): Boolean
  +evaluarQuorum24h(): Float
  +reprogramarSesion(nuevaFecha: Date, nuevaHora: Time, motivo: String): Void
  +cancelarSesion(motivo: String): Void
}

class ReservaCupo {
  -id_reserva: UUID
  -id_sesion: UUID
  -id_mentoreado: UUID
  -fecha_reserva: DateTime
  -fecha_confirmacion: DateTime
  -estado: EstadoReservaEnum
  -codigo_qr_ticket: String
  -asistencia_efectiva: Boolean
  +reservarVacante(): Boolean
  +confirmarAsistencia(): Boolean
  +desistirReserva(): Boolean
  +revocarPorMorosidad(): Void
  +marcarAsistencia(presente: Boolean): Void
}

class EspacioFisico {
  -id_espacio: Integer
  -codigo_aula: String
  -pabellon: String
  -capacidad: Integer
  -equipamiento: String
  +consultarDisponibilidad(dia: Integer, hora: Time): Boolean
}

class EspacioVirtual {
  -id_virtual: Integer
  -plataforma: String
  -url_reunion_meet: String
  -canal_discord_id: String
  +generarEnlaceVideollamada(): String
  +revocarSala(): Void
}

class BitacoraSesion {
  -id_bitacora: UUID
  -id_sesion: UUID
  -temas_cubiertos: String
  -observaciones_pedagogicas: String
  -total_asistentes_reales: Integer
  -horas_pedagogicas_dictadas: Integer
  -fecha_cierre: DateTime
  -estado_visado: String
  -auditor_id: UUID
  +cerrarBitacora(asistencias: Map, resumen: String): Boolean
  +visarBitacora(auditorId: UUID): Void
  +observarBitacora(motivo: String): Void
}

class EncuestaSatisfaccion {
  -id_encuesta: UUID
  -id_reserva: UUID
  -score_dominio_tecnico: Integer
  -score_claridad_pedagogica: Integer
  -score_puntualidad: Integer
  -score_calidad_material: Integer
  -comentario_cualitativo: String
  -fecha_registro: DateTime
  +calcularPromedioEncuesta(): Float
  +anonimizarFeedback(): String
}

class SolicitudDemanda {
  -id_demanda: UUID
  -id_estudiante: UUID
  -id_asignatura: Integer
  -id_tema: Integer
  -descripcion_dificultad: String
  -modalidad_preferida: ModalidadEnum
  -franja_horaria_propuesta: String
  -fecha_creacion: DateTime
  -estado_atendida: Boolean
  +marcarComoAtendida(): Void
}

class ReputacionGamificacion {
  -id_reputacion: UUID
  -id_mentor: UUID
  -score_global_promedio: Float
  -total_horas_acumuladas: Integer
  -tasa_cumplimiento_bitacoras: Float
  -tasa_asistencia_grupal: Float
  -insignias_otorgadas_json: JSON
  +recalcularScoreCompuesto(): Float
  +desbloquearInsignia(nombreInsignia: String): Void
}

class CertificadoMentor {
  -id_certificado: UUID
  -id_mentor: UUID
  -semestre_lectivo: String
  -correlativo_resolucion: String
  -total_horas_reconocidas: Integer
  -hash_sha256_verificacion: String
  -url_documento_pdf: String
  -fecha_emision: Date
  +calcularHashVerificacion(): String
  +validarAutenticidadHash(hashEntrante: String): Boolean
}

' ===================================================
' RELACIONES ESTRUCTURALES
' ===================================================
Usuario "1" *-- "1" PerfilAcademico : compone
Usuario "1" -- "0..*" OfertaMentoria : dicta (Mentor)
Usuario "1" -- "0..*" ReservaCupo : inscribe (Mentoreado)
Usuario "1" -- "0..*" SolicitudDemanda : solicita
Usuario "1" -- "0..1" ReputacionGamificacion : posee
Usuario "1" -- "0..*" CertificadoMentor : recibe

AsignaturaFiltro "1" *-- "1..*" TemaConceptual : desglosa
AsignaturaFiltro "1" -- "0..*" OfertaMentoria : clasifica
AsignaturaFiltro "1" -- "0..*" SolicitudDemanda : agrupa

OfertaMentoria "1" *-- "0..*" ReservaCupo : administra
OfertaMentoria "1" -- "0..1" EspacioFisico : asigna aula
OfertaMentoria "1" -- "0..1" EspacioVirtual : aprovisiona sala
OfertaMentoria "1" *-- "0..1" BitacoraSesion : documenta cierre

ReservaCupo "1" -- "0..1" EncuestaSatisfaccion : evalúa (asistente)
EncuestaSatisfaccion "1..*" ..> ReputacionGamificacion : alimenta cálculo
BitacoraSesion "1..*" ..> CertificadoMentor : sustenta horas
@enduml
```

Fuente: Elaboración propia.

El análisis del diagrama de clases del modelo lógico evidencia la completa cohesión y acoplamiento controlado del sistema:
1. **Gobernanza Rigurosa de Estados:** Los tipos enumerados (`EstadoSesionEnum`, `EstadoReservaEnum`, `ModalidadEnum`, `RolEnum`) eliminan ambigüedades en la máquina de estados, impidiendo transiciones inválidas entre fases operativas.
2. **Encapsulamiento y Métricas Auditables:** La separación de `PerfilAcademico`, `ReputacionGamificacion` y `BitacoraSesion` garantiza que el cálculo de reputación y la acreditación de horas se sustenten exclusivamente en datos visados y verificados.
3. **Trazabilidad Criptográfica de Certificados:** La entidad `CertificadoMentor` almacena el hash criptográfico SHA-256 generado al emitir la constancia oficial en PDF/A, habilitando una verificación pública institucional mediante código QR que previene adulteraciones en la convalidación de méritos universitarios.

### 6.3.4.1. CUS01 – Vista Lógica Parcial de Clases: Iniciar Sesión Institucional con 2FA

La vista lógica parcial para `CUS01` delimita el conjunto de clases de dominio, servicios de aplicación y adaptadores de infraestructura que participan en la autenticación institucional multifactor (2FA) y en la gobernanza de datos bajo la Ley N° 29733. Se explicitan los atributos privados fuertemente tipados, las operaciones públicas de verificación de negocio, los tipos enumerados de gobernanza de estados (`RolEnum`, `EstadoOTPEnum`) y las relaciones estructurales de composición y dependencia.

#### Diagrama 6.16.1: Diagrama de Clases Lógico Parcial - CUS01: Iniciar Sesión Institucional con 2FA

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS01: Iniciar Sesión Institucional con 2FA\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum RolEnum {
  MENTOREADO
  MENTOR
  ADMINISTRADOR
}

enum EstadoOTPEnum {
  EMITIDO
  VALIDADO
  EXPIRADO
  BLOQUEADO
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
  -rol_activo: RolEnum
  -consentimiento_ley29733: Boolean
  -fecha_consentimiento: DateTime
  -estado_activo: Boolean
  +validarPertenenciaDominio(): Boolean
  +validarConsentimientoLey29733(): Boolean
  +registrarConsentimiento(ip: String, timestamp: DateTime): Void
}

class CredencialOTP {
  -id_otp: UUID
  -id_usuario: UUID
  -hash_codigo: String
  -fecha_emision: DateTime
  -fecha_expiracion: DateTime
  -intentos_fallidos: Integer
  -estado: EstadoOTPEnum
  -consumido: Boolean
  +generarClaveAleatoria(): String
  +validarVigenciaTemporal(): Boolean
  +registrarIntentoFallido(): Boolean
  +marcarConsumido(): Void
}

class RegistroConsentimiento {
  -id_consentimiento: UUID
  -id_usuario: UUID
  -version_politica: String
  -direccion_ip: String
  -user_agent: String
  -fecha_aceptacion: DateTime
  +generarConstanciaAuditoria(): JSON
}

class SesionTokenJWT {
  -token_string: String
  -id_usuario: UUID
  -rol_asociado: RolEnum
  -fecha_emision: DateTime
  -fecha_expiracion: DateTime
  +validarFirmaCriptografica(): Boolean
  +estaExpirado(): Boolean
}

class AuthService {
  +solicitarCodigoOTP(correo: String): Boolean
  +verificarCodigoOTP(correo: String, codigo: String): SesionTokenJWT
  +formalizarConsentimiento(idUsuario: UUID, ip: String): Boolean
}

class AdaptadorSMTP {
  -servidor_host: String
  -puerto: Integer
  -usuario_servicio: String
  +enviarPlantillaOTP(destinatario: String, codigo: String): Boolean
}

Usuario "1" *-- "0..*" CredencialOTP : genera
Usuario "1" -- "0..1" RegistroConsentimiento : formaliza
Usuario "1" ..> "0..*" SesionTokenJWT : origina
AuthService ..> Usuario : consulta y actualiza
AuthService ..> CredencialOTP : administra ciclo de vida
AuthService ..> RegistroConsentimiento : persiste traza
AuthService ..> AdaptadorSMTP : delega despacho
AuthService ..> SesionTokenJWT : construye
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial valida la alta cohesión del subsistema de seguridad: la entidad `CredencialOTP` encapsula el control de vigencia perentoria (5 minutos) y el conteo de fallos de validación; `RegistroConsentimiento` desacopla la auditoría legal exigida por la normativa peruana; y `AuthService` articula la emisión de `SesionTokenJWT` sin acoplar la capa de dominio a los detalles de conectividad del protocolo SMTP universitario.

### 6.3.4.2. CUS04 – Vista Lógica Parcial de Clases: Reservar Cupo de Mentoría

La vista lógica parcial para `CUS04` delimita las clases del modelo lógico, servicios de aplicación y repositorios que hacen posible la reserva concurrente de cupos bajo control de aforo (RN-05). Se especifican las entidades `Usuario`, `SesionMentoria` y `ReservaCupo`, sus atributos privados, visibilidades y métodos de negocio críticos, así como los tipos enumerados de gobernanza (`EstadoSesionEnum`, `EstadoReservaEnum`, `ModalidadEnum`) y el servicio de aplicación `ReservaService`.

#### Diagrama 6.16.2: Diagrama de Clases Lógico Parcial - CUS04: Reservar Cupo de Mentoría

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS04: Reservar Cupo de Mentoría\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum ModalidadEnum {
  PRESENCIAL
  VIRTUAL
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
  -ciclo_actual: Integer
  -estado_activo: Boolean
  +validarElegibilidadCiclo(cicloRequerido: Integer): Boolean
  +estaHabilitado(): Boolean
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -id_asignatura: Integer
  -modalidad: ModalidadEnum
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -fecha_hora_inicio: DateTime
  -estado: EstadoSesionEnum
  +hayCuposDisponibles(): Boolean
  +calcularAforoSegunModalidad(): Integer
  +incrementarCuposOcupados(): Boolean
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -fecha_reserva: DateTime
  -fecha_confirmacion: DateTime
  -estado: EstadoReservaEnum
  +crearReservaPendiente(idUsuario: UUID, idSesion: UUID): ReservaCupo
  +calcularLimiteConfirmacionT24(): DateTime
}

class ReservaService {
  +solicitarReservaCupo(idUsuario: UUID, idSesion: UUID): ReservaCupo
  +validarAusenciaCrucesHorarios(idUsuario: UUID, fechaHora: DateTime): Boolean
}

class ReservaRepository {
  +bloquearSesionParaActualizacion(idSesion: UUID): SesionMentoria
  +insertarReserva(reserva: ReservaCupo): UUID
  +actualizarContadorCupos(idSesion: UUID, nuevosCupos: Integer): Void
  +verificarReservaExistente(idUsuario: UUID, idSesion: UUID): Boolean
}

Usuario "1" -- "0..*" ReservaCupo : registra
SesionMentoria "1" *-- "0..*" ReservaCupo : administra
ReservaService ..> Usuario : consulta elegibilidad
ReservaService ..> SesionMentoria : valida aforo
ReservaService ..> ReservaCupo : instancia
ReservaService ..> ReservaRepository : delega persistencia
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS04 modela el acoplamiento mínimo y la alta cohesión de las entidades de reserva: `SesionMentoria` encapsula las reglas de aforo diferencial (10 para presencial, 20 para virtual, según RN-05); `ReservaCupo` almacena el ciclo de vida de la plaza inscrita iniciando rigurosamente en `PENDIENTE_CONFIRMACION`; y `ReservaService` colabora con `ReservaRepository` para ejecutar transacciones protegidas con bloqueo pesimista en la base de datos PostgreSQL, garantizando la consistencia ACID exigida por RNF04.

### 6.3.4.3. CUS24 – Vista Lógica Parcial de Clases: Confirmar Asistencia a Mentoría

La vista lógica parcial para `CUS24` delimita las clases del modelo analítico involucradas en la ratificación formal de asistencia y emisión del ticket digital con código QR. Se especifican los atributos privados y métodos de negocio de `Usuario`, `SesionMentoria`, `ReservaCupo` y `TicketAsistencia`, junto con la capa de coordinación `ConfirmacionService` y el adaptador de notificación `AdaptadorSMTP`.

#### Diagrama 6.16.3: Diagrama de Clases Lógico Parcial - CUS24: Confirmar Asistencia a Mentoría

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS24: Confirmar Asistencia a Mentoría\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
}

class SesionMentoria {
  -id_sesion: UUID
  -fecha_hora_inicio: DateTime
  -modalidad: String
  -aula_asignada: String
  -enlace_reunion: String
  +estaEnVentanaConfirmacion(): Boolean
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -fecha_reserva: DateTime
  -fecha_confirmacion: DateTime
  -estado: EstadoReservaEnum
  +confirmarAsistencia(): Boolean
  +esConfirmable(): Boolean
}

class TicketAsistencia {
  -id_ticket: UUID
  -id_reserva: UUID
  -hash_seguridad: String
  -imagen_qr_base64: String
  -fecha_generacion: DateTime
  +validarFirma(): Boolean
}

class ConfirmacionService {
  +ratificarReserva(idReserva: UUID, idUsuario: UUID): TicketAsistencia
  +validarVentanaCorte(fechaInicio: DateTime): Boolean
}

class AdaptadorSMTP {
  +despacharTicketConfirmacion(destinatario: String, ticket: TicketAsistencia): Boolean
}

Usuario "1" -- "0..*" ReservaCupo : posee
SesionMentoria "1" *-- "0..*" ReservaCupo : agrupa
ReservaCupo "1" -- "0..1" TicketAsistencia : genera
ConfirmacionService ..> ReservaCupo : transiciona
ConfirmacionService ..> SesionMentoria : valida regla RN-08
ConfirmacionService ..> TicketAsistencia : instancia
ConfirmacionService ..> AdaptadorSMTP : delega notificación
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS24 confirma que la ratificación preserva la inmutabilidad de la relación original y se concentra en la mutación de estado de `ReservaCupo` hacia `CONFIRMADA`. La introducción de la clase de entidad `TicketAsistencia` desacopla la generación del hash de seguridad y la imagen QR en Base64, asegurando que el token de control de asistencia cuente con los atributos criptográficos necesarios para ser escaneado por el mentor en la bitácora de cierre (CUS08).

### 6.3.4.4. CUS23 – Vista Lógica Parcial de Clases: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

La vista lógica parcial para `CUS23` modela las clases del sistema responsables del procesamiento por lotes desatendido, la ejecución transaccional del corte de reservas morosas y la evaluación algorítmica de quórum según RN-09. Se especifican los atributos privados y métodos de negocio de `SesionMentoria`, `ReservaCupo`, `Usuario`, junto a la capa de infraestructura y coordinación compuesta por `CronQuorumService`, `EvaluadorQuorumRepository` y el adaptador `AdaptadorEmailSMTP`.

#### Diagrama 6.16.4: Diagrama de Clases Lógico Parcial - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS23: Ejecutar Alertas y Evaluación Automática de Quórum en T-24h\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
  -estado_activo: Boolean
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -fecha_hora_inicio: DateTime
  -estado: EstadoSesionEnum
  +evaluarQuorumMinimo(confirmados: Integer): Boolean
  +actualizarEstadoSesion(nuevoEstado: EstadoSesionEnum): Void
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -fecha_reserva: DateTime
  -fecha_confirmacion: DateTime
  -estado: EstadoReservaEnum
  +revocarPorFaltaConfirmacion(): Void
}

class CronQuorumService {
  +ejecutarCicloCorteT24(): ResumenCorteDTO
  +procesarCorteSesion(idSesion: UUID): Boolean
}

class EvaluadorQuorumRepository {
  +obtenerSesionesCorteT24(): List<SesionMentoria>
  +marcarReservasNoConfirmadas(idSesion: UUID): Integer
  +contarReservasConfirmadas(idSesion: UUID): Integer
  +persistirEstadoSesion(idSesion: UUID, estado: EstadoSesionEnum): Void
}

class AdaptadorEmailSMTP {
  +despacharConfirmacionSesion(idSesion: UUID, destinatarios: List<String>): Boolean
  +despacharAlertaQuorumInsuficiente(idSesion: UUID, correoMentor: String): Boolean
}

Usuario "1" -- "0..*" ReservaCupo : posee
SesionMentoria "1" *-- "0..*" ReservaCupo : contiene
CronQuorumService ..> EvaluadorQuorumRepository : consulta y actualiza
CronQuorumService ..> SesionMentoria : evalúa regla RN-09
CronQuorumService ..> ReservaCupo : revoca estado
CronQuorumService ..> AdaptadorEmailSMTP : delega alertas
EvaluadorQuorumRepository ..> SesionMentoria : hidrata entidad
EvaluadorQuorumRepository ..> ReservaCupo : persiste cambios
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS23 explicita la lógica algorítmica para la preservación de la regla institucional RN-09. La clase de servicio `CronQuorumService` orquesta la transacción de corte a través de `EvaluadorQuorumRepository`, el cual actualiza masivamente las reservas morosas mutando su estado a `NO_CONFIRMADA`. A partir del recuento estricto de cupos en estado `CONFIRMADA`, la entidad `SesionMentoria` computa la razón de quórum ($\ge 50\%$) y actualiza su ciclo de vida hacia `CONFIRMADA` o `QUORUM_INSUFICIENTE`, delegando en `AdaptadorEmailSMTP` el despacho de las alertas institucionales pertinentes.

### 6.3.4.5. CUS07 – Vista Lógica Parcial de Clases: Gestionar Sesión ante Quórum Insuficiente

La vista lógica parcial para `CUS07` formaliza las clases y dependencias analíticas requeridas para ejecutar la resolución por quórum insuficiente. Modela las responsabilidades de las entidades `SesionMentoria`, `ReservaCupo`, `EspacioFisico` y `RegistroAuditoria`, coordinadas por la clase de servicio `ResolucionQuorumService` y comunicadas externamente mediante `AdaptadorEmailSMTP` y `AdaptadorReservaAulas`.

#### Diagrama 6.16.5: Diagrama de Clases Lógico Parcial - CUS07: Gestionar Sesión ante Quórum Insuficiente

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS07: Gestionar Sesión ante Quórum Insuficiente\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

enum DecisionQuorumEnum {
  DICTADO_EXCEPCIONAL
  CANCELAR_SESION
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -modalidad: String
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -estado: EstadoSesionEnum
  -aula_asignada: String
  -enlace_virtual: String
  +ratificarDictadoExcepcional(): Void
  +cancelarPorFaltaQuorum(): Void
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -estado: EstadoReservaEnum
  +cancelarPorSistema(): Void
}

class EspacioFisico {
  -id_aula: String
  -pabellon: String
  -capacidad: Integer
  -estado_disponibilidad: Boolean
  +liberarAmbiente(): Boolean
}

class RegistroAuditoria {
  -id_auditoria: UUID
  -id_sesion: UUID
  -tipo_evento: String
  -penalizacion: Boolean
  -regla_aplicada: String
  -fecha_registro: DateTime
  +asentarExencionPenalidad(regla: String): Void
}

class ResolucionQuorumService {
  +procesarResolucion(idSesion: UUID, idMentor: UUID, decision: DecisionQuorumEnum): Boolean
  +desasignarRecursosLogisticos(idSesion: UUID): Void
}

class AdaptadorEmailSMTP {
  +notificarDictadoExcepcional(idSesion: UUID, correos: List<String>): Boolean
  +notificarCancelacionQuorum(idSesion: UUID, correos: List<String>): Boolean
}

class AdaptadorReservaAulas {
  +liberarHorarioAmbiente(idAula: String, inicio: DateTime, fin: DateTime): Boolean
}

Usuario "1" -- "0..*" ReservaCupo : posee
SesionMentoria "1" *-- "0..*" ReservaCupo : administra
SesionMentoria "0..1" -- "0..1" EspacioFisico : utiliza
ResolucionQuorumService ..> SesionMentoria : transiciona
ResolucionQuorumService ..> ReservaCupo : muta a CANCELADA_SISTEMA
ResolucionQuorumService ..> RegistroAuditoria : asienta constancia
ResolucionQuorumService ..> AdaptadorReservaAulas : libera aula
ResolucionQuorumService ..> AdaptadorEmailSMTP : despacha avisos
AdaptadorReservaAulas ..> EspacioFisico : actualiza disponibilidad
@enduml
```

Fuente: Elaboración propia.

El modelo de clases parcial de CUS07 formaliza la arquitectura que sostiene la regla RN-10 de indemnidad docente y estudiantil ante quórum insuficiente. `ResolucionQuorumService` ejecuta la decisión gobernada por el mentor (`DecisionQuorumEnum`), coordinando con la entidad `SesionMentoria` para su transición a `CONFIRMADA_EXCEPCIONAL` o `CANCELADA_QUORUM`. En caso de cancelación, el servicio instruye a `ReservaCupo` para anular las confirmaciones sin demérito (`CANCELADA_SISTEMA`), devuelve los espacios físicos a disponibilidad mediante `AdaptadorReservaAulas` e inserta en `RegistroAuditoria` el comprobante de no-penalización para resguardo institucional.

### 6.3.4.6. CUS09 – Vista Lógica Parcial de Clases: Publicar Oferta de Mentoría Individual o Grupal

La vista lógica parcial para `CUS09` delimita las clases del modelo analítico involucradas en la definición, parametrización y persistencia de ofertas de mentoría. Se especifican los atributos privados y métodos de negocio de `SesionMentoria`, `Asignatura`, `EspacioFisico`, `EspacioVirtual` y `Usuario`, junto a la capa de coordinación `PublicacionService` y los adaptadores de infraestructura física y virtual.

#### Diagrama 6.16.6: Diagrama de Clases Lógico Parcial - CUS09: Publicar Oferta de Mentoría Individual o Grupal

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS09: Publicar Oferta de Mentoría Individual o Grupal\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum ModalidadEnum {
  PRESENCIAL
  VIRTUAL
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -correo_institucional: String
  -nombres: String
  -apellidos: String
  -ciclo_actual: Integer
  -estado_activo: Boolean
  +validarElegibilidadMentor(): Boolean
}

class Asignatura {
  -id_asignatura: Integer
  -codigo_asignatura: String
  -nombre_asignatura: String
  -ciclo_pertenencia: Integer
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -id_asignatura: Integer
  -titulo: String
  -descripcion: String
  -modalidad: ModalidadEnum
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -fecha_hora_inicio: DateTime
  -estado: EstadoSesionEnum
  +validarAnticipacion48h(): Boolean
  +validarLimiteAforo(): Boolean
  +publicar(): Void
}

class EspacioFisico {
  -id_aula: String
  -pabellon: String
  -capacidad: Integer
  -esta_disponible: Boolean
  +reservarParaSesion(inicio: DateTime, fin: DateTime): Boolean
}

class EspacioVirtual {
  -id_espacio: UUID
  -url_reunion: String
  -plataforma: String
  -proveedor_api: String
}

class PublicacionService {
  +crearSesionMentoria(datos: SesionDTO, idMentor: UUID): SesionMentoria
  +verificarDisponibilidadHoraria(idMentor: UUID, fechaHora: DateTime): Boolean
}

class SesionRepository {
  +insertarSesion(sesion: SesionMentoria): UUID
  +existeSolapamientoMentor(idMentor: UUID, fechaHora: DateTime): Boolean
}

Usuario "1" -- "0..*" SesionMentoria : crea
Asignatura "1" -- "0..*" SesionMentoria : clasifica
SesionMentoria "0..1" -- "0..1" EspacioFisico : asigna aula
SesionMentoria "0..1" -- "0..1" EspacioVirtual : asigna sala
PublicacionService ..> Usuario : valida rol RN-01
PublicacionService ..> SesionMentoria : orquesta reglas RN-04 y RN-05
PublicacionService ..> SesionRepository : persiste entidad
@enduml
```

Fuente: Elaboración propia.

El modelo de clases parcial de CUS09 explicita el acoplamiento y las restricciones estáticas que gobiernan la emisión de mentorías. `PublicacionService` actúa como orquestador de dominio validando con `Usuario` la habilitación académica del mentor (RN-01), mientras que `SesionMentoria` encapsula las reglas invariantes de anticipación temporal ($\ge 48\text{ h}$, RN-04) y el límite paramétrico de aforos según modalidad (RN-05). La asignación polimórfica de ambientes hacia `EspacioFisico` o `EspacioVirtual` asegura que la sesión nazca en estado `PUBLICADA` con todos sus recursos de infraestructura formalmente asegurados.

### 6.3.4.7. CUS14 – Vista Lógica Parcial de Clases: Consultar Agenda y Horarios de Mentorías

La vista lógica parcial para `CUS14` define las clases del modelo analítico involucradas en la provisión de información de agenda, filtrado multidimensional y cálculo dinámico de aforo libre. Se especifican los atributos privados y métodos de consulta de `SesionMentoria`, `Asignatura`, `Usuario`, los objetos de transferencia de datos `FiltrosAgendaDTO` e `ItemAgendaDTO`, coordinados por `AgendaService` y apoyados en `SesionRepository` y `CacheManager`.

#### Diagrama 6.16.7: Diagrama de Clases Lógico Parcial - CUS14: Consultar Agenda y Horarios de Mentorías

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS14: Consultar Agenda y Horarios de Mentorías\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}
skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum ModalidadEnum {
  PRESENCIAL
  VIRTUAL
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -id_asignatura: Integer
  -titulo: String
  -modalidad: ModalidadEnum
  -aforo_maximo: Integer
  -cupos_ocupados: Integer
  -fecha_hora_inicio: DateTime
  -estado: EstadoSesionEnum
  +calcularCuposDisponibles(): Integer
  +estaDisponibleParaInscripcion(): Boolean
}

class Asignatura {
  -id_asignatura: Integer
  -codigo_asignatura: String
  -nombre_asignatura: String
  -ciclo_pertenencia: Integer
}

class Usuario {
  -id_usuario: UUID
  -nombres: String
  -apellidos: String
  -correo_institucional: String
}

class FiltrosAgendaDTO {
  +mes: Integer
  +anio: Integer
  +idAsignatura: Integer
  +modalidad: ModalidadEnum
}

class ItemAgendaDTO {
  +idSesion: UUID
  +titulo: String
  +nombreAsignatura: String
  +nombreMentor: String
  +fechaHoraInicio: DateTime
  +modalidad: ModalidadEnum
  +aforoMaximo: Integer
  +cuposDisponibles: Integer
  +inscritoPorUsuario: Boolean
}

class AgendaService {
  +consultarAgendaMensual(filtros: FiltrosAgendaDTO, idUsuario: UUID): List<ItemAgendaDTO>
  +invalidarCacheAgenda(): Void
}

class SesionRepository {
  +buscarPorRangoYFiltros(inicio: DateTime, fin: DateTime, filtros: FiltrosAgendaDTO): List<SesionMentoria>
  +verificarInscripcion(idSesion: UUID, idUsuario: UUID): Boolean
}

class CacheManager {
  +obtener(clave: String): String
  +almacenar(clave: String, valor: String, ttlSegundos: Integer): Void
}

AgendaService ..> FiltrosAgendaDTO : recibe
AgendaService ..> ItemAgendaDTO : produce
AgendaService ..> SesionRepository : consulta
AgendaService ..> CacheManager : gestiona aceleración
SesionRepository ..> SesionMentoria : recupera
SesionRepository ..> Asignatura : relaciona
SesionRepository ..> Usuario : relaciona mentor
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS14 modela la capa de lectura y serialización optimizada para la agenda institucional. `AgendaService` orquesta la recuperación de datos mediante `SesionRepository`, enriqueciendo la información con el cálculo dinámico de vacantes disponibles en la entidad `SesionMentoria` (`aforo_maximo - cupos_ocupados`, conforme a RN-05). La incorporación de `CacheManager` asegura el cumplimiento de RNF01 desacoplando la consulta de la persistencia directa, mientras que `ItemAgendaDTO` encapsula el estado exacto de cada sesión de mentoría para su renderizado directo en la interfaz SPA.

### 6.3.4.8. CUS11 - Vista Lógica Parcial de Clases: Registrar Asistencia Mediante Código QR

La vista lógica parcial para `CUS11` delimita el conjunto de clases de dominio, servicios de aplicación, esquemas de transferencia y repositorios que estructuran el subsistema de validación de asistencia y verificación óptica. Se especifican los atributos privados y métodos de negocio de `SesionMentoria`, `ReservaCupo`, `TicketAsistencia` y `RegistroAsistencia`, junto con la capa de coordinación `AsistenciaService`, el verificador criptográfico `QRTokenVerifier` y el enumerado `MetodoAsistenciaEnum`.

#### Diagrama 6.16.8: Diagrama de Clases Lógico Parcial - CUS11: Registrar Asistencia Mediante Código QR

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS11: Registrar Asistencia Mediante Código QR\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

enum EstadoTicketEnum {
  EMITIDO
  CONSUMIDO
  EXPIRADO
}

enum MetodoAsistenciaEnum {
  ESCANEO_QR
  MANUAL_MENTOR
  REGULARIZACION_BITACORA
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -fecha_reserva: DateTime
  -estado: EstadoReservaEnum
  +marcarAsistida(): Void
  +esValidaParaRegistro(): Boolean
}

class TicketAsistencia {
  -id_ticket: UUID
  -id_reserva: UUID
  -codigo_hash: String
  -fecha_emision: DateTime
  -fecha_expiracion: DateTime
  -estado: EstadoTicketEnum
  +consumirTicket(): Void
  +estaVigente(ahora: DateTime): Boolean
}

class RegistroAsistencia {
  -id_asistencia: UUID
  -id_reserva: UUID
  -id_usuario: UUID
  -registrado_por: UUID
  -metodo: MetodoAsistenciaEnum
  -fecha_hora_registro: DateTime
  -observacion: String
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -fecha_hora_inicio: DateTime
  -fecha_hora_fin: DateTime
  +estaEnVentanaAsistencia(ahora: DateTime): Boolean
}

class EscaneoQRDTO {
  +idTicket: UUID
  +idReserva: UUID
  +tokenFirma: String
  +timestampLectura: Long
}

class ResultadoAsistenciaDTO {
  +exitoso: Boolean
  +idReserva: UUID
  +nombreEstudiante: String
  +horaMarcacion: DateTime
  +mensaje: String
}

class QRTokenVerifier {
  -secretKey: String
  +verificarFirma(idTicket: UUID, idReserva: UUID, token: String): Boolean
  +calcularHash(payload: String): String
}

class AsistenciaService {
  +registrarPorQR(dto: EscaneoQRDTO, idMentor: UUID): ResultadoAsistenciaDTO
  +validarVentanaTolerancia(fechaInicio: DateTime, ahora: DateTime): Boolean
}

class AsistenciaRepository {
  +bloquearParaActualizacion(idReserva: UUID, idTicket: UUID): Boolean
  +actualizarEstadosAsistencia(idReserva: UUID, idTicket: UUID): Void
  +crearRegistroAuditoria(registro: RegistroAsistencia): Void
}

ReservaCupo "1" *-- "1" TicketAsistencia : emite
ReservaCupo "1" *-- "0..1" RegistroAsistencia : acredita
SesionMentoria "1" o-- "1..*" ReservaCupo : administra
AsistenciaService ..> EscaneoQRDTO : procesa
AsistenciaService ..> ResultadoAsistenciaDTO : genera
AsistenciaService ..> QRTokenVerifier : valida criptografía
AsistenciaService ..> AsistenciaRepository : persiste
AsistenciaRepository ..> ReservaCupo : muta
AsistenciaRepository ..> TicketAsistencia : muta
AsistenciaRepository ..> RegistroAsistencia : inserta
@enduml
```

Fuente: Elaboración propia.

El modelo de clases lógico parcial de CUS11 define un acoplamiento cohesivo orientado a la integridad transaccional. La clase `AsistenciaService` delega la comprobación matemática a `QRTokenVerifier`, separando la validación del protocolo criptográfico de la lógica del negocio universitario. El método `estaEnVentanaAsistencia()` en `SesionMentoria` encapsula de forma estricta la tolerancia temporal de RN-11 (-15 min a +30 min). La relación de composición entre `ReservaCupo` y `TicketAsistencia` formaliza la trazabilidad unívoca de cada cupo confirmado, asegurando que el estado `ASISTIDA` y el registro de auditoría `RegistroAsistencia` reflejen fidedignamente la asistencia efectiva requerida para la acreditación académica.

### 6.3.4.9. CUS10 - Vista Lógica Parcial de Clases: Registrar Bitácora Pedagógica de Sesión

La vista lógica parcial para `CUS10` delimita el conjunto de clases de dominio, servicios de aplicación, esquemas DTO y repositorios que estructuran el proceso de cierre académico y acreditación horaria de las sesiones de mentoría. Se especifican los atributos privados y métodos de negocio de `SesionMentoria`, `BitacoraSesion`, `ReservaCupo` y `BolsaHorasMentor`, coordinados por `BitacoraService` y apoyados en `BitacoraRepository` para asegurar la observancia de las reglas RN-07 (plazo de 24 horas), RN-11 (regularización de inasistencias) y RN-12 (acumulación de horas).

#### Diagrama 6.16.9: Diagrama de Clases Lógico Parcial - CUS10: Registrar Bitácora Pedagógica de Sesión

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS10: Registrar Bitácora Pedagógica de Sesión\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoSesionEnum {
  BORRADOR
  PUBLICADA
  CONFIRMADA
  CONFIRMADA_EXCEPCIONAL
  QUORUM_INSUFICIENTE
  EN_CURSO
  FINALIZADA
  CANCELADA_MENTOR
  CANCELADA_QUORUM
}

enum EstadoReservaEnum {
  PENDIENTE_CONFIRMACION
  CONFIRMADA
  CANCELADA_USUARIO
  NO_CONFIRMADA
  CANCELADA_SISTEMA
  ASISTIDA
  INASISTENCIA
}

enum EstadoBitacoraEnum {
  BORRADOR
  REGISTRADA
  VISADA
  OBSERVADA
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -titulo: String
  -fecha_hora_inicio: DateTime
  -fecha_hora_fin: DateTime
  -duracion_horas: Integer
  -estado: EstadoSesionEnum
  +estaEnPlazoBitacora(ahora: DateTime): Boolean
  +finalizarSesion(): Void
}

class BitacoraSesion {
  -id_bitacora: UUID
  -id_sesion: UUID
  -id_mentor: UUID
  -temas_tratados: String
  -dificultades_detectadas: String
  -observaciones_pedagogicas: String
  -horas_dictadas: Integer
  -fecha_registro: DateTime
  -estado: EstadoBitacoraEnum
  +validarLongitudTemas(): Boolean
  +asentarBitacora(): Void
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -estado: EstadoReservaEnum
  +cerrarPorInasistencia(): Void
}

class BolsaHorasMentor {
  -id_bolsa: UUID
  -id_mentor: UUID
  -horas_acumuladas: Integer
  -horas_validadas_tutoria: Integer
  -fecha_ultima_actualizacion: DateTime
  +acumularHoras(horas: Integer): Void
}

class RegistroBitacoraDTO {
  +temasTratados: String
  +dificultadesDetectadas: String
  +observacionesPedagogicas: String
}

class ContextoBitacoraDTO {
  +idSesion: UUID
  +tituloSesion: String
  +fechaHoraFin: DateTime
  +duracionHoras: Integer
  +totalAsistentes: Integer
  +totalInasistencias: Integer
}

class BitacoraService {
  +obtenerContextoSesion(idSesion: UUID, idMentor: UUID): ContextoBitacoraDTO
  +registrarBitacora(idSesion: UUID, idMentor: UUID, dto: RegistroBitacoraDTO): BitacoraSesion
}

class BitacoraRepository {
  +bloquearSesionParaCierre(idSesion: UUID): SesionMentoria
  +regularizarInasistencias(idSesion: UUID): Integer
  +guardarBitacora(bitacora: BitacoraSesion): Void
  +acumularHoras(idMentor: UUID, horas: Integer): Void
}

SesionMentoria "1" *-- "0..1" BitacoraSesion : documenta
SesionMentoria "1" o-- "1..*" ReservaCupo : comprende
BitacoraService ..> RegistroBitacoraDTO : recibe
BitacoraService ..> ContextoBitacoraDTO : produce
BitacoraService ..> BitacoraRepository : coordina
BitacoraRepository ..> SesionMentoria : muta estado
BitacoraRepository ..> BitacoraSesion : persiste
BitacoraRepository ..> ReservaCupo : actualiza inasistencias
BitacoraRepository ..> BolsaHorasMentor : incrementa horas
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS10 consolida la arquitectura del cierre docente universitario. La entidad `BitacoraSesion` salvaguarda los contenidos pedagógicos obligatorios y su validación semántica, relacionándose íntimamente con `SesionMentoria` mediante una composición unívoca. El método `estaEnPlazoBitacora()` protege la restricción temporal fijada en RN-07 (24 horas perentorias tras finalizar el evento). La interacción orquestada entre `BitacoraService` y `BitacoraRepository` asegura que las horas dictadas sean reconocidas en `BolsaHorasMentor` exclusivamente tras la persistencia atómica de la bitácora y la liquidación formal de las inasistencias (`RN-11` y `RN-12`).

### 6.3.4.10. CUS05 - Vista Lógica Parcial de Clases: Responder Encuesta de Calidad Post-Mentoría

La vista lógica parcial para `CUS05` formaliza la estructura de clases del modelo de dominio, servicios de aplicación y adaptadores de anonimización requeridos para la captura de encuestas docentes. Se especifican los atributos privados y métodos de las entidades `EncuestaSatisfaccion`, `ReputacionMentor` y `ReservaCupo`, coordinadas por `EncuestaService` y apoyadas en `AnonimizadorService` para garantizar el estricto cumplimiento de la Ley N° 29733 de Protección de Datos Personales y el cálculo de la media móvil ponderada estipulada en RN-13.

#### Diagrama 6.16.10: Diagrama de Clases Lógico Parcial - CUS05: Responder Encuesta de Calidad Post-Mentoría

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS05: Responder Encuesta de Calidad Post-Mentoría\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

class EncuestaSatisfaccion {
  -id_encuesta: UUID
  -id_sesion: UUID
  -id_mentor: UUID
  -hash_estudiante_anonimo: String
  -puntuacion_dominio: Integer
  -puntuacion_claridad: Integer
  -puntuacion_puntualidad: Integer
  -puntuacion_recursos: Integer
  -promedio_sesion: Float
  -comentario_cualitativo: String
  -fecha_registro: DateTime
  +calcularPromedio(): Float
  +esValida(): Boolean
}

class ReputacionMentor {
  -id_reputacion: UUID
  -id_mentor: UUID
  -score_promedio: Float
  -total_evaluaciones: Integer
  -nivel_reputacion: String
  -fecha_actualizacion: DateTime
  +actualizarConNuevaEvaluacion(promedioSesion: Float): Void
  +determinarNivel(): String
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -estado: EstadoReservaEnum
  -encuesta_completada: Boolean
  +marcarEncuestaCompletada(): Void
  +esAptaParaEncuesta(): Boolean
}

class BitacoraSesion {
  -id_bitacora: UUID
  -id_sesion: UUID
  -fecha_registro: DateTime
  +estaEnVentanaEvaluacion(ahora: DateTime): Boolean
}

class EnvioEncuestaDTO {
  +puntuacionDominio: Integer
  +puntuacionClaridad: Integer
  +puntuacionPuntualidad: Integer
  +puntuacionRecursos: Integer
  +comentarioCualitativo: String
}

class SesionPendienteEncuestaDTO {
  +idSesion: UUID
  +tituloSesion: String
  +nombreMentor: String
  +fechaCierreBitacora: DateTime
  +tiempoRestanteMinutos: Integer
}

class AnonimizadorService {
  -saltInstitucional: String
  +generarHashAnonimo(idUsuario: UUID, idSesion: UUID): String
  +sanitizarComentario(texto: String): String
}

class EncuestaService {
  +listarPendientes(idUsuario: UUID): List<SesionPendienteEncuestaDTO>
  +registrarEvaluacion(idSesion: UUID, idUsuario: UUID, dto: EnvioEncuestaDTO): Void
}

class EncuestaRepository {
  +verificarElegibilidad(idSesion: UUID, idUsuario: UUID): Boolean
  +marcarReservaEvaluada(idReserva: UUID): Void
  +guardarEncuesta(encuesta: EncuestaSatisfaccion): Void
  +actualizarReputacion(idMentor: UUID, promedioSesion: Float): Void
}

EncuestaSatisfaccion "0..*" -- "1" ReputacionMentor : nutre media ponderada
ReservaCupo "1" -- "0..1" EncuestaSatisfaccion : origina evaluación
BitacoraSesion "1" ..> EncuestaSatisfaccion : delimita ventana 24h
EncuestaService ..> EnvioEncuestaDTO : procesa
EncuestaService ..> SesionPendienteEncuestaDTO : retorna
EncuestaService ..> AnonimizadorService : anonimiza
EncuestaService ..> EncuestaRepository : coordina
EncuestaRepository ..> EncuestaSatisfaccion : inserta
EncuestaRepository ..> ReservaCupo : muta flag
EncuestaRepository ..> ReputacionMentor : actualiza
@enduml
```

Fuente: Elaboración propia.

El modelo de clases lógico parcial de CUS05 formaliza el acoplamiento desacoplado entre la opinión estudiantil y el historial público del mentor. `EncuestaService` actúa como fachada transaccional, recurriendo a `AnonimizadorService` para cifrar la identidad del alumno antes de que `EncuestaRepository` persista la entidad `EncuestaSatisfaccion`. La relación entre `EncuestaSatisfaccion` y `ReputacionMentor` actualiza matemáticamente la media móvil ponderada, garantizando que el sistema compute la reputación de forma incremental sin recalcular costosamente todo el histórico relacional (RNF01 y RN-13).

### 6.3.4.11. CUS19 - Vista Lógica Parcial de Clases: Consultar Historial de Sesiones y Asistencia

La vista lógica parcial para `CUS19` delimita las clases de dominio, objetos de transferencia de datos (*DTOs*), servicios de aplicación y repositorios de lectura optimizados para la consulta del expediente histórico. Se especifican los esquemas fuertemente tipados `FiltrosHistorialDTO`, `ItemHistorialDTO`, `MetricasResumenDTO` y `DetalleBitacoraHistorialDTO`, orquestados por `HistorialService` y ejecutados a través de `HistorialRepository` mediante consultas seguras bajo el esquema de seguridad RLS de PostgreSQL.

#### Diagrama 6.16.11: Diagrama de Clases Lógico Parcial - CUS19: Consultar Historial de Sesiones y Asistencia

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS19: Consultar Historial de Sesiones y Asistencia\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

class FiltrosHistorialDTO {
  +semestre: String
  +idAsignatura: Integer
  +rolFiltro: String
  +pagina: Integer
  +tamanoPagina: Integer
}

class ItemHistorialDTO {
  +idSesion: UUID
  +titulo: String
  +nombreAsignatura: String
  +rolEnSesion: String
  +modalidad: String
  +fechaHoraInicio: DateTime
  +estadoAsistencia: String
  +estadoSesion: String
  +tieneBitacora: Boolean
}

class MetricasResumenDTO {
  +totalSesiones: Integer
  +sesionesAsistidas: Integer
  +porcentajeAsistencia: Float
  +horasMentorAcumuladas: Integer
  +calcularPorcentaje(): Float
}

class HistorialPaginadoDTO {
  +items: List<ItemHistorialDTO>
  +totalItems: Integer
  +metricas: MetricasResumenDTO
}

class DetalleBitacoraHistorialDTO {
  +idSesion: UUID
  +temasTratados: String
  +dificultadesDetectadas: String
  +observacionesPedagogicas: String
  +recursosUrl: String
}

class SesionMentoria {
  -id_sesion: UUID
  -id_mentor: UUID
  -titulo: String
  -modalidad: String
  -fecha_hora_inicio: DateTime
  -estado: String
}

class ReservaCupo {
  -id_reserva: UUID
  -id_usuario: UUID
  -id_sesion: UUID
  -estado: String
}

class BitacoraSesion {
  -id_bitacora: UUID
  -id_sesion: UUID
  -temas_tratados: String
  -dificultades_detectadas: String
  -observaciones_pedagogicas: String
  -horas_dictadas: Integer
}

class HistorialService {
  +consultarHistorial(idUsuario: UUID, filtros: FiltrosHistorialDTO): HistorialPaginadoDTO
  +obtenerDetalleBitacora(idSesion: UUID, idUsuario: UUID): DetalleBitacoraHistorialDTO
}

class HistorialRepository {
  +buscarSesionesUsuario(idUsuario: UUID, filtros: FiltrosHistorialDTO): List<ItemHistorialDTO>
  +calcularMetricasUsuario(idUsuario: UUID): MetricasResumenDTO
  +recuperarBitacoraDetalle(idSesion: UUID): DetalleBitacoraHistorialDTO
}

HistorialService ..> FiltrosHistorialDTO : procesa
HistorialService ..> HistorialPaginadoDTO : produce
HistorialService ..> DetalleBitacoraHistorialDTO : produce
HistorialService ..> HistorialRepository : delega
HistorialRepository ..> SesionMentoria : consulta
HistorialRepository ..> ReservaCupo : consulta
HistorialRepository ..> BitacoraSesion : consulta
HistorialPaginadoDTO *-- "0..*" ItemHistorialDTO : contiene
HistorialPaginadoDTO *-- "1" MetricasResumenDTO : consolida
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS19 modela la segregación de responsabilidades requerida para soportar vistas analíticas de alta concurrencia. `HistorialService` actúa como punto único de entrada, estructurando la respuesta en el objeto compuesto `HistorialPaginadoDTO` para evitar transferencias redundantes. La consolidación de métricas dentro de `MetricasResumenDTO` desacopla el cálculo analítico de la persistencia directa de las entidades `SesionMentoria`, `ReservaCupo` y `BitacoraSesion`, asegurando un tiempo de serialización óptimo y una experiencia interactiva ágil en la interfaz SPA.

### 6.3.4.12. CUS16 - Vista Lógica Parcial de Clases: Consultar Tablero de Insignias y Reputación

La vista lógica parcial para `CUS16` formaliza las clases de dominio, objetos de transferencia de datos (*DTOs*), enumeraciones de estado y componentes de servicio requeridos para la cuantificación analítica del prestigio docente y el subsistema de gamificación. Se especifican los atributos privados y métodos de las entidades `ReputacionMentor`, `Insignia`, `InsigniaOtorgada` y `EncuestaSatisfaccion`, coordinadas por `GamificacionService` y soportadas en `GamificacionRepository` y `CalculadorReputacionDomain` para aplicar de forma matemática la fórmula de ponderación multivariable fijada en la regla de negocio RN-13.

#### Diagrama 6.16.12: Diagrama de Clases Lógico Parcial - CUS16: Consultar Tablero de Insignias y Reputación

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS16: Consultar Tablero de Insignias y Reputación\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum NivelMentorEnum {
  CALIBRACION
  INICIAL
  ACTIVO
  SENIOR
  DESTACADO
  MAESTRO
}

enum CategoriaInsigniaEnum {
  HORAS_DICTADAS
  CALIDAD_PEDAGOGICA
  ASISTENCIA_PERFECTA
  PUNTUALIDAD_BITACORA
}

class ReputacionMentor {
  -id_reputacion: UUID
  -id_mentor: UUID
  -score_global: Float
  -score_satisfaccion: Float
  -tasa_cumplimiento: Float
  -puntualidad_bitacoras: Float
  -nivel_reputacion: NivelMentorEnum
  -total_evaluaciones: Integer
  -fecha_actualizacion: DateTime
  +recalcularPonderado(avgLikert: Float, tasaSesiones: Float, tasaBitacoras: Float): Float
  +determinarNivel(): NivelMentorEnum
}

class Insignia {
  -id_insignia: UUID
  -codigo: String
  -nombre: String
  -descripcion: String
  -categoria: CategoriaInsigniaEnum
  -icono_url: String
  -umbral_requerido: Float
  -es_activa: Boolean
  +esAlcanzada(progresoActual: Float): Boolean
}

class InsigniaOtorgada {
  -id_otorgamiento: UUID
  -id_mentor: UUID
  -id_insignia: UUID
  -fecha_otorgamiento: DateTime
  -hash_verificacion: String
  -es_publica: Boolean
  +generarUrlVerificacion(): String
}

class EncuestaSatisfaccion {
  -id_encuesta: UUID
  -id_sesion: UUID
  -id_mentor: UUID
  -promedio_sesion: Float
  -puntuacion_dominio: Integer
  -puntuacion_claridad: Integer
  -puntuacion_puntualidad: Integer
  -puntuacion_recursos: Integer
  -comentario_cualitativo: String
  -creado_en: DateTime
}

class TableroGamificacionDTO {
  +scoreGlobal: Float
  +nivel: String
  +enCalibracion: Boolean
  +dimensiones: DesgloseDimensionesDTO
  +insigniasActivas: List<InsigniaCardDTO>
  +proximasInsignias: List<ProgresoInsigniaDTO>
  +comentariosAnonimos: List<ComentarioFeedDTO>
}

class DesgloseDimensionesDTO {
  +promedioDominio: Float
  +promedioClaridad: Float
  +promedioPuntualidad: Float
  +promedioRecursos: Float
}

class InsigniaCardDTO {
  +idOtorgamiento: UUID
  +nombre: String
  +descripcion: String
  +iconoUrl: String
  +fechaObtencion: DateTime
  +hashVerificacion: String
}

class ProgresoInsigniaDTO {
  +idInsignia: UUID
  +nombre: String
  +iconoUrl: String
  +umbralRequerido: Float
  +progresoActual: Float
  +porcentajeAvance: Float
}

class ComentarioFeedDTO {
  +comentario: String
  +fecha: DateTime
}

class GamificacionService {
  +obtenerTableroCompleto(idMentor: UUID): TableroGamificacionDTO
  +obtenerResumenPublico(idMentor: UUID): TableroGamificacionDTO
  +compartirInsignia(idOtorgamiento: UUID, idMentor: UUID): String
}

class GamificacionRepository {
  +recuperarMetricasEncuestas(idMentor: UUID): DesgloseDimensionesDTO
  +recuperarInsigniasOtorgadas(idMentor: UUID): List<InsigniaCardDTO>
  +recuperarInsigniasPendientes(idMentor: UUID): List<ProgresoInsigniaDTO>
  +asentarOtorgamiento(idMentor: UUID, idInsignia: UUID, hash: String): Void
  +actualizarScoreReputacion(idMentor: UUID, score: Float, nivel: NivelMentorEnum): Void
}

ReputacionMentor --> NivelMentorEnum : clasificado en
Insignia --> CategoriaInsigniaEnum : tipificada por
InsigniaOtorgada "0..*" -- "1" Insignia : referencia
ReputacionMentor "1" -- "0..*" InsigniaOtorgada : condecora
EncuestaSatisfaccion "0..*" -- "1" ReputacionMentor : alimenta media
GamificacionService ..> TableroGamificacionDTO : produce
GamificacionService ..> GamificacionRepository : delega
TableroGamificacionDTO *-- "1" DesgloseDimensionesDTO : contiene
TableroGamificacionDTO *-- "0..*" InsigniaCardDTO : lista
TableroGamificacionDTO *-- "0..*" ProgresoInsigniaDTO : lista
TableroGamificacionDTO *-- "0..*" ComentarioFeedDTO : lista
GamificacionRepository ..> ReputacionMentor : actualiza
GamificacionRepository ..> InsigniaOtorgada : persiste
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS16 modela la segregación de responsabilidades requerida para articular la lógica lúdica institucional. La clase de entidad `ReputacionMentor` encapsula el cálculo de la media ponderada multivariable según RN-13, derivando en las transiciones de estado representadas por `NivelMentorEnum`. La entidad `InsigniaOtorgada` desacopla el catálogo normativo estático (`Insignia`) de las condecoraciones efectivas, sellando cada logro con un hash criptográfico de fe pública. A nivel de aplicación, `GamificacionService` estructura el objeto compuesto `TableroGamificacionDTO`, permitiendo que el cliente SPA consuma en un único intercambio de red los velocímetros de score, los promedios desagregados por reactivo didáctico, el avance hacia próximas insignias y los comentarios constructivos disociados de los estudiantes.

### 6.3.4.13. CUS13 - Vista Lógica Parcial de Clases: Parametrizar y Emitir Certificados

La vista lógica parcial para `CUS13` formaliza las entidades del modelo de dominio, objetos de transferencia de datos (*DTOs*), componentes de servicio y adaptadores criptográficos necesarios para la emisión oficial de certificaciones formativas en la EPIS-UPT. Se especifican los atributos privados y métodos de negocio de las entidades `ParametroCertificacion`, `Certificado`, `BitacoraSesion` y `BolsaHorasMentor`, articuladas mediante `CertificacionService` y sustentadas en `CertificacionRepository` y `GeneradorDocumentalCriptografico` para asegurar el cumplimiento estricto de las reglas normativas RN-12 y RN-14.

#### Diagrama 6.16.13: Diagrama de Clases Lógico Parcial - CUS13: Parametrizar y Emitir Certificados

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS13: Parametrizar y Emitir Certificados\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoCertificadoEnum {
  EMITIDO
  REVOCADO
  RECTIFICADO
}

enum EstadoBitacoraEnum {
  BORRADOR
  REGISTRADA
  VISADA
  OBSERVADA
}

class ParametroCertificacion {
  -id_parametro: UUID
  -semestre: String
  -horas_minimas: Integer
  -score_minimo: Float
  -resolucion_decanato: String
  -fecha_cierre_convocatoria: DateTime
  -activo: Boolean
  +esVigente(): Boolean
  +validarUmbrales(): Boolean
}

class Certificado {
  -id_certificado: UUID
  -id_mentor: UUID
  -id_parametro: UUID
  -semestre: String
  -codigo_correlativo: String
  -horas_totales_reconocidas: Integer
  -promedio_reputacion: Float
  -fecha_emision: DateTime
  -hash_sha256: String
  -ruta_almacenamiento_pdf: String
  -qr_url: String
  -estado: EstadoCertificadoEnum
  +revocar(motivo: String): Void
  +verificarIntegridad(hashCalculado: String): Boolean
}

class BitacoraSesion {
  -id_bitacora: UUID
  -id_sesion: UUID
  -horas_dictadas: Integer
  -estado: EstadoBitacoraEnum
  +esAcreditable(): Boolean
}

class BolsaHorasMentor {
  -id_bolsa: UUID
  -id_mentor: UUID
  -horas_acumuladas: Integer
  -horas_certificadas: Integer
  +acreditarHoras(horas: Integer): Void
  +obtenerSaldoCertificable(): Integer
}

class ParametrosAcreditacionDTO {
  +semestre: String
  +horasMinimas: Integer
  +scoreMinimo: Float
  +resolucionDecanato: String
}

class CandidatoCertificacionDTO {
  +idMentor: UUID
  +codigoEstudiante: String
  +nombresCompletos: String
  +correoInstitucional: String
  +horasAuditadas: Integer
  +scoreReputacion: Float
  +esElegible: Boolean
}

class NominaElegiblesDTO {
  +candidatos: List<CandidatoCertificacionDTO>
  +totalCandidatos: Integer
  +semestre: String
}

class OrdenEmisionBatchDTO {
  +semestre: String
  +mentoresSeleccionados: List<UUID>
  +idParametro: UUID
}

class ResumenEmisionBatchDTO {
  +totalProcesados: Integer
  +totalExitosos: Integer
  +totalFallidos: Integer
  +fechaEjecucion: DateTime
}

class CertificacionService {
  +evaluarElegibilidad(dto: ParametrosAcreditacionDTO): NominaElegiblesDTO
  +emitirLoteCertificados(orden: OrdenEmisionBatchDTO): ResumenEmisionBatchDTO
  +emitirCertificadoExcepcional(idMentor: UUID, resolucion: String): Certificado
}

class CertificacionRepository {
  +guardarParametro(parametro: ParametroCertificacion): UUID
  +obtenerMentoresConHorasVisadas(semestre: String, horasMin: Integer, scoreMin: Float): List<CandidatoCertificacionDTO>
  +obtenerSiguienteCorrelativo(semestre: String): String
  +guardarCertificado(certificado: Certificado): Void
  +actualizarBolsaHoras(idMentor: UUID, horas: Integer): Void
}

class GeneradorDocumentalCriptografico {
  +componerPDFA(candidato: CandidatoCertificacionDTO, correlativo: String): Array<Byte>
  +calcularSHA256(bytes: Array<Byte>): String
  +generarCodigoQR(urlValidacion: String): String
}

Certificado --> EstadoCertificadoEnum : tipificado por
BitacoraSesion --> EstadoBitacoraEnum : gobernado por
ParametroCertificacion "1" -- "0..*" Certificado : rige
Certificado "0..*" -- "1" BolsaHorasMentor : liquida horas de
NominaElegiblesDTO *-- "0..*" CandidatoCertificacionDTO : consolida
CertificacionService ..> ParametrosAcreditacionDTO : procesa
CertificacionService ..> NominaElegiblesDTO : produce
CertificacionService ..> OrdenEmisionBatchDTO : procesa
CertificacionService ..> ResumenEmisionBatchDTO : produce
CertificacionService ..> CertificacionRepository : delega
CertificacionService ..> GeneradorDocumentalCriptografico : utiliza
CertificacionRepository ..> Certificado : persiste
CertificacionRepository ..> BolsaHorasMentor : actualiza
CertificacionRepository ..> BitacoraSesion : audita
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS13 formaliza la arquitectura institucional de certificación y fe pública. La entidad `ParametroCertificacion` salvaguarda los umbrales aprobados por la Dirección de Escuela para cada ciclo lectivo, garantizando la inmutabilidad de los criterios de acreditación. La clase `Certificado` encapsula los atributos de integridad (`hash_sha256`, `codigo_correlativo` y `qr_url`), gobernada por `EstadoCertificadoEnum`. El servicio `CertificacionService` actúa como orquestador del ciclo completo, apoyado en `GeneradorDocumentalCriptografico` para la renderización estandarizada de archivos PDF/A y en `CertificacionRepository` para la auditoría y liquidación atómica del saldo de horas en `BolsaHorasMentor`.

### 6.3.4.14. CUS09 - Vista Lógica Parcial de Clases: Descargar Certificado de Horas de Mentoría

La vista lógica parcial para `CUS09` modela las clases del dominio, objetos de transferencia (*DTOs*), componentes de servicio y adaptadores de almacenamiento requeridos para la consulta, descarga protegida y verificación pública de certificados de mentoría. Se especifican los atributos privados y métodos de las entidades `Certificado`, `Usuario` y `RegistroAuditoriaVerificacion`, coordinadas por `DescargaCertificadoService` y soportadas en `DescargaCertificadoRepository` y `StorageAdapter` para garantizar la inalterabilidad criptográfica del archivo (RNF09) y el servicio de fe pública digital institucional.

#### Diagrama 6.16.14: Diagrama de Clases Lógico Parcial - CUS09: Descargar Certificado de Horas de Mentoría

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS09: Descargar Certificado de Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

enum EstadoCertificadoEnum {
  EMITIDO
  REVOCADO
  RECTIFICADO
}

enum TipoCanalVerificacionEnum {
  DESCARGA_DIRECTA
  PORTAL_QR_PUBLICO
  API_INTERNA
}

class Certificado {
  -id_certificado: UUID
  -id_mentor: UUID
  -semestre: String
  -codigo_correlativo: String
  -horas_totales_reconocidas: Integer
  -promedio_reputacion: Float
  -fecha_emision: DateTime
  -hash_sha256: String
  -ruta_almacenamiento_pdf: String
  -qr_url: String
  -estado: EstadoCertificadoEnum
  +esVigente(): Boolean
  +validarChecksum(hashCalculado: String): Boolean
  +obtenerMetadataDescarga(): MetadataDescargaDTO
}

class RegistroAuditoriaVerificacion {
  -id_auditoria: UUID
  -hash_consultado: String
  -ip_origen: String
  -user_agent: String
  -canal: TipoCanalVerificacionEnum
  -fecha_hora: DateTime
  +registrarAcceso(): Void
}

class Usuario {
  -id_usuario: UUID
  -codigo_estudiante: String
  -nombres: String
  -apellidos: String
  -correo_institucional: String
  +obtenerNombreCompleto(): String
}

class CertificadoResumenDTO {
  +idCertificado: UUID
  +semestre: String
  +codigoCorrelativo: String
  +horasReconocidas: Integer
  +promedioReputacion: Float
  +fechaEmision: DateTime
  +qrUrl: String
  +estado: String
}

class MetadataDescargaDTO {
  +nombreArchivo: String
  +tamanoBytes: Long
  +mimeType: String
  +hashSha256: String
}

class FichaVerificacionPublicaDTO {
  +autentico: Boolean
  +codigoCorrelativo: String
  +nombreMentor: String
  +codigoEstudiante: String
  +horasAcreditadas: Integer
  +semestre: String
  +fechaEmision: DateTime
  +estado: String
  +hashSha256: String
}

class DescargaCertificadoService {
  +listarMisCertificados(idMentor: UUID): List<CertificadoResumenDTO>
  +obtenerStreamCertificado(idCertificado: UUID, idMentor: UUID): StreamBinarioDTO
  +verificarPublicamentePorHash(hashSha256: String, ip: String, ua: String): FichaVerificacionPublicaDTO
}

class DescargaCertificadoRepository {
  +buscarPorMentor(idMentor: UUID): List<Certificado>
  +buscarPorIdYMentor(idCertificado: UUID, idMentor: UUID): Certificado
  +buscarPorHash(hashSha256: String): Certificado
  +asentarAuditoriaVerificacion(auditoria: RegistroAuditoriaVerificacion): Void
}

class StorageAdapter {
  +descargarBinario(rutaAlmacenamiento: String): Array<Byte>
  +verificarExistenciaObjeto(ruta: String): Boolean
}

Certificado --> EstadoCertificadoEnum : gobernado por
RegistroAuditoriaVerificacion --> TipoCanalVerificacionEnum : clasificado por
Usuario "1" -- "0..*" Certificado : titular de
Certificado "1" ..> MetadataDescargaDTO : provee
DescargaCertificadoService ..> CertificadoResumenDTO : produce lista
DescargaCertificadoService ..> FichaVerificacionPublicaDTO : produce
DescargaCertificadoService ..> DescargaCertificadoRepository : delega
DescargaCertificadoService ..> StorageAdapter : utiliza
DescargaCertificadoRepository ..> Certificado : consulta
DescargaCertificadoRepository ..> RegistroAuditoriaVerificacion : persiste
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS09 formaliza el desacoplamiento entre la persistencia relacional de metadatos de certificación y el acceso al repositorio de objetos protegidos. La entidad `Certificado` actúa como guardiana de la integridad criptográfica mediante el método `validarChecksum()`, asegurando que ninguna discrepancia binaria pase desapercibida. A nivel de infraestructura, `StorageAdapter` aísla las llamadas a Supabase Storage, mientras que `RegistroAuditoriaVerificacion` garantiza que cualquier consulta de fe pública originada en el escaneo de un código QR quede registrada con fines forenses y estadísticos, consolidando un esquema de fe pública digital conforme al estándar institucional EPIS-UPT.

### 6.3.4.15. CUS22 - Vista Lógica Parcial de Clases: Auditar Bitácoras, Asistencia y Horas de Mentoría

La vista lógica parcial para `CUS22` modela las clases del dominio, objetos de transferencia de datos (*DTOs*), componentes de servicio y adaptadores requeridos para la fiscalización, visado y emisión de observaciones sobre las sesiones de mentoría y bitácoras docentes. Se especifican los atributos privados y métodos de negocio de las entidades `BitacoraSesion`, `SesionMentoria`, `ReservaCupo`, `BolsaHorasMentor`, `ObservacionBitacora` y `RegistroAuditoriaAdmin`, gobernadas por `AuditoriaBitacorasService` e interactuando con `NotificadorEmailInstitucionalAdapter` para garantizar el estricto apego a las reglas de negocio institucionales `RN-12` (visado docente previo para acreditación) y `RN-14` (auditoría oficial para certificación semestral).

#### Diagrama 6.16.15: Diagrama de Clases Lógico Parcial - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS22: Auditar Bitácoras, Asistencia y Horas de Mentoría\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

' ===================================================
' ENUMERADOS
' ===================================================
enum EstadoBitacoraEnum {
  BORRADOR
  REGISTRADA
  VISADA
  OBSERVADA
}

enum EstadoSesionEnum {
  PROGRAMADA
  CONFIRMADA
  EN_CURSO
  FINALIZADA
  CANCELADA_QUORUM
}

enum DictamenAuditoriaEnum {
  VISADO_APROBADO
  OBSERVACION_EMITIDA
  RECHAZADO_DISCIPLINARIO
}

enum TipoFaltaObservacionEnum {
  DISCREPANCIA_ASISTENCIA
  EVIDENCIA_INSUFICIENTE
  CONTENIDO_PEDAGOGICO_OMISO
  DESFASE_TEMPORAL
}

enum EstadoObservacionEnum {
  EMITIDA_PENDIENTE
  SUBSANADA
  EXPIRADA_RECHAZADA
}

' ===================================================
' CLASES DE ENTIDAD (MODELO DE DOMINIO)
' ===================================================
class BitacoraSesion {
  -id: UUID
  -idSesion: UUID
  -idMentor: UUID
  -idAuditorVisador: UUID
  -resumenTematico: String
  -dificultadesDetectadas: String
  -trabajoAutonomoAsignado: String
  -urlEvidenciaAdjunta: String
  -horasDeclaradas: Decimal
  -estado: EstadoBitacoraEnum
  -fechaRegistro: DateTime
  -fechaVisado: DateTime
  -fechaObservacion: DateTime
  +registrarContenido(resumen: String, dificultades: String, horas: Decimal): Void
  +visar(idAuditor: UUID): Void
  +observar(idAuditor: UUID, pliego: String): Void
  +esAuditable(): Boolean
}

class SesionMentoria {
  -id: UUID
  -codigoSesion: String
  -idMentor: UUID
  -idAsignatura: UUID
  -estado: EstadoSesionEnum
  -cuposOcupados: Integer
  -aforoMaximo: Integer
  -fechaHoraInicio: DateTime
  -fechaHoraFin: DateTime
  +obtenerTotalAsistenciasValidadas(): Integer
  +verificarElegibilidadAuditoria(): Boolean
}

class ReservaCupo {
  -id: UUID
  -idSesion: UUID
  -idEstudiante: UUID
  -estado: String
  -asistio: Boolean
  -fechaHoraFirmaQR: DateTime
  +ratificarAsistenciaFisica(): Void
}

class BolsaHorasMentor {
  -id: UUID
  -idMentor: UUID
  -semestreAcademico: String
  -horasProvisionales: Decimal
  -horasOficialesAcreditadas: Decimal
  +acumularHorasProvisionales(horas: Decimal): Void
  +consolidarHorasOficiales(horas: Decimal): Void
  +congelarHorasPorObservacion(horas: Decimal): Void
}

class ObservacionBitacora {
  -id: UUID
  -idBitacora: UUID
  -idAuditor: UUID
  -tipoFalta: TipoFaltaObservacionEnum
  -detallePliego: String
  -fechaEmision: DateTime
  -fechaLimiteSubsanacion: DateTime
  -estado: EstadoObservacionEnum
  +emitirPliego(plazoHoras: Integer): Void
  +subsanar(evidenciaAdicional: String): Void
  +verificarVencimiento(): Boolean
}

class RegistroAuditoriaAdmin {
  -id: UUID
  -idUsuarioAdmin: UUID
  -accion: DictamenAuditoriaEnum
  -tablaAfectada: String
  -idRegistroAfectado: UUID
  -detalleJson: String
  -direccionIp: String
  -fechaHora: DateTime
  +asentarLogAuditable(): Void
}

' ===================================================
' DTOs (DATA TRANSFER OBJECTS)
' ===================================================
class BandejaAuditoriaItemDTO {
  +idBitacora: UUID
  +idSesion: UUID
  +codigoSesion: String
  +tema: String
  +nombreMentor: String
  +fechaHoraFin: DateTime
  +horasDeclaradas: Decimal
  +estadoBitacora: EstadoBitacoraEnum
}

class ExpedienteAuditoriaCompletoDTO {
  +idSesion: UUID
  +idBitacora: UUID
  +datosSesion: Object
  +resumenTematico: String
  +dificultadesDetectadas: String
  +urlEvidenciaAdjunta: String
  +nominaAsistenciaQR: List<Object>
  +totalInscritos: Integer
  +totalAsistenciasRatificadas: Integer
  +horasDeclaradas: Decimal
}

class VisadoExitosoDTO {
  +idBitacora: UUID
  +estado: EstadoBitacoraEnum
  +horasOficialesConsolidadas: Decimal
  +mensaje: String
}

class ObservacionRequestDTO {
  +tipoFalta: TipoFaltaObservacionEnum
  +pliego: String
  +plazoHoras: Integer
}

class ObservacionRegistradaDTO {
  +idObservacion: UUID
  +idBitacora: UUID
  +estadoBitacora: EstadoBitacoraEnum
  +fechaLimiteSubsanacion: DateTime
}

' ===================================================
' COMPONENTES DE SERVICIO Y PUERTOS
' ===================================================
class AuditoriaBitacorasService {
  -auditoriaRepo: AuditoriaDocenteRepository
  -notificadorEmail: NotificadorEmailInstitucionalAdapter
  +obtenerBandejaPendientes(semestre: String): List<BandejaAuditoriaItemDTO>
  +obtenerExpedienteDetallado(idSesion: UUID): ExpedienteAuditoriaCompletoDTO
  +visarBitacora(idBitacora: UUID, idAuditor: UUID): VisadoExitosoDTO
  +observarBitacora(idBitacora: UUID, req: ObservacionRequestDTO, idAuditor: UUID): ObservacionRegistradaDTO
}

class AuditoriaDocenteRepository {
  +buscarPendientesVisado(): List<BitacoraSesion>
  +buscarExpedienteCompleto(idSesion: UUID): ExpedienteAuditoriaCompletoDTO
  +ejecutarVisadoTransaccional(idBitacora: UUID, idMentor: UUID, horas: Decimal, idAuditor: UUID): Boolean
  +ejecutarObservacionTransaccional(obs: ObservacionBitacora, idAuditor: UUID): Boolean
}

class NotificadorEmailInstitucionalAdapter {
  +despacharPliegoObservacion(emailMentor: String, pliego: String, limite: DateTime): Boolean
}

' ===================================================
' RELACIONES
' ===================================================
BitacoraSesion --> EstadoBitacoraEnum : gobernada por
SesionMentoria --> EstadoSesionEnum : gobernada por
ObservacionBitacora --> TipoFaltaObservacionEnum : tipificada por
ObservacionBitacora --> EstadoObservacionEnum : clasificada por
RegistroAuditoriaAdmin --> DictamenAuditoriaEnum : categorizado por

SesionMentoria "1" *-- "0..1" BitacoraSesion : registra
SesionMentoria "1" *-- "0..*" ReservaCupo : administra
BitacoraSesion "1" *-- "0..*" ObservacionBitacora : acumula pliegos
BolsaHorasMentor "1" -- "0..*" BitacoraSesion : consolida horas de

AuditoriaBitacorasService ..> BandejaAuditoriaItemDTO : produce lista
AuditoriaBitacorasService ..> ExpedienteAuditoriaCompletoDTO : produce
AuditoriaBitacorasService ..> VisadoExitosoDTO : emite
AuditoriaBitacorasService ..> ObservacionRegistradaDTO : emite
AuditoriaBitacorasService ..> ObservacionRequestDTO : consume
AuditoriaBitacorasService ..> AuditoriaDocenteRepository : delega
AuditoriaBitacorasService ..> NotificadorEmailInstitucionalAdapter : invoca
AuditoriaDocenteRepository ..> BitacoraSesion : persiste
AuditoriaDocenteRepository ..> ObservacionBitacora : persiste
AuditoriaDocenteRepository ..> RegistroAuditoriaAdmin : asienta
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS22 formaliza el acoplamiento controlado entre la fiscalización académica y la contabilidad horaria en la EPIS-UPT. Mediante la coordinación de `AuditoriaBitacorasService` con `AuditoriaDocenteRepository`, la entidad `BolsaHorasMentor` protege la integridad del saldo docente impidiendo incrementos no visados. A su vez, la relación compuesta con `ObservacionBitacora` y la persistencia inmutable en `RegistroAuditoriaAdmin` aseguran que cualquier dictamen evaluativo cuente con trazabilidad forense completa y respaldo documental exigido para la acreditación ante comisiones institucionales.

### 6.3.4.16. CUS12 - Vista Lógica Parcial de Clases: Destacar Mentorías Prioritarias

La vista lógica parcial para `CUS12` modela las clases del dominio, objetos de transferencia de datos (*DTOs*), servicios de aplicación y adaptadores de infraestructura para la gestión de prioridades curriculares (`RF24`) y su bonificación algorítmica (`RN-11`). Se especifican los atributos privados y métodos de negocio de las entidades `Asignatura`, `PoliticaPrioridadAsignatura`, `TemaSilabico`, `OfertaMentoria`, `MetricasRendimientoAcademico` y `RegistroAuditoriaAdmin`, coordinadas por `PriorizacionCurricularService` en interacción con `PriorizacionCurricularRepository`, `CacheManagerPort` (Redis) y `RecommendationEngine` para garantizar la consistencia en el catálogo de mentorías y en el feed personalizado de recomendaciones.

#### Diagrama 6.16.16: Diagrama de Clases Lógico Parcial - CUS12: Destacar Mentorías Prioritarias

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS12: Destacar Mentorías Prioritarias\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

' ===================================================
' ENUMERADOS
' ===================================================
enum EstadoPoliticaEnum {
  PENDIENTE_APROBACION
  ACTIVA
  CONCLUIDA
  REVOCADA
}

enum EstadoOfertaEnum {
  BORRADOR
  PUBLICADA
  COMPLETADA
  CANCELADA
}

enum NivelRiesgoCurricularEnum {
  BAJO
  MEDIO
  CRITICO_ALTO
}

' ===================================================
' CLASES DE ENTIDAD (MODELO DE DOMINIO)
' ===================================================
class Asignatura {
  -id: UUID
  -codigo: String
  -nombre: String
  -ciclo: Integer
  -creditos: Integer
  -esPrioritaria: Boolean
  +marcarComoPrioritaria(): Void
  +desmarcarPrioritaria(): Void
  +obtenerEstadoVigente(): Boolean
}

class PoliticaPrioridadAsignatura {
  -id: UUID
  -idAsignatura: UUID
  -idAdminResponsable: UUID
  -factorAlfa: Decimal
  -fechaInicio: Date
  -fechaFin: Date
  -numeroResolucion: String
  -estado: EstadoPoliticaEnum
  -fechaCreacion: DateTime
  +activar(factor: Decimal, inicio: Date, fin: Date, resolucion: String): Void
  +revocar(): Void
  +estaVigente(fechaActual: Date): Boolean
}

class TemaSilabico {
  -id: UUID
  -idAsignatura: UUID
  -unidad: Integer
  -nombreTema: String
  -esCritico: Boolean
  +marcarTemaCritico(): Void
}

class OfertaMentoria {
  -id: UUID
  -idMentor: UUID
  -idAsignatura: UUID
  -idTema: UUID
  -titulo: String
  -estado: EstadoOfertaEnum
  -fechaCreacion: DateTime
  +esOfertaPrioritaria(): Boolean
  +obtenerFactorBonificacion(): Decimal
}

class MetricasRendimientoAcademico {
  -id: UUID
  -idAsignatura: UUID
  -semestre: String
  -tasaReprobacion: Decimal
  -estudiantesEnRiesgo: Integer
  -promedioGeneral: Decimal
  +esAsignaturaEnRiesgoCritico(): Boolean
  +clasificarNivelRiesgo(): NivelRiesgoCurricularEnum
}

class RegistroAuditoriaAdmin {
  -id: UUID
  -idUsuarioAdmin: UUID
  -accion: String
  -tablaAfectada: String
  -idRegistroAfectado: UUID
  -detalleJson: String
  -direccionIp: String
  -fechaHora: DateTime
  +asentarLogAuditable(): Void
}

' ===================================================
' DTOs (DATA TRANSFER OBJECTS)
' ===================================================
class AsignaturaRendimientoDTO {
  +idAsignatura: UUID
  +codigo: String
  +nombre: String
  +ciclo: Integer
  +tasaReprobacion: Decimal
  +estudiantesEnRiesgo: Integer
  +nivelRiesgo: NivelRiesgoCurricularEnum
  +esPrioritaria: Boolean
  +idPoliticaActiva: UUID
}

class ActivarPrioridadRequestDTO {
  +idAsignatura: UUID
  +factorAlfa: Decimal
  +fechaInicio: Date
  +fechaFin: Date
  +numeroResolucion: String
  +justificacion: String
}

class PrioridadActivadaDTO {
  +idPolitica: UUID
  +idAsignatura: UUID
  +estado: EstadoPoliticaEnum
  +factorAlfa: Decimal
  +fechaInicio: Date
  +fechaFin: Date
  +mensaje: String
}

class OfertaRecomendadaDTO {
  +idOferta: UUID
  +titulo: String
  +nombreAsignatura: String
  +nombreMentor: String
  +scoreFinal: Float
  +esPrioritaria: Boolean
  +badgeInstitucional: String
}

' ===================================================
' COMPONENTES DE SERVICIO Y PUERTOS
' ===================================================
class PriorizacionCurricularService {
  -priorizacionRepo: PriorizacionCurricularRepository
  -cacheService: CacheManagerPort
  +obtenerRendimientoAsignaturas(semestre: String): List<AsignaturaRendimientoDTO>
  +activarPrioridadInstitucional(req: ActivarPrioridadRequestDTO, idAdmin: UUID): PrioridadActivadaDTO
  +desactivarPrioridad(idPolitica: UUID, idAdmin: UUID): Boolean
}

class PriorizacionCurricularRepository {
  +buscarAsignaturasConMetricas(): List<AsignaturaRendimientoDTO>
  +guardarPoliticaTransaccional(politica: PoliticaPrioridadAsignatura, idAdmin: UUID): Boolean
  +actualizarIndicadorAsignatura(idAsignatura: UUID, esPrioritaria: Boolean): Void
}

interface CacheManagerPort {
  +purgarClavesPatron(patron: String): Integer
  +invalidarCacheRecomendaciones(): Void
}

class RecommendationEngine {
  +inferirRecomendacionesTopK(idEstudiante: UUID, topK: Integer): List<OfertaRecomendadaDTO>
  +aplicarPonderacionAlfa(scoreBase: Float, alfa: Decimal): Float
}

' ===================================================
' RELACIONES
' ===================================================
PoliticaPrioridadAsignatura --> EstadoPoliticaEnum : gobernada por
OfertaMentoria --> EstadoOfertaEnum : clasificada por
MetricasRendimientoAcademico --> NivelRiesgoCurricularEnum : evalúa a

Asignatura "1" *-- "0..*" TemaSilabico : desglosa
Asignatura "1" *-- "0..*" PoliticaPrioridadAsignatura : recibe
Asignatura "1" -- "0..1" MetricasRendimientoAcademico : analizada por
Asignatura "1" -- "0..*" OfertaMentoria : clasifica

PriorizacionCurricularService ..> AsignaturaRendimientoDTO : produce lista
PriorizacionCurricularService ..> PrioridadActivadaDTO : emite
PriorizacionCurricularService ..> ActivarPrioridadRequestDTO : consume
PriorizacionCurricularService ..> PriorizacionCurricularRepository : delega
PriorizacionCurricularService ..> CacheManagerPort : invoca
PriorizacionCurricularRepository ..> PoliticaPrioridadAsignatura : persiste
PriorizacionCurricularRepository ..> Asignatura : actualiza
PriorizacionCurricularRepository ..> RegistroAuditoriaAdmin : asienta

RecommendationEngine ..> OfertaRecomendadaDTO : genera
RecommendationEngine ..> PoliticaPrioridadAsignatura : consulta alfa
RecommendationEngine ..> OfertaMentoria : evalúa
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS12 formaliza la estructura de control directivo y optimización algorítmica del Sistema Web P2P. La clase `PoliticaPrioridadAsignatura` encapsula los parámetros de gobernanza académica dictaminados por la Dirección EPIS y Tutoría, incluyendo la vigencia temporal y el factor multiplicador $\alpha$ restringido por `RN-11`. La desacoplada interfaz `CacheManagerPort` garantiza que cualquier cambio en la prioridad invalide los resultados cacheados en Redis, forzando a `RecommendationEngine` a ponderar las ofertas críticas con el badge visual correspondiente, reforzando la retención estudiantil en los cursos de mayor índice de reprobación.

### 6.3.4.17. CUS14 - Vista Lógica Parcial de Clases: Visualizar Tablero de Analíticas Institucionales

La vista lógica parcial para `CUS14` modela las clases del dominio analítico, objetos de transferencia de datos (*DTOs*), servicios de procesamiento OLAP y puertos de exportación criptográficamente protegidos conforme a `RF25` y `RN-13`. Se especifican los atributos privados y métodos de las entidades `KpiInstitucionalAcademico`, `DemandaInsatisfechaArea`, `MapeoAnonimizadoEstudiante` y `RegistroAuditoriaAdmin`, orquestadas por `AnaliticaInstitucionalService` en colaboración con `AnaliticaInstitucionalRepository`, `AnonimizationPort` y `ReportCompilerPort` para asegurar un cuadro de mando integral con fe pública y privacidad garantizada bajo la Ley N° 29733.

#### Diagrama 6.16.17: Diagrama de Clases Lógico Parcial - CUS14: Visualizar Tablero de Analíticas Institucionales

```plantuml
@startuml
title Diagrama de Clases Lógico Parcial - CUS14: Visualizar Tablero de Analíticas Institucionales\nSistema Web P2P - EPIS UPT

skinparam classAttributeIconSize 0
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName Arial
skinparam fontSize 10

skinparam class {
    BackgroundColor #F8F9FA
    BorderColor #2B3A42
    ArrowColor #2B3A42
}

skinparam enum {
    BackgroundColor #FFF2DF
    BorderColor #D97706
}

' ===================================================
' ENUMERADOS
' ===================================================
enum TipoExportacionAnaliticaEnum {
  DOSSIER_PDF_EJECUTIVO
  DATASET_CSV_ANONIMIZADO
  MATRIZ_EXCEL_RESUMEN
}

enum NivelAgregacionTemporalEnum {
  SEMESTRAL
  MENSUAL
  SEMANAL_EXAMENES
}

' ===================================================
' CLASES DE ENTIDAD (MODELO DE DOMINIO ANALÍTICO)
' ===================================================
class KpiInstitucionalAcademico {
  -id: UUID
  -semestre: String
  -totalEstudiantesBeneficiados: Integer
  -totalHorasDictadas: Decimal
  -ratioQuorumGlobal: Decimal
  -tasaAsistenciaReal: Decimal
  -tasaRevocacionT24h: Decimal
  -promedioSatisfaccionCsat: Decimal
  -fechaCalculo: DateTime
  +calcularVariacionIntersemestral(): Decimal
  +serializarResumenEjecutivo(): String
}

class DemandaInsatisfechaArea {
  -id: UUID
  -idAsignatura: UUID
  -nombreAsignatura: String
  -totalSolicitudesSinAtender: Integer
  -temasCriticosSolicitados: List<String>
  +calcularDeficitHorario(): Decimal
}

class MapeoAnonimizadoEstudiante {
  -idOriginal: UUID
  -hashAnonimo: String
  -saltRotativo: String
  -fechaGeneracion: DateTime
  +disociarIdentidad(idUsuario: UUID, salt: String): String
}

class RegistroAuditoriaAdmin {
  -id: UUID
  -idUsuarioAdmin: UUID
  -accion: String
  -tablaAfectada: String
  -idRegistroAfectado: UUID
  -detalleJson: String
  -direccionIp: String
  -fechaHora: DateTime
  +asentarLogAuditable(): Void
}

' ===================================================
' DTOs (DATA TRANSFER OBJECTS)
' ===================================================
class TableroAnaliticoDTO {
  +semestre: String
  +metricasGenerales: WidgetKpiDTO
  +distribucionQuorum: Object
  +mapaCalorDemanda: List<MapaCalorDemandaDTO>
  +tasaAusentismo: Decimal
  +puntajeNetoCalidad: Decimal
}

class WidgetKpiDTO {
  +totalAlumnos: Integer
  +totalHoras: Decimal
  +porcentajeQuorum: Decimal
  +satisfaccionGlobal: Decimal
}

class MapaCalorDemandaDTO {
  +asignatura: String
  +solicitudesVacias: Integer
  +porcentajeDificultad: Decimal
}

class FiltroAnaliticoRequestDTO {
  +semestre: String
  +nivelAgregacion: NivelAgregacionTemporalEnum
  +cicloInicio: Integer
  +cicloFin: Integer
}

class DatasetInvestigacionItemDTO {
  +hashEstudiante: String
  +hashMentor: String
  +codigoAsignatura: String
  +modalidad: String
  +asistioSesion: Boolean
  +puntajeEncuesta: Integer
  +semestre: String
}

' ===================================================
' COMPONENTES DE SERVICIO Y PUERTOS
' ===================================================
class AnaliticaInstitucionalService {
  -analiticaRepo: AnaliticaInstitucionalRepository
  -anonimizationPort: AnonimizationPort
  -reportCompiler: ReportCompilerPort
  +compilarCuadroMando(req: FiltroAnaliticoRequestDTO): TableroAnaliticoDTO
  +exportarDossierPDF(semestre: String): Array<Byte>
  +exportarDatasetInvestigacion(semestre: String, idAdmin: UUID): Array<Byte>
}

class AnaliticaInstitucionalRepository {
  +consultarKpisAgregados(semestre: String): KpiInstitucionalAcademico
  +obtenerDemandaInsatisfechaPorMateria(): List<DemandaInsatisfechaArea>
  +extraerMicrodatosEncuestas(semestre: String): List<Object>
  +asentarRegistroAuditoria(log: RegistroAuditoriaAdmin): Void
}

interface AnonimizationPort {
  +aplicarHashSeudoanonimo(idEstudiante: UUID, salt: String): String
  +sanitizarCamposSensibles(fila: Object): DatasetInvestigacionItemDTO
}

interface ReportCompilerPort {
  +renderizarPdfEjecutivo(kpi: KpiInstitucionalAcademico, demandas: List<DemandaInsatisfechaArea>): Array<Byte>
  +serializarCsvDataset(items: List<DatasetInvestigacionItemDTO>): Array<Byte>
}

' ===================================================
' RELACIONES
' ===================================================
FiltroAnaliticoRequestDTO --> NivelAgregacionTemporalEnum : categorizado por
AnaliticaInstitucionalService ..> TipoExportacionAnaliticaEnum : despacha

KpiInstitucionalAcademico "1" *-- "0..*" DemandaInsatisfechaArea : consolida
AnaliticaInstitucionalService ..> TableroAnaliticoDTO : produce
TableroAnaliticoDTO *-- WidgetKpiDTO : integra
TableroAnaliticoDTO *-- MapaCalorDemandaDTO : integra
AnaliticaInstitucionalService ..> FiltroAnaliticoRequestDTO : consume
AnaliticaInstitucionalService ..> AnaliticaInstitucionalRepository : delega
AnaliticaInstitucionalService ..> AnonimizationPort : invoca (RN-13)
AnaliticaInstitucionalService ..> ReportCompilerPort : utiliza
AnaliticaInstitucionalRepository ..> KpiInstitucionalAcademico : consulta
AnaliticaInstitucionalRepository ..> RegistroAuditoriaAdmin : persiste
AnonimizationPort ..> MapeoAnonimizadoEstudiante : genera
AnonimizationPort ..> DatasetInvestigacionItemDTO : produce
ReportCompilerPort ..> DatasetInvestigacionItemDTO : transforma
@enduml
```

Fuente: Elaboración propia.

El diagrama de clases parcial de CUS14 formaliza la infraestructura de analítica institucional y privacidad de datos de la EPIS-UPT. La clase `KpiInstitucionalAcademico` centraliza los agregados OLAP de retención, quórum y satisfacción estudiantil, permitiendo que `AnaliticaInstitucionalService` provea tanto vistas gerenciales instantáneas (`TableroAnaliticoDTO`) como expedientes PDF oficiales. La estricta separación de responsabilidades a través de `AnonimizationPort` y `MapeoAnonimizadoEstudiante` garantiza que la exportación de registros tabulares para propósitos científicos desvincule los identificadores personales de forma unidireccional e irreversible, cumpliendo cabalmente con la Ley N° 29733 de Protección de Datos Personales y la directiva `RN-13`.

---

# 7. Conclusiones

**Estructuración Formal y Exhaustiva del Alcance Funcional:** Se consolidó la línea base analítica y funcional del Sistema Web P2P para la EPIS-UPT, delimitando con precisión los veinticuatro casos de uso oficiales (`CUS01` al `CUS24`), los veintiséis requerimientos funcionales canónicos (`RF01` al `RF26`), los diez requerimientos no funcionales bajo el estándar ISO/IEC 25010 (`RNF01` al `RNF10`) y las catorce reglas de negocio institucionales (`RN-01` al `RN-14`). Esta definición integral proporciona una cobertura metodológica sobre las necesidades pedagógicas y operativas del programa de mentorías peer-to-peer.

**Robustez en Autenticación, Seguridad y Cumplimiento Normativo:** La arquitectura de seguridad especifica un esquema multicapa sustentado en autenticación institucional obligatoria con segundo factor por correo (Email OTP), tokens criptográficos efímeros JWT y políticas de seguridad a nivel de fila (*Row Level Security - RLS*) en PostgreSQL. Asimismo, el sistema formaliza el consentimiento informado digital exigido por la Ley N° 29733 (Ley de Protección de Datos Personales del Perú), resguardando los historiales formativos y el anonimato de las encuestas de evaluación cualitativa.

**Gobernanza Automatizada de Recursos, Quórum y Logística:** Mediante la formalización del Servicio Cron desatendido y el protocolo de ratificación anticipada con corte en $T-24\text{ h}$, el sistema contribuye a mitigar el ausentismo estudiantil y el desperdicio de ambientes físicos en la facultad. La verificación de aulas mediante el motor parser de horarios y la generación dinámica de salas virtuales (Google Meet / Discord) optimizan la utilización de la infraestructura universitaria sin sobrecarga burocrática para los docentes y directores.

**Trazabilidad Pedagógica, Gamificación y Fe Pública Universitaria:** La articulación secuencial entre el registro estructurado de bitácoras, el control de asistencia mediante códigos QR, la captura de encuestas en ventanas de 24 horas y el visado administrativo por parte de la Comisión de Tutoría formaliza que la certificación de horas para prácticas preprofesionales y créditos extracurriculares cuente con un respaldo documental auditable, sustentado en constancias foliadas en PDF/A, códigos hash SHA-256 y enlaces QR de verificación institucional.

**Madurez y Viabilidad Metodológica para la Fase de Construcción:** La exhaustividad alcanzada en los escenarios narrativos canónicos (con sus 4 tablas estructuradas por caso de uso) y en los modelos lógicos de objetos, actividades, secuencias y clases (bajo el estándar UWE) minimiza los riesgos de ambigüedad técnica o retrabajo, proporcionando al equipo de desarrollo una guía directa y auditable para la implementación en la FASE 3 (Construcción del Software) y la ejecución del catálogo experimental de pruebas.

---

# 8. Bibliografía

- Congreso de la República del Perú. (2011). *Ley N° 29733: Ley de Protección de Datos Personales*. Diario Oficial El Peruano, 3 de julio de 2011.
- Congreso de la República del Perú. (2014). *Ley N° 30220: Ley Universitaria (Art. 40: Tutoría y Consejería Estudiantil)*. Diario Oficial El Peruano, 9 de julio de 2014.
- IEEE Computer Society. (1998). *IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications*. IEEE Standards Association.
- ISO/IEC/IEEE. (2018). *ISO/IEC/IEEE 29148:2018 Systems and software engineering - Life cycle processes - Requirements engineering*. International Organization for Standardization.
- Koch, N., & Kraus, A. (2002). *The Expressive Power of UML-based Web Engineering*. En Second International Workshop on Web-oriented Software Technology (IWWOST02).
- Pressman, R. S., & Maxim, B. R. (2020). *Ingeniería del software: Un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
- Sommerville, I. (2016). *Software Engineering* (10.ª ed.). Pearson Education.
- Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7.ª ed.). Pearson.