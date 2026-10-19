/* Carrito de la tienda: se guarda en el navegador y se ve en todas las páginas. */
(() => {
  "use strict";
  // Eventos para Google Tag Manager: "whatsapp" al tocar cualquier enlace de WhatsApp y "pago_wompi" al ir a la página de pago
  window.dataLayer = window.dataLayer || [];
  document.addEventListener("click", e => {
    const a = e.target.closest('a[href*="wa.me/"]');
    if (a) dataLayer.push({ event: "whatsapp", ubicacion: a.classList.contains("wa-flot") ? "boton_flotante" : "enlace", pagina: location.pathname });
  }, true);
  // Avisa del pago y luego abre la página de pago (máximo 0,35 segundos de espera para no demorar al cliente)
  window.FYPago = (url, total, ref) => {
    let ido = false; const ir = () => { if (!ido) { ido = true; location.href = url; } };
    dataLayer.push({ event: "pago_wompi", value: total, currency: "COP", transaction_id: ref, eventCallback: ir, eventTimeout: 300 });
    setTimeout(ir, 350);
  };
  // Manda los datos del pedido a tu correo como formulario (Web3Forms/FormSubmit) desde el navegador, sin hacer esperar al cliente
  window.FYForm = f => {
    if (!f || !f.url || !f.datos) return;
    try { fetch(f.url, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(f.datos), keepalive: true }).catch(() => {}); } catch {}
  };
  const K = "fy_carrito";
  const leer = () => { try { const v = JSON.parse(localStorage.getItem(K) || "[]"); return Array.isArray(v) ? v.filter(l => l && l.pid) : []; } catch { return []; } };
  const guardar = c => { try { localStorage.setItem(K, JSON.stringify(c)); } catch {} pintar(); };
  const contar = () => leer().reduce((a, l) => a + (l.cant || 1), 0);
  function agregar(pid, pack, cant) {
    const c = leer(), l = c.find(x => x.pid === pid && !!x.pack === !!pack);
    if (l) l.cant = Math.min(10, (l.cant || 1) + (cant || 1)); else c.push({ pid, pack: !!pack, cant: Math.min(10, cant || 1) });
    guardar(c);
  }
  function pintar() { const n = contar(); document.querySelectorAll("[data-cart-n]").forEach(e => { e.textContent = n; e.hidden = !n; }); }
  let t = null;
  function aviso(txt) {
    let el = document.getElementById("fy-toast");
    if (!el) { el = document.createElement("div"); el.id = "fy-toast"; el.className = "fy-toast"; el.setAttribute("role", "status"); document.body.append(el); }
    el.innerHTML = `<span></span><a href="/carrito.php">Ver carrito</a>`; el.firstChild.textContent = txt;
    el.classList.add("on"); clearTimeout(t); t = setTimeout(() => el.classList.remove("on"), 3800);
  }
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-add]"); if (!b) return;
    e.preventDefault();
    agregar(b.dataset.add, b.dataset.pack === "1", 1);
    if (b.dataset.ir) { location.href = "/carrito.php"; return; }
    aviso(b.dataset.pack === "1" ? "Pack anual agregado al carrito" : "Agregado al carrito");
  });
  window.FYCart = { leer, guardar, agregar, contar, pintar, aviso };
  pintar();
  document.addEventListener("DOMContentLoaded", pintar);
  window.addEventListener("storage", pintar);
})();
