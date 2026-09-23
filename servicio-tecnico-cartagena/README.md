# Servicio Técnico Cartagena — sitio reestructurado para SEO orgánico

Novena iteración: se agregaron las fotos reales de **Electrolux**, se quitó
por completo la sección "Equipos que Reparamos" que pediste eliminar, y se
agregó una **sección de palabras clave visible** (no solo en el `<meta>`)
en las 13 plantillas de página del sitio, para reforzar el SEO on-page.

## 1. Se quitó "Equipos que Reparamos"

Quitaste esa sección explícitamente. La eliminé por completo de la página
principal de cada marca. Las fotos de la galería de cada marca (Samsung,
LG, Whirlpool, Mabe) no se perdieron: ahora aparecen como una fila
pequeña de 4 miniaturas dentro de la sección "Especialistas en Reparación
de Neveras {marca}", sin un encabezado H2 propio que compitiera por
atención ni duplicara contenido.

## 2. Electrolux con fotos reales

Agregué las 5 imágenes que enviaste:

- Logo oficial (`logo-electrolux.png`), con el azul marino real de
  Electrolux (`#002964`) tomado directamente del logo.
- Foto principal (hero): la asesora en el Centro de Servicio Oficial
  atendiendo a un cliente en el mostrador.
- Foto de equipo: la asesora de atención al cliente con diadema.
- Galería: la nevera Electrolux en cocina ("Marca europea para vivir
  mejor") y el banner de tecnología AutoSense/Inverter.

Con esto, Electrolux ya está completo (autorizado, con fotos reales) —
solo falta Haceb.

## 3. Sección de palabras clave visible (más SEO real, no solo en meta)

Antes, las palabras clave de cada página solo vivían en la etiqueta
`<meta name="keywords">`, que Google prácticamente ignora para
posicionar. Agregué una sección visible, al final de **las 13 plantillas
de página** (inicio, cada marca, cada sub-página de marca, zonas,
marca+zona, servicios, preguntas frecuentes, blog y la guía de fallas
comunes), titulada **"Servicio Técnico [contexto] Cartagena: Términos
Relacionados"**, mostrando las mismas palabras clave como una nube de
etiquetas visibles y rastreables por buscadores. Esto es contenido real
en el HTML, no solo metadata, así que ayuda de verdad al posicionamiento.

## 4. Organización del sitio — cómo está estructurado

Para que quede claro cómo se organiza todo:

```
index.html                              → Inicio (todas las marcas)
blog.html                                → Índice de las 25 guías del sitio
preguntas-frecuentes.html                → FAQ general
fallas-comunes-neveras-cartagena.html    → Guía pilar de fallas, todas las marcas
servicios/{slug}.html                    → 3 páginas de servicio (independientes de marca)
zonas/{slug}.html                        → 8 páginas de zona (todas las marcas)
marcas/{marca}/index.html                → Página principal de cada marca
marcas/{marca}/fallas-comunes.html       → Fallas comunes de esa marca
marcas/{marca}/mantenimiento-preventivo.html
marcas/{marca}/instalacion-nevecones.html
marcas/{marca}/repuestos-originales.html
marcas/{marca}/preguntas-frecuentes.html
marcas/{marca}/zonas/{slug}.html         → Esa marca + esa zona (8 por marca)
```

Cada página de marca sigue siempre el mismo orden de secciones: hero →
teléfono destacado → quiénes somos (con galería) → cómo solicitar visita
técnica → fallas comunes (resumen) → tarjetas de sub-páginas → artículo
largo → testimonios → preguntas frecuentes → otras marcas/zonas →
palabras clave relacionadas → formulario de contacto. Ese mismo patrón se
repite en las 6 marcas, así que si conoces la estructura de una, conoces
la de todas.

## Estado de las imágenes y autorización por marca

Las 6 marcas están confirmadas como autorizadas. Fotos reales: Samsung,
LG, Whirlpool, Mabe y ahora **Electrolux** completos. Solo falta Haceb —
ver `IMAGENES-LEEME.md`.

## Pendiente de tu parte

1. Enviar las imágenes de Haceb (ya confirmaste que es autorizada, solo
   falta el material).
2. Confirmar el correo de contacto (uso
   `contacto@servicio-tecnico-en-cartagena.com` en todo el sitio).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
