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
  JSON-LD `LocalBusiness` — no una plantilla genérica con el nombre pegado.

## Estructura

```
index.html                  Hub global: elige tu país
{pais}/index.html            Página de inicio de cada país (hero, por qué
                              elegirnos, quiénes somos, garantía, blog, FAQ)
{pais}/zonas-de-cobertura.html   Índice de ciudades/zonas del país
{pais}/zonas/{ciudad}.html   Página propia por ciudad (título y contenido únicos)
{pais}/electrodomesticos/{tipo}/  6 tipos × 6 páginas cada uno (igual en
                              los 8 países): index, fallas-comunes,
                              mantenimiento, instalacion, repuestos, FAQ
{pais}/blog/                 9 artículos por país (localizados)
{pais}/diagnostico.html      Herramienta de diagnóstico rápido (fallas
                              filtrables de los 6 tipos)
{pais}/nosotros.html, garantia.html, preguntas-frecuentes.html, servicios/
```

Países y sus carpetas: `panama/`, `costarica/`, `colombia/`, `ecuador/`,
`guatemala/`, `el-salvador/`, `paraguay/`, `chile/`.

## Decisiones de contenido (para que sepas qué esperar)

1. **Ciudades por país** (las que definiste):
   - Panamá: las 8 zonas ya construidas (San Francisco, Bella Vista, etc.)
   - Costa Rica: los 8 cantones ya construidos (San José Centro, Escazú, etc.)
   - Colombia: Medellín, Cali, Bucaramanga, Cartagena, Ibagué, Barranquilla,
     Valledupar, Manizales, Bogotá, Cúcuta, Pereira (11 ciudades)
   - Ecuador: Guayaquil, Quito, Cuenca
   - Guatemala: solo Ciudad de Guatemala (la capital)
   - El Salvador: solo San Salvador (la capital)
   - Paraguay: solo Asunción (la capital)
   - Chile: 8 comunas de Santiago (Santiago Centro, Providencia, Las Condes,
     Ñuñoa, La Florida, Maipú, Puente Alto, Vitacura)
2. **Profundidad por ciudad**: cada ciudad tiene **una página completa**
   (hero propio, por qué elegirnos, los 6 electrodomésticos en tarjetas,
   testimonios, FAQ) con título y meta descripción únicos. El detalle
   profundo por electrodoméstico (fallas comunes, mantenimiento,
   instalación, repuestos) vive a nivel país, no repetido 41 veces —
   evita duplicar miles de páginas casi idénticas y sigue dando SEO local
   fuerte por ciudad.
3. **Vocabulario por país** (la marca lo pide, ya lo veníamos haciendo):
   - Panamá, Colombia: **nevera**
   - Costa Rica, Ecuador, Guatemala, El Salvador: **refrigeradora**
   - Paraguay: **heladera** (como se dice en la región del Río de la Plata)
   - Chile: **refrigerador** (masculino — toda la gramática del sitio de
     Chile está ajustada: "el refrigerador", "un refrigerador", "los
     refrigeradores")
4. **Teléfonos**: exactamente los que diste, incluida la reutilización a
   propósito del mismo número en varios países (Panamá/Guatemala/El
   Salvador comparten uno; Ecuador/Paraguay comparten otro).
5. **6 tipos de electrodomésticos en los 8 países** (neveras/refrigeradoras,
   lavadoras, secadoras, torres de lavado, cocinas, hornos) — le di a todos
   los países el catálogo más completo que ya teníamos en Costa Rica, para
   maximizar el SEO en todos lados por igual.
6. **hreflang real entre países**: al estar todo bajo un mismo dominio
   (`centrodeserviciotecnicomabe.com/{pais}/`), la página de inicio de cada
   país enlaza correctamente por `hreflang` a las de los otros 7 países y al
   hub — esto es SEO internacional hecho como corresponde, algo que no era
   posible cuando Panamá y Costa Rica vivían en dominios separados.

## Estado de las imágenes

- **Panamá y Costa Rica**: sus fotos reales de cliente ya usadas (no se
  tocaron).
- **Colombia, Ecuador, Guatemala, El Salvador, Paraguay, Chile**: fotos de
  catálogo Mabe genéricas (las mismas que ya usábamos, es el mismo
  fabricante y modelos), renombradas por país. Ninguna se presenta como
  "foto real de un cliente de X país" — cuando tengas fotos propias de
  cada país, dime y las reemplazo con el mismo criterio que ya usamos en
  Panamá/Costa Rica.
- **Logo**: el mismo logo real "servicio mabe" en los 8 países (misma
  marca).

## Pendiente de tu parte

1. Fotos reales de cliente para Colombia, Ecuador, Guatemala, El Salvador,
   Paraguay y Chile (opcional — el sitio funciona bien con las fotos de
   catálogo mientras tanto).
2. Confirmar si quieres números de WhatsApp reales y propios para cada país
   más adelante (dijiste que sabías que no eran los reales de cada país y
   que lo dejáramos así por ahora).
3. Revisar el listado de ciudades de Colombia/Ecuador — si tienes zonas
   específicas dentro de cada ciudad (no solo la ciudad completa) que
   quieras destacar, dímelo y las agrego como páginas adicionales.

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
