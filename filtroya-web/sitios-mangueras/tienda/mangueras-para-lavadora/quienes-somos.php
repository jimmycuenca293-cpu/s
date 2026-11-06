<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de mangueras para lavadoras (entrada de agua, desagüe, tina-bomba), con asesoría por WhatsApp y envíos a todo el país.', '/mangueras-para-lavadora/quienes-somos.php', '', '')
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de mangueras para lavadoras: de entrada de agua fría y caliente, negras con rosca, de desagüe y tina-bomba. Te ayudamos a encontrar la manguera que necesita tu lavadora y te la enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo cuál manguera necesitas por WhatsApp, para que pidas la correcta.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos por WhatsApp: Mangueras para lavadora 305 479 6329 o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
