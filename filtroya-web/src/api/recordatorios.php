<?php
declare(strict_types=1);
// Recordatorio automático de cambio de filtro (cada 6 meses), solo a quien lo autorizó.
// Hostinger > Avanzado > Cron Jobs, una vez al día:  php /home/USUARIO/public_html/api/recordatorios.php
// (o por URL: https://tudominio.com/api/recordatorios.php?clave=TU_CRON_CLAVE)
require __DIR__ . '/lib.php';

if (PHP_SAPI !== 'cli') {
    $clave = (string) cfg()['cron_clave'];
    if ($clave === '' || !hash_equals($clave, (string) ($_GET['clave'] ?? ''))) fail('No autorizado.', 403);
}
$limite = date('c', strtotime('-6 months +5 days'));
$st = db()->prepare("SELECT * FROM pedidos WHERE recordar = 1 AND recordado = 0 AND estado IN ('pagado','enviado','entregado') AND pagado_en <= ?");
$st->execute([$limite]);
$n = 0;
$cat = catalogo()['productos'];
foreach ($st->fetchAll() as $p) {
    $url = base_url() . '/' . (isset($cat[$p['pid']]) ? 'filtro/' . $cat[$p['pid']]['slug'] . '/' : '');
    enviar_correo($p['email'], 'Ya casi toca cambiar el filtro de tu nevecón',
        '<h2 style="margin:0 0 8px">Hola, ' . h(explode(' ', $p['nombre'])[0]) . '</h2><p>Hace casi 6 meses compraste el <b>' . h($p['producto']) . '</b> (ref. ' . h($p['refprod']) . '). '
        . 'Ya casi toca cambiarlo para que el agua siga saliendo limpia y sin mal sabor.</p><p><a href="' . h($url) . '" style="display:inline-block;background:#0f7f70;color:#fff;padding:12px 18px;border-radius:10px;text-decoration:none;font-weight:bold">Pedir mi filtro</a></p>'
        . '<p style="color:#5a6873;font-size:13px">Te escribimos porque lo autorizaste al comprar. Si no quieres más recordatorios, responde este correo con la palabra NO.</p>');
    db()->prepare('UPDATE pedidos SET recordado = 1 WHERE ref = ?')->execute([$p['ref']]);
    $n++;
}
PHP_SAPI === 'cli' ? print("Recordatorios enviados: $n\n") : out(['enviados' => $n]);
