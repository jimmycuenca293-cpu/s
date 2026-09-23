# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Octava iteración: confirmaste que **las 6 marcas son autorizadas**, se
agregaron más fotos de Mabe, se reemplazó la sección genérica de
"Tecnología" por un proceso claro de **"Cómo solicitar visita técnica"**,
se agregó una sección de **teléfono destacado** en cada página de marca,
zona y servicio, se sumó markup **speakable** para asistentes de IA/Google,
y se creó un **Blog** con todas las guías del sitio enlazado desde el menú
y el pie de página de las 99 páginas.

## 1. Las 6 marcas ahora son "Autorizado"

Confirmaste que Samsung, LG, Electrolux, Whirlpool, Mabe y Haceb son todas
autorizadas. Ahora las 6 muestran el sello "&#10003; Autorizado" en el
encabezado de su página y en el logo del header, igual que ya tenía
Samsung.

## 2. Más fotos de Mabe

Agregué las 5 fotos nuevas que enviaste a la galería de Mabe (ahora tiene 7
imágenes): la nevera con tecnología Home Energy Saver, el modelo Side by
Side plateado, la instalación empotrada en cocina integral, y los dos
modelos negro mate con la garantía de 10 años en el compresor.

## 3. Se quitó "Tecnología" y se agregó "Cómo Solicitar una Visita Técnica"

Antes, la sección de galería de cada marca tenía el título "Tecnología
{marca} que Reparamos en Cartagena". Cambié ese título a "Equipos {marca}
que Reparamos en Cartagena" y agregué una sección nueva, completamente
distinta, llamada **"Cómo Solicitar una Visita Técnica {marca} en
Cartagena"**, con 4 pasos claros: 1) escríbanos o llame, 2) agendamos su
visita, 3) diagnóstico en el sitio, 4) reparación con garantía. Esta
sección aparece en las 6 páginas principales de marca.

## 4. Sección de teléfono destacado

Se agregó un bloque grande y visible con el título **"Teléfono Servicio
Técnico {Marca} Cartagena"** y el número +57 321 799 6144 en formato
grande y clickeable, apuntando a `tel:` y a WhatsApp. Aparece en:

- Las 6 páginas principales de marca (con el nombre de la marca).
- La página de inicio.
- Las 8 páginas de zona (Bocagrande, Manga, etc.).
- Las 3 páginas de servicio (mantenimiento, instalación, compresores).
- El blog.

Esto ayuda al posicionamiento de búsquedas como "teléfono servicio técnico
[marca] cartagena", que es justo lo que pediste.

## 5. Secciones pensadas para IA / buscadores con IA (AEO)

Agregué markup `speakable` (schema.org `SpeakableSpecification`) en el
JSON-LD de todas las páginas, apuntando a las secciones de teléfono
destacado y a los acordeones de preguntas frecuentes. Esto es lo que Google
y los asistentes de IA (Google AI Overviews, asistentes de voz) usan para
identificar qué fragmento de la página pueden citar directamente como
respuesta corta. En la práctica: la sección de teléfono destacado y las
preguntas frecuentes de cada página están marcadas como contenido
"citable" para IA.

## 6. Blog nuevo, enlazado desde todas las secciones del sitio

Creé `blog.html`: un índice que agrupa las 25 guías del sitio (fallas
comunes, mantenimiento, instalación y repuestos, tanto generales como por
marca). Agregué el enlace **"Blog"** al menú principal y al pie de página,
así que aparece literalmente en las 99 páginas del sitio, en todas las
secciones (marcas, zonas, servicios, preguntas frecuentes, inicio).

## Estado de las imágenes y autorización por marca

Las 6 marcas están confirmadas como autorizadas. Fotos reales: Samsung, LG,
Whirlpool y Mabe completos. Electrolux y Haceb siguen pendientes de tus
fotos — ver `IMAGENES-LEEME.md`.

## Pendiente de tu parte

1. Enviar las imágenes de Electrolux y Haceb (ya confirmaste que ambas son
   autorizadas, solo faltan las fotos).
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
