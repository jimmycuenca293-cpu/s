# Servicio Técnico Mabe Panamá

## Última actualización: logo real, paleta de marca y SEO de torres Mabe

1. **Logo real y paleta de colores**: se reemplazó el logo genérico por el
   logo real que enviaste ("servicio mabe"), en el header, el footer y el
   JSON-LD. Además, toda la paleta de colores del sitio (azules del CSS)
   se recalculó tomando los colores reales del logo (`#20749C` / `#0D3C52`
   / `#051E2A`), en vez de un azul inventado.
2. **Fotos reales para las 3 categorías que faltaban**: lavadoras,
   secadoras y torres/centros de lavado ahora usan las fotos de producto
   reales que enviaste (antes eran marcadores de posición). También se
   agregó una foto adicional de nevera a la galería de neveras.
3. **Mucho más SEO para Torres Mabe** (el equipo que más se daña y más se
   busca reparar, según nos indicaste):
   - La categoría pasó de llamarse "Centros de Lavado" a **"Torres de
     Lavado"**, el término real con el que la gente busca en Panamá,
     reflejado en el título, la descripción, las migas de pan y el menú.
   - Se pasó de 4 a **7 fallas comunes** documentadas (no seca, no
     centrifuga, no enciende tras un apagón, fuga de agua, mal olor,
     puerta trabada, etc.).
   - Se pasó de 3 a **8 preguntas frecuentes**, todas con la frase real de
     búsqueda ("¿por qué mi torre Mabe no seca?", "¿se puede reparar o hay
     que cambiar todo el gabinete?", "¿cuánto cuesta reparar una torre de
     lavado Mabe en Panamá?", etc.).
   - Se agregó una **nube de palabras clave específica de torres** con 12
     términos de búsqueda reales.
   - Se agregó un **artículo de blog nuevo, dedicado 100% a la reparación
     de torres Mabe** ("Torre Mabe no seca, no centrifuga o no enciende:
     guía de reparación en Panamá"), con un síntoma por sección.
   - 3 testimonios (antes 1), 5 repuestos documentados (antes 3).
4. **Nuevas secciones en todas las páginas de inicio y de cada
   electrodoméstico**:
   - "Señales de alerta" — lista de señales tempranas con nivel de
     urgencia (vigilar / pronto / urgente), para que el cliente sepa
     cuándo llamar antes de que la falla se agrave.
   - Nube de palabras clave específica por tipo de electrodoméstico
     (neveras, lavadoras, secadoras, torres), no solo en la página de
     inicio.

## Qué se hizo antes (resumen)

- Diseño visual propio (Manrope + Inter, header con menú desplegable,
  botón de WhatsApp flotante, línea de tiempo, acordeón FAQ).
- Arquitectura de SEO basada en contenido único por página (no páginas
  casi duplicadas): 8 zonas reales de Panamá, 4 tipos de electrodoméstico
  con 6 páginas cada uno, blog con artículos largos.
- JSON-LD: LocalBusiness, Service, FAQPage, BreadcrumbList, Organization,
  WebSite, Article, HowTo.
- Corrección de rutas absolutas → relativas (para que funcione igual en
  el dominio real y en cualquier vista previa).

## Estado de las imágenes

- **Neveras**: fotos reales (incluye una nevera top freezer plateada con
  dispensador, la última que enviaste).
- **Lavadoras**: foto real (lavadora automática negra Mabe, 24 kg).
- **Secadoras**: foto real (secadora Mabe con sensor de humedad).
- **Torres de Lavado**: foto real (torre Mabe gris oscuro).
- **Logo**: el logo real "servicio mabe" que enviaste, usado en todo el
  sitio (header, footer y datos estructurados).
- **Blog**: portadas siguen siendo marcadores de posición por categoría.

## Pendiente de tu parte

1. Si tienes más fotos por electrodoméstico (para la galería de cada uno,
   no solo la foto principal), las voy agregando.
2. Fotos para las portadas del blog, si quieres reemplazar los
   marcadores de posición.
3. Confirmar el correo de contacto (uso
   `contacto@serviciotecnicomabepanama.click`).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
