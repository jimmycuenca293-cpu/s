<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza("Términos y condiciones | " . $n['nombre'], "Términos y condiciones", '/mangueras-para-lavadora/terminos.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Términos y condiciones</h1><p>Este sitio presenta mangueras para lavadoras (de desagüe, de entrada de agua, tina-bomba, presostato y dispensador). No tiene carrito ni pago en línea: los pedidos se hacen por WhatsApp con un asesor y se pagan contra entrega.</p>
<h2>Cómo se hace un pedido</h2><p>Escribe al asesor por WhatsApp con la clase de manguera y el modelo de tu lavadora, o una foto de la manguera vieja. El asesor te confirma la manguera, el precio, el valor del envío y si hay pago contra entrega en tu ciudad antes de despachar.</p>
<h2>Confirma antes de comprar</h2><p>Las fotos son de referencia. Antes de pagar, compara la manguera con la que tienes o confirma el modelo de tu lavadora con el asesor. La instalación es responsabilidad del comprador; si no tienes experiencia con las partes internas de la lavadora, pídele ayuda a un técnico.</p>
<h2>Marcas</h2><p>Los nombres de marca se usan solo para indicar el tipo de lavadora. Somos un comercio independiente.</p><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>
<?php lav_pie(); ?>
