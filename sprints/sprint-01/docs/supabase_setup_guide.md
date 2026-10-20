# Guía Canónica de Configuración de Supabase — Sistema Web P2P EPIS-UPT

**Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
**Curso:** Construcción de Software I  
**Institución:** Universidad Privada de Tacna — Escuela Profesional de Ingeniería de Sistemas  
**Equipo:** Grupo 03 — Joan Medina / Renzo Antayhua  
**Vigencia:** Semestre 2026-II  
**Tareas Asociadas:** T-01 (Conexión Supabase), T-03 (Autenticación y Sesión), T-07 (Políticas RLS), T-09 (Catálogo Curricular)  

---

## 1. Propósito y Alcance

La presente guía proporciona las directrices paso a paso para vincular un proyecto existente en la plataforma **Supabase** con el entorno de desarrollo del **Sistema Web P2P**. Se instruye al desarrollador o evaluador sobre la obtención de credenciales de red, la ejecución de las migraciones del catálogo curricular (**T-09**), el aprovisionamiento de las políticas de seguridad a nivel de fila (**RLS - T-07**) y la sincronización del secreto criptográfico para la emisión de tokens JWT de sesión (**T-03**).

---

## 2. Parámetros Técnicos y Requisitos Previos

A continuación, se especifican las variables y credenciales requeridas en el archivo local `aplicacion/backend/.env`:

### Cuadro 2.1: Parámetros de Entorno y Configuración de Supabase

| Parámetro | Ubicación en Supabase Dashboard | Propósito en el Sistema | Ejemplo Representativo |
| :--- | :--- | :--- | :--- |
| **`DATABASE_URL`** | Project Settings → Database → Connection string → URI (Pestaña *Session pooler*, IPv4) | Conexión del motor SQLAlchemy y migraciones Alembic | `postgresql+psycopg://postgres.[REF]:[PASS]@[HOST]:5432/postgres?sslmode=require` |
| **`JWT_SECRET_KEY`** | Project Settings → API → JWT Settings → JWT Secret | Firma y validación de tokens de sesión emitidos en el acceso OTP | `tu-supabase-jwt-secret-super-seguro` |
| **`APP_ENV`** | Variable local del entorno | Habilita endpoints de diagnóstico como `/api/v1/health/db` | `development` |

Fuente: Elaboración propia conforme a la arquitectura de seguridad SAD FD04 y PB-008.

Como se observa en el cuadro anterior, la cadena de conexión debe emplear el **Session Pooler** (puerto 5432 o 6543) para permitir la conectividad desde redes domésticas o institucionales que utilicen direccionamiento IPv4, asegurando que la contraseña de PostgreSQL tenga sus caracteres especiales codificados en formato URL (%-encoding).

---

## 3. Pasos de Configuración en Supabase y Entorno Local

### Paso 1: Obtención de la Cadena de Conexión (Session Pooler)
1. Inicie sesión en la consola web de [Supabase](https://supabase.com/dashboard).
2. Seleccione su proyecto activo.
3. Puede obtener la cadena de conexión por dos vías:
   - **Vía Rápida (Botón Connect):** En la barra superior de su proyecto, haga clic en el botón verde **Connect** → pestaña **ORM** (o **URI**) → seleccione **Session Pooler** (puerto `5432`, IPv4).
   - **Vía Configuración del Proyecto:** En la barra lateral izquierda, haga clic en **Project Settings** (ícono de engranaje) → **Database** → sección **Connection string** → pestaña **URI** → elija **Session pooler** (puerto `5432`).
4. Copie la cadena provista. Reemplace `[YOUR-PASSWORD]` por la contraseña maestra de PostgreSQL que asignó al crear su proyecto. Si su contraseña contiene caracteres especiales como `@`, `:`, `#` o `/`, debe codificarlos en formato URL (por ejemplo, `@` se codifica como `%40`).

### Paso 2: Configuración del Archivo `.env` del Backend
1. Abra el archivo `aplicacion/backend/.env` (o copie desde `.env.example`).
2. Configure los valores de la siguiente manera:

```dotenv
APP_ENV=development
PROJECT_NAME="Sistema Web P2P - EPIS UPT"
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]

# Cadena de conexión Session Pooler de Supabase (puerto 5432)
DATABASE_URL="postgresql+psycopg://postgres.TU_PROJECT_REF:TU_PASSWORD_CODIFICADO@TU_POOLER_HOST:5432/postgres?sslmode=require"

# Secreto JWT copiado de Supabase Dashboard (Project Settings -> API -> JWT Settings -> JWT Secret)
JWT_SECRET_KEY="tu-supabase-jwt-secret-de-32-caracteres-o-mas"
```

### Paso 3: Aplicación de Migraciones de Base de Datos (Alembic)
Para crear las tablas de catálogo curricular (`asignaturas`, `temas_conceptuales`), la tabla de auditoría OTP (`auth_challenges`), cargar automáticamente las **5 materias filtro** con sus temas silábicos y sincronizar la secuencia de claves primarias:

```powershell
# Desde la raíz del backend:
cd aplicacion/backend

# Con el entorno virtual activo:
.\.venv\Scripts\activate

# Ejecutar las migraciones hacia Supabase:
alembic upgrade head
```

*Resultado esperado:* Alembic ejecutará la revisión `20261019_001`, creará las 3 tablas con sus índices, insertará los registros semilla de *Cálculo I, Cálculo II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*, y sincronizará automáticamente la secuencia autoincremental `asignaturas_id_asignatura_seq` para garantizar inserciones futuras sin colisión de claves primarias.

### Paso 4: Activación de Políticas RLS (Row Level Security - T-07)
1. En el Dashboard de Supabase de su proyecto, abra la sección **SQL Editor** en la barra lateral.
2. Haga clic en **New query** (Nueva consulta).
3. Abra el archivo `aplicacion/backend/scripts/supabase_rls_setup.sql` del repositorio, copie todo su contenido y péguelo en el editor de Supabase.
4. Haga clic en el botón verde **Run** (Ejecutar).

*Efecto de seguridad:*
- Se habilita `ROW LEVEL SECURITY` en las tablas `asignaturas`, `temas_conceptuales` y `auth_challenges`.
- Se otorgan permisos explícitos de tabla (`GRANT SELECT`, `GRANT ALL`) para roles `anon`, `authenticated` y `service_role`.
- Se autoriza la **lectura pública** del catálogo de cursos y temas silábicos para la SPA React.
- Se restringen las operaciones de inserción y modificación de cursos exclusivamente a usuarios con rol `administrador` o conexiones autenticadas con `service_role`.
- Se blinda la tabla `auth_challenges` permitiendo la emisión únicamente para correos con dominio oficial `@upt.pe` y evitando la lectura de códigos por usuarios no autorizados.

### Paso 5: Comprobación de Conectividad y Salud
1. Inicie el servidor FastAPI:
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
2. Abra en su navegador el endpoint de salud de base de datos:
   `http://localhost:8000/api/v1/health/db`
   Debe responder:
   ```json
   {
     "status": "connected",
     "database": "postgresql",
     "detail": "Conexión a PostgreSQL (Supabase) verificada con éxito",
     "latency_ms": 125.4,
     "environment": "development"
   }
   ```
3. Abra el endpoint del catálogo curricular:
   `http://localhost:8000/api/v1/curriculum/courses`
   Debe responder con la lista de las 5 materias filtro persistidas en su proyecto Supabase.

---

## 4. Matriz de Trazabilidad y Verificación

A continuación, se presenta la matriz de validación técnica de las tareas vinculadas a Supabase:

### Cuadro 4.1: Matriz de Verificación de Integración con Supabase

| ID Tarea | Requisito / CUS | Artefacto de Integración | Mecanismo de Verificación | Estado |
| :--- | :--- | :--- | :--- | :---: |
| **T-01** | PB-001 / RNF09 | `app/db/session.py` | Consulta `SELECT 1` y endpoint `/api/v1/health/db` | ✅ Verificado |
| **T-09** | PB-006 / CUS21 | Migración `20261019_001` | Creación de tablas e inserción de 5 materias filtro | ✅ Verificado |
| **T-07** | PB-008 / RNF02 | `supabase_rls_setup.sql` | `ENABLE ROW LEVEL SECURITY` y políticas de catálogo/OTP | ✅ Verificado |
| **T-03** | PB-002 / CUS01 | `app/api/v1/endpoints/auth.py` | Emisión y verificación OTP con JWT firmado | ✅ Verificado |

Fuente: Elaboración propia conforme al Plan de Sprints y Tareas (`PLAN_SPRINTS_Y_TAREAS.md`).

La correcta aplicación de estos 5 pasos asegura que el proyecto en la nube opere bajo los más rigurosos estándares de seguridad y trazabilidad académica, garantizando la persistencia institucional de la Escuela Profesional de Ingeniería de Sistemas de la Universidad Privada de Tacna.
