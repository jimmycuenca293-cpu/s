#!/usr/bin/env python3
"""Diseño profesional para un sitio de una ciudad generado con ST_SOLO (Panamá).
Uso: python3 pa_diseno.py <carpeta_del_sitio>
- Reconstruye la portada en 9 secciones ordenadas (hero, datos rápidos, equipos, cómo funciona, zonas, fallas, ciudad, preguntas, contacto).
- Quita la acción bajo cada imagen (los botones de WhatsApp de las tarjetas y los pies de foto) y la cinta de barrios.
- Compacta las páginas interiores (menos espacio en blanco, imágenes con tamaño uniforme)."""
import hashlib, html, pathlib, re, sys
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
/* portada */
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
.pa-steps{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;counter-reset:s;list-style:none;margin:0;padding:0}.pa-steps li{counter-increment:s;background:#fff;border:1px solid #e1e7f3;border-radius:16px;padding:18px;font-size:.92rem;line-height:1.45;color:#2a3a5c}.pa-steps li::before{content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#1428a0;color:#fff;font-weight:800;margin-bottom:10px}
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
        nombre = re.sub(r"\s+en\s+Ciudad de Panamá\s*$", "", txt(x)); k = nombre.split()[0].capitalize()
        k = {"Estufa": "Estufas y hornos", "Horno": "Estufas y hornos"}.get(k, k + "s" if not k.endswith("s") else k)
        if k in ("Refrigeradoras", "Lavadoras", "Secadoras", "Lavavajillas", "Estufas y hornos", "Microondas"):
            grp.setdefault(k, []).append((h, nombre))
    tabs = "".join(f'<button type="button" data-t="{n}" class="{"on" if n == 0 else ""}">{esc(k)}</button>' for n, k in enumerate(grp))
    paneles = "".join(f'<div class="pa-pn {"on" if n == 0 else ""}" data-p="{n}">' + "".join(f'<a href="{h}">{esc(x)}</a>' for h, x in v[:8]) + "</div>" for n, (k, v) in enumerate(grp.items()))
    datos = re.search(r'<table class="spec-table">(.*?)</table>', sec("Datos de"), re.S)
    clima = "".join(f"<p>{txt(p)}</p>" for p in re.findall(r"<p>(.*?)</p>", sec("Ciudad de Panamá: clima"))[:2])
    mapa = re.search(r"<iframe.*?</iframe>", sec("Mapa"), re.S)
    faq = re.search(r'<div class="faq-num">(.*?)</div>', sec("Preguntas frecuentes"), re.S)
    rap = sec("Preguntas rápidas"); pares = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", rap, re.S)
    faq_html = (faq.group(1).replace("<details open>", "<details>") if faq else "") + "".join(f"<details><summary>{txt(q)}</summary><p>{txt(a)}</p></details>" for q, a in pares)
    guias = "".join(f'<a href="{h}">{txt(x)}</a>' for h, x in re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Guías y respuestas") + sec("Artículos del blog")))
    mas = "".join(f'<a href="{h}">{txt(x)}</a>' for h, x in re.findall(r'<a href="([^"]+)">([^<]+)</a>', sec("Más sobre electrodomésticos")) if not h.startswith("http"))
    ciudad = h1.replace("Servicio técnico Samsung en ", "")
    nuevo = (f'<section class="pa-hero"><div class="pa-w pa-hg"><div><span class="pa-kick">Servicio técnico independiente · {esc(ciudad)}</span><h1>{esc(h1)}</h1><p>{esc(sub)}</p>'
             f'<div class="pa-btns"><a class="pa-b wa" href="{wa}" target="_blank" rel="noopener">Escribir por WhatsApp</a><a class="pa-b sol" href="{sol}">Solicitar visita</a></div>'
             '<ul class="pa-ck"><li>Visita a domicilio</li><li>Diagnóstico primero</li><li>Valor confirmado antes de reparar</li></ul></div>'
             f'<figure class="pa-fig"><img src="{himg.group(1)}" alt="{esc(himg.group(2))}" width="1024" height="572" fetchpriority="high" decoding="async"><span class="pa-badge">WhatsApp<small>+{tel[:3]} {tel[3:7]}-{tel[7:]}</small></span></figure></div></section>'
             f'<section class="pa-s" style="padding-top:0"><div class="pa-w"><div class="pa-quick">{"".join(quick)}</div></div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">Equipos Samsung que reparamos en {esc(ciudad)}</h2><p class="pa-sub">Elige tu electrodoméstico y mira las fallas que atendemos, qué revisa el técnico y cómo pedir la visita.</p><div class="pa-eq">{"".join(cards)}</div></div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Cómo funciona</h2><p class="pa-sub">De tu mensaje de WhatsApp a la reparación, en cinco pasos.</p><ol class="pa-steps">{pasos}</ol><div style="height:28px"></div>{incluye}</div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">Zonas y barrios que atendemos</h2><p class="pa-sub">Toca tu barrio para ver el servicio en tu zona.</p><div class="pa-zon">{zon}</div></div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Fallas más consultadas</h2><p class="pa-sub">Elige el equipo y entra a la falla que describe tu problema.</p><div class="pa-tabs" id="pa-tabs">{tabs}</div>{paneles}</div></section>'
             f'<section class="pa-s"><div class="pa-w"><h2 class="pa-h2">{esc(ciudad)} y tus electrodomésticos</h2><div class="pa-two"><div class="pa-card"><h3>Datos que influyen</h3><table>{datos.group(1) if datos else ""}</table></div><div class="pa-card"><h3>Clima y electricidad</h3>{clima}</div></div><div class="pa-map" style="margin-top:20px">{mapa.group(0) if mapa else ""}</div></div></section>'
             f'<section class="pa-s alt"><div class="pa-w"><h2 class="pa-h2">Preguntas frecuentes</h2><div class="pa-faq">{faq_html}</div></div></section>'
             f'<section class="pa-s"><div class="pa-w"><div class="pa-cta"><div><h2>¿Tu Samsung falla? Escríbenos</h2><p>Cuéntanos el equipo, el modelo y la falla: coordinamos la visita en {esc(ciudad)}.</p></div><div class="pa-btns" style="margin:0"><a class="pa-b wa" href="{wa}" target="_blank" rel="noopener">WhatsApp</a><a class="pa-b line" href="tel:+{tel}">Llamar</a></div></div><div style="height:26px"></div><h3 style="margin:0 0 10px;font:800 1rem Inter,sans-serif;color:#0b1f4d">Sigue explorando</h3><div class="pa-links">{guias}{mas}</div></div></section>'
             '<script>(function(){var t=document.getElementById("pa-tabs");if(!t)return;t.addEventListener("click",function(e){var b=e.target.closest("button");if(!b)return;[].forEach.call(t.children,function(x){x.classList.toggle("on",x===b)});[].forEach.call(document.querySelectorAll(".pa-pn"),function(p){p.classList.toggle("on",p.dataset.p===b.dataset.t)})})})();</script>')
    return t[:i] + nuevo + t[j:]
FAMILIAS = [("puerta", r"puerta|saluda|llegando|visita-a-domicilio-\\d"), ("recepcion", r"recepcion|asesora|atencion|orden-de-servicio"), ("rep-nevera", r"reparando-(nevera|refrigeradora)|revisando-(nevera|compresor)|revision-en-casa"), ("rep-lavadora", r"lavadora.*(tecnico|reparando|diagnosticando)|tecnico.*lavadora")]
cont = 0
for f in R.rglob("*.html"):
    t = f.read_text(encoding="utf-8", errors="ignore")
    o = t
    if f == R / "index.html" and '<section class="hero st-split">' in t:
        t = portada(t)
    t = re.sub(r"<figcaption>.*?</figcaption>", "", t, flags=re.S)
    if f != R / "index.html":
        vistas, n_img = set(), [0]
        def _fig(m):
            fig = m.group(0); src = re.search(r'<img[^>]*src="([^"]+)"', fig)
            if not src: return fig
            nombre = src.group(1).rsplit("/", 1)[-1]; base = re.sub(r"-(s|m|400)\.webp$", ".webp", nombre)
            fam = next((k for k, rx in FAMILIAS if re.search(rx, base)), base)
            if fam in vistas or n_img[0] >= 4: return ""
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
