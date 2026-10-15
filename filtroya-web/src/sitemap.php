<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: application/xml; charset=utf-8');
$b = sitio()['base'];
$cat = catalogo();
$urls = ['/' => '1.0'];
foreach ($cat['marcas'] as $m) $urls['/marca/' . $m['slug'] . '/'] = '0.8';
foreach ($cat['productos'] as $p) $urls['/filtro/' . $p['slug'] . '/'] = '0.9';
foreach ($cat['paginas'] ?? [] as $u) $urls[$u] = str_starts_with($u, '/referencia/') || str_starts_with($u, '/nevecon/') ? '0.7' : '0.6';
$urls['/quienes-somos.php'] = '0.5'; $urls['/terminos.php'] = '0.2'; $urls['/privacidad.php'] = '0.2';
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
$fotos = [];
foreach ($cat['productos'] as $id => $p) $fotos['/filtro/' . $p['slug'] . '/'] = "/img/$id.jpg";
foreach ($urls as $u => $pr) echo '  <url><loc>' . htmlspecialchars($b . $u) . '</loc><lastmod>' . $cat['fecha'] . '</lastmod><priority>' . $pr . '</priority>'
    . (isset($fotos[$u]) ? '<image:image><image:loc>' . htmlspecialchars($b . $fotos[$u]) . '</image:loc></image:image>' : '') . "</url>\n";
echo '</urlset>';
