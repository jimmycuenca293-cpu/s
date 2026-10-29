<?php
declare(strict_types=1);
require __DIR__ . '/../../partes.php';
require_once __DIR__ . '/../../filtrosnevecones-api/instalacion-lib.php';
header('X-Robots-Tag: noindex');
$r = inst_buscar((string) ($_GET['ref'] ?? ''));
$ok = $r && hash_equals(inst_token($r['ref']), (string) ($_GET['t'] ?? ''));
if ($ok && isset($_GET['ics'])) { header('Content-Type: text/calendar; charset=utf-8'); header('Content-Disposition: attachment; filename="instalacion-' . $r['ref'] . '.ics"'); echo inst_ics($r); exit; }
cabeza('Tu reserva de instalación | ' . cfg()['negocio']['nombre'], 'Tu reserva de instalación.', '/instalacion-nevecon-cali/reserva/', '<link rel="stylesheet" href="/instalacion-nevecon-cali/instalacion.css?v=20261029a">', false);
$wa = inst_tel_wa(); $tel = cfg()['negocio']['telefono'] ?? '301 381 0242';
if (!$ok) { echo '<div class="ic"><div class="ic-reserva"><h1>No encontramos esa reserva</h1><p class="m">Revisa el enlace que te llegó al correo o escríbenos por WhatsApp al ' . h($tel) . '.</p><a class="btn" href="/instalacion-nevecon-cali/">Hacer una reserva</a></div></div>'; pie(); exit; }
$total = ($r['forma_pago'] ?? 'reserva') === 'total';
$link = inst_link_pago($r);
$hasta = date('g:i a', strtotime($r['creado']) + INST_RETENER_MIN * 60);
$resta = max(0, strtotime($r['creado']) + INST_RETENER_MIN * 60 - time());
$msgwa = rawurlencode('Hola, soy ' . $r['nombre'] . '. Sobre mi reserva de instalación ' . $r['ref'] . ' del ' . inst_fecha_txt($r['fecha']) . ' a las ' . inst_franja_txt((int) $r['franja']) . '.');
?>
<div class="ic"><div class="ic-reserva">
<h1>Tu reserva de instalación</h1>
<?php if ($r['estado'] === 'esperando_pago'): ?>
  <div class="ic-estado warn"><b><?= $total ? 'Falta pagar para confirmar tu instalación' : 'Falta pagar la 1ª parte para asegurar tu horario' ?></b><span><?php if ($total): ?>Pagas <b><?= h(cop((int) $r['reserva'])) ?></b> en línea<?= (int) $r['saldo'] > 0 ? ' y ' . h(cop((int) $r['saldo'])) . ' en efectivo al terminar, por el recargo de zona o la manguera adicional' : ', y al terminar no pagas nada más' ?>.<?php else: ?>Hoy pagas <b><?= h(cop((int) $r['reserva'])) ?></b> en línea y al terminar le pagas <b><?= h(cop((int) $r['saldo'])) ?></b> en efectivo al técnico.<?php endif; ?> Tu horario queda apartado <b class="ic-cuenta" id="cuenta"><?= sprintf('%02d:%02d', intdiv($resta, 60), $resta % 60) ?></b> más (hasta las <?= h($hasta) ?>).</span></div>
  <?php if ($link !== ''): ?>
    <a class="btn" id="pagar" href="<?= h($link) ?>" target="_blank" rel="noopener" style="font-size:18px"><?= $total ? 'Pagar ' . h(cop((int) $r['reserva'])) . ' con Wompi' : 'Pagar ' . h(cop((int) $r['reserva'])) . ' hoy (1ª parte) con Wompi' ?></a>
    <p class="m" style="font-size:14px">Se abre la página segura de Wompi (tarjeta, PSE o Nequi). En «Nombre» y «Correo» usa los mismos datos de tu reserva para que podamos encontrar tu pago. Cuando termines, toca el botón de abajo.</p>
    <button class="btn ghost" id="ya" type="button">Ya pagué: avísenle al técnico</button><div id="ya-m" class="m" role="status"></div>
  <?php else: ?>
    <div class="ic-estado warn"><b>Paga por WhatsApp</b><span>Escríbenos y te enviamos el link de pago de <?= h(cop((int) $r['reserva'])) ?>.</span></div>
    <a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, soy ' . $r['nombre'] . '. Reservé la instalación ' . $r['ref'] . ' y quiero pagar ' . cop((int) $r['reserva']) . '. ¿Me envías el link de pago?') ?>" target="_blank" rel="noopener" style="font-size:18px">💬 Pedir el link de pago por WhatsApp</a>
  <?php endif; ?>
<?php elseif ($r['estado'] === 'reservada'): ?>
  <div class="ic-estado ok"><b>¡Reserva confirmada!</b><span>Un asesor te escribe por WhatsApp para darte el nombre del técnico. La instalación es el <?= h(inst_fecha_txt($r['fecha'])) ?>, <?= h(inst_franja_txt((int) $r['franja'])) ?>. <?= $total ? ((int) $r['saldo'] > 0 ? 'Pagaste el combo en línea. Al terminar pagas en efectivo ' . h(cop((int) $r['saldo'])) . ' por el recargo de zona o la manguera adicional.' : 'Ya pagaste todo: al terminar no pagas nada más.') : 'El saldo de ' . h(cop((int) $r['saldo'])) . ' lo pagas en efectivo al técnico al terminar.' ?></span></div>
<?php elseif ($r['estado'] === 'completada'): ?>
  <div class="ic-estado ok"><b>Instalación completada</b><span>Gracias por confiar en nosotros. Tienes 1 año de garantía en la instalación.</span></div>
<?php else: ?>
  <div class="ic-estado bad"><b>Esta reserva fue cancelada</b><span>Si quieres, haz una nueva reserva o escríbenos por WhatsApp.</span></div>
<?php endif; ?>
<section class="ic-card" style="padding:18px"><h3 style="margin-bottom:6px">Resumen</h3><?= inst_tabla($r, false) ?></section>
<section class="ic-card"><h3>Qué sigue</h3><ol class="ic-sigue">
  <?php if ($r['estado'] === 'esperando_pago'): ?><li><b>Pagas <?= $total ? 'el total' : 'la reserva' ?>.</b> Con eso queda confirmado tu horario.</li><?php else: ?><li><b>Tu horario está confirmado.</b></li><?php endif; ?>
  <li><b>Un asesor te escribe por WhatsApp</b> al <?= h($r['tel']) ?> para confirmar tu instalación y darte el <b>nombre del técnico</b>.</li>
  <li><b>El día de la instalación</b> el técnico llega en el horario escogido.</li>
  <li><b>Revisas el agua funcionando</b> y <?= $total ? ((int) $r['saldo'] > 0 ? 'pagas en efectivo ' . h(cop((int) $r['saldo'])) . ' (recargo de zona o manguera adicional).' : 'listo: ya pagaste todo.') : 'pagas el saldo en efectivo al técnico.' ?></li></ol>
  <p class="m" style="font-size:14px">Ten a mano: una persona adulta en casa, el nevecón con espacio para moverlo y a la vista el punto de agua.</p></section>
<section class="ic-card"><h3>Guarda tu reserva</h3><p class="m" style="font-size:14px">Tu reserva es este enlace. Guárdalo o mándatelo por WhatsApp para tenerlo a mano.</p>
  <a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, hice la reserva de instalación ' . $r['ref'] . ' para el ' . inst_fecha_txt($r['fecha']) . ', ' . inst_franja_txt((int) $r['franja']) . '. Mi enlace: ' . inst_url_reserva($r['ref'])) ?>" target="_blank" rel="noopener">💬 Enviarme mi reserva por WhatsApp</a>
  <button class="btn ghost" type="button" id="copiar">Copiar el enlace de mi reserva</button><span class="m" id="copiado" role="status"></span></section>
<a class="btn ghost" href="?ref=<?= h(rawurlencode($r['ref'])) ?>&amp;t=<?= h((string) $_GET['t']) ?>&amp;ics=1">📅 Guardar en mi calendario</a>
<p class="m">¿Necesitas cambiar el día o la hora, o cancelar? Avísanos con 24 horas por WhatsApp y lo reprogramamos sin costo.</p>
<a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= $msgwa ?>" target="_blank" rel="noopener">💬 WhatsApp <?= h($tel) ?></a>
<a class="btn ghost" href="/">Volver a la tienda</a>
</div></div>
<?php if ($r['estado'] === 'esperando_pago'): ?>
<script>
(function () { var el = document.getElementById("cuenta"); if (!el) return; var resta = <?= (int) $resta ?>, t0 = Date.now();
  function p() { var s = Math.max(0, resta - Math.floor((Date.now() - t0) / 1000)); el.textContent = ("0" + Math.floor(s / 60)).slice(-2) + ":" + ("0" + (s % 60)).slice(-2);
    if (!s) { el.parentNode.innerHTML = "<b>Tu horario ya no está apartado.</b> Si ya pagaste, escríbenos por WhatsApp con tu número de reserva. Si no, haz una nueva reserva."; clearInterval(iv); } }
  var iv = window._icIv = setInterval(p, 1000); p(); })();
</script>
<?php endif; ?>
<?php if ($r['estado'] === 'esperando_pago' && $link !== ''): ?>
<script>
document.getElementById("ya").addEventListener("click", async e => {
  const b = e.currentTarget, m = document.getElementById("ya-m"); b.disabled = true;
  try { const r = await fetch("/filtrosnevecones-api/instalacion.php?a=pagado", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ref: <?= json_encode($r['ref']) ?>, t: <?= json_encode((string) $_GET['t']) ?> }) });
    if (!r.ok) throw 0; m.textContent = "Listo. El técnico revisa tu pago y te confirma por correo y WhatsApp en poco tiempo."; var c = document.getElementById("cuenta"); if (c) { if (window._icIv) clearInterval(window._icIv); c.parentNode.innerHTML = "<b>Tu horario sigue apartado</b> mientras el técnico confirma tu pago."; } } catch { m.textContent = "No pudimos avisar. Escríbenos por WhatsApp con tu número de reserva."; b.disabled = false; }
});
</script>
<?php endif; ?>
<script>
document.getElementById("copiar").addEventListener("click", function () { var u = location.href.replace(/&ics=1/, ""), m = document.getElementById("copiado");
  function ok() { m.textContent = "Enlace copiado."; }
  try { navigator.clipboard.writeText(u).then(ok, function () { m.textContent = "Copia el enlace desde la barra de direcciones."; }); } catch (e) { m.textContent = "Copia el enlace desde la barra de direcciones."; } });
</script>
<?php pie(); ?>
