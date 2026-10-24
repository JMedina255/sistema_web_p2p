-- ==============================================================================
-- Script de Seguridad a Nivel de Fila (Row Level Security - RLS) para Supabase
-- Proyecto: Sistema Web P2P - EPIS UPT (Sprint 2)
-- Tareas Vinculadas: T-05, T-08, T-12, T-13
-- Requerimientos: RF02, RF03, RF04, RN-02, RN-03, RNF02 (Aislamiento de Privacidad)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Habilitación de Row Level Security (RLS) en las 5 tablas del Sprint 2
-- ------------------------------------------------------------------------------
ALTER TABLE consentimientos_legales ENABLE ROW LEVEL SECURITY;
ALTER TABLE roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE usuario_roles ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_academicos ENABLE ROW LEVEL SECURITY;
ALTER TABLE disponibilidades_horarias ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------------------
-- 2. Políticas para 'consentimientos_legales' (T-05 / RF02 / Ley N° 29733)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS p_consentimientos_select_propio ON consentimientos_legales;
-- Lectura: los estudiantes solo pueden consultar sus propios consentimientos legales
CREATE POLICY p_consentimientos_select_propio
ON consentimientos_legales
FOR SELECT
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
);

DROP POLICY IF EXISTS p_consentimientos_insert_propio ON consentimientos_legales;
-- Inserción: los estudiantes solo pueden registrar conformidad para su propio correo
CREATE POLICY p_consentimientos_insert_propio
ON consentimientos_legales
FOR INSERT
TO authenticated
WITH CHECK (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
);

-- ------------------------------------------------------------------------------
-- 3. Políticas para 'roles' (T-08 / RF03 / CUS10)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS p_roles_select_todos ON roles;
-- Lectura: cualquier usuario autenticado puede consultar el catálogo de roles
CREATE POLICY p_roles_select_todos
ON roles
FOR SELECT
TO authenticated
USING (true);

DROP POLICY IF EXISTS p_roles_modificar_admin ON roles;
-- Modificación: reservada exclusivamente para service_role y administradores
CREATE POLICY p_roles_modificar_admin
ON roles
FOR ALL
TO authenticated
USING (
    (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
);

-- ------------------------------------------------------------------------------
-- 4. Políticas para 'usuario_roles' (T-08 / RF03 / RN-03 / T-13)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS p_usuario_roles_select ON usuario_roles;
-- Lectura: el usuario puede ver sus propios roles o un administrador puede ver todos
CREATE POLICY p_usuario_roles_select
ON usuario_roles
FOR SELECT
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
);

DROP POLICY IF EXISTS p_usuario_roles_admin_only ON usuario_roles;
-- Inserción / Actualización / Eliminación: solo administradores institucionales
-- Se prohíbe de forma terminante la autopromoción a mentor sin validación (T-13)
CREATE POLICY p_usuario_roles_admin_only
ON usuario_roles
FOR ALL
TO authenticated
USING (
    (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
)
WITH CHECK (
    (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
);

-- ------------------------------------------------------------------------------
-- 5. Políticas para 'perfiles_academicos' (T-12 / RF04 / CUS15 / T-13)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS p_perfiles_select ON perfiles_academicos;
-- Lectura: cada estudiante consulta su perfil privado, administradores y mentores pueden consultar perfiles asignados
CREATE POLICY p_perfiles_select
ON perfiles_academicos
FOR SELECT
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol IN ('administrador', 'mentor') AND ur.activo = true
    )
);

DROP POLICY IF EXISTS p_perfiles_modificar_propio ON perfiles_academicos;
-- Inserción / Actualización: un estudiante solo puede modificar su propio perfil
CREATE POLICY p_perfiles_modificar_propio
ON perfiles_academicos
FOR ALL
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol = 'administrador' AND ur.activo = true
    )
)
WITH CHECK (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
);

-- ------------------------------------------------------------------------------
-- 6. Políticas para 'disponibilidades_horarias' (T-12 / RF04 / CUS15)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS p_disponibilidad_select ON disponibilidades_horarias;
-- Lectura: disponibilidad visible para el propio estudiante y para el algoritmo de emparejamiento / mentores
CREATE POLICY p_disponibilidad_select
ON disponibilidades_horarias
FOR SELECT
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
    OR (auth.jwt() ->> 'email') IN (
        SELECT ur.email FROM usuario_roles ur
        JOIN roles r ON ur.id_rol = r.id_rol
        WHERE r.nombre_rol IN ('administrador', 'mentor') AND ur.activo = true
    )
);

DROP POLICY IF EXISTS p_disponibilidad_modificar_propio ON disponibilidades_horarias;
-- Inserción / Actualización / Borrado: solo el titular puede modificar sus bloques de agenda
CREATE POLICY p_disponibilidad_modificar_propio
ON disponibilidades_horarias
FOR ALL
TO authenticated
USING (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
)
WITH CHECK (
    email = (auth.jwt() ->> 'email')
    OR (auth.jwt() ->> 'role') = 'service_role'
);

-- Fin del script RLS Sprint 2
