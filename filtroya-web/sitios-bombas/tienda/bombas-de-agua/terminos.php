<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza("Términos y condiciones | " . $n['nombre'], "Términos y condiciones", '/bombas-de-agua/terminos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Términos y condiciones</h1><p>Este sitio presenta bombas de agua (bombas de desagüe) para lavadoras. No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con el modelo de tu lavadora o una foto de la bomba vieja. El asesor te confirma la bomba, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de despachar.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara la bomba con la que tienes o confirma el modelo de tu lavadora con el asesor. La instalación es responsabilidad del comprador; si no tienes experiencia con la parte eléctrica o hidráulica, pídele ayuda a un técnico.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>
<?php lav_pie(); ?>
