/* =====================================================================
   TecniGuía personal sencilla — sin cuenta ni base de datos.
   La IA pasa por api/ia.php (con tu clave). El historial queda en este
   teléfono. Si no hay clave, la app funciona sin la parte de IA.
   ===================================================================== */
(() => {
  "use strict";
  const lsGet = k => { try { return localStorage.getItem(k) || ""; } catch { return ""; } };
  const lsSet = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
  let estado = null;
  const listo = (async () => {
    try { const r = await fetch("api/ia.php", { cache: "no-store" }); estado = r.ok ? await r.json() : { ia: false }; }
    catch { estado = { ia: false }; }
    if (estado.ia && estado.codigo && !lsGet("tg_codigo")) await pedirCodigo();
  })();

  function pedirCodigo(msg) {
    return new Promise(res => {
      const ov = document.createElement("div");
      ov.style.cssText = "position:fixed;inset:0;z-index:60;background:var(--bg);display:grid;place-items:center;padding:16px";
      ov.innerHTML = `<form style="max-width:340px;width:100%;display:flex;flex-direction:column;gap:12px" class="panel">
        <b style="font-size:18px">Código de acceso</b>
        <span class="sync" style="margin:0">${msg || "Escribe tu código. Solo se pide una vez en este teléfono."}</span>
        <input type="password" inputmode="numeric" autocomplete="off" style="font-size:18px;padding:10px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink)">
        <button class="btn" type="submit">Entrar</button></form>`;
      document.body.append(ov);
      const inp = ov.querySelector("input"); setTimeout(() => inp.focus(), 50);
      ov.querySelector("form").onsubmit = e => { e.preventDefault(); lsSet("tg_codigo", inp.value.trim()); ov.remove(); res(); };
    });
  }

  function b64(blob) { return new Promise((r, j) => { const f = new FileReader(); f.onload = () => r(String(f.result).split(",")[1]); f.onerror = j; f.readAsDataURL(blob); }); }
  async function prepImage(blob) {
    let src;
    try { src = await createImageBitmap(blob, { imageOrientation: "from-image" }); }
    catch { src = await new Promise((r, j) => { const im = new Image(); im.onload = () => r(im); im.onerror = j; im.src = URL.createObjectURL(blob); }); }
    const w = src.width || src.naturalWidth, h = src.height || src.naturalHeight, k = Math.min(1, 1568 / Math.max(w, h));
    const c = document.createElement("canvas"); c.width = Math.round(w * k); c.height = Math.round(h * k);
    const x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, c.width, c.height); x.drawImage(src, 0, 0, c.width, c.height);
    return { mediaType: "image/jpeg", data: await b64(await new Promise(r => c.toBlob(r, "image/jpeg", 0.85))) };
  }
  function mapErr(status, j, e) {
    if (e?.name === "AbortError") return { code: "cancelled", message: "cancelado" };
    const msg = j?.mensaje || "Sin conexión";
    if (status === 401 && j?.error === "codigo") { lsSet("tg_codigo", ""); pedirCodigo("El código no es correcto. Escríbelo otra vez y repite la consulta."); return { code: "codigo", message: msg }; }
    if (status === 429 || (status === 503 && j?.error === "rate_limited")) return { code: "rate_limited", message: msg };
    if (status === 422) return { code: "refused", message: msg };
    if (status === 413) return { code: "prompt_too_large", message: msg };
    if (status === 400 && j?.error === "image_rejected") return { code: "image_rejected", message: msg };
    return { code: "upstream_error", message: msg };
  }
  async function sample(input, opts = {}) {
    if (opts.signal?.aborted) throw { code: "cancelled", message: "cancelado" };
    let images = [];
    if (opts.images) {
      const list = opts.images instanceof Blob ? [opts.images] : [...opts.images];
      try { images = await Promise.all(list.slice(0, 8).map(prepImage)); } catch { throw { code: "image_rejected", message: "No se pudo leer una imagen." }; }
    }
    let r, j = null;
    try {
      r = await fetch("api/ia.php", { method: "POST", signal: opts.signal, headers: { "X-TG": "1", "X-Codigo": lsGet("tg_codigo"), "Content-Type": "application/json" },
        body: JSON.stringify({ input, images, tier: opts.modelTier || "default", json: !!opts._json }) });
      try { j = await r.json(); } catch {}
    } catch (e) { throw mapErr(0, null, e); }
    if (!r.ok) throw mapErr(r.status, j);
    try { opts.onText && opts.onText({ text: j.text, delta: j.text }); } catch {}
    return { text: j.text, truncated: !!j.truncated, modelTierApplied: opts.modelTier || "default" };
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

  const downloads = {
    async save({ filename, data }) {
      const blob = data instanceof Blob ? data : new Blob([data], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = filename;
      document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
      return { status: "saved" };
    }
  };
  // db y user quedan en null: la app guarda el historial en este teléfono.
  window.claude = { use: async name => { await listo; if (name === "sample") return estado?.ia ? sample : null; if (name === "downloads") return downloads; return null; } };
})();
