<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de bombas de agua (bombas de desagüe) para lavadoras Samsung y LG, con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '')
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de bombas de agua (bombas de desagüe) para lavadoras. Te ayudamos a encontrar la bomba que necesita tu lavadora y te la enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo el modelo de tu lavadora por WhatsApp, para que pidas la bomba correcta.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: Samsung 305 479 6329 · LG 320 510 2995 o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
