<?php require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza('Quiénes somos | ' . $n['nombre'], 'Somos un comercio colombiano de filtros de pelusas para lavadoras, con asesoría por WhatsApp y envíos a todo el país.', '/quienes-somos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Quiénes somos</h1>
<p><?= h($n['nombre']) ?> es un comercio colombiano de filtros de pelusas y bolsas de malla para lavadoras. Te ayudamos a encontrar el filtro que necesita tu lavadora y te lo enviamos a donde estés.</p>
<p>Antes de que compres, un asesor revisa contigo el modelo de tu lavadora por WhatsApp, para que pidas el filtro correcto.</p>
<p>Atendemos <?= h($n['horario']) ?>. Escríbenos al WhatsApp <?= h($n['telefono']) ?> o al correo <?= h($n['correo']) ?>.</p>
<p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?></p></div></div>
<?php lav_pie(); ?>
