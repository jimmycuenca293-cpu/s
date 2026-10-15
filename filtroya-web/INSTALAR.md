# FiltroYa en tu propia página (Hostinger + Wompi)

La tienda vende sola: el cliente escoge el filtro, paga en Wompi y a ti te llega un correo con el pedido pagado
y todos los datos para despacharlo. Nada llega a WhatsApp.

## Lo que necesitas
1. **Hostinger** con un plan que tenga PHP (cualquier plan de hosting web) y **un dominio** (ej. filtroyacali.com).
2. **Cuenta de comercio en Wompi** (wompi.com): la abres con tu cédula o RUT y tu cuenta bancaria.

## Paso 1. Subir la tienda
1. En Hostinger entra a **Archivos > Administrador de archivos** y abre la carpeta `public_html`.
2. Sube el archivo `filtroya-web.zip` y descomprímelo ahí (clic derecho > Extraer).
   Debe quedar `public_html/index.php`, `public_html/filtro/`, `public_html/api/`, etc.

## Paso 2. Crear el correo de la tienda
En Hostinger: **Correos > Cuentas de correo** y crea `pedidos@tudominio.com`. Desde ahí salen los recibos.

## Paso 3. Poner tus datos y llaves
1. Dentro de `public_html/api/` copia `config.sample.php` y ponle de nombre `config.php`.
2. Ábrelo (clic derecho > Editar) y llena:
   - `dominio`: tu dominio con https, ej. `https://filtroyacali.com`
   - `negocio`: tu nombre o el de la empresa, cédula o NIT, dirección, teléfono, correo y horario.
   - `correo_avisos`: el correo donde quieres recibir los pedidos pagados (puede ser tu Gmail).
   - `correo_remitente`: `pedidos@tudominio.com` (el del paso 2).
   - `admin_clave`: una clave larga para entrar a tu panel de pedidos.
   - `cron_clave`: otra clave cualquiera (para los recordatorios).
   - `wompi`: tus llaves (paso 4).

## Paso 4. Conectar Wompi
En el panel de Wompi, entra a **Desarrolladores**:
1. Copia la **llave pública** (`pub_test_...` para pruebas, `pub_prod_...` para cobrar de verdad) en `public_key`.
2. Copia el **secreto de integridad** en `integridad`.
3. Copia el **secreto de eventos** en `eventos`.
4. En **URL de eventos** pon: `https://tudominio.com/api/wompi.php`
   (así Wompi avisa a tu tienda apenas el cliente paga, aunque cierre el navegador).

Primero prueba con las llaves de prueba (`pub_test_`): haz una compra con los datos de prueba que da Wompi
y revisa que te llegue el correo. Cuando todo esté bien, cambia a las llaves de producción (`pub_prod_`).

## Paso 5. Recordatorios automáticos (cada 6 meses)
En Hostinger: **Avanzado > Cron Jobs**, crea una tarea **una vez al día** con este comando
(cambia USUARIO por el tuyo; Hostinger te muestra la ruta):

    /usr/bin/php /home/USUARIO/public_html/api/recordatorios.php

Le escribe por correo, solo a quien lo autorizó al comprar, cuando ya casi le toca cambiar el filtro.

## Paso 6. Google
1. Entra a **search.google.com/search-console**, agrega tu dominio y verifícalo (Hostinger te ayuda con el registro DNS).
2. En **Sitemaps** escribe `sitemap.xml` y envía.
3. Crea tu **Perfil de Empresa en Google** (business.google.com) con la dirección en Cali y el link de la tienda.

La tienda trae 150 páginas para Google: una por cada filtro, **una por cada referencia equivalente** (84, por ejemplo
`/referencia/ukf8001/` o `/referencia/haf-cin/`), **una por cada modelo de nevecón** (34, por ejemplo `/nevecon/rf28hmedbsr/`),
4 guías, la página de Cali y los directorios de referencias y de neveras. Además trae todo lo que Google pide: una página por cada filtro con su referencia, precio, envío y devoluciones
(datos estructurados de producto), páginas por marca, mapa del sitio y robots.txt. Google tarda de unos días a
unas semanas en mostrar las páginas, y subir en los resultados depende de la competencia; nadie lo puede garantizar.

## Tu día a día
- Te llega un correo por cada pedido **pagado**, con todos los datos.
- En `https://tudominio.com/admin.php` (con tu clave) ves los pedidos. Cuando despachas, pon el número de guía
  y toca **Marcar enviado**: al cliente le llega un correo con la guía.
- Las devoluciones de dinero se hacen desde el panel de Wompi.

## Cambiar precios o agregar filtros
Los precios salen de la app de Claude. Pídeme el cambio y te genero un paquete nuevo
(se sube igual; tu `config.php` y tus pedidos en `data/` no se tocan).
