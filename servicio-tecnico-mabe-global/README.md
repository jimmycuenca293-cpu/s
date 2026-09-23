# Servicio Técnico Mabe Global

Sitio raíz para **centrodeserviciotecnicomabe.com**: un hub que conecta 8
sitios de país, cada uno con su propia arquitectura completa (igual a la ya
validada en Panamá y Costa Rica), pero con vocabulario, ciudades, número de
WhatsApp y contenido genuinamente propios por país.

- **8 países**: Panamá, Costa Rica, Colombia, Ecuador, Guatemala, El
  Salvador, Paraguay y Chile.
- **482 páginas** generadas y validadas (0 errores reales de HTML/JSON-LD,
  0 enlaces o imágenes rotos, sin placeholders sin resolver).
- **41 ciudades y zonas** con página propia, cada una con su propio título
  SEO (`Servicio Técnico Mabe en {Ciudad}, {País}`), meta descripción y
  JSON-LD `LocalBusiness`.
- **Barrios y sectores reales** listados en cada una de las 41 páginas de
  ciudad (sección "Cobertura"), con nube de palabras clave propia por
  ciudad y un párrafo adicional de texto orientado a búsqueda.
- **Nuevas secciones con fotos** en la página de inicio de cada país: "Así
  es una visita de Servicio Técnico Mabe" (3 fotos, paso a paso) y "Nuestro
  Estándar" (centro de reparación autorizado).

## Estructura

```
index.html                  Hub global: elige tu país
{pais}/index.html            Página de inicio de cada país (hero, por qué
                              elegirnos, cómo trabajamos con fotos, quiénes
                              somos, nuestro estándar, garantía, blog, FAQ)
{pais}/zonas-de-cobertura.html   Índice de ciudades/zonas del país
{pais}/zonas/{ciudad}.html   Página propia por ciudad: detalle, barrios que
                              cubrimos, señales de alerta, nube de palabras
                              clave local
{pais}/electrodomesticos/{tipo}/  6 tipos × 6 páginas cada uno (igual en
                              los 8 países): index (con enlaces a cada
                              ciudad), fallas-comunes, mantenimiento,
                              instalacion, repuestos, FAQ
{pais}/blog/                 9 artículos por país (localizados)
{pais}/diagnostico.html      Herramienta de diagnóstico rápido
{pais}/nosotros.html, garantia.html, preguntas-frecuentes.html, servicios/
```

Países y sus carpetas: `panama/`, `costarica/`, `colombia/`, `ecuador/`,
`guatemala/`, `el-salvador/`, `paraguay/`, `chile/`.

## Decisiones de contenido (para que sepas qué esperar)

1. **Ciudades por país** (las que definiste): Panamá (8 zonas ya
   construidas), Costa Rica (8 cantones ya construidos), Colombia
   (Medellín, Cali, Bucaramanga, Cartagena, Ibagué, Barranquilla,
   Valledupar, Manizales, Bogotá, Cúcuta, Pereira), Ecuador (Guayaquil,
   Quito, Cuenca), Guatemala (solo la capital), El Salvador (solo la
   capital), Paraguay (solo Asunción), Chile (8 comunas de Santiago).
2. **Barrios dentro de cada ciudad**: cada página de ciudad ahora incluye
   una sección "Barrios y sectores que cubrimos" con 3 a 5 barrios reales
   (por ejemplo, en Medellín: El Poblado, Laureles, Belén, La América,
   Envigado). Es contenido dentro de la misma página, no una página nueva
   por barrio — así se evita duplicar miles de páginas casi idénticas
   mientras se sigue reforzando el SEO local.
3. **Profundidad por ciudad**: una página completa por ciudad (no el árbol
   completo de 6 páginas × 6 electrodomésticos repetido en cada una). El
   detalle profundo por electrodoméstico vive a nivel país, con enlaces
   directos desde ahí a cada ciudad.
4. **Vocabulario por país**: nevera (Panamá/Colombia), refrigeradora
   (Costa Rica/Ecuador/Guatemala/El Salvador), heladera (Paraguay),
   refrigerador masculino (Chile, con toda la gramática ajustada).
5. **Teléfonos**: exactamente los que diste, incluida la reutilización a
   propósito del mismo número en varios países.
6. **6 tipos de electrodomésticos en los 8 países**, con enlaces cruzados
   entre cada tipo y cada ciudad del país (por ejemplo, la página de
   Neveras de Colombia enlaza a Medellín, Cali, Bogotá, etc.).
7. **hreflang real entre países** bajo un mismo dominio.

## Fotos nuevas que enviaste

Las 5 fotos de "técnico Mabe" que enviaste se aplicaron en la página de
inicio de los 8 países, en dos secciones nuevas:
- **"Así es una visita de Servicio Técnico Mabe"**: llegada al domicilio,
  diagnóstico explicado, reparación con garantía (3 fotos).
- **"Nuestro Estándar"**: la foto del centro de reparación autorizado,
  presentada como el estándar de organización que seguimos en cada visita
  a domicilio (no como una tienda física en cada ciudad, para no prometer
  algo que no es cierto).

## Estado de las demás imágenes

- **Panamá y Costa Rica**: sus fotos reales de cliente ya usadas.
- **Colombia, Ecuador, Guatemala, El Salvador, Paraguay, Chile**: fotos de
  catálogo Mabe genéricas (mismo fabricante y modelos), renombradas por
  país. Cuando tengas fotos propias de cada país, dime y las reemplazo.
- **Logo**: el mismo logo real "servicio mabe" en los 8 países.

## Pendiente de tu parte

1. Fotos reales de cliente para los 6 países nuevos (opcional).
2. Confirmar si más adelante quieres números de WhatsApp reales y propios
   por país.
3. Si tienes zonas específicas dentro de Colombia/Ecuador que quieras
   destacar además de las ya incluidas, dímelo.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
