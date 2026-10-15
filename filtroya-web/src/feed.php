<?php
// Productos para Google Merchant Center (fichas gratis en Google Shopping). Dirección: https://tudominio.com/feed.xml
require __DIR__ . '/api/sitio.php';
header('Content-Type: application/xml; charset=utf-8');
$b = sitio()['base'];
$n = cfg()['negocio'];
$x = fn($s) => htmlspecialchars((string) $s, ENT_XML1 | ENT_QUOTES, 'UTF-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0"><channel>'
    . '<title>' . $x($n['nombre']) . '</title><link>' . $x($b) . '/</link><description>Filtros de agua para nevecón con envío gratis a toda Colombia</description>' . "\n";
foreach (catalogo()['productos'] as $id => $p) {
    $desc = "Filtro de agua para nevecón {$p['marca']}, referencia {$p['ref']}" . ($p['alias'] ? '. También aparece como ' . implode(', ', array_slice($p['alias'], 0, 6)) : '')
        . '. Envío gratis a toda Colombia en 2 días hábiles; en Cali, domicilio gratis e instalación a domicilio. Cámbialo cada 6 meses.';
    echo '<item><g:id>' . $x($id) . '</g:id><g:title>' . $x($p['nombre'] . ' para nevecón ' . $p['marca'] . ' - filtro de agua') . '</g:title>'
        . '<g:description>' . $x($desc) . '</g:description><g:link>' . $x("$b/filtro/{$p['slug']}/") . '</g:link>'
        . '<g:image_link>' . $x("$b/img/$id.jpg") . '</g:image_link><g:availability>in_stock</g:availability>'
        . '<g:price>' . (int) $p['precio'] . '.00 COP</g:price><g:brand>' . $x($p['marca']) . '</g:brand><g:mpn>' . $x($p['ref']) . '</g:mpn>'
        . '<g:condition>new</g:condition><g:google_product_category>Hogar y jardín &gt; Electrodomésticos &gt; Accesorios para electrodomésticos</g:google_product_category>'
        . '<g:product_type>' . $x('Filtros de agua para nevecón > ' . $p['marca']) . '</g:product_type>'
        . '<g:shipping><g:country>CO</g:country><g:price>0.00 COP</g:price></g:shipping></item>' . "\n";
}
echo '</channel></rss>';
