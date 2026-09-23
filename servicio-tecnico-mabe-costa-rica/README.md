# Servicio Técnico Mabe Costa Rica

Sitio nuevo, construido reutilizando la arquitectura y el diseño ya
validados en el proyecto de Panamá, pero con contenido, cantones,
electrodomésticos y volumen de SEO propios de Costa Rica — no es una
copia con el nombre del país cambiado.

- **Dominio**: https://serviciotecnicomabecostarica.click/
- **WhatsApp / teléfono**: +506 7005-5853
- **63 páginas** generadas y validadas (0 errores de HTML, 0 errores de
  JSON-LD, 0 enlaces/imágenes rotas, sin salto de scroll).

## Corrección aplicada antes de esta entrega

Al reutilizar las fotos reales de Panamá para neveras, lavadoras,
secadoras y torres de lavado, los archivos seguían nombrados
`*-panama.jpg` mientras el código generaba nombres `*-costarica.jpg`.
Eso hacía que el sitio mostrara marcadores de posición en vez de las
fotos reales, aunque los archivos sí estaban copiados. Se renombraron
todos los archivos para que coincidan, y se verificó visualmente que
las fotos reales ya aparecen en inicio y en cada página de
electrodoméstico.

## Qué tiene de más respecto al sitio de Panamá (a propósito)

1. **6 tipos de electrodomésticos en vez de 4**: se agregaron **Cocinas**
   y **Hornos** (con contenido propio de gas: qué hacer si huele a gas,
   llama amarilla, fugas), además de Neveras, Lavadoras, Secadoras y
   Torres de Lavado. Eso son 36 páginas de electrodoméstico (6 tipos × 6
   páginas cada uno) en vez de las 24 de Panamá.
2. **9 artículos de blog** en vez de 7, incluyendo dos artículos nuevos
   específicos: "Mi cocina Mabe huele a gas: qué hacer" y "Horno Mabe no
   calienta o cocina desparejo".
3. **30 fallas documentadas** en la herramienta de Diagnóstico Rápido (en
   vez de 19), con pestañas para los 6 tipos de electrodoméstico.
4. **Cantones reales del Gran Área Metropolitana** (no una copia de las
   zonas de Panamá): San José Centro, Escazú, Santa Ana, Curridabat,
   Heredia, Alajuela, Cartago y Desamparados — cada uno con
   características reales y distintas (clima, tipo de vivienda, acceso).
5. **Lenguaje costarricense real**: "época lluviosa" (mayo–noviembre) en
   vez de "clima húmedo" genérico, referencia al ICE para los cortes de
   luz, "costarricense" como gentilicio, "refrigeradora" junto a "nevera",
   y contenido de seguridad específico para cocinas de gas (algo que
   Panamá no tenía porque ese sitio no incluye cocinas).
6. Mismas herramientas que Panamá pero ampliadas: página de Garantía,
   sección de WhatsApp destacada, "Señales de Alerta", nube de palabras
   clave por tipo — aplicadas ahora a 6 tipos en vez de 4.

## Estructura del sitio

```
index.html                        Inicio
nosotros.html                     Sobre el servicio técnico
garantia.html                     Página de garantía
diagnostico.html                  Herramienta: 30 fallas filtrables por tipo
zonas-de-cobertura.html           Índice de los 8 cantones
zonas/{canton}.html               8 páginas de cantón (contenido único c/u)
preguntas-frecuentes.html         FAQ general (11 preguntas)
blog/index.html + 9 artículos     Blog con guías largas, 2 nuevas de cocinas/hornos
servicios/*.html                  3 servicios genéricos
electrodomesticos/{tipo}/         6 tipos × 6 páginas cada uno:
  index.html, fallas-comunes.html, mantenimiento.html,
  instalacion.html, repuestos.html, preguntas-frecuentes.html
```

## Estado de las imágenes

- **Neveras, Lavadoras, Secadoras, Torres de Lavado**: mismas fotos
  reales de producto Mabe que en el sitio de Panamá (es el mismo
  fabricante y los mismos modelos que se venden en ambos países, así que
  reutilizar las fotos es legítimo).
- **Cocinas**: foto real que enviaste (cocina de gas Mabe con horno).
- **Hornos**: todavía en marcador de posición — la foto que enviaste es
  de una cocina completa (no un horno empotrado independiente), así que
  preferí no reutilizarla para no mostrar el producto equivocado. Envía
  una foto de horno cuando puedas.
- **Logo y paleta de colores**: el mismo logo real "servicio mabe" y la
  misma paleta azul-teal + naranja que en Panamá (es la misma marca).

## Pendiente de tu parte

1. Foto de horno (empotrado o de cocina) para la categoría de Hornos.
2. Fotos adicionales para las galerías de cualquier tipo, si tienes más
   de una foto.
3. Confirmar el correo de contacto (uso
   `contacto@serviciotecnicomabecostarica.click`).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
