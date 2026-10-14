/* =====================================================================
   TecniGuía Pro — puente entre la app y el servidor propio.
   La app pide sus capacidades con claude.use("sample" | "db" | "user" |
   "downloads"); aquí se cumplen con la API PHP del servidor del técnico.
   ===================================================================== */
(() => {
  "use strict";
  const API = "api/";
  const $ = s => document.querySelector(s);
  let authResolve;
  const authReady = new Promise(r => { authResolve = r; });
  const TG = window.TG = { user: null, cfg: {} };
  const lsDel = (...k) => { try { k.forEach(x => localStorage.removeItem(x)); } catch {} };
  const lsGet = k => { try { return localStorage.getItem(k); } catch { return null; } };
  const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch {} };

  async function api(path, { method = "GET", body, signal } = {}) {
    const r = await fetch(API + path, {
      method, signal, credentials: "same-origin",
      headers: { "X-TG": "1", ...(body !== undefined ? { "Content-Type": "application/json" } : {}) },
      body: body !== undefined ? JSON.stringify(body) : undefined
    });
    let j = null; try { j = await r.json(); } catch {}
    if (!r.ok) { const e = new Error(j?.mensaje || "Error " + r.status); e.status = r.status; e.data = j; throw e; }
    return j;
  }

  /* ---------- Imágenes: reducir a 1568 px y JPEG antes de subir ---------- */
  function blobToB64(blob) {
    return new Promise((res, rej) => { const fr = new FileReader(); fr.onload = () => res(String(fr.result).split(",")[1]); fr.onerror = rej; fr.readAsDataURL(blob); });
  }
  async function prepImage(blob) {
    let src;
    try { src = await createImageBitmap(blob, { imageOrientation: "from-image" }); }
    catch {
      src = await new Promise((res, rej) => { const im = new Image(); im.onload = () => res(im); im.onerror = rej; im.src = URL.createObjectURL(blob); });
    }
    const w = src.width || src.naturalWidth, h = src.height || src.naturalHeight, k = Math.min(1, 1568 / Math.max(w, h));
    const c = document.createElement("canvas"); c.width = Math.round(w * k); c.height = Math.round(h * k);
    const x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, c.width, c.height); x.drawImage(src, 0, 0, c.width, c.height);
    const out = await new Promise(r => c.toBlob(r, "image/jpeg", 0.85));
    return { mediaType: "image/jpeg", data: await blobToB64(out) };
  }

  /* ---------- Errores con los mismos códigos que usa la app ---------- */
  function mapErr(e) {
    if (e?.name === "AbortError") return { code: "cancelled", message: "cancelado" };
    const s = e?.status, msg = e?.data?.mensaje || e?.message || "";
    if (s === 401) { showAuth(); return { code: "session_expired", message: msg }; }
    if (s === 402) { showPay(msg); return { code: "plan", message: msg }; }
    if (s === 429 || s === 503) return { code: "rate_limited", message: msg };
    if (s === 422) return { code: "refused", message: msg };
    if (s === 413) return { code: "prompt_too_large", message: msg };
    if (s === 400 && e?.data?.error === "image_rejected") return { code: "image_rejected", message: msg };
    return { code: "upstream_error", message: msg || "Sin conexión" };
  }

  /* ---------- sample: la IA a través de api/ia.php ---------- */
  async function sample(input, opts = {}) {
    if (opts.signal?.aborted) throw { code: "cancelled", message: "cancelado" };
    let images = [];
    if (opts.images) {
      const list = opts.images instanceof Blob ? [opts.images] : [...opts.images];
      try { images = await Promise.all(list.slice(0, 8).map(prepImage)); } catch { throw { code: "image_rejected", message: "No se pudo leer una imagen." }; }
    }
    try {
      const r = await api("ia.php", { method: "POST", signal: opts.signal, body: { input, images, tier: opts.modelTier || "default", json: !!opts._json } });
      try { opts.onText && opts.onText({ text: r.text, delta: r.text }); } catch {}
      return { text: r.text, truncated: !!r.truncated, modelTierApplied: opts.modelTier || "default" };
    } catch (e) { throw (e && e.code) ? e : mapErr(e); }
  }
  function parseJSON(t) {
    const s = String(t || "").trim();
    try { return JSON.parse(s); } catch {}
    const f = /```(?:json)?\s*([\s\S]*?)```/i.exec(s); if (f) { try { return JSON.parse(f[1]); } catch {} }
    const a = s.search(/[\[{]/), b = Math.max(s.lastIndexOf("}"), s.lastIndexOf("]"));
    if (a >= 0 && b > a) { try { return JSON.parse(s.slice(a, b + 1)); } catch {} }
    return undefined;
  }
  sample.json = async (input, opts = {}) => {
    const r = await sample(input, { ...opts, _json: true });
    const v = parseJSON(r.text);
    if (v === undefined) throw { code: "invalid_json", message: "respuesta sin JSON", text: r.text };
    return v;
  };
  sample.limits = async () => ({ maxPromptBytes: 262144, images: { maxCount: 8, maxInputBytes: 20e6, mediaTypes: ["image/jpeg", "image/png", "image/webp", "image/gif"] } });

  /* ---------- db: visitas del técnico en api/visitas.php ---------- */
  const db = {
    collection(name) {
      if (name !== "visitas") throw new Error("colección no soportada");
      const q = {
        orderBy() { return q; }, limit() { return q; },
        async get() { const list = await api("visitas.php"); return { docs: list.map(v => ({ id: String(v.id), data: () => v })) }; },
        doc(id) {
          return {
            set: d => api("visitas.php", { method: "POST", body: { visita: d } }),
            delete: () => api("visitas.php?id=" + encodeURIComponent(id), { method: "DELETE" })
          };
        }
      };
      return q;
    }
  };
  const user = { isOwner: async () => true, canEdit: async () => true, can: async () => true, id: async () => String(TG.user?.id ?? "") };
  const downloads = {
    async save({ filename, data }) {
      const blob = data instanceof Blob ? data : new Blob([data], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = filename;
      document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
      return { status: "saved" };
    }
  };
  window.claude = { use: async name => { await authReady; return { sample, db, user, downloads }[name] || null; } };

  /* ---------- Pantallas de cuenta ---------- */
  function showAuth() { $("#tg-auth").hidden = false; }
  function showPay(msg) {
    if (msg) $("#tg-pay-msg").textContent = msg;
    $("#tg-pay").hidden = false;
  }
  function applyMode() {
    const c = TG.cfg || {};
    if (c.registro === false) { $("#tg-t-reg").hidden = true; tab(false); }
    if (c.personal) {
      $("#tg-r-acepto").closest("label").hidden = true;
      $("#tg-wa1").closest("p").hidden = true;
      $("#tg-r-tel").closest("label").hidden = true;
      $("#tg-r-go").textContent = "Crear mi cuenta";
      if (c.registro) tab(true);
    }
  }
  function fillCfg() {
    applyMode();
    const wa = TG.cfg.whatsapp || "";
    ["#tg-wa1", "#tg-wa2"].forEach(s => { const el = $(s); if (el) el.textContent = wa; });
    const digits = wa.replace(/[^0-9]/g, "");
    const msg = encodeURIComponent(`Hola, quiero activar mi cuenta de ${TG.cfg.nombre_app || "TecniGuía"}. Mi correo: ${TG.user?.email || ""}`);
    $("#tg-wa-link").href = digits ? `https://wa.me/${digits}?text=${msg}` : "#";
  }
  function planText(u) {
    if (TG.cfg.personal) return "Cuenta personal";
    if (u.admin) return "Administrador";
    if (!u.plan_ok) return u.estado === "suspendido" ? "Cuenta suspendida" : "Plan vencido";
    const d = Math.max(0, u.dias_restantes ?? 0);
    return u.estado === "prueba" ? `Prueba: ${d} día${d === 1 ? "" : "s"}` : `Plan activo: ${d} días`;
  }
  function renderBar() {
    const bar = $("#tg-userbar"); if (!bar) return;
    const u = TG.user;
    bar.hidden = false;
    bar.innerHTML = `<span style="min-width:0;display:flex;flex-direction:column;align-items:flex-end"><b></b><span>${planText(u)}</span></span>${u.admin && !TG.cfg.personal ? '<a href="admin.html" style="font-size:12.5px">Panel</a>' : ""}<button type="button" id="tg-out">Salir</button>`;
    bar.querySelector("b").textContent = u.nombre;
    $("#tg-out").onclick = async () => { try { await api("auth.php?a=salir", { method: "POST", body: {} }); } catch {} lsDel("tg_visits", "tg_draft", "tg_uid"); location.reload(); };
    const old = $("#tg-planbox"); if (old) old.remove();
    if (!u.plan_ok) {
      const box = document.createElement("div"); box.id = "tg-planbox"; box.className = "tg-plan";
      box.innerHTML = `<span>${u.estado === "suspendido" ? "Tu cuenta está suspendida." : "Tu plan venció."} El diagnóstico con IA está pausado.</span><button class="btn" type="button" style="padding:6px 12px">Activar</button>`;
      box.querySelector("button").onclick = () => showPay();
      $("#v-diag")?.prepend(box);
    } else if (u.estado === "prueba" && !u.admin && (u.dias_restantes ?? 9) <= 2) {
      const box = document.createElement("div"); box.id = "tg-planbox"; box.className = "tg-plan";
      box.innerHTML = `<span>Te quedan ${Math.max(0, u.dias_restantes)} día(s) de prueba.</span><button class="btn ghost" type="button" style="padding:6px 12px">Activar plan</button>`;
      box.querySelector("button").onclick = () => showPay("Activa tu plan antes de que termine la prueba.");
      $("#v-diag")?.prepend(box);
    }
  }
  function onLogged(j) {
    TG.user = j.usuario; TG.cfg = j.cfg || TG.cfg;
    // Datos de otro técnico en este teléfono: se borran antes de cargar los del nuevo
    if (lsGet("tg_uid") !== String(TG.user.id)) { lsDel("tg_visits", "tg_draft", "tg_resume"); lsSet("tg_uid", String(TG.user.id)); }
    $("#tg-auth").hidden = true;
    fillCfg(); renderBar();
    if (!TG.user.plan_ok) showPay(TG.user.estado === "suspendido" ? "Tu cuenta está suspendida." : "Tu prueba o tu plan terminó.");
    authResolve();
  }

  function tab(reg) {
    $("#tg-t-login").setAttribute("aria-pressed", String(!reg)); $("#tg-t-reg").setAttribute("aria-pressed", String(reg));
    $("#tg-login").hidden = reg; $("#tg-reg").hidden = !reg;
  }
  $("#tg-t-login").onclick = () => tab(false);
  $("#tg-t-reg").onclick = () => tab(true);
  $("#tg-pay-close").onclick = () => { $("#tg-pay").hidden = true; };

  $("#tg-login").addEventListener("submit", async e => {
    e.preventDefault(); const btn = $("#tg-l-go"), err = $("#tg-l-err"); err.textContent = ""; btn.disabled = true;
    try { onLogged(await api("auth.php?a=login", { method: "POST", body: { email: $("#tg-l-email").value, clave: $("#tg-l-clave").value } })); }
    catch (x) { err.textContent = x.data?.mensaje || "No se pudo entrar. Revisa tu conexión."; }
    finally { btn.disabled = false; }
  });
  $("#tg-reg").addEventListener("submit", async e => {
    e.preventDefault(); const btn = $("#tg-r-go"), err = $("#tg-r-err"); err.textContent = ""; btn.disabled = true;
    try {
      onLogged(await api("auth.php?a=registro", { method: "POST", body: {
        nombre: $("#tg-r-nombre").value, email: $("#tg-r-email").value, telefono: $("#tg-r-tel").value,
        clave: $("#tg-r-clave").value, acepto: $("#tg-r-acepto").checked } }));
    } catch (x) { err.textContent = x.data?.mensaje || "No se pudo crear la cuenta. Revisa tu conexión."; }
    finally { btn.disabled = false; }
  });

  (async () => {
    try { onLogged(await api("auth.php?a=yo")); }
    catch (e) {
      TG.cfg = e.data?.cfg || {}; fillCfg();
      if (e.status === 500 && e.data?.error === "config") { $("#tg-auth").hidden = false; $("#tg-l-err").textContent = e.data.mensaje; return; }
      showAuth();
    }
  })();
})();
