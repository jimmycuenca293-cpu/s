<?php
declare(strict_types=1);
// Panel de pedidos: solo con la clave de config.php.
require __DIR__ . '/partes.php';
session_set_cookie_params(['httponly' => true, 'samesite' => 'Strict', 'secure' => str_starts_with(base_url(), 'https')]);
session_start();
header('X-Robots-Tag: noindex');
$clave = (string) cfg()['admin_clave'];
$msg = '';

if (isset($_POST['salir'])) { $_SESSION = []; session_destroy(); header('Location: /admin.php'); exit; }
if (isset($_POST['clave'])) {
    usleep(400000); // frena intentos repetidos
    if ($clave !== '' && hash_equals($clave, (string) $_POST['clave'])) { session_regenerate_id(true); $_SESSION['ok'] = true; $_SESSION['csrf'] = bin2hex(random_bytes(16)); header('Location: /admin.php'); exit; }
    $msg = 'Clave incorrecta.';
}
cabeza('Pedidos | ' . cfg()['negocio']['nombre'], 'Panel de pedidos', '/admin.php', '', false);
if ($clave === '') { echo '<div class="estado bad">Pon una clave en <b>admin_clave</b> dentro de api/config.php para usar este panel.</div>'; pie(); exit; }
if (empty($_SESSION['ok'])) {
    echo '<h1>Pedidos</h1><form method="post" class="caja" style="max-width:360px"><label>Clave<br><input type="password" name="clave" autofocus style="width:100%"></label><button class="btn">Entrar</button>'
        . ($msg ? '<span class="m" style="color:var(--bad)">' . h($msg) . '</span>' : '') . '</form>';
    pie(); exit;
}

// Acciones: marcar enviado (con guía), entregado o anulado
if ($_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? ''))) {
    $ref = (string) ($_POST['ref'] ?? '');
    $acc = (string) ($_POST['accion'] ?? '');
    $st = db()->prepare('SELECT * FROM pedidos WHERE ref = ?'); $st->execute([$ref]); $p = $st->fetch();
    if ($p && in_array($acc, ['enviado', 'entregado', 'anulado'], true) && $p['estado'] !== 'pendiente') {
        $guia = mb_substr(trim((string) ($_POST['guia'] ?? '')), 0, 80);
        db()->prepare('UPDATE pedidos SET estado = ?, guia = COALESCE(NULLIF(?, ""), guia) WHERE ref = ?')->execute([$acc, $guia, $ref]);
        if ($acc === 'enviado') {
            enviar_correo($p['email'], "Tu pedido {$p['ref']} va en camino", '<h2 style="margin:0 0 8px">Tu filtro va en camino</h2><p>Despachamos tu pedido <b>' . h($p['ref']) . '</b> (' . h($p['producto']) . ').'
                . ($guia ? ' Número de guía: <b>' . h($guia) . '</b>.' : '') . '</p><p style="color:#5a6873;font-size:13px">' . h(cfg()['negocio']['nombre']) . ' · ' . h(cfg()['negocio']['correo']) . '</p>');
        }
        $msg = "Pedido $ref marcado como $acc." . ($acc === 'enviado' ? ' Le avisamos al cliente por correo.' : '');
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && hash_equals($_SESSION['csrf'] ?? '', (string) ($_POST['csrf'] ?? '')) && isset($_POST['resena'])) {
    db()->prepare('UPDATE resenas SET visible = 1 - visible WHERE id = ?')->execute([(int) $_POST['resena']]);
    $msg = 'Opinión actualizada.';
}
$filtro = (string) ($_GET['ver'] ?? 'activos');
$where = ['activos' => "estado IN ('pagado','enviado')", 'pendientes' => "estado = 'pendiente'", 'todos' => '1=1'][$filtro] ?? "estado IN ('pagado','enviado')";
$rows = db()->query("SELECT * FROM pedidos WHERE $where ORDER BY creado DESC LIMIT 300")->fetchAll();
$tot = db()->query("SELECT COUNT(*) n, COALESCE(SUM(total),0) s FROM pedidos WHERE estado IN ('pagado','enviado','entregado')")->fetch();
$csrf = h($_SESSION['csrf']);
?>
<?php if ($f = datos_sin_llenar()): ?><div class="estado bad"><b>Tu tienda todavía muestra datos de ejemplo.</b> Cámbialos en api/config.php antes de anunciar en Google Ads: <?= h(implode(', ', $f)) ?>.</div><?php endif; ?>
<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap"><h1>Pedidos</h1><form method="post"><button class="btn ghost sm" name="salir" value="1">Salir</button></form></div>
<div class="caja"><b><?= (int) $tot['n'] ?> pedidos pagados · <?= cop((int) $tot['s']) ?> vendidos</b>
<span class="m">Cada pedido pagado también te llega al correo <?= h(cfg()['correo_avisos']) ?>.</span></div>
<?= $msg ? '<div class="estado ok">' . h($msg) . '</div>' : '' ?>
<nav class="chips"><?php foreach (['activos' => 'Por despachar', 'pendientes' => 'Sin pagar', 'todos' => 'Todos', 'opiniones' => 'Opiniones'] as $k => $v) echo '<a class="badge" href="?ver=' . $k . '"' . ($k === $filtro ? ' style="outline:2px solid var(--accent)"' : '') . '>' . $v . '</a>'; ?></nav>
<?php if ($filtro === 'opiniones') {
    $rs = db()->query('SELECT * FROM resenas ORDER BY creado DESC LIMIT 300')->fetchAll();
    if (!$rs) echo '<p class="m">Todavía no hay opiniones. Se piden solas por correo 7 días después de cada pago.</p>';
    foreach ($rs as $r) {
        echo '<div class="caja"><span>' . estrellas_html((float) $r['estrellas']) . ' <b>' . h($r['nombre']) . '</b> · ' . h($r['ciudad']) . ' · ' . h(catalogo()['productos'][$r['pid']]['nombre'] ?? $r['pid']) . '</span>'
            . '<span>' . h($r['texto']) . '</span><form method="post"><input type="hidden" name="csrf" value="' . $csrf . '"><input type="hidden" name="resena" value="' . (int) $r['id'] . '">'
            . '<button class="btn ghost sm">' . ($r['visible'] ? 'Ocultar (solo si es ofensiva o falsa)' : 'Mostrar') . '</button></form></div>';
    }
    $rows = [];
} elseif (!$rows) echo '<p class="m">No hay pedidos aquí.</p>'; ?>
<?php foreach ($rows as $p): ?>
<div class="caja">
  <div style="display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap"><b><?= h($p['ref']) ?></b><span class="badge <?= h($p['estado']) ?>"><?= h($p['estado']) ?></span></div>
  <?php foreach (lineas_pedido($p) as $l) echo '<span>' . h(linea_txt($l)) . '</span>'; ?><b><?= cop((int) $p['total']) ?></b>
  <span class="m"><?= h(entrega_txt($p['entrega'])) ?> · <?= h(date('d/m/Y H:i', strtotime($p['creado']))) ?><?= $p['guia'] ? ' · Guía ' . h($p['guia']) : '' ?></span>
  <span><?= h($p['nombre']) ?> · <a href="tel:+57<?= h($p['tel']) ?>"><?= h($p['tel']) ?></a> · <a href="mailto:<?= h($p['email']) ?>"><?= h($p['email']) ?></a></span>
  <span><?= h($p['dir']) ?>, <?= h($p['barrio']) ?>, <?= h($p['ciudad']) ?><?= $p['indicaciones'] ? ' · ' . h($p['indicaciones']) : '' ?><?= $p['modelo'] ? ' · Nevecón ' . h($p['modelo']) : '' ?></span>
  <?php if (in_array($p['estado'], ['pagado', 'enviado'], true)): ?>
  <form method="post" style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
    <input type="hidden" name="csrf" value="<?= $csrf ?>"><input type="hidden" name="ref" value="<?= h($p['ref']) ?>">
    <?php if ($p['estado'] === 'pagado'): ?><input name="guia" placeholder="Número de guía (opcional)" style="flex:1;min-width:160px"><button class="btn sm" name="accion" value="enviado">Marcar enviado</button><?php endif; ?>
    <button class="btn ghost sm" name="accion" value="entregado">Entregado</button>
  </form>
  <?php endif; ?>
</div>
<?php endforeach; ?>
<?php pie(); ?>
