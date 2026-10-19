<?php
require __DIR__ . '/partes.php';
$cat = catalogo();
$pub = ['ciudades' => $cat['ciudades'], 'dias' => (object) ($cat['dias'] ?? []), 'productos' => array_map(fn($p) => ['nombre' => $p['nombre'], 'ref' => $p['ref'], 'marca' => $p['marca'], 'precio' => $p['precio'], 'pack' => $p['pack'], 'slug' => $p['slug'], 'ubic' => $p['ubic']], $cat['productos']), 'inst_ext' => 0, 'pago_link' => !con_llaves()];
cabeza('Tu carrito | ' . cfg()['negocio']['nombre'], 'Carrito de compras.', '/carrito.php', '', false);
?>
<link rel="preconnect" href="https://checkout.wompi.co"><link rel="dns-prefetch" href="https://checkout.wompi.co">
<h1>Tu carrito</h1>
<div id="vacio" class="caja" hidden><b>Tu carrito está vacío.</b><span class="m">Busca el filtro de tu nevecón por la referencia o por el modelo.</span><a class="btn" href="/tienda/">Ver todos los filtros</a></div>
<div class="checkout" id="checkout" hidden>
  <div class="col">
    <section class="caja paso">
      <h2><span class="np">1</span>Tus productos</h2>
      <div id="lineas"></div>
      <button type="button" class="link vaciar" id="vaciar">Vaciar carrito</button>
    </section>
    <section class="caja paso">
      <h2><span class="np">2</span>Tus datos</h2>
      <p class="m nota-req">Los campos con <b class="req">*</b> son obligatorios para hacer el pedido.</p>
      <div class="campos">
        <label class="f2" data-f="nombre"><span>Nombre completo <b class="req">*</b></span><input id="c-nombre" autocomplete="name" maxlength="80" aria-required="true"><small class="msg" hidden></small></label>
        <label class="f2" data-f="tel"><span>Celular <b class="req">*</b></span><input id="c-tel" type="tel" inputmode="numeric" autocomplete="tel" placeholder="300 123 4567" maxlength="16" aria-required="true"><small class="msg" hidden></small></label>
        <label class="f2 ancho" data-f="email"><span>Correo (te llega el recibo) <b class="req">*</b></span><input id="c-email" type="email" inputmode="email" autocomplete="email" placeholder="tucorreo@gmail.com" maxlength="120" aria-required="true"><small class="msg" hidden></small></label>
      </div>
    </section>
    <section class="caja paso">
      <h2><span class="np">3</span>¿A dónde lo enviamos?</h2>
      <div class="campos">
        <label class="f2" data-f="ciudad"><span>Ciudad <b class="req">*</b></span><select id="c-ciudad" aria-required="true"></select><small class="msg" hidden></small></label>
        <label class="f2" data-f="barrio"><span>Barrio <b class="req">*</b></span><input id="c-barrio" maxlength="80" aria-required="true"><small class="msg" hidden></small></label>
        <label class="f2 ancho" data-f="dir"><span>Dirección <b class="req">*</b></span><input id="c-dir" autocomplete="street-address" placeholder="Calle 5 # 66-20, apto 301" maxlength="160" aria-required="true"><small class="msg" hidden></small></label>
        <label class="f2 ancho"><span>Indicaciones para la entrega <i>(opcional)</i></span><input id="c-ind" maxlength="200" placeholder="Torre 2, portería; llamar antes"></label>
        <label class="f2 ancho"><span>Modelo del nevecón <i>(opcional)</i></span><input id="c-modelo" maxlength="40" placeholder="Nos ayuda a confirmar que le sirve"></label>
      </div>
      <div id="entrega" class="entrega"></div>
    </section>
  </div>
  <aside class="col resumen">
    <section class="caja paso">
      <h2><span class="np">4</span>Resumen y pago</h2>
      <div id="totales"></div>
      <div class="lista-req" id="lista-req" aria-live="polite"></div>
      <label class="check2" data-f="acepto"><input type="checkbox" id="c-acepto" aria-required="true"><span><b>Acepto los <a href="/terminos.php" target="_blank" rel="noopener">términos</a>, la <a href="/garantia-y-retracto.php" target="_blank" rel="noopener">garantía y el retracto</a> y la <a href="/privacidad.php" target="_blank" rel="noopener">política de datos</a> <b class="req">*</b></b></span></label>
      <small class="msg" id="m-acepto" hidden></small>
      <label class="check2"><input type="checkbox" id="c-rec"><span>Recuérdame por correo cuando toque cambiar el filtro (cada 6 meses). <i>Opcional.</i></span></label>
      <button class="btn block" type="button" id="pagar">Pagar</button>
      <div class="err" id="err" role="alert" aria-live="assertive"></div>
      <div class="sellos"><span>🔒 Pago seguro</span><span>🚚 Envío gratis a toda Colombia</span><span>💬 Asesoría por WhatsApp</span></div><?= medios_pago_html() ?>
      <p class="m" style="font-size:12.5px;margin:0">Pagas con tarjeta, PSE, Nequi o botón Bancolombia.</p>
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
  function instalacion() { return entrega === "instalacion" && lineas().some(l => P[l.pid].ubic === "externo") ? C.inst_ext : 0; }
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
        <div class="lder"><button type="button" class="lx" data-del="${i}" aria-label="Quitar ${esc(p.nombre)} del carrito" title="Quitar del carrito">✕</button><b class="lprecio">${cop(unit * l.cant)}</b></div></div>`;
    }).join("");
    const ciudad = $("#c-ciudad").value, cali = false;  // la entrega local se coordina por WhatsApp
    const ext = L.some(l => P[l.pid].ubic === "externo"), cInst = ext ? C.inst_ext : 0;
    const ops = cali ? [["instalacion", "Te lo llevamos e instalamos", ext ? `Te llamamos para acordar el día y la hora. La instalación del filtro externo (en la manguera) cuesta ${cop(C.inst_ext)}${C.pago_link ? " y se paga el día de la instalación" : ""}; los internos se instalan gratis.` : "Te llamamos para acordar el día y la hora.", cInst], ["domicilio", "Solo entrega, sin instalación", "Te llamamos para acordar el día y la hora.", 0]]
      : ciudad ? [["transportadora", "Envío por transportadora", `Llega en unos ${(C.dias || {})[ciudad] || 2} días hábiles, hacia el ${habiles((C.dias || {})[ciudad] || 2)}. Te enviamos la guía al correo.`, 0]] : [];
    if (!ops.some(o => o[0] === entrega)) entrega = ops[0]?.[0] || null;
    $("#entrega").innerHTML = ciudad ? `<b>Entrega en ${esc(ciudad)}</b>` + ops.map(([k, t, s, v]) => `<label class="opc"><input type="radio" name="ent" value="${k}" ${k === entrega ? "checked" : ""}><span><b>${t}</b><small>${s}</small></span><span class="${v ? "" : "gratis"}">${v ? cop(v) : "Gratis"}</span></label>`).join("") : `<span class="m">Escoge tu ciudad para ver la entrega.</span>`;
    const n = L.reduce((a, l) => a + l.cant * (l.pack ? 2 : 1), 0), inst = instalacion(), t = total() + (C.pago_link ? 0 : inst);
    $("#totales").innerHTML = `<div class="tl"><span>${n} ${n === 1 ? "filtro" : "filtros"}</span><span>${cop(total())}</span></div><div class="tl"><span>Envío${cali ? " a domicilio" : ""}</span><span class="gratis">Gratis</span></div>`
      + (inst ? `<div class="tl"><span>Instalación del filtro externo${C.pago_link ? " (se paga al instalar)" : ""}</span><span>${cop(inst)}</span></div>` : "")
      + `<div class="tl total"><span>${C.pago_link && inst ? "Total a pagar ahora" : "Total"}</span><span>${cop(t)}</span></div>`;
    $("#pagar").textContent = `Pagar ${cop(t)}`;
  }
  $("#c-ciudad").innerHTML = `<option value="">Escoge tu ciudad</option>` + C.ciudades.map(c => `<option>${esc(c)}</option>`).join("");
  const prev = ls.get("fy_cliente", {}), cityPrev = ls.get("fy_city", "");
  [["c-nombre", "nombre"], ["c-tel", "tel"], ["c-email", "email"], ["c-barrio", "barrio"], ["c-dir", "dir"]].forEach(([id, k]) => { if (prev[k]) $("#" + id).value = prev[k]; });
  if (C.ciudades.includes(cityPrev)) $("#c-ciudad").value = cityPrev;
  $("#c-rec").checked = !!prev.recordar;
  $("#c-ciudad").addEventListener("change", e => { ls.set("fy_city", e.target.value); pintar(); });
  document.addEventListener("change", e => { if (e.target.name === "ent") { entrega = e.target.value; pintar(); } });
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
  $("#vaciar").addEventListener("click", () => { FYCart.guardar([]); pintar(); });
  // ---- Campos obligatorios: se marcan y se dice cuáles faltan ----
  const val = {
    nombre: { id: "c-nombre", et: "Nombre completo", ok: v => v.trim().length >= 3, msg: "Escribe tu nombre completo." },
    tel: { id: "c-tel", et: "Celular", ok: v => /^3\d{9}$/.test(telok(v)), msg: "Escribe un celular de 10 dígitos que empiece por 3." },
    email: { id: "c-email", et: "Correo", ok: v => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.trim()), msg: "Escribe un correo válido, como nombre@gmail.com." },
    ciudad: { id: "c-ciudad", et: "Ciudad", ok: v => !!v, msg: "Escoge tu ciudad." },
    barrio: { id: "c-barrio", et: "Barrio", ok: v => v.trim().length >= 2, msg: "Escribe el barrio." },
    dir: { id: "c-dir", et: "Dirección", ok: v => v.trim().length >= 5, msg: "Escribe la dirección completa." },
    acepto: { id: "c-acepto", et: "Aceptar términos y política de datos", ok: () => $("#c-acepto").checked, msg: "Debes aceptar los términos y la política de datos." }
  };
  function telok(v) { return v.replace(/\D/g, "").replace(/^57(?=3\d{9}$)/, ""); }
  const tocado = new Set();
  function marcar(k) {
    const f = val[k], el = $("#" + f.id), bad = !f.ok(el.value), cont = k === "acepto" ? $('[data-f="acepto"]') : el.closest("label"), msg = k === "acepto" ? $("#m-acepto") : cont.querySelector(".msg");
    const mostrar = bad && tocado.has(k);
    cont.classList.toggle("malo", mostrar); el.setAttribute("aria-invalid", mostrar ? "true" : "false");
    if (msg) { msg.hidden = !mostrar; msg.textContent = mostrar ? f.msg : ""; }
    return bad;
  }
  function lista() {
    const falta = Object.keys(val).filter(k => !val[k].ok($("#" + val[k].id).value));
    $("#lista-req").innerHTML = falta.length
      ? `<b>Para hacer el pedido te falta:</b><ul>${falta.map(k => `<li><button type="button" class="link" data-ir="${k}">${esc(val[k].et)}</button></li>`).join("")}</ul>`
      : `<span class="ok-req">✓ Tienes todos los datos. Ya puedes pagar.</span>`;
    return falta;
  }
  Object.keys(val).forEach(k => {
    const el = $("#" + val[k].id);
    ["input", "change"].forEach(ev => el.addEventListener(ev, () => { if (tocado.has(k)) marcar(k); lista(); }));
    el.addEventListener("blur", () => { tocado.add(k); marcar(k); });
  });
  $("#lista-req").addEventListener("click", e => { const b = e.target.closest("[data-ir]"); if (!b) return; const el = $("#" + val[b.dataset.ir].id); el.scrollIntoView({ behavior: "smooth", block: "center" }); el.focus({ preventScroll: true }); });
  $("#pagar").addEventListener("click", async () => {
    const v = id => $("#" + id).value.trim(), err = $("#err");
    const cli = { nombre: v("c-nombre"), tel: telok(v("c-tel")), email: v("c-email"), ciudad: $("#c-ciudad").value, barrio: v("c-barrio"), dir: v("c-dir"), indicaciones: v("c-ind"), modelo: v("c-modelo"), recordar: $("#c-rec").checked };
    Object.keys(val).forEach(k => tocado.add(k));
    const falta = Object.keys(val).filter(marcar);
    lista();
    if (falta.length) {
      err.innerHTML = `<b>Faltan ${falta.length} ${falta.length === 1 ? "dato" : "datos"} para hacer el pedido:</b> ${falta.map(k => esc(val[k].et)).join(", ")}.`;
      const el = $("#" + val[falta[0]].id); el.scrollIntoView({ behavior: "smooth", block: "center" }); el.focus({ preventScroll: true });
      return;
    }
    const b = $("#pagar"), old = b.textContent; b.disabled = true; b.textContent = "Abriendo el pago seguro…"; err.textContent = "";
    ls.set("fy_cliente", { nombre: cli.nombre, tel: cli.tel, email: cli.email, barrio: cli.barrio, dir: cli.dir, recordar: cli.recordar });
    try {
      const L = lineas(), t = total() + (C.pago_link ? 0 : instalacion());
      const r = await fetch("/api/pedido.php", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ acepto: true, items: L.map(l => ({ pid: l.pid, pack: !!l.pack, cant: l.cant })), total: t, entrega, cliente: cli }) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.url) throw new Error(j.mensaje || "No se pudo crear el pedido. Intenta de nuevo.");
      window.FYForm && FYForm(j.form);  // los datos del cliente llegan a tu correo como formulario (sin esperar)
      const cambio = new Date(); cambio.setMonth(cambio.getMonth() + 6);
      const o = ls.get("fy_orders", []).filter(x => x.id !== j.ref);
      o.unshift({ id: j.ref, fecha: new Date().toISOString(), cambio: cambio.toISOString(), producto: P[L[0].pid].nombre + (L.length > 1 ? ` y ${L.length - 1} más` : ""), ref: P[L[0].pid].ref, pid: L[0].pid, total: j.total, ciudad: cli.ciudad, entrega, pago: "wompi", estado: "Pago pendiente", cliente: { recordar: cli.recordar } });
      ls.set("fy_orders", o.slice(0, 50));
      window.FYPago ? FYPago(j.url, j.total, j.ref) : (location.href = j.url);
    } catch (x) { err.textContent = x.message; b.disabled = false; b.textContent = old; }
  });
  pintar(); lista();
});
</script>
<?php pie(); ?>
