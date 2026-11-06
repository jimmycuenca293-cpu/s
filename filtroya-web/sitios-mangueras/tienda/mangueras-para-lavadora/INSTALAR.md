# Mangueras para lavadora (todas las marcas), dentro de https://filtrosparalavadoras.click

Todo vive en la carpeta `mangueras-para-lavadora/`, así que no pisa nada de las otras tiendas (`/samsung/`, `/lg/`, `/bombas-de-agua/`, `api/`, `.htaccess`, etc.).

- Tienda: https://filtrosparalavadoras.click/mangueras-para-lavadora/ (sin marcas: sirve para todas las lavadoras)
- Asesor WhatsApp: 305 479 6329 (para cambiarlo, edita WHATSAPP y TELEFONO al inicio de `mangueras.py` y vuelve a generar)

Sin carrito ni pago en línea: los pedidos se hacen por WhatsApp con el asesor (pago contra entrega).

1. En Hostinger abre el administrador de archivos del dominio filtrosparalavadoras.click, entra a `public_html`, sube `tienda-mangueras-para-lavadora.zip` y descomprímelo ahí. Se crea solo la carpeta `mangueras-para-lavadora`.
2. Dentro de `mangueras-para-lavadora/api/` copia `config.sample.php` como `config.php` y completa el correo, el titular y el documento (iguales a los de la otra tienda). El Tag Manager (GTM-5SCP73SQ) y la verificación de Search Console ya vienen puestos.
3. Cada clic en un botón de WhatsApp manda el mismo evento `whatsapp` a Tag Manager, igual que en las otras tiendas, así que cuenta como la misma conversión.
4. En Search Console agrega el sitemap https://filtrosparalavadoras.click/mangueras-para-lavadora/sitemap.xml (la propiedad es la misma).
5. Precios: mientras una manguera no tenga precio, su página dice «pregúntale al asesor».
