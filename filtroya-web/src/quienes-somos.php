<?php
require __DIR__ . '/partes.php';
$c = cfg(); $n = $c['negocio']; $t = $c['tecnico'] ?? [];
$nombre = trim((string) ($t['nombre'] ?? '')) ?: $n['titular'];
$anos = trim((string) ($t['anos'] ?? ''));
$esp = trim((string) ($t['especialidad'] ?? '')) ?: 'neveras, nevecones, lavadoras y secadoras';
$foto = is_file(__DIR__ . '/img/tecnico.jpg') ? '/img/tecnico.jpg' : '';
$ld = ['@context' => 'https://schema.org', '@graph' => [
    ['@type' => 'AboutPage', 'name' => 'Quiénes somos', 'url' => base_url() . '/quienes-somos.php'],
    ['@type' => 'Person', 'name' => $nombre, 'jobTitle' => 'Técnico de ' . $esp, 'worksFor' => ['@type' => 'Store', 'name' => $n['nombre']],
     'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Cali', 'addressCountry' => 'CO']] + ($foto ? ['image' => base_url() . $foto] : []),
]];
cabeza('Quiénes somos | ' . $n['nombre'], $n['nombre'] . ': filtros de agua para nevecón escogidos por un técnico de ' . $esp . ' en Cali.', '/quienes-somos.php',
    '<script type="application/ld+json">' . json_encode($ld, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) . '</script>');
?>
<nav class="miga"><a href="/">Inicio</a> › Quiénes somos</nav>
<h1>Quiénes somos</h1>
<div class="caja autor">
  <?php if ($foto): ?><img src="<?= h($foto) ?>" alt="<?= h($nombre) ?>, técnico en Cali" width="64" height="64"><?php endif; ?>
  <div><b><?= h($nombre) ?></b><br><span class="m">Técnico de <?= h($esp) ?> en Cali<?= $anos ? ' · ' . h($anos) . ' años de experiencia' : '' ?></span></div>
</div>
<p><?= h($n['nombre']) ?> nació de la experiencia en el taller: todos los días vemos nevecones con el agua sabiendo mal, el dispensador echando agua despacio o la máquina de hielo forzada, y casi siempre la causa es un filtro vencido o una referencia equivocada.</p>
<?php if (!empty($t['historia'])): ?><p><?= nl2br(h($t['historia'])) ?></p><?php endif; ?>
<p>Por eso armamos una tienda sencilla: buscas la referencia de tu filtro o el modelo de tu nevecón, te mostramos el que le sirve con todas sus equivalencias, pagas en línea y te llega a la casa. En Cali, además, lo instalamos nosotros mismos sin costo y de paso revisamos el nevecón.</p>
<section class="caja"><h2>Lo que nos importa</h2>
<ul class="ok"><li><b>La referencia correcta.</b> Cada página explica cómo confirmar que el filtro es el tuyo antes de comprar.</li><li><b>Precios claros.</b> El precio que ves es el que pagas, con el envío incluido.</li><li><b>Respaldo.</b> Si no encaja, te lo cambiamos. Tienes 5 días para retractarte y 30 días de garantía.</li></ul></section>
<section class="caja"><h2>Contacto</h2><p><?= h($n['nombre']) ?> · <?= h($n['titular']) ?> · <?= h($n['documento']) ?><br><?= h($n['direccion']) ?><br>Teléfono <?= h($n['telefono']) ?> · <?= h($n['correo']) ?><br>Atención: <?= h($n['horario']) ?></p></section>
<p><a href="/guia/">Lee nuestras guías</a> · <a href="/#catalogo">Ver los filtros</a></p>
<?php pie(); ?>
