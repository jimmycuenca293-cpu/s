<?php
declare(strict_types=1);
require __DIR__ . '/../../partes.php';
require_once __DIR__ . '/../../filtrosnevecones-api/instalacion-lib.php';
header('X-Robots-Tag: noindex');
$r = inst_buscar((string) ($_GET['ref'] ?? ''));
$ok = $r && hash_equals(inst_token($r['ref']), (string) ($_GET['t'] ?? ''));
cabeza('Tu reserva de instalación | ' . cfg()['negocio']['nombre'], 'Tu reserva de instalación.', '/instalacion-nevecon-cali/reserva/', '<link rel="stylesheet" href="/instalacion-nevecon-cali/instalacion.css?v=20261029a">', false);
$wa = inst_tel_wa(); $tel = cfg()['negocio']['telefono'] ?? '301 381 0242';
if (!$ok) { echo '<div class="ic"><div class="ic-reserva"><h1>No encontramos esa reserva</h1><p class="m">Revisa el enlace que te llegó al correo o escríbenos por WhatsApp al ' . h($tel) . '.</p><a class="btn" href="/instalacion-nevecon-cali/">Hacer una reserva</a></div></div>'; pie(); exit; }
$total = ($r['forma_pago'] ?? 'reserva') === 'total';
$link = $total ? '' : (string) (inst_config()['links'][$r['servicio']] ?? '');
$hasta = date('g:i a', strtotime($r['creado']) + INST_RETENER_MIN * 60);
$msgwa = rawurlencode('Hola, soy ' . $r['nombre'] . '. Sobre mi reserva de instalación ' . $r['ref'] . ' del ' . inst_fecha_txt($r['fecha']) . ' a las ' . inst_franja_txt((int) $r['franja']) . '.');
?>
<div class="ic"><div class="ic-reserva">
<h1>Tu reserva de instalación</h1>
<?php if ($r['estado'] === 'esperando_pago' && $total): ?>
  <div class="ic-estado warn"><b>Falta pagar el total para confirmar tu instalación</b><span>Escogiste pagar todo en línea (<b><?= h(cop((int) $r['total'])) ?></b>). Escríbenos por WhatsApp y te enviamos el link de pago por ese valor. Tu horario queda apartado hasta las <?= h($hasta) ?>. Al terminar no pagas nada más.</span></div>
  <a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= rawurlencode('Hola, soy ' . $r['nombre'] . '. Reservé la instalación ' . $r['ref'] . ' y quiero pagar el total (' . cop((int) $r['total']) . '). ¿Me envías el link de pago?') ?>" target="_blank" rel="noopener" style="font-size:18px">💬 Pedir el link de pago por WhatsApp</a>
<?php elseif ($r['estado'] === 'esperando_pago'): ?>
  <div class="ic-estado warn"><b>Falta pagar la reserva para asegurar tu horario</b><span>Pagas <b><?= h(cop((int) $r['reserva'])) ?></b> ahora y el saldo de <?= h(cop((int) $r['saldo'])) ?> en efectivo al técnico, al terminar la instalación. Tu horario queda apartado hasta las <?= h($hasta) ?>.</span></div>
  <?php if ($link !== ''): ?>
    <a class="btn" id="pagar" href="<?= h($link) ?>" target="_blank" rel="noopener" style="font-size:18px">Pagar la reserva <?= h(cop((int) $r['reserva'])) ?> con Wompi</a>
    <p class="m" style="font-size:14px">Se abre la página segura de Wompi. En «Nombre» y «Correo» usa los mismos datos de tu reserva para que podamos encontrar tu pago. Cuando termines, toca el botón de abajo.</p>
    <button class="btn ghost" id="ya" type="button">Ya pagué: avísenle al técnico</button><div id="ya-m" class="m" role="status"></div>
  <?php else: ?>
    <div class="ic-estado warn"><b>Paga tu reserva por WhatsApp</b><span>Escríbenos y te enviamos el link de pago de <?= h(cop((int) $r['reserva'])) ?>.</span></div>
  <?php endif; ?>
<?php elseif ($r['estado'] === 'reservada'): ?>
  <div class="ic-estado ok"><b>¡Reserva confirmada!</b><span>El técnico llega el <?= h(inst_fecha_txt($r['fecha'])) ?>, <?= h(inst_franja_txt((int) $r['franja'])) ?>. <?= $total ? 'Ya pagaste todo: al terminar no pagas nada más.' : 'El saldo de ' . h(cop((int) $r['saldo'])) . ' lo pagas en efectivo al técnico al terminar.' ?></span></div>
<?php elseif ($r['estado'] === 'completada'): ?>
  <div class="ic-estado ok"><b>Instalación completada</b><span>Gracias por confiar en nosotros. Tienes 1 año de garantía en la instalación.</span></div>
<?php else: ?>
  <div class="ic-estado bad"><b>Esta reserva fue cancelada</b><span>Si quieres, haz una nueva reserva o escríbenos por WhatsApp.</span></div>
<?php endif; ?>
<section class="ic-card" style="padding:18px"><h3 style="margin-bottom:6px">Resumen</h3><?= inst_tabla($r, false) ?></section>
<p class="m">¿Necesitas cambiar el día o la hora? Avísanos con 24 horas y lo reprogramamos sin costo.</p>
<a class="btn wa" href="https://wa.me/57<?= h($wa) ?>?text=<?= $msgwa ?>" target="_blank" rel="noopener">💬 WhatsApp <?= h($tel) ?></a>
<a class="btn ghost" href="/">Volver a la tienda</a>
</div></div>
<?php if ($r['estado'] === 'esperando_pago' && $link !== ''): ?>
<script>
document.getElementById("ya").addEventListener("click", async e => {
  const b = e.currentTarget, m = document.getElementById("ya-m"); b.disabled = true;
  try { const r = await fetch("/filtrosnevecones-api/instalacion.php?a=pagado", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ref: <?= json_encode($r['ref']) ?>, t: <?= json_encode((string) $_GET['t']) ?> }) });
    if (!r.ok) throw 0; m.textContent = "Listo. El técnico revisa tu pago y te confirma por correo y WhatsApp en poco tiempo."; } catch { m.textContent = "No pudimos avisar. Escríbenos por WhatsApp con tu número de reserva."; b.disabled = false; }
});
</script>
<?php endif; ?>
<?php pie(); ?>
