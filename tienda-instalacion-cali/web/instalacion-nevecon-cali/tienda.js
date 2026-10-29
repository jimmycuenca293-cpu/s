/* Tienda de instalación (portada y fichas): precios por zona, enlaces de reserva, hora de Colombia y próximo horario libre. */
(() => {
  "use strict";
  const I = window.INST, $ = s => document.querySelector(s);
  const cop = n => "$ " + Math.round(n).toLocaleString("es-CO"), nb = n => cop(n).replace(" ", " ");
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  let zona = "", forma = "reserva", off = 0, dias = [];
  const leerZona = () => {
    const q = new URLSearchParams(location.search).get("z"); if (q && I.zonas[q]) return q;
    try { const s = sessionStorage.getItem("ic_zona"); if (s && I.zonas[s]) return s; } catch (e) {}
    return Object.keys(I.zonas)[0];
  };
  function enlaces() {
    document.querySelectorAll("a[data-r]").forEach(a => { a.href = "/instalacion-nevecon-cali/reservar/?s=" + encodeURIComponent(a.dataset.r) + "&z=" + encodeURIComponent(zona) + "&f=" + (a.dataset.f || forma); });
  }
  function aplicar(z) {
    zona = z; try { sessionStorage.setItem("ic_zona", z); } catch (e) {}
    const Z = I.zonas[z];
    document.querySelectorAll("[data-zona]").forEach(b => b.setAttribute("aria-pressed", b.dataset.zona === z));
    document.querySelectorAll("[data-zn]").forEach(e => { e.textContent = Z.nombre; });
    document.querySelectorAll("[data-s][data-k]").forEach(e => {
      const s = I.servicios[e.dataset.s]; if (!s) return;
      const tot = s.precio + Z.recargo, on = ((I.total_online[e.dataset.s] || {})[z]) || s.precio, k = e.dataset.k;
      if (k === "precio") e.textContent = cop(tot);
      else if (k === "online") e.textContent = nb(on);
      else if (k === "resto") e.textContent = nb(tot - s.reserva);
      else if (k === "s2total") e.textContent = tot - on > 0 ? "+ " + cop(tot - on) + " en efectivo al terminar (recargo de zona)." : "Al terminar no pagas nada más.";
    });
    enlaces();
  }
  document.addEventListener("click", e => { const b = e.target.closest("[data-zona]"); if (b) aplicar(b.dataset.zona); });
  document.addEventListener("change", e => { if (e.target.name === "fp") { forma = e.target.value; enlaces(); } });
  aplicar(leerZona());
  const fp = document.querySelector('input[name="fp"]:checked'); if (fp) { forma = fp.value; enlaces(); }

  // Hora de Colombia y estado de atención (se corrige con la hora del servidor)
  const fmtF = new Intl.DateTimeFormat("es-CO", { timeZone: "America/Bogota", weekday: "long", day: "numeric", month: "long", year: "numeric" });
  const fmtH = new Intl.DateTimeFormat("es-CO", { timeZone: "America/Bogota", hour: "numeric", minute: "2-digit", second: "2-digit", hour12: true });
  const fmtP = new Intl.DateTimeFormat("en-US", { timeZone: "America/Bogota", weekday: "short", hour: "2-digit", minute: "2-digit", hour12: false });
  const DN = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 }, NOM = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  function atencion(d) {
    const p = Object.fromEntries(fmtP.formatToParts(d).map(x => [x.type, x.value])), dow = DN[p.weekday], h = (+p.hour % 24) + (+p.minute) / 60, [a, c] = I.atencion || [8, 17];
    if (dow !== 0 && h >= a && h < c) return { abierto: true, txt: "<b>Asesores atendiendo ahora</b> (lunes a sábado, " + a + ":00 a. m. a " + (c - 12) + ":00 p. m.)" };
    let sig = h < a && dow !== 0 ? 0 : 1, n = (dow + sig) % 7; while (n === 0) { sig++; n = (dow + sig) % 7; }
    return { abierto: false, txt: "<b>Atención cerrada ahora.</b> Te escribimos " + (sig === 0 ? "hoy" : sig === 1 ? "mañana " + NOM[n] : "el " + NOM[n]) + " desde las " + a + ":00 a. m." };
  }
  function reloj() {
    const el = $("#ahora-co-t"); if (!el) return;
    const n = new Date(Date.now() + off), a = atencion(n), f1 = fmtF.format(n);
    el.innerHTML = "Hoy es " + esc(f1.charAt(0).toUpperCase() + f1.slice(1)) + " · <b>" + fmtH.format(n) + "</b> (hora de Colombia)<br>" + a.txt;
    el.parentNode.classList.toggle("cerrado", !a.abierto);
  }
  function proximo() {
    const el = $("#proximo"); if (!el || !dias.length) return;
    const d = dias.find(x => x.libres > 0); if (!d) { el.hidden = true; return; }
    const h = d.franjas.find(z => z.libre), sem = dias.slice(0, 7).reduce((n, x) => n + x.libres, 0);
    el.textContent = "Próximo horario libre: " + d.txt + ", " + h.txt + " · " + sem + (sem === 1 ? " cupo" : " cupos") + " en los próximos 7 días";
    el.hidden = false;
  }
  async function cargar() {
    try { const r = await fetch("/filtrosnevecones-api/instalacion.php?a=dias", { cache: "no-store" }), j = await r.json(); if (Array.isArray(j.dias)) { dias = j.dias; if (j.ts) off = j.ts * 1000 - Date.now(); } } catch (e) {}
    proximo(); reloj();
  }
  setInterval(reloj, 1000); reloj();
  if ($("#ahora-co-t") || $("#proximo")) { cargar(); setInterval(() => { if (!document.hidden) cargar(); }, 60000); }
})();
