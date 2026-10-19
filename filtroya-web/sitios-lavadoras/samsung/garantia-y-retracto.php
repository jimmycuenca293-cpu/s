<?php require __DIR__ . '/partes.php'; $n = cfg()['negocio']; cabeza('Garantía y derecho de retracto | ' . $n['nombre'], 'Garantía legal, derecho de retracto de 5 días hábiles y reversión del pago en ' . $n['nombre'] . ': cómo pedirlos paso a paso.', '/garantia-y-retracto.php'); ?>
<article class="legal">
<h1>Garantía y derecho de retracto</h1>
<p class="m">Según la Ley 1480 de 2011 (Estatuto del Consumidor). Vigente desde el 15 de octubre de 2026.</p>
<h2>Antes de comprar</h2><p>La forma más fácil de no tener problemas es comprar el filtro correcto. Compara la referencia impresa en tu filtro viejo o el modelo de tu lavadora con la del producto, y si tienes dudas escríbenos por WhatsApp al <?= h($n['telefono']) ?>: te confirmamos antes de pagar.</p>
<h2>Garantía legal</h2><p>Todos nuestros filtros tienen la garantía legal. Si el filtro llega con un defecto o falla por un defecto de fabricación, avísanos con fotos o un video corto y lo revisamos para cambiártelo o devolverte el dinero, según la ley. La garantía no cubre daños por mala instalación, golpes o el desgaste normal del filtro (dura unos 6 meses).</p>
<h2>Derecho de retracto: 5 días hábiles</h2><p>Como es una compra por internet, tienes <b>5 días hábiles desde que recibes el filtro</b> para arrepentirte, sin dar explicaciones. El filtro debe estar <b>sin instalar y en su empaque</b>. El transporte de la devolución corre por tu cuenta y te devolvemos el dinero en máximo 30 días calendario.</p>
<h2>Reversión del pago</h2><p>Si pagaste con un medio electrónico y fuiste víctima de fraude, no autorizaste la compra, el producto no llegó, no es el que pediste o está defectuoso, puedes pedir la reversión del pago dentro de los 5 días hábiles siguientes a que lo sepas o lo recibas. Escríbenos y también avísale a tu banco.</p>
<h2>Cómo pedir la garantía, el retracto o la reversión</h2>
<ol><li>Escríbenos por WhatsApp al <?= h($n['telefono']) ?> o al correo <?= h($n['correo']) ?> con tu número de pedido (te llega en el correo de confirmación).</li><li>Cuéntanos qué pasó y manda una foto del filtro y de la etiqueta.</li><li>Te respondemos en máximo 15 días hábiles con la solución y, si hay que devolverlo, cómo enviarlo.</li></ol>
<p>Si no quedas conforme, puedes acudir a la Superintendencia de Industria y Comercio: <a href="https://www.sic.gov.co" rel="nofollow">www.sic.gov.co</a>. Lee también los <a href="/terminos.php">Términos y condiciones</a>.</p>
</article>
<?php pie(); ?>
