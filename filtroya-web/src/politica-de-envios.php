<?php
require __DIR__ . '/partes.php';
$c = cfg(); $n = $c['negocio'];
$ld = ['@context' => 'https://schema.org', '@graph' => [['@type' => 'WebPage', 'name' => 'Política de envíos', 'url' => base_url() . '/politica-de-envios.php', 'inLanguage' => 'es-CO']]];
cabeza('Política de envíos | ' . $n['nombre'], 'Cobertura, costo, tiempos de entrega y seguimiento de los envíos de ' . $n['nombre'] . ' a toda Colombia: envío gratis y número de guía.', '/politica-de-envios.php',
    '<script type="application/ld+json">' . json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>');
?>
<nav class="miga"><a href="/">Inicio</a> › Política de envíos</nav>
<article class="legal">
<h1>Política de envíos</h1>
<p>Última actualización: octubre de 2026. Esta política aplica a todas las compras hechas en <?= h($n['nombre']) ?>.</p>
<h2>1. Cobertura</h2><p>Enviamos a todas las ciudades y municipios de Colombia por transportadora. Puedes ver el tiempo estimado de tu ciudad en la <a href="/envios/">página de envíos</a>.</p>
<h2>2. Costo</h2><p>El envío es <b>gratis</b>. El precio que ves en cada producto es el precio final que pagas, sin cargos adicionales de transporte.</p>
<h2>3. Cuándo despachamos</h2><p>Despachamos tu pedido cuando la pasarela de pagos confirma el pago. Recibes un correo con el recibo y, cuando el paquete sale, otro correo con el número de guía.</p>
<h2>4. Tiempos de entrega</h2><p>A las principales ciudades llega en 2 a 3 días hábiles después del despacho. A otros municipios puede tardar algunos días más, según la transportadora. Los tiempos son estimados y pueden variar por temporadas de alta demanda, clima u orden público.</p>
<h2>5. Seguimiento</h2><p>Con el número de guía puedes seguir tu paquete en la página de la transportadora. Si no lo recibes en el tiempo estimado, escríbenos y lo revisamos.</p>
<h2>6. Dirección y recepción</h2><p>Revisa que tu dirección, barrio, ciudad y celular estén correctos antes de pagar: la transportadora te llamará para entregar. Si nadie recibe el paquete, la transportadora hará nuevos intentos y te contactará.</p>
<h2>7. Si el paquete llega con daños</h2><p>Revisa el paquete al recibirlo. Si llega abierto o golpeado, anótalo en la guía de entrega y escríbenos el mismo día con fotos para ayudarte.</p>
<h2>8. Devoluciones y garantía</h2><p>Consulta el <a href="/garantia-y-retracto.php">derecho de retracto y la garantía</a>.</p>
<h2>9. Contacto</h2><p><?= identificacion() ?> Escríbenos desde la página de <a href="/contacto.php">contacto</a> o al correo <?= h($n['correo']) ?>. Atención: <?= h($n['horario']) ?>.</p>
</article>
<?php pie(); ?>
