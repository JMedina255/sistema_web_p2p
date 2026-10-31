-- ==============================================================================
-- Script de Seguridad a Nivel de Fila (Row Level Security - RLS) para Supabase
-- Proyecto: Sistema Web P2P - EPIS UPT (Sprint 4: Reservas y Quórum)
-- Tareas Vinculadas: T-22, T-24
-- Requerimientos: RF12, RF13, RF15, RN-05, RN-08, RN-09, RNF07 (Prevención de Sobrecupo)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. Habilitación de Row Level Security (RLS) en las tablas del Sprint 4
-- ------------------------------------------------------------------------------
ALTER TABLE reservas_cupo ENABLE ROW LEVEL SECURITY;
ALTER TABLE solicitudes_demanda ENABLE ROW LEVEL SECURITY;

-- ------------------------------------------------------------------------------
-- 2. Políticas para 'reservas_cupo' (T-22 / T-24 / CUS04 / RF12 / RNF07)
-- ------------------------------------------------------------------------------

-- Lectura: Estudiante ve sus propias reservas; Mentor ve reservas de sus sesiones; Administrador ve todas
DROP POLICY IF EXISTS rls_reservas_select ON reservas_cupo;
CREATE POLICY rls_reservas_select ON reservas_cupo
FOR SELECT TO authenticated
USING (
    auth.jwt() ->> 'email' = estudiante_email OR
    EXISTS (
        SELECT 1 FROM sesiones_mentoria s
        WHERE s.id_sesion = reservas_cupo.id_sesion
          AND s.mentor_email = auth.jwt() ->> 'email'
    ) OR
    auth.jwt() ->> 'role' = 'administrador'
);

-- Inserción: Solo el estudiante autenticado puede reservar para su propia cuenta
DROP POLICY IF EXISTS rls_reservas_insert ON reservas_cupo;
CREATE POLICY rls_reservas_insert ON reservas_cupo
FOR INSERT TO authenticated
WITH CHECK (
    auth.jwt() ->> 'email' = estudiante_email
);

-- Modificación: Titular para desistimiento voluntario (RN-10); Mentor y Sistema para asistencia y quórum
DROP POLICY IF EXISTS rls_reservas_update ON reservas_cupo;
CREATE POLICY rls_reservas_update ON reservas_cupo
FOR UPDATE TO authenticated
USING (
    auth.jwt() ->> 'email' = estudiante_email OR
    EXISTS (
        SELECT 1 FROM sesiones_mentoria s
        WHERE s.id_sesion = reservas_cupo.id_sesion
          AND s.mentor_email = auth.jwt() ->> 'email'
    ) OR
    auth.jwt() ->> 'role' = 'administrador'
);

-- ------------------------------------------------------------------------------
-- 3. Políticas para 'solicitudes_demanda' (CUS03 / RF07)
-- ------------------------------------------------------------------------------

DROP POLICY IF EXISTS rls_demandas_select ON solicitudes_demanda;
CREATE POLICY rls_demandas_select ON solicitudes_demanda
FOR SELECT TO authenticated
USING (true);

DROP POLICY IF EXISTS rls_demandas_insert ON solicitudes_demanda;
CREATE POLICY rls_demandas_insert ON solicitudes_demanda
FOR INSERT TO authenticated
WITH CHECK (
    auth.jwt() ->> 'email' = estudiante_email
);

DROP POLICY IF EXISTS rls_demandas_update ON solicitudes_demanda;
CREATE POLICY rls_demandas_update ON solicitudes_demanda
FOR UPDATE TO authenticated
USING (
    auth.jwt() ->> 'email' = estudiante_email OR
    auth.jwt() ->> 'role' = 'administrador'
);
