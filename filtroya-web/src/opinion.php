<?php
declare(strict_types=1);
// Opinión de un comprador real: el enlace llega por correo, firmado para su pedido.
require __DIR__ . '/partes.php';
$ref = (string) ($_GET['r'] ?? $_POST['r'] ?? '');
$tok = (string) ($_GET['t'] ?? $_POST['t'] ?? '');
$st = db()->prepare("SELECT * FROM pedidos WHERE ref = ? AND estado IN ('pagado','enviado','entregado')");
$st->execute([$ref]);
$p = $st->fetch();
$ok = $p && hash_equals(token_resena($ref), $tok);
$hecha = false;
$err = '';
if ($ok && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $est = (int) ($_POST['estrellas'] ?? 0);
    $txt = mb_substr(trim((string) ($_POST['texto'] ?? '')), 0, 800);
    if ($est < 1 || $est > 5) $err = 'Escoge de 1 a 5 estrellas.';
    else {
        $partes = preg_split('/\s+/', trim($p['nombre']));
        $nombre = $partes[0] . (isset($partes[1]) ? ' ' . mb_substr($partes[1], 0, 1) . '.' : '');
        $pids = array_column(lineas_pedido($p), 'pid');
        $pid = in_array((string) ($_POST['pid'] ?? ''), $pids, true) ? (string) $_POST['pid'] : $pids[0];
        db()->prepare('INSERT INTO resenas (ref, pid, nombre, ciudad, estrellas, texto, creado) VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(ref) DO UPDATE SET pid = excluded.pid, estrellas = excluded.estrellas, texto = excluded.texto, creado = excluded.creado')
            ->execute([$ref, $pid, $nombre, $p['ciudad'], $est, $txt, date('c')]);
        $hecha = true;
    }
}
cabeza('Tu opinión | ' . cfg()['negocio']['nombre'], 'Cuéntanos cómo te fue con tu filtro.', '/opinion.php', '', false);
if (!$ok) { echo '<h1>Enlace no válido</h1><p>Este enlace no corresponde a un pedido. Revisa el correo que te enviamos.</p>'; pie(); exit; }
if ($hecha) { echo '<h1>¡Gracias por tu opinión!</h1><div class="estado ok">Ya quedó publicada en la página del filtro. Nos ayuda mucho a que otras personas encuentren el filtro correcto.</div><a class="btn ghost" href="/">Volver a la tienda</a>'; pie(); exit; }
?>
<h1>¿Cómo te fue con tu filtro?</h1>
<p><?= h($p['producto']) ?> · pedido <?= h($p['ref']) ?></p>
<form method="post" class="caja">
  <input type="hidden" name="r" value="<?= h($ref) ?>"><input type="hidden" name="t" value="<?= h($tok) ?>">
  <?php $ls = lineas_pedido($p); if (count($ls) > 1): ?><label>¿Qué filtro quieres calificar?<br><select name="pid" style="width:100%"><?php foreach ($ls as $l) echo '<option value="' . h($l['pid']) . '">' . h($l['nombre']) . '</option>'; ?></select></label><?php endif; ?>
  <b>Califícalo</b>
  <div class="rate"><?php for ($i = 5; $i >= 1; $i--) echo '<input type="radio" name="estrellas" value="' . $i . '" id="e' . $i . '"><label for="e' . $i . '" title="' . $i . ' estrellas">★</label>'; ?></div>
  <label>Cuéntanos (opcional)<br><textarea name="texto" rows="4" maxlength="800" style="width:100%" placeholder="¿Le sirvió a tu nevecón? ¿Cómo fue la entrega?"></textarea></label>
  <?= $err ? '<span style="color:var(--bad)">' . h($err) . '</span>' : '' ?>
  <button class="btn">Publicar mi opinión</button>
  <span class="m">Se publica con tu primer nombre y la inicial del apellido.</span>
</form>
<?php pie(); ?>
