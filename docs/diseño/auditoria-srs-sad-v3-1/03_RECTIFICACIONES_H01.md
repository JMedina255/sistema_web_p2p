# INFORME DE RECTIFICACIÓN DE HOMOLOGACIÓN Y EVIDENCIAS (H01-R)
## Auditoría y Refinamiento Documental SRS/SAD v3.1

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT<br>
**Curso:** Construcción de Software I<br>
**Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas<br>
**Equipo Consultor:** Grupo 03 / C-SharkTeam (Joan Cristian Medina Quispe y Renzo Antonio Antayhua Mamani)<br>
**Docente de Cátedra:** Dr. Ricardo Eduardo Valcárcel Alvarado<br>
**Semestre Académico:** 2026-II<br>
**Fecha de Emisión:** 14 de Noviembre de 2026<br>
**Rama de Trabajo:** `docs/srs-sad-v3-1-refinamiento-h02`<br>
**Commit Base Inicial de Auditoría:** `097f90d725e537f411ebadac740905e0c0448f61`<br>
**Commit Base Integrado en Main:** `0542aa2af8d30ecb6afdfa9d4561d0f07a1801b0` (PR #11)

---

## Control de Versiones

A continuación, se presenta el registro histórico de versiones del presente entregable de rectificación:

### Cuadro 3.1: Registro de Control de Versiones del Entregable H01-R

| Versión | Responsable | Revisada por | Aprobada por | Fecha | Descripción del Cambio |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1.0** | Joan Cristian Medina Quispe / Renzo Antonio Antayhua Mamani | Pendiente de revisión (Dr. Ricardo Valcárcel) | Pendiente de aprobación (Dirección EPIS) | 14/11/2026 | Emisión del informe de rectificación de homologación (H01-R): delimitación de tres estados metodológicos, rectificación de estatus en RF20, diferimiento explícito de edición del SAD, notas de validación en pruebas (682 históricas), registro de hallazgo `dummyIdToken` en frontend, unificación de autor a Joan Cristian y portabilidad de enlaces relativos. |

Fuente: Elaboración propia.

El presente cuadro certifica el origen formal del informe H01-R dentro del marco de auditoría continua, garantizando transparencia técnica y rigor metodológico ante las instancias evaluadoras de la Escuela Profesional de Ingeniería de Sistemas.

---

## 1. Propósito y Fundamento del Hito H01-R

El presente informe formaliza las rectificaciones técnicas y metodológicas aplicadas sobre los artefactos generados en los hitos preliminares H00 ([00_DIAGNOSTICO_Y_LINEA_BASE.md](./00_DIAGNOSTICO_Y_LINEA_BASE.md)) y H01 ([01_MATRIZ_HOMOLOGACION.md](./01_MATRIZ_HOMOLOGACION.md) y [02_GUIA_NARRATIVAS_DETALLADAS.md](./02_GUIA_NARRATIVAS_DETALLADAS.md)), los cuales fueron integrados en la rama principal `main` mediante el Pull Request #11 (commit merge `0542aa2af8d30ecb6afdfa9d4561d0f07a1801b0`).

La auditoría de control de calidad identificó la necesidad de subsanar inconsistencias interpretativas y documentales antes de acometer el refinamiento funcional del SRS (H02). En particular, se establece como principio rector que **una matriz de homologación o un consenso del equipo no equivale a tener las modificaciones efectivamente aplicadas en los documentos maestros (SRS y SAD)**.

---

## 2. Principio Metodológico Tripartito de Trazabilidad

A fin de evitar confusiones entre el diagnóstico de una desviación, el acuerdo técnico de solución y la edición efectiva de los documentos, se adopta formalmente la siguiente taxonomía de tres estados:

A continuación, se define la clasificación tripartita de estados documentales:

### Cuadro 3.2: Taxonomía de Estados Metodológicos de Homologación

| Estado Metodológico | Definición Operativa | Criterio de Verificación Documental | Aplicación Práctica en el Proyecto |
| :---: | :--- | :--- | :--- |
| **1. Discrepancia Diagnosticada** | Desviación técnica identificada formalmente entre la documentación histórica y la implementación en código fuente. | Evidenciada con citas textuales de secciones y líneas de código en el informe de línea base ([00_DIAGNOSTICO_Y_LINEA_BASE.md](./00_DIAGNOSTICO_Y_LINEA_BASE.md)). | Los 11 hallazgos críticos detectados (`HALL-01` al `HALL-11`). |
| **2. Decisión de Homologación Aprobada** | Criterio técnico y funcional consensuado por el equipo consultor para resolver la discrepancia. | Formalizada en la matriz canónica de trazabilidad ([01_MATRIZ_HOMOLOGACION.md](./01_MATRIZ_HOMOLOGACION.md)). | Aprobación de RF20 como CSAT 24h, Python 3.13, 16 tablas relacionales y servicios externos reales. |
| **3. Corrección Efectivamente Aplicada** | Edición material, redacción exhaustiva y validación formal dentro de los documentos maestros (SRS o SAD). | Reflejada en los archivos Markdown rectores (`FD03` y `FD04`) mediante generadores estables y auditada con scripts de verificación. | **En SRS:** Secciones 1–5 en H02; Casos de Uso en H04–H06.<br>**En SAD:** Vistas arquitectónicas y persistencia diferidas a H07–H09. |

Fuente: Elaboración propia.

El análisis del Cuadro 3.2 asegura que ningún evaluador asuma que un requisito o especificación arquitectónica se encuentra ya incorporada en los informes definitivos mientras permanezca en estado de decisión pendiente de redacción.

---

## 3. Registro Exhaustivo de Rectificaciones Aplicadas (H01-R)

A continuación, se desglosan las diez (10) rectificaciones obligatorias ejecutadas:

### Cuadro 3.3: Matriz de Rectificaciones Técnicas y Documentales del Hito H01-R

| Nº | Área / Componente | Situación Previa en H00/H01 | Rectificación Aplicada en H01-R | Impacto en Documentos y Código |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Trazabilidad de Commits** | Referencia única a commit `097f90d` sin explicitar el commit merge de PR #11. | Incorporación explícita del commit base inicial `097f90d725e537f411ebadac740905e0c0448f61` y del commit integrado en `main` `0542aa2af8d30ecb6afdfa9d4561d0f07a1801b0` (PR #11). | Mayor rigor y reproducibilidad histórica en cabeceras documentales. |
| **2** | **Definición de RF20** | Consignado como "Resuelto ✅" en Cuadro 1.2 y Cuadro 1.3 de la Matriz de Homologación. | Rectificado a **Decisión de homologación aprobada / Pendiente de aplicación en Sección 5 del SRS (H02)**. Se explicita que la Tabla 5.3 del SRS v3.0 aún conserva el texto histórico ("Recursos Académicos"). | Honestidad metodológica: se resolverá materialmente en H02 modificando `generate_part_a.py`. |
| **3** | **Actualización del SAD** | El informe sugería que el SAD ya incorporaba 16 tablas relacionales, Python 3.13 y servicios externos. | Se rectifica formalmente: **el SAD v3.0 actual contiene 15 tablas, declara Python 3.14 y carece de fichas de servicios externos**. Las decisiones están adoptadas, pero la edición del SAD está formalmente diferida a los hitos H07, H08 y H09. | Delimitación estricta del alcance: H02 no modificará el SAD. |
| **4** | **Consistencia CUS/RF** | Existían referencias cruzadas históricas residuales sobre CUS08 y CUS11. | Se ratifica la alineación canónica de diseño: `CUS-008` = Espacios Físicos (MOD-02) y `CUS-011` = Reportes Analíticos (MOD-08), quedando `CUS-012` para Asistencia y `CUS-013` para Bitácora. | Se programó su depuración textual exhaustiva en SRS Secciones 1–5 (H02). |
| **5** | **Estatus de Aprobación Institucional** | Tablas de control de versiones indicaban "Revisada por: Dr. Ricardo Valcárcel" y "Aprobada por: Dirección EPIS" como si estuviesen refrendadas. | Se sustituyen dichas afirmaciones por **"Pendiente de revisión (Dr. Ricardo Valcárcel)"** y **"Pendiente de aprobación (Dirección EPIS)"** en todos los cuadros de versiones de la auditoría. | Cumplimiento del principio de veracidad académica (ausencia de firma física o acta previa). |
| **6** | **Métrica de Pruebas Automatizadas** | Se afirmaba de forma categórica la existencia de 682 pruebas superadas con éxito al 100%. | Se consignan las **682 pruebas como cifra histórica reportada** en el commit `3f6e31d`, indicando que se encuentran **pendientes de nueva validación técnica** debido a que ejecuciones recientes del flujo de CI en `main` registraron fallos de linteo. | Precaución técnica: no sobreestimar el estado de verificación hasta la remediación del pipeline. |
| **7** | **Identidad de Autores** | Presencia errónea de "Joan Carlos Medina Quispe" en narrativas de diseño y scripts generadores. | Sustitución sistemática por el nombre oficial del estudiante: **Joan Cristian Medina Quispe** (Código 2022074255) en los archivos intervenidos (`mod01.py`, `mod04.py`, `audit_srs.py` y documentos de auditoría). | Corrección ortonímica y consistencia con padrón institucional UPT. |
| **8** | **Hallazgo Técnico `dummyIdToken`** | No estaba documentada la ruta de contingencia encontrada en el componente de login frontend. | Se incorpora como **HALL-11**: documentación técnica de `LoginOtpView.tsx` (líneas 263–272), donde `handleGoogleFederatedFallback` genera un token simulado en Base64 ante fallos del SDK de Google. | Catalogado como hallazgo de deuda técnica de seguridad pendiente; código fuente conservado intacto. |
| **9** | **Portabilidad de Enlaces** | Uso de esquemas de ruta absolutos locales de Windows (`file:///c:/Users/Admin/...`). | Reemplazo total por **rutas relativas portables de repositorio** (ej. `../FD03-EPIS-Informe SRS de Proyecto.md`, `../../../aplicacion/`). | Navegabilidad garantizada tanto en visualizadores locales como en GitHub. |
| **10** | **Actualización de Entregables H00 y H01** | Los archivos de auditoría previos no reflejaban las distinciones metodológicas precedentes. | Se actualizaron integralmente `00_DIAGNOSTICO_Y_LINEA_BASE.md`, `01_MATRIZ_HOMOLOGACION.md` y `02_GUIA_NARRATIVAS_DETALLADAS.md`, verificando consistencia cruzada. | Línea base saneada y lista para el inicio del hito H02. |

Fuente: Elaboración propia.

---

## 4. Detalle del Hallazgo Técnico HALL-11 (`dummyIdToken`)

Durante la inspección de código de frontend en `aplicacion/frontend/src/components/LoginOtpView.tsx`, se detectó la siguiente rutina de contingencia en el método `handleGoogleFederatedFallback`:

```typescript
// aplicacion/frontend/src/components/LoginOtpView.tsx (líneas 256–277)
try {
  const clean = email.trim().toLowerCase();
  const targetEmail =
    clean && (clean.endsWith('@virtual.upt.pe') || clean.endsWith('@upt.pe'))
      ? clean
      : 'ra2022073504@virtual.upt.pe';

  const mockPayload = btoa(
    JSON.stringify({
      email: targetEmail,
      given_name: 'Renzo Antonio',
      family_name: 'Antayhua Mamani',
    })
  );
  const dummyIdToken = `header.${mockPayload}.signature`;

  const resp = await authService.loginWithGoogle(dummyIdToken);
  setVerifyResult(resp);
  setStep('success');
  if (onLoginSuccess) {
    onLoginSuccess(resp);
  }
}
```

### Análisis Técnico y Recomendación
1. **Propósito Original:** Permitir el flujo de autenticación durante pruebas de interfaz en entornos locales desconectados de Internet o en computadoras de laboratorio donde el dominio institucional bloquee la carga del script `https://accounts.google.com/gsi/client`.
2. **Riesgo Identificado:** En un despliegue de producción real, este mecanismo permitiría iniciar sesión sin validación criptográfica de la firma del token de Google si el backend aceptara el payload simulado. En el backend actual (`auth_service.py`), el backend exige verificación de token o modo mock restringido por variables de entorno.
3. **Decisión Metodológica:** Se cataloga formalmente como **hallazgo de deuda técnica pendiente de mitigación**. De acuerdo con la regla rectora número 1 ("No modificar código funcional de frontend ni backend"), **no se realiza modificación alguna sobre `LoginOtpView.tsx` en este hito**, difiriéndose su remediación a la fase de construcción y seguridad del sistema.

---

## 5. Validación de Scripts y Consistencia

Se ejecutó la suite de auditoría estructural sobre las narrativas y artefactos generados tras la corrección del nombre de autor a Joan Cristian Medina Quispe:

```text
=== Auditing docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md ===
Total CUS blocks found: 24
Results for docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md: 0 errors.

=== Auditando Diagramas de Secuencia: docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md ===
Total diagramas encontrados: 24
Resultado auditoría docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md: 0 errores detectados.
```

Ambas herramientas certifican el 100% de cumplimiento de los criterios estructurales, validando que la rectificación no introdujo regresiones en los archivos del proyecto.

---

## 6. Conclusión y Habilitación del Hito H02

El presente informe H01-R rectifica las imprecisiones documentales previas, delimita con estricta rigurosidad los tres estados metodológicos y deja expedita la línea de trabajo para ejecutar el **Hito H02: Refinamiento Funcional del SRS**, el cual intervendrá las secciones 1 a 5 de `docs/diseño/FD03-EPIS-Informe SRS de Proyecto.md` a través de su generador canónico `tools/design_sections/generate_part_a.py`.