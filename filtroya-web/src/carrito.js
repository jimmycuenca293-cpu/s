/* Carrito de la tienda: se guarda en el navegador y se ve en todas las páginas. */
(() => {
  "use strict";
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
