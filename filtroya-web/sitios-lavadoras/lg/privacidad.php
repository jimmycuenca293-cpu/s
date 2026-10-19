<?php require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza("Tratamiento de datos personales | " . $n['nombre'], "Tratamiento de datos personales", '/privacidad.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Tratamiento de datos personales</h1><p>Cuando nos escribes por WhatsApp usamos tu nombre, tu número y los datos que nos des (ciudad, dirección, modelo de la lavadora) solo para atender tu consulta, confirmar tu pedido y coordinar el envío.</p>
<p>No vendemos tus datos. Puedes pedirnos que los corrijamos o los eliminemos escribiéndonos por WhatsApp o al correo de contacto.</p>
<p>Este sitio puede usar herramientas de medición (como Google Analytics) para saber cuántas personas lo visitan.</p><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>
<?php lav_pie(); ?>
