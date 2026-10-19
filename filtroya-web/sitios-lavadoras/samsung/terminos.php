<?php require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza("Términos y condiciones | " . $n['nombre'], "Términos y condiciones", '/terminos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Términos y condiciones</h1><p>Este sitio presenta filtros de pelusas y bolsas de malla para lavadoras. No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con el modelo de tu lavadora o una foto del filtro viejo. El asesor te confirma el filtro, el precio, el valor del envío y la forma de pago antes de que compres.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara el filtro con el que tienes o confirma el modelo de tu lavadora con el asesor.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>
<?php lav_pie(); ?>
