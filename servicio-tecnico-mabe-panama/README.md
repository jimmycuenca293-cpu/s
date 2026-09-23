# Servicio Técnico Mabe Panamá

## Última actualización: corrección de la foto de Neveras + nuevas secciones de SEO

Se detectó y corrigió un error real: la categoría **Neveras y
Refrigeradores** nunca había mostrado una foto real de nevera, ni en la
página de inicio ni en su propia página — la foto que aparecía ahí era
en realidad la del técnico saludando al cliente (una foto genérica que
sí pertenece al sitio, pero no era una nevera). Se corrigió así:

- La foto del técnico se conservó, pero se movió a un archivo propio
  (`images/nosotros/tecnico-saludo-cliente-panama.jpg`) para usarla solo
  como imagen genérica de portada/confianza, ya no asociada a "Neveras".
- La categoría "Neveras y Refrigeradores" ahora muestra la foto real de
  nevera que enviaste, tanto en la tarjeta de inicio como en su propia
  página de electrodoméstico.
- Se agregaron tres secciones nuevas a la página de inicio, pensadas
  para reforzar el posicionamiento (las mismas que se agregaron en el
  sitio de Costa Rica): **"Por Qué Elegirnos"**, **"Quiénes Somos"** y
  **"Garantía en cada reparación"**. La sección "Qué Reparamos" se
  mantuvo (no se eliminó) porque la razón para quitarla era que las
  fotos no correspondían al equipo real — ese era exactamente el error
  de la foto de nevera, ya corregido en la raíz; quitar la sección
  hubiera sacrificado enlaces internos útiles hacia cada página de
  electrodoméstico sin resolver nada que no se resolviera ya arreglando
  la foto.

## Anterior: herramienta de Diagnóstico Rápido

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

## Nota sobre este control de calidad

Antes de esta entrega se revisó archivo por archivo (con hash, no solo
visualmente) que cada foto real corresponda al electrodoméstico que
dice mostrar, se corrió el validador de HTML/JSON-LD (0 errores reales)
y el verificador de enlaces e imágenes (0 rotos sobre 1390 referencias
en 49 páginas).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
