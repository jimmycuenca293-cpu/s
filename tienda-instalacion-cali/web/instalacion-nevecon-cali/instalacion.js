/* Reserva de instalación: precio, agenda y envío. El servidor vuelve a calcular el precio y revisa que el horario siga libre. */
(() => {
  "use strict";
  const I = window.INST, $ = s => document.querySelector(s), f = $("#f");
  const cop = n => "$ " + Math.round(n).toLocaleString("es-CO");
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  const st = { fecha: "", franja: -1, dias: [], off: 0 };
  const val = n => (f.elements[n] && f.elements[n].value || "").trim();
  const radio = n => { const r = f.querySelector(`input[name="${n}"]:checked`); return r ? r.value : ""; };
  window.dataLayer = window.dataLayer || [];

  function marcaOtra() { const o = $("#otra-marca"); if (o) o.hidden = val("marca_nevecon") !== "Otra"; }
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
    const dia = st.dias.find(d => d.fecha === st.fecha), hr = dia && dia.franjas[st.franja] && dia.franjas[st.franja].libre ? dia.franjas[st.franja] : null;
    const L = [["Servicio", p.s.corto], ["Zona", p.z ? p.z.nombre + (p.z.recargo ? " (+" + cop(p.z.recargo) + ")" : "") : "Escoge tu zona"],
      ["Manguera", metrosTxt[p.m] + (p.extra ? " (+" + cop(p.extra) + ")" : "")], ["Día", dia ? dia.txt : "Escoge el día"], ["Hora", hr ? hr.txt : "Escoge la hora"]];
    $("#lineas").innerHTML = L.map(([a, b]) => `<div class="l"><span>${a}</span><b>${esc(b)}</b></div>`).join("");
    const tot = radio("forma_pago") === "total", online = tot ? p.s.precio : p.reserva, efec = p.total - online;
    $("#total").textContent = cop(p.total); $("#reserva").textContent = cop(online);
    $("#ahora-t").textContent = tot ? "Hoy pagas, en línea" : "Hoy pagas la 1ª parte, en línea";
    $("#ahora-s").innerHTML = tot ? (efec ? 'Y ' + cop(efec) + " en efectivo al técnico al terminar (recargo de zona o manguera adicional)." : "Con Wompi, desde la siguiente pantalla. Al terminar no pagas nada más.")
      : 'Y el saldo de <b id="saldo" style="display:inline;font-size:inherit">' + cop(efec) + "</b> en efectivo al técnico, al terminar.";
    $("#enviar").textContent = tot ? "Reservar y pagar todo: " + cop(online) : "Reservar y pagar la 1ª parte: " + cop(online);
    const ft = $("#fp-total"), fd = $("#fp-dos");
    if (ft) ft.textContent = "Pagas " + cop(p.s.precio) + " hoy en línea con Wompi. Al terminar " + (p.total - p.s.precio ? "solo pagas " + cop(p.total - p.s.precio) + " en efectivo (recargo de zona o manguera adicional)." : "no pagas nada más.");
    if (fd) fd.textContent = "Hoy pagas " + cop(p.reserva) + " en línea. Al terminar le pagas " + cop(p.total - p.reserva) + " en efectivo al técnico.";
    $("#barra-r").textContent = "Hoy pagas " + cop(online);
    $("#barra-t").textContent = tot ? (efec ? "Total " + cop(p.total) + " · efectivo " + cop(efec) : "Total " + cop(p.total) + " · pago único") : "Total " + cop(p.total) + " · saldo en efectivo " + cop(efec);
    $("#p1").classList.toggle("hecho", !!p.s); $("#p2").classList.toggle("hecho", !!p.z); $("#p3").classList.add("hecho");
    const fa = [...new Set(faltantes().map(x => x[1]))];
    $("#falta").textContent = fa.length ? "Te falta: " + fa.join(", ") + "." : "¡Todo listo! Ya puedes reservar.";
    $("#falta").classList.toggle("listo", !fa.length);
    $("#p4").classList.toggle("hecho", !!(dia && hr)); $("#p6").classList.toggle("hecho", !!(val("nombre") && val("tel") && val("email") && val("barrio") && val("dir")));
  }
  const DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"], MESES = ["", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
  function pintarFechas() {
    const box = $("#cal");
    if (!st.dias.length) { box.innerHTML = `<span class="m">No pudimos cargar la agenda. Recarga la página o escríbenos por WhatsApp.</span>`; return; }
    const lead = (st.dias[0].dow + 6) % 7;
    let h = DIAS.map(d => `<span class="cab">${d}</span>`).join("") + '<span class="ic-d vacio"></span>'.repeat(lead);
    st.dias.forEach((d, i) => {
            const pasado = !d.cerrado && d.franjas.every(x => x.estado === "pasado");
      const cls = d.cerrado || pasado ? "cerrado" : d.libres === 0 ? "lleno" : d.libres <= 2 ? "pocos" : "libre";
      const txt = d.cerrado ? "—" : pasado ? "ya pasó" : d.libres === 0 ? "lleno" : d.libres === 1 ? "1 cupo" : d.libres + " cupos";
      const lab = i === 0 ? "hoy" : d.dia === 1 ? MESES[d.mes] : "";
      h += `<button type="button" class="ic-d ${cls}" data-f="${d.fecha}" aria-pressed="${d.fecha === st.fecha}" ${cls === "libre" || cls === "pocos" ? "" : "disabled"} aria-label="${esc(d.txt)}: ${esc(d.cerrado ? d.motivo : txt)}"><span class="mes">${esc(lab)}</span><b>${d.dia}</b><small>${txt}</small></button>`;
    });
    box.innerHTML = h;
    pintarHoras();
  }
  const ETQ = { libre: "", ocupado: "Ocupado", pasado: "Muy pronto" };
  function pintarHoras() {
    const d = st.dias.find(x => x.fecha === st.fecha), box = $("#horas");
    if (!d) { box.innerHTML = `<span class="m">Escoge primero un día del calendario.</span>`; return; }
    box.innerHTML = d.franjas.map(x => `<button type="button" class="ic-hora" data-i="${x.i}" aria-pressed="${x.i === st.franja && x.libre}" ${x.libre ? "" : "disabled"}><span>${esc(x.txt)}</span>${x.libre ? "" : `<small>${ETQ[x.estado] || ""}</small>`}</button>`).join("");
  }
  function proximo() {
    const el = $("#proximo"); if (!el || !st.dias.length) return;
    const sem = st.dias.slice(0, 7).reduce((n, d) => n + d.libres, 0);
    const d = st.dias.find(x => x.libres > 0); if (!d) { el.hidden = true; return; }
    const h = d.franjas.find(z => z.libre);
    el.textContent = "Próximo horario libre: " + d.txt + ", " + h.txt + (sem ? " · " + sem + (sem === 1 ? " cupo" : " cupos") + " en los próximos 7 días" : "");
    el.hidden = false;
  }
  // Reloj con la hora de Colombia (se corrige con la hora del servidor, aunque el celular tenga la hora mal)
  const fmtF = new Intl.DateTimeFormat("es-CO", { timeZone: "America/Bogota", weekday: "long", day: "numeric", month: "long", year: "numeric" });
  const fmtH = new Intl.DateTimeFormat("es-CO", { timeZone: "America/Bogota", hour: "numeric", minute: "2-digit", second: "2-digit", hour12: true });
  function reloj() {
    const n = new Date(Date.now() + st.off), el = $("#reloj"); if (!el) return;
    const f1 = fmtF.format(n); el.textContent = "Hoy es " + f1.charAt(0).toUpperCase() + f1.slice(1) + " · " + fmtH.format(n) + " (hora de Colombia)";
  }
  setInterval(reloj, 1000); reloj();
  async function cargarDias(silencioso) {
    const tenia = st.franja >= 0 ? { fecha: st.fecha, franja: st.franja } : null;
    try {
      const r = await fetch("/filtrosnevecones-api/instalacion.php?a=dias", { cache: "no-store" }), j = await r.json();
      st.dias = j.dias || []; if (j.ts) st.off = j.ts * 1000 - Date.now();
    } catch { if (silencioso) return; st.dias = []; }
    if (st.fecha) {
      const d = st.dias.find(x => x.fecha === st.fecha), ok = d && d.franjas[st.franja] && d.franjas[st.franja].libre;
      if (!ok) { st.franja = -1; if (tenia) $("#aviso-horario").textContent = "El horario que habías escogido ya no está disponible (alguien lo reservó o ya falta poco). Escoge otro, por favor."; }
      if (!d || !d.libres) { st.fecha = ""; st.franja = -1; }
    }
    pintarFechas(); pintar(); proximo(); reloj();
  }
  setInterval(() => { if (!document.hidden) cargarDias(true); }, 30000);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) cargarDias(true); });
  document.addEventListener("click", e => {
    const a = e.target.closest("[data-f]"); if (a) { st.fecha = a.dataset.f; st.franja = -1; $("#aviso-horario").textContent = ""; pintarFechas(); pintar(); $("#horas").scrollIntoView({ block: "nearest", behavior: "smooth" }); return; }
    const h = e.target.closest("[data-i]"); if (h) { st.franja = +h.dataset.i; $("#aviso-horario").textContent = ""; pintarHoras(); pintar(); }
  });
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-pick]"); if (!b) return;
    const r = f.querySelector(`input[name="servicio"][value="${b.dataset.pick}"]`); if (r) r.checked = true;
    const fp = b.dataset.forma && f.querySelector(`input[name="forma_pago"][value="${b.dataset.forma}"]`); if (fp) fp.checked = true;
    pintar();
  });
  f.addEventListener("input", pintar); f.addEventListener("change", () => { marcaOtra(); pintar(); });

  function faltantes() {
    const F = [];
    if (!radio("zona")) F.push(["p2", "tu zona"]);
    if (!st.fecha || st.franja < 0) F.push(["p4", "el día y la hora"]);
    const c = { nombre: val("nombre").length >= 3, tel: /^3\d{9}$/.test(val("tel").replace(/\D/g, "").replace(/^57(?=3\d{9}$)/, "")), email: /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(val("email")),
      marca: !!val("marca_nevecon"), barrio: !!val("barrio"), dir: val("dir").length >= 5 };
    if (!c.nombre) F.push(["p6", "tu nombre"]); if (!c.tel) F.push(["p6", "un celular válido (10 dígitos que empiezan por 3)"]); if (!c.email) F.push(["p6", "un correo válido"]);
    if (!c.marca) F.push(["p6", "la marca del nevecón"]); if (val("marca_nevecon") === "Otra" && !val("marca_otra")) F.push(["p6", "cuál es la otra marca"]); if (!c.barrio) F.push(["p6", "el barrio"]); if (!c.dir) F.push(["p6", "la dirección"]);
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
    if (body.marca_nevecon === "Otra") body.marca_nevecon = "Otra: " + (val("marca_otra") || "sin decir");
    try {
      const r = await fetch("/filtrosnevecones-api/instalacion.php?a=reservar", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const j = await r.json().catch(() => ({}));
      if (!r.ok || !j.url) { if (r.status === 409) cargarDias(); throw new Error(j.mensaje || "No se pudo crear la reserva. Intenta de nuevo o escríbenos por WhatsApp."); }
      let ido = false; const ir = () => { if (!ido) { ido = true; location.href = j.url; } };
      dataLayer.push({ event: "reserva_instalacion", value: j.total, currency: "COP", transaction_id: j.ref, eventCallback: ir, eventTimeout: 300 });
      setTimeout(ir, 350);
    } catch (x) { err.textContent = x.message; b.disabled = false; b.textContent = old; }
  });
  // Recuerda tus datos en este navegador para la próxima vez, y da formato al celular
  const KEEP = ["nombre", "tel", "email", "marca_nevecon", "modelo", "barrio", "dir", "detalle"];
  try { const g = JSON.parse(localStorage.getItem("ic_cliente") || "{}"); KEEP.forEach(k => { if (g[k] && f.elements[k] && !f.elements[k].value) f.elements[k].value = g[k]; }); } catch {}
  f.addEventListener("input", e => {
    if (e.target.name === "tel") { const d = e.target.value.replace(/\D/g, "").replace(/^57(?=3)/, "").slice(0, 10); e.target.value = d.replace(/(\d{3})(\d{0,3})(\d{0,4})/, (m, a, b, c) => [a, b, c].filter(Boolean).join(" ")); }
    try { const g = {}; KEEP.forEach(k => g[k] = val(k)); localStorage.setItem("ic_cliente", JSON.stringify(g)); } catch {}
  });
  cargarDias(); pintar();
})();
