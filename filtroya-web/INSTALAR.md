# PuroFiltro en tu propia página (Hostinger + Wompi)

La tienda vende sola: el cliente escoge el filtro, paga en Wompi y a ti te llega un correo con el pedido pagado
y todos los datos para despacharlo. Nada llega a WhatsApp.

## Lo que necesitas
1. **Hostinger** con un plan que tenga PHP (cualquier plan de hosting web) y **un dominio** (ej. filtrosdeaguanevecon.com).
2. **Cuenta de comercio en Wompi** (wompi.com): la abres con tu cédula o RUT y tu cuenta bancaria.

## Paso 1. Subir la tienda
1. En Hostinger entra a **Archivos > Administrador de archivos** y abre la carpeta `public_html`.
2. Sube el archivo `filtroya-web.zip` y descomprímelo ahí (clic derecho > Extraer).
   Debe quedar `public_html/index.php`, `public_html/purofiltro-filtro/`, `public_html/purofiltro-api/`, etc.

## Paso 2. Crear el correo de la tienda
En Hostinger: **Correos > Cuentas de correo** y crea `pedidos@tudominio.com`. Desde ahí salen los recibos.

## Paso 3. Poner tus datos y llaves
1. Dentro de `public_html/purofiltro-api/` copia `config.sample.php` y ponle de nombre `config.php`.
2. Ábrelo (clic derecho > Editar) y llena:
   - `dominio`: tu dominio con https, ej. `https://filtrosdeaguanevecon.com`
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
4. En **URL de eventos** pon: `https://filtrosdeaguanevecon.com/purofiltro-api/wompi.php`
   (así Wompi avisa a tu tienda apenas el cliente paga, aunque cierre el navegador).

Primero prueba con las llaves de prueba (`pub_test_`): haz una compra con los datos de prueba que da Wompi
y revisa que te llegue el correo. Cuando todo esté bien, cambia a las llaves de producción (`pub_prod_`).

## Paso 5. Recordatorios automáticos (cada 6 meses)
En Hostinger: **Avanzado > Cron Jobs**, crea una tarea **una vez al día** con este comando
(cambia USUARIO por el tuyo; Hostinger te muestra la ruta):

    /usr/bin/php /home/USUARIO/public_html/purofiltro-api/recordatorios.php

Le escribe por correo, solo a quien lo autorizó al comprar, cuando ya casi le toca cambiar el filtro.

## Paso 6. Google
1. Entra a **search.google.com/search-console**, agrega tu dominio y verifícalo (Hostinger te ayuda con el registro DNS).
2. En **Sitemaps** escribe `sitemap.xml` y envía.
3. Crea tu **Perfil de Empresa en Google** (business.google.com) como **empresa de servicio sin local** (oculta la dirección y pon como zona de servicio Colombia) y el link de la tienda.

La tienda trae 150 páginas para Google: una por cada filtro, **una por cada referencia equivalente** (84, por ejemplo
`/referencia/ukf8001/` o `/referencia/haf-cin/`), **una por cada modelo de nevecón** (34, por ejemplo `/nevecon/rf28hmedbsr/`),
8 guías, 159 páginas de envíos por ciudad y los directorios de referencias y de neveras. Además trae todo lo que Google pide: una página por cada filtro con su referencia, precio, envío y devoluciones
(datos estructurados de producto), páginas por marca, mapa del sitio y robots.txt. Google tarda de unos días a
unas semanas en mostrar las páginas, y subir en los resultados depende de la competencia; nadie lo puede garantizar.

## Paso 7. Google Shopping, Analytics y tu perfil (lo que más ayuda a vender)
1. **Google Merchant Center** (merchants.google.com): crea la cuenta con tu dominio, agrega una fuente de productos
   "programada" con la dirección `https://tudominio.com/feed.xml` (se actualiza sola) y configura envío gratis a Colombia
   y devoluciones de 5 días. Así tus filtros salen gratis con foto y precio en Google Shopping.
2. **Search Console**: si eliges verificar con "etiqueta HTML", copia solo el código de `content="..."` en `google_verificacion` de config.php.
3. **Google Analytics 4** (opcional): crea la propiedad y pega el código `G-XXXXXXX` en `ga4` de config.php.
   Mide visitas y compras (cada pago aprobado se registra como venta).
4. **Quiénes somos**: llena la sección `tecnico` de config.php (tu nombre, años de experiencia y tu historia) y sube una foto
   tuya como `public_html/purofiltro-img/tecnico.jpg`. Google confía más en las tiendas atendidas por expertos, y las guías salen firmadas por ti.

## Para que las IA te lean y te recomienden
La tienda trae `tudominio.com/llms.txt` y `tudominio.com/llms-full.txt`: un texto escrito para asistentes de IA
(ChatGPT, Gemini, Claude, Perplexity, el resumen con IA de Google) con lo que vendes, precios, equivalencias, envío,
garantía y dónde está cada página. Se actualiza solo con el catálogo. El robots.txt deja entrar a los lectores de esas IA,
y cada filtro tiene un cuadro de "Datos rápidos" que ellas pueden citar tal cual.
Llena `redes` en config.php con tus perfiles (Facebook, Instagram, Perfil de Google, Mercado Libre): ayuda a que reconozcan tu tienda.

## Opiniones con estrellas
Siete días después de cada pago, la tienda le pide la opinión al cliente por correo (con la misma tarea programada del paso 5).
Solo puede opinar quien compró. Las opiniones salen en la página del filtro y Google puede mostrar las estrellas en los resultados.
En el panel (`admin.php`, pestaña Opiniones) puedes ocultar una opinión ofensiva o falsa; no ocultes las negativas reales:
Google lo prohíbe y además responderlas bien genera confianza.

## Tu día a día
- Te llega un correo por cada pedido **pagado**, con todos los datos.
- En `https://tudominio.com/admin.php` (con tu clave) ves los pedidos. Cuando despachas, pon el número de guía
  y toca **Marcar enviado**: al cliente le llega un correo con la guía.
- Las devoluciones de dinero se hacen desde el panel de Wompi.

## Cambiar precios o agregar filtros
Los precios salen de la app de Claude. Pídeme el cambio y te genero un paquete nuevo
(se sube igual; tu `config.php` y tus pedidos en `purofiltro-data/` no se tocan).

## Carpetas con el nombre del proyecto

Todas las carpetas de la tienda empiezan por `purofiltro-` (purofiltro-img, purofiltro-api, purofiltro-filtro, purofiltro-guia...) para no chocar con las carpetas que ya tengas en tu hosting. Los únicos archivos que pueden coincidir con los tuyos son `index.php` (la página de inicio de la tienda) y `.htaccess`: si ya tienes un `index.html` o `index.php` en `public_html`, la tienda reemplaza tu página de inicio; si ya tienes un `.htaccess`, une su contenido con el de la tienda en vez de borrarlo.

## Google Tag Manager y conversiones de Google Ads

La tienda ya trae tu contenedor **GTM-N39G66VJ** y la verificación de Search Console (en `purofiltro-api/config.php`: `gtm` y `google_verificacion`). Manda estos eventos al `dataLayer`:

| Evento | Cuándo pasa | Datos |
|---|---|---|
| `whatsapp` | El cliente toca el botón verde de WhatsApp (o cualquier enlace de WhatsApp) | `ubicacion` (boton_flotante o enlace), `pagina` |
| `pago_wompi` | El cliente toca "Pagar" y va a la página de pago | `value` (total en pesos), `currency` (COP), `transaction_id` (número de pedido) |

En Tag Manager, para cada uno:
1. **Activadores → Nuevo → Evento personalizado**, nombre del evento: `whatsapp` (y otro con `pago_wompi`).
2. **Etiquetas → Nueva → Seguimiento de conversiones de Google Ads**, con el ID y la etiqueta de conversión que te da Google Ads. En la de `pago_wompi` pon como valor la variable de capa de datos `value` y moneda `COP`.
3. Agrega también la etiqueta **Vinculador de conversiones** (Conversion Linker) con el activador "All Pages".
4. **Enviar → Publicar.**

El número de WhatsApp del botón flotante se cambia en `purofiltro-api/config.php` → `whatsapp`.

## Sitios por marca (Samsung, LG, Whirlpool y GE)
Además de la tienda principal hay un zip por marca: `purofiltro-samsung.zip`, `purofiltro-lg.zip`,
`purofiltro-whirlpool.zip` y `purofiltro-ge.zip`. Cada uno es una tienda completa (carrito, pago, pedidos)
que solo vende esa marca, con su propio diseño. Cada una va en **su propio dominio**:
1. En Hostinger agrega el dominio de la marca como sitio nuevo y sube el zip de esa marca a su `public_html` (paso 1).
2. Crea su `purofiltro-api/config.php` igual que en el paso 3: puedes copiar el de la tienda principal,
   pero cambia `dominio` por el dominio de esa marca. Las llaves de Wompi y tu correo pueden ser los mismos.
3. Wompi solo deja poner **una** URL de eventos: déjala con la tienda principal. En los sitios de marca el pago se
   confirma cuando el cliente vuelve de la página de pago. Si un pedido queda «pendiente», míralo en tu panel de Wompi.
4. En Search Console agrega cada dominio como propiedad nueva, verifícalo y envía `https://dominiodelamarca.com/sitemap.xml`.
5. Cada sitio guarda sus pedidos aparte: entra a `https://dominiodelamarca.com/admin.php` para verlos.
