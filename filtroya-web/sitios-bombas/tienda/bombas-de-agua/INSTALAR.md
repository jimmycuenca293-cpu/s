# Bombas de agua para lavadoras Samsung y LG, dentro de https://filtrosparalavadoras.click

Todo vive en la carpeta `bombas-de-agua/`, así que no pisa nada de la tienda de filtros (`/samsung/`, `/lg/`, `api/`, `.htaccess`, etc.).

- Portada: https://filtrosparalavadoras.click/bombas-de-agua/ (elige marca)
- Samsung: https://filtrosparalavadoras.click/bombas-de-agua/samsung/ (asesor WhatsApp 305 479 6329)
- LG: https://filtrosparalavadoras.click/bombas-de-agua/lg/ (asesor WhatsApp 320 510 2995)

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger abre el administrador de archivos del dominio filtrosparalavadoras.click, entra a `public_html`, sube `tienda-bombas-de-agua.zip` y descomprímelo ahí. Se crea solo la carpeta `bombas-de-agua`.
2. Dentro de `bombas-de-agua/api/` copia `config.sample.php` como `config.php` y completa el correo, el titular y el documento (iguales a los de la otra tienda). El Tag Manager (GTM-5SCP73SQ) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el mismo evento `whatsapp` a Tag Manager (con la marca, la página y el texto del botón), igual que en la tienda de filtros, así que cuenta como la misma conversión.
4. En Search Console agrega el sitemap https://filtrosparalavadoras.click/bombas-de-agua/sitemap.xml (la propiedad es la misma).
5. Precios: mientras una bomba no tenga precio, su página dice «pregúntale al asesor».
