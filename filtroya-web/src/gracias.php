<?php require __DIR__ . '/partes.php'; cabeza('Estado de tu pago | ' . cfg()['negocio']['nombre'], 'Estado de tu pago.', '/gracias.php', '', false); ?>
<h1 id="t">Revisando tu pago…</h1>
<div id="out" class="estado warn"><span class="m">Un momento, estamos confirmando tu pago.</span></div>
<a class="btn ghost" href="/">Volver a la tienda</a>
<script>
(async () => {
  const id = new URLSearchParams(location.search).get("id"), out = document.getElementById("out"), t = document.getElementById("t");
  const cop = n => "$ " + Math.round(n).toLocaleString("es-CO");
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  if (!id) { t.textContent = "No encontramos el pago"; out.className = "estado bad"; out.textContent = "Si pagaste, te llega la confirmación a tu correo."; return; }
  for (let i = 0; i < 8; i++) {
    let j = null;
    try { const r = await fetch("/api/estado.php?id=" + encodeURIComponent(id), { cache: "no-store" }); j = await r.json(); } catch {}
    if (j && !j.error) {
      try { const o = JSON.parse(localStorage.getItem("fy_orders") || "[]"); const x = o.find(z => z.id === j.ref); if (x) { x.estado = j.estado === "pagado" ? "Pagado" : j.estado === "rechazado" ? "Pago rechazado" : "Pago pendiente"; localStorage.setItem("fy_orders", JSON.stringify(o)); } } catch {}
      if (j.estado === "pagado" || j.estado === "enviado" || j.estado === "entregado") {
        t.textContent = "¡Pago aprobado! Gracias por tu compra";
        try { if (window.gtag && !sessionStorage.getItem("ga-" + j.ref)) { gtag("event", "purchase", { transaction_id: j.ref, value: j.total, currency: "COP", items: [{ item_id: j.pid, item_name: j.producto, quantity: j.unidades }] }); sessionStorage.setItem("ga-" + j.ref, "1"); } } catch {}
        out.className = "estado ok";
        try { localStorage.removeItem("fy_carrito"); } catch {}
        out.innerHTML = `<b>Pedido ${esc(j.ref)} · ${cop(j.total)}</b>${(j.items || []).map(i => `<span>${esc(i.texto)}</span>`).join("")}<span>${j.entrega === "transportadora" ? "Lo despachamos por transportadora a " + esc(j.ciudad) + " y te llega en unos 2 días hábiles. Te enviamos la guía a tu correo." : "Te llamamos para acordar el día y la hora de la entrega en Cali."}</span><span class="m">Te enviamos el recibo a ${esc(j.email)}.</span>`;
        return;
      }
      if (j.estado === "rechazado") {
        t.textContent = "El pago no se aprobó";
        out.className = "estado bad";
        out.innerHTML = `<span>El banco no aprobó el pago del pedido ${esc(j.ref)}. No se te cobró nada.</span><a class="btn" href="/carrito.php">Volver al carrito e intentar de nuevo</a>`;
        return;
      }
      out.innerHTML = `<span>Tu pago del pedido ${esc(j.ref)} está en proceso (puede pasar con PSE o Nequi). Te avisamos a tu correo apenas se apruebe.</span>`;
    }
    await new Promise(r => setTimeout(r, 4000));
  }
  t.textContent = "Tu pago está en proceso";
})();
</script>
<?php pie(); ?>
