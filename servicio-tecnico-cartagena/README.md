# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Cuarta iteración: corrige el bug de navegación, agrega las fotos reales de
LG, suma 2 páginas dedicadas más por marca (repuestos originales y preguntas
frecuentes) y amplía el texto SEO en las páginas más cortas.

## Estructura del sitio (50 páginas)

```
index.html                                 → home, todas las marcas
preguntas-frecuentes.html                  → FAQ general (pilar)
fallas-comunes-neveras-cartagena.html      → pilar de fallas (enlaza a cada marca)

marcas/samsung/   (6 páginas cada una)
marcas/lg/
marcas/electrolux/
marcas/whirlpool/
marcas/mabe/
marcas/haceb/
  index.html
  fallas-comunes.html
  mantenimiento-preventivo.html
  instalacion-nevecones.html
  repuestos-originales.html      ← nueva
  preguntas-frecuentes.html      ← nueva

servicios/            → 3 páginas "pilar" (genéricas, enlazan a cada marca)
zonas/                → 8 páginas, una por sector de Cartagena
```

36 páginas de marca (6 × 6) + 8 de zona + 3 de servicio + 3 generales = 50.

## Qué se corrigió en esta iteración

1. **Bug de navegación corregido.** En las páginas de fallas, mantenimiento,
   instalación (y los pilares de servicios/zonas), el botón principal del
   hero (“Agenda tu…”) era un ancla `#contacto` que saltaba a la sección de
   contacto pegada justo antes del pie de página. En páginas cortas eso se
   sentía como si el clic te mandara al footer. Ahora ese botón va
   directamente a WhatsApp con el mensaje pre-cargado, y se agregó un botón
   "Llamar" al lado. El salto a `#contacto` solo se mantiene en el home y en
   el resumen de cada marca, donde sí existe un formulario completo más
   abajo.
2. **Imágenes reales de LG** (logo, nevera French Door en cocina, cliente
   usando InstaView, galería de producto) reemplazando los placeholders,
   con el rojo oficial de LG (`#AD0036`) como color de acento.
3. **2 páginas nuevas por marca**: `repuestos-originales.html` (compresores,
   tarjetas electrónicas, empaques y motores originales, con FAQ propia) y
   `preguntas-frecuentes.html` (preguntas específicas de esa marca: precio,
   garantía, zonas). La pestaña de navegación de cada marca ahora tiene 6
   secciones en vez de 4.
4. **Más texto SEO** en las secciones más cortas (frecuencia de
   mantenimiento, tiempo de instalación), agregando contexto de zonas y
   tecnología específica de cada marca en vez de un párrafo genérico de una
   sola línea.

## Estado de las imágenes por marca

Ver `IMAGENES-LEEME.md`. Resumen: Samsung y LG completos; Electrolux,
Whirlpool, Mabe y Haceb siguen con el placeholder de color.

## Pendiente de tu parte

1. Enviar las imágenes de las 4 marcas restantes (logo + fotos), y decirme
   si cada una es oficialmente autorizada por el fabricante o no.
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).
3. Reemplazar los testimonios por reseñas reales o reseñas de Google
   Business Profile.
4. Subir el sitio a Google Search Console (la etiqueta ya está en el
   `<head>` de las 50 páginas) y enviar `sitemap.xml`.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
