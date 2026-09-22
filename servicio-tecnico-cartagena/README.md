# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Quinta iteración: página propia por marca y por zona (48 páginas nuevas),
fotos de técnico de LG, palabra clave "servicio técnico [marca] en Cartagena"
resaltada en negrita en todas las páginas, y una nota importante sobre el
reporte de navegación.

## Sobre el reporte de "los enlaces llevan al pie de página"

Antes de este cambio ya se había corregido un bug real: el botón principal
del hero en las páginas cortas usaba un ancla `#contacto` que saltaba a la
sección de contacto pegada al pie de página (ver iteración anterior).

En este mensaje se reportó que **todos** los enlaces internos seguían
teniendo ese problema. Antes de tocar nada, probé exhaustivamente el sitio
real (los mismos archivos de este zip) con un navegador automatizado
(Playwright), simulando clics reales de usuario en: tarjetas de marca,
pestañas de navegación, menú superior, enlaces del pie de página, tarjetas
de servicio y enlaces entre zona y marca. **En los 98 archivos reales, cada
clic deja la página en `scrollY = 0` (arriba del todo)** — no encontré ningún
enlace que salte al pie de página.

Mi conclusión: el archivo que se sube a Hostinger (este zip) navega
correctamente. Si en la vista previa del enlace de Artifact seguía viéndose
el salto al footer, es muy probablemente una particularidad de cómo esa
vista previa maneja la navegación entre varios archivos HTML dentro de un
mismo enlace — no algo en el código del sitio. Para confirmar el
comportamiento real, la forma más fiable es probarlo con
`python3 -m http.server` desde esta carpeta (ver abajo) o subiéndolo
directamente a Hostinger.

## Qué se agregó en esta iteración

1. **Página propia por marca y por zona** (`marcas/{marca}/zonas/{zona}.html`):
   48 páginas nuevas (6 marcas × 8 zonas), cada una con su propio título,
   meta description, testimonio filtrado por esa zona cuando existe, FAQ de
   tiempo de llegada + una pregunta propia de la marca, y enlaces cruzados a
   las otras 7 zonas de esa marca y a las 4 páginas de servicio de esa marca.
   El sitio pasó de 50 a 98 páginas.
2. **Palabra clave resaltada**: la frase exacta "servicio técnico [marca] en
   Cartagena" ahora aparece en **negrita** en el párrafo principal de cada
   página de marca (resumen, fallas, mantenimiento, instalación, repuestos,
   preguntas frecuentes y ahora también zona), no solo en el título.
3. **Fotos reales de LG actualizadas**: reemplacé las fotos de catálogo por
   las 2 fotos de técnico que enviaste (maletín "LG Service", carné), usadas
   ahora como imagen principal y de equipo; las fotos de catálogo (cocina,
   InstaView, ThinQ, línea de productos) pasaron a la galería.
4. **Sin la palabra "Autorizado" en LG** — no confirmaste que seas
   distribuidor autorizado de LG, así que mantuve esa etiqueta solo en
   Samsung. Ver `IMAGENES-LEEME.md`.

## Estructura del sitio (98 páginas)

```
marcas/samsung/   (7 tipos de página cada una)
marcas/lg/
marcas/electrolux/
marcas/whirlpool/
marcas/mabe/
marcas/haceb/
  index.html
  fallas-comunes.html
  mantenimiento-preventivo.html
  instalacion-nevecones.html
  repuestos-originales.html
  preguntas-frecuentes.html
  zonas/
    bocagrande.html  manga.html  el-laguito.html  castillogrande.html
    crespo.html  centro-historico.html  pie-de-la-popa.html  turbaco.html
```

## Pendiente de tu parte

1. Enviar las imágenes de Electrolux, Whirlpool, Mabe y Haceb, y decirme si
   cada una es autorizada oficialmente por el fabricante.
2. Confirmar si LG te autorizó oficialmente (para agregar la etiqueta
   "Autorizado" como en Samsung).
3. Probar la navegación real subiendo este zip a Hostinger (o con
   `python3 -m http.server`), y avisarme si el salto al pie de página
   persiste ahí — en ese caso sería un caso distinto al que ya revisé y
   necesitaría el enlace exacto donde ocurre.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
