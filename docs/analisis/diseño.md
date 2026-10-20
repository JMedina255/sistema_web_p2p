# 📘 Design System & UI Style Guide — DNA Portal Web UPT

Guía exhaustiva del sistema de diseño, paleta de colores, tipografía, componentes y tokens CSS/Tailwind extraídos de la interfaz del portal universitario para el **Sistema Web P2P de Mentorías Académicas (EPIS-UPT, 2026)**.

---

## Control de Versiones

| Versión | Responsable | Aprobado por | Fecha | Descripción del Documento |
| :---: | :--- | :--- | :---: | :--- |
| **1.0** | Equipo de UI/UX | Docente EPIS-UPT | 05/09/2026 | Definición de tokens, componentes, paleta institucional y guía de estilos. |

---

## Tabla de Contenidos

1. [🎨 Paleta de Colores & Tokens](#1--paleta-de-colores--tokens)
   - 1.1 [Colores Principales (Brand Identity)](#11-colores-principales-brand-identity)
   - 1.2 [Colores de Superficie y Fondo](#12-colores-de-superficie-y-fondo)
   - 1.3 [Colores de Texto y Tipografía](#13-colores-de-texto-y-tipografía)
2. [✍️ Tipografía](#2-️-tipografía)
   - 2.1 [Familias Tipográficas](#21-familias-tipográficas)
   - 2.2 [Escala y Jerarquía Tipográfica](#22-escala-y-jerarquía-tipográfica)
3. [📐 Layouts y Estructuras](#3--layouts-y-estructuras)
   - 3.1 [Barras de Navegación Dual](#31-barras-de-navegación-dual)
   - 3.2 [Barras Flotantes Laterales (Dock Bars)](#32-barras-flotantes-laterales-dock-bars)
4. [🧩 Especificación de Componentes](#4--especificación-de-componentes)
   - 4.1 [Botones (Buttons)](#41-botones-buttons)
   - 4.2 [Tarjetas de Eventos / Noticias (EventCard)](#42-tarjetas-de-eventos--noticias-eventcard)
   - 4.3 [Tarjetas de Testimonios ("Experiencias que Inspiran")](#43-tarjetas-de-testimonios-experiencias-que-inspiran)
   - 4.4 [Carruseles & Paginación](#44-carruseles--paginación)
5. [💻 Configuración para Tailwind CSS](#5--configuración-para-tailwind-css-tailwindconfigjs)
6. [🌐 Variables CSS Nativas](#6--variables-css-nativas-themecss)

---

## 1. 🎨 Paleta de Colores & Tokens

### 1.1 Colores Principales (Brand Identity)

| Rol / Token | Código HEX | RGB / HSL | Uso Principal |
| :--- | :---: | :---: | :--- |
| `--color-primary-navy` | `#1C2A59` | `rgb(28, 42, 89)` | Topbar superior, títulos H1/H2, enlaces principales, pie de página |
| `--color-secondary-blue` | `#0066CC` | `rgb(0, 102, 204)` | Botones secundarios, acentos dinámicos, banners degradados |
| `--color-accent-gold` | `#B99451` | `rgb(185, 148, 81)` | Botones de acción *"Admisión"*, *"Escríbenos"*, *"Más detalles"*, insignias |
| `--color-accent-gold-dark` | `#9D7A39` | `rgb(157, 122, 57)` | Estado `:hover` y `:active` de botones dorados |
| `--color-accent-gold-light` | `#D9BF7D` | `rgb(217, 191, 125)` | Bordes decorativos circulares (avatares, marcos de fotos) |

### 1.2 Colores de Superficie y Fondo

| Token | Código HEX | RGB | Uso |
| :--- | :---: | :---: | :--- |
| `--color-bg-main` | `#F4F6F9` | `rgb(244, 246, 249)` | Fondo general de secciones (Eventos, Testimonios) |
| `--color-bg-card` | `#FFFFFF` | `rgb(255, 255, 255)` | Fondo de tarjetas y contenedor de contenidos |
| `--color-bg-topbar` | `#172349` | `rgb(23, 35, 73)` | Barra ultra-superior de enlaces institucionales |
| `--color-border-subtle` | `#E2E8F0` | `rgb(226, 232, 240)` | Bordes de tarjetas, divisores horizontales y botones flotantes |

### 1.3 Colores de Texto y Tipografía

| Token | Código HEX | RGB | Uso |
| :--- | :---: | :---: | :--- |
| `--color-text-heading` | `#1E2B5A` | `rgb(30, 43, 90)` | Títulos principales de sección y nombres |
| `--color-text-body` | `#5A6578` | `rgb(90, 101, 120)` | Texto de párrafo, testimonios, descripciones |
| `--color-text-muted` | `#8A94A6` | `rgb(138, 148, 166)` | Metadatos, fechas, pie de tarjetas |
| `--color-text-gold` | `#A6823F` | `rgb(166, 130, 63)` | Subtítulos de cargos/carreras en testimonios |

---

## 2. ✍️ Tipografía

### 2.1 Familias Tipográficas
- **Familia Primaria:** `Montserrat`, `Inter` o `Plus Jakarta Sans`, sans-serif.
- **Respaldo del Sistema:** `system-ui`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, sans-serif.

### 2.2 Escala y Jerarquía Tipográfica

| Nivel / Rol | Tamaño (Desktop) | Peso (Font-Weight) | Altura de Línea | Color Aplicado | Transformación / Estilo |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Display / Hero Titles** | `36px - 44px` | Bold (700) / ExtraBold (800) | `1.2` | `#1C2A59` | Normal / Tracking ajustado |
| **Section Heading (H2)** | `28px - 32px` | Bold (700) | `1.3` | `#1C2A59` | Normal |
| **Card Title (H3)** | `16px - 18px` | ExtraBold (800) | `1.35` | `#1C2A59` | `uppercase` |
| **Body Text** | `14px - 15px` | Regular (400) / Italic | `1.6` | `#5A6578` | Lectura continua |
| **Microcopy / Links** | `12px - 13px` | Medium (500) | `1.4` | `#8A94A6` | `letter-spacing: 0.02em` |

---

## 3. 📐 Layouts y Estructuras

### 3.1 Barras de Navegación Dual

#### Top Utility Bar
- **Fondo:** `#172349`
- **Altura:** `36px`
- **Enlaces con iconos:** Ubicados a la derecha (*Inicio, UPT Internacional, UPT Calidad, GPS Alumni, UPT Idiomas*).
- **Tipografía:** Texto blanco `12px` con opacidad `0.85` en reposo y `1.0` en `:hover`.

#### Main Header
- **Fondo:** `#FFFFFF` con sombra tenue `box-shadow: 0 2px 10px rgba(0,0,0,0.05)`.
- **Altura:** `70px - 80px`.
- **Lado Izquierdo:** Logotipo heráldico con escudo institucional y tipografía en serif/sans-serif.
- **Centro / Derecha:** Menú horizontal interactivo con dropdowns (*Pregrado ▾, Postgrado, Servicios ▾, Oficinas ▾, Nosotros*).
- **Botones de Llamado a la Acción (CTA):**
  - **Botón "Admisión":** Dorado, bordes redondeados `10px`, icono de libro/registro.
  - **Botón "Escríbenos":** Dorado, bordes redondeados `10px`, icono de mensaje/avión.

### 3.2 Barras Flotantes Laterales (Dock Bars)

- **Dock Izquierdo (Accesos Rápidos Universitarios):**
  - Barra vertical fija en pantalla con fondo blanco (`#FFFFFF`).
  - Bordes redondeados `12px`, borde perimetral `#E2E8F0`.
  - Iconos lineales en azul marino: *Matrícula, Avisos, Notas, Biblioteca, Trámites, Horarios, Pagos, Campus Virtual*.
- **Dock Derecho (Redes Sociales):**
  - Píldora vertical flotante blanca con iconos interactivos: *Facebook, Instagram, LinkedIn, TikTok*.

---

## 4. 🧩 Especificación de Componentes

### 4.1 Botones (Buttons)

```css
/* Botón Principal Dorado (CTA) */
.btn-gold {
  background-color: #B99451;
  color: #FFFFFF;
  font-weight: 600;
  font-size: 14px;
  padding: 10px 24px;
  border-radius: 9999px; /* Pill shape o 10px según variante */
  border: none;
  cursor: pointer;
  transition: all 0.25s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-gold:hover {
  background-color: #9D7A39;
  box-shadow: 0 4px 12px rgba(185, 148, 81, 0.35);
  transform: translateY(-1px);
}

/* Botón Navegación Ovalado (Píldora Azul Oscuro) */
.btn-pill-navy {
  background-color: #1C2A59;
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.btn-pill-navy:hover {
  background-color: #172349;
}
```

### 4.2 Tarjetas de Eventos / Noticias (EventCard)

- **Contenedor:** Fondo blanco `#FFFFFF`, bordes redondeados de `20px`, sombra suave `box-shadow: 0 8px 24px rgba(28, 42, 89, 0.06)`.
- **Imagen Superior:** Aspect ratio `4:3` o `1:1`, esquinas redondeadas internas `14px`, marco contenedor con padding de `12px`.
- **Cuerpo del Contenido:**
  - **Título:** Mayúsculas negrita (`#1C2A59`, `15px`).
  - **Resumen / Descripción:** Color `#5A6578`, tamaño `13px`, máximo 3 líneas con ellipsis.
  - **Acción:** Botón *"Más detalles"* dorado full-width o centrado con bordes redondeados de `16px`.

### 4.3 Tarjetas de Testimonios ("Experiencias que Inspiran")

- **Avatar:** Fotografía circular de `110px × 110px` centrada, con un borde dorado grueso (`3px solid #D9BF7D`).
- **Cita:** En estilo cursiva (*italic*), color `#5A6578`, tamaño `13px`, texto justificado o centrado.
- **Autor:** Nombre en negrita azul marino (`#1C2A59`, `16px`).
- **Subtítulo:** Carrera en `#8A94A6` y cargo/empresa destacado en dorado institucional (`#A6823F`).

### 4.4 Carruseles & Paginación

- **Flechas de navegación flotantes:** Botones circulares translúcidos en azul `#1C2A59` con opacidad `0.6`, flechas blancas centradas, y opacidad `1.0` al hacer `:hover`.
- **Puntos de navegación (Dots):** Píldoras de `8px`, con color activo en dorado `#B99451` e inactivos en gris suave `#D1D5DB`.

---

## 5. 💻 Configuración para Tailwind CSS (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        upt: {
          navy: '#1C2A59',
          'navy-dark': '#172349',
          blue: '#0066CC',
          gold: '#B99451',
          'gold-dark': '#9D7A39',
          'gold-light': '#D9BF7D',
          bg: '#F4F6F9',
          text: '#5A6578',
        }
      },
      borderRadius: {
        'card': '20px',
        'btn': '12px',
      },
      boxShadow: {
        'upt-card': '0 8px 25px -5px rgba(28, 42, 89, 0.08), 0 8px 10px -6px rgba(28, 42, 89, 0.04)',
        'upt-float': '0 4px 18px rgba(0, 0, 0, 0.12)',
      },
      fontFamily: {
        sans: ['Montserrat', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

---

## 6. 🌐 Variables CSS Nativas (`theme.css`)

```css
:root {
  /* Brand Colors */
  --primary-navy: #1C2A59;
  --primary-navy-dark: #172349;
  --primary-blue: #0066CC;
  --accent-gold: #B99451;
  --accent-gold-hover: #9D7A39;
  --accent-gold-border: #D9BF7D;

  /* Surfaces & Backgrounds */
  --bg-page: #F4F6F9;
  --bg-surface: #FFFFFF;
  --border-color: #E2E8F0;

  /* Typography Colors */
  --text-primary: #1C2A59;
  --text-body: #5A6578;
  --text-muted: #8A94A6;
  --text-accent: #A6823F;

  /* Radii */
  --radius-card: 20px;
  --radius-button: 12px;
  --radius-pill: 9999px;

  /* Shadows */
  --shadow-card: 0 8px 24px rgba(28, 42, 89, 0.07);
  --shadow-floating: 0 4px 14px rgba(0, 0, 0, 0.08);
}
```