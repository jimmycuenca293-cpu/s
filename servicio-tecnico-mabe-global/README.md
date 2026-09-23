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

- **Fotos reales** (las que enviaste): Ecuador, Chile, Colombia, Costa Rica
  y Panamá.
- **Simplificadas** (no tenía foto real de esa bandera, así que generé una
  versión plana con los colores oficiales en vez de inventar una foto):
  Guatemala, El Salvador y Paraguay. Si me pasas la foto real de estas 3,
  las reemplazo directo.

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
