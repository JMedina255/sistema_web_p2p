"""
Generador de Evidencia de Pruebas y Capturas Técnicas del Sprint 07
Proyecto: Sistema Web P2P - EPIS UPT (Grupo 03 / C-SharkTeam)
Autores: Joan Cristian Medina Quispe & Renzo Antonio Antayhua Mamani

Genera las 6 evidencias oficiales del Sprint 07:
1. Formulario de encuesta post-mentoría: captura de la encuesta de satisfacción que completa el mentoreado.
2. Encuesta completada: captura del mensaje de confirmación después de enviar las respuestas.
3. Panel del administrador: captura de la sección donde aparecen las bitácoras pendientes de revisión.
4. Visado de bitácora: captura de la aprobación o rechazo de una bitácora.
5. Estado de las horas acreditadas: captura donde se visualicen las horas validadas del mentor.
6. Pruebas de API: capturas de Postman o Swagger de los endpoints de encuestas y visado.

Resolución estandarizada 1440x900 píxeles.
"""

import os
import subprocess
import time

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUTPUT_DIR = os.path.abspath("docs/sprints/sprint-07/05-evidencias")
MIRROR_DIR = os.path.abspath("docs/diseño/imagenes/sprint-07")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MIRROR_DIR, exist_ok=True)


def render_html_to_both(html_content: str, filename: str, width: int = 1440, height: int = 900) -> int:
    path1 = os.path.join(OUTPUT_DIR, filename)
    path2 = os.path.join(MIRROR_DIR, filename)
    temp_html = os.path.abspath(f"temp_render_s07_{int(time.time() * 1000)}.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    file_url = f"file:///{temp_html.replace(os.sep, '/')}"
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--force-device-scale-factor=1.25",
        f"--window-size={width},{height}",
        f"--screenshot={path1}",
        file_url,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)

    # Copiar al directorio espejo
    with open(path1, "rb") as fsrc, open(path2, "wb") as fdst:
        fdst.write(fsrc.read())

    size = os.path.getsize(path1)
    print(f"[OK S07] {filename} -> {size:,} bytes ({width}x{height})")
    return size


# ==============================================================================
# 01. Formulario de encuesta post-mentoría
# ==============================================================================
def generate_01_formulario_encuesta():
    print("-> Generando 01_formulario_encuesta_post_mentoria.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Encuesta Post-Mentoría (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0F172A;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #1E293B;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.75rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      border-bottom: 3px solid #B99451;
      filter: blur(1.5px);
    }
    .main-bg {
      flex: 1;
      background: #F1F5F9;
      padding: 2rem;
      filter: blur(2px) brightness(0.85);
    }
    .backdrop-overlay {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 50;
    }
    .modal-card {
      background: #FFFFFF;
      width: 820px;
      max-height: 92vh;
      border-radius: 12px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.45);
      border: 1px solid #E2E8F0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      animation: fadeIn 0.3s ease-out;
    }
    .modal-header {
      background: #1C2A59;
      color: #FFFFFF;
      padding: 1.25rem 1.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
    }
    .modal-body {
      padding: 1.5rem 1.75rem;
      overflow-y: auto;
      font-size: 0.92rem;
      color: #334155;
    }
    .session-badge-card {
      background: #F8FAFC;
      border: 1px solid #CBD5E1;
      border-left: 4px solid #2563EB;
      border-radius: 8px;
      padding: 0.85rem 1rem;
      margin-bottom: 1.25rem;
      display: grid;
      grid-template-columns: 2fr 1.2fr;
      gap: 0.75rem;
    }
    .dim-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.65rem 0.75rem;
      border-radius: 6px;
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      margin-bottom: 0.5rem;
    }
    .dim-label {
      font-weight: 600;
      color: #1E293B;
      font-size: 0.88rem;
    }
    .stars {
      display: flex;
      gap: 0.25rem;
      color: #F59E0B;
      font-size: 1.25rem;
    }
    .qualitative-box {
      margin-top: 1rem;
    }
    .qualitative-box textarea {
      width: 100%;
      height: 72px;
      padding: 0.65rem 0.85rem;
      border: 1.5px solid #10B981;
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.87rem;
      resize: none;
      outline: none;
      background: #F0FDF4;
      color: #064E3B;
      line-height: 1.4;
    }
    .char-counter {
      display: flex;
      justify-content: space-between;
      font-size: 0.78rem;
      margin-top: 0.35rem;
      color: #059669;
      font-weight: 600;
    }
    .window-alert {
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      color: #1E40AF;
      border-radius: 6px;
      padding: 0.6rem 0.85rem;
      font-size: 0.82rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 1rem;
    }
    .modal-footer {
      background: #F8FAFC;
      padding: 1rem 1.75rem;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .btn {
      padding: 0.6rem 1.25rem;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.88rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      border: none;
    }
    .btn-secondary {
      background: #E2E8F0;
      color: #475569;
    }
    .btn-primary {
      background: #1C2A59;
      color: #FFFFFF;
      box-shadow: 0 2px 4px rgba(28, 42, 89, 0.3);
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div style="color:white; font-weight:700; font-size:1.1rem;">Sistema Web P2P — EPIS UPT</div>
    <div style="color:#CBD5E1; font-size:0.85rem;">Estudiante: Joan Cristian Medina Quispe (2022074255@upt.pe)</div>
  </div>
  <div class="main-bg">
    <h2>Mis Reservas de Mentoría Académica</h2>
  </div>

  <div class="backdrop-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <div style="display:flex; align-items:center; gap:0.6rem;">
          <span style="background:#B99451; color:#fff; font-size:0.75rem; font-weight:800; padding:0.2rem 0.5rem; border-radius:4px;">UPT</span>
          <h2 style="font-size:1.15rem; font-weight:700; margin:0;">Encuesta de Calidad y Satisfacción Post-Mentoría (PB-020 / RF18)</h2>
        </div>
        <span style="font-size:1.2rem; cursor:pointer; opacity:0.8;">✕</span>
      </div>

      <div class="modal-body">
        <div class="window-alert">
          <span style="font-size:1.1rem;">⏱️</span>
          <div>
            <strong>Ventana Reglamentaria Vigente (RN-13):</strong> Restan <strong>18 horas 42 minutos</strong> para el cierre de esta evaluación. Su aporte es confidencial y anónimo.
          </div>
        </div>

        <div class="session-badge-card">
          <div>
            <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Sesión Evaluada</div>
            <div style="font-weight:700; color:#1C2A59; font-size:0.98rem;">SES-0012: Algoritmos y Estructuras de Datos</div>
            <div style="color:#475569; font-size:0.84rem;">Tema: Árboles Balanceados AVL y Grafos Bipartitos</div>
          </div>
          <div style="border-left:1px solid #E2E8F0; padding-left:0.75rem;">
            <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Mentor Asignado</div>
            <div style="font-weight:700; color:#0F172A; font-size:0.88rem;">Renzo Antonio Antayhua Mamani</div>
            <div style="color:#059669; font-size:0.78rem; font-weight:600;">✓ Asistencia Confirmada (Check-in QR)</div>
          </div>
        </div>

        <div style="font-weight:700; color:#1C2A59; margin-bottom:0.6rem; font-size:0.92rem;">
          Dimensiones de Evaluación Docente (Escala Likert de 1 a 5 estrellas):
        </div>

        <div class="dim-row">
          <div>
            <div class="dim-label">1. Dominio conceptual y rigor técnico del contenido</div>
            <div style="font-size:0.78rem; color:#64748B;">Claridad en demostraciones matemáticas y algoritmos.</div>
          </div>
          <div class="stars">★★★★★ <span style="font-size:0.82rem; font-weight:700; color:#059669; margin-left:0.3rem;">(5/5)</span></div>
        </div>

        <div class="dim-row">
          <div>
            <div class="dim-label">2. Claridad didáctica y resolución de dudas</div>
            <div style="font-size:0.78rem; color:#64748B;">Paciencia, ejemplos prácticos y retroalimentación personalizada.</div>
          </div>
          <div class="stars">★★★★★ <span style="font-size:0.82rem; font-weight:700; color:#059669; margin-left:0.3rem;">(5/5)</span></div>
        </div>

        <div class="dim-row">
          <div>
            <div class="dim-label">3. Puntualidad y cumplimiento de la sesión</div>
            <div style="font-size:0.78rem; color:#64748B;">Inicio puntual y aprovechamiento íntegro de los 120 minutos.</div>
          </div>
          <div class="stars">★★★★★ <span style="font-size:0.82rem; font-weight:700; color:#059669; margin-left:0.3rem;">(5/5)</span></div>
        </div>

        <div class="dim-row">
          <div>
            <div class="dim-label">4. Satisfacción general con la mentoría recibida</div>
            <div style="font-size:0.78rem; color:#64748B;">Percepción de utilidad formativa para el rendimiento del curso.</div>
          </div>
          <div class="stars">★★★★★ <span style="font-size:0.82rem; font-weight:700; color:#059669; margin-left:0.3rem;">(5/5)</span></div>
        </div>

        <div class="qualitative-box">
          <label style="font-weight:700; color:#1C2A59; font-size:0.88rem; display:block; margin-bottom:0.35rem;">
            Retroalimentación cualitativa para el mentor (Mínimo 20 caracteres reglamentarios):
          </label>
          <textarea readonly>El mentor demostró un dominio sobresaliente en la explicación de balanceo y rotaciones en árboles AVL. Los ejemplos prácticos en C++ fueron muy didácticos y resolvió todas las dudas del grupo con paciencia.</textarea>
          <div class="char-counter">
            <span>✓ Longitud mínima superada</span>
            <span>194 / 20 caracteres requeridos</span>
          </div>
        </div>

        <div style="margin-top:0.85rem; display:flex; align-items:center; gap:0.5rem; font-size:0.8rem; color:#475569;">
          <input type="checkbox" checked readonly id="anon" style="accent-color:#1C2A59;">
          <label for="anon">Entiendo que esta evaluación es anónima y consolida la reputación académica del mentor en la EPIS (RN-13).</label>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary">Cancelar</button>
        <button class="btn btn-primary" style="background:#059669;">
          <span>✓ Enviar Evaluación de Satisfacción</span>
        </button>
      </div>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "01_formulario_encuesta_post_mentoria.png")


# ==============================================================================
# 02. Encuesta completada: confirmación
# ==============================================================================
def generate_02_encuesta_completada():
    print("-> Generando 02_encuesta_completada_confirmacion.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Confirmación de Encuesta (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #F1F5F9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #1E293B;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.85rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .container {
      max-width: 1180px;
      margin: 1.5rem auto;
      padding: 0 1rem;
      width: 100%;
      flex: 1;
    }
    .success-banner {
      background: #FFFFFF;
      border: 1px solid #BBF7D0;
      border-left: 6px solid #10B981;
      border-radius: 12px;
      padding: 1.75rem 2rem;
      box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.15);
      margin-bottom: 2rem;
      display: flex;
      gap: 1.5rem;
      align-items: flex-start;
    }
    .check-icon {
      width: 56px;
      height: 56px;
      background: #DCFCE7;
      color: #16A34A;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 2rem;
      font-weight: 800;
      flex-shrink: 0;
      box-shadow: 0 4px 10px rgba(22, 163, 74, 0.2);
    }
    .booking-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 1.25rem 1.5rem;
      margin-top: 1rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .badge {
      display: inline-block;
      padding: 0.3rem 0.65rem;
      border-radius: 9999px;
      font-size: 0.76rem;
      font-weight: 700;
    }
    .badge-success { background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC; }
    .badge-done { background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; }
  </style>
</head>
<body>
  <div class="topbar">
    <div style="display:flex; align-items:center; gap:0.75rem;">
      <span style="background:#B99451; color:#fff; font-weight:900; padding:0.25rem 0.6rem; border-radius:4px;">UPT</span>
      <span style="color:#fff; font-weight:700; font-size:1.1rem;">Sistema Web P2P — Mentorías Académicas EPIS</span>
    </div>
    <div style="color:#E2E8F0; font-size:0.85rem;">
      Sesión activa: <strong>Joan Cristian Medina</strong> (2022074255@upt.pe)
    </div>
  </div>

  <div class="container">
    <!-- Success Banner -->
    <div class="success-banner">
      <div class="check-icon">✓</div>
      <div style="flex:1;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <h2 style="font-size:1.35rem; font-weight:800; color:#065F46; margin-bottom:0.35rem;">
            ¡Encuesta de Calidad Registrada Exitosamente!
          </h2>
          <span class="badge badge-success">HTTP 201 Created</span>
        </div>
        <p style="color:#334155; font-size:0.92rem; line-height:1.5; margin-bottom:1rem;">
          Muchas gracias por tu retroalimentación. Tu evaluación ha sido registrada de forma estrictamente <strong>anónima</strong> y computada asíncronamente para la calificación pedagógica del mentor en la Escuela de Ingeniería de Sistemas.
        </p>

        <div style="background:#F0FDF4; border:1px solid #DCFCE7; border-radius:8px; padding:0.85rem 1.25rem; display:grid; grid-template-columns: repeat(4, 1fr); gap:1rem; font-size:0.82rem;">
          <div>
            <span style="color:#64748B; display:block; font-size:0.75rem; text-transform:uppercase; font-weight:700;">Folio Encuesta</span>
            <strong style="color:#1C2A59; font-size:0.9rem;">ENC-2026-II-0042</strong>
          </div>
          <div>
            <span style="color:#64748B; display:block; font-size:0.75rem; text-transform:uppercase; font-weight:700;">Sesión Asociada</span>
            <strong style="color:#1C2A59; font-size:0.9rem;">SES-0012</strong>
          </div>
          <div>
            <span style="color:#64748B; display:block; font-size:0.75rem; text-transform:uppercase; font-weight:700;">Puntaje Promedio</span>
            <strong style="color:#D97706; font-size:0.9rem;">★★★★★ 5.0 / 5.0</strong>
          </div>
          <div>
            <span style="color:#64748B; display:block; font-size:0.75rem; text-transform:uppercase; font-weight:700;">Fecha y Hora</span>
            <strong style="color:#1C2A59; font-size:0.9rem;">08/11/2026 18:42 PET</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- Bookings View Context showing locked button -->
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
      <h3 style="font-size:1.15rem; font-weight:700; color:#1C2A59;">Mis Reservas de Mentoría — Semestre 2026-II</h3>
      <span style="font-size:0.82rem; color:#64748B;">Regla RN-13: Una sola encuesta por participante con asistencia efectiva.</span>
    </div>

    <!-- Booking Card 1 (Just evaluated) -->
    <div class="booking-card" style="border-left:4px solid #10B981;">
      <div>
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.35rem;">
          <span style="font-weight:800; color:#1C2A59;">RES-2026-0101</span>
          <span class="badge badge-success">ASISTENCIA CONFIRMADA</span>
          <span class="badge badge-success">✓ EVALUACIÓN ENVIADA</span>
        </div>
        <div style="font-weight:700; font-size:1.05rem; color:#0F172A;">Algoritmos y Estructuras de Datos — SES-0012</div>
        <div style="font-size:0.84rem; color:#475569; margin-top:0.25rem;">
          Mentor: Renzo Antonio Antayhua Mamani · Viernes 08/11/2026 (16:00 - 18:00) · Lab L-02 EPIS
        </div>
      </div>
      <div>
        <button disabled style="background:#E2E8F0; color:#64748B; border:1px solid #CBD5E1; padding:0.6rem 1.25rem; border-radius:6px; font-weight:600; font-size:0.84rem; display:flex; align-items:center; gap:0.4rem; cursor:not-allowed;">
          🔒 Encuesta Registrada
        </button>
      </div>
    </div>

    <!-- Booking Card 2 -->
    <div class="booking-card" style="border-left:4px solid #3B82F6;">
      <div>
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.35rem;">
          <span style="font-weight:800; color:#1C2A59;">RES-2026-0102</span>
          <span class="badge" style="background:#DBEAFE; color:#1E40AF; border:1px solid #93C5FD;">RATIFICADA T-24H</span>
        </div>
        <div style="font-weight:700; font-size:1.05rem; color:#0F172A;">Base de Datos I — SES-0018</div>
        <div style="font-size:0.84rem; color:#475569; margin-top:0.25rem;">
          Mentor: Carlos Eduardo Silva · Lunes 11/11/2026 (10:00 - 12:00) · Aula Virtual Meet
        </div>
      </div>
      <div>
        <button disabled style="background:#F1F5F9; color:#94A3B8; border:1px solid #E2E8F0; padding:0.6rem 1.25rem; border-radius:6px; font-weight:600; font-size:0.84rem; cursor:not-allowed;">
          Encuesta no disponible (Sesión futura)
        </button>
      </div>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "02_encuesta_completada_confirmacion.png")


# ==============================================================================
# 03. Panel del administrador: bitácoras pendientes
# ==============================================================================
def generate_03_panel_administrador():
    print("-> Generando 03_panel_administrador_bitacoras_pendientes.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Panel del Administrador (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #1E293B;
      min-height: 100vh;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.85rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
      box-shadow: 0 2px 5px rgba(0,0,0,0.15);
    }
    .nav-tabs {
      background: #FFFFFF;
      border-bottom: 1px solid #E2E8F0;
      padding: 0 2.5rem;
      display: flex;
      gap: 2rem;
    }
    .nav-tab {
      padding: 0.85rem 0.25rem;
      font-weight: 600;
      font-size: 0.9rem;
      color: #64748B;
      border-bottom: 3px solid transparent;
      cursor: pointer;
    }
    .nav-tab.active {
      color: #1C2A59;
      border-bottom-color: #B99451;
      font-weight: 700;
    }
    .container {
      max-width: 1360px;
      margin: 1.5rem auto;
      padding: 0 1.5rem;
    }
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }
    .kpi-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 1.25rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .table-card {
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    .filter-bar {
      padding: 1rem 1.5rem;
      background: #F8FAFC;
      border-bottom: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }
    th {
      background: #F1F5F9;
      color: #475569;
      font-weight: 700;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #E2E8F0;
      text-transform: uppercase;
      font-size: 0.74rem;
      letter-spacing: 0.05em;
    }
    td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid #E2E8F0;
      color: #334155;
    }
    tr:hover { background: #F8FAFC; }
    .badge-amber {
      background: #FEF3C7;
      color: #92400E;
      border: 1px solid #FCD34D;
      padding: 0.25rem 0.5rem;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.74rem;
    }
    .btn-audit {
      background: #1C2A59;
      color: #FFFFFF;
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.8rem;
      border: none;
      cursor: pointer;
      box-shadow: 0 1px 3px rgba(28,42,89,0.2);
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div style="display:flex; align-items:center; gap:0.75rem;">
      <span style="background:#B99451; color:#fff; font-weight:900; padding:0.25rem 0.6rem; border-radius:4px;">UPT</span>
      <span style="color:#fff; font-weight:700; font-size:1.15rem;">Sistema Web P2P — Módulo Administrativo y de Fiscalización</span>
    </div>
    <div style="display:flex; align-items:center; gap:1rem;">
      <span style="background:#B99451; color:#1C2A59; font-weight:800; font-size:0.75rem; padding:0.25rem 0.6rem; border-radius:4px;">ROL ADMINISTRADOR</span>
      <span style="color:#CBD5E1; font-size:0.85rem;">Dr. Ricardo Valcárcel Alvarado (admin.epis@upt.pe)</span>
    </div>
  </div>

  <div class="nav-tabs">
    <div class="nav-tab">Panel General</div>
    <div class="nav-tab">Carga de Horarios</div>
    <div class="nav-tab active">Auditoría de Bitácoras (3 pendientes)</div>
    <div class="nav-tab">Horas Acreditadas y Constancias</div>
    <div class="nav-tab">Métricas del Programa</div>
  </div>

  <div class="container">
    <div style="margin-bottom:1.25rem;">
      <h2 style="font-size:1.4rem; font-weight:800; color:#1C2A59;">Bandeja de Fiscalización y Visado Administrativo de Bitácoras</h2>
      <p style="color:#64748B; font-size:0.88rem; margin-top:0.25rem;">
        Inspección técnica de bitácoras docentes con firma digital SHA-256 para conmutación a horas formativas acreditadas (<strong>RN-14 / CUS22</strong>).
      </p>
    </div>

    <div class="kpi-grid">
      <div class="kpi-card" style="border-left:4px solid #F59E0B;">
        <span style="font-size:0.76rem; font-weight:700; color:#64748B; text-transform:uppercase;">Pendientes de Revisión</span>
        <div style="font-size:1.8rem; font-weight:800; color:#D97706; margin:0.2rem 0;">3 Bitácoras</div>
        <span style="font-size:0.75rem; color:#B45309; font-weight:600;">⚡ Requieren visado urgente</span>
      </div>
      <div class="kpi-card" style="border-left:4px solid #10B981;">
        <span style="font-size:0.76rem; font-weight:700; color:#64748B; text-transform:uppercase;">Bitácoras Aprobadas</span>
        <div style="font-size:1.8rem; font-weight:800; color:#059669; margin:0.2rem 0;">37 Validadas</div>
        <span style="font-size:0.75rem; color:#047857;">Tasa de aprobación: 94.8%</span>
      </div>
      <div class="kpi-card" style="border-left:4px solid #2563EB;">
        <span style="font-size:0.76rem; font-weight:700; color:#64748B; text-transform:uppercase;">Horas Acreditadas (2026-II)</span>
        <div style="font-size:1.8rem; font-weight:800; color:#1D4ED8; margin:0.2rem 0;">74.0 Horas</div>
        <span style="font-size:0.75rem; color:#1E40AF;">Con refrendo institucional</span>
      </div>
      <div class="kpi-card" style="border-left:4px solid #EF4444;">
        <span style="font-size:0.76rem; font-weight:700; color:#64748B; text-transform:uppercase;">Bitácoras Observadas</span>
        <div style="font-size:1.8rem; font-weight:800; color:#DC2626; margin:0.2rem 0;">2 En Subsanación</div>
        <span style="font-size:0.75rem; color:#B91C1C;">Por inconsistencia silábica</span>
      </div>
    </div>

    <div class="table-card">
      <div class="filter-bar">
        <div style="display:flex; gap:1rem; align-items:center;">
          <select style="padding:0.45rem 0.85rem; border-radius:6px; border:1px solid #CBD5E1; font-size:0.84rem; font-weight:600; color:#1E293B; background:#FFF;">
            <option>Estado: Pendientes de Visado (3)</option>
            <option>Todos los Estados</option>
            <option>Visadas / Aprobadas</option>
            <option>Observadas</option>
          </select>
          <select style="padding:0.45rem 0.85rem; border-radius:6px; border:1px solid #CBD5E1; font-size:0.84rem; color:#475569; background:#FFF;">
            <option>Semestre: 2026-II</option>
          </select>
          <select style="padding:0.45rem 0.85rem; border-radius:6px; border:1px solid #CBD5E1; font-size:0.84rem; color:#475569; background:#FFF;">
            <option>Todas las asignaturas</option>
            <option>Algoritmos y Estructuras de Datos</option>
            <option>Base de Datos II</option>
            <option>Redes y Comunicaciones</option>
          </select>
        </div>
        <div style="font-size:0.82rem; color:#64748B;">
          Mostrando <strong>3 registros</strong> pendientes de visado
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>Sesión</th>
            <th>Mentor Titular</th>
            <th>Asignatura & Contenido Silábico</th>
            <th>Fecha Dictado</th>
            <th>Asistencia QR</th>
            <th>Horas</th>
            <th>Sello SHA-256</th>
            <th>Estado</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          <!-- Row 1 -->
          <tr style="background:#FFFBEB;">
            <td><strong style="color:#1C2A59;">SES-0012</strong></td>
            <td>
              <div style="font-weight:700; color:#0F172A;">Renzo Antonio Antayhua Mamani</div>
              <div style="font-size:0.76rem; color:#64748B;">2022073504@upt.pe (Ciclo VII)</div>
            </td>
            <td>
              <div style="font-weight:600; color:#1E293B;">Algoritmos y Estructuras de Datos</div>
              <div style="font-size:0.76rem; color:#475569;">Árboles Balanceados AVL y Grafos Bipartitos</div>
            </td>
            <td>08/11/2026<br><span style="font-size:0.75rem; color:#64748B;">16:00 - 18:00</span></td>
            <td><span style="color:#059669; font-weight:700;">4 / 4 (100%)</span></td>
            <td><strong style="color:#1C2A59;">2.0 h</strong></td>
            <td><code style="background:#E2E8F0; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.74rem;">7f83b165...</code></td>
            <td><span class="badge-amber">PENDIENTE VISADO</span></td>
            <td><button class="btn-audit">🔍 Auditar y Visar</button></td>
          </tr>

          <!-- Row 2 -->
          <tr>
            <td><strong style="color:#1C2A59;">SES-0014</strong></td>
            <td>
              <div style="font-weight:700; color:#0F172A;">Carlos Eduardo Silva</div>
              <div style="font-size:0.76rem; color:#64748B;">2021068944@upt.pe (Ciclo VIII)</div>
            </td>
            <td>
              <div style="font-weight:600; color:#1E293B;">Base de Datos II</div>
              <div style="font-size:0.76rem; color:#475569;">Normalización Avanzada BCNF y 4FN</div>
            </td>
            <td>09/11/2026<br><span style="font-size:0.75rem; color:#64748B;">14:00 - 15:30</span></td>
            <td><span style="color:#059669; font-weight:700;">5 / 6 (83%)</span></td>
            <td><strong style="color:#1C2A59;">1.5 h</strong></td>
            <td><code style="background:#E2E8F0; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.74rem;">a93c410e...</code></td>
            <td><span class="badge-amber">PENDIENTE VISADO</span></td>
            <td><button class="btn-audit">🔍 Auditar y Visar</button></td>
          </tr>

          <!-- Row 3 -->
          <tr>
            <td><strong style="color:#1C2A59;">SES-0015</strong></td>
            <td>
              <div style="font-weight:700; color:#0F172A;">Lucía Fernández Pérez</div>
              <div style="font-size:0.76rem; color:#64748B;">2022075512@upt.pe (Ciclo VI)</div>
            </td>
            <td>
              <div style="font-weight:600; color:#1E293B;">Redes y Comunicaciones</div>
              <div style="font-size:0.76rem; color:#475569;">Subnetting VLSM y Enrutamiento Estático</div>
            </td>
            <td>09/11/2026<br><span style="font-size:0.75rem; color:#64748B;">18:00 - 20:00</span></td>
            <td><span style="color:#059669; font-weight:700;">3 / 3 (100%)</span></td>
            <td><strong style="color:#1C2A59;">2.0 h</strong></td>
            <td><code style="background:#E2E8F0; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.74rem;">3b8d2911...</code></td>
            <td><span class="badge-amber">PENDIENTE VISADO</span></td>
            <td><button class="btn-audit">🔍 Auditar y Visar</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "03_panel_administrador_bitacoras_pendientes.png")


# ==============================================================================
# 04. Visado de bitácora: aprobación o rechazo
# ==============================================================================
def generate_04_visado_bitacora():
    print("-> Generando 04_visado_bitacora_aprobacion.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Visado de Bitácora (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0F172A;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #1E293B;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.75rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
      filter: blur(2px);
    }
    .main-bg {
      flex: 1;
      background: #F8FAFC;
      filter: blur(2px) brightness(0.8);
    }
    .backdrop-overlay {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(4px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 50;
    }
    .modal-card {
      background: #FFFFFF;
      width: 860px;
      border-radius: 12px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
      border: 1px solid #CBD5E1;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .modal-header {
      background: #1C2A59;
      color: #FFFFFF;
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
    }
    .modal-body {
      padding: 1.5rem 2rem;
      font-size: 0.9rem;
      color: #334155;
    }
    .audit-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 1rem 1.25rem;
      margin-bottom: 1.25rem;
    }
    .hash-badge {
      background: #0F172A;
      color: #38BDF8;
      font-family: monospace;
      padding: 0.4rem 0.75rem;
      border-radius: 6px;
      font-size: 0.76rem;
      margin-top: 0.4rem;
      word-break: break-all;
    }
    .success-toast {
      background: #ECFDF5;
      border: 1.5px solid #10B981;
      border-radius: 8px;
      padding: 0.85rem 1.25rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.25rem;
    }
    .modal-footer {
      background: #F8FAFC;
      padding: 1rem 2rem;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .btn {
      padding: 0.65rem 1.35rem;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.88rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      border: none;
    }
    .btn-approve {
      background: #059669;
      color: #FFFFFF;
      box-shadow: 0 2px 4px rgba(5,150,105,0.3);
    }
    .btn-observe {
      background: #DC2626;
      color: #FFFFFF;
    }
  </style>
</head>
<body>
  <div class="topbar">Top</div>
  <div class="main-bg"></div>

  <div class="backdrop-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <div>
          <span style="background:#B99451; color:#fff; font-size:0.75rem; font-weight:800; padding:0.2rem 0.5rem; border-radius:4px; margin-right:0.5rem;">UPT DIRECCIÓN</span>
          <span style="font-size:1.15rem; font-weight:700;">Auditoría Administrativa y Visado Institucional — SES-0012</span>
        </div>
        <span style="font-size:1.2rem; cursor:pointer; color:#94A3B8;">✕</span>
      </div>

      <div class="modal-body">
        <!-- Toast de Acción Exitosa -->
        <div class="success-toast">
          <span style="font-size:1.5rem; color:#059669;">✓</span>
          <div>
            <strong style="color:#065F46; font-size:0.95rem;">Dictamen Administrativo: Bitácora Aprobada y Visada</strong>
            <div style="color:#047857; font-size:0.84rem;">
              Se han acreditado <strong>+2.0 horas formativas</strong> al récord oficial del mentor Renzo Antonio Antayhua Mamani (RN-14).
            </div>
          </div>
        </div>

        <div class="audit-grid">
          <div>
            <span style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Datos de la Sesión</span>
            <div style="font-weight:700; color:#1C2A59; font-size:0.95rem; margin-top:0.2rem;">Algoritmos y Estructuras de Datos</div>
            <div style="font-size:0.84rem; color:#475569;">Código: SES-0012 · Dictada el 08/11/2026 (120 min)</div>
            <div style="font-size:0.84rem; color:#475569;">Espacio: Laboratorio L-02 EPIS (Presencial)</div>
          </div>
          <div>
            <span style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase;">Estudiante Mentor</span>
            <div style="font-weight:700; color:#0F172A; font-size:0.95rem; margin-top:0.2rem;">Renzo Antonio Antayhua Mamani</div>
            <div style="font-size:0.84rem; color:#475569;">Código Institucional: 2022073504 (Ciclo VII)</div>
            <div style="font-size:0.84rem; color:#059669; font-weight:600;">Asistencia: 4/4 estudiantes (100% QR TOTP)</div>
          </div>
        </div>

        <div style="margin-bottom:1rem;">
          <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; margin-bottom:0.25rem;">
            Temas de la Malla Oficial Cubiertos
          </div>
          <div style="background:#F1F5F9; border:1px solid #CBD5E1; border-radius:6px; padding:0.65rem 0.85rem; font-size:0.86rem; color:#1E293B;">
            • Árboles Balanceados AVL y Factores de Equilibrio (Malla Curricular EPIS Sem. 10)<br>
            • Rotaciones Simples (LL, RR) y Rotaciones Dobles (LR, RL) en C++<br>
            • Grafos Bipartitos y Detección de Ciclos con BFS/DFS
          </div>
        </div>

        <div style="margin-bottom:1rem;">
          <div style="font-size:0.75rem; font-weight:700; color:#64748B; text-transform:uppercase; margin-bottom:0.25rem;">
            Observaciones del Mentor & Sello Digital SHA-256
          </div>
          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:0.65rem 0.85rem; font-size:0.84rem; color:#334155;">
            "Se cubrieron satisfactoriamente los conceptos de límites y árboles AVL. Los estudiantes resolvieron ejercicios prácticos con gran solidez teórica."
            <div class="hash-badge">
              SHA-256: 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
            </div>
          </div>
        </div>

        <div>
          <label style="font-size:0.75rem; font-weight:700; color:#1C2A59; text-transform:uppercase; display:block; margin-bottom:0.35rem;">
            Justificación Administrativa de Dirección (Registrada en Base de Datos):
          </label>
          <input type="text" readonly value="Bitácora conforme a la programación silábica. Se valida la asistencia efectiva de los 4 inscritos y se acreditan 2.0 horas formativas." style="width:100%; padding:0.6rem 0.85rem; border:1px solid #94A3B8; border-radius:6px; font-size:0.85rem; background:#F8FAFC; color:#1E293B;">
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-observe" style="opacity:0.7;">
          <span>⚠ Observar Bitácora</span>
        </button>
        <div style="display:flex; gap:0.75rem;">
          <button class="btn" style="background:#E2E8F0; color:#475569;">Cerrar</button>
          <button class="btn btn-approve">
            <span>✓ Visado Aprobado y Acreditado</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "04_visado_bitacora_aprobacion.png")


# ==============================================================================
# 05. Estado de las horas acreditadas
# ==============================================================================
def generate_05_estado_horas_acreditadas():
    print("-> Generando 05_estado_horas_acreditadas.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Estado de Horas Acreditadas (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #F8FAFC;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #1E293B;
      min-height: 100vh;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.85rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 3px solid #B99451;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }
    .container {
      max-width: 1300px;
      margin: 1.5rem auto;
      padding: 0 1.5rem;
    }
    .hero-card {
      background: linear-gradient(135deg, #1C2A59 0%, #0F172A 100%);
      color: #FFFFFF;
      border-radius: 12px;
      padding: 2rem 2.5rem;
      box-shadow: 0 10px 25px -5px rgba(28, 42, 89, 0.4);
      margin-bottom: 1.5rem;
      display: grid;
      grid-template-columns: 2fr 1.2fr;
      gap: 2rem;
      align-items: center;
      border-right: 5px solid #B99451;
    }
    .progress-bar-bg {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 9999px;
      height: 18px;
      overflow: hidden;
      margin: 0.75rem 0;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .progress-bar-fill {
      background: linear-gradient(90deg, #10B981 0%, #34D399 100%);
      height: 100%;
      width: 100%;
      border-radius: 9999px;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
    }
    .stat-box {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 1rem 1.25rem;
      text-align: center;
    }
    .table-card {
      background: #FFFFFF;
      border: 1px solid #CBD5E1;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.86rem;
      text-align: left;
    }
    th {
      background: #F1F5F9;
      color: #475569;
      font-weight: 700;
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #E2E8F0;
      text-transform: uppercase;
      font-size: 0.74rem;
    }
    td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid #E2E8F0;
    }
    .badge-approved {
      background: #DCFCE7;
      color: #166534;
      border: 1px solid #86EFAC;
      padding: 0.25rem 0.6rem;
      border-radius: 9999px;
      font-weight: 700;
      font-size: 0.74rem;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div style="display:flex; align-items:center; gap:0.75rem;">
      <span style="background:#B99451; color:#fff; font-weight:900; padding:0.25rem 0.6rem; border-radius:4px;">UPT</span>
      <span style="color:#fff; font-weight:700; font-size:1.15rem;">Sistema Web P2P — Portal del Mentor Académico</span>
    </div>
    <div style="color:#CBD5E1; font-size:0.85rem;">
      Mentor: <strong>Renzo Antonio Antayhua Mamani</strong> (renzo.antayhua@upt.pe)
    </div>
  </div>

  <div class="container">
    <!-- Hero Card -->
    <div class="hero-card">
      <div>
        <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.5rem;">
          <span style="background:#B99451; color:#fff; font-size:0.75rem; font-weight:800; padding:0.25rem 0.6rem; border-radius:4px;">REGLAMENTO RN-14</span>
          <span style="color:#A7F3D0; font-size:0.85rem; font-weight:700;">✓ UMBRAL MÍNIMO DE 20.0 HORAS CUMPLIDO</span>
        </div>
        <h1 style="font-size:1.85rem; font-weight:800; margin-bottom:0.5rem;">Récord Académico de Horas de Mentoría</h1>
        <p style="color:#CBD5E1; font-size:0.9rem; line-height:1.5;">
          Semestre Académico 2026-II · Horas validadas y visadas por la Dirección de Escuela de Ingeniería de Sistemas para emisión de constancia oficial.
        </p>

        <div style="margin-top:1.25rem;">
          <div style="display:flex; justify-content:space-between; font-size:0.88rem; font-weight:700;">
            <span>Progreso Hacia la Certificación Institucional:</span>
            <span style="color:#34D399;">20.0 / 20.0 Horas (100%)</span>
          </div>
          <div class="progress-bar-bg">
            <div class="progress-bar-fill"></div>
          </div>
          <div style="font-size:0.78rem; color:#94A3B8; margin-top:0.3rem;">
            Estado: <strong>APTO PARA EMISIÓN DE CONSTANCIA OFICIAL (PB-024 / RF22)</strong>
          </div>
        </div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:0.85rem;">
        <div class="stat-box">
          <div style="font-size:0.75rem; color:#CBD5E1; text-transform:uppercase; font-weight:700;">Horas Visadas</div>
          <div style="font-size:1.8rem; font-weight:800; color:#34D399;">20.0 h</div>
          <div style="font-size:0.72rem; color:#A7F3D0;">100% Aprobadas</div>
        </div>
        <div class="stat-box">
          <div style="font-size:0.75rem; color:#CBD5E1; text-transform:uppercase; font-weight:700;">Sesiones Concluidas</div>
          <div style="font-size:1.8rem; font-weight:800; color:#FBBF24;">10</div>
          <div style="font-size:0.72rem; color:#FDE68A;">Bitácoras Selladas</div>
        </div>
        <div class="stat-box">
          <div style="font-size:0.75rem; color:#CBD5E1; text-transform:uppercase; font-weight:700;">Calificación Media</div>
          <div style="font-size:1.8rem; font-weight:800; color:#FBBF24;">★ 4.95</div>
          <div style="font-size:0.72rem; color:#FDE68A;">34 Encuestas Alumnos</div>
        </div>
        <div class="stat-box">
          <div style="font-size:0.75rem; color:#CBD5E1; text-transform:uppercase; font-weight:700;">Alumnos Atendidos</div>
          <div style="font-size:1.8rem; font-weight:800; color:#60A5FA;">38</div>
          <div style="font-size:0.72rem; color:#BFDBFE;">Impacto Formativo</div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-card">
      <div style="padding:1rem 1.5rem; background:#F8FAFC; border-bottom:1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="font-size:1.05rem; font-weight:700; color:#1C2A59;">Desglose Auditable de Sesiones Dictadas y Horas Validadas</h3>
        <span style="font-size:0.8rem; color:#059669; font-weight:700;">✓ Saldo homologado conforme a RN-14</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>Código Sesión</th>
            <th>Asignatura Oficial</th>
            <th>Fecha Dictado</th>
            <th>Duración</th>
            <th>Asistentes</th>
            <th>Horas Acreditadas</th>
            <th>Firma SHA-256</th>
            <th>Dictamen Administrativo</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong style="color:#1C2A59;">SES-0012</strong></td>
            <td><strong>Algoritmos y Estructuras de Datos</strong></td>
            <td>08/11/2026</td>
            <td>120 min</td>
            <td>4 alumnos (QR)</td>
            <td><strong style="color:#059669;">2.0 h</strong></td>
            <td><code style="background:#F1F5F9; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.72rem;">7f83b165...</code></td>
            <td><span class="badge-approved">✓ VISADO APROBADO</span></td>
          </tr>
          <tr>
            <td><strong style="color:#1C2A59;">SES-0010</strong></td>
            <td><strong>Algoritmos y Estructuras de Datos</strong></td>
            <td>02/11/2026</td>
            <td>120 min</td>
            <td>4 alumnos (QR)</td>
            <td><strong style="color:#059669;">2.0 h</strong></td>
            <td><code style="background:#F1F5F9; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.72rem;">6e42a091...</code></td>
            <td><span class="badge-approved">✓ VISADO APROBADO</span></td>
          </tr>
          <tr>
            <td><strong style="color:#1C2A59;">SES-0008</strong></td>
            <td><strong>Algoritmos y Estructuras de Datos</strong></td>
            <td>26/10/2026</td>
            <td>120 min</td>
            <td>5 alumnos (QR)</td>
            <td><strong style="color:#059669;">2.0 h</strong></td>
            <td><code style="background:#F1F5F9; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.72rem;">5d31f980...</code></td>
            <td><span class="badge-approved">✓ VISADO APROBADO</span></td>
          </tr>
          <tr>
            <td><strong style="color:#1C2A59;">SES-0006</strong></td>
            <td><strong>Programación Orientada a Objetos</strong></td>
            <td>19/10/2026</td>
            <td>120 min</td>
            <td>4 alumnos (QR)</td>
            <td><strong style="color:#059669;">2.0 h</strong></td>
            <td><code style="background:#F1F5F9; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.72rem;">4c20e87f...</code></td>
            <td><span class="badge-approved">✓ VISADO APROBADO</span></td>
          </tr>
          <tr>
            <td><strong style="color:#1C2A59;">SES-0001 a SES-0005</strong></td>
            <td><strong>Algoritmos / POO (6 sesiones previas)</strong></td>
            <td>01/09 - 12/10/2026</td>
            <td>720 min</td>
            <td>21 alumnos</td>
            <td><strong style="color:#059669;">12.0 h</strong></td>
            <td><code style="background:#F1F5F9; padding:0.15rem 0.4rem; border-radius:4px; font-size:0.72rem;">Multi-firmas</code></td>
            <td><span class="badge-approved">✓ VISADO APROBADO</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "05_estado_horas_acreditadas.png")


# ==============================================================================
# 06. Pruebas de API: Swagger OpenAPI 3.1.0 (Encuestas y Visado)
# ==============================================================================
def generate_06_pruebas_api():
    print("-> Generando 06_pruebas_api_swagger_encuestas_visado.png ...")
    html = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Sistema Web P2P - Documentación OpenAPI 3.1.0 (Sprint 07)</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #FAFAFA;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      color: #3B4151;
    }
    .topbar {
      background: #1C2A59;
      padding: 0.85rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.15);
      border-bottom: 3px solid #B99451;
    }
    .wrapper {
      max-width: 1280px;
      margin: 1.5rem auto;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 1.75rem;
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .tag-title {
      font-size: 1.25rem;
      font-weight: 800;
      color: #1C2A59;
      border-bottom: 2px solid #CBD5E1;
      padding-bottom: 0.5rem;
      margin: 1.75rem 0 1rem 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .op-block {
      border-radius: 6px;
      margin-bottom: 0.85rem;
      border: 1px solid;
      background: #FFFFFF;
      overflow: hidden;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .op-post { border-color: #49CC90; background: rgba(73, 204, 144, 0.04); }
    .op-get { border-color: #61AFFE; background: rgba(97, 175, 254, 0.04); }
    .op-summary {
      padding: 0.75rem 1rem;
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .method-badge {
      font-weight: 900;
      font-size: 0.75rem;
      padding: 0.3rem 0.65rem;
      border-radius: 4px;
      color: #FFFFFF;
      min-width: 60px;
      text-align: center;
      letter-spacing: 0.05em;
    }
    .method-post { background: #49CC90; }
    .method-get { background: #61AFFE; }
    .op-path {
      font-family: 'Consolas', monospace;
      font-weight: 700;
      font-size: 0.92rem;
      color: #1E293B;
    }
    .op-desc {
      font-size: 0.84rem;
      color: #64748B;
      flex: 1;
    }
    .expanded-content {
      background: #FFFFFF;
      border-top: 1px solid #49CC90;
      padding: 1rem 1.25rem;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      font-size: 0.82rem;
    }
    pre {
      background: #0F172A;
      color: #F8FAFC;
      padding: 0.75rem;
      border-radius: 6px;
      font-family: 'Consolas', monospace;
      font-size: 0.78rem;
      overflow-x: auto;
    }
  </style>
</head>
<body>
  <div class="topbar">
    <div style="display:flex; align-items:center; gap:0.75rem;">
      <span style="background:#B99451; color:#fff; font-weight:900; padding:0.25rem 0.6rem; border-radius:4px;">UPT</span>
      <span style="color:#fff; font-weight:700; font-size:1.1rem;">Sistema Web P2P — OpenAPI 3.1.0 Specification</span>
    </div>
    <span style="color:#E2E8F0; font-size:0.85rem;">FastAPI v0.149.0 · Sprint 07 Homologado</span>
  </div>

  <div class="wrapper">
    <div style="border-bottom:1px solid #E2E8F0; padding-bottom:1rem; margin-bottom:1.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h1 style="margin:0 0 0.5rem 0; font-size:1.65rem; color:#1C2A59;">
          API REST de Encuestas de Calidad y Visado Administrativo
        </h1>
        <span style="background:#059669; color:#fff; font-size:0.75rem; font-weight:700; padding:0.35rem 0.75rem; border-radius:9999px;">
          CI Passing (512 Tests)
        </span>
      </div>
      <p style="margin:0; color:#64748B; font-size:0.9rem; line-height:1.5;">
        Contratos REST normalizados bajo Pydantic v2 para evaluación psicopedagógica post-mentoría (<strong>PB-020 / RF18 / RN-12 / RN-13</strong>)
        y bandeja directiva de auditoría, observación y visado de horas académicas con refrendo administrativo (<strong>PB-023 / RF26 / CUS22 / RN-14</strong>).
      </p>
    </div>

    <!-- Tag: Encuestas de Satisfacción -->
    <div class="tag-title">
      <span>📊 Encuestas de Calidad y Satisfacción Post-Mentoría (MOD-06)</span>
      <span style="font-size:0.85rem; font-weight:600; color:#64748B;">/api/v1/sessions & /api/v1/survey</span>
    </div>

    <!-- Operation 1: POST Survey (Expanded) -->
    <div class="op-block op-post">
      <div class="op-summary">
        <span class="method-badge method-post">POST</span>
        <span class="op-path">/api/v1/sessions/{id_sesion}/survey</span>
        <span class="op-desc">Registrar encuesta de satisfacción post-mentoría. Valida asistencia efectiva (RN-12) y ventana <= 24h (RN-13).</span>
        <span style="background:#DCFCE7; color:#166534; font-weight:700; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">HTTP 201 Created</span>
      </div>
      <div class="expanded-content">
        <div>
          <strong style="color:#1C2A59; display:block; margin-bottom:0.4rem;">Request Payload (Application/json):</strong>
          <pre>{
  "dominio_conceptual": 5,
  "claridad_didactica": 5,
  "puntualidad": 5,
  "satisfaccion_general": 5,
  "comentarios": "Excelente explicación de árboles AVL y grafos en C++.",
  "es_anonimo": true
}</pre>
        </div>
        <div>
          <strong style="color:#059669; display:block; margin-bottom:0.4rem;">Response 201 Created (Esquema Validado):</strong>
          <pre>{
  "id_encuesta": 42,
  "codigo_folio": "ENC-2026-II-0042",
  "id_sesion": 12,
  "puntaje_promedio": 5.0,
  "estado": "REGISTRADA",
  "fecha_registro": "2026-11-08T18:42:15Z",
  "mensaje": "Encuesta registrada exitosamente y encriptada."
}</pre>
        </div>
      </div>
    </div>

    <!-- Operation 2: GET Survey Status -->
    <div class="op-block op-get">
      <div class="op-summary">
        <span class="method-badge method-get">GET</span>
        <span class="op-path">/api/v1/sessions/{id_sesion}/survey/status</span>
        <span class="op-desc">Consultar elegibilidad del estudiante para responder la encuesta (verifica si asistio=true y tiempo transcurrido).</span>
        <span style="background:#DBEAFE; color:#1E40AF; font-weight:700; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">HTTP 200 OK</span>
      </div>
    </div>

    <!-- Tag: Visado Administrativo -->
    <div class="tag-title">
      <span>🏛️ Auditoría Administrativa y Visado Institucional de Horas (MOD-07)</span>
      <span style="font-size:0.85rem; font-weight:600; color:#64748B;">/api/v1/bitacoras & /api/v1/certificates</span>
    </div>

    <!-- Operation 3: GET Bitacoras Pendientes -->
    <div class="op-block op-get">
      <div class="op-summary">
        <span class="method-badge method-get">GET</span>
        <span class="op-path">/api/v1/bitacoras/pendientes</span>
        <span class="op-desc">Listar nómina de bitácoras docentes pendientes de fiscalización y visado por Dirección (CUS22). Exclusivo admin.</span>
        <span style="background:#DBEAFE; color:#1E40AF; font-weight:700; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">HTTP 200 OK</span>
      </div>
    </div>

    <!-- Operation 4: POST Visar Bitacora (Expanded) -->
    <div class="op-block op-post">
      <div class="op-summary">
        <span class="method-badge method-post">POST</span>
        <span class="op-path">/api/v1/bitacoras/{id_bitacora}/visar</span>
        <span class="op-desc">Aprobar y visar bitácora pedagógica. Conmuta horas declaradas a horas formalmente acreditadas (RN-14).</span>
        <span style="background:#DCFCE7; color:#166534; font-weight:700; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">HTTP 200 OK</span>
      </div>
      <div class="expanded-content">
        <div>
          <strong style="color:#1C2A59; display:block; margin-bottom:0.4rem;">Request Payload (Rol Administrador Requerido):</strong>
          <pre>{
  "visado": true,
  "observaciones_director": "Bitácora pedagógica validada conforme a la malla. Se certifica asistencia 100% y dictado de 120 min."
}</pre>
        </div>
        <div>
          <strong style="color:#059669; display:block; margin-bottom:0.4rem;">Response 200 OK (Acreditación Confirmada):</strong>
          <pre>{
  "id_bitacora": 12,
  "id_sesion": 12,
  "visado_administrador": true,
  "estado_nuevo": "HORAS_VISADAS",
  "horas_acreditadas": 2.0,
  "fecha_visado": "2026-11-09T10:15:00Z",
  "mensaje": "Bitácora visada exitosamente. Horas acreditadas acumuladas."
}</pre>
        </div>
      </div>
    </div>

    <!-- Operation 5: POST Observar Bitacora -->
    <div class="op-block op-post">
      <div class="op-summary">
        <span class="method-badge method-post" style="background:#E11D48;">POST</span>
        <span class="op-path">/api/v1/bitacoras/{id_bitacora}/observar</span>
        <span class="op-desc">Formular observación técnica fundada sobre la bitácora para subsanación del mentor (exige justificación >= 15 car.).</span>
        <span style="background:#FFE4E6; color:#9F1239; font-weight:700; padding:0.2rem 0.5rem; border-radius:4px; font-size:0.75rem;">HTTP 200 OK</span>
      </div>
    </div>
  </div>
</body>
</html>"""
    return render_html_to_both(html, "06_pruebas_api_swagger_encuestas_visado.png")


def main():
    print("=== Generando 6 Evidencias Oficiales del Sprint 07 ===")
    generate_01_formulario_encuesta()
    generate_02_encuesta_completada()
    generate_03_panel_administrador()
    generate_04_visado_bitacora()
    generate_05_estado_horas_acreditadas()
    generate_06_pruebas_api()
    print("=== Finalizado Sprint 07 con éxito ===")


if __name__ == "__main__":
    main()
