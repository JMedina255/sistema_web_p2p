# Documento Informe de Visión de Proyecto

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Docente:** Dr. RICARDO EDUARDO VALCARCEL ALVARADO  
**Autores:**  
- ANTAYHUA MAMANI, Renzo Antonio (2022073504)  
- MEDINA QUISPE, Joan Cristian (2022074255)  
**Institución:** Universidad Privada de Tacna - Facultad de Ingeniería - Escuela Profesional de Ingeniería de Sistemas  
**Lugar y Fecha:** Tacna – Perú, 2026  

---

## Control de Versiones

| Versión | Hecha por | Revisada por | Aprobada por | Fecha | Motivo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1.0 | JCM | RAM | RVA | 04/09/2026 | Versión 1.0 |

---

## ÍNDICE GENERAL

1. [Introducción](#1-introducción)  
   1.1. [Propósito](#11-propósito)  
   1.2. [Alcance](#12-alcance)  
   1.3. [Definiciones, Siglas y Abreviaturas](#13-definiciones-siglas-y-abreviaturas)  
   1.4. [Visión General](#14-visión-general)  
2. [Posicionamiento](#2-posicionamiento)  
   2.1. [Oportunidad de negocio](#21-oportunidad-de-negocio)  
   2.2. [Definición del problema](#22-definición-del-problema)  
3. [Descripción de los Interesados y Usuarios](#3-descripción-de-los-interesados-y-usuarios)  
   3.1. [Resumen de los interesados](#31-resumen-de-los-interesados)  
   3.2. [Resumen de los usuarios](#32-resumen-de-los-usuarios)  
   3.3. [Entorno de usuario](#33-entorno-de-usuario)  
   3.4. [Perfiles de los interesados](#34-perfiles-de-los-interesados)  
   3.5. [Perfiles de los usuarios](#35-perfiles-de-los-usuarios)  
   3.6. [Necesidades de los interesados y usuarios](#36-necesidades-de-los-interesados-y-usuarios)  
4. [Vista General del Producto](#4-vista-general-del-producto)  
   4.1. [Perspectiva del producto](#41-perspectiva-del-producto)  
   4.2. [Resumen de capacidades](#42-resumen-de-capacidades)  
   4.3. [Suposiciones y dependencias](#43-suposiciones-y-dependencias)  
   4.4. [Costos y precios](#44-costos-y-precios)  
   4.5. [Licenciamiento e instalación](#45-licenciamiento-e-instalación)  
5. [Características del Producto](#5-características-del-producto)  
6. [Restricciones](#6-restricciones)  
7. [Rangos de Calidad](#7-rangos-de-calidad)  
8. [Precedencia y Prioridad](#8-precedencia-y-prioridad)  
9. [Otros Requerimientos del Producto](#9-otros-requerimientos-del-producto)  
   9.1. [Estándares legales](#91-estándares-legales)  
   9.2. [Estándares de comunicación](#92-estándares-de-comunicación)  
   9.3. [Estándares de cumplimiento de la plataforma](#93-estándares-de-cumplimiento-de-la-plataforma)  
   9.4. [Estándares de calidad y seguridad](#94-estándares-de-calidad-y-seguridad)  
10. [Conclusiones](#conclusiones)  
11. [Recomendaciones](#recomendaciones)  

---

## 1. Introducción

### 1.1. Propósito
El presente documento de visión define las necesidades del negocio, las expectativas de los interesados, las características clave y las restricciones arquitecturales para el desarrollo del **"Sistema web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT, 2026"**. Su objetivo es establecer un marco contractual y técnico de referencia que alinee los esfuerzos del equipo de desarrollo con los objetivos académicos y de permanencia estudiantil de la facultad.

### 1.2. Alcance
El alcance del producto comprende el diseño, desarrollo e implantación de una plataforma web distribuida orientada a la gestión y personalización del aprendizaje entre pares:

1. **Módulo de Emparejamiento Inteligente:** Motor algorítmico híbrido (filtrado colaborativo y similitud coseno sobre vectores de competencias curriculares) para emparejar a mentores y mentoreados de forma adaptativa.
2. **Módulo de Gestión de Sesiones P2P:** Agendamiento, registro de asistencia, enlaces a salas virtuales o ubicación de cubículos físicos, y retroalimentación multidimensional post-sesión.
3. **Módulo de Gamificación y Reconocimiento:** Sistema de reputación basado en valoraciones, asignación de insignias temáticas y registro auditable de horas de mentoría.
4. **Panel Administrativo Institucional:** Tablero de control web para la Dirección de Escuela y coordinadores de tutoría con métricas de cobertura, materias de mayor demanda y alertas tempranas de riesgo académico.
5. **Límite de Alcance:** El sistema operará de manera exclusiva como aplicación web responsiva (optimizada para navegadores de escritorio y dispositivos en campus), excluyendo en esta etapa el desarrollo de aplicaciones móviles nativas.

### 1.3. Definiciones, Siglas y Abreviaturas

| Sigla / Término | Definición Técnica |
| :--- | :--- |
| **P2P (Peer-to-Peer)** | Modelo de red y aprendizaje horizontal distribuido donde los estudiantes interactúan de forma directa como pares formativos. |
| **EdRecSys** | *Educational Recommender System*. Sistema de software diseñado para guiar y recomendar recursos, tutores o contenidos pedagógicos. |
| **EPIS-UPT** | Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna. |
| **Similitud Coseno** | Métrica matemática que evalúa el coseno del ángulo formado por dos vectores de atributos, utilizada para cuantificar la afinidad temática entre perfiles. |
| **RLS (Row Level Security)** | Mecanismo de PostgreSQL que restringe la visualización o edición de registros en base a políticas de seguridad a nivel de fila según el usuario autenticado. |
| **SUS (System Usability Scale)** | Escala psicométrica estandarizada de 10 preguntas utilizada para cuantificar la usabilidad global percibida de un sistema de software. |
| **NDCG** | *Normalized Discounted Cumulative Gain*. Métrica para medir la calidad del ranking y relevancia posicional en sistemas de recomendación. |
| **JWT (JSON Web Token)** | Estándar abierto para la transmisión compacta y segura de afirmaciones de identidad entre el cliente web y el backend. |

### 1.4. Visión General
El documento se estructura detallando el posicionamiento del producto, los perfiles de los usuarios e interesados, el resumen de capacidades funcionales, los atributos de calidad bajo la norma ISO/IEC 25010 y los estándares legales y técnicos aplicables al entorno institucional de la EPIS-UPT.

---

## 2. Posicionamiento

### 2.1. Oportunidad de negocio
Los modelos tradicionales de tutoría en facultades de ingeniería operan usualmente de manera reactiva, formal y con saturación en la carga de los docentes tutores. Esta situación genera que los estudiantes de ciclos formativos iniciales (I al IV ciclo) recurran a canales informales (chats no supervisados) cuando presentan dificultades en asignaturas filtro de alta reprobación (Cálculo, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos).

La oportunidad del producto radica en implementar un entorno web centralizado que articule el talento técnico de los estudiantes de ciclos superiores (VII al X ciclo) para brindar acompañamiento adaptativo. A través de un motor de recomendación híbrido, se optimiza el emparejamiento tutor-estudiante según compatibilidad temática y horaria, reduciendo la deserción temprana e integrando a la Dirección de Escuela como entidad supervisora de la calidad académica.

### 2.2. Definición del problema

| Elemento | Declaración |
| :--- | :--- |
| **El problema de...** | La falta de personalización, trazabilidad e incentivos formales en el acompañamiento pedagógico para la superación de cursos filtro de ingeniería. |
| **Afecta a...** | Estudiantes de semestres iniciales (I a IV ciclo), mentores potenciales de ciclos superiores y la Dirección de Escuela EPIS-UPT. |
| **El impacto de lo cual es...** | Elevadas tasas de reprobación, riesgo de deserción estudiantil, saturación del programa de tutoría docente y desaprovechamiento del talento estudiantil avanzado. |
| **Una solución exitosa sería...** | Una plataforma web P2P con algoritmo de recomendación híbrido que automatice el emparejamiento adaptativo, gestione las sesiones con trazabilidad y otorgue incentivos de gamificación y horas de servicio. |

---

## 3. Descripción de los Interesados y Usuarios

### 3.1. Resumen de los interesados

| Nombre | Descripción | Responsabilidad / Rol |
| :--- | :--- | :--- |
| **Dirección de Escuela EPIS-UPT** | Autoridad académica ejecutiva de la carrera. | Aprobar la implantación del sistema, validar la convalidación de horas y supervisar métricas globales. |
| **Comité de Tutoría de Facultad** | Ente docente encargado del acompañamiento estudiantil. | Monitorear el impacto pedagógico y coordinar intervenciones docentes secundarias. |
| **Equipo de Desarrollo** | Autores del proyecto (Estudiantes de Construcción de Software I). | Diseñar, codificar, probar y desplegar la plataforma web y el motor algorítmico. |

### 3.2. Resumen de los usuarios

| Nombre | Descripción | Tipo |
| :--- | :--- | :--- |
| **Estudiante Mentoreado** | Alumno matriculado en ciclos I a IV con requerimiento de reforzamiento en asignaturas filtro. | Usuario Final |
| **Estudiante Mentor** | Alumno de ciclos VII a X con excelente desempeño académico que dicta tutorías P2P. | Usuario Final |
| **Administrador / Coordinador** | Personal académico encargado de la gestión de la plataforma y validación de reportes. | Usuario Administrativo |

### 3.3. Entorno de usuario
- **Plataforma objetivo:** Web responsiva (Google Chrome, Firefox, Safari, Edge).
- **Dispositivos:** Laptops, PCs de escritorio y tablets en laboratorios del campus o conexiones remotas en el hogar.
- **Conectividad:** Requiere conexión a Internet (mínimo 2 Mbps).

### 3.4. Perfiles de los interesados
- **Dirección de Escuela:** Interesada en elevar el indicador de retención y aprobación en cursos filtro. Requiere reportes ejecutivos consolidados y garantía de protección de datos (Ley N° 29733).

### 3.5. Perfiles de los Usuarios
- **Estudiantes Mentoreados:** Buscan recomendaciones rápidas de mentores afines a su horario y dificultad específica.
- **Estudiantes Mentores:** Requieren una agenda clara de sesiones, enlaces virtuales y acreditación automática de sus horas dedicadas.

### 3.6. Necesidades de los interesados y usuarios

| Necesidad | Solución Propuesta | Requerimiento Asociado |
| :--- | :--- | :--- |
| Emparejamiento óptimo tutor-alumno | Motor de recomendación híbrido (contenido + colaborativo) | Algoritmo de recomendación con similitud coseno |
| Control de sesiones y asistencia | Módulo de agendamiento y confirmación de sesiones | Registro de asistencia y feedback bidireccional |
| Reconocimiento al mentor | Sistema de reputación e insignias de gamificación | Módulo de Gamificación |
| Reportes e indicadores institucionales | Panel analítico con dashboards ejecutivos | Módulo de Reportes Administrativos |

### Diagrama de Actores y Módulos (Regla 3.1 - PlantUML)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Estudiante Mentoreado
(Ciclos I-IV)" as Mentoreado
actor "Estudiante Mentor
(Ciclos VII-X)" as Mentor
actor "Coordinador / Dirección
EPIS-UPT" as Admin

rectangle "Sistema Web P2P de Mentorías" {
  usecase "Solicitar Recomendación de Mentor" as UC1
  usecase "Agendar y Evaluar Sesión P2P" as UC2
  usecase "Aceptar Sesión y Registrar Asistencia" as UC3
  usecase "Ver Insignias y Horas Acumuladas" as UC4
  usecase "Supervisar Dashboards y Alertas" as UC5
}

Mentoreado --> UC1
Mentoreado --> UC2
Mentor --> UC3
Mentor --> UC4
Admin --> UC5
@enduml
```

---

## 4. Vista General del Producto

### 4.1. Perspectiva del producto
El sistema web P2P se concibe como una solución independiente e integrada dentro del ecosistema tecnológico de la EPIS-UPT, interactuando de forma transparente entre la capa cliente web (React) y los servicios desacoplados en la nube (FastAPI + Supabase PostgreSQL).

### 4.2. Resumen de capacidades

| Capacidad Principal | Descripción de Funcionalidades |
| :--- | :--- |
| **Motor de Recomendación Inteligente** | Recomienda los top-N mentores con mayor grado de afinidad temática y disponibilidad horaria. |
| **Gestión de Agenda P2P** | Permite solicitar, reprogramar y confirmar tutorías individuales o grupales. |
| **Gamificación & Trazabilidad** | Otorga reputación, badges por logros y genera constancias digitales de horas acumuladas. |
| **Mantenimiento & Seguridad** | Autenticación JWT, control de accesos RLS en PostgreSQL y cifrado de datos. |

### 4.3. Suposiciones y dependencias
- Disponibilidad y estabilidad de los servicios cloud gratuitos/PaaS (Render y Supabase).
- Colaboración activa de los mentores de ciclos superiores para mantener actualizada su disponibilidad.

### 4.4. Costos y precios
El software se desarrolla dentro del marco académico de la asignatura Construcción de Software I sin costo de licenciamiento comercial para la UPT. Los costos operativos de infraestructura (hosting/cloud) están proyectados a ser cubiertos mediante capas estándar o suscripciones institucionales de bajo costo.

### 4.5. Licenciamiento e instalación
- **Licencia:** Software académico de código abierto bajo términos institucionales de la UPT.
- **Despliegue:** 100% basado en la nube (no requiere instalación local por parte del usuario final).

---

## 5. Características del Producto

1. **Recomendaciones Adaptativas:** Ajuste en tiempo real de sugerencias basado en el historial de calificaciones del mentoreado y la tasa de éxito de los mentores.
2. **Evaluación Bidireccional:** Retroalimentación post-sesión donde el mentoreado evalúa la claridad explicativa y el mentor la puntualidad/compromiso.
3. **Notificaciones Automáticas:** Alertas vía correo/pantalla para confirmación de sesiones y recordatorios.
4. **Exportación de Reportes:** Generación de reportes PDF/Excel para la Dirección de Escuela sobre el avance de las tutorías.

---

## 6. Restricciones

- **Tecnológicas:** El desarrollo backend debe estar implementado en Python y la interfaz cliente en React.
- **Legales:** Estricto cumplimiento de la Ley N° 29733 de Protección de Datos Personales.
- **Acceso:** Limitado a la comunidad universitaria mediante autenticación con correo institucional o credenciales validadas.

---

## 7. Rangos de Calidad (ISO/IEC 25010)

| Atributo de Calidad | Criterio de Aceptación / Rango Objetivo |
| :--- | :--- |
| **Usabilidad (SUS)** | Puntaje promedio percibido $\ge 75$ puntos en la escala SUS. |
| **Rendimiento / Tiempo de Respuesta** | Tiempo de respuesta del endpoint de recomendación $< 1.5$ segundos. |
| **Disponibilidad** | Disponibilidad de la plataforma en la nube $\ge 99.0\%$ durante el semestre lectivo. |
| **Seguridad** | Cero vulnerabilidades críticas en la autenticación JWT y políticas RLS activas. |

---

## 8. Precedencia y Prioridad

1. **Prioridad Alta (Fase Inicial):** Módulo de Autenticación, Motor de Recomendación Híbrido y Agendamiento P2P.
2. **Prioridad Media:** Módulo de Gamificación (Reputación e Insignias) y Notificaciones.
3. **Prioridad Baja (Fase Final):** Dashboards analíticos avanzados para la administración institucional.

---

## 9. Otros Requerimientos del Producto

### 9.1. Estándares legales
- Cumplimiento de la Ley N° 29733 (Protección de datos personales en el Perú).

### 9.2. Estándares de comunicación
- Comunicación cifrada bajo el protocolo HTTPS / TLS 1.3.

### 9.3. Estándares de cumplimiento de la plataforma
- Compatibilidad estándar con navegadores web HTML5 / ES6+.

### 9.4. Estándares de calidad y seguridad
- Arquitectura desacoplada, diseño de componentes reutilizables y hashes seguros de contraseñas.

---

## Conclusiones

1. El documento de visión establece con claridad el problema detectado en la EPIS-UPT y la propuesta de valor centrada en la personalización de mentorías P2P a través de inteligencia artificial adaptativa.
2. La definición precisa de los perfiles de usuario e interesados garantiza que las características desarrolladas atiendan directamente las necesidades de la comunidad universitaria.

---

## Recomendaciones

1. Socializar el documento de visión con los representantes de tutoría y la Dirección de Escuela para validar los incentivos de gamificación y horas de convalidación.
2. Priorizar el desarrollo del motor de recomendación en la Fase 3 del proyecto para asegurar un tiempo suficiente de calibración algorítmica.
