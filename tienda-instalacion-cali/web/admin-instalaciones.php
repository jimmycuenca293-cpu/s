<?php
declare(strict_types=1);
// Panel del técnico: reservas de instalación (confirmar el pago de la reserva, marcar completada, cancelar).
require __DIR__ . '/partes.php';
require_once __DIR__ . '/filtrosnevecones-api/instalacion-lib.php';
session_set_cookie_params(['httponly' => true, 'samesite' => 'Strict', 'secure' => str_starts_with(base_url(), 'https')]);
session_start();
header('X-Robots-Tag: noindex');
$clave = (string) (cfg()['admin_clave'] ?? '');
$msg = '';
if (isset($_POST['salir'])) { $_SESSION = []; session_destroy(); header('Location: /admin-instalaciones.php'); exit; }
if (isset($_POST['clave'])) {
    usleep(400000);
    if ($clave !== '' && hash_equals($clave, (string) $_POST['clave'])) { session_regenerate_id(true); $_SESSION['ok'] = true; $_SESSION['csrf'] = bin2hex(random_bytes(16)); header('Location: /admin-instalaciones.php'); exit; }
    $msg = 'Clave incorrecta.';
}
cabeza('Instalaciones | ' . cfg()['negocio']['nombre'], 'Panel de instalaciones', '/admin-instalaciones.php', '', false);
if ($clave === '') { echo '<div class="estado bad">Pon una clave en <b>admin_clave</b> dentro de filtrosnevecones-api/ajustes.php para usar este panel.</div>'; pie(); exit; }
if (empty($_SESSION['ok'])) {
    echo '<h1>Instalaciones</h1><form method="post" class="caja" style="max-width:360px"><label>Clave<br><input type="password" name="clave" autofocus style="width:100%"></label><button class="btn">Entrar</button>'
        . ($msg ? '<span class="m" style="color:var(--bad)">' . h($msg) . '</span>' : '') . '</form>';
    pie(); exit;
}
$ok_csrf = $_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? ''));
if ($ok_csrf && isset($_POST['accion'])) {
    $r = inst_buscar((string) ($_POST['ref'] ?? '')); $acc = (string) $_POST['accion'];
    if ($r) {
        $nuevo = ['confirmar' => 'reservada', 'completar' => 'completada', 'cancelar' => 'cancelada'][$acc] ?? '';
        if ($nuevo !== '') {
            $ocupado = false;
            if ($nuevo === 'reservada') {   // por si otro cliente tomó el horario mientras esta reserva esperaba el pago
                $st = inst_db()->prepare("SELECT COUNT(*) FROM instalaciones WHERE fecha = ? AND franja = ? AND estado = 'reservada' AND ref <> ?"); $st->execute([$r['fecha'], $r['franja'], $r['ref']]);
                $ocupado = (int) $st->fetchColumn() > 0;
            }
            if ($ocupado) $msg = 'Ese horario ya tiene otra reserva confirmada. Cancela una de las dos o llama al cliente para cambiar el día.';
            else {
                inst_db()->prepare('UPDATE instalaciones SET estado = ?, pagado_en = CASE WHEN ? = "reservada" THEN ? ELSE pagado_en END WHERE ref = ?')->execute([$nuevo, $nuevo, date('c'), $r['ref']]);
                $r = inst_buscar($r['ref']);
                if ($nuevo === 'reservada') enviar_correo($r['email'], 'Reserva confirmada ' . $r['ref'] . ': ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']),
                    '<h2 style="margin:0 0 8px">¡Tu reserva está confirmada!</h2><p>Recibimos el pago de tu reserva. El técnico llega en el horario que escogiste.</p>' . inst_tabla($r, false)
                    . '<p>El saldo de ' . h(cop((int) $r['saldo'])) . ' lo pagas al terminar. Tienes 1 año de garantía en la instalación.</p>');
                $msg = 'Reserva ' . $r['ref'] . ': ' . inst_estado_txt($nuevo) . '.' . ($nuevo === 'reservada' ? ' Le avisamos al cliente por correo.' : '');
            }
        }
    }
}
$filtro = (string) ($_GET['ver'] ?? 'proximas');
$donde = ['proximas' => "estado IN ('reservada','esperando_pago') AND fecha >= date('now','-1 day','localtime')", 'completadas' => "estado = 'completada'", 'canceladas' => "estado = 'cancelada'", 'todas' => '1=1'][$filtro] ?? '1=1';
$rows = inst_db()->query("SELECT * FROM instalaciones WHERE $donde ORDER BY fecha, franja LIMIT 300")->fetchAll();
$tot = inst_db()->query("SELECT COUNT(*) n, COALESCE(SUM(total),0) s FROM instalaciones WHERE estado IN ('reservada','completada')")->fetch();
?>
<h1>Instalaciones</h1>
<?php if ($msg): ?><div class="estado warn"><span><?= h($msg) ?></span></div><?php endif; ?>
<p class="m"><?= (int) $tot['n'] ?> reservas confirmadas o completadas · <?= h(cop((int) $tot['s'])) ?> en servicios. La reserva en línea la ves en tu panel de Wompi; el saldo lo cobras al terminar.</p>
<p style="display:flex;gap:8px;flex-wrap:wrap"><?php foreach (['proximas' => 'Próximas', 'completadas' => 'Completadas', 'canceladas' => 'Canceladas', 'todas' => 'Todas'] as $k => $n): ?><a class="btn <?= $filtro === $k ? '' : 'ghost' ?>" href="?ver=<?= $k ?>"><?= $n ?></a><?php endforeach; ?>
<form method="post" style="margin-left:auto"><button class="btn ghost" name="salir" value="1">Salir</button></form></p>
<?php if (!$rows): ?><div class="caja"><b>No hay reservas en esta lista.</b></div><?php endif; ?>
<?php foreach ($rows as $r): $est = $r['estado']; ?>
<section class="caja" style="margin-bottom:12px">
  <h2 style="font-size:18px"><?= h(inst_fecha_txt($r['fecha'])) ?> · <?= h(inst_franja_txt((int) $r['franja'])) ?> <span class="badge <?= $est === 'reservada' || $est === 'completada' ? 'pagado' : '' ?>"><?= h(inst_estado_txt($est)) ?></span></h2>
  <?= inst_tabla($r, true) ?>
  <p style="display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 0">
    <a class="btn ghost" href="https://wa.me/57<?= h($r['tel']) ?>?text=<?= rawurlencode('Hola ' . $r['nombre'] . ', soy el técnico de Filtros Nevecones. Sobre tu instalación del ' . inst_fecha_txt($r['fecha']) . ' a las ' . inst_franja_txt((int) $r['franja']) . '.') ?>" target="_blank" rel="noopener">WhatsApp al cliente</a>
    <a class="btn ghost" href="https://www.google.com/maps/search/?api=1&query=<?= rawurlencode($r['dir'] . ', ' . $r['barrio'] . ', ' . (inst_config()['zonas'][$r['zona']]['nombre'] ?? '') . ', Colombia') ?>" target="_blank" rel="noopener">Ver en el mapa</a>
    <?php foreach (['esperando_pago' => [['confirmar', 'Confirmar reserva pagada'], ['cancelar', 'Cancelar']], 'reservada' => [['completar', 'Instalación hecha y saldo cobrado'], ['cancelar', 'Cancelar']]][$est] ?? [] as [$ac, $tx]): ?>
      <form method="post"><input type="hidden" name="csrf" value="<?= h($_SESSION['csrf']) ?>"><input type="hidden" name="ref" value="<?= h($r['ref']) ?>"><button class="btn <?= $ac === 'cancelar' ? 'ghost' : '' ?>" name="accion" value="<?= $ac ?>"><?= $tx ?></button></form>
    <?php endforeach; ?>
  </p>
</section>
<?php endforeach; ?>
<?php pie(); ?>
