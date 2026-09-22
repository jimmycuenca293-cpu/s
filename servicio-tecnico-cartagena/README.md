# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Rediseño del sitio `servicio-tecnico-en-cartagena.com` a partir del archivo
que compartiste (`public_html_4.zip`: `default.php`, `lg`, `electrolux`,
`whirlpool`, `mabe`, `haceb`). Mismo contenido y textos aprovechados donde
eran buenos, con una **arquitectura nueva** pensada para posicionar en
Google en Cartagena.

## Qué tenía el sitio original (diagnóstico)

1. **Sin página de inicio real**: `default.php` era en realidad la página de
   Samsung — no existía una página "todas las marcas".
2. **Páginas aisladas, sin enlaces internas**: ninguna de las 6 páginas
   (`default.php`, `lg`, `electrolux`, `whirlpool`, `mabe`, `haceb`) enlazaba
   a las demás, ni siquiera a la home. Google no podía descubrirlas navegando
   el sitio, y el usuario no podía cambiar de marca sin conocer la URL exacta.
3. **Todas las imágenes cargaban desde un dominio ajeno**
   (`turepuestoslg.click`), lo que hace el sitio más lento y frágil (ver
   `IMAGENES-LEEME.md`).
4. **Tailwind vía CDN** (`cdn.tailwindcss.com`): ese script compila los
   estilos en el navegador en cada carga, lo cual Tailwind mismo desaconseja
   en producción por el impacto en velocidad.
5. **Datos de contacto inconsistentes**: cada página tenía un correo
   distinto (`servicio@samsungcartagena.com`, `servicio@lgcartagena.com`,
   etc.) que no coincide con tu dominio real, y una dirección de relleno
   ("Mock Address"). Para Google, el NAP (nombre, dirección, teléfono) debe
   ser idéntico en todo el sitio y en tu ficha de Google Business Profile.
6. **Contenido casi idéntico entre páginas** (FAQ y "consejos rápidos" con el
   mismo texto cambiando solo el nombre de la marca), lo que Google puede
   interpretar como contenido duplicado o páginas puerta ("doorway pages").
7. **Testimonios con los mismos nombres repetidos en cada marca** (María P.,
   Carlos R., Luisa T. en todas las páginas), lo que se ve poco creíble.

## Qué cambia en esta versión

- **`index.html`**: nueva página de inicio, "todas las marcas", con su propio
  contenido único (quiénes somos, por qué elegirnos, zonas, testimonios, FAQ
  resumida) y una cuadrícula que enlaza a cada marca.
- **`/marcas/samsung.html`, `lg.html`, `electrolux.html`, `whirlpool.html`,
  `mabe.html`, `haceb.html`**: una página por marca, cada una con:
  - Encabezado, menú y pie de página **iguales e interconectados** (home ↔
    cada marca ↔ FAQ), con menú "Marcas" desplegable y migas de pan
    (breadcrumbs).
  - Contenido específico y diferenciado por marca (fallas comunes reales de
    cada tecnología: Linear Compressor de LG, Twin Cooling de Samsung, No
    Frost de Mabe/Haceb, Sixth Sense de Whirlpool, tarjetas electrónicas de
    Electrolux).
  - Solo 2 preguntas frecuentes propias de la marca + enlace a la página
    general de preguntas frecuentes (evita duplicar el mismo FAQ seis veces).
  - Enlaces a "otras marcas que reparamos" (refuerza el enlazado interno).
  - Datos estructurados (`schema.org`): `Service`, `FAQPage` y
    `BreadcrumbList` propios de cada página.
- **`preguntas-frecuentes.html`**: página "pilar" con las preguntas generales
  (garantía, zonas, repuestos, frecuencia de mantenimiento), enlazada desde
  todas las demás páginas.
- **Imágenes locales y organizadas por carpeta** (`/images/samsung/`,
  `/images/lg/`, etc.) en vez de hotlink a un dominio externo — ver
  `IMAGENES-LEEME.md` para reemplazarlas por fotos reales.
- **Sin frameworks pesados**: CSS propio y liviano (`css/estilos.css`, ~9 KB)
  en vez del script de Tailwind por CDN. Menos peso, carga más rápida.
- **`robots.txt` y `sitemap.xml`** actualizados con las 8 páginas del sitio.
- **NAP consistente**: mismo teléfono, mismo correo
  (`contacto@servicio-tecnico-en-cartagena.com`) y misma zona de cobertura en
  todas las páginas.
- **Acordeón de FAQ y fallas comunes con `<details>/<summary>` nativo**: no
  depende de JavaScript para mostrar el contenido (mejor para SEO y
  accesibilidad) y es más liviano que la versión anterior.
- **Formulario de agendamiento**: arma el mensaje y redirige a WhatsApp
  (`js/main.js`), sin necesidad de backend.

## Pendiente de tu parte (importante)

1. **Reemplaza las imágenes** por fotos reales — instrucciones en
   `IMAGENES-LEEME.md`.
2. **Confirma o corrige los datos de contacto**: usé
   `contacto@servicio-tecnico-en-cartagena.com` como correo consistente. Si
   tienes un correo real o una dirección física para mostrar (o prefieres
   dejar solo "servicio a domicilio" sin dirección, que es válido para un
   negocio sin local propio), dímelo y lo actualizo.
3. **Reemplaza los testimonios** por reseñas reales de clientes, o mejor aún,
   incrusta tus reseñas reales de Google Business Profile — los testimonios
   inventados repetidos son un riesgo de credibilidad.
4. **Sube el sitio a Google Search Console** y envía `sitemap.xml` una vez
   esté publicado en el dominio real.
5. Verifica el ID de Google Tag Manager (`GTM-5BNQCQ7G`, tomado del sitio
   original) y el meta de verificación de Search Console si necesitas
   volver a añadirlo.

## Estructura de carpetas

```
servicio-tecnico-cartagena/
  index.html
  preguntas-frecuentes.html
  robots.txt
  sitemap.xml
  css/estilos.css
  js/main.js
  marcas/
    samsung.html
    lg.html
    electrolux.html
    whirlpool.html
    mabe.html
    haceb.html
  images/
    logo/
    home/
    samsung/  lg/  electrolux/  whirlpool/  mabe/  haceb/
```

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
