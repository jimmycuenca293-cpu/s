# Servicio Técnico Mabe Panamá

## Última actualización: herramienta de Diagnóstico Rápido (nueva)

Nueva página **`/diagnostico.html`** — "Diagnóstico Rápido: ¿Qué le Pasa
a tu Electrodoméstico Mabe?":

- Reúne las **19 fallas comunes** documentadas en las 4 páginas de
  electrodoméstico (neveras, lavadoras, secadoras, torres de lavado) en
  una sola herramienta, con síntoma, causa probable y nivel de urgencia
  (Vigilar / Revisar pronto / Urgente).
- **Filtro interactivo** por tipo de electrodoméstico (pestañas), hecho
  en JavaScript puro — pero todo el contenido está en el HTML desde el
  inicio (no oculto detrás de JS), así que es 100% indexable por Google
  aunque el filtro no funcione.
- Cada falla tiene su propio botón de WhatsApp que abre un mensaje **ya
  redactado con esa falla específica** (mejora la conversión: el cliente
  no tiene que explicar el problema desde cero).
- Enlaza de vuelta a la página completa de fallas de cada
  electrodoméstico (refuerza el enlazado interno).
- JSON-LD `ItemList` con las 19 fallas para SEO estructurado.
- Enlazada desde el menú principal, el menú móvil, el pie de página, y
  una sección promocional nueva en la página de inicio.

Por qué esta herramienta y no otra sección más de texto: es la primera
pieza interactiva real del sitio (no solo contenido estático), agrupa
en una sola URL todas las búsquedas tipo "qué le pasa a mi [equipo]
mabe [síntoma]" en vez de tenerlas repartidas en 4 páginas distintas, y
da un motivo concreto para que alguien use el sitio antes de decidirse
a escribir por WhatsApp.

## Resumen de todo lo hecho hasta ahora

1. Diseño visual propio (Manrope + Inter, paleta tomada del logo real,
   naranja de marca en vez de amarillo).
2. Arquitectura de SEO basada en contenido único (no páginas
   duplicadas): 8 zonas reales, 4 tipos de electrodoméstico × 6 páginas,
   blog con artículos largos, SEO reforzado especialmente en Torres de
   Lavado.
3. Rutas relativas (funciona igual en el dominio real y en cualquier
   vista previa).
4. Fotos reales del cliente en neveras, lavadoras, secadoras, torres,
   blog, Nosotros y Garantía — mostradas completas, sin recortar.
5. Página de Garantía, sección de WhatsApp destacada, y ahora la
   herramienta de Diagnóstico Rápido.

## Pendiente de tu parte

1. Fotos adicionales para galerías (si tienes más de una foto por tipo).
2. Confirmar el correo de contacto
   (`contacto@serviciotecnicomabepanama.click`).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
