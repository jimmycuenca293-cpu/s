<?php
require __DIR__ . '/partes.php';
$cat = catalogo();
$pub = ['ciudades' => $cat['ciudades'], 'productos' => array_map(fn($p) => ['nombre' => $p['nombre'], 'ref' => $p['ref'], 'marca' => $p['marca'], 'precio' => $p['precio'], 'pack' => $p['pack'], 'slug' => $p['slug']], $cat['productos'])];
cabeza('Tu carrito | ' . cfg()['negocio']['nombre'], 'Carrito de compras.', '/carrito.php', '', false);
?>
<h1>Tu carrito</h1>
<div id="vacio" class="caja" hidden><b>Tu carrito está vacío.</b><span class="m">Busca el filtro de tu nevecón por la referencia o por el modelo.</span><a class="btn" href="/tienda/">Ver todos los filtros</a></div>
<div class="checkout" id="checkout" hidden>
  <div class="col">
    <section class="caja"><h2>Productos</h2><div id="lineas"></div></section>
    <section class="caja">
      <h2>¿A dónde lo enviamos?</h2>
      <div class="campos">
        <label class="f2"><span>Nombre completo</span><input id="c-nombre" autocomplete="name" maxlength="80"></label>
        <label class="f2"><span>Celular</span><input id="c-tel" type="tel" inputmode="numeric" autocomplete="tel" placeholder="300 123 4567" maxlength="16"></label>
        <label class="f2"><span>Correo (te llega el recibo)</span><input id="c-email" type="email" inputmode="email" autocomplete="email" placeholder="tucorreo@gmail.com" maxlength="120"></label>
        <label class="f2"><span>Ciudad</span><select id="c-ciudad"></select></label>
        <label class="f2"><span>Barrio</span><input id="c-barrio" maxlength="80"></label>
        <label class="f2 ancho"><span>Dirección</span><input id="c-dir" autocomplete="street-address" placeholder="Calle 5 # 66-20, apto 301" maxlength="160"></label>
        <label class="f2 ancho"><span>Indicaciones para la entrega (opcional)</span><input id="c-ind" maxlength="200" placeholder="Torre 2, portería; llamar antes"></label>
        <label class="f2 ancho"><span>Modelo del nevecón (opcional)</span><input id="c-modelo" maxlength="40" placeholder="Nos ayuda a confirmar que le sirve"></label>
      </div>
      <div id="entrega" class="entrega"></div>
      <label class="check2"><input type="checkbox" id="c-rec"><span><b>Recuérdame por correo cuando toque cambiar el filtro</b> (cada 6 meses). Opcional.</span></label>
    </section>
  </div>
  <aside class="col resumen">
    <section class="caja">
      <h2>Resumen</h2>
      <div id="totales"></div>
      <button class="btn block" type="button" id="pagar">Pagar</button>
      <p class="err" id="err" aria-live="polite"></p>
      <div class="sellos"><span>🔒 Pago 100 % seguro</span><span>🚚 Envío gratis a toda Colombia</span><span>↩︎ 30 días de garantía</span></div>
      <p class="m" style="font-size:12.5px;margin:0">Pagas con tarjeta, PSE, Nequi o botón Bancolombia. Al pagar aceptas los <a href="/terminos.php" target="_blank">Términos</a> y autorizas el tratamiento de tus datos según la <a href="/privacidad.php" target="_blank">Política de datos</a>.</p>
    </section>
  </aside>
</div>
<script>
window.FY_CAT = <?= json_encode($pub, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?>;
// carrito.js carga con defer: se arranca cuando la página termina de cargar
document.addEventListener("DOMContentLoaded", () => {
  "use strict";
  const $ = s => document.querySelector(s), C = window.FY_CAT, P = C.productos;
  const cop = n => "$ " + Math.round(n).toLocaleString("es-CO");
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const ls = { get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } }, set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} } };
  let entrega = null;
  function lineas() { return FYCart.leer().filter(l => P[l.pid]); }
  function total() { return lineas().reduce((a, l) => a + (l.pack ? P[l.pid].pack : P[l.pid].precio) * l.cant, 0); }
  function habiles(n) { const d = new Date(); let k = 0; while (k < n) { d.setDate(d.getDate() + 1); const w = d.getDay(); if (w && w < 6) k++; } return d.toLocaleDateString("es-CO", { weekday: "long", day: "numeric", month: "long" }); }
  function pintar() {
    const L = lineas();
    $("#vacio").hidden = !!L.length; $("#checkout").hidden = !L.length;
    if (!L.length) return;
    $("#lineas").innerHTML = L.map((l, i) => {
      const p = P[l.pid], unit = l.pack ? p.pack : p.precio, ahorro = p.precio * 2 - p.pack;
      return `<div class="linea">
        <a class="lim" href="/filtro/${p.slug}/"><picture><source srcset="/img/${l.pid}-400.webp" type="image/webp"><img src="/img/${l.pid}.jpg" alt="${esc(p.nombre)}"></picture></a>
        <div class="ltx"><a href="/filtro/${p.slug}/"><b>${esc(p.nombre)}</b></a><span class="ref">${esc(p.ref)}</span>${l.pack ? `<span class="badge pagado">Pack anual de 2 · ahorras ${cop(ahorro)}</span>` : ""}
          <div class="lact"><span class="qty"><button type="button" data-q="-1" data-i="${i}" aria-label="Menos">−</button><b>${l.cant}</b><button type="button" data-q="1" data-i="${i}" aria-label="Más">+</button></span>
          <button type="button" class="link" data-del="${i}">Quitar</button>${!l.pack ? `<button type="button" class="link" data-topack="${i}">Cambiar a pack de 2 y ahorrar ${cop(ahorro)}</button>` : ""}</div></div>
        <b class="lprecio">${cop(unit * l.cant)}</b></div>`;
    }).join("");
    const ciudad = $("#c-ciudad").value, cali = ciudad === "Cali";
    const ops = cali ? [["instalacion", "Te lo llevamos e instalamos", "Te llamamos para acordar el día y la hora."], ["domicilio", "Solo entrega, sin instalación", "Te llamamos para acordar el día y la hora."]]
      : ciudad ? [["transportadora", "Envío por transportadora", `Llega en unos 2 días hábiles, hacia el ${habiles(2)}. Te enviamos la guía al correo.`]] : [];
    if (!ops.some(o => o[0] === entrega)) entrega = ops[0]?.[0] || null;
    $("#entrega").innerHTML = ciudad ? `<b>Entrega en ${esc(ciudad)}</b>` + ops.map(([k, t, s]) => `<label class="opc"><input type="radio" name="ent" value="${k}" ${k === entrega ? "checked" : ""}><span><b>${t}</b><small>${s}</small></span><span class="gratis">Gratis</span></label>`).join("") : `<span class="m">Escoge tu ciudad para ver la entrega.</span>`;
    const t = total(), n = L.reduce((a, l) => a + l.cant * (l.pack ? 2 : 1), 0);
    $("#totales").innerHTML = `<div class="tl"><span>${n} ${n === 1 ? "filtro" : "filtros"}</span><span>${cop(t)}</span></div><div class="tl"><span>Envío${cali ? " e instalación" : ""}</span><span class="gratis">Gratis</span></div><div class="tl total"><span>Total</span><span>${cop(t)}</span></div>`;
    $("#pagar").textContent = `Pagar ${cop(t)}`;
  }
  $("#c-ciudad").innerHTML = `<option value="">Escoge tu ciudad</option>` + C.ciudades.map(c => `<option>${esc(c)}</option>`).join("");
  const prev = ls.get("fy_cliente", {}), cityPrev = ls.get("fy_city", "");
  [["c-nombre", "nombre"], ["c-tel", "tel"], ["c-email", "email"], ["c-barrio", "barrio"], ["c-dir", "dir"]].forEach(([id, k]) => { if (prev[k]) $("#" + id).value = prev[k]; });
  if (C.ciudades.includes(cityPrev)) $("#c-ciudad").value = cityPrev;
  $("#c-rec").checked = !!prev.recordar;
  $("#c-ciudad").addEventListener("change", e => { ls.set("fy_city", e.target.value); pintar(); });
  document.addEventListener("change", e => { if (e.target.name === "ent") entrega = e.target.value; });
  document.addEventListener("click", e => {
    const q = e.target.closest("[data-q]"), d = e.target.closest("[data-del]"), tp = e.target.closest("[data-topack]");
    if (!q && !d && !tp) return;
    const c = lineas();
    if (q) { c[+q.dataset.i].cant = Math.max(1, Math.min(10, c[+q.dataset.i].cant + +q.dataset.q)); }
    if (d) c.splice(+d.dataset.del, 1);
    if (tp) { const l = c[+tp.dataset.topack]; const ya = c.find(x => x.pid === l.pid && x.pack); if (ya) ya.cant = Math.min(10, ya.cant + 1); else c.push({ pid: l.pid, pack: true, cant: 1 }); if (l.cant > 1) l.cant--; else c.splice(c.indexOf(l), 1); }
    FYCart.guardar(c); pintar();
  });
  window.addEventListener("storage", pintar);
  $("#pagar").addEventListener("click", async () => {
    const v = id => $("#" + id).value.trim(), err = $("#err");
    const cli = { nombre: v("c-nombre"), tel: v("c-tel").replace(/\D/g, "").replace(/^57(?=3\d{9}$)/, ""), email: v("c-email"), ciudad: $("#c-ciudad").value, barrio: v("c-barrio"), dir: v("c-dir"), indicaciones: v("c-ind"), modelo: v("c-modelo"), recordar: $("#c-rec").checked };
    const falta = [cli.nombre.length < 3 && "tu nombre", !/^3\d{9}$/.test(cli.tel) && "un celular válido (10 dígitos que empiezan por 3)", !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(cli.email) && "un correo válido", !cli.ciudad && "la ciudad", !cli.barrio && "el barrio", cli.dir.length < 5 && "la dirección"].filter(Boolean);
    if (falta.length) { err.textContent = "Falta " + falta.join(", ") + "."; return; }
    const b = $("#pagar"), old = b.textContent; b.disabled = true; b.textContent = "Abriendo el pago seguro…"; err.textContent = "";
    ls.set("fy_cliente", { nombre: cli.nombre, tel: cli.tel, email: cli.email, barrio: cli.barrio, dir: cli.dir, recordar: cli.recordar });
    try {
      const L = lineas(), t = total();
      const r = await fetch("/api/pedido.php", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ items: L.map(l => ({ pid: l.pid, pack: !!l.pack, cant: l.cant })), total: t, entrega, cliente: cli }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.url) throw new Error(j.mensaje || "No se pudo crear el pedido. Intenta de nuevo.");
      const cambio = new Date(); cambio.setMonth(cambio.getMonth() + 6);
      const o = ls.get("fy_orders", []).filter(x => x.id !== j.ref);
      o.unshift({ id: j.ref, fecha: new Date().toISOString(), cambio: cambio.toISOString(), producto: P[L[0].pid].nombre + (L.length > 1 ? ` y ${L.length - 1} más` : ""), ref: P[L[0].pid].ref, pid: L[0].pid, total: j.total, ciudad: cli.ciudad, entrega, pago: "wompi", estado: "Pago pendiente", cliente: { recordar: cli.recordar } });
      ls.set("fy_orders", o.slice(0, 50));
      location.href = j.url;
    } catch (x) { err.textContent = x.message; b.disabled = false; b.textContent = old; }
  });
  pintar();
});
</script>
<?php pie(); ?>
