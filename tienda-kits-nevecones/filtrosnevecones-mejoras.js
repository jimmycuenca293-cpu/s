/* Mejoras de la tienda: animación al agregar, barra de compra fija en el celular, fecha estimada de entrega, zoom de la foto,
   «vistos recientemente», compartir y aparición suave de las tarjetas. No toca precios, links de pago ni el carrito. */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const seguro = f => { try { f(); } catch (e) {} };
  const css = `
.fy-vuelo{position:fixed;z-index:9999;pointer-events:none;border-radius:12px;box-shadow:0 10px 28px rgba(0,0,0,.28);object-fit:contain;background:#fff}
.fy-bump{animation:fybump .5s}@keyframes fybump{30%{transform:scale(1.2)}60%{transform:scale(.95)}}
.fy-rv{opacity:0;transform:translateY(14px)}.fy-rv.fy-in{opacity:1;transform:none;transition:opacity .5s ease,transform .5s ease}
.fy-buybar{position:fixed;left:0;right:0;bottom:0;z-index:45;display:flex;align-items:center;gap:12px;padding:10px max(16px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));background:#fff;border-top:1px solid #d9e2fa;box-shadow:0 -8px 24px rgba(11,31,107,.14);transform:translateY(115%);transition:transform .28s ease}
.fy-buybar.on{transform:none}.fy-buybar .t{min-width:0;flex:1;line-height:1.2}.fy-buybar .t b{display:block;font-size:13px;color:#0b1a45;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.fy-buybar .t span{font-size:19px;font-weight:800;color:#ff4d2e}
.fy-buybar .btn{flex:0 0 auto;min-height:48px;padding:0 20px}
body.fy-conbar .wa-flot{bottom:calc(86px + env(safe-area-inset-bottom,0px))}body.fy-conbar main{padding-bottom:80px}
.fy-entrega{display:flex;gap:6px;align-items:flex-start;font-size:14px;font-weight:700;color:#1d7a46;margin:4px 0}
.fy-comp{align-self:flex-start;border:1px solid #d9e2fa;background:transparent;color:inherit;border-radius:10px;padding:8px 12px;font:inherit;font-weight:700;font-size:14px;cursor:pointer}
.fy-lb{position:fixed;inset:0;z-index:9998;background:rgba(5,12,40,.9);display:grid;place-items:center;padding:16px;cursor:zoom-out}.fy-lb img{max-width:min(96vw,900px);max-height:88vh;background:#fff;border-radius:14px;object-fit:contain}
.prod .foto img{cursor:zoom-in}
.fy-vistos{padding-block:8px 24px}.fy-vistos h2{font-size:19px;margin:0 0 10px}.fy-vs{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x proximity;padding-bottom:6px}
.fy-vs a{flex:0 0 150px;scroll-snap-align:start;background:#fff;border:1px solid #d9e2fa;border-radius:14px;padding:8px;display:flex;flex-direction:column;gap:4px;text-decoration:none;color:inherit}
.fy-vs img{width:100%;height:110px;object-fit:contain;background:#fff;border-radius:10px}.fy-vs b{font-size:13px;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.fy-vs span{font-weight:800;color:#ff4d2e}
@media (prefers-reduced-motion:reduce){.fy-rv{opacity:1;transform:none}.fy-bump{animation:none}}`;
  const st = document.createElement("style"); st.textContent = css; document.head.append(st);

  /* 1. Al agregar: la foto vuela hacia el carrito y el carrito «rebota» */
  seguro(() => document.addEventListener("click", e => {
    const b = e.target.closest("[data-add]"); if (!b || b.dataset.ir || quieto) return;
    const img = (b.closest(".card,.prod,.caja") || document).querySelector("img"), meta = $(".cartbtn,.cart-top");
    if (!img || !meta) return;
    const a = img.getBoundingClientRect(), z = meta.getBoundingClientRect(); if (!a.width || !z.width) return;
    const v = img.cloneNode(); v.className = "fy-vuelo"; v.removeAttribute("loading"); v.style.cssText = `left:${a.left}px;top:${a.top}px;width:${a.width}px;height:${a.height}px`;
    document.body.append(v);
    const an = v.animate([{ transform: "translate(0,0) scale(1)", opacity: 1 }, { transform: `translate(${z.left + z.width / 2 - a.left - a.width / 2}px,${z.top + z.height / 2 - a.top - a.height / 2}px) scale(.12)`, opacity: .2 }], { duration: 650, easing: "cubic-bezier(.5,0,.8,.4)" });
    an.onfinish = () => { v.remove(); meta.classList.remove("fy-bump"); void meta.offsetWidth; meta.classList.add("fy-bump"); };
  }));

  /* 2. Páginas de producto */
  const prod = $(".prod"), compra = $(".prod .compra");
  const nombre = () => ($("h1") || {}).textContent || document.title;
  const precio = () => (($(".prod .precio") || {}).textContent || "").trim();

  /* 2a. Fecha estimada de entrega (2 a 3 días hábiles, hora de Colombia) */
  seguro(() => { const p = $(".prod .precio"); if (!p) return;
    const hoy = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Bogota" }));
    const mas = n => { const d = new Date(hoy); let k = 0; while (k < n) { d.setDate(d.getDate() + 1); const w = d.getDay(); if (w && w < 6) k++; } return d.toLocaleDateString("es-CO", { weekday: "long", day: "numeric", month: "long" }); };
    const el = document.createElement("div"); el.className = "fy-entrega"; el.textContent = `🚚 Pídelo hoy y llega entre el ${mas(2)} y el ${mas(3)} (2 a 3 días hábiles)`;
    p.after(el); });

  /* 2b. Barra de compra fija en el celular cuando el botón principal sale de la pantalla */
  seguro(() => { if (!compra || !matchMedia("(max-width:760px)").matches || !("IntersectionObserver" in window)) return;
    const barra = document.createElement("div"); barra.className = "fy-buybar"; barra.setAttribute("aria-hidden", "true");
    barra.innerHTML = `<div class="t"><b></b><span></span></div><button type="button" class="btn">Agregar al carrito</button>`;
    document.body.append(barra);
    const poner = () => { $("b", barra).textContent = nombre(); $("span", barra).textContent = precio(); };
    $("button", barra).addEventListener("click", () => { const r = $("[data-add]:not([data-ir])", compra) || $("[data-add]", compra); if (r) r.click(); });
    new IntersectionObserver(([x]) => { const on = !x.isIntersecting; if (on) poner(); barra.classList.toggle("on", on); barra.setAttribute("aria-hidden", String(!on)); document.body.classList.toggle("fy-conbar", on); }).observe(compra); });

  /* 2c. Zoom de la foto */
  seguro(() => { const f = $(".prod .foto img"); if (!f) return;
    f.addEventListener("click", () => { const lb = document.createElement("div"); lb.className = "fy-lb"; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-label", "Foto ampliada"); const i = document.createElement("img"); i.src = f.currentSrc || f.src; i.alt = f.alt; lb.append(i);
      const cerrar = () => { lb.remove(); document.removeEventListener("keydown", k); }; const k = ev => { if (ev.key === "Escape") cerrar(); };
      lb.addEventListener("click", cerrar); document.addEventListener("keydown", k); document.body.append(lb); }); });

  /* 2d. Compartir */
  seguro(() => { if (!compra) return; const b = document.createElement("button"); b.type = "button"; b.className = "fy-comp"; b.textContent = "↗ Compartir este producto"; compra.after(b);
    b.addEventListener("click", () => { const d = { title: nombre(), text: `${nombre()} ${precio()} con envío gratis`, url: location.href };
      if (navigator.share) navigator.share(d).catch(() => {}); else window.open("https://wa.me/?text=" + encodeURIComponent(`${d.text}: ${d.url}`), "_blank", "noopener"); }); });

  /* 3. Vistos recientemente */
  seguro(() => { const K = "fy_vistos", leer = () => { try { return JSON.parse(localStorage.getItem(K) || "[]"); } catch { return []; } };
    let v = leer(); const aqui = location.pathname;
    if (prod) { const im = $(".prod .foto img"); const e = { u: aqui, n: nombre().trim(), p: precio(), i: im ? (im.getAttribute("src") || "") : "" };
      if (e.n && e.p && e.i) { v = [e].concat(v.filter(x => x.u !== aqui)).slice(0, 8); try { localStorage.setItem(K, JSON.stringify(v)); } catch {} } }
    const pie = $("footer.pie"), ok = prod || ["/", "/filtrosnevecones-tienda/", "/kits-instalacion-nevecones/"].includes(aqui);
    const lista = v.filter(x => x.u !== aqui); if (!pie || !ok || !lista.length) return;
    const s = document.createElement("section"); s.className = "wrap fy-vistos"; s.innerHTML = "<h2>Vistos recientemente</h2>";
    const c = document.createElement("div"); c.className = "fy-vs";
    lista.slice(0, 6).forEach(x => { const a = document.createElement("a"); a.href = x.u; const im = document.createElement("img"); im.src = x.i; im.alt = ""; im.loading = "lazy"; const b = document.createElement("b"); b.textContent = x.n; const p = document.createElement("span"); p.textContent = x.p; a.append(im, b, p); c.append(a); });
    s.append(c); pie.before(s); });

  /* 4. Aparición suave de las tarjetas que están más abajo */
  seguro(() => { if (quieto || !("IntersectionObserver" in window)) return;
    const t = $$(".grid .card").filter(x => x.getBoundingClientRect().top > innerHeight); if (!t.length) return;
    const o = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add("fy-in"); o.unobserve(x.target); } }), { rootMargin: "0px 0px -40px 0px" });
    t.forEach(x => { x.classList.add("fy-rv"); o.observe(x); }); setTimeout(() => t.forEach(x => x.classList.add("fy-in")), 2500); });
})();
