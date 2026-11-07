# Diagramas de Secuencia del Sistema — Fase de Diseño

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS-UPT.<br>
**Fase:** Diseño y Construcción.<br>
**Estado:** Canónico consolidado (24 casos de uso modelados en 8 módulos).<br>
**Documento Canónico Completo:** [DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md)<br>
**Especificación en el SRS:** [FD03-EPIS-Informe SRS de Proyecto.md (Sección 6.3.3)](file:///d:/sistema_web_p2p/docs/diseño/FD03-EPIS-Informe%20SRS%20de%20Proyecto.md#633-diagramas-de-secuencia-del-sistema-fase-de-diseño)

---

## Índice General de Diagramas de Secuencia (CUS-001 al CUS-024)

### MOD-01: Seguridad, Autenticación y Gobernanza
- **Diagrama 6.15.1:** [CUS-001: Iniciar sesión institucional con 2FA y formalización de consentimiento digital](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6151-diagrama-de-secuencia---cus-001-iniciar-sesión-institucional-con-2fa)
- **Diagrama 6.15.2:** [CUS-010: Gestionar asignación y revocación de roles institucionales de usuario](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6152-diagrama-de-secuencia---cus-010-gestionar-asignación-de-roles-de-usuario)

### MOD-02: Ofertas de Mentoría y Gestión de Recursos
- **Diagrama 6.15.3:** [CUS-006: Publicar oferta de mentoría académica con validación de antelación y aforo](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6153-diagrama-de-secuencia---cus-006-publicar-oferta-de-mentoría-académica)
- **Diagrama 6.15.4:** [CUS-008: Consultar disponibilidad de espacios físicos y aulas de la EPIS](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6154-diagrama-de-secuencia---cus-008-consultar-disponibilidad-de-espacios-y-recursos)

### MOD-03: Perfil del Mentor y Plan de Aprendizaje
- **Diagrama 6.15.5:** [CUS-005: Gestionar perfil académico formativo y matriz de disponibilidad horaria semanal](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6155-diagrama-de-secuencia---cus-005-gestionar-perfil-académico-y-disponibilidad-horaria)
- **Diagrama 6.15.6:** [CUS-021: Explorar catálogo curricular jerárquico de asignaturas y materias críticas](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6156-diagrama-de-secuencia---cus-021-explorar-catálogo-curricular-de-asignaturas-filtro)

### MOD-04: Demanda y Recomendaciones Personalizadas
- **Diagrama 6.15.7:** [CUS-002: Explorar cartelera inteligente de recomendaciones de mentoría Top-k](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6157-diagrama-de-secuencia---cus-002-explorar-recomendaciones-personalizadas-top-k)
- **Diagrama 6.15.8:** [CUS-003: Registrar solicitud de mentoría por demanda académica no atendida](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6158-diagrama-de-secuencia---cus-003-registrar-solicitud-de-demanda-académica)

### MOD-05: Quórum, Confirmación y Cancelaciones
- **Diagrama 6.15.9:** [CUS-004: Reservar cupo de mentoría académica con control de aforo y concurrencia](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-6159-diagrama-de-secuencia---cus-004-reservar-cupo-de-mentoría-académica)
- **Diagrama 6.15.10:** [CUS-024: Ratificar asistencia obligatoria a sesión de mentoría académica a T-24h](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61510-diagrama-de-secuencia---cus-024-ratificar-asistencia-a-sesión-de-mentoría)
- **Diagrama 6.15.11:** [CUS-017: Desistir voluntariamente de reserva de cupo sin penalidad antes de T-24h](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61511-diagrama-de-secuencia---cus-017-desistir-voluntariamente-de-reserva)
- **Diagrama 6.15.12:** [CUS-023: Evaluar automáticamente el quórum reglamentario de sesiones de mentoría a T-24h](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61512-diagrama-de-secuencia---cus-023-evaluar-quórum-automático-a-t-24h)
- **Diagrama 6.15.13:** [CUS-007: Gestionar sesión de mentoría y decisión resolutiva ante quórum insuficiente](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61513-diagrama-de-secuencia---cus-007-decisión-del-mentor-ante-quórum-insuficiente)

### MOD-06: Asistencia, Bitácoras y Feedback
- **Diagrama 6.15.14:** [CUS-012: Registrar asistencia interactiva a sesión de mentoría mediante código QR dinámico](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61514-diagrama-de-secuencia---cus-012-registrar-asistencia-a-sesión-de-mentoría)
- **Diagrama 6.15.15:** [CUS-013: Registrar bitácora pedagógica y reporte formativo de sesión de mentoría](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61515-diagrama-de-secuencia---cus-013-registrar-bitácora-pedagógica-de-sesión)
- **Diagrama 6.15.16:** [CUS-014: Visualizar historial académico integral de sesiones y bitácoras pedagógicas](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61516-diagrama-de-secuencia---cus-014-visualizar-historial-y-bitácoras-académicas)

### MOD-07: Gamificación e Incentivos
- **Diagrama 6.15.17:** [CUS-018: Emitir constancia oficial de horas de mentoría con firma criptográfica y QR](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61517-diagrama-de-secuencia---cus-018-emitir-constancia-institucional-de-horas-de-mentoría)
- **Diagrama 6.15.18:** [CUS-019: Gestionar insignias de logro formativo y reputación gamificada de mentores](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61518-diagrama-de-secuencia---cus-019-gestionar-insignias-y-reputación-gamificada)

### MOD-08: Analítica, Notificaciones y Configuración
- **Diagrama 6.15.19:** [CUS-009: Notificar eventos críticos y alertas de confirmación a T-24h](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61519-diagrama-de-secuencia---cus-009-notificar-eventos-críticos-y-alertas-temporales)
- **Diagrama 6.15.20:** [CUS-011: Generar reportes consolidados e indicadores analíticos de gestión de mentorías](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61520-diagrama-de-secuencia---cus-011-generar-reportes-e-indicadores-analíticos)
- **Diagrama 6.15.21:** [CUS-015: Consultar métricas de correlación de retención estudiantil y desempeño académico](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61521-diagrama-de-secuencia---cus-015-consultar-métricas-de-retención-y-desempeño)
- **Diagrama 6.15.22:** [CUS-016: Auditar trazas inmutables de seguridad y consentimientos legales digitales](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61522-diagrama-de-secuencia---cus-016-auditar-trazas-de-seguridad-y-consentimiento)
- **Diagrama 6.15.23:** [CUS-020: Configurar parámetros operativos institucionales y umbrales de gobernanza](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61523-diagrama-de-secuencia---cus-020-configurar-parámetros-institucionales-y-umbrales)
- **Diagrama 6.15.24:** [CUS-022: Gestionar catálogo de temas curriculares, asignaturas filtro y malla oficial](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md#diagrama-61524-diagrama-de-secuencia---cus-022-gestionar-catálogo-de-temas-y-materias-críticas)

---
Para visualizar el código fuente PlantUML completo y el desglose de los 7 niveles de participantes de cada caso de uso, consulte directamente [DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md](file:///d:/sistema_web_p2p/docs/diseño/DIAGRAMAS_DE_SECUENCIA_CONSOLIDADOS.md).
