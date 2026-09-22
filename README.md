# Página web SEO — Reformas García (ejemplo)

Plantilla de página web (`index.html`) optimizada para posicionamiento orgánico
en Google, lista para personalizar con los datos de tu negocio.

## Qué incluye

- **Meta tags SEO**: `title`, `description`, `keywords`, `canonical`, `robots`.
- **Open Graph y Twitter Cards** para compartir en redes sociales.
- **Datos estructurados (JSON-LD)**: `LocalBusiness` y `FAQPage` (Schema.org),
  para aparecer con rich snippets en Google.
- **HTML semántico**: un único `<h1>`, jerarquía de `<h2>`/`<h3>`, `<header>`,
  `<main>`, `<section>`, `<footer>`.
- **Contenido orientado a conversión**: hero con CTA, servicios, proceso,
  testimonios, FAQ y bloque de contacto.
- **Responsive** sin dependencias externas (CSS puro).
- `robots.txt` y `sitemap.xml` básicos.

## Cómo personalizarla

1. **Reemplaza los datos del negocio** en `index.html`:
   - Nombre, teléfono, email, dirección (también dentro del JSON-LD).
   - Dominio real en `canonical`, `og:url`, `og:image` y en `sitemap.xml`/`robots.txt`.
2. **Ajusta las palabras clave** (`title`, `meta description`, `h1`, `h2`)
   a tu servicio y ciudad reales (ej. "reformas integrales en \[ciudad]").
3. **Añade imágenes reales** con atributo `alt` descriptivo (mejora el SEO
   de imágenes) — actualmente la plantilla no usa imágenes para mantenerla
   ligera y rápida.
4. **Sube el sitio a Google Search Console** y envía el `sitemap.xml`.

## Buenas prácticas de SEO ya aplicadas

- Un solo `<h1>` con la palabra clave principal.
- Contenido único y relevante (evita duplicar texto de otras webs).
- Velocidad de carga: sin frameworks pesados, CSS inline.
- Enlaces internos por anclas (`#servicios`, `#contacto`, etc.).
- Sección de preguntas frecuentes con marcado `FAQPage` para rich snippets.

## Próximos pasos recomendados

- Servir el sitio por **HTTPS** con dominio propio.
- Añadir **Google Analytics / Search Console**.
- Optimizar imágenes (WebP, `loading="lazy"`).
- Conseguir enlaces externos (backlinks) de calidad.
- Publicar contenido nuevo (blog) para reforzar el posicionamiento a largo plazo.
