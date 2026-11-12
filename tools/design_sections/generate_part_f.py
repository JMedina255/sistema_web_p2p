# -*- coding: utf-8 -*-
"""
Generator for Part F of docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md
Covers:
- Sección 7: Conclusiones (Actualizada con las métricas finales de los 8 Sprints)
- Sección 8: Bibliografía
"""

def get_part_f():
    return r'''# 7. Conclusiones

**1. Estructuración Formal y Madurez del Alcance Funcional:** Se consolidó con éxito la línea base técnica e institucional del Sistema Web P2P para la EPIS-UPT, articulando de manera armónica los ocho módulos canónicos (`MOD-01` al `MOD-08`), los veinticuatro casos de uso oficiales (`CUS-001` al `CUS-024`), los veintiséis requerimientos funcionales atómicos (`RF01` al `RF26`), las catorce reglas de negocio institucionales (`RN-01` al `RN-14`) y los diez requerimientos no funcionales bajo el estándar ISO/IEC 25010 (`RNF01` al `RNF10`). Esta especificación exhaustiva traduce las necesidades pedagógicas de tutoría universitaria en especificaciones arquitectónicas reproducibles y de alta fidelidad.

**2. Eficiencia y Precisión Demostrada del Motor Algorítmico (EdRecSys):** La calibración experimental del microservicio de recomendación híbrido demostró un desempeño analítico sobresaliente que supera con holgura los criterios de diseño iniciales: se alcanzaron métricas empíricas de **Precision@3 = 83.3%**, **Precision@5 = 80.0%** y un índice de posicionamiento acumulado de **NDCG = 0.82**, manteniendo un tiempo medio de inferencia vectorial de apenas **12.4 ms** (umbral de aceptación $\le 500$ ms). Estos resultados ratifican que la combinación de similitud coseno sobre competencias silábicas con filtrado colaborativo ponderado por reputación y balance de carga personaliza eficazmente el apoyo formativo para los estudiantes de los primeros ciclos.

**3. Integridad Transaccional, Quórum y Concurrencia Confiable:** La implementación de patrones de persistencia transaccional ACID con cerrojos pesimistas a nivel de fila (`SELECT ... FOR UPDATE`) en PostgreSQL erradicó por completo el riesgo de condiciones de carrera (*race conditions*), alcanzando una tasa de sobreasignación de cupos de **estrictamente 0.0%** bajo pruebas de estrés simultáneo. Asimismo, la automatización del demonio cron de backend para el corte de $T-24\text{ h}$ y el protocolo de resolución de contingencia del mentor ante quórum deficiente optimizan el aprovechamiento de las aulas físicas y recursos virtuales de la facultad, eliminando cancelaciones tardías e imprevistas.

**4. Seguridad Multicapa, Privacidad y Fe Pública Universitaria:** La arquitectura de software blindó el ecosistema universitario mediante autenticación multifactor 2FA con códigos OTP de 6 dígitos con expiración de 5 minutos, tokens de sesión efímeros JWT (HS256) de 8 horas y políticas activas de *Row Level Security* (RLS) en las 15 tablas relacionales de la base de datos. Se formalizó el estricto cumplimiento vinculante de la Ley N° 29733 de Protección de Datos Personales del Perú mediante registros inmutables de consentimiento digital. Finalmente, la articulación entre pases QR dinámicos TOTP, bitácoras firmadas con hash SHA-256 en 48 horas y la emisión digital de certificados PDF con código correlativo institucional y código QR de validación en línea otorga plena validez y trazabilidad a las horas acumuladas para convalidación de créditos extracurriculares.

**5. Calidad de Construcción y Verificación Empírica Integral:** La culminación de los ocho sprints de desarrollo se encuentra sólidamente respaldada por una batería automatizada de **627 pruebas de software aprobadas con 0 fallos (280 pruebas unitarias/integración backend con Pytest y 347 pruebas unitarias/componentes frontend con Vitest)**, alcanzando una cobertura global de código superior al **85%** en ambas capas. Las interfaces implementan el estándar de accesibilidad **WCAG 2.1 Nivel AA** y registran una puntuación media superior a los **75 puntos en la escala estandarizada System Usability Scale (SUS)**, garantizando una herramienta ergonómica, resiliente y de alto impacto para la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.

---

# 8. Bibliografía

- Congreso de la República del Perú. (2011). *Ley N° 29733: Ley de Protección de Datos Personales*. Diario Oficial El Peruano, 3 de julio de 2011.
- Congreso de la República del Perú. (2014). *Ley N° 30220: Ley Universitaria (Art. 40: Tutoría y Consejería Estudiantil)*. Diario Oficial El Peruano, 9 de julio de 2014.
- IEEE Computer Society. (1998). *IEEE Std 830-1998: IEEE Recommended Practice for Software Requirements Specifications*. IEEE Standards Association.
- ISO/IEC/IEEE. (2018). *ISO/IEC/IEEE 29148:2018 Systems and software engineering - Life cycle processes - Requirements engineering*. International Organization for Standardization.
- ISO/IEC. (2011). *ISO/IEC 25010:2011 Systems and software engineering - Systems and software Quality Requirements and Evaluation (SQuaRE) - System and software quality models*. International Organization for Standardization.
- Jacobson, I., Booch, G., & Rumbaugh, J. (1999). *The Unified Software Development Process*. Addison-Wesley.
- Koch, N., & Kraus, A. (2002). *The Expressive Power of UML-based Web Engineering*. En Second International Workshop on Web-oriented Software Technology (IWWOST02).
- Pressman, R. S., & Maxim, B. R. (2020). *Ingeniería del software: Un enfoque práctico* (9.ª ed.). McGraw-Hill Interamericana.
- Ricci, F., Rokach, L., & Shapira, B. (2015). *Recommender Systems Handbook* (2.ª ed.). Springer.
- Sommerville, I. (2016). *Software Engineering* (10.ª ed.). Pearson Education.
- Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice* (7.ª ed.). Pearson.
- W3C. (2018). *Web Content Accessibility Guidelines (WCAG) 2.1*. World Wide Web Consortium.
'''
