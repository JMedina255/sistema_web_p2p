# Documento de Formalización 06: Implementación de Navegación y Protección de Vistas por Rol (RBAC)

**Proyecto:** Sistema Web P2P de Mentorías Académicas — EPIS UPT  
**Fase:** Fase 03 — Navegación Dinámica y Guardas Frontend por Perfil  
**Rama:** `feat/formalizacion-ux-roles`  
**Directorio de Trabajo:** `C:\Users\Admin\Desktop\Proyectos\sistema_web_p2p-formalizacion`  
**Fecha:** 7 de noviembre de 2026  
**Estado:** COMPLETADO CON ÉXITO (311 pruebas passing, 0 errores ESLint)

---

## 1. Resumen Ejecutivo

La Fase 03 de la formalización del Sistema Web P2P ha transformado la arquitectura de navegación del frontend, sustituyendo la barra estática de demostración técnica por un sistema integral de **Control de Acceso Basado en Roles (RBAC)** y navegación contextual dinámica.

### Objetivos Alcanzados
1. **Diferenciación estricta entre Visitantes y Usuarios Autenticados:** Los visitantes solo tienen acceso al inicio de sesión institucional (`auth`) y al catálogo público de cursos (`curriculum`).
2. **Menú Dinámico por Rol Activo:** Cada perfil institucional (`mentoreado`, `mentor`, `administrador`) visualiza exclusivamente las opciones pertinentes a sus responsabilidades académicas.
3. **Guardas de Renderizado Preventivas (`ProtectedView`):** Las vistas privadas no se montan ni renderizan en el DOM si el usuario no dispone de sesión activa o del rol autorizado, impidiendo la emisión de solicitudes de red no autorizadas y eliminando toda posibilidad de fuga de información.
4. **Eliminación Total de Credenciales Simuladas por Defecto:** Se erradicaron definitivamente los correos ficticios de respaldo (`admin.epis@upt.pe` y `mentor.avanzado@upt.pe`), exigiendo identidad autenticada real (`user.email`).
5. **Sincronización Bidireccional de URL (`?tab=`):** Soporte completo para navegación directa mediante parámetro de consulta con validación y sanitización determinista.
6. **Conmutación Reactiva de Perfiles Multi-rol:** Los usuarios con múltiples roles asignados pueden alternar libremente su rol activo desde el encabezado institucional, adaptando inmediatamente el menú y redirigiendo a la vista principal correspondiente.
7. **Batería de Pruebas Automatizadas NAV-01 a NAV-14:** Implementación y aprobación al 100% de los 14 escenarios de prueba de navegación, logrando un total de 311 pruebas unitarias e integrales exitosas en Vitest.

---

## 2. Arquitectura de Navegación Modular

Se diseñó e implementó una arquitectura desacoplada y escalable bajo los directorios `src/navigation/`, `src/components/layout/` y `src/components/auth/`:

```
aplicacion/frontend/src/
├── navigation/
│   ├── navigationConfig.ts        # Tipos canónicos NavTab, matriz de pestañas y resolución por rol
│   ├── navigationPermissions.ts   # Políticas puras de autorización (canAccessTab, sanitizeRequestedTab)
│   └── __tests__/
│       └── navigation.test.tsx    # Batería de pruebas automatizadas NAV-01 a NAV-14
├── components/
│   ├── auth/
│   │   └── ProtectedView.tsx      # Componente guard de protección y bloqueo de renderizado
│   └── layout/
│       ├── Header.tsx             # Identidad UPT, sesión, conmutador de rol y estado legal
│       ├── RoleNavigation.tsx     # Selector contextual de pestañas (WAI-ARIA accessible)
│       ├── Footer.tsx             # Pie institucional formal de la Escuela Profesional
│       └── AppLayout.tsx          # Shell unificado que orquesta layout y flujos guiados
└── App.tsx                        # Integración reactiva del Shell con AuthContext y vistas de negocio
```

### 2.1. Configuración Centralizada (`navigationConfig.ts`)
Define el tipo de unión canónico `NavTab` y el registro exhaustivo `NAVIGATION_ITEMS`:
- `auth`: Iniciar sesión (`visitor`, `requiresAuth: false`)
- `consent`: Consentimiento informado (`mentoreado`, `mentor`, `administrador`, `requiresAuth: true`)
- `curriculum`: Catálogo curricular (`visitor`, `mentoreado`, `mentor`, `administrador`, `requiresAuth: false`)
- `recommendations`: Explorar mentorías (`mentoreado`, `requiresAuth: true`, default mentoreado)
- `bookings`: Mis reservas (`mentoreado`, `requiresAuth: true`)
- `profile`: Mi perfil formativo (`mentoreado`, `mentor`, `requiresAuth: true`)
- `sessions`: Mis sesiones de mentoría (`mentor`, `requiresAuth: true`, default mentor)
- `offers`: Publicar mentoría (`mentor`, `requiresAuth: true`)
- `admin`: Panel directivo institucional (`administrador`, `requiresAuth: true`, default administrador)
- `services`: Estado y telemetría de servicios (`administrador`, `requiresAuth: true`)

### 2.2. Políticas y Verificación de Permisos (`navigationPermissions.ts`)
Provee funciones puras de decisión:
- `isTabProtected(tab: NavTab): boolean`
- `canAccessTab(tab: NavTab, activeRole: UserRole | null, isAuthenticated: boolean): boolean`
- `getDefaultTabForRole(role: UserRole | null): NavTab`
- `isValidTab(tab: unknown): tab is NavTab`
- `sanitizeRequestedTab(requestedTab: string | null, activeRole, isAuthenticated, strictAuthorization?): NavTab`

---

## 3. Matriz de Permisos y Menús por Rol

| Pestaña (`NavTab`) | Etiqueta Visible | Visitante | Mentoreado | Mentor | Administrador | Vista por Defecto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `auth` | 🔐 Iniciar sesión | ✅ | — | — | — | **Visitante** |
| `curriculum` | 📚 Cursos | ✅ | ✅ | ✅ | ✅ | — |
| `recommendations`| 🎯 Explorar mentorías| ❌ | ✅ | ❌ | ❌ | **Mentoreado** |
| `bookings` | 📅 Mis reservas | ❌ | ✅ | ❌ | ❌ | — |
| `profile` | 👤 Mi perfil | ❌ | ✅ | ✅ | ❌ | — |
| `sessions` | 📋 Mis sesiones | ❌ | ❌ | ✅ | ❌ | **Mentor** |
| `offers` | 🏷️ Publicar mentoría | ❌ | ❌ | ✅ | ❌ | — |
| `admin` | 🛡️ Administración | ❌ | ❌ | ❌ | ✅ | **Administrador** |
| `services` | 🛰️ Estado del sistema| ❌ | ❌ | ❌ | ✅ | — |
| `consent` | ⚖️ Consentimiento | ❌ | ✅ (vía modal)| ✅ (vía modal)| ✅ (vía modal)| — |

---

## 4. Funcionamiento de la Guarda `ProtectedView`

El componente `<ProtectedView>` encapsula el renderizado de cada módulo asegurando tres niveles de protección:

1. **Nivel Público (ej. `curriculum`):**  
   Se renderiza directamente para cualquier usuario sin comprobación de credenciales.
2. **Nivel Privado sin Autenticación (`!isAuthenticated`):**  
   - **Bloqueo absoluto de montaje:** Los componentes hijos (`children`) **no se instancian ni se montan en el DOM**, evitando llamadas no autorizadas al backend o el uso de identidades sustitutas.
   - **Tarjeta Institucional de Acceso Restringido:** Se despliega un panel accesible (`role="region"`, `aria-label="Acceso Restringido"`) con el mensaje oficial de la UPT:  
     *"Para consultar este módulo institucional, debes iniciar sesión con tu cuenta institucional de la Universidad Privada de Tacna (@upt.pe)."*
   - Botón primario: `Iniciar Sesión Institucional` (redirige fluidamente a la pestaña `auth`).
3. **Nivel Privado con Rol No Autorizado (`!canAccessTab`):**  
   - **Bloqueo absoluto de montaje:** Se previene la carga del módulo solicitado.
   - **Alerta Accesible (`role="alert"`):** Se informa al usuario que su perfil activo no dispone de privilegios para el módulo solicitado.
   - **Detección de Roles Alternativos:** Si el usuario posee múltiples roles y uno de sus otros roles sí tiene acceso permitido, se despliega una sugerencia interactiva con el botón `Cambiar a perfil [rol]`.
   - Botón de retorno: `Volver a mi panel principal` (redirige a la vista por defecto autorizada de su rol activo).

---

## 5. Eliminación de Credenciales Ficticias

En cumplimiento estricto de los principios de seguridad de la arquitectura formalizada:
- Se eliminó `mentorEmail={studentEmail ?? 'mentor.avanzado@upt.pe'}` de `MentorSessionsView`. Ahora consume directamente `user.email` garantizado por `ProtectedView`.
- Se eliminó `adminEmail={studentEmail ?? 'admin.epis@upt.pe'}` de `AdminDashboardView`.
- Se eliminó el parámetro por defecto `adminEmail = 'admin.epis@upt.pe'` dentro de `AdminDashboardView.tsx`.
- Toda operación de negocio en el frontend está indefectiblemente ligada a una sesión JWT válida expedida a una dirección `@upt.pe`.

---

## 6. Sincronización con URL y Persistencia de Sesión

### Parámetros de Consulta (`?tab=`)
- La aplicación lee el parámetro `?tab=` en el arranque mediante `sanitizeRequestedTab`.
- Si se proporciona un valor no reconocido (ej. `?tab=hack123`), se normaliza inmediatamente hacia la pestaña por defecto del perfil activo.
- Si se proporciona una ruta válida pero protegida (ej. `?tab=admin` para un visitante o mentoreado), la aplicación carga dicha pestaña en el estado pero `ProtectedView` intercepta el renderizado mostrando la tarjeta de restricción o no autorización correspondiente.
- Toda conmutación de pestaña actualiza la URL mediante `window.history.pushState` sin recarga de página.
- Se implementó un escuchador para eventos `popstate`, garantizando que los botones "Atrás" y "Adelante" del navegador funcionen correctamente.

### Reanudación Sin Parpadeos (NAV-12)
- Se optimizó la inicialización del estado en `AuthContext.tsx`, permitiendo resolver de manera síncrona el usuario inicial y el rol activo desde el token JWT almacenado en `authService.getToken()` y `sessionStorage.getItem('p2p_active_role')`.
- Esto previene el parpadeo de la pantalla de login durante el montaje de la aplicación y garantiza que los tests y usuarios autenticados aterricen de inmediato en su panel correspondiente.

---

## 7. Batería de Pruebas Automatizadas (NAV-01 a NAV-14)

Se diseñó la suite `src/navigation/__tests__/navigation.test.tsx` con cobertura del 100% de los escenarios solicitados:

| Código | Escenario de Prueba | Resultado |
| :--- | :--- | :---: |
| **NAV-01** | Visitante no autenticado visualiza únicamente 'auth' y 'curriculum' | **PASSED** |
| **NAV-02** | Visitante que consulta `?tab=admin` recibe tarjeta de Acceso Restringido sin montar panel directivo | **PASSED** |
| **NAV-03** | Visitante que consulta `?tab=sessions` recibe tarjeta de Acceso Restringido sin montar panel de mentor | **PASSED** |
| **NAV-04** | Usuario Mentoreado visualiza menú de estudiante y aterriza por defecto en recomendaciones | **PASSED** |
| **NAV-05** | Usuario Mentoreado que consulta `?tab=admin` recibe Acceso No Autorizado y botón de retorno | **PASSED** |
| **NAV-06** | Usuario Mentor visualiza menú de mentor y aterriza por defecto en sesiones | **PASSED** |
| **NAV-07** | Usuario Mentor que consulta `?tab=admin` recibe bloqueo por falta de rol administrativo | **PASSED** |
| **NAV-08** | Usuario Administrador visualiza menú directivo y aterriza por defecto en administración | **PASSED** |
| **NAV-09** | Usuario multi-rol conmute perfiles, actualizando menú y vistas de forma reactiva | **PASSED** |
| **NAV-10** | Cierre de sesión destruye tokens, limpia storage y retorna al formulario de visitante | **PASSED** |
| **NAV-11** | Pestaña de consentimiento informed está disponible y refleja la política de privacidad | **PASSED** |
| **NAV-12** | Sesión persistida en storage se reanuda síncronamente sin parpadeo de pantalla de login | **PASSED** |
| **NAV-13** | Pestaña inexistente en URL (`?tab=inexistente123`) se sanitiza redirigiendo al panel por defecto | **PASSED** |
| **NAV-14** | Acceso autorizado a Cursos renderiza el catálogo para cualquier perfil sin restricciones | **PASSED** |

---

## 8. Resultados Globales de Verificación

### 8.1. Pruebas Automatizadas (Vitest)
```
Test Files:  29 passed (29)
Tests:       311 passed (311)
Duration:    38.19s
Status:      100% SUCCESS
```

### 8.2. Calidad de Código (ESLint)
```
> eslint .
Status: 0 errors, 0 warnings
```

### 8.3. Verificación de Tipos TypeScript (`tsconfig.app.json`)
```
Código de aplicación (App.tsx, layout, navigation, ProtectedView, context): 0 errores.
(Las únicas 3 advertencias conocidas corresponden a pruebas del Sprint 04 en MentorSessionsView.test.tsx asignadas a la Fase 04).
```

---

## 9. Próximos Pasos (Hacia la Fase 04)

Con la navegación contextual y la protección de vistas del frontend plenamente operativas, el sistema se encuentra listo para la **Fase 04: Formalización de Autorización y Endpoints FastAPI**:
1. Implementación de dependencias de autorización RBAC en el backend (`require_role("mentor")`, `require_role("administrador")`).
2. Sincronización del contrato JWT entre frontend y backend para claims de roles.
3. Validación de autorización a nivel de endpoints y pruebas de integración API.
