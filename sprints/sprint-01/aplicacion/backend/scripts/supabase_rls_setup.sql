-- ============================================================================
-- Script de Configuración de Políticas RLS (Row Level Security) para Supabase
-- Proyecto: Sistema Web P2P - EPIS UPT (Construcción de Software I, 2026-II)
-- Tarea: T-07 (Implementar políticas RLS iniciales - PB-008 / RNF02)
-- ============================================================================

-- 1. Habilitación obligatoria de RLS en las tablas de la aplicación
ALTER TABLE IF EXISTS asignaturas ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS temas_conceptuales ENABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS auth_challenges ENABLE ROW LEVEL SECURITY;

-- Garantizar que RLS aplique a clientes PostgREST/anon/authenticated sin bloquear al propietario de BD (postgres)
ALTER TABLE IF EXISTS asignaturas NO FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS temas_conceptuales NO FORCE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS auth_challenges NO FORCE ROW LEVEL SECURITY;

-- Concesión de permisos de tabla requeridos para que RLS pueda operar
GRANT SELECT ON asignaturas TO anon, authenticated;
GRANT SELECT ON temas_conceptuales TO anon, authenticated;
GRANT ALL ON asignaturas TO service_role;
GRANT ALL ON temas_conceptuales TO service_role;

GRANT SELECT, INSERT, UPDATE ON auth_challenges TO anon, authenticated;
GRANT ALL ON auth_challenges TO service_role;

-- ============================================================================
-- 2. Políticas para el Catálogo Curricular (asignaturas y temas_conceptuales)
-- ============================================================================

-- Lectura pública para alumnos, mentores y visitantes (CUS21 / RF05)
DROP POLICY IF EXISTS "p2p_curriculum_asignaturas_select_public" ON asignaturas;
CREATE POLICY "p2p_curriculum_asignaturas_select_public"
ON asignaturas FOR SELECT
TO anon, authenticated
USING (estado_activo = true);

DROP POLICY IF EXISTS "p2p_curriculum_temas_select_public" ON temas_conceptuales;
CREATE POLICY "p2p_curriculum_temas_select_public"
ON temas_conceptuales FOR SELECT
TO anon, authenticated
USING (estado_activo = true);

-- Inserción, actualización y borrado restringidos exclusivamente a Administradores o service_role
DROP POLICY IF EXISTS "p2p_curriculum_asignaturas_admin_all" ON asignaturas;
CREATE POLICY "p2p_curriculum_asignaturas_admin_all"
ON asignaturas FOR ALL
TO authenticated, service_role
USING (
    coalesce(auth.jwt() ->> 'role', '') = 'administrador'
    OR coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin'
    OR current_user = 'service_role'
)
WITH CHECK (
    coalesce(auth.jwt() ->> 'role', '') = 'administrador'
    OR coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin'
    OR current_user = 'service_role'
);

DROP POLICY IF EXISTS "p2p_curriculum_temas_admin_all" ON temas_conceptuales;
CREATE POLICY "p2p_curriculum_temas_admin_all"
ON temas_conceptuales FOR ALL
TO authenticated, service_role
USING (
    coalesce(auth.jwt() ->> 'role', '') = 'administrador'
    OR coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin'
    OR current_user = 'service_role'
)
WITH CHECK (
    coalesce(auth.jwt() ->> 'role', '') = 'administrador'
    OR coalesce(auth.jwt() -> 'app_metadata' ->> 'role', '') = 'admin'
    OR current_user = 'service_role'
);

-- ============================================================================
-- 3. Políticas para Desafíos OTP y Autenticación (auth_challenges)
-- ============================================================================

-- Acceso irrestricto para operaciones backend directas mediante clave service_role
DROP POLICY IF EXISTS "p2p_auth_challenges_service_all" ON auth_challenges;
CREATE POLICY "p2p_auth_challenges_service_all"
ON auth_challenges FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Inserción de desafíos: Solo permitida para correos con terminación estricta @upt.pe
DROP POLICY IF EXISTS "p2p_auth_challenges_insert_upt" ON auth_challenges;
CREATE POLICY "p2p_auth_challenges_insert_upt"
ON auth_challenges FOR INSERT
TO anon, authenticated
WITH CHECK (
    email LIKE '%@upt.pe'
    AND expires_at > now()
);

-- Lectura de desafíos: Limitada a la verificación activa del desafío
DROP POLICY IF EXISTS "p2p_auth_challenges_select_active" ON auth_challenges;
CREATE POLICY "p2p_auth_challenges_select_active"
ON auth_challenges FOR SELECT
TO anon, authenticated
USING (
    email LIKE '%@upt.pe'
    AND consumed = false
    AND expires_at > now()
);

-- Actualización: Solo para marcar el desafío como consumido tras verificación exitosa
DROP POLICY IF EXISTS "p2p_auth_challenges_update_consumed" ON auth_challenges;
CREATE POLICY "p2p_auth_challenges_update_consumed"
ON auth_challenges FOR UPDATE
TO anon, authenticated
USING (
    consumed = false
)
WITH CHECK (
    consumed = true
);

-- ============================================================================
-- 4. Verificación de estado de políticas
-- ============================================================================
SELECT 
    schemaname, 
    tablename, 
    policyname, 
    permissive, 
    roles, 
    cmd 
FROM pg_policies 
WHERE tablename IN ('asignaturas', 'temas_conceptuales', 'auth_challenges')
ORDER BY tablename, policyname;
