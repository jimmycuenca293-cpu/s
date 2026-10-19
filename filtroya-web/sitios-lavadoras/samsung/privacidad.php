<?php require __DIR__ . '/partes.php'; $n = cfg()['negocio']; cabeza('Política de tratamiento de datos | ' . $n['nombre'], 'Cómo ' . $n['nombre'] . ' trata tus datos personales (Ley 1581 de 2012).', '/privacidad.php'); ?>
<article class="legal">
<h1>Política de tratamiento de datos</h1>
<p class="m">Ley 1581 de 2012 y Decreto 1074 de 2015. Vigente desde el 15 de octubre de 2026.</p>
<h2>Responsable</h2><p><?= identificacion() ?> Correo: <?= h($n['correo']) ?>. Teléfono: <?= h($n['telefono']) ?>.</p>
<h2>Qué datos pedimos</h2><p>Nombre, correo, celular, ciudad, barrio, dirección, indicaciones de entrega y, si lo das, el modelo de tu lavadora. Los datos de pago los recibe y procesa la pasarela de pagos; nosotros no vemos ni guardamos tu tarjeta.</p>
<h2>Para qué los usamos</h2><ul><li>Procesar tu pago, despachar, entregar e instalar tu pedido.</li><li>Enviarte el recibo, el número de guía y avisos sobre tu pedido.</li><li>Atender garantías, cambios, devoluciones y reclamos.</li><li>Cumplir obligaciones legales y contables.</li><li>Pedirte tu opinión sobre la compra. Si la das, se publica con tu primer nombre, la inicial del apellido y tu ciudad.</li><li>Solo si lo autorizas al comprar (es opcional): enviarte un correo cuando toque cambiar el filtro.</li></ul><h2>Medición de visitas</h2><p>Si está activado, usamos Google Analytics para contar visitas y compras de forma agregada (sin tu nombre ni tus datos de entrega).</p>
<h2>Autorización</h2><p>Al tocar el botón de pago autorizas el tratamiento de tus datos para estas finalidades.</p>
<h2>Con quién los compartimos</h2><p>Con la pasarela de pagos que procesa tu pago, con la transportadora para entregarte el pedido y con el servicio de formularios y correo que nos hace llegar los datos del pedido (FormSubmit y el proveedor de correo de la tienda), solo para atender tu compra. No vendemos ni alquilamos tus datos.</p>
<h2>Lo que se guarda en tu teléfono</h2><p>La tienda guarda en tu navegador tu ciudad, tus datos de entrega y tus pedidos para que no tengas que escribirlos otra vez. Puedes borrarlos borrando los datos del sitio en tu navegador.</p>
<h2>Tus derechos</h2><p>Puedes conocer, actualizar, rectificar y pedir que borremos tus datos; pedir prueba de tu autorización; revocarla; saber cómo los usamos y presentar quejas ante la Superintendencia de Industria y Comercio. Escríbenos a <?= h($n['correo']) ?>. Respondemos consultas en máximo 10 días hábiles y reclamos en máximo 15 días hábiles.</p>
</article>
<?php pie(); ?>
