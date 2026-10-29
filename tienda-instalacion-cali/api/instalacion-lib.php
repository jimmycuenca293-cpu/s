<?php
declare(strict_types=1);
// Instalación a domicilio del kit de agua del nevecón (Cali y Jamundí): precios, agenda y reservas.
require_once __DIR__ . '/lib.php';
date_default_timezone_set('America/Bogota');

const INST_RETENER_MIN = 60;
const INST_RETENER_PAGO_HORAS = 24;   // si el cliente avisó «ya pagué», el horario se aparta hasta que el técnico confirme (máx. este tiempo)   // una reserva sin pagar aparta el horario este tiempo; pagada, lo aparta hasta que se complete o se cancele

function inst_config(): array
{
    static $c = null;
    if ($c !== null) return $c;
    $f = fn(string $m, string $r, string $img) => ['marca' => $m, 'ref' => $r, 'img' => $img];
    $base = [
        'servicios' => [
            'basica'           => ['nombre' => 'Instalación básica', 'corto' => 'Solo instalación', 'precio' => 137900, 'reserva' => 60000, 'filtro' => null],
            'filtro-samsung'   => ['nombre' => 'Instalación con filtro externo Samsung', 'corto' => 'Con filtro Samsung', 'precio' => 169900, 'reserva' => 90000, 'filtro' => $f('Samsung', 'DA29-10105J', 'sam-ex-o')],
            'filtro-lg'        => ['nombre' => 'Instalación con filtro externo LG', 'corto' => 'Con filtro LG', 'precio' => 169900, 'reserva' => 90000, 'filtro' => $f('LG', 'ADQ73693903', 'lg-ex-o')],
            'filtro-whirlpool' => ['nombre' => 'Instalación con filtro externo Whirlpool', 'corto' => 'Con filtro Whirlpool', 'precio' => 179900, 'reserva' => 100000, 'filtro' => $f('Whirlpool', '4378411RB', 'wp-ex-o')],
        ],
        'zonas' => ['cali' => ['nombre' => 'Cali', 'recargo' => 0], 'jamundi' => ['nombre' => 'Jamundí', 'recargo' => 20000]],
        'metro_extra' => 14000,   // cada 5 m de manguera adicionales a los 5 m incluidos
        'franjas' => [[8, 0, 9, 30], [9, 30, 11, 0], [11, 0, 12, 30], [13, 30, 15, 0], [15, 30, 17, 0]],
        'dias_adelante' => 28,
        'anticipacion_horas' => 3,   // un horario se ofrece solo si empieza dentro de más de estas horas
        'bloqueados' => [],        // fechas sin servicio: ['2026-12-08', ...]
        'links' => ['basica' => '', 'filtro-samsung' => '', 'filtro-lg' => '', 'filtro-whirlpool' => ''],
        'links_total' => ['basica' => '', 'filtro-samsung' => '', 'filtro-lg' => '', 'filtro-whirlpool' => ''],   // links de pago del combo COMPLETO (uno por servicio)
    ];
    // Ajustes propios de la instalación (links de pago de la reserva, clave del panel, fechas sin servicio): instalacion-ajustes.php
    $f = __DIR__ . '/instalacion-ajustes.php';
    $o = is_file($f) && is_array($a = require $f) ? $a : [];
    foreach (['servicios', 'zonas', 'links', 'links_total'] as $k) if (isset($o[$k]) && is_array($o[$k])) $base[$k] = array_replace_recursive($base[$k], $o[$k]);
    foreach (['metro_extra', 'dias_adelante', 'anticipacion_horas'] as $k) if (isset($o[$k])) $base[$k] = (int) $o[$k];
    if (isset($o['bloqueados']) && is_array($o['bloqueados'])) $base['bloqueados'] = array_values($o['bloqueados']);
    $base['clave_panel'] = (string) ($o['clave_panel'] ?? '');
    return $c = $base;
}

function inst_db(): PDO
{
    $pdo = db();
    $pdo->exec('CREATE TABLE IF NOT EXISTS instalaciones (
        ref TEXT PRIMARY KEY, creado TEXT NOT NULL, estado TEXT NOT NULL DEFAULT "esperando_pago",
        servicio TEXT, total INTEGER, reserva INTEGER, saldo INTEGER, fecha TEXT, franja INTEGER,
        zona TEXT, metros TEXT, marca_nevecon TEXT, modelo TEXT, toma TEXT, nombre TEXT, email TEXT, tel TEXT,
        barrio TEXT, dir TEXT, detalle TEXT, notas TEXT, ip TEXT, pagado_en TEXT, nota_tecnico TEXT, avisado_pago INTEGER DEFAULT 0)');
    $cols = array_column($pdo->query('PRAGMA table_info(instalaciones)')->fetchAll(), 'name');
    if (!in_array('tx_id', $cols, true)) $pdo->exec('ALTER TABLE instalaciones ADD COLUMN tx_id TEXT');
    if (!in_array('forma_pago', $cols, true)) $pdo->exec('ALTER TABLE instalaciones ADD COLUMN forma_pago TEXT DEFAULT "reserva"');
    $pdo->exec('CREATE INDEX IF NOT EXISTS inst_fecha ON instalaciones (fecha, franja)');
    return $pdo;
}

function inst_franja_txt(int $i): string
{
    $f = inst_config()['franjas'][$i] ?? null;
    if (!$f) return '';
    $per = fn(int $h): string => $h >= 12 ? 'p. m.' : 'a. m.';
    $h = fn(int $h, int $m): string => ($h > 12 ? $h - 12 : $h) . ':' . str_pad((string) $m, 2, '0', STR_PAD_LEFT);
    return $per($f[0]) === $per($f[2]) ? $h($f[0], $f[1]) . ' a ' . $h($f[2], $f[3]) . ' ' . $per($f[2])
        : $h($f[0], $f[1]) . ' ' . $per($f[0]) . ' a ' . $h($f[2], $f[3]) . ' ' . $per($f[2]);
}

function inst_fecha_txt(string $ymd, bool $larga = true): string
{
    $d = DateTimeImmutable::createFromFormat('Y-m-d', $ymd, new DateTimeZone('America/Bogota'));
    if (!$d) return $ymd;
    $dias = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];
    $meses = ['', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'];
    $dia = $dias[(int) $d->format('w')];
    return $larga ? ucfirst($dia) . ' ' . (int) $d->format('j') . ' de ' . $meses[(int) $d->format('n')] : mb_substr($dia, 0, 3) . ' ' . (int) $d->format('j');
}

function inst_ahora(): DateTimeImmutable
{
    return new DateTimeImmutable('now', new DateTimeZone('America/Bogota'));
}

function inst_slot_inicio(string $ymd, int $i): ?DateTimeImmutable
{
    $f = inst_config()['franjas'][$i] ?? null;
    if (!$f) return null;
    return DateTimeImmutable::createFromFormat('Y-m-d H:i', $ymd . ' ' . sprintf('%02d:%02d', $f[0], $f[1]), new DateTimeZone('America/Bogota')) ?: null;
}

// Un horario se puede reservar solo si empieza con la anticipación mínima (por defecto 3 horas) desde la hora actual de Colombia
function inst_slot_futuro(string $ymd, int $i): bool
{
    $s = inst_slot_inicio($ymd, $i);
    return $s !== null && $s >= inst_ahora()->modify('+' . inst_config()['anticipacion_horas'] . ' hours');
}

function inst_dia_cerrado(string $ymd): string
{
    $d = DateTimeImmutable::createFromFormat('Y-m-d', $ymd, new DateTimeZone('America/Bogota'));
    if ($d && $d->format('w') === '0') return 'Domingo: sin servicio';
    if (in_array($ymd, inst_config()['bloqueados'], true)) return 'Sin servicio ese día';
    return '';
}

// Días que se pueden reservar: de hoy en adelante, de lunes a sábado, con al menos un horario a tiempo
function inst_fechas(): array
{
    $c = inst_config(); $r = [];
    $d = inst_ahora()->setTime(0, 0);
    for ($i = 0; $i < $c['dias_adelante']; $i++, $d = $d->modify('+1 day')) {
        $y = $d->format('Y-m-d');
        if (inst_dia_cerrado($y) !== '') continue;
        for ($k = 0; $k < count($c['franjas']); $k++) if (inst_slot_futuro($y, $k)) { $r[] = $y; break; }
    }
    return $r;
}

// Horarios ocupados por reservas pagadas o recién creadas (aún dentro del tiempo para pagar)
function inst_ocupados(string $desde, string $hasta): array
{
    $st = inst_db()->prepare("SELECT fecha, franja FROM instalaciones WHERE fecha BETWEEN ? AND ? AND (estado = 'reservada' OR (estado = 'esperando_pago' AND (creado > ? OR (avisado_pago = 1 AND creado > ?))))");
    $st->execute([$desde, $hasta, date('c', time() - INST_RETENER_MIN * 60), date('c', time() - INST_RETENER_PAGO_HORAS * 3600)]);
    $o = [];
    foreach ($st->fetchAll() as $r) $o[$r['fecha'] . '|' . $r['franja']] = true;
    return $o;
}

function inst_agenda(): array
{
    $c = inst_config(); $n = count($c['franjas']);
    $d = inst_ahora()->setTime(0, 0);
    $hasta = $d->modify('+' . ($c['dias_adelante'] - 1) . ' days')->format('Y-m-d');
    $oc = inst_ocupados($d->format('Y-m-d'), $hasta);
    $r = [];
    for ($i = 0; $i < $c['dias_adelante']; $i++, $d = $d->modify('+1 day')) {
        $y = $d->format('Y-m-d'); $cerrado = inst_dia_cerrado($y); $fr = []; $libres = 0;
        for ($k = 0; $k < $n; $k++) {
            $estado = $cerrado !== '' ? 'cerrado' : (!inst_slot_futuro($y, $k) ? 'pasado' : (isset($oc[$y . '|' . $k]) ? 'ocupado' : 'libre'));
            if ($estado === 'libre') $libres++;
            $fr[] = ['i' => $k, 'txt' => inst_franja_txt($k), 'estado' => $estado, 'libre' => $estado === 'libre'];
        }
        $r[] = ['fecha' => $y, 'txt' => inst_fecha_txt($y), 'corto' => inst_fecha_txt($y, false), 'dow' => (int) $d->format('w'), 'dia' => (int) $d->format('j'), 'mes' => (int) $d->format('n'),
            'cerrado' => $cerrado !== '', 'motivo' => $cerrado, 'libres' => $libres, 'franjas' => $fr];
    }
    return $r;
}

// Precio calculado siempre en el servidor
function inst_precio(string $servicio, string $zona, string $metros): ?array
{
    $c = inst_config();
    $s = $c['servicios'][$servicio] ?? null; $z = $c['zonas'][$zona] ?? null;
    if (!$s || !$z || !in_array($metros, ['5', '10', '15', '20', 'nose'], true)) return null;
    $extra = in_array($metros, ['10', '15', '20'], true) ? (((int) $metros - 5) / 5) * $c['metro_extra'] : 0;
    $total = (int) $s['precio'] + (int) $z['recargo'] + (int) $extra;
    return ['servicio' => $s, 'zona' => $z, 'extra' => (int) $extra, 'total' => $total, 'reserva' => (int) $s['reserva'], 'saldo' => $total - (int) $s['reserva']];
}

// Pago completo: devuelve [monto que se paga en línea, link de Wompi]. Cada servicio puede tener un link por zona (el monto incluye el recargo de esa zona)
// o un solo link con el precio base (entonces el recargo de zona se paga en efectivo al terminar).
function inst_total_online(string $servicio, string $zona): array
{
    $c = inst_config(); $precio = (int) ($c['servicios'][$servicio]['precio'] ?? 0); $rec = (int) ($c['zonas'][$zona]['recargo'] ?? 0);
    $l = $c['links_total'][$servicio] ?? '';
    if (is_string($l)) return $l !== '' ? [$precio, $l] : [$precio + $rec, ''];
    if (!empty($l[$zona])) return [$precio + $rec, (string) $l[$zona]];
    $base = (string) ($l['cali'] ?? ''); if ($base !== '') return [$precio, $base];
    return [$precio + $rec, ''];
}

// Link de Wompi que le toca pagar al cliente: la reserva (monto fijo por servicio) o el pago completo
function inst_link_pago(array $r): string
{
    if (($r['forma_pago'] ?? 'reserva') === 'total') return inst_total_online($r['servicio'], $r['zona'])[1];
    return (string) (inst_config()['links'][$r['servicio']] ?? '');
}

function inst_token(string $ref): string
{
    $k = inst_config()['clave_panel'] . 'inst-' . dirname(__DIR__);
    return substr(hash_hmac('sha256', $ref, $k), 0, 16);
}

function inst_url_reserva(string $ref): string
{
    return base_url() . '/instalacion-nevecon-cali/reserva/?ref=' . rawurlencode($ref) . '&t=' . inst_token($ref);
}

function inst_metros_txt(string $m): string
{
    return ['5' => 'Hasta 5 m (incluidos)', '10' => 'Hasta 10 m', '15' => 'Hasta 15 m', '20' => 'Hasta 20 m', 'nose' => 'No sabe: el técnico la mide'][$m] ?? $m;
}

function inst_toma_txt(string $t): string
{
    return ['llave' => 'Llave o toma de agua visible en la cocina', 'tubo' => 'Tubo de agua en la pared', 'lavaplatos' => 'Debajo del lavaplatos', 'nose' => 'No sabe'][$t] ?? $t;
}

// Reserva el horario sin permitir que dos clientes tomen el mismo
function inst_crear(array $v): string
{
    $pdo = inst_db();
    $ref = 'IN-' . date('ymd') . '-' . strtoupper(substr(bin2hex(random_bytes(4)), 0, 6));
    $pdo->exec('BEGIN IMMEDIATE');
    try {
        $oc = inst_ocupados($v['fecha'], $v['fecha']);
        if (isset($oc[$v['fecha'] . '|' . $v['franja']])) { $pdo->exec('ROLLBACK'); return ''; }
        $pdo->prepare('INSERT INTO instalaciones (ref, creado, servicio, total, reserva, saldo, fecha, franja, zona, metros, marca_nevecon, modelo, toma, nombre, email, tel, barrio, dir, detalle, notas, ip)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')->execute([
            $ref, date('c'), $v['servicio'], $v['total'], $v['reserva'], $v['saldo'], $v['fecha'], $v['franja'], $v['zona'], $v['metros'], $v['marca_nevecon'], $v['modelo'], $v['toma'],
            $v['nombre'], $v['email'], $v['tel'], $v['barrio'], $v['dir'], $v['detalle'], $v['notas'], $v['ip']]);
        $pdo->prepare('UPDATE instalaciones SET forma_pago = ? WHERE ref = ?')->execute([$v['forma_pago'] ?? 'reserva', $ref]);
        $pdo->exec('COMMIT');
    } catch (Throwable $e) { try { $pdo->exec('ROLLBACK'); } catch (Throwable $x) {} throw $e; }
    return $ref;
}

function inst_buscar(string $ref): ?array
{
    $st = inst_db()->prepare('SELECT * FROM instalaciones WHERE ref = ?'); $st->execute([$ref]);
    return $st->fetch() ?: null;
}

function inst_estado_txt(string $e): string
{
    return ['esperando_pago' => 'Esperando el pago', 'reservada' => 'Reserva confirmada', 'completada' => 'Instalación completada', 'cancelada' => 'Cancelada'][$e] ?? $e;
}

function inst_resumen_filas(array $r, bool $tecnico): array
{
    $c = inst_config(); $s = $c['servicios'][$r['servicio']] ?? ['nombre' => $r['servicio']]; $z = $c['zonas'][$r['zona']]['nombre'] ?? $r['zona'];
    $f = [
        'Reserva' => $r['ref'], 'Estado' => inst_estado_txt($r['estado']),
        'Servicio' => $s['nombre'], 'Día' => inst_fecha_txt($r['fecha']), 'Hora' => inst_franja_txt((int) $r['franja']),
        'Zona' => $z, 'Dirección' => $r['dir'] . ', ' . $r['barrio'], 'Manguera' => inst_metros_txt($r['metros']),
        'Total de la instalación' => cop((int) $r['total']),
    ] + (($r['forma_pago'] ?? 'reserva') === 'total'
        ? ['Forma de pago' => 'Paga el TOTAL en línea', 'Pagas hoy, en línea (Wompi)' => cop((int) $r['reserva'])] + ((int) $r['saldo'] > 0 ? ['En efectivo al terminar' => cop((int) $r['saldo'])] : [])
        : ['Forma de pago' => 'Reserva en línea y el resto en efectivo al técnico', 'Pagas hoy, en línea' => cop((int) $r['reserva']), 'Resto en efectivo al técnico, al terminar' => cop((int) $r['saldo'])]);
    if ($tecnico) $f += ['Cliente' => $r['nombre'], 'Celular' => $r['tel'], 'Correo' => $r['email'], 'Nevecón' => trim($r['marca_nevecon'] . ' ' . $r['modelo']) ?: '-',
        'Toma de agua' => inst_toma_txt($r['toma']), 'Detalle de la dirección' => $r['detalle'] ?: '-', 'Notas del cliente' => $r['notas'] ?: '-'];
    return $f;
}

function inst_tabla(array $r, bool $tecnico): string
{
    $h = '<table style="border-collapse:collapse;width:100%">';
    foreach (inst_resumen_filas($r, $tecnico) as $k => $v)
        $h .= '<tr><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb;color:#5a6873;width:38%">' . h($k) . '</td><td style="padding:6px 8px;border-bottom:1px solid #e3e8eb"><b>' . nl2br(h((string) $v)) . '</b></td></tr>';
    return $h . '</table>';
}

// Los mismos 13 campos de un pedido normal, para que la hoja de Google de siempre reciba también las instalaciones sin cambiar nada
function inst_campos_hoja(array $r): array
{
    $c = inst_config(); $s = $c['servicios'][$r['servicio']]['nombre'] ?? $r['servicio']; $z = $c['zonas'][$r['zona']]['nombre'] ?? $r['zona'];
    return ['Pedido' => $r['ref'], 'Estado' => 'INSTALACIÓN · ' . inst_estado_txt($r['estado']), 'Nombre' => $r['nombre'], 'Celular' => $r['tel'], 'Correo del cliente' => $r['email'], 'Ciudad' => $z,
        'Barrio' => $r['barrio'], 'Direccion' => $r['dir'] . ($r['detalle'] ? ' (' . $r['detalle'] . ')' : ''),
        'Indicaciones' => trim('Toma de agua: ' . inst_toma_txt($r['toma']) . '. Manguera: ' . inst_metros_txt($r['metros']) . '. ' . ($r['notas'] ?: ''), ' '),
        'Productos' => $s . ' | DÍA: ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']),
        'Total' => cop((int) $r['total']) . (($r['forma_pago'] ?? 'reserva') === 'total' ? ' (PAGA EL TOTAL EN LÍNEA: ' . cop((int) $r['reserva']) . ((int) $r['saldo'] > 0 ? ' + ' . cop((int) $r['saldo']) . ' en efectivo al terminar por recargo de zona o manguera adicional' : '') . ')' : ' (1ª parte ' . cop((int) $r['reserva']) . ' + resto en efectivo al terminar ' . cop((int) $r['saldo']) . ')'),
        'Entrega' => 'Instalación a domicilio el ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']), 'Modelo del nevecon' => trim($r['marca_nevecon'] . ' ' . $r['modelo']) ?: '-'];
}

function inst_hoja(array $campos, string $tipo, string $asunto): array
{
    $h = cfg()['hoja'] ?? [];
    $cuerpo = json_encode(['clave' => (string) ($h['clave'] ?? ''), 'tipo' => $tipo, 'asunto' => $asunto, 'campos' => $campos], JSON_UNESCAPED_UNICODE);
    $ch = curl_init((string) ($h['url'] ?? ''));
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $cuerpo, CURLOPT_RETURNTRANSFER => true, CURLOPT_FOLLOWLOCATION => true, CURLOPT_MAXREDIRS => 5, CURLOPT_TIMEOUT => 20, CURLOPT_HTTPHEADER => ['Content-Type: application/json']]);
    $res = curl_exec($ch); $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE); $err = curl_error($ch); curl_close($ch);
    $j = json_decode((string) $res, true);
    $ok = $code >= 200 && $code < 300 && is_array($j) && !empty($j['ok']);
    return ['ok' => $ok, 'mensaje' => $ok ? '' : (is_array($j) ? (string) ($j['mensaje'] ?? 'Respuesta no válida') : ($err ?: "Respuesta $code"))];
}

// Avisa al técnico (correo + hoja de Google). tipo: 'reserva' o 'pago-avisado' o 'cambio'
function inst_avisar(array $r, string $tipo, string $asunto, string $html): void
{
    $ok = false; $m = '';
    foreach (correos_destino() as $dest) { $x = enviar_correo($dest, $asunto, $html, $mm); $ok = $ok || $x; $m .= $mm ? $dest . ': ' . $mm . ' ' : ''; }
    anotar_aviso($r['ref'], 'inst-' . $tipo, 'correo', $ok, trim($m));
    if (hoja_activa()) { $x = inst_hoja(inst_campos_hoja($r), $tipo, $asunto); anotar_aviso($r['ref'], 'inst-' . $tipo, 'hoja', $x['ok'], $x['mensaje']); }
}

function inst_tel_wa(): string
{
    return substr(preg_replace('/\D/', '', (string) (cfg()['whatsapp'] ?? '3013810242')), -10);
}

// Correo para el cliente: confirma lo que pidió y le dice qué sigue
function inst_correo_cliente(array $r): void
{
    $tel = cfg()['negocio']['telefono'] ?? '301 381 0242';
    $total = ($r['forma_pago'] ?? 'reserva') === 'total';
    if ($r['estado'] === 'esperando_pago') $pagar = '<p><b>Falta un paso:</b> ' . ($total ? 'paga el total (' . h(cop((int) $r['reserva'])) . ')' : 'paga la reserva de ' . h(cop((int) $r['reserva']))) . ' para asegurar tu horario. <a href="' . h(inst_url_reserva($r['ref'])) . '">' . ($total ? 'Pagar ahora' : 'Pagar la reserva') . '</a></p><p>Apenas pagues, <b>un asesor te escribe por WhatsApp</b> para confirmar tu instalación y darte el nombre del técnico.</p>';
    else $pagar = '<p>Tu reserva está confirmada. Un asesor te escribe por WhatsApp para darte el nombre del técnico.</p>';
    $fin = $total ? ((int) $r['saldo'] > 0 ? '<p>Al terminar pagas en efectivo ' . h(cop((int) $r['saldo'])) . ' por el recargo de zona o la manguera adicional. Tienes 1 año de garantía.</p>' : '<p>Pagas todo en línea: al terminar no tienes que pagar nada más. Tienes 1 año de garantía.</p>')
        : '<p>El resto, ' . h(cop((int) $r['saldo'])) . ', lo pagas en efectivo al técnico al terminar la instalación, cuando ya veas el agua funcionando. Tienes 1 año de garantía.</p>';
    $html = '<h2 style="margin:0 0 8px">Tu instalación quedó agendada</h2>' . $pagar . inst_tabla($r, false) . $fin
        . '<p>¿Necesitas cambiar el día o la hora? Avísanos con 24 horas y la reprogramamos sin costo: WhatsApp ' . h($tel) . '.</p>';
    enviar_correo($r['email'], 'Tu instalación ' . $r['ref'] . ': ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']), $html);
}

// Archivo de calendario (.ics) para que el cliente guarde la cita en su celular
function inst_ics(array $r): string
{
    $f = inst_config()['franjas'][(int) $r['franja']] ?? [8, 0, 9, 30];
    $d = str_replace('-', '', $r['fecha']);
    $t = fn(int $h, int $m): string => str_pad((string) $h, 2, '0', STR_PAD_LEFT) . str_pad((string) $m, 2, '0', STR_PAD_LEFT) . '00';
    $esc = fn(string $x): string => str_replace(["\\", ';', ',', "\n"], ['\\\\', '\\;', '\\,', '\\n'], $x);
    $serv = inst_config()['servicios'][$r['servicio']]['nombre'] ?? 'Instalación';
    $l = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Filtros Nevecones//Instalacion//ES', 'CALSCALE:GREGORIAN', 'BEGIN:VEVENT',
        'UID:' . $r['ref'] . '@filtrosnevecones', 'DTSTAMP:' . gmdate('Ymd\THis\Z'),
        'DTSTART;TZID=America/Bogota:' . $d . 'T' . $t($f[0], $f[1]), 'DTEND;TZID=America/Bogota:' . $d . 'T' . $t($f[2], $f[3]),
        'SUMMARY:' . $esc($serv . ' en tu casa'), 'LOCATION:' . $esc($r['dir'] . ', ' . $r['barrio']),
        'DESCRIPTION:' . $esc('Reserva ' . $r['ref'] . ((int) $r['saldo'] > 0 ? '. En efectivo al técnico al terminar: ' . cop((int) $r['saldo']) : '. Todo pagado en línea') . '. WhatsApp ' . (cfg()['negocio']['telefono'] ?? '301 381 0242')),
        'BEGIN:VALARM', 'TRIGGER:-PT1H', 'ACTION:DISPLAY', 'DESCRIPTION:Instalación del agua de tu nevecón en 1 hora', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR'];
    return implode("\r\n", $l) . "\r\n";
}

// Confirma la reserva (pago recibido): queda apartado el horario, le llega el correo al cliente y se te avisa. $via: 'panel' o 'wompi'
function inst_confirmar_reserva(array $r, string $via, string $txid = ''): bool
{
    $st = inst_db()->prepare("SELECT COUNT(*) FROM instalaciones WHERE fecha = ? AND franja = ? AND estado = 'reservada' AND ref <> ?"); $st->execute([$r['fecha'], $r['franja'], $r['ref']]);
    if ((int) $st->fetchColumn() > 0) return false;   // el horario ya lo tiene otra reserva confirmada
    $up = inst_db()->prepare("UPDATE instalaciones SET estado = 'reservada', pagado_en = ?, tx_id = COALESCE(NULLIF(?, ''), tx_id) WHERE ref = ? AND estado = 'esperando_pago'");
    $up->execute([date('c'), $txid, $r['ref']]);
    if ($up->rowCount() !== 1) return true;   // ya estaba confirmada
    $r = inst_buscar($r['ref']);
    $total = ($r['forma_pago'] ?? 'reserva') === 'total';
    enviar_correo($r['email'], 'Reserva confirmada ' . $r['ref'] . ': ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']),
        '<h2 style="margin:0 0 8px">¡Tu reserva está confirmada!</h2><p>Recibimos tu pago. Un asesor te escribe por WhatsApp para darte el nombre del técnico.</p>' . inst_tabla($r, false)
        . ($total ? ((int) $r['saldo'] > 0 ? '<p>Al terminar pagas en efectivo ' . h(cop((int) $r['saldo'])) . ' por el recargo de zona o la manguera adicional. Tienes 1 año de garantía en la instalación.</p>' : '<p>Ya pagaste todo: al terminar no pagas nada más. Tienes 1 año de garantía en la instalación.</p>')
            : '<p>El resto, ' . h(cop((int) $r['saldo'])) . ', lo pagas en efectivo al técnico al terminar. Tienes 1 año de garantía en la instalación.</p>'));
    if ($via === 'wompi') inst_avisar($r, 'pago-confirmado', 'PAGO CONFIRMADO ' . $r['ref'] . ' — ' . inst_fecha_txt($r['fecha'], false) . ' ' . inst_franja_txt((int) $r['franja']) . ' — ' . $r['nombre'],
        '<h2 style="margin:0 0 8px">Wompi confirmó el pago de esta instalación</h2><p>Ya está confirmada la reserva y le llegó el correo al cliente. <b>Escríbele por WhatsApp</b> para confirmar y darle el nombre del técnico.</p>' . inst_tabla($r, true)
        . '<p><a href="https://wa.me/57' . h($r['tel']) . '">Escribirle al cliente</a></p>');
    return true;
}

// Pago de Wompi con link de pago: se busca la reserva por correo (o celular) y monto exacto
function inst_aplicar_pago_link(array $tx): ?array
{
    if (($tx['status'] ?? '') !== 'APPROVED' || ($tx['currency'] ?? 'COP') !== 'COP') return null;
    [$email, $tel, $monto] = datos_pago_link($tx);
    $txid = (string) ($tx['id'] ?? '');
    if ($monto <= 0 || $monto != (int) $monto || $txid === '' || ($email === '' && $tel === '')) return null;
    $ya = inst_db()->prepare('SELECT COUNT(*) FROM instalaciones WHERE tx_id = ?'); $ya->execute([$txid]);
    if ((int) $ya->fetchColumn() > 0) return null;
    $st = inst_db()->prepare("SELECT * FROM instalaciones WHERE estado = 'esperando_pago' AND reserva = ? ORDER BY creado ASC"); $st->execute([(int) $monto]);
    foreach ($st->fetchAll() as $r) {
        if (strtotime((string) $r['creado']) < time() - 5 * 86400) continue;
        if (!(($email !== '' && strtolower((string) $r['email']) === $email) || ($tel !== '' && substr((string) $r['tel'], -10) === $tel))) continue;
        if (inst_confirmar_reserva($r, 'wompi', $txid)) return inst_buscar($r['ref']);
        // Pagó, pero otro cliente ya tiene confirmado ese horario: te avisamos para que lo resuelvas a mano
        inst_avisar($r, 'conflicto', 'REVISAR: pagaron la reserva ' . $r['ref'] . ' pero el horario ya está ocupado',
            '<h2 style="margin:0 0 8px">Pagaron una reserva cuyo horario ya está ocupado</h2><p>Wompi aprobó el pago de ' . h(cop((int) $monto)) . ', pero otra reserva confirmada tiene ese mismo día y hora. Escríbele al cliente para cambiarle el horario y luego confírmala en el panel.</p>' . inst_tabla($r, true));
        return ['ref' => $r['ref'], 'estado' => 'conflicto de horario'];
    }
    return null;
}
