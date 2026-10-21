# Tienda de bombas de agua para lavadoras Samsung y LG (un solo dominio)

Dominio: https://bombasparalavadoras.com
- Portada: `/` (elige marca)
- Samsung: `/samsung/` (asesor WhatsApp 305 479 6329)
- LG: `/lg/` (asesor WhatsApp 320 510 2995)

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger agrega el dominio, sube `tienda-bombas.zip` a `public_html` y descomprime.
2. Copia `api/config.sample.php` como `api/config.php` y completa el correo, el titular y el documento. Pon el GTM y la verificación de Search Console de este dominio en `gtm` y `google_verificacion`.
3. Cada clic en un botón de WhatsApp manda el evento `whatsapp` a Tag Manager (marca, página y texto del botón).
4. Agrega `https://bombasparalavadoras.com/sitemap.xml` en Search Console.
5. Fotos: pon la foto real de cada bomba en `imagenes-bombas/<marca>/` y vuelve a generar con `python3 bombas.py https://bombasparalavadoras.com`. Las que falten salen con «Foto próximamente».
6. Precios y referencias: llena `precio` y `ref` en `PRODUCTOS` de `bombas.py`. Mientras no haya precio, la página dice «pregúntale al asesor».
