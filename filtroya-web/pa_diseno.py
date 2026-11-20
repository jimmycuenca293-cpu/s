#!/usr/bin/env python3
"""Diseño profesional para un sitio de una ciudad generado con ST_SOLO (Panamá).
Uso: python3 pa_diseno.py <carpeta_del_sitio>
- Reconstruye la portada en 9 secciones ordenadas (hero, datos rápidos, equipos, cómo funciona, zonas, fallas, ciudad, preguntas, contacto).
- Quita la acción bajo cada imagen (los botones de WhatsApp de las tarjetas y los pies de foto) y la cinta de barrios.
- Compacta las páginas interiores (menos espacio en blanco, imágenes con tamaño uniforme)."""
import hashlib, html, pathlib, re, sys
from pa_cfg import CFG
R = pathlib.Path(sys.argv[1])
esc = lambda s: html.escape(s, quote=True)
txt = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
CSS = r"""
/* ===== Panamá Pro: diseño ordenado ===== */
.aq-ticker{display:none!important}
.sec-img figcaption{display:none!important}
.sec-img{max-width:none!important;margin:0 0 16px!important}.sec-img img{display:block;width:100%;height:auto;max-height:340px;object-fit:cover;border-radius:18px;box-shadow:0 8px 26px rgba(11,31,77,.12)}.sec-img.prod img{object-fit:contain;background:#fff;border:1px solid #e6ebf6;padding:14px}
.aq-sec.chap{padding:40px 0!important}.aq-sec.chap .wrap>h2{margin:0 0 16px!important;font-size:1.55rem!important}
@media(min-width:960px){.aq-sec.chap .wrap{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,.75fr);gap:14px 44px;align-items:start}.aq-sec.chap .wrap>h2{grid-column:1/-1}.aq-sec.chap .wrap>.sec-img{width:100%!important;float:none!important;grid-column:2;grid-row:2/span 8;position:sticky;top:96px}.aq-sec.chap .wrap>*:not(h2):not(.sec-img){grid-column:1}.aq-sec.chap.st-equipos .wrap,.aq-sec.chap .wrap:has(>iframe){display:block}}
.aq-qa-sec{padding:14px 0!important}.aq-qa-sec .qa{padding:16px 20px!important}.toc-sec{padding:10px 0!important}
.st-eq-btn{display:none!important}
.st-eq-c{transition:.2s}.st-eq-c:hover{transform:translateY(-3px);box-shadow:0 14px 32px rgba(11,31,77,.14)}
/* interiores en tarjetas de dos columnas */
.pa-grid{max-width:1180px;margin:0 auto;padding:12px 20px 40px;display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:start}
.pa-grid>section.aq-sec{background:#fff!important;border:1px solid #e1e7f3;border-radius:20px;padding:24px!important;box-shadow:0 8px 24px rgba(11,31,77,.06)}
.pa-grid>section.aq-sec .wrap{max-width:none!important;width:auto!important;padding:0!important;display:block!important;margin:0!important}
.pa-grid>section.aq-sec .wrap>h2{font-size:1.25rem!important;margin:0 0 14px!important}
.pa-grid>section.aq-sec .sec-img{position:static!important;width:100%!important;margin:0 0 14px!important}.pa-grid>section.aq-sec .sec-img img{max-height:230px}
.pa-grid>section.pa-full{grid-column:1/-1}
.pa-grid .city-tags{margin:0}
@media(max-width:860px){.pa-grid{grid-template-columns:1fr;padding:8px 16px 32px}.pa-grid>section.aq-sec{padding:18px!important}}
/* contacto fijo, 4 pasos, menú de líneas */
.pa-info{background:#0b1f4d;color:#fff;padding:28px 0}.pa-info .in{max-width:1180px;margin:0 auto;padding:0 20px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.pa-info div.c{display:flex;gap:12px;align-items:flex-start}.pa-info i{font-style:normal;width:42px;height:42px;border-radius:12px;background:rgba(255,255,255,.12);display:grid;place-items:center;font-size:1.2rem;flex:none}.pa-info small{display:block;color:#a9bbe8;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.pa-info b,.pa-info a{color:#fff;font:700 1rem Inter,sans-serif;text-decoration:none}.pa-info a:hover{text-decoration:underline}
.pa-4{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;list-style:none;margin:0;padding:0;counter-reset:q}.pa-4 li{counter-increment:q;background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:18px 18px 18px 64px;position:relative;font-weight:600;color:#14213d;font-size:.95rem;line-height:1.4}.pa-4 li::before{content:counter(q);position:absolute;left:16px;top:16px;width:36px;height:36px;border-radius:50%;background:#16a34a;color:#fff;display:grid;place-items:center;font-weight:800}.pa-4 small{display:block;color:#5b6478;font-weight:500;margin-top:4px}
.aq-pop.lin .aq-chips a{white-space:nowrap}
@media(max-width:900px){.pa-info .in,.pa-4{grid-template-columns:1fr 1fr}}@media(max-width:560px){.pa-info .in,.pa-4{grid-template-columns:1fr}}
/* artículos, blog y legales */
.pa-hero-s{padding:38px 0 44px}.pa-hero-s h1{font-size:clamp(1.7rem,3.4vw,2.5rem)!important}.pa-hero-s p{margin:0 0 6px}.pa-meta{font-size:.9rem!important;color:#bcd0ff!important;margin-top:12px!important}
.pa-art{padding:34px 0 24px;background:#f4f7fc}.pa-cols{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:34px;align-items:start}
.pa-prose{background:#fff;border:1px solid #e1e7f3;border-radius:20px;padding:34px 38px;color:#2a3a5c;line-height:1.7;font-size:1.02rem}.pa-prose h2{font:800 1.45rem/1.25 Inter,sans-serif;color:#0b1f4d;margin:34px 0 12px}.pa-prose h2:first-of-type{margin-top:8px}.pa-prose p{margin:0 0 14px}.pa-prose ul,.pa-prose ol{margin:0 0 16px;padding-left:22px}.pa-prose li{margin:0 0 8px}.pa-prose a{color:#1428a0;text-decoration:underline}
.pa-lead{font-size:1.15rem!important;color:#0b1f4d;font-weight:500;line-height:1.6}.pa-toc{background:#f4f7fc;border:1px solid #e1e7f3;border-radius:14px;padding:16px 20px;margin:0 0 22px}.pa-toc b{display:block;margin-bottom:8px;color:#0b1f4d}.pa-toc ol{margin:0!important;padding-left:20px!important}.pa-toc li{margin:0 0 4px!important}.pa-toc a{text-decoration:none!important}
.pa-aside{position:sticky;top:96px;display:grid;gap:16px}.pa-aside .pa-card{background:#fff;border:1px solid #e1e7f3;border-radius:18px;padding:20px}.pa-aside .pa-card h3{margin:0 0 8px;font:800 1.05rem Inter,sans-serif;color:#0b1f4d}.pa-aside .pa-card p{color:#3d4b6b;font-size:.92rem;margin:0 0 12px}
.pa-rc{display:block;border-top:1px solid #eef1f8;padding:12px 0;text-decoration:none}.pa-rc:first-of-type{border-top:0}.pa-rc b{display:block;color:#0b1f4d;font-size:.95rem;line-height:1.35;margin:4px 0}.pa-rc small{color:#5b6478}.pa-cat{display:inline-block;background:#e8eeff;color:#1428a0;border-radius:999px;padding:3px 10px;font:700 .72rem Inter,sans-serif;text-transform:uppercase;letter-spacing:.04em}
.pa-cta2{background:linear-gradient(135deg,#0b1f4d,#1428a0);color:#fff;border-radius:18px;padding:26px;margin-top:30px}.pa-cta2 h3{margin:0 0 6px;font:800 1.25rem Inter,sans-serif;color:#fff}.pa-cta2 p{color:#d6e0ff!important;margin:0 0 14px!important}
.pa-bg{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.pa-bc{display:flex;flex-direction:column;gap:8px;background:#fff;border:1px solid #e1e7f3;border-radius:18px;padding:20px;text-decoration:none;color:#14213d;transition:.2s}.pa-bc:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(11,31,77,.12)}.pa-bc b{font:800 1.05rem/1.3 Inter,sans-serif;color:#0b1f4d}.pa-bc p{margin:0;color:#4a5878;font-size:.9rem;line-height:1.5}.pa-bc small{margin-top:auto;color:#5b6478}
@media(max-width:960px){.pa-cols{grid-template-columns:1fr}.pa-aside{position:static}.pa-bg{grid-template-columns:1fr 1fr}.pa-prose{padding:24px}}@media(max-width:600px){.pa-bg{grid-template-columns:1fr}}
/* portada */
.pa-sd{display:grid;grid-template-columns:1.15fr .85fr;gap:36px;align-items:center}.pa-sd figure{margin:0}.pa-sd img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:20px;box-shadow:0 14px 36px rgba(11,31,77,.16)}@media(max-width:860px){.pa-sd{grid-template-columns:1fr}.pa-sd figure{order:-1}}
.pa-ph{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:26px 0}.pa-ph img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px;box-shadow:0 8px 22px rgba(11,31,77,.12)}@media(max-width:700px){.pa-ph{grid-template-columns:1fr 1fr}}
.pa-w{max-width:1180px;margin:0 auto;padding:0 20px}.pa-s{padding:56px 0}.pa-s.alt{background:#f4f7fc}.pa-h2{font:800 1.9rem/1.2 Inter,sans-serif;color:#0b1f4d;margin:0 0 8px;letter-spacing:-.02em}.pa-sub{color:#5b6478;margin:0 0 28px;max-width:70ch}
.pa-hero{background:linear-gradient(135deg,#0b1f4d 0%,#1428a0 100%);color:#fff;padding:54px 0 64px}.pa-hg{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center}.pa-hero h1{color:#fff!important;font:800 clamp(2rem,4.2vw,3.1rem)/1.1 Inter,sans-serif;margin:0 0 16px;letter-spacing:-.02em}.pa-hero p{color:#d6e0ff;font-size:1.1rem;line-height:1.55;margin:0 0 24px;max-width:56ch}
.pa-kick{display:inline-block;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 14px;font:700 .78rem Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;margin-bottom:16px}
.pa-btns{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:22px}.pa-b{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:52px;padding:0 24px;border-radius:14px;font:800 1rem Inter,sans-serif;text-decoration:none}.pa-b.wa{background:#16a34a;color:#fff}.pa-b.sol{background:#fff;color:#0b1f4d}.pa-b.line{background:transparent;color:#fff;border:2px solid rgba(255,255,255,.55)}
.pa-ck{display:flex;flex-wrap:wrap;gap:8px 22px;list-style:none;margin:0;padding:0;color:#e6eeff;font-weight:600;font-size:.95rem}.pa-ck li::before{content:"✓";color:#4ade80;font-weight:800;margin-right:8px}
.pa-fig{position:relative;margin:0}.pa-fig img{display:block;width:100%;height:auto;border-radius:22px;box-shadow:0 24px 60px rgba(0,0,0,.35)}.pa-badge{position:absolute;left:-14px;bottom:-16px;background:#fff;color:#0b1f4d;border-radius:14px;padding:12px 16px;box-shadow:0 14px 34px rgba(0,0,0,.25);font:700 .92rem Inter,sans-serif}.pa-badge small{display:block;font-weight:500;color:#5b6478}
.pa-quick{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:-34px;position:relative;z-index:2}.pa-q{background:#fff;border:1px solid #e1e7f3;border-radius:18px;padding:20px;box-shadow:0 12px 30px rgba(11,31,77,.1)}.pa-q h3{margin:0 0 8px;font:800 1rem/1.3 Inter,sans-serif;color:#0b1f4d}.pa-q p{margin:0;color:#3d4b6b;font-size:.94rem;line-height:1.5}
.pa-trust{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:0;padding:0;list-style:none}.pa-trust li{display:flex;gap:12px;align-items:center;font-weight:700;color:#0b1f4d;font-size:.95rem}.pa-trust i{width:44px;height:44px;border-radius:12px;background:#e8eeff;display:grid;place-items:center;font-style:normal;font-size:1.3rem;flex:none}
.pa-eq{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.pa-c{display:flex;flex-direction:column;background:#fff;border:1px solid #e1e7f3;border-radius:20px;overflow:hidden;text-decoration:none;color:#14213d;transition:.2s}.pa-c:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(11,31,77,.14)}.pa-c .im{background:#fff;border-bottom:1px solid #eef1f8;aspect-ratio:4/3;display:grid;place-items:center}.pa-c img{width:72%;height:88%;object-fit:contain}.pa-c .bd{padding:18px 20px 20px}.pa-c h3{margin:0 0 6px;font:800 1.15rem Inter,sans-serif;color:#0b1f4d}.pa-c .ln{color:#5b6478;font-size:.88rem;line-height:1.4;margin:0 0 12px}.pa-c .go{margin-top:auto;font-weight:800;color:#1428a0;font-size:.92rem}
.pa-tags{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 12px;padding:0;list-style:none}.pa-tags li{background:#eef2ff;color:#1428a0;border-radius:999px;padding:4px 10px;font:600 .76rem Inter,sans-serif}
.pa-steps.pa-v{grid-template-columns:1fr!important}.pa-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;counter-reset:s;list-style:none;margin:0;padding:0}.pa-steps li{counter-increment:s;background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:18px;font-size:.92rem;line-height:1.45;color:#2a3a5c}.pa-steps li::before{content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#1428a0;color:#fff;font-weight:800;margin-bottom:10px}
.pa-two{display:grid;grid-template-columns:1fr 1fr;gap:20px}.pa-card{background:#fff;border:1px solid #e1e7f3;border-radius:18px;padding:22px}.pa-card h3{margin:0 0 12px;font:800 1.05rem Inter,sans-serif;color:#0b1f4d}.pa-card ul{margin:0;padding-left:18px;color:#2a3a5c;line-height:1.55}.pa-card li{margin:0 0 6px}.pa-card table{width:100%;border-collapse:collapse;font-size:.92rem}.pa-card td{padding:8px 0;border-bottom:1px solid #eef1f8;vertical-align:top}.pa-card td:first-child{color:#5b6478;width:42%}
.pa-zon{display:flex;flex-wrap:wrap;gap:8px}.pa-zon a{background:#fff;border:1.5px solid #dbe3f4;border-radius:999px;padding:8px 14px;font:600 .88rem Inter,sans-serif;color:#0b1f4d;text-decoration:none}.pa-zon a:hover{border-color:#1428a0;color:#1428a0}
.pa-tabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}.pa-tabs button{border:1.5px solid #cfd8ee;background:#fff;border-radius:999px;padding:9px 16px;font:700 .92rem Inter,sans-serif;color:#0b1f4d;cursor:pointer}.pa-tabs button.on{background:#1428a0;border-color:#1428a0;color:#fff}.pa-pn{display:none;grid-template-columns:repeat(2,1fr);gap:10px}.pa-pn.on{display:grid}.pa-pn a{background:#fff;border:1px solid #e1e7f3;border-radius:12px;padding:14px 16px;font-weight:600;color:#14213d;text-decoration:none}.pa-pn a:hover{border-color:#1428a0;color:#1428a0}
.pa-faq details{background:#fff;border:1px solid #e1e7f3;border-radius:14px;margin:0 0 10px}.pa-faq summary{cursor:pointer;padding:16px 20px;font-weight:700;color:#0b1f4d}.pa-faq details p{margin:0;padding:0 20px 16px;color:#3d4b6b;line-height:1.6}
.pa-cta{background:linear-gradient(135deg,#0b1f4d,#1428a0);color:#fff;border-radius:24px;padding:36px;display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between}.pa-cta h2{margin:0 0 6px;font:800 1.6rem Inter,sans-serif}.pa-cta p{margin:0;color:#d6e0ff}
.pa-map iframe{width:100%;height:300px;border:0;border-radius:18px}
.pa-links{display:flex;flex-wrap:wrap;gap:8px}.pa-links a{background:#fff;border:1px solid #dbe3f4;border-radius:10px;padding:8px 12px;font:600 .86rem Inter,sans-serif;color:#1428a0;text-decoration:none}
@media(max-width:900px){.pa-hg,.pa-two{grid-template-columns:1fr}.pa-quick,.pa-eq{grid-template-columns:1fr 1fr}.pa-trust{grid-template-columns:1fr 1fr}.pa-steps{grid-template-columns:1fr 1fr}.pa-pn{grid-template-columns:1fr}.pa-badge{left:10px}.pa-s{padding:40px 0}}
@media(max-width:760px){.aq-brand img,.aq-brand .st-logo{max-height:30px;width:auto}.aq-bar{flex-wrap:nowrap;justify-content:center;gap:12px;font-size:.78rem}.pa-kick{font-size:.68rem;letter-spacing:.04em}}
@media(max-width:560px){.pa-quick,.pa-eq,.pa-trust,.pa-steps{grid-template-columns:1fr}.pa-quick{margin-top:-22px}.pa-hero{padding:30px 0 44px}.pa-b{width:100%}.pa-h2{font-size:1.5rem}.pa-cta{padding:26px}}
"""
# 1) CSS al final de tema.css
tema = R / "tema.css"
base = tema.read_text(encoding="utf-8")
if "Panamá Pro" not in base: tema.write_text(base + CSS, encoding="utf-8")
ver = hashlib.md5(tema.read_bytes()).hexdigest()[:8]
# 2) portada nueva
def portada(t):
    i = t.find('<section class="hero'); j = t.find("<footer")
    b = t[i:j]
    secs = re.findall(r"<section.*?</section>", b, re.S)
    sec = lambda titulo_ini: next((s for s in secs if re.search(r"<h2[^>]*>" + re.escape(titulo_ini), s)), "")
    h1 = txt(re.search(r"<h1[^>]*>(.*?)</h1>", secs[0], re.S).group(1))
    sub = txt(re.search(r'<p class="sub"[^>]*>(.*?)</p>', secs[0], re.S).group(1))
    wa = re.search(r'href="(https://wa\.me/[^"]+)"', secs[0]).group(1)
    sol = re.search(r'class="st-btn sol" href="([^"]+)"', secs[0]).group(1)
    himg = re.search(r'<img src="([^"]+)" alt="([^"]*)"', secs[0])
    tel = re.search(r"wa\.me/(\d+)", wa).group(1)
    quick = []
    for s in secs[1:4]:
        h = re.search(r"<h2[^>]*>(.*?)</h2>", s, re.S); p = next((m for m in re.finditer(r"<p[^>]*>(.*?)</p>", s, re.S) if len(txt(m.group(1))) > 45 and "Respuesta rápida" not in m.group(1)), None)
        if h and p: quick.append(f'<div class="pa-q"><h3>{txt(h.group(1))}</h3><p>{txt(p.group(1))}</p></div>')
    cards = []
    for a in re.findall(r'<article class="st-eq-c">(.*?)</article>', sec("Todos los electrodomésticos"), re.S):
        href = re.search(r'<a class="st-foto" href="([^"]+)"', a).group(1); im = re.search(r'<img class="st-fimg" src="([^"]+)" alt="([^"]*)"', a)
        h3 = txt(re.search(r"<h3>(.*?)</h3>", a).group(1)); ln = txt(re.search(r'<p class="st-eq-lin">(.*?)</p>', a).group(1))
        chips = "".join(f"<li>{txt(c)}</li>" for c in re.findall(r"<li>(.*?)</li>", a)[:3])
        cards.append(f'<a class="pa-c" href="{href}"><div class="im"><img src="{im.group(1)}" alt="{esc(im.group(2))}" loading="lazy" decoding="async"></div><div class="bd"><h3>{h3}</h3><p class="ln">{ln}</p><ul class="pa-tags">{chips}</ul><span class="go">Ver servicio →</span></div></a>')
    pasos = "".join(f"<li>{txt(x)}</li>" for x in re.findall(r"<li>(.*?)</li>", sec("Cómo funciona")))
    inc = sec("Qué incluye"); tds = re.findall(r"<td>(.*?)</td>", inc, re.S)
    lista = lambda td: "".join(f"<li>{txt(x)}</li>" for x in re.split(r"<br>", td) if txt(x)).replace("• ", "")
    incluye = f'<div class="pa-two"><div class="pa-card"><h3>La visita incluye</h3><ul>{lista(tds[0])}</ul></div><div class="pa-card"><h3>Importante saber</h3><ul>{lista(tds[1])}</ul></div></div>' if len(tds) >= 2 else ""
    zon = "".join(f'<a href="{h}">{txt(x)}</a>' for h, x in re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Servicio técnico por barrio")) if "/" in h and "ver todos" not in x.lower() and not txt(x).lower().startswith(("clima", "guía", "mapa")))[:20000]
    fall = re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Fallas frecuentes"))
    grp = {}
    for h, x in fall:
        nombre = re.sub(r"\s+en\s+" + re.escape(CFG["ciudad"]) + r"\s*$", "", txt(x)); k = nombre.split()[0].capitalize()
        k = CFG["eq_nombre_falla"].get(k, k + "s" if not k.endswith("s") else k)
        if k in CFG["eq_clave"]:
            grp.setdefault(k, []).append((h, nombre))
    tabs = "".join(f'<button type="button" data-t="{n}" class="{"on" if n == 0 else ""}">{esc(k)}</button>' for n, k in enumerate(grp))
    paneles = "".join(f'<div class="pa-pn {"on" if n == 0 else ""}" data-p="{n}">' + "".join(f'<a href="{h}">{esc(x)}</a>' for h, x in v[:8]) + "</div>" for n, (k, v) in enumerate(grp.items()))
    datos = re.search(r'<table class="spec-table">(.*?)</table>', sec("Datos de"), re.S)
    clima = "".join(f"<p>{txt(p)}</p>" for p in re.findall(r"<p>(.*?)</p>", sec(CFG["ciudad"] + ": clima"))[:2])
    mapa = re.search(r"<iframe.*?</iframe>", sec("Mapa"), re.S)
    faq = re.search(r'<div class="faq-num">(.*?)</div>', sec("Preguntas frecuentes"), re.S)
    rap = sec("Preguntas rápidas"); pares = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", rap, re.S)
    faq_html = (faq.group(1).replace("<details open>", "<details>") if faq else "") + "".join(f"<details><summary>{txt(q)}</summary><p>{txt(a)}</p></details>" for q, a in pares)
    guias = "".join(f'<a href="{h}">{txt(x)}</a>' for h, x in re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Guías y respuestas") + sec("Artículos del blog")))
    guias += "".join(f'<a href="{h}">{esc(n)}</a>' for h, n in CFG["extras_links"])
    mas = "".join(f'<a href="{h}">{txt(x)}</a>' for h, x in re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Más sobre electrodomésticos")) if not h.startswith("http"))
    fotos = "".join(f'<img src="img/{n}" alt="{esc(a)}" loading="lazy" decoding="async">' for n, a in NUEVAS if (R / "img" / n).exists())
    def lado(i, cuerpo):
        n, a = NUEVAS[i % len(NUEVAS)]
        return f'<div class="pa-sd"><div>{cuerpo}</div><figure><img src="img/{n}" alt="{esc(a)}" loading="lazy" decoding="async"></figure></div>'
    ciudad = h1.replace("Servicio técnico Samsung en ", "")
    nuevo = (f'<section class="pa-hero"><div class="pa-w pa-hg"><div><span class="pa-kick">Servicio técnico independiente · {esc(ciudad)}</span><h1>{esc(h1)}</h1><p>{esc(sub)}</p>'
             f'<div class="pa-btns"><a class="pa-b wa" href="{wa}" target="_blank" rel="noopener">Escribir por WhatsApp</a><a class="pa-b sol" href="{sol}">Solicitar visita</a></div>'
             '<ul class="pa-ck"><li>Visita a domicilio</li><li>Diagnóstico primero</li><li>Valor confirmado antes de reparar</li></ul></div>'
             f'<figure class="pa-fig"><img src="{himg.group(1)}" alt="{esc(himg.group(2))}" width="1024" height="572" fetchpriority="high" decoding="async"><span class="pa-badge">WhatsApp<small>{CFG["tel"]}</small></span></figure></div></section>'
             f'<section class="pa-s" style="padding-top:0"><div class="pa-w"><div class="pa-quick">{"".join(quick)}</div><h2 class="pa-h2" style="margin-top:34px">Pide tu visita en 4 pasos</h2><p class="pa-sub" style="margin-bottom:16px">Sin vueltas: de tu mensaje a la reparación.</p>' + PASOS4 + '</div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">Equipos Samsung que reparamos en {esc(ciudad)}</h2><p class="pa-sub">Elige tu electrodoméstico y mira las fallas que atendemos, qué revisa el técnico y cómo pedir la visita.</p><div class="pa-eq">{"".join(cards)}</div></div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Cómo funciona</h2><p class="pa-sub">De tu mensaje de WhatsApp a la reparación, en cinco pasos.</p>{lado(0, '<ol class="pa-steps pa-v">' + pasos + '</ol>')}<div style="height:26px"></div>{lado(2, incluye)}</div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">Zonas y barrios que atendemos</h2><p class="pa-sub">Toca tu barrio para ver el servicio en tu zona.</p>{lado(1, '<div class="pa-zon">' + zon + '</div>')}</div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Fallas más consultadas</h2><p class="pa-sub">Elige el equipo y entra a la falla que describe tu problema.</p><div class="pa-tabs" id="pa-tabs">{tabs}</div>{paneles}</div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">{esc(ciudad)} y tus electrodomésticos</h2><div class="pa-two"><div class="pa-card"><h3>Datos que influyen</h3><table>{datos.group(1) if datos else ""}</table></div><div class="pa-card"><h3>Clima y electricidad</h3>{clima}</div></div><div class="pa-map" style="margin-top:20px">{mapa.group(0) if mapa else ""}</div></div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Preguntas frecuentes</h2>{lado(3, '<div class="pa-faq">' + faq_html + '</div>')}</div></section>'
             f'<section class="pa-s"><div class="pa-w"><div class="pa-cta"><div><h2>¿Tu Samsung falla? Escríbenos</h2><p>Cuéntanos el equipo, el modelo y la falla: coordinamos la visita en {esc(ciudad)}.</p></div><div class="pa-btns" style="margin:0"><a class="pa-b wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a><a class="pa-b line" href="tel:+{tel}">Llamar</a></div></div><div style="height:26px"></div><h3 style="margin:0 0 10px;font:800 1rem Inter,sans-serif;color:#0b1f4d">Sigue explorando</h3><div class="pa-links">{guias}{mas}</div></div></section>'
             '<script>(function(){var t=document.getElementById("pa-tabs");if(!t)return;t.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;[].forEach.call(t.children,function(x){x.classList.toggle("on",x===b)});[].forEach.call(document.querySelectorAll(".pa-pn"),function(p){p.classList.toggle("on",p.dataset.p===b.dataset.t)})})})();</script>')
    return t[:i] + nuevo + t[j:]
NUEVAS = [("tecnico-explicando-diagnostico-con-tablet.webp", "Técnico explicando el diagnóstico a un cliente con una tablet en su sala"),
           ("asesora-atendiendo-cliente-en-mostrador.webp", "Asesora atendiendo a un cliente en el mostrador de servicio"),
           ("tecnico-saluda-al-cliente-en-su-casa.webp", "Técnico saludando a un cliente en la puerta de su casa antes de la visita"),
           ("equipo-de-tecnicos-en-taller.webp", "Equipo de técnicos reunido en el taller de reparación")]
_dir_nuevas = pathlib.Path(__file__).resolve().parent / "st_img" / "panama"
for _n, _a in NUEVAS:
    if (_dir_nuevas / _n).exists():
        (R / "img").mkdir(exist_ok=True); (R / "img" / _n).write_bytes((_dir_nuevas / _n).read_bytes())
FAMILIAS = [("puerta", r"puerta|saluda|llegando|visita-a-domicilio-\\d"), ("recepcion", r"recepcion|asesora|atencion|orden-de-servicio"), ("rep-nevera", r"reparando-(nevera|refrigeradora)|revisando-(nevera|compresor)|revision-en-casa"), ("rep-lavadora", r"lavadora.*(tecnico|reparando|diagnosticando)|tecnico.*lavadora")]
DIR = CFG["dir"]
TELV, WAN = CFG["tel"], CFG["wa"]
LINEAS = [("bespoke-samsung", "Bespoke"), ("family-hub-samsung", "Family Hub"), ("ecobubble-samsung", "EcoBubble"), ("addwash-samsung", "AddWash")]
EQUIPOS = [(v, k) for k, v in CFG["eq_slug"].items()]
MAPA = "https://www.google.com/maps?q=" + __import__("urllib.parse").parse.quote_plus(CFG["nombre"] + ", " + DIR) + "&amp;output=embed"
def pref(f):
    return "../" * (len(f.relative_to(R).parts) - 1)
def menu_lineas(p):
    ln = "".join(f'<a href="{p}{u}/">{n}</a>' for u, n in LINEAS if (R / u).exists())
    eq = "".join(f'<a href="{p}{u}/">{n}</a>' for u, n in EQUIPOS if (R / u).exists())
    return (f'<details class="aq-dd"><summary>Líneas Samsung</summary><div class="aq-pop lin"><div class="aq-wrap"><div><h5>Por línea</h5><div class="aq-chips">{ln}</div></div><div><h5>Por equipo</h5><div class="aq-chips">{eq}</div></div></div></div></details>')
def franja(p):
    return ('<section class="pa-info" aria-label="Datos de contacto"><div class="in">'
            f'<div class="c"><i>🕒</i><div><small>Horario</small><b>Abierto las 24 horas</b></div></div>'
            f'<div class="c"><i>📞</i><div><small>Teléfono</small><a href="tel:{TELV.replace(" ", "").replace("-", "")}">{TELV}</a></div></div>'
            f'<div class="c"><i>💬</i><div><small>WhatsApp</small><a href="https://wa.me/{WAN}?text=Hola%2C%20necesito%20servicio%20t%C3%A9cnico%20Samsung" target="_blank" rel="noopener">{TELV}</a></div></div>'
            f'<div class="c"><i>📍</i><div><small>Dirección</small><a href="{p}ubicacion-y-horario/"><b>{DIR}</b></a></div></div></div></section>')
PASOS4 = ('<ol class="pa-4"><li>Escríbenos por WhatsApp<small>Equipo, modelo y falla.</small></li><li>Coordinamos la visita<small>Día y franja en tu barrio.</small></li><li>Diagnóstico en tu casa<small>Te confirmamos el valor antes de reparar.</small></li><li>Reparación y prueba<small>Solo si tú lo apruebas.</small></li></ol>')
def fix_title(t):
    t = html.unescape(t).strip()
    t = re.sub(r" en Ciudad(?: de)?$", "", t) if CFG["ciudad"].startswith("Ciudad") else t                                        # sufijo cortado
    m = re.search(r" en (?:" + re.escape(CFG["ciudad"]) + "|" + re.escape(CFG["corto"]) + r")$", t)
    if m and CFG["corto"] in t[:m.start()]: t = t[:m.start()]
    if len(t) > 66: t = t.replace(CFG["ciudad"], CFG["corto"])
    if len(t) > 66: t = t[:66].rsplit(" ", 1)[0].rstrip(" ,:;·|-")
    return t
cont = 0
for f in R.rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    o = t
    if f == R / "index.html" and '<section class="hero st-split">' in t:
        t = portada(t)
    t = re.sub(r"<figcaption>.*?</figcaption>", "", t, flags=re.S)
    p_ = pref(f)
    t = re.sub(r'(<li><a href=")((?:\.\./)*)(quienes-somos/">Quiénes somos</a></li>)', lambda m: m.group(0) + f'<li><a href="{m.group(2)}politica-de-privacidad/">Política de privacidad</a></li><li><a href="{m.group(2)}terminos-y-condiciones/">Términos y condiciones</a></li>' if "politica-de-privacidad" not in t else m.group(0), t, count=1)
    t = re.sub(r"<title>(.*?)</title>", lambda m: "<title>" + html.escape(fix_title(m.group(1)), quote=False) + "</title>", t, count=1, flags=re.S)
    t = re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content=")([^"]*)(")', lambda m: m.group(1) + html.escape(fix_title(m.group(2))) + m.group(3), t)
    if "pa-info" not in t and "<footer" in t:
        t = t.replace("<footer", franja(p_) + "<footer", 1)
    if "Líneas Samsung" not in t and "</summary>" in t and 'class="aq-dd"><summary>Servicios' in t:
        t = re.sub(r'(<details class="aq-dd"><summary>Servicios</summary>.*?</details>)', lambda m: m.group(1) + menu_lineas(p_), t, count=1, flags=re.S)
    t = re.sub(r'(<iframe[^>]*src=")https://www\.google\.com/maps\?q=[^"]+(")', lambda m: m.group(1) + MAPA + m.group(2), t)
    t = re.sub(r'title="Mapa de [^"]*"', 'title="Mapa: ' + CFG["nombre"] + ', ' + DIR + '"', t)
    if f != R / "index.html":
        vistas, n_img = set(), [0]
        def _fig(m):
            fig = m.group(0); src = re.search(r'<img[^>]*src="([^"]+)"', fig)
            if not src: return fig
            nombre = src.group(1).rsplit("/", 1)[-1]; base = re.sub(r"-(s|m|400)\.webp$", ".webp", nombre)
            fam = next((k for k, rx in FAMILIAS if re.search(rx, base)), base)
            if fam in vistas or n_img[0] >= 4:
                if n_img[0] < 4:
                    for nn, aa in sorted(NUEVAS, key=lambda x: hashlib.md5((str(f) + x[0]).encode()).hexdigest()):
                        if nn not in vistas and (R / "img" / nn).exists():
                            vistas.add(nn); n_img[0] += 1
                            fig = re.sub(r'(<img[^>]*src=")[^"]+(")', lambda q: q.group(1) + ("../" * (len(f.relative_to(R).parts) - 1)) + "img/" + nn + q.group(2), fig, count=1)
                            return re.sub(r'(<img[^>]*alt=")[^"]*(")', lambda q: q.group(1) + esc(aa) + q.group(2), fig, count=1)
                return ""
            vistas.add(fam); n_img[0] += 1; return fig
        t = re.sub(r"<figure class=\"sec-img[^>]*>.*?</figure>", _fig, t, flags=re.S)
    if f != R / "index.html" and "pa-grid" not in t:
        a = t.find('<section class="aq-sec chap'); z = t.find("<footer")
        if a > 0 and z > a:
            bloque = t[a:z]
            bloque = re.sub(r'<section class="aq-sec chap( alt)?([^"]*)"', lambda m: '<section class="aq-sec chap' + (m.group(2) or "") + ('" ' if False else "") + ('' ) + ('"' if True else ""), bloque)
            def _full(m):
                sec = m.group(0)
                grande = any(k in sec for k in ("faq-num", "tbl-wrap", "<iframe", "city-tags", "st-eq", "spec-table")) or len(re.sub(r"<[^>]+>", "", sec)) > 1600
                return sec.replace('<section class="aq-sec chap', '<section class="aq-sec chap pa-full' if grande else '<section class="aq-sec chap', 1)
            bloque = re.sub(r"<section class=\"aq-sec chap.*?</section>", _full, bloque, flags=re.S)
            t = t[:a] + '<div class="pa-grid">' + bloque + "</div>" + t[z:]
    t = re.sub(r'<div class="st-eq-btn">.*?</div>', "", t, flags=re.S) if '<div class="st-eq-btn">' in t else t
    t = re.sub(r"tema\.css\?v=[0-9a-f]+", f"tema.css?v={ver}", t)
    if t != o: f.write_text(t, encoding="utf-8"); cont += 1
print("páginas modificadas:", cont)
