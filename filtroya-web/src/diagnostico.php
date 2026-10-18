<?php
declare(strict_types=1);
// Diagnóstico de la pasarela de pagos: solo con la sesión del panel de pedidos.
require __DIR__ . '/partes.php';
session_set_cookie_params(['httponly' => true, 'samesite' => 'Strict', 'secure' => str_starts_with(base_url(), 'https')]);
session_start();
header('X-Robots-Tag: noindex');
if (empty($_SESSION['ok'])) { header('Location: /admin.php'); exit; }

$c = cfg();
$w = $c['wompi'];
$pk = (string) $w['public_key'];
$prod = str_starts_with($pk, 'pub_prod_');
$filas = [];
$ok = function (string $t, string $d) use (&$filas) { $filas[] = ['ok', $t, $d]; };
$mal = function (string $t, string $d) use (&$filas) { $filas[] = ['bad', $t, $d]; };
$aviso = function (string $t, string $d) use (&$filas) { $filas[] = ['warn', $t, $d]; };

// 1. Sitio
base_url() && str_starts_with(base_url(), 'https') ? $ok('Sitio con HTTPS', 'Wompi exige HTTPS para cobrar de verdad.') : $aviso('Sitio sin HTTPS', 'Activa el certificado SSL en Hostinger antes de cobrar.');
$host = parse_url(base_url(), PHP_URL_HOST); $dom = parse_url((string) $c['dominio'], PHP_URL_HOST);
$host === $dom ? $ok('Dominio de config.php', 'Coincide con el que estás usando: ' . h((string) $dom)) : $aviso('El dominio de config.php no coincide', 'config.php dice «' . h((string) $dom) . '» y estás entrando por «' . h((string) $host) . '». Los correos usarán el de config.php.');
$falta = datos_sin_llenar();
$falta ? $mal('Datos del negocio sin llenar', 'Faltan: ' . h(implode(', ', $falta))) : $ok('Datos del negocio', 'Titular, documento, dirección, teléfono y correos llenos.');

// 2. Llaves de Wompi
if (!con_llaves()) {
    $aviso('Sin llaves de Wompi', 'La tienda usa los links de pago de cada producto (una unidad a la vez). Pon tus llaves en config.php para cobrar el carrito completo.');
} else {
    $ok('Modo de Wompi', $prod ? '<b>PRODUCCIÓN</b>: se cobra de verdad.' : '<b>PRUEBAS</b>: no se cobra. Cambia a llaves pub_prod_ cuando todo funcione.');
    $int = (string) $w['integridad']; $ev = (string) $w['eventos'];
    $coincide = $prod ? (str_starts_with($int, 'prod_integrity_') && str_starts_with($ev, 'prod_events_')) : (str_starts_with($int, 'test_integrity_') && str_starts_with($ev, 'test_events_'));
    $coincide ? $ok('Las 3 llaves son del mismo modo', 'Pública, secreto de integridad y secreto de eventos.') : $mal('Las llaves mezclan pruebas y producción', 'Las tres llaves tienen que ser de prueba o las tres de producción.');
    // 3. Conexión con Wompi
    $ch = curl_init(wompi_api() . '/merchants/' . rawurlencode($pk));
    curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15]);
    $res = curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE); curl_close($ch);
    $m = $code === 200 ? (json_decode((string) $res, true)['data'] ?? null) : null;
    $m ? $ok('Wompi reconoce tu llave pública', 'Comercio: <b>' . h((string) ($m['name'] ?? '')) . '</b> (' . h(wompi_api()) . ')') : $mal('Wompi no reconoce la llave pública', 'Respuesta ' . $code . ' de ' . h(wompi_api()) . '. Revisa que la copiaste completa y que el servidor puede salir a internet.');
}
$url_eventos = base_url() . rtrim(dirname($_SERVER['SCRIPT_NAME']), '/') . '/filtrosnevecones-api/wompi.php';
$aviso('URL de eventos que debe tener Wompi', 'En Wompi > Desarrolladores > URL de eventos pon: <code>' . h($url_eventos) . '</code>');

// 4. Servidor
try { db()->query('SELECT 1'); is_writable(__DIR__ . '/filtrosnevecones-data') || is_writable(__DIR__ . '/data') ? $ok('Base de pedidos', 'Se puede leer y escribir.') : $mal('La carpeta de datos no se puede escribir', 'Dale permisos de escritura a filtrosnevecones-data.'); }
catch (Throwable $e) { $mal('Base de pedidos', h($e->getMessage())); }
function_exists('curl_init') ? $ok('cURL disponible', 'Necesario para consultar a Wompi.') : $mal('Falta cURL', 'Pide a Hostinger activar la extensión cURL de PHP.');
$prueba = null;
$formulario = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? '')) && isset($_POST['probar_formulario'])) {
    $formulario = enviar_formulario('Prueba del formulario de pedidos — ' . $c['negocio']['nombre'], ['Pedido' => 'PRUEBA', 'Nombre' => 'Cliente de prueba', 'Celular' => '3000000000', 'Ciudad' => 'Cali', 'Direccion' => 'Calle de prueba', 'Productos' => '1 × Filtro de prueba']);
}
if ($_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? '')) && isset($_POST['probar_correo'])) {
    $r = enviar_correo(correo_destino(), 'Prueba de correo — ' . $c['negocio']['nombre'], '<h2 style="margin:0 0 8px">Prueba de correo</h2><p>Si lees esto, los pedidos con los datos del cliente te van a llegar a este correo.</p>', $motivo);
    $prueba = [$r, (string) $motivo];
}
$smtp = $c['smtp'] ?? [];
(($smtp['clave'] ?? '') !== '' && ($smtp['usuario'] ?? '') !== '') ? $ok('SMTP configurado', 'Usuario ' . h((string) $smtp['usuario']) . ' en ' . h((string) $smtp['host']) . ':' . (int) $smtp['puerto'])
    : $mal('SMTP sin configurar', 'Sin él, los correos dependen de mail() y muchas veces NO llegan. En config.php llena <b>smtp → clave</b> con la clave del buzón pedidos@ que creaste en Hostinger.');
$ok('Correo donde llegan los pedidos', h(correo_destino()));
function_exists('mail') ? $ok('Envío de correo', 'Función mail() disponible. Haz una compra de prueba para confirmar que llegan los correos.') : $mal('Sin envío de correo', 'mail() no está disponible.');
(string) $c['cron_clave'] !== '' ? $ok('Clave del cron', 'Definida.') : $aviso('Falta cron_clave', 'Sin ella no se pueden usar las tareas programadas por URL.');

// 5. Actividad reciente
$n = (int) db()->query("SELECT COUNT(*) FROM pedidos WHERE estado = 'pendiente' AND creado < '" . date('c', time() - 1800) . "'")->fetchColumn();
$n ? $aviso("$n pedido(s) pendiente(s) hace más de 30 minutos", 'Puede ser gente que no terminó de pagar. La tarea «reconciliar» los revisa en Wompi cada 15 minutos.') : $ok('Pedidos pendientes', 'Ninguno antiguo sin resolver.');
$ev = db()->query('SELECT recibido, evento, ref, estado, resultado FROM eventos_wompi ORDER BY id DESC LIMIT 10')->fetchAll();
cabeza('Diagnóstico de pagos | ' . $c['negocio']['nombre'], 'Diagnóstico de pagos', '/diagnostico.php', '', false);
echo '<h1>Diagnóstico de pagos</h1><p class="m"><a href="/admin.php">← Volver a los pedidos</a></p><div style="display:flex;flex-direction:column;gap:8px">';
foreach ($filas as [$tipo, $t, $d]) {
    $ico = ['ok' => '✅', 'warn' => '⚠️', 'bad' => '❌'][$tipo];
    echo '<div class="caja" style="display:flex;gap:12px"><span aria-hidden="true">' . $ico . '</span><div><b>' . h($t) . '</b><br><span class="m">' . $d . '</span></div></div>';
}
echo '</div><h2>Prueba de correo</h2><form method="post" class="caja"><input type="hidden" name="csrf" value="' . h($_SESSION['csrf'] ?? '') . '"><p class="m">Manda un correo de prueba a <b>' . h(correo_destino()) . '</b>.</p><button class="btn sm" name="probar_correo" value="1">Enviar correo de prueba</button>'
    . ($prueba ? '<p style="margin-top:10px">' . ($prueba[0] ? '✅ Enviado' . ($prueba[1] ? ' (' . h($prueba[1]) . ')' : '') . '. Revisa la bandeja y el spam.' : '❌ No se pudo enviar: <b>' . h($prueba[1]) . '</b>') . '</p>' : '') . '</form>';
echo '<h2>Datos del pedido como formulario (FormSubmit)</h2><form method="post" class="caja"><input type="hidden" name="csrf" value="' . h($_SESSION['csrf'] ?? '') . '"><p class="m">Cada pedido también se manda a <b>' . h(correo_destino()) . '</b> como un formulario. La primera vez FormSubmit te manda un correo para activarlo: toca <b>Activate Form</b>. Después de eso llegan solos.</p><button class="btn sm" name="probar_formulario" value="1">Enviar formulario de prueba</button>'
    . ($formulario ? '<p style="margin-top:10px">' . ($formulario['ok'] ? '✅ Enviado: ' : '❌ ') . h($formulario['mensaje']) . '</p>' : '') . '</form>';
echo '<h2>Tareas programadas (Hostinger > Avanzado > Cron Jobs)</h2><div class="caja"><p class="m">Cada 15 minutos (revisa pagos que no llegaron por aviso):</p><code>/usr/bin/php /home/USUARIO/public_html/filtrosnevecones-api/reconciliar.php</code>'
    . '<p class="m" style="margin-top:12px">Una vez al día (recordatorios y opiniones):</p><code>/usr/bin/php /home/USUARIO/public_html/filtrosnevecones-api/recordatorios.php</code></div>';
$av = db()->query('SELECT creado, ref, tipo, canal, ok, mensaje FROM avisos ORDER BY id DESC LIMIT 12')->fetchAll();
echo '<h2>Avisos de pedidos enviados a tu correo</h2>';
if (!$av) echo '<p class="m">Todavía no se ha enviado ningún aviso de pedido.</p>';
else {
    echo '<div class="caja" style="overflow-x:auto"><table class="t"><tr><th>Fecha</th><th>Pedido</th><th>Tipo</th><th>Canal</th><th>Resultado</th></tr>';
    foreach ($av as $r) echo '<tr><td>' . h($r['creado']) . '</td><td>' . h($r['ref']) . '</td><td>' . h($r['tipo']) . '</td><td>' . h($r['canal']) . '</td><td>' . ($r['ok'] ? '✅ ' : '❌ ') . h($r['mensaje']) . '</td></tr>';
    echo '</table></div>';
}
echo '<h2>Últimos avisos de Wompi</h2>';
if (!$ev) echo '<p class="m">Todavía no ha llegado ningún aviso. Haz una compra de prueba con llaves pub_test_.</p>';
else {
    echo '<div class="caja" style="overflow-x:auto"><table class="t"><tr><th>Fecha</th><th>Evento</th><th>Pedido</th><th>Estado</th><th>Resultado</th></tr>';
    foreach ($ev as $r) echo '<tr><td>' . h($r['recibido']) . '</td><td>' . h($r['evento']) . '</td><td>' . h($r['ref']) . '</td><td>' . h($r['estado']) . '</td><td>' . h($r['resultado']) . '</td></tr>';
    echo '</table></div>';
}
pie();
