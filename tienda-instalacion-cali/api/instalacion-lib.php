<?php
declare(strict_types=1);
// Instalación a domicilio del kit de agua del nevecón (Cali, Jamundí, Yumbo y Palmira): precios, agenda y reservas.
require_once __DIR__ . '/lib.php';
date_default_timezone_set('America/Bogota');

const INST_RETENER_MIN = 60;   // una reserva sin pagar aparta el horario este tiempo; pagada, lo aparta hasta que se complete o se cancele

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
        'zonas' => ['cali' => ['nombre' => 'Cali', 'recargo' => 0], 'jamundi' => ['nombre' => 'Jamundí', 'recargo' => 15000],
                    'yumbo' => ['nombre' => 'Yumbo', 'recargo' => 20000], 'palmira' => ['nombre' => 'Palmira', 'recargo' => 20000]],
        'metro_extra' => 14000,   // cada 5 m de manguera adicionales a los 5 m incluidos
        'franjas' => [[8, 0, 9, 30], [9, 30, 11, 0], [11, 0, 12, 30], [13, 30, 15, 0], [15, 30, 17, 0]],
        'dias_adelante' => 21,
        'bloqueados' => [],        // fechas sin servicio: ['2026-12-08', ...]
        'links' => ['basica' => '', 'filtro-samsung' => '', 'filtro-lg' => '', 'filtro-whirlpool' => ''],
    ];
    // Ajustes propios de la instalación (links de pago de la reserva, clave del panel, fechas sin servicio): instalacion-ajustes.php
    $f = __DIR__ . '/instalacion-ajustes.php';
    $o = is_file($f) && is_array($a = require $f) ? $a : [];
    foreach (['servicios', 'zonas', 'links'] as $k) if (isset($o[$k]) && is_array($o[$k])) $base[$k] = array_replace_recursive($base[$k], $o[$k]);
    foreach (['metro_extra', 'dias_adelante'] as $k) if (isset($o[$k])) $base[$k] = (int) $o[$k];
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

// Fechas que se pueden reservar: desde mañana, de lunes a sábado, sin las fechas bloqueadas
function inst_fechas(): array
{
    $c = inst_config(); $r = [];
    $d = new DateTimeImmutable('tomorrow', new DateTimeZone('America/Bogota'));
    for ($i = 0; $i < $c['dias_adelante']; $i++, $d = $d->modify('+1 day')) {
        if ($d->format('w') === '0' || in_array($d->format('Y-m-d'), $c['bloqueados'], true)) continue;
        $r[] = $d->format('Y-m-d');
    }
    return $r;
}

// Horarios ocupados por reservas pagadas o recién creadas (aún dentro del tiempo para pagar)
function inst_ocupados(string $desde, string $hasta): array
{
    $st = inst_db()->prepare("SELECT fecha, franja FROM instalaciones WHERE fecha BETWEEN ? AND ? AND (estado = 'reservada' OR (estado = 'esperando_pago' AND creado > ?))");
    $st->execute([$desde, $hasta, date('c', time() - INST_RETENER_MIN * 60)]);
    $o = [];
    foreach ($st->fetchAll() as $r) $o[$r['fecha'] . '|' . $r['franja']] = true;
    return $o;
}

function inst_agenda(): array
{
    $f = inst_fechas();
    if (!$f) return [];
    $oc = inst_ocupados($f[0], end($f));
    $n = count(inst_config()['franjas']);
    $r = [];
    foreach ($f as $d) {
        $fr = [];
        for ($i = 0; $i < $n; $i++) $fr[] = ['i' => $i, 'txt' => inst_franja_txt($i), 'libre' => !isset($oc[$d . '|' . $i])];
        $r[] = ['fecha' => $d, 'txt' => inst_fecha_txt($d), 'corto' => inst_fecha_txt($d, false), 'franjas' => $fr];
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
    return ['esperando_pago' => 'Esperando el pago de la reserva', 'reservada' => 'Reserva confirmada', 'completada' => 'Instalación completada', 'cancelada' => 'Cancelada'][$e] ?? $e;
}

function inst_resumen_filas(array $r, bool $tecnico): array
{
    $c = inst_config(); $s = $c['servicios'][$r['servicio']] ?? ['nombre' => $r['servicio']]; $z = $c['zonas'][$r['zona']]['nombre'] ?? $r['zona'];
    $f = [
        'Reserva' => $r['ref'], 'Estado' => inst_estado_txt($r['estado']),
        'Servicio' => $s['nombre'], 'Día' => inst_fecha_txt($r['fecha']), 'Hora' => inst_franja_txt((int) $r['franja']),
        'Zona' => $z, 'Dirección' => $r['dir'] . ', ' . $r['barrio'], 'Manguera' => inst_metros_txt($r['metros']),
        'Total del servicio' => cop((int) $r['total']), 'Reserva en línea' => cop((int) $r['reserva']), 'Saldo al terminar' => cop((int) $r['saldo']),
    ];
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
        'Total' => cop((int) $r['total']) . ' (reserva ' . cop((int) $r['reserva']) . ' + saldo al terminar ' . cop((int) $r['saldo']) . ')',
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
    $pagar = $r['estado'] === 'esperando_pago'
        ? '<p><b>Falta un paso:</b> paga la reserva de ' . h(cop((int) $r['reserva'])) . ' para asegurar tu horario. <a href="' . h(inst_url_reserva($r['ref'])) . '">Pagar la reserva</a></p>'
        : '<p>Tu reserva está confirmada. El técnico llega en el horario que escogiste.</p>';
    $html = '<h2 style="margin:0 0 8px">Tu instalación quedó agendada</h2>' . $pagar . inst_tabla($r, false)
        . '<p>El saldo de ' . h(cop((int) $r['saldo'])) . ' lo pagas al terminar la instalación, cuando ya veas el agua funcionando. Tienes 1 año de garantía.</p>'
        . '<p>¿Necesitas cambiar el día o la hora? Avísanos con 24 horas y la reprogramamos sin costo: WhatsApp ' . h($tel) . '.</p>';
    enviar_correo($r['email'], 'Tu instalación ' . $r['ref'] . ': ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']), $html);
}
