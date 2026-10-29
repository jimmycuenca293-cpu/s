<?php
declare(strict_types=1);
// API de la instalación a domicilio: horarios libres (GET ?a=dias), reservar (POST ?a=reservar) y avisar que ya pagó (POST ?a=pagado).
require __DIR__ . '/instalacion-lib.php';

$a = (string) ($_GET['a'] ?? '');
if ($a === 'dias') out(['ahora' => inst_ahora()->format('c'), 'ts' => time(), 'anticipacion' => inst_config()['anticipacion_horas'], 'dias' => inst_agenda()]);

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail('Método no permitido.', 405);
$raw = file_get_contents('php://input', false, null, 0, 20001);
if ($raw === false || strlen($raw) > 20000) fail('Petición no válida.');
$b = json_decode($raw, true);
if (!is_array($b)) fail('Petición no válida.');
$origen = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
if ($origen !== '' && parse_url($origen, PHP_URL_HOST) !== parse_url(base_url(), PHP_URL_HOST)) fail('Origen no permitido.', 403);
// IP real del cliente (el hosting puede ir detrás de un proxy)
$ip = trim(explode(',', (string) ($_SERVER['HTTP_CF_CONNECTING_IP'] ?? $_SERVER['HTTP_X_FORWARDED_FOR'] ?? $_SERVER['REMOTE_ADDR'] ?? ''))[0]);

if ($a === 'pagado') {
    $r = inst_buscar((string) ($b['ref'] ?? ''));
    if (!$r || !hash_equals(inst_token($r['ref']), (string) ($b['t'] ?? ''))) fail('No encontramos esa reserva.', 404);
    if ($r['estado'] === 'esperando_pago' && !(int) $r['avisado_pago']) {
        inst_db()->prepare('UPDATE instalaciones SET avisado_pago = 1 WHERE ref = ?')->execute([$r['ref']]);
        out_y_seguir(['ok' => true], fn() => inst_avisar($r, 'pago-avisado', 'EL CLIENTE DICE QUE YA PAGÓ ' . (($r['forma_pago'] ?? 'reserva') === 'total' ? 'EL TOTAL' : 'la reserva') . ' ' . $r['ref'] . ' — revisa Wompi y confírmala',
            '<h2 style="margin:0 0 8px">El cliente avisó que ya pagó la reserva</h2><p>Revisa en tu panel de Wompi que el pago de ' . h(cop((int) $r['reserva'])) . ($r['forma_pago'] === 'total' ? ' (pago del total)' : ' (reserva)') . ' entró (busca el nombre o el correo del cliente) y luego confirma la reserva en tu panel.</p>'
            . inst_tabla($r, true) . '<p><a href="' . h(base_url()) . '/admin-instalaciones.php">Abrir el panel de instalaciones</a></p>'));
    }
    out(['ok' => true]);
}
if ($a !== 'reservar') fail('Petición no válida.');

if (!empty($b['web'])) out(['ok' => true]);   // campo trampa para robots
if (empty($b['acepto'])) fail('Acepta las condiciones del servicio y la política de datos para continuar.');
$c = inst_config();
$serv = (string) ($b['servicio'] ?? ''); $zona = (string) ($b['zona'] ?? ''); $metros = (string) ($b['metros'] ?? '5');
$P = inst_precio($serv, $zona, $metros);
if (!$P) fail('Escoge el servicio, la zona y la distancia de la manguera.');
if ((int) ($b['total'] ?? -1) !== $P['total']) fail('El precio se actualizó. Recarga la página para ver el valor correcto.', 409);

$t = fn(string $k, int $max = 160) => mb_substr(trim((string) ($b[$k] ?? '')), 0, $max);
$fecha = $t('fecha', 10); $franja = (int) ($b['franja'] ?? -1);
if (!in_array($fecha, inst_fechas(), true) || $franja < 0 || $franja >= count($c['franjas'])) fail('Escoge un día y una hora disponibles.');
if (!inst_slot_futuro($fecha, $franja)) fail('Ese horario ya no está disponible: faltan menos de ' . $c['anticipacion_horas'] . ' horas. Escoge otro, por favor.', 409);
$forma = $t('forma_pago', 10) === 'total' ? 'total' : 'reserva';
// Pago total: en línea va el combo completo (precio del servicio); el recargo de zona y la manguera adicional se pagan en efectivo al terminar
$online = $forma === 'total' ? inst_total_online($serv, $zona)[0] : $P['reserva'];
$v = ['servicio' => $serv, 'zona' => $zona, 'metros' => $metros, 'total' => $P['total'], 'reserva' => $online, 'saldo' => $P['total'] - $online, 'fecha' => $fecha, 'franja' => $franja,
    'marca_nevecon' => $t('marca_nevecon', 40), 'modelo' => $t('modelo', 40), 'toma' => in_array($t('toma', 20), ['llave', 'tubo', 'lavaplatos', 'nose'], true) ? $t('toma', 20) : 'nose',
    'nombre' => $t('nombre', 80), 'email' => $t('email', 120), 'tel' => preg_replace('/\D/', '', $t('tel', 20)), 'barrio' => $t('barrio', 80), 'dir' => $t('dir', 160),
    'detalle' => $t('detalle', 160), 'notas' => $t('notas', 300), 'ip' => $ip, 'forma_pago' => $forma];
if (strlen($v['tel']) === 12 && str_starts_with($v['tel'], '57')) $v['tel'] = substr($v['tel'], 2);
if (mb_strlen($v['nombre']) < 3) fail('Escribe tu nombre completo.');
if (!filter_var($v['email'], FILTER_VALIDATE_EMAIL)) fail('Escribe un correo válido.');
if (!preg_match('/^3\d{9}$/', $v['tel'])) fail('Escribe un celular válido (10 dígitos que empiezan por 3).');
if ($v['barrio'] === '' || mb_strlen($v['dir']) < 5) fail('Escribe el barrio y la dirección completa.');
if ($v['marca_nevecon'] === '') fail('Escoge la marca de tu nevecón.');

// Freno contra abusos: máximo 8 reservas sin pagar por hora desde la misma conexión
$st = inst_db()->prepare("SELECT COUNT(*) FROM instalaciones WHERE ip = ? AND estado = 'esperando_pago' AND creado > ?");
$st->execute([$ip, date('c', time() - 3600)]);
if ((int) $st->fetchColumn() >= 8) fail('Demasiados intentos. Espera un rato o escríbenos por WhatsApp.', 429);

$ref = inst_crear($v);
if ($ref === '') fail('Ese horario se acaba de ocupar. Escoge otro, por favor.', 409);
$r = inst_buscar($ref);
$asunto = ($v['forma_pago'] === 'total' ? 'PAGA EL TOTAL · ' : '') . 'NUEVA INSTALACIÓN ' . $ref . ' — ' . inst_fecha_txt($fecha, false) . ' ' . inst_franja_txt($franja) . ' — ' . $c['zonas'][$zona]['nombre'] . ' — ' . $v['nombre'];
out_y_seguir(['ok' => true, 'ref' => $ref, 'url' => inst_url_reserva($ref), 'total' => $P['total'], 'reserva' => $online], function () use ($r, $asunto) {
    inst_avisar($r, 'reserva', $asunto, '<h2 style="margin:0 0 8px">Nueva instalación agendada</h2><p>' . ($r['forma_pago'] === 'total' ? '<b>El cliente va a pagar el TOTAL en línea (' . cop((int) $r['reserva']) . ') con el link de Wompi de su servicio.</b> ' : '') . 'El cliente quedó en la pantalla para pagar. El horario está apartado por ' . INST_RETENER_MIN . ' minutos; cuando veas el pago en Wompi, confírmala en tu panel.</p>'
        . inst_tabla($r, true) . '<p><b>Recuerda:</b> apenas confirmes el pago, escríbele por WhatsApp para confirmar la instalación y darle el nombre del técnico. <a href="https://wa.me/57' . h($r['tel']) . '">Escribirle al cliente por WhatsApp</a> · <a href="' . h(base_url()) . '/admin-instalaciones.php">Abrir el panel de instalaciones</a></p>');
    inst_correo_cliente($r);
});
