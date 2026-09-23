# Servicio Técnico Mabe Panamá — segunda versión (diseño y arquitectura propios)

Este sitio fue reconstruido desde cero. La primera versión reutilizaba el
CSS y la estructura de páginas del sitio de Cartagena (otro proyecto de
este mismo repositorio) solo cambiando el texto — con justa razón no era
lo que se pidió. Esta versión tiene:

- **Diseño visual propio**: tipografía (Manrope + Inter), paleta azul
  marino + ámbar (no la paleta azul de Cartagena), header con menú
  desplegable, tarjetas con animación al hacer scroll, botón de WhatsApp
  flotante con pulso, barra fija inferior en móvil, línea de tiempo
  "cómo funciona", nube de palabras clave, y acordeón de preguntas
  frecuentes.
- **Arquitectura de SEO más sólida, no solo más páginas**: la primera
  versión generaba 32 páginas casi idénticas (8 zonas × 4 electrodomésticos,
  cambiando solo el nombre de la zona). Eso es exactamente el tipo de
  "contenido delgado" (thin/doorway content) que Google penaliza en vez de
  premiar. Esta versión tiene **8 páginas de zona** (una por cada zona real
  de Ciudad de Panamá, con contenido único sobre el tipo de edificios,
  acceso y tiempos de esa zona específica) y **24 páginas por tipo de
  electrodoméstico** (resumen, fallas comunes, mantenimiento, instalación,
  repuestos y preguntas frecuentes × 4 tipos), cada una con contenido
  realmente distinto, no plantillas con una palabra cambiada.
- **Blog con artículos largos y propios** (6 artículos de 700-900 palabras
  sobre temas específicos de Panamá: voltaje y apagones, clima húmedo,
  reparar vs. reemplazar, centros de lavado para apartamentos pequeños),
  no páginas de relleno.
- **SEO técnico ampliado**: además de JSON-LD `LocalBusiness`, `Service` y
  `FAQPage`, se agregó `Organization`, `WebSite`, `Article` en el blog,
  `HowTo` en las páginas de mantenimiento e instalación (contenido basado
  en pasos), etiquetas `hreflang` para español de Panamá, y meta
  `geo.region`/`geo.placename`.
- **46 páginas en total**, todas validadas: HTML balanceado, JSON-LD sin
  errores de sintaxis, 0 enlaces o imágenes rotas, sin salto de scroll al
  navegar.

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
