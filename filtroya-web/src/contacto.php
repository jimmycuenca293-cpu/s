<?php
require __DIR__ . '/partes.php';
$c = cfg(); $n = $c['negocio'];
$tel = preg_replace('/\D/', '', (string) ($c['whatsapp'] ?? ''));
if (strlen($tel) === 10) $tel = '57' . $tel;
$ld = ['@context' => 'https://schema.org', '@graph' => [
    ['@type' => 'ContactPage', 'name' => 'Contacto', 'url' => base_url() . '/contacto.php'],
    ['@type' => 'Store', '@id' => base_url() . '/#tienda', 'name' => $n['nombre'], 'url' => base_url() . '/', 'email' => $n['correo'], 'telephone' => $n['telefono'],
     'areaServed' => ['@type' => 'Country', 'name' => 'Colombia'], 'openingHours' => $n['horario'],
     'contactPoint' => ['@type' => 'ContactPoint', 'contactType' => 'customer service', 'telephone' => $n['telefono'], 'email' => $n['correo'], 'areaServed' => 'CO', 'availableLanguage' => 'es']],
]];
cabeza('Contacto | ' . $n['nombre'], 'Escríbenos por WhatsApp o al correo: te ayudamos a encontrar el filtro de agua de tu nevera. ' . $n['nombre'] . ', envíos a toda Colombia.', '/contacto.php',
    '<script type="application/ld+json">' . json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>');
?>
<nav class="miga"><a href="/">Inicio</a> › Contacto</nav>
<h1>Contacto</h1>
<p>¿No sabes cuál filtro necesita tu nevera? Mándanos la foto del filtro viejo o la etiqueta del modelo y te confirmamos antes de que compres.</p>
<div class="grid">
  <section class="caja"><h2>WhatsApp</h2><p>La forma más rápida. Respondemos en el horario de atención.</p>
    <?php if ($tel): ?><a class="btn" href="https://wa.me/<?= h($tel) ?>?text=<?= rawurlencode('Hola, ' . $n['nombre'] . '. Necesito ayuda para escoger el filtro de mi nevera.') ?>" target="_blank" rel="noopener">Escribir por WhatsApp</a><?php endif; ?></section>
  <section class="caja"><h2>Correo</h2><p><?= h($n['correo']) ?></p><p class="m">Te respondemos en el horario de atención.</p></section>
  <section class="caja"><h2>Horario</h2><p><?= h(ucfirst($n['horario'])) ?></p><p class="m">Pedidos en línea las 24 horas.</p></section>
</div>
<section class="caja"><h2>Antes de escribirnos</h2>
  <ul class="ok"><li>Tenemos <a href="/otras-marcas/preguntas-frecuentes/">preguntas frecuentes</a> con respuestas rápidas.</li><li>Busca tu filtro por <a href="/referencias/">referencia</a> o por <a href="/neveras/">modelo de nevera</a>.</li><li>Mira cómo <a href="/instalacion/">instalar tu filtro</a> paso a paso.</li><li>Consulta los <a href="/envios/">tiempos de envío por ciudad</a>.</li></ul></section>
<section class="caja"><h2>Datos del negocio</h2><p><?= identificacion() ?></p></section>
<?php pie(); ?>
