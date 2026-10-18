<?php
declare(strict_types=1);
// Funciones comunes de la tienda: configuración, base de datos, Wompi y correos.

function cfg(): array
{
    static $c = null;
    if ($c === null) {
        $f = __DIR__ . '/config.php';
        $c = is_file($f) ? require $f : require __DIR__ . '/config.sample.php';
        // En el sitio de una marca el nombre que ve el cliente es el de la tienda de la marca (ej. «Filtros GE»)
        $m = dirname(__DIR__) . '/purofiltro-marca.json';
        if (is_file($m) && ($j = json_decode((string) file_get_contents($m), true)) && !empty($j['tienda'])) $c['negocio']['nombre'] = $j['tienda'];
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

// Medios de pago que acepta la pasarela (se muestran como sellos de confianza)
function medios_pago_html(): string
{
    $m = ['Visa', 'Mastercard', 'American Express', 'PSE', 'Nequi', 'Bancolombia'];
    return '<div class="medios" aria-label="Medios de pago">' . implode('', array_map(fn($x) => '<span>' . $x . '</span>', $m)) . '</div>';
}

// Datos de ejemplo de config.sample.php que no se pueden quedar en la tienda publicada
function datos_sin_llenar(): array
{
    $c = cfg(); $n = $c['negocio']; $falta = [];
    $ej = ['titular' => 'Nombre del titular', 'documento' => '000.000.000', 'direccion' => 'Dirección del negocio', 'telefono' => '300 000 0000', 'correo' => 'tudominio'];
    foreach ($ej as $k => $v) if (str_contains((string) ($n[$k] ?? ''), $v)) $falta[] = "negocio → $k";
    if (str_contains($c['dominio'], 'tudominio')) $falta[] = 'dominio';
    if (str_contains($c['correo_avisos'], 'tucorreo')) $falta[] = 'correo_avisos';
    if (str_contains($c['correo_remitente'], 'tudominio')) $falta[] = 'correo_remitente';
    return $falta;
}

// "Filtros Nevecones Colombia, de Nombre, C.C. ..." solo con los datos que ya están llenos (nunca muestra datos de ejemplo)
function identificacion(): string
{
    $n = cfg()['negocio']; $ok = fn($k, $ej) => trim((string) ($n[$k] ?? '')) !== '' && !str_contains((string) $n[$k], $ej);
    $p = [h($n['nombre'])];
    if ($ok('titular', 'Nombre del titular')) $p[] = 'de ' . h($n['titular']);
    if ($ok('documento', '000.000.000')) $p[] = h($n['documento']);
    $txt = implode(', ', $p) . '.';
    if ($ok('direccion', 'Dirección del negocio')) $txt .= ' Dirección: ' . h($n['direccion']) . '.';
    return $txt;
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
    $pdo->exec('CREATE TABLE IF NOT EXISTS resenas (
        id INTEGER PRIMARY KEY AUTOINCREMENT, ref TEXT UNIQUE, pid TEXT, nombre TEXT, ciudad TEXT, estrellas INTEGER,
        texto TEXT, creado TEXT, visible INTEGER DEFAULT 1)');
    $cols = array_column($pdo->query('PRAGMA table_info(pedidos)')->fetchAll(), 'name');
    if (!in_array('pedida_resena', $cols, true)) $pdo->exec('ALTER TABLE pedidos ADD COLUMN pedida_resena INTEGER DEFAULT 0');
    if (!in_array('items', $cols, true)) $pdo->exec('ALTER TABLE pedidos ADD COLUMN items TEXT');
    if (!in_array('acepto_en', $cols, true)) $pdo->exec('ALTER TABLE pedidos ADD COLUMN acepto_en TEXT');
    $pdo->exec('CREATE TABLE IF NOT EXISTS eventos_wompi (id INTEGER PRIMARY KEY AUTOINCREMENT, recibido TEXT, evento TEXT, ref TEXT, estado TEXT, resultado TEXT)');
    return $pdo;
}

// Enlace firmado para que solo el comprador opine sobre su pedido
function token_resena(string $ref): string
{
    $c = cfg();
    return substr(hash_hmac('sha256', 'resena|' . $ref, $c['wompi']['integridad'] . '|' . $c['admin_clave'] . '|' . $c['cron_clave']), 0, 24);
}

function enlace_resena(string $ref): string
{
    return base_url() . '/opinion.php?r=' . rawurlencode($ref) . '&t=' . token_resena($ref);
}

// Resumen de opiniones visibles de un producto: ['n' => 3, 'prom' => 4.7, 'lista' => [...]]
function resenas(string $pid, int $max = 20): array
{
    try {
        $st = db()->prepare('SELECT nombre, ciudad, estrellas, texto, creado FROM resenas WHERE pid = ? AND visible = 1 ORDER BY creado DESC');
        $st->execute([$pid]);
        $todas = $st->fetchAll();
    } catch (Throwable $e) {
        return ['n' => 0, 'prom' => 0, 'lista' => []];
    }
    $n = count($todas);
    return ['n' => $n, 'prom' => $n ? round(array_sum(array_column($todas, 'estrellas')) / $n, 1) : 0, 'lista' => array_slice($todas, 0, $max)];
}

function estrellas_html(float $v): string
{
    $llenas = (int) round($v);
    return '<span class="stars" aria-label="' . h((string) $v) . ' de 5">' . str_repeat('★', $llenas) . '<span>' . str_repeat('★', 5 - $llenas) . '</span></span>';
}

// Etiqueta de Google Analytics 4, solo si está configurada
// Google Tag Manager (cabeza) + Google Analytics directo si se configuró
function analytics_html(): string
{
    $gtm = preg_replace('/[^A-Z0-9\-]/', '', strtoupper((string) (cfg()['gtm'] ?? '')));
    $html = $gtm === '' ? '' : "<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','$gtm');</script>";
    return $html . analytics_ga4();
}

function gtm_body_html(): string
{
    $gtm = preg_replace('/[^A-Z0-9\-]/', '', strtoupper((string) (cfg()['gtm'] ?? '')));
    return $gtm === '' ? '' : '<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=' . $gtm . '" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>';
}

// Botón flotante de WhatsApp (el clic manda el evento "whatsapp" a Tag Manager desde carrito.js)
function whatsapp_html(): string
{
    $num = preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? ''));
    if (strlen($num) === 10) $num = '57' . $num;
    if ($num === '') return '';
    $txt = rawurlencode('Hola, ' . cfg()['negocio']['nombre'] . '. Quiero asesoría con un filtro de agua para mi nevecón.');
    return '<a class="wa-flot" href="https://wa.me/' . $num . '?text=' . $txt . '" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">'
        . '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.1 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>'
        . '<span>¿Dudas? Escríbenos</span></a>';
}

function analytics_ga4(): string
{
    $id = preg_replace('/[^A-Z0-9\-]/', '', strtoupper((string) (cfg()['ga4'] ?? '')));
    if ($id === '') return '';
    return '<script async src="https://www.googletagmanager.com/gtag/js?id=' . $id . '"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","' . $id . '");</script>';
}

function verificacion_html(): string
{
    $v = preg_replace('/[^A-Za-z0-9_\-]/', '', (string) (cfg()['google_verificacion'] ?? ''));
    return $v === '' ? '' : '<meta name="google-site-verification" content="' . $v . '">';
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

// Líneas del carrito con el precio del servidor. Cada línea: producto suelto (cant 1–10) o pack anual de 2.
function calcular_items(array $items): array
{
    $cat = catalogo()['productos'];
    $lineas = [];
    foreach (array_slice($items, 0, 20) as $it) {
        $pid = (string) ($it['pid'] ?? '');
        if (!isset($cat[$pid])) continue;
        $pack = !empty($it['pack']);
        $cant = max(1, min(10, (int) ($it['cant'] ?? 1)));
        $p = $cat[$pid];
        $unit = $pack ? (int) $p['pack'] : (int) $p['precio'];
        $k = $pid . ($pack ? '#pack' : '');
        if (isset($lineas[$k])) { $lineas[$k]['cant'] = min(10, $lineas[$k]['cant'] + $cant); }
        else $lineas[$k] = ['pid' => $pid, 'nombre' => $p['nombre'], 'ref' => $p['ref'], 'pack' => $pack, 'cant' => $cant, 'unit' => $unit];
    }
    $total = 0; $unidades = 0;
    foreach ($lineas as &$l) { $l['subtotal'] = $l['unit'] * $l['cant']; $total += $l['subtotal']; $unidades += $l['cant'] * ($l['pack'] ? 2 : 1); }
    return ['lineas' => array_values($lineas), 'total' => $total, 'unidades' => $unidades];
}

// ¿Hay llaves de Wompi configuradas? Sin ellas se usan los links de pago de cada producto
function con_llaves(): bool
{
    $w = cfg()['wompi'];
    return str_starts_with($w['public_key'], 'pub_') && !str_contains($w['public_key'], 'XXXX') && $w['integridad'] !== '' && !str_contains($w['integridad'], 'XXXX');
}

// Instalación con costo (hoy no se ofrece en la tienda: se coordina por WhatsApp)
function costo_instalacion(array $lineas, string $entrega): int
{
    if ($entrega !== 'instalacion') return 0;
    $cat = catalogo()['productos'];
    foreach ($lineas as $l) if (($cat[$l['pid']]['ubic'] ?? '') === 'externo') return (int) (cfg()['instalacion_externo'] ?? 30000);
    return 0;
}

function lineas_pedido(array $p): array
{
    $it = json_decode((string) ($p['items'] ?? ''), true);
    if (is_array($it) && $it) return $it;
    return [['pid' => $p['pid'], 'nombre' => $p['producto'], 'ref' => $p['refprod'], 'pack' => (bool) $p['pack'], 'cant' => $p['pack'] ? 1 : (int) $p['unidades'], 'unit' => 0, 'subtotal' => (int) $p['total']]];
}

function linea_txt(array $l): string
{
    return $l['cant'] . ' × ' . $l['nombre'] . ' (ref. ' . $l['ref'] . ')' . ($l['pack'] ? ' — pack anual de 2' : '');
}

function entrega_txt(string $e): string
{
    return ['instalacion' => 'Domicilio + instalación', 'domicilio' => 'Domicilio', 'transportadora' => 'Envío por transportadora'][$e] ?? $e;
}

// Envío por SMTP (el buzón de tu dominio en Hostinger). Es mucho más confiable que mail(), que muchos hosting bloquean o mandan a spam.
// Devuelve '' si salió bien o el motivo del error.
function smtp_enviar(string $para, string $asunto, string $html, string $de, string $nombre, string $responder): string
{
    $s = cfg()['smtp'] ?? [];
    $host = (string) ($s['host'] ?? ''); $puerto = (int) ($s['puerto'] ?? 465); $user = (string) ($s['usuario'] ?? ''); $clave = (string) ($s['clave'] ?? '');
    if ($host === '' || $user === '' || $clave === '') return 'SMTP sin configurar';
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client(($puerto === 465 ? 'ssl://' : 'tcp://') . $host . ':' . $puerto, $en, $es, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) return "No se pudo conectar a $host:$puerto ($es)";
    stream_set_timeout($fp, 15);
    $leer = function () use ($fp): string { $r = ''; while (($l = fgets($fp, 515)) !== false) { $r .= $l; if (strlen($l) < 4 || $l[3] === ' ') break; } return $r; };
    $cmd = function (string $c, string $esp) use ($fp, $leer): ?string { fwrite($fp, $c . "\r\n"); $r = $leer(); return str_starts_with($r, $esp) ? null : trim($r); };
    $r = $leer();
    if (!str_starts_with($r, '220')) { fclose($fp); return 'Respuesta inesperada: ' . trim($r); }
    $dom = parse_url(base_url(), PHP_URL_HOST) ?: 'localhost';
    if ($e = $cmd("EHLO $dom", '250')) { fclose($fp); return "EHLO: $e"; }
    if ($puerto === 587) {
        if ($e = $cmd('STARTTLS', '220')) { fclose($fp); return "STARTTLS: $e"; }
        if (!@stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) { fclose($fp); return 'No se pudo activar TLS'; }
        if ($e = $cmd("EHLO $dom", '250')) { fclose($fp); return "EHLO: $e"; }
    }
    if ($e = $cmd('AUTH LOGIN', '334') ?? $cmd(base64_encode($user), '334') ?? $cmd(base64_encode($clave), '235')) { fclose($fp); return "Usuario o clave del correo incorrectos: $e"; }
    if ($e = $cmd("MAIL FROM:<$de>", '250')) { fclose($fp); return "MAIL FROM: $e"; }
    if ($e = $cmd("RCPT TO:<$para>", '25')) { fclose($fp); return "RCPT TO: $e"; }
    if ($e = $cmd('DATA', '354')) { fclose($fp); return "DATA: $e"; }
    $cab = ['Date: ' . date('r'), 'From: =?UTF-8?B?' . base64_encode($nombre) . "?= <$de>", "To: <$para>", "Reply-To: $responder", 'Subject: =?UTF-8?B?' . base64_encode($asunto) . '?=',
        'Message-ID: <' . bin2hex(random_bytes(8)) . "@$dom>", 'MIME-Version: 1.0', 'Content-Type: text/html; charset=UTF-8', 'Content-Transfer-Encoding: base64'];
    $cuerpo = chunk_split(base64_encode($html));
    if ($e = $cmd(implode("\r\n", $cab) . "\r\n\r\n" . $cuerpo . "\r\n.", '250')) { fclose($fp); return "Envío: $e"; }
    $cmd('QUIT', '221');
    fclose($fp);
    return '';
}

// $motivo (opcional) recibe por qué falló, para mostrarlo en el diagnóstico
function enviar_correo(string $para, string $asunto, string $html, ?string &$motivo = null): bool
{
    $c = cfg();
    $de = $c['correo_remitente'];
    $nombre = $c['negocio']['nombre'];
    $cuerpo = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#15212b;max-width:560px">' . $html . '</div>';
    $ok = false;
    $motivo = '';
    if (!filter_var($para, FILTER_VALIDATE_EMAIL)) $motivo = 'El correo de destino no es válido: «' . $para . '»';
    else {
        $e = smtp_enviar($para, $asunto, $cuerpo, $de, $nombre, $c['negocio']['correo']);
        if ($e === '') $ok = true;
        else {
            $motivo = $e;
            $headers = implode("\r\n", ['MIME-Version: 1.0', 'Content-Type: text/html; charset=UTF-8', 'From: =?UTF-8?B?' . base64_encode($nombre) . "?= <$de>", 'Reply-To: ' . $c['negocio']['correo']]);
            $ok = (bool) @mail($para, '=?UTF-8?B?' . base64_encode($asunto) . '?=', $cuerpo, $headers, '-f' . $de);
            if ($ok) $motivo = ($e === 'SMTP sin configurar' ? '' : $e . ' — se envió con mail()');
            elseif ($e === 'SMTP sin configurar') $motivo = 'mail() no pudo enviarlo y el SMTP no está configurado';
        }
    }
    if (!$ok) {
        // Sin servidor de correo (o en pruebas) queda guardado aquí para no perderlo
        @file_put_contents(__DIR__ . '/../data/correos.log', date('c') . " PARA: $para\nASUNTO: $asunto\nMOTIVO: $motivo\n" . strip_tags(preg_replace('/<a [^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/s', '$2 ($1)', str_replace(['<br>', '</p>', '</tr>'], "\n", $html))) . "\n----\n", FILE_APPEND);
    }
    return $ok;
}

function tabla_pedido(array $p, bool $completo): string
{
    $filas = [
        'Pedido' => $p['ref'], 'Productos' => implode("\n", array_map('linea_txt', lineas_pedido($p))),
        'Total pagado' => cop((int) $p['total']), 'Entrega' => entrega_txt($p['entrega']), 'Ciudad' => $p['ciudad'],
    ];
    if ($completo) {
        $filas += ['Nombre' => $p['nombre'], 'Celular' => $p['tel'], 'Correo' => $p['email'], 'Barrio' => $p['barrio'], 'Dirección' => $p['dir'],
            'Indicaciones' => $p['indicaciones'] ?: '—', 'Modelo del nevecón' => $p['modelo'] ?: '—', 'Recordatorio de cambio' => $p['recordar'] ? 'Sí' : 'No',
            'Pago Wompi' => trim(($p['metodo'] ?: '') . ' · ' . ($p['tx_id'] ?: ''), ' ·')];
    }
    $html = '<table style="border-collapse:collapse;width:100%">';
    foreach ($filas as $k => $v) {
        $html .= '<tr><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb;color:#5a6873;width:38%">' . h($k) . '</td><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb"><b>' . nl2br(h((string) $v)) . '</b></td></tr>';
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
