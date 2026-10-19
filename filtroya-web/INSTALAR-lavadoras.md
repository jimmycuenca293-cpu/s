# Tienda de filtros para lavadoras Samsung y LG (un solo dominio)

Dominio: https://filtrosparalavadoras.click
- Portada: `/` (elige marca)
- Samsung: `/samsung/` (asesor WhatsApp 305 479 6329)
- LG: `/lg/` (asesor WhatsApp 320 510 2995)

Esta tienda no tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor.

1. En Hostinger agrega el dominio, sube `tienda-lavadoras.zip` a `public_html` y descomprime.
2. Copia `api/config.sample.php` como `api/config.php` y completa el correo, el titular y el documento. El GTM (GTM-5SCP73SQ) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el evento `whatsapp` a Tag Manager (con la marca, la página y el texto del botón).
4. Agrega `https://filtrosparalavadoras.click/sitemap.xml` en Search Console.
5. Precios: mientras un filtro no tenga precio, su página dice «pregúntale al asesor».
