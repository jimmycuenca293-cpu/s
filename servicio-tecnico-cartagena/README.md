# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Decimotercera iteración: **la página de inicio ya tiene fotos reales** —
era la última página del sitio que seguía con imágenes de placeholder.
Con esto, las 99 páginas del sitio usan fotos reales o contenido 100%
específico, sin genéricos automáticos pendientes.

## Página de inicio con fotos reales

Agregué las 5 imágenes que enviaste:

- **Hero** (portada): nevera abierta mostrando el interior organizado con
  panel digital.
- **Quiénes somos**: persona revisando el contenido de la nevera desde el
  celular.
- **Por qué elegirnos**: nevera abierta de perfil, plano dramático.
- **Nuestros servicios**: primer plano del panel digital y dispensador.
- **Reseñas de clientes**: nevera instalada en un comedor moderno.

Como en las páginas de marca, cada foto está junto a su sección
correspondiente, no agrupadas.

## SEO: lo que ya está y lo que falta para el primer lugar en Cartagena

Preguntaste qué le falta al sitio para posicionar en el primer lugar en
Cartagena por marca. Esto es lo que ya está construido y lo que depende
de ti a partir de ahora:

### Lo que ya está resuelto en el sitio (on-page)

1. **Estructura completa de silos**: home → marca → zona → servicio, con
   99 páginas interconectadas, cada una con su propio título, meta
   descripción, palabras clave y URL canónica.
2. **Datos estructurados (JSON-LD)**: `LocalBusiness`, `Service`,
   `FAQPage`, `BreadcrumbList` y `SpeakableSpecification` en todas las
   páginas, para que Google entienda el negocio, el servicio y pueda
   citar fragmentos en respuestas de IA.
3. **Contenido único por marca y por zona**: fallas, tips de
   mantenimiento, modelos, testimonios y preguntas frecuentes distintos
   para cada una de las 6 marcas y las 8 zonas — nada duplicado.
4. **Fotos reales con `alt` descriptivo** en las 99 páginas, con nombres
   de archivo también optimizados (`hero-samsung-cartagena.jpg`, etc.).
5. **Google Search Console** ya verificado (meta tag instalado desde la
   primera iteración).
6. **robots.txt y sitemap.xml** generados y actualizados automáticamente.
7. **Velocidad**: CSS propio sin frameworks pesados, imágenes
   comprimidas, sin JavaScript innecesario.

### Lo que depende de ti (off-page — esto es lo que más pesa para el "primer lugar")

El contenido on-page ya está al nivel que puede sostener el primer lugar,
pero **Google posiciona sobre todo por señales externas al sitio**, que
ningún código puede generar por sí solo:

1. **Perfil de Negocio de Google (Google Business Profile)**: es lo más
   importante para aparecer en el mapa y en el "paquete de 3 locales" de
   Cartagena. Si no lo tienes, créalo ya en
   business.google.com con el nombre, dirección de referencia, teléfono
   +57 321 799 6144, categoría "Servicio de reparación de
   electrodomésticos" y el link a tu sitio. Pide reseñas reales a cada
   cliente después de cada servicio — esto es lo que más mueve la aguja.
2. **Reseñas reales de Google** (no solo los testimonios de la página):
   apunta a conseguir al menos 20-30 reseñas de 5 estrellas en los
   primeros meses, mencionando la marca de la nevera cuando sea posible
   ("reparó mi nevera Samsung en Bocagrande").
3. **Backlinks locales**: que otros sitios de Cartagena te enlacen —
   directorios locales, páginas de barrio/administración de edificios,
   grupos de Facebook de la ciudad, o alianzas con ferreterías/almacenes
   de electrodomésticos que te recomienden.
4. **Consistencia NAP** (Name, Address, Phone): que tu nombre, dirección
   y teléfono aparezcan exactamente igual en Google Business, redes
   sociales, directorios y el sitio web. Cualquier inconsistencia le
   resta confianza a Google.
5. **Actividad constante**: publicar en redes sociales (Instagram,
   Facebook) con el mismo enlace al sitio, y mantener el Perfil de Google
   activo con fotos y publicaciones nuevas cada mes.
6. **Tiempo**: un sitio nuevo, sin importar qué tan bien esté construido,
   normalmente tarda de 3 a 6 meses en escalar posiciones en Google para
   términos competidos como "servicio técnico [marca] cartagena". Los
   términos con menos competencia (zonas específicas, marca+zona) suelen
   posicionar más rápido.

En resumen: el sitio ya tiene todo el trabajo técnico y de contenido que
se puede hacer desde el código. Lo que queda es trabajo tuyo, fuera del
sitio: Google Business Profile, reseñas reales y presencia constante en
Cartagena. Si quieres, en la próxima iteración puedo ayudarte a redactar
la descripción y las publicaciones para tu Perfil de Google Business.

## Pendiente de tu parte

1. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).
2. Crear/optimizar tu Perfil de Negocio de Google (ver arriba).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
