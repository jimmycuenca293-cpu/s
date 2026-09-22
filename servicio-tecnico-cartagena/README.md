# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Tercera iteración: cada marca ahora tiene su **propio logo en el encabezado**,
sus **propias páginas dedicadas** de fallas comunes / mantenimiento /
instalación (nada compartido ni mezclado entre marcas), todas las zonas de
cobertura enlazadas desde cada marca, y un rediseño visual completo del CSS.

## Estructura del sitio (38 páginas)

```
index.html                                 → home, todas las marcas
preguntas-frecuentes.html                  → FAQ general (pilar)
fallas-comunes-neveras-cartagena.html      → pilar de fallas (enlaza a cada marca)

marcas/samsung/
  index.html                → resumen de la marca (logo propio en el header)
  fallas-comunes.html       → guía completa de fallas Samsung
  mantenimiento-preventivo.html
  instalacion-nevecones.html
marcas/lg/            (mismas 4 páginas)
marcas/electrolux/    (mismas 4 páginas)
marcas/whirlpool/     (mismas 4 páginas)
marcas/mabe/          (mismas 4 páginas)
marcas/haceb/         (mismas 4 páginas)

servicios/            → 3 páginas "pilar" (genéricas, enlazan a cada marca)
zonas/                → 8 páginas, una por sector de Cartagena
```

24 páginas de marca (4 × 6) + 8 de zona + 3 de servicio + 3 generales = 38.

## Qué cambió en esta iteración (a partir de tu feedback)

1. **Logo propio por marca en el encabezado.** Cada una de las 24 páginas de
   marca muestra el logo de esa marca (no el genérico "STC") en el header,
   con "Servicio Técnico [Marca] · Cartagena" y una pestaña "Autorizado"
   cuando aplica (por ahora, solo Samsung, que confirmaste que es autorizado).
   La barra superior incluye un enlace "&larr; Todas las marcas" para volver
   al sitio general sin perder la navegación.
2. **Cada marca tiene sus propias páginas**, no contenido genérico compartido:
   - `fallas-comunes.html`: guía completa de diagnóstico, propia de esa marca.
   - `mantenimiento-preventivo.html`: consejos de cuidado específicos de su
     tecnología (compresor, sistema No Frost, etc.), no un texto genérico.
   - `instalacion-nevecones.html`: consideraciones de instalación propias de
     esa marca.
   - Pestañas de navegación (Resumen / Fallas Comunes / Mantenimiento /
     Instalación) en la parte superior de cada página de marca.
3. **Todas las zonas de Cartagena enlazadas desde cada marca** (antes solo se
   mostraba una muestra de 4; ahora las 8, con enlace a la página de cada
   zona).
4. **Rediseño completo del CSS**: sombras y elevación más cuidadas, tarjetas
   con hover, header con efecto de desenfoque (blur) al hacer scroll, hero
   con acento decorativo, tipografía con mejor jerarquía, footer con línea de
   acento superior — sin frameworks externos, sigue cargando rápido.
5. **Imágenes reales de Samsung** (logo, técnico autorizado con carné y
   maletín Samsung, galería de producto) reemplazando los placeholders,
   ahora usadas como foto principal y no solo como imágenes secundarias.

## Estado de las imágenes por marca

Ver `IMAGENES-LEEME.md` para el detalle. Resumen: Samsung completo con fotos
reales; LG, Electrolux, Whirlpool, Mabe y Haceb siguen con el placeholder de
color a la espera de sus imágenes.

## Pendiente de tu parte

1. Enviar las imágenes de las 5 marcas restantes (logo + fotos), y decirme si
   cada una es oficialmente autorizada por el fabricante o no.
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).
3. Reemplazar los testimonios por reseñas reales o reseñas de Google Business
   Profile.
4. Subir el sitio a Google Search Console (la etiqueta ya está en el
   `<head>` de las 38 páginas) y enviar `sitemap.xml`.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
