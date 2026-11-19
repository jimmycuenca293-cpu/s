# Tienda de repuestos de línea blanca: estructura

Nombre de trabajo: **Repuestos de línea blanca** (dominio por definir; sin nombres de marca en la dirección).

## Idea central
Una sola tienda donde el cliente llega por **equipo → marca → pieza → modelo**, y la tienda le dice qué le sirve.
Se crece sumando filas a `catalogo.csv`: cada fila crea sola su página, su lugar en los filtros, el mapa del sitio y los datos de Google.

## Mapa de URLs
- `/` portada: categorías por equipo, piezas más buscadas, buscador por modelo.
- `/lavadoras/` y `/neveras/` (y `/protectores-de-voltaje/`): todas las piezas del equipo, con filtros.
- `/lavadoras/mangueras/`, `/lavadoras/presostatos/`, `/neveras/filtros-de-agua/`… : una página por tipo de pieza.
- `/marca/samsung/`, `/marca/lg/`… : repuestos por marca de electrodoméstico.
- `/producto/<pieza>/`: ficha con foto, precio, compatibilidad, especificaciones, preguntas y datos de producto.
- `/buscar-por-modelo/`: el cliente escribe su modelo y ve las piezas compatibles (solo si hay compatibilidad confirmada).
- Guías por pieza (cómo saber si falla, cómo cambiarla), envíos, pagos, garantía, contacto, términos.
- Carrito, pago con Wompi (un link por producto al comienzo) y contra entrega.

## Reglas para no tener problemas con Google
- Precio, envío y devoluciones de la tienda iguales a los del anuncio y del archivo de productos.
- Sin "original" ni "autorizado" si no es verdad; sin promesas de resultado.
- Compatibilidad solo con modelos confirmados; si no se sabe, se pide el modelo por WhatsApp.
- Cada producto con la marca real del fabricante y foto propia.

## Datos del catálogo (`catalogo.csv`)
`sku, nombre, equipo, categoria, marca_equipo, marca_producto, referencia, modelos_compatibles, precio_venta, costo, envio_gratis, stock, foto, descripcion`
La columna `estado_datos` dice qué falta en cada fila. Una fila sin precio no se publica con precio: manda al asesor.

## Semana de trabajo
1. **Día 1–2:** base multimarca desde el CSV (portada, equipo, categoría, ficha, carrito, pagos, correo y hoja de siempre).
2. **Día 3:** filtros por equipo, marca y pieza, y buscador por modelo.
3. **Día 4:** SEO: páginas de categoría y marca, preguntas, datos de producto, mapa del sitio, `llms.txt`, archivo de productos para Merchant Center.
4. **Día 5:** GTM nuevo, Search Console, pruebas de compra y zips.
5. **Después:** cada semana, más piezas (neveras: sellos, termostatos, ventiladores; lavadoras: válvulas, bombas, correas, amortiguadores).

## Pendiente de confirmar
- Dominio y GTM nuevo.
- Precios de las 11 mangueras/presostatos.
- Línea económica de protectores: marca del fabricante, foto, ficha y precio.
- Precio final de Breakermatic (propuesto 109.900) y del combo de dos.
- Links de pago de Wompi por producto.
