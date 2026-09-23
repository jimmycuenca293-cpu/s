# Servicio Técnico Mabe Panamá — diseño y arquitectura propios

Este sitio fue reconstruido desde cero (ver historial de commits): la
primera versión reutilizaba el CSS y la estructura de páginas del sitio de
Cartagena solo cambiando el texto, y la segunda versión (esta) tiene diseño
visual propio y una arquitectura de SEO más sólida.

## Corrección importante: rutas relativas

Después de publicar la segunda versión, al abrirla en la vista previa del
Artifact se veía sin estilos ni imágenes. La causa: el sitio usaba rutas
"absolutas desde la raíz" (`/css/estilos.css`, `/images/...`,
`/electrodomesticos/...`). Esas rutas funcionan perfecto cuando el sitio
vive en la raíz de `serviciotecnicomabepanama.click`, pero se rompen en
cualquier vista previa que lo sirva desde una subcarpeta (como el Artifact
de Claude). Se corrigió todo el generador para usar **rutas relativas**
(`./css/...`, `../images/...`, etc., según la profundidad de cada página),
que funcionan igual de bien en el dominio real y en cualquier previsualización.
Se validó sirviendo el sitio completo desde una subcarpeta simulada: 0
enlaces o imágenes rotas.

## Qué incluye

- **Diseño visual propio**: tipografía (Manrope + Inter), paleta azul
  marino + ámbar, header con menú desplegable, tarjetas con animación al
  hacer scroll, botón de WhatsApp flotante con pulso, barra fija inferior
  en móvil, línea de tiempo "cómo funciona", nube de palabras clave, y
  acordeón de preguntas frecuentes.
- **Arquitectura de SEO más sólida, no solo más páginas**: 8 páginas de
  zona (una por cada zona real de Ciudad de Panamá, con contenido único
  sobre el tipo de edificios, acceso y tiempos de esa zona específica) y
  24 páginas por tipo de electrodoméstico (resumen, fallas comunes,
  mantenimiento, instalación, repuestos y preguntas frecuentes × 4 tipos),
  en vez de páginas casi duplicadas cambiando solo un nombre.
- **Blog con 6 artículos largos y propios** (700-900 palabras) sobre temas
  específicos de Panamá: voltaje y apagones, clima húmedo, reparar vs.
  reemplazar, centros de lavado para apartamentos pequeños.
- **SEO técnico ampliado**: JSON-LD `LocalBusiness`, `Service`, `FAQPage`,
  `BreadcrumbList`, `Organization`, `WebSite`, `Article` (blog) y `HowTo`
  (mantenimiento e instalación), `hreflang` es-PA, meta `geo.region`.
- **46 páginas en total**, validadas: HTML balanceado, JSON-LD sin
  errores, 0 enlaces o imágenes rotas (probado también desde una
  subcarpeta), sin salto de scroll al navegar.

## Estructura del sitio

```
index.html                        Inicio
nosotros.html                     Sobre el servicio técnico
zonas-de-cobertura.html           Índice de las 8 zonas
zonas/{zona}.html                 8 páginas de zona (contenido único c/u)
preguntas-frecuentes.html         FAQ general
blog/index.html + 6 artículos     Blog con guías largas
servicios/*.html                  3 servicios genéricos
electrodomesticos/{tipo}/         4 tipos × 6 páginas cada uno:
  index.html                        resumen
  fallas-comunes.html               tabla de fallas + detalle
  mantenimiento.html                rutina de mantenimiento (HowTo)
  instalacion.html                  buenas prácticas de instalación (HowTo)
  repuestos.html                    piezas más reemplazadas
  preguntas-frecuentes.html         FAQ propia del tipo
```

## Estado de las imágenes

- **Neveras**: fotos reales del equipo (las que ya enviaste, reutilizadas
  porque es la misma marca/producto).
- **Lavadoras, Secadoras, Centros de Lavado**: imágenes de marcador de
  posición (placeholder) con el color de marca, a la espera de las fotos
  que vas a enviar.
- **Blog**: portadas de marcador de posición por categoría.
- El logo del sitio (`images/logo/logo.svg`) es un ícono propio generado
  para este negocio, no el logo oficial de Mabe — así evitamos dar a
  entender una afiliación oficial con la marca que no has confirmado.

## Pendiente de tu parte

1. Fotos de lavadoras, secadoras y centros de lavado.
2. Fotos para las portadas del blog (o las genero con las mismas fotos de
   producto si prefieres no enviar fotos nuevas para esto).
3. Confirmar el correo de contacto (uso
   `contacto@serviciotecnicomabepanama.click`).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
