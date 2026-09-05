# Sistema Web P2P de Mentorías Académicas — EPIS UPT (2026)

> **Proyecto:** Sistema Web P2P con algoritmo de recomendación para la personalización de mentorías académicas en la EPIS-UPT  
> **Curso:** Construcción de Software I  
> **Institución:** Universidad Privada de Tacna — Facultad de Ingeniería — Escuela Profesional de Ingeniería de Sistemas  
> **Autores:**  
> - ANTAYHUA MAMANI, Renzo Antonio (2022073504)  
> - MEDINA QUISPE, Joan Cristian (2022074255)  
> **Docente:** Dr. Ricardo Eduardo Valcárcel Alvarado  

---

## 📌 Descripción General

El **Sistema Web P2P** es una plataforma orientada a conectar a estudiantes de ciclos formativos (I al IV ciclo) con estudiantes de ciclos superiores (VII al X ciclo) para el refuerzo adaptativo en asignaturas filtro críticas (*Cálculo I/II, Algoritmos y Estructuras de Datos, Programación Orientada a Objetos y Base de Datos*).

El sistema incorpora:
1. **Catálogo de Clases y Mentorías en Vivo:** Con cuadro de búsqueda reactivo por escritura para encontrar mentorías por tema, asignatura, mentor o modalidad.
2. **Motor de Recomendación Top-k:** Emparejamiento adaptativo por afinidad temática y valoraciones históricas.
3. **Agendamiento P2P:** Coordinación y confirmación de franjas horarias libres.
4. **Gamificación y Convalidación:** Acreditación de horas efectivas de servicio universitario ante la Dirección de Escuela de la EPIS e insignias dinámicas.
5. **Cumplimiento Legal:** Consentimiento digital informado bajo la Ley N° 29733 (Protección de Datos Personales).

---

## 📁 Estructura del Repositorio

```text
Proyecto_Sistema_Web_P2P/
├── docs/
│   ├── FD01-EPIS-Informe de Factibilidad.md
│   ├── FD01-EPIS-Informe de Factibilidad.pdf
│   ├── FD02-EPIS-Informe Vision de Proyecto.md
│   ├── FD02-EPIS-Informe Vision de Proyecto.pdf
│   ├── Requerimientos.md
│   ├── diagramas_de_secuencia.md
│   └── diseño.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BookingView.tsx
│   │   │   ├── ConsentModal.tsx
│   │   │   ├── GamificationView.tsx
│   │   │   ├── HomeView.tsx
│   │   │   ├── ImageCarousel.tsx
│   │   │   ├── LateralDocks.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── RecommendationView.tsx
│   │   ├── data/
│   │   │   └── mockData.ts
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── rules_doc.md
├── .gitignore
└── README.md
```

---

## 🚀 Instalación y Ejecución de la Maqueta Web

### Requisitos Previos
- Node.js (versión 18+ o superior)
- npm o yarn

### Pasos
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/JMedina255/sistema_web_p2p.git
   cd sistema_web_p2p
   ```
2. Acceder al directorio del frontend e instalar dependencias:
   ```bash
   cd frontend
   npm install
   ```
3. Iniciar el servidor de desarrollo:
   ```bash
   npm run dev
   ```
4. Abrir en el navegador: [http://localhost:5173](http://localhost:5173)

### Compilación para Producción
```bash
npm run build
```

---

## ⚖️ Licencia y Cumplimiento
Proyecto desarrollado con fines académicos en la Universidad Privada de Tacna. Cumplimiento estricto con la Ley N° 29733 de Protección de Datos Personales del Perú.
