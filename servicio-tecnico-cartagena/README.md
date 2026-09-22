# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Rediseño del sitio `servicio-tecnico-en-cartagena.com` con una arquitectura
ampliada para posicionar en Google en Cartagena: más páginas indexables,
enlazado interno, enlaces salientes de autoridad y cobertura de palabras
clave. Ver `IMAGENES-LEEME.md` para el estado de las fotos por marca.

## Estructura del sitio (20 páginas)

```
index.html                                 → home, todas las marcas
preguntas-frecuentes.html                  → FAQ general (pilar)
fallas-comunes-neveras-cartagena.html      → pilar de fallas por marca

marcas/
  samsung.html  lg.html  electrolux.html
  whirlpool.html  mabe.html  haceb.html    → 1 página por marca

servicios/
  mantenimiento-preventivo-neveras-cartagena.html
  instalacion-nevecones-cartagena.html
  reparacion-compresores-neveras-cartagena.html

zonas/
  bocagrande.html   manga.html        el-laguito.html
  castillogrande.html  crespo.html    centro-historico.html
  pie-de-la-popa.html  turbaco.html   → 1 página por sector de Cartagena
```

Todo enlaza entre sí: el menú tiene desplegables de **Marcas**, **Servicios**
y **Zonas**; cada página de marca enlaza a servicios y zonas relacionadas;
cada página de servicio y de zona enlaza de vuelta a las 6 marcas; y el pie
de página repite el mapa completo del sitio en todas las páginas.

## SEO técnico incluido

- Meta tags completos (title, description, keywords, canonical, Open Graph).
- **Etiqueta de verificación de Google Search Console** en las 20 páginas.
- Datos estructurados `schema.org`: `LocalBusiness`, `Service`, `FAQPage`,
  `BreadcrumbList` según la página.
- Enlaces salientes de autoridad: sitio oficial de cada marca y la
  Superintendencia de Industria y Comercio (garantías al consumidor).
- `robots.txt` y `sitemap.xml` con las 20 páginas.
- Sin frameworks pesados: CSS propio y liviano en vez de Tailwind por CDN.
- Imágenes locales organizadas por carpeta, sin depender de servidores
  externos.

## Estado de las imágenes por marca

- **Samsung**: fotos reales aplicadas (logo oficial + 4 fotos de producto),
  con `alt` descriptivo y el color de acento de la página tomado del azul
  real del logo (`#034EA2`).
- **LG, Electrolux, Whirlpool, Mabe, Haceb**: siguen con el placeholder de
  color a la espera de que envíes las imágenes de cada una.

Detalle completo en `IMAGENES-LEEME.md`.

## Pendiente de tu parte

1. Enviar las imágenes de las 5 marcas restantes (logo + fotos), igual que
   hiciste con Samsung.
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).
3. Reemplazar los testimonios por reseñas reales o reseñas de Google
   Business Profile.
4. Verificar que los enlaces a los sitios oficiales de cada marca sigan
   vigentes antes de publicar.
5. Subir el sitio a Google Search Console (la etiqueta ya está en el
   `<head>` de las 20 páginas) y enviar `sitemap.xml`.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
