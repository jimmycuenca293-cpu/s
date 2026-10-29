/* Reserva de instalación: precio, agenda y envío. El servidor vuelve a calcular el precio y revisa que el horario siga libre. */
(() => {
  "use strict";
  const I = window.INST, $ = s => document.querySelector(s), f = $("#f");
  const cop = n => "$ " + Math.round(n).toLocaleString("es-CO");
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const st = { fecha: "", franja: -1, dias: [] };
  const val = n => (f.elements[n] && f.elements[n].value || "").trim();
  const radio = n => { const r = f.querySelector(`input[name="${n}"]:checked`); return r ? r.value : ""; };
  window.dataLayer = window.dataLayer || [];

  function precio() {
    const s = I.servicios[radio("servicio")], z = I.zonas[radio("zona")], m = val("metros");
    if (!s) return null;
    const extra = ["10", "15", "20"].includes(m) ? ((+m - 5) / 5) * I.metro_extra : 0;
    const total = s.precio + (z ? z.recargo : 0) + extra;
    return { s, z, m, extra, total, reserva: s.reserva, saldo: total - s.reserva };
  }
  const metrosTxt = { 5: "Hasta 5 m (incluidos)", 10: "Hasta 10 m", 15: "Hasta 15 m", 20: "Hasta 20 m", nose: "El técnico la mide" };
  function pintar() {
    const p = precio(); if (!p) return;
    const dia = st.dias.find(d => d.fecha === st.fecha), hr = dia && dia.franjas[st.franja];
    const L = [["Servicio", p.s.corto], ["Zona", p.z ? p.z.nombre + (p.z.recargo ? " (+" + cop(p.z.recargo) + ")" : "") : "Escoge tu zona"],
      ["Manguera", metrosTxt[p.m] + (p.extra ? " (+" + cop(p.extra) + ")" : "")], ["Día", dia ? dia.txt : "Escoge el día"], ["Hora", hr ? hr.txt : "Escoge la hora"]];
    $("#lineas").innerHTML = L.map(([a, b]) => `<div class="l"><span>${a}</span><b>${esc(b)}</b></div>`).join("");
    const tot = radio("forma_pago") === "total";
    $("#total").textContent = cop(p.total); $("#reserva").textContent = cop(tot ? p.total : p.reserva);
    $("#ahora-t").textContent = tot ? "Pagas el total en línea" : "Pagas ahora para reservar";
    $("#ahora-s").innerHTML = tot ? "Te enviamos el link de pago por WhatsApp. Al terminar no pagas nada más." : 'Y el saldo de <b id="saldo" style="display:inline;font-size:inherit">' + cop(p.saldo) + "</b> en efectivo al técnico, al terminar.";
    $("#enviar").textContent = tot ? "Reservar y pagar el total " + cop(p.total) : "Reservar y pagar " + cop(p.reserva);
    $("#barra-r").textContent = tot ? "Total " + cop(p.total) : "Reserva " + cop(p.reserva); $("#barra-t").textContent = tot ? "Pago en línea del total" : "Total " + cop(p.total) + " · saldo en efectivo " + cop(p.saldo);
    $("#p1").classList.toggle("hecho", !!p.s); $("#p2").classList.toggle("hecho", !!p.z); $("#p3").classList.add("hecho");
    $("#p4").classList.toggle("hecho", !!(dia && hr)); $("#p6").classList.toggle("hecho", !!(val("nombre") && val("tel") && val("email") && val("barrio") && val("dir")));
  }
  function pintarFechas() {
    const box = $("#fechas");
    if (!st.dias.length) { box.innerHTML = `<span class="m">No hay días disponibles ahora. Escríbenos por WhatsApp.</span>`; return; }
    box.innerHTML = st.dias.map(d => {
      const libres = d.franjas.filter(x => x.libre).length, [dia, num] = d.corto.split(" ");
      return `<button type="button" class="ic-fecha" data-f="${d.fecha}" aria-pressed="${d.fecha === st.fecha}" ${libres ? "" : "disabled"} aria-label="${esc(d.txt)}"><span>${esc(dia)}</span><b>${esc(num)}</b><span>${libres ? libres + (libres === 1 ? " cupo" : " cupos") : "lleno"}</span></button>`;
    }).join("");
    pintarHoras();
  }
  function pintarHoras() {
    const d = st.dias.find(x => x.fecha === st.fecha), box = $("#horas");
    if (!d) { box.innerHTML = `<span class="m">Escoge primero un día.</span>`; return; }
    box.innerHTML = d.franjas.map(x => `<button type="button" class="ic-hora" data-i="${x.i}" aria-pressed="${x.i === st.franja}" ${x.libre ? "" : "disabled"}>${esc(x.txt)}</button>`).join("");
  }
  function proximo() {
    const el = $("#proximo"); if (!el || !st.dias.length) return;
    const sem = st.dias.slice(0, 6).reduce((n, d) => n + d.franjas.filter(x => x.libre).length, 0);
    const d = st.dias.find(x => x.franjas.some(z => z.libre)); if (!d) return;
    const h = d.franjas.find(z => z.libre);
    el.textContent = "Próximo horario libre: " + d.txt + ", " + h.txt + (sem ? " · " + sem + (sem === 1 ? " cupo" : " cupos") + " en los próximos días" : "");
    el.hidden = false;
  }
  async function cargarDias() {
    try {
      const r = await fetch("/filtrosnevecones-api/instalacion.php?a=dias", { cache: "no-store" }), j = await r.json();
      st.dias = j.dias || [];
      if (st.fecha && !st.dias.find(d => d.fecha === st.fecha && d.franjas[st.franja] && d.franjas[st.franja].libre)) { st.franja = -1; }
    } catch { st.dias = []; }
    pintarFechas(); pintar(); proximo();
  }
  document.addEventListener("click", e => {
    const a = e.target.closest("[data-f]"); if (a) { st.fecha = a.dataset.f; st.franja = -1; pintarFechas(); pintar(); $("#horas").scrollIntoView({ block: "nearest", behavior: "smooth" }); return; }
    const h = e.target.closest("[data-i]"); if (h) { st.franja = +h.dataset.i; pintarHoras(); pintar(); }
  });
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-pick]"); if (!b) return;
    const r = f.querySelector(`input[name="servicio"][value="${b.dataset.pick}"]`); if (r) { r.checked = true; pintar(); }
  });
  f.addEventListener("input", pintar); f.addEventListener("change", pintar);

  function faltantes() {
    const F = [];
    if (!radio("zona")) F.push(["p2", "tu zona"]);
    if (!st.fecha || st.franja < 0) F.push(["p4", "el día y la hora"]);
    const c = { nombre: val("nombre").length >= 3, tel: /^3\d{9}$/.test(val("tel").replace(/\D/g, "").replace(/^57(?=3\d{9}$)/, "")), email: /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val("email")),
      marca: !!val("marca_nevecon"), barrio: !!val("barrio"), dir: val("dir").length >= 5 };
    if (!c.nombre) F.push(["p6", "tu nombre"]); if (!c.tel) F.push(["p6", "un celular válido (10 dígitos que empiezan por 3)"]); if (!c.email) F.push(["p6", "un correo válido"]);
    if (!c.marca) F.push(["p6", "la marca del nevecón"]); if (!c.barrio) F.push(["p6", "el barrio"]); if (!c.dir) F.push(["p6", "la dirección"]);
    if (!f.elements.acepto.checked) F.push(["p6", "aceptar las condiciones"]);
    return F;
  }
  $("#barra-b").addEventListener("click", e => {
    const F = faltantes(); if (!F.length) { e.preventDefault(); f.requestSubmit(); return; }
    e.preventDefault(); const el = document.getElementById(F[0][0]); el && el.scrollIntoView({ behavior: "smooth", block: "start" });
  });
  f.addEventListener("submit", async e => {
    e.preventDefault();
    const err = $("#err"), b = $("#enviar"), F = faltantes();
    if (F.length) { err.textContent = "Falta " + [...new Set(F.map(x => x[1]))].join(", ") + "."; document.getElementById(F[0][0]).scrollIntoView({ behavior: "smooth", block: "start" }); return; }
    const p = precio(), old = b.textContent; b.disabled = true; b.textContent = "Apartando tu horario…"; err.textContent = "";
    const body = { servicio: radio("servicio"), zona: radio("zona"), metros: val("metros"), total: p.total, fecha: st.fecha, franja: st.franja, acepto: f.elements.acepto.checked, web: val("web"), forma_pago: radio("forma_pago") };
    ["nombre", "tel", "email", "marca_nevecon", "modelo", "toma", "barrio", "dir", "detalle", "notas"].forEach(k => body[k] = val(k));
    try {
      const r = await fetch("/filtrosnevecones-api/instalacion.php?a=reservar", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.url) { if (r.status === 409) cargarDias(); throw new Error(j.mensaje || "No se pudo crear la reserva. Intenta de nuevo o escríbenos por WhatsApp."); }
      let ido = false; const ir = () => { if (!ido) { ido = true; location.href = j.url; } };
      dataLayer.push({ event: "reserva_instalacion", value: j.total, currency: "COP", transaction_id: j.ref, eventCallback: ir, eventTimeout: 300 });
      setTimeout(ir, 350);
    } catch (x) { err.textContent = x.message; b.disabled = false; b.textContent = old; }
  });
  cargarDias(); pintar();
})();
