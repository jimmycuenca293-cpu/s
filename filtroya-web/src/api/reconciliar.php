<?php
declare(strict_types=1);
// Revisa en Wompi los pagos que quedaron «pendientes» (el cliente cerró el navegador o falló un aviso) y actualiza el pedido.
// Hostinger > Avanzado > Cron Jobs, cada 15 minutos:  php /home/USUARIO/public_html/filtrosnevecones-api/reconciliar.php
// (o por URL: https://tudominio.com/filtrosnevecones-api/reconciliar.php?clave=TU_CRON_CLAVE)
require __DIR__ . '/lib.php';

if (PHP_SAPI !== 'cli') {
    $clave = (string) cfg()['cron_clave'];
    if ($clave === '' || !hash_equals($clave, (string) ($_GET['clave'] ?? ''))) fail('No autorizado.', 403);
}
if (!con_llaves()) { $m = 'Sin llaves de Wompi en config.php: no hay nada que reconciliar.'; PHP_SAPI === 'cli' ? print($m . "\n") : out(['ok' => true, 'mensaje' => $m]); exit; }

// Pedidos sin pagar de entre 5 minutos y 7 días (los muy recientes pueden seguir en pago)
$st = db()->prepare("SELECT ref FROM pedidos WHERE estado IN ('pendiente','rechazado') AND creado <= ? AND creado >= ? ORDER BY creado LIMIT 60");
$st->execute([date('c', time() - 300), date('c', time() - 7 * 86400)]);
$revisados = 0; $cambios = [];
foreach ($st->fetchAll(PDO::FETCH_COLUMN) as $ref) {
    $ch = curl_init(wompi_api() . '/transactions?reference=' . rawurlencode($ref));
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15]);
    $res = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ($code !== 200) continue;
    $lista = json_decode((string) $res, true)['data'] ?? [];
    if (!is_array($lista) || !$lista) { $revisados++; continue; }
    usort($lista, fn($a, $b) => strcmp((string) ($b['created_at'] ?? ''), (string) ($a['created_at'] ?? '')));
    // Si alguna transacción quedó aprobada, esa manda; si no, la más reciente
    $tx = $lista[0];
    foreach ($lista as $t) if (($t['status'] ?? '') === 'APPROVED') { $tx = $t; break; }
    $antes = db()->query("SELECT estado FROM pedidos WHERE ref = " . db()->quote($ref))->fetchColumn();
    $p = aplicar_transaccion($tx);
    $revisados++;
    if ($p && $p['estado'] !== $antes) $cambios[] = $ref . ': ' . $antes . ' → ' . $p['estado'];
}
$resumen = ['ok' => true, 'revisados' => $revisados, 'cambios' => $cambios];
PHP_SAPI === 'cli' ? print(json_encode($resumen, JSON_UNESCAPED_UNICODE) . "\n") : out($resumen);
