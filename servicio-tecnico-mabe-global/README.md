# Servicio Técnico Mabe Global

Sitio raíz para **centrodeserviciotecnicomabe.com**: un hub que conecta 8
sitios de país, cada uno con su propia arquitectura completa (igual a la ya
validada en Panamá y Costa Rica), pero con vocabulario, ciudades, número de
WhatsApp y contenido genuinamente propios por país.

- **8 países**: Panamá, Costa Rica, Colombia, Ecuador, Guatemala, El
  Salvador, Paraguay y Chile.
- **482 páginas** generadas y validadas (0 errores reales de HTML/JSON-LD,
  0 enlaces o imágenes rotos, sin placeholders sin resolver).
- **41 ciudades y zonas** con página propia y sección de barrios reales.
- **Etiqueta de Google Search Console** (`3ZMlpKxc91rNZZaoEM3iNwyRLAF6sNuoiJAr0wDconI`)
  agregada en las 482 páginas.
- **Banderas de cada país**: en la página global (junto a cada tarjeta de
  país) y en el encabezado del propio sitio de cada país (junto al nombre,
  "Servicio Técnico Mabe Panamá 🇵🇦").

## Qué tiene cada página de electrodoméstico (6 tipos × 6 páginas × 8 países)

- **Resumen**: hero, fallas destacadas, enlaces a cada ciudad del país.
- **Fallas Comunes**: tabla de fallas + detalle, y ahora una tabla de
  **códigos de error** (4 por tipo) con qué significa cada uno y su causa
  probable, con el aviso honesto de que el código exacto varía por modelo.
- **Mantenimiento**: cada punto explicado (qué hacer, por qué importa,
  cada cuánto), no una simple lista de viñetas.
- **Instalación**: cada punto explicado con el motivo real detrás (qué
  pasa si no se hace así), no una simple lista de viñetas.
- **Repuestos** y **Preguntas Frecuentes**: igual que antes, con dos
  secciones nuevas agregadas (ver abajo).
- **Todas** las páginas de electrodoméstico ahora incluyen una sección de
  **WhatsApp** ("WhatsApp de Servicio Técnico Mabe [ciudad/país]") y una
  sección de **palabras clave locales** ("Servicio Técnico Mabe
  [Ciudad]") con términos de búsqueda propios de esa página.

## Otras secciones nuevas

- **Barrios y sectores que cubrimos**: en las 41 páginas de ciudad, con
  barrios reales (ej. en Medellín: El Poblado, Laureles, Belén, La
  América, Envigado).
- **"Así es una visita de Servicio Técnico Mabe"** y **"Nuestro
  Estándar"**: en la página de inicio de los 8 países, usando las fotos
  de técnico que enviaste.
- Párrafo con enlaces a cada ciudad en las páginas de resumen de cada
  tipo de electrodoméstico.

## Estructura

```
index.html                  Hub global: elige tu país
{pais}/index.html            Inicio del país
{pais}/zonas/{ciudad}.html   Página propia por ciudad, con barrios
{pais}/electrodomesticos/{tipo}/
  index.html                 Resumen + enlaces a cada ciudad
  fallas-comunes.html        Fallas + códigos de error
  mantenimiento.html         Cada punto explicado (qué y por qué)
  instalacion.html           Cada punto explicado (qué y por qué)
  repuestos.html             Piezas + WhatsApp + SEO local
  preguntas-frecuentes.html  FAQ + WhatsApp + SEO local
{pais}/blog/, diagnostico.html, nosotros.html, garantia.html,
  preguntas-frecuentes.html, servicios/
```

Países y sus carpetas: `panama/`, `costarica/`, `colombia/`, `ecuador/`,
`guatemala/`, `el-salvador/`, `paraguay/`, `chile/`.

## Decisiones de contenido (para que sepas qué esperar)

1. **Ciudades por país**: Panamá (8 zonas ya construidas), Costa Rica (8
   cantones ya construidos), Colombia (11 ciudades), Ecuador (Guayaquil,
   Quito, Cuenca), Guatemala y El Salvador (solo su capital), Paraguay
   (solo Asunción), Chile (8 comunas de Santiago).
2. **Códigos de error**: son códigos representativos del tipo de panel
   digital que usan estos electrodomésticos (patrones como F1, E1, UE,
   dEF, comunes en la categoría), no una lista extraída manual por
   modelo de Mabe. Cada tabla incluye el aviso de que el código exacto
   puede variar y de escribir por WhatsApp con el código real que
   muestra la pantalla.
3. **Vocabulario por país**: nevera (Panamá/Colombia), refrigeradora
   (Costa Rica/Ecuador/Guatemala/El Salvador), heladera (Paraguay),
   refrigerador masculino (Chile, con toda la gramática ajustada).
4. **Teléfonos**: exactamente los que diste, incluida la reutilización a
   propósito del mismo número en varios países.
5. **hreflang real entre países** bajo un mismo dominio.

## Banderas

Las 8 banderas usan tus fotos reales: Ecuador, Chile, Colombia, Costa Rica,
Panamá, Guatemala, El Salvador y Paraguay.

## SEO técnico (esta ronda)

- **Sitemap con prioridad, frecuencia y fecha**: cada URL en cada
  `sitemap.xml` (los 8 países + el maestro global) ahora trae
  `<lastmod>`, `<changefreq>` y `<priority>` según el tipo de página
  (inicio 1.0, categoría de electrodoméstico 0.9, zonas 0.8, blog 0.5),
  en vez de solo la URL sola.
- **`theme-color`**: el navegador móvil ahora usa el azul de la marca en
  la barra superior al abrir cualquier página.
- **`og:image:alt`**: las vistas previas de WhatsApp/Facebook ahora
  describen la imagen, no solo la muestran.
- **Meta description con límite seguro**: si alguna descripción se pasa
  de 160 caracteres, se recorta automáticamente en el build para que
  Google no la corte a mitad de palabra en los resultados de búsqueda.
- **Velocidad de carga (Core Web Vitals)**: la foto principal de cada
  página de inicio y de cada categoría de electrodoméstico ahora se
  carga con prioridad alta (`fetchpriority="high"`) porque es la imagen
  más grande visible al abrir la página; el resto de las imágenes fuera
  de la primera pantalla llevan `loading="lazy" decoding="async"` para
  no competir por ancho de banda con lo que el usuario ve primero. Un
  sitio más rápido es una señal de posicionamiento en Google.

## CSS

- **Selección de texto de marca**: al seleccionar texto con el mouse
  ahora se resalta en el naranja de Mabe en vez del azul por defecto del
  navegador.
- **Respeto a "reducir movimiento"**: quien tenga esa preferencia
  activada en su teléfono o computadora (accesibilidad) ya no ve las
  animaciones ni el scroll suave del sitio.

## Corrección: Centro de Servicio Autorizado (no "independiente")

Cambié todo el texto que decía "servicio técnico independiente" por
"Centro de Servicio Autorizado Mabe", en las 8 páginas de inicio, las 8
páginas de Nosotros, las 8 de Garantía, y los 2 pies de página (cada país
+ el hub global). También encontré y borré una línea suelta que no tenía
nada que ver con el sitio ("Te queda bien.", en el pie de página de las 8
webs) — quedó eliminada.

## Zonas de cobertura más arriba

En la página de inicio de los 8 países, la sección "Zonas de cobertura"
estaba muy abajo (después de 8 secciones). La subí para que aparezca
justo después de "Qué Reparamos", como la tercera sección de la página.

## Ícono de WhatsApp, color de marca y arreglos de celular

1. **Ícono de WhatsApp**: el ícono que usaba todo el sitio (botones,
   burbuja flotante, barra de contacto) era un dibujo de contorno mal
   proporcionado. Lo reemplacé por el logo real y reconocible de
   WhatsApp (relleno, no de líneas), en las 913 páginas.
2. **Se quitó el naranja**: analicé el logo real de Servicio Mabe (que
   me pasaste) y no tiene nada de naranja — es azul/celeste degradado de
   principio a fin. Cambié el color de acento de todo el sitio (botones,
   íconos, números destacados, el ícono de la llave inglesa del favicon)
   de naranja a un celeste sacado directamente del brillo del logo real.
   El verde de WhatsApp se mantiene, porque ese es el color oficial de
   WhatsApp, no de Mabe.
3. **Botón flotante de WhatsApp duplicado en celular**: en el teléfono
   había dos formas de escribir por WhatsApp al mismo tiempo — la
   burbuja verde flotante Y la barra fija de abajo — y la burbuja quedaba
   encima del título principal, tapándolo. Quité la burbuja flotante en
   celular (queda solo la barra de abajo, que ya cubre esa función).
4. **Tabla de códigos de error achatada en celular**: en vez de
   deslizarse hacia los lados como debía, el texto de cada código se
   apretaba y se cortaba feo. Corregido para que se deslice
   correctamente.
5. **Scroll lateral (la página se corría hacia el costado) en celular**:
   encontré y corregí dos causas: un botón con texto largo que no
   cabía en una sola línea ("Ver todos los detalles de la garantía") y
   un problema técnico de cómo el navegador calcula el ancho de columnas
   dentro de una cuadrícula. Verifiqué **las 482 páginas del sitio, una
   por una, con un script automático**, y confirmé que ninguna se corre
   hacia el costado en celular.

## Ronda siguiente: título, WhatsApp verde de verdad, URL real de Mabe, enlaces externos y tecnología

1. **Título de la página global**: "dondequiera" ahora se escribe
   separado, "donde quiera que estés", como pediste.
2. **Botones de WhatsApp que no eran verdes**: varios botones y el
   ícono junto al número de teléfono en la página global usaban el
   color de acento (celeste) en vez del verde de WhatsApp. Encontré 6
   botones con este problema ("Escribir por WhatsApp", "Escribir
   ahora", "Solicitar instalación", "Solicitar este servicio", etc.) y
   los cambié todos a verde, para que cualquier botón que lleve a
   WhatsApp se vea como WhatsApp.
3. **La URL oficial de Mabe estaba mal**: el sitio tenía guardado
   `www.mabe.com`, que no es el dominio real. Lo busqué y corregí a
   **`mabeglobal.com`** (el sitio oficial verificado del fabricante),
   usado tanto en los datos estructurados para Google (Schema.org)
   como en el enlace visible nuevo.
4. **Nueva sección "Enlaces de interés"**: agregada al pie de página de
   las 913 páginas (los 8 países + el hub), con 2 enlaces externos
   verificados: el sitio oficial de Mabe y el artículo de Wikipedia
   sobre electrodomésticos. Los enlaces externos a fuentes confiables
   ayudan al SEO porque le dan contexto temático a Google sobre de qué
   trata tu página.
5. **Nueva sección "Tecnología"**: se agregó a la página principal de
   cada uno de los 6 tipos de electrodoméstico, en los 8 países (48
   páginas en total). Explica 4 tecnologías reales de cada tipo de
   equipo (ej. en neveras: sistema No Frost, compresor de alta
   eficiencia, control electrónico de temperatura, dispensador con
   filtro) y por qué importan para el diagnóstico.

Solo usé URLs externas que pude confirmar que existen de verdad (no
inventé ninguna): el sitio oficial de Mabe y el artículo de Wikipedia
mencionados arriba.

## Estado de las imágenes

- **Panamá y Costa Rica**: sus fotos reales de cliente ya usadas.
- **Colombia, Ecuador, Guatemala, El Salvador, Paraguay, Chile**: fotos de
  catálogo Mabe genéricas (mismo fabricante y modelos), renombradas por
  país.
- **Las 5 fotos de técnico** que enviaste: aplicadas en la página de
  inicio de los 8 países.
- **Logo**: el mismo logo real "servicio mabe" en los 8 países.

## Pendiente de tu parte

1. Fotos reales de cliente para los 6 países nuevos (opcional).
2. Si tienes los códigos de error reales de algún modelo específico de
   Mabe (del manual del equipo), pásamelos y reemplazo los genéricos por
   los exactos.
3. Confirmar si más adelante quieres números de WhatsApp reales y propios
   por país.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
