# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Rediseño del sitio `servicio-tecnico-en-cartagena.com` a partir del archivo
que compartiste (`public_html_4.zip`), con una **arquitectura ampliada**
pensada para posicionar en Google en Cartagena: más páginas indexables, más
enlazado interno, enlaces salientes de autoridad y más cobertura de palabras
clave.

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

## Qué se corrigió de la versión anterior

1. No existía una página de inicio "todas las marcas" (la home era en
   realidad la página de Samsung).
2. Las páginas estaban aisladas, sin ningún enlace entre ellas.
3. Todas las imágenes cargaban desde un dominio ajeno (`turepuestoslg.click`).
4. Tailwind por CDN, más lento que un CSS propio.
5. Correo y dirección distintos e inconsistentes en cada página (NAP).
6. FAQ y "consejos rápidos" casi idénticos entre marcas (contenido duplicado).
7. Testimonios con los mismos nombres repetidos en las 6 páginas.
8. Sin páginas propias por servicio o por zona, sin enlaces salientes, y con
   poca cobertura de palabras clave de cola larga.

## Qué se agregó en esta iteración (a partir de tu feedback)

- **Etiqueta de verificación de Google Search Console** añadida a las 20
  páginas: `google-site-verification` con tu código.
- **3 páginas de servicio** independientes de marca (mantenimiento
  preventivo, instalación de nevecones, reparación de compresores), cada una
  con su propio `<title>`, meta description, FAQ y datos estructurados
  `Service`.
- **8 páginas de zona** (Bocagrande, Manga, El Laguito, Castillogrande,
  Crespo, Centro Histórico, Pie de la Popa, Turbaco), cada una con contenido
  propio sobre las características reales de ese sector (brisa marina en
  Bocagrande, cercanía al aeropuerto en Crespo, etc.), no una copia genérica.
- **Página pilar de fallas comunes** (`fallas-comunes-neveras-cartagena.html`)
  que reúne las fallas principales de las 6 marcas en una sola página, con
  enlace profundo a la sección de fallas de cada marca.
- **Enlaces salientes (autoridad)**: cada página de marca y la home enlazan
  al sitio oficial de la marca en Colombia y a la Superintendencia de
  Industria y Comercio (SIC) para información de garantías al consumidor.
- **Más palabras clave de cola larga** en meta keywords y contenido: "cerca
  de mí", "cuánto cuesta", por sector, por servicio.
- **Menú de navegación ampliado** con desplegables de Marcas, Servicios y
  Zonas (antes solo existía el de Marcas).
- **FAQ general ampliado** de 6 a 11 preguntas (precio del diagnóstico,
  atención en fines de semana, marcas atendidas, diferencia entre
  mantenimiento y reparación, negocios/restaurantes).
- **`sitemap.xml`** actualizado con las 20 páginas.

## Pendiente de tu parte

1. **Reemplaza las imágenes** por fotos reales — instrucciones en
   `IMAGENES-LEEME.md`.
2. **Confirma el correo de contacto**: sigo usando
   `contacto@servicio-tecnico-en-cartagena.com` como correo consistente en
   todo el sitio. Si tienes uno real, dímelo y lo actualizo en las 20
   páginas de una vez.
3. **Reemplaza los testimonios** por reseñas reales o incrusta tus reseñas
   de Google Business Profile.
4. **Verifica los enlaces salientes** a los sitios oficiales de cada marca
   (Samsung, LG, Electrolux, Whirlpool, Mabe, Haceb): puse las URLs
   oficiales conocidas para Colombia, pero confírmalas antes de publicar por
   si alguna cambió.
5. **Sube el sitio a Google Search Console** — la etiqueta de verificación
   ya está en el `<head>` de las 20 páginas, así que Google debería poder
   verificar la propiedad en cuanto publiques el sitio. Luego envía
   `sitemap.xml`.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
