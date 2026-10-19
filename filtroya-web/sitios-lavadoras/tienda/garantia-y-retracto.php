<?php $MARCA = 'home'; require __DIR__ . '/lav.php';
$n = sitio()['negocio'];
lav_cabeza("Garantía y retracto | " . $n['nombre'], "Garantía y retracto", '/garantia-y-retracto.php', '', '');
?>
<div class="m-wrap"><div class="m-texto"><h1>Garantía y retracto</h1><p>Si el filtro llega con algún defecto, escríbenos por WhatsApp con una foto y lo revisamos.</p>
<p>Para compras a distancia puedes ejercer el derecho de retracto dentro de los 5 días hábiles siguientes a la entrega, según la ley colombiana, siempre que el producto no haya sido usado y esté en buen estado. Coordina la devolución con el asesor.</p>
<p>Autoridad de protección al consumidor: <a href="https://www.sic.gov.co/" target="_blank" rel="noopener">Superintendencia de Industria y Comercio</a>.</p><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?> · <?= h($n['correo']) ?></p></div></div>
<?php lav_pie(); ?>
