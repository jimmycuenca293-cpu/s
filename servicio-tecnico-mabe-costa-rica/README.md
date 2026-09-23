# Servicio Técnico Mabe Costa Rica

Sitio nuevo, construido reutilizando la arquitectura y el diseño ya
validados en el proyecto de Panamá, pero con contenido, cantones,
electrodomésticos y volumen de SEO propios de Costa Rica — no es una
copia con el nombre del país cambiado.

- **Dominio**: https://serviciotecnicomabecostarica.click/
- **WhatsApp / teléfono**: +506 7005-5853
- **63 páginas** generadas y validadas (0 errores de HTML, 0 errores de
  JSON-LD, 0 enlaces/imágenes rotas, sin salto de scroll).

## Correcciones aplicadas en esta entrega

1. **Terminología costarricense real**: en Costa Rica no se dice
   "nevera", se dice **"refrigeradora"**. La categoría se llamaba
   "Neveras y Refrigeradores" (copiada de Panamá) y usaba "nevera" como
   término principal en más de 50 lugares del sitio (nav, inicio, la
   página del tipo de electrodoméstico, FAQ, blog). Se corrigió el
   vocabulario en todo el sitio para que el término principal sea
   "Refrigeradora" (se dejó una sola mención de "nevera" como palabra
   clave secundaria, porque también se busca así).
2. **La categoría de Refrigeradoras nunca mostraba una foto real de
   refrigeradora** — el mismo error existía en el sitio de Panamá: la
   foto que aparecía ahí (en inicio y en la página del tipo) era en
   realidad la del técnico saludando al cliente. Se corrigió: esa foto
   se conservó pero se movió a un archivo propio
   (`images/nosotros/tecnico-saludo-cliente-costarica.jpg`) para usarla
   solo como imagen genérica de portada, y la categoría Refrigeradoras
   ahora muestra la foto real de refrigeradora que enviaste.
3. **Foto de Hornos agregada**: ya se aplicó la foto real del horno
   empotrado Mabe que enviaste, tanto en la tarjeta de inicio como en
   la página de Hornos y en el artículo de blog correspondiente.
4. **Tres secciones nuevas en la página de inicio**, pensadas para
   reforzar el posicionamiento en Costa Rica: **"Por Qué Elegirnos"**,
   **"Quiénes Somos"** y **"Garantía en cada reparación"**. La sección
   "Qué Reparamos" se mantuvo (no se eliminó) porque la razón para
   quitarla era que las fotos no correspondían al equipo real — ese
   era el error del punto 2, ya corregido en la raíz; quitar la sección
   hubiera sacrificado enlaces internos útiles hacia cada página de
   electrodoméstico sin resolver nada que no se resolviera ya
   arreglando la foto.

### Nota técnica (control de calidad)

Al procesar las dos fotos nuevas que enviaste (refrigeradora y horno)
se detectó que en un paso intermedio quedaron intercambiadas —la foto
de horno se había guardado como refrigeradora y viceversa—, el mismo
tipo de error de fondo que motivó esta ronda de correcciones. Se
detectó por hash antes de la entrega y se corrigió en ambos sitios
(Panamá también usa la foto de refrigeradora). Ambas fotos ya están
verificadas visualmente en su lugar correcto.

## Qué tiene de más respecto al sitio de Panamá (a propósito)

1. **6 tipos de electrodomésticos en vez de 4**: se agregaron **Cocinas**
   y **Hornos** (con contenido propio de gas: qué hacer si huele a gas,
   llama amarilla, fugas), además de Refrigeradoras, Lavadoras, Secadoras y
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

- **Refrigeradoras, Lavadoras, Secadoras, Torres de Lavado**: foto real
  de refrigeradora que enviaste, más fotos reales de producto Mabe para
  las demás (es el mismo fabricante y los mismos modelos que se venden
  en ambos países, así que reutilizarlas es legítimo).
- **Cocinas**: foto real que enviaste (cocina de gas Mabe con horno).
- **Hornos**: foto real que enviaste (horno empotrado Mabe), ya
  aplicada en inicio, en la página de Hornos y en el blog.
- **Logo y paleta de colores**: el mismo logo real "servicio mabe" y la
  misma paleta azul-teal + naranja que en Panamá (es la misma marca).

## Pendiente de tu parte

1. Fotos adicionales para las galerías de cualquier tipo, si tienes más
   de una foto.
2. Confirmar el correo de contacto (uso
   `contacto@serviciotecnicomabecostarica.click`).

## Nota sobre este control de calidad

Antes de esta entrega se revisó archivo por archivo (con hash, no solo
visualmente) que cada foto real corresponda al electrodoméstico que
dice mostrar, se corrió el validador de HTML/JSON-LD (0 errores reales)
y el verificador de enlaces e imágenes (0 rotos sobre 1944 referencias
en 63 páginas).

## Cómo previsualizarlo

Desde esta carpeta:

```bash
python3 -m http.server 8080
```

y abre `http://localhost:8080/index.html`.
