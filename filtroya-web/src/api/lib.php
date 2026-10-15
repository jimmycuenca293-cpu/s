<?php
declare(strict_types=1);
// Funciones comunes de la tienda: configuración, base de datos, Wompi y correos.

function cfg(): array
{
    static $c = null;
    if ($c === null) {
        $f = __DIR__ . '/config.php';
        $c = is_file($f) ? require $f : require __DIR__ . '/config.sample.php';
    }
    return $c;
}

function catalogo(): array
{
    static $cat = null;
    return $cat ??= require __DIR__ . '/catalogo.php';
}

function base_url(): string
{
    // En la tarea programada (cron) no hay dominio en la petición: se usa el de config.php
    if (PHP_SAPI === 'cli') return rtrim((string) (cfg()['dominio'] ?? 'https://tudominio.com'), '/');
    $https = ($_SERVER['HTTPS'] ?? '') === 'on' || ($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https';
    $host = preg_replace('/[^a-zA-Z0-9.\-:]/', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    return ($https ? 'https' : 'http') . '://' . $host;
}

function out(mixed $data, int $code = 200): never
{
    http_response_code($code);
    header('Content-Type: application/json; charset=utf-8');
    header('Cache-Control: no-store');
    header('X-Content-Type-Options: nosniff');
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function fail(string $mensaje, int $code = 400): never
{
    out(['error' => true, 'mensaje' => $mensaje], $code);
}

function h(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
}

function cop(int $n): string
{
    return '$ ' . number_format($n, 0, ',', '.');
}

function db(): PDO
{
    static $pdo = null;
    if ($pdo) return $pdo;
    $dir = __DIR__ . '/../data';
    if (!is_dir($dir)) mkdir($dir, 0750, true);
    $pdo = new PDO('sqlite:' . $dir . '/pedidos.sqlite', null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
    $pdo->exec('PRAGMA journal_mode = WAL');
    $pdo->exec('CREATE TABLE IF NOT EXISTS pedidos (
        ref TEXT PRIMARY KEY, creado TEXT NOT NULL, estado TEXT NOT NULL DEFAULT "pendiente",
        pid TEXT, producto TEXT, refprod TEXT, unidades INTEGER, pack INTEGER, total INTEGER,
        entrega TEXT, ciudad TEXT, nombre TEXT, email TEXT, tel TEXT, barrio TEXT, dir TEXT,
        indicaciones TEXT, modelo TEXT, recordar INTEGER DEFAULT 0, ip TEXT,
        tx_id TEXT, tx_estado TEXT, metodo TEXT, pagado_en TEXT, guia TEXT, notas TEXT,
        avisado INTEGER DEFAULT 0, recordado INTEGER DEFAULT 0)');
    return $pdo;
}

function wompi_api(): string
{
    if (!empty(cfg()['wompi']['api'])) return rtrim(cfg()['wompi']['api'], '/'); // solo para pruebas
    return str_starts_with(cfg()['wompi']['public_key'], 'pub_prod_') ? 'https://production.wompi.co/v1' : 'https://sandbox.wompi.co/v1';
}

// Firma de integridad del checkout: SHA-256 de referencia + monto en centavos + moneda + secreto
function firma_integridad(string $ref, int $centavos): string
{
    return hash('sha256', $ref . $centavos . 'COP' . cfg()['wompi']['integridad']);
}

// Valor de "transaction.status" dentro de data
function valor_ruta(array $data, string $ruta): string
{
    $v = $data;
    foreach (explode('.', $ruta) as $k) {
        if (!is_array($v) || !array_key_exists($k, $v)) return '';
        $v = $v[$k];
    }
    return is_scalar($v) ? (is_bool($v) ? ($v ? 'true' : 'false') : (string) $v) : '';
}

// Aplica el estado de una transacción de Wompi al pedido. Devuelve el pedido actualizado o null.
function aplicar_transaccion(array $tx): ?array
{
    $ref = (string) ($tx['reference'] ?? '');
    $st = db()->prepare('SELECT * FROM pedidos WHERE ref = ?');
    $st->execute([$ref]);
    $p = $st->fetch();
    if (!$p) return null;
    $estadoTx = (string) ($tx['status'] ?? '');
    // El monto tiene que ser exactamente el del pedido: si no, no se marca como pagado
    $montoOk = (int) ($tx['amount_in_cents'] ?? -1) === (int) $p['total'] * 100 && ($tx['currency'] ?? 'COP') === 'COP';
    $nuevo = $p['estado'];
    if ($p['estado'] === 'pendiente' || $p['estado'] === 'rechazado') {
        if ($estadoTx === 'APPROVED' && $montoOk) $nuevo = 'pagado';
        elseif (in_array($estadoTx, ['DECLINED', 'VOIDED', 'ERROR'], true)) $nuevo = 'rechazado';
    }
    db()->prepare('UPDATE pedidos SET tx_id = ?, tx_estado = ?, metodo = ?, estado = ?, pagado_en = COALESCE(pagado_en, ?) WHERE ref = ?')
        ->execute([(string) ($tx['id'] ?? ''), $estadoTx . ($estadoTx === 'APPROVED' && !$montoOk ? ' (MONTO NO COINCIDE)' : ''), (string) ($tx['payment_method_type'] ?? ''), $nuevo, $nuevo === 'pagado' ? date('c') : null, $ref]);
    $st->execute([$ref]);
    $p = $st->fetch();
    if ($p['estado'] === 'pagado' && !(int) $p['avisado']) {
        // Se marca primero para no mandar dos veces el correo si llegan dos avisos juntos
        $up = db()->prepare('UPDATE pedidos SET avisado = 1 WHERE ref = ? AND avisado = 0');
        $up->execute([$ref]);
        if ($up->rowCount() === 1) avisar_pago($p);
    }
    return $p;
}

function entrega_txt(string $e): string
{
    return ['instalacion' => 'Domicilio + instalación en Cali', 'domicilio' => 'Domicilio en Cali', 'transportadora' => 'Envío por transportadora'][$e] ?? $e;
}

function enviar_correo(string $para, string $asunto, string $html): bool
{
    $c = cfg();
    $de = $c['correo_remitente'];
    $nombre = '=?UTF-8?B?' . base64_encode($c['negocio']['nombre']) . '?=';
    $headers = implode("\r\n", [
        'MIME-Version: 1.0', 'Content-Type: text/html; charset=UTF-8', "From: $nombre <$de>", 'Reply-To: ' . $c['negocio']['correo'],
    ]);
    $cuerpo = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#15212b;max-width:560px">' . $html . '</div>';
    $ok = filter_var($para, FILTER_VALIDATE_EMAIL) && @mail($para, '=?UTF-8?B?' . base64_encode($asunto) . '?=', $cuerpo, $headers, '-f' . $de);
    if (!$ok) {
        // Sin servidor de correo (o en pruebas) queda guardado aquí para no perderlo
        @file_put_contents(__DIR__ . '/../data/correos.log', date('c') . " PARA: $para\nASUNTO: $asunto\n" . strip_tags(str_replace(['<br>', '</p>', '</tr>'], "\n", $html)) . "\n----\n", FILE_APPEND);
    }
    return (bool) $ok;
}

function tabla_pedido(array $p, bool $completo): string
{
    $filas = [
        'Pedido' => $p['ref'], 'Producto' => "{$p['unidades']} × {$p['producto']} (ref. {$p['refprod']})" . ($p['pack'] ? ' — pack anual' : ''),
        'Total pagado' => cop((int) $p['total']), 'Entrega' => entrega_txt($p['entrega']), 'Ciudad' => $p['ciudad'],
    ];
    if ($completo) {
        $filas += ['Nombre' => $p['nombre'], 'Celular' => $p['tel'], 'Correo' => $p['email'], 'Barrio' => $p['barrio'], 'Dirección' => $p['dir'],
            'Indicaciones' => $p['indicaciones'] ?: '—', 'Modelo del nevecón' => $p['modelo'] ?: '—', 'Recordatorio de cambio' => $p['recordar'] ? 'Sí' : 'No',
            'Pago Wompi' => trim(($p['metodo'] ?: '') . ' · ' . ($p['tx_id'] ?: ''), ' ·')];
    }
    $html = '<table style="border-collapse:collapse;width:100%">';
    foreach ($filas as $k => $v) {
        $html .= '<tr><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb;color:#5a6873;width:38%">' . h($k) . '</td><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb"><b>' . h((string) $v) . '</b></td></tr>';
    }
    return $html . '</table>';
}

function avisar_pago(array $p): void
{
    $c = cfg();
    $n = $c['negocio'];
    enviar_correo($c['correo_avisos'], "Nuevo pedido pagado {$p['ref']} — " . cop((int) $p['total']),
        '<h2 style="margin:0 0 8px">Nuevo pedido pagado</h2><p>Ya está pagado en Wompi. Despáchalo con estos datos:</p>' . tabla_pedido($p, true)
        . '<p><a href="' . h(base_url()) . '/admin.php">Ver todos los pedidos</a></p>');
    $que = $p['entrega'] === 'transportadora'
        ? 'Lo despachamos por transportadora y te llega en unos 2 días hábiles. Te enviamos el número de guía a este correo.'
        : 'Te llamamos al ' . h($p['tel']) . ' para acordar el día y la hora de la entrega' . ($p['entrega'] === 'instalacion' ? ' y la instalación' : '') . '.';
    enviar_correo($p['email'], "Recibimos tu pago — pedido {$p['ref']}",
        '<h2 style="margin:0 0 8px">¡Gracias por tu compra, ' . h(explode(' ', $p['nombre'])[0]) . '!</h2><p>Recibimos tu pago. ' . $que . '</p>' . tabla_pedido($p, false)
        . '<p style="color:#5a6873;font-size:13px">¿Dudas? Responde este correo o escríbenos a ' . h($n['correo']) . ' (' . h($n['horario']) . ').<br>' . h($n['nombre']) . ' · ' . h($n['titular']) . ' · ' . h($n['documento']) . '</p>');
}
