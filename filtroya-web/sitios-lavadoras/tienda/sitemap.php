<?php
require __DIR__ . '/api/sitio.php';
header('Content-Type: application/xml; charset=utf-8');
$b = sitio()['base'];
$cat = catalogo();
$urls = array_fill_keys($cat['paginas'], '0.8') + ['/quienes-somos.php' => '0.4', '/terminos.php' => '0.2', '/privacidad.php' => '0.2', '/garantia-y-retracto.php' => '0.3'];
$urls['/'] = '1.0';
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($urls as $u => $pr) echo '  <url><loc>' . htmlspecialchars($b . $u) . '</loc><lastmod>' . $cat['fecha'] . '</lastmod><priority>' . $pr . '</priority></url>' . "\n";
echo '</urlset>';
