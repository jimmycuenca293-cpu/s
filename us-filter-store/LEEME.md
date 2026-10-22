# Tienda de filtros de agua para refrigeradores (EE. UU.)

Sitio estático en inglés, pensado para posicionamiento orgánico. Se sube el contenido de `tienda-eeuu.zip` (carpeta `site/`) a la raíz del hosting del dominio.

## Lo que tienes que completar (en `config.json` y `prices.csv`)
| Dato | Dónde | Estado |
|---|---|---|
| Dominio real | `config.json` → `domain` | Provisional: `https://fridgefilterdepot.com` |
| Nombre de la tienda | `config.json` → `store_name` | Provisional: Fridge Filter Depot |
| **Client ID de PayPal (Live)** | `config.json` → `paypal_client_id` | Vacío: sin él el botón dice «coming soon» |
| **Precios en dólares** | `prices.csv` (`price_usd`, `pack2_usd`) | Vacíos: sin precio, la página manda a WhatsApp |
| Correo de la tienda | `config.json` → `email` | Vacío (no se muestra) |
| Envío (si lo cobras) | `config.json` → `shipping_flat_usd` | 0 |
| Verificación de Search Console | `config.json` → `gsc_verification` | Vacío |
| Google Analytics 4 | `config.json` → `ga4_id` | Vacío |

Cuando cambies datos, hay que volver a generar: `python3 _fuente/build.py` (lo hago yo). Los precios también se pueden ajustar sin regenerar editando `assets/prices.json` en el hosting; el HTML (y los datos para Google) se actualizan al regenerar.

## WhatsApp
+57 301 381 0242 (botón flotante, botones de cada filtro y encabezado). Cada clic envía el evento `whatsapp` a `dataLayer`.

## PayPal
1. Crea una cuenta PayPal Business y verifícala.
2. developer.paypal.com → Apps & Credentials → Live → crea una app y copia el **Client ID**.
3. Pégalo en `config.json` y avísame para regenerar. El botón aparece solo en los filtros que tengan precio.
4. Al pagar, el cliente da su dirección en PayPal y vuelve a `/thank-you/`.

## Páginas (SEO)
- Inicio, 4 marcas, todos/internos/externos, 18 filtros.
- 1 página por número de parte (`/part-numbers/…`) + tabla de equivalencias.
- 1 página por modelo de refrigerador (`/refrigerator-models/…`).
- 20 guías (`/guides/…`), buscador por modelo o número de parte (`/finder/`), preguntas frecuentes, contacto, envíos y devoluciones, privacidad, términos y aviso de marcas.
- `sitemap.xml`, `robots.txt`, `llms.txt`, datos estructurados (Product, FAQ, HowTo, Article, BreadcrumbList, Organization, WebSite).

## Antes de publicar
- Confirma que puedes enviar los filtros desde un depósito en EE. UU. (el sitio lo dice en todas partes).
- Revisa `Shipping & returns`: es un borrador razonable, ajústalo a tu política real.
- No uses «OEM», «genuine» ni «NSF certified» salvo que lo puedas demostrar (facturas del proveedor o certificado).
