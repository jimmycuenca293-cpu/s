# Base visual y funciones de página del proyecto de servicio técnico (se ejecuta dentro de st_samsung.py).
css = (AQUI / "ads22_tema.css").read_text(encoding="utf-8")
css += """
.st-paises{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}
.st-pais{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 18px 16px;display:flex;flex-direction:column;gap:10px;box-shadow:0 10px 26px rgba(20,40,160,.07);transition:.2s}
.st-pais:hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(20,40,160,.16)}
.st-pais h3{margin:0;font-size:1.25rem;display:flex;align-items:center;gap:10px}.st-flag{font-size:1.9rem;line-height:1}
.st-pais .city-tags{margin:0}.st-pais .st-go{margin-top:auto}
.st-servs{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}
.st-serv{display:flex;flex-direction:column;align-items:center;text-align:center;gap:8px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 12px;text-decoration:none;color:var(--ink);box-shadow:0 8px 22px rgba(20,40,160,.06);transition:.2s}
.st-serv:hover{transform:translateY(-3px);border-color:var(--aqua);box-shadow:0 16px 32px rgba(20,40,160,.16)}
.st-serv b{font-size:1.02rem}.st-serv small{color:var(--mute);font-size:.8rem}.ilus{max-width:100%}
.st-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 20px;border-radius:999px;font:700 15px Inter,sans-serif;text-decoration:none;border:2px solid var(--ocean);color:var(--ocean);background:#fff;cursor:pointer}
.st-btn.sol{background:var(--ocean);color:#fff}.st-btn.wa{border-color:#16a34a;color:#15803d}.st-btn:hover{box-shadow:0 8px 22px rgba(20,40,160,.22)}
.st-acc{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}
.aq-hero .st-btn{border-color:#fff}.aq-hero .st-btn.sol{background:#fff;color:var(--navy)}.aq-hero .st-btn.wa{background:#16a34a;color:#fff;border-color:#16a34a}
.st-pasos{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;counter-reset:p}
.st-paso{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px;position:relative}.st-paso b{display:block;margin-bottom:4px}
.st-paso::before{counter-increment:p;content:counter(p);position:absolute;right:14px;top:10px;font:800 1.6rem Inter,sans-serif;color:var(--aqua2)}
.st-filtros{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}.st-filtros a{background:#fff;border:1px solid var(--line);border-radius:14px;padding:10px;text-align:center;text-decoration:none;color:var(--ink);font-size:.85rem}.st-filtros img{width:100%;height:130px;object-fit:contain}
.st-brand-logo{height:22px;width:auto;display:block}.aq-brand{min-width:0;max-width:100%}@media(max-width:640px){.aq-brand{gap:8px}.aq-brand span small{display:none}.aq-brand span b{font-size:12.5px;line-height:1.15;white-space:normal}.st-brand-logo{height:18px}.aq-cta{padding:9px 14px;font-size:13px}}
.aq-ticker{display:flex;align-items:center;height:36px;background:#fff;border-bottom:1px solid var(--line);overflow:hidden}.aq-tk-tag{flex:none;height:100%;display:flex;align-items:center;background:var(--ocean);color:#fff;font:800 12.5px Inter,sans-serif;padding:0 16px;white-space:nowrap}.aq-tk-view{flex:1;overflow:hidden;min-width:0}.aq-tk-track{display:inline-flex;white-space:nowrap;animation:aqtk var(--d,120s) linear infinite}.aq-tk-track:hover{animation-play-state:paused}.aq-tk-track span{padding:0 14px;font:600 13px Inter,sans-serif;color:var(--ink2)}.aq-tk-track span::after{content:'•';margin-left:28px;color:var(--aqua)}@keyframes aqtk{to{transform:translateX(-50%)}}@media(prefers-reduced-motion:reduce){.aq-tk-track{animation:none}.aq-tk-view{overflow-x:auto}}
.qa-datos{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:8px}.qa-datos li{background:rgba(255,255,255,.7);border:1px solid var(--line);border-radius:10px;padding:8px 12px;font-size:.88rem}.qa-datos b{display:block;font-size:.72rem;letter-spacing:.04em;text-transform:uppercase;color:var(--ocean)}.qa-meta{margin:12px 0 0;font-size:.78rem;opacity:.7}.aq-qa-sec{padding:0 0 12px}
.aq-hero.compacto{padding:14px 0 44px}.aq-hero.compacto h1{font-size:clamp(1.7rem,3.2vw,2.5rem);margin:2px 0 8px}.aq-hero.compacto .aq-stage{display:none}.st-hero-art{display:none}@media(min-width:980px){.aq-hero.compacto .wrap{grid-template-columns:1.15fr .85fr!important}.st-hero-art{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;background:rgba(255,255,255,.12);padding:16px;border-radius:22px;border:1px solid rgba(255,255,255,.25)}.st-hero-art span{background:#fff;border-radius:14px;padding:8px 4px;display:flex;justify-content:center}}
.st-barra{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;gap:8px;padding:8px max(10px,env(safe-area-inset-left,0px)) calc(8px + env(safe-area-inset-bottom,0px));background:#fff;border-top:1px solid var(--line);box-shadow:0 -8px 22px rgba(20,40,160,.12)}.st-barra a{flex:1}
@media(max-width:760px){.st-barra{display:flex}body{padding-bottom:64px}.aq-wa{display:none}}
.st-form{display:grid;gap:12px;max-width:640px}.st-form label{display:grid;gap:4px;font-weight:600;font-size:.92rem}.st-form input,.st-form select,.st-form textarea{font:inherit;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink)}.st-form textarea{min-height:100px}.st-ok{background:#ecfdf5;border:1px solid #86efac;border-radius:14px;padding:16px}.st-hp{position:absolute;left:-9999px}
.st-aviso{font-size:.8rem;color:var(--mute);margin-top:10px}
.st-eq{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.st-eq-c{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:16px;display:flex;flex-direction:column;gap:10px;box-shadow:0 10px 26px rgba(20,40,160,.07);transition:.2s}
.st-eq-c:hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(20,40,160,.16);border-color:var(--aqua)}
.st-eq-top{display:flex;gap:14px;align-items:center}.st-eq-img{flex:none;background:var(--aqua-soft);border-radius:16px;padding:8px;display:flex}.st-eq-top h3{margin:0;font-size:1.12rem;line-height:1.2}
.st-eq-top img{height:13px;width:auto;display:block;margin-top:6px;opacity:.9}.st-eq-lin{margin:0;font-size:.82rem;color:var(--mute)}
.st-eq-chips{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}.st-eq-chips li{background:var(--aqua-soft);color:var(--ocean);border-radius:999px;padding:4px 10px;font-size:.76rem;font-weight:600}
.st-eq-btn{display:flex;gap:8px;margin-top:auto}.st-eq-btn a{flex:1;text-align:center;padding:10px 8px;font-size:13.5px}.st-eq-badge{font-size:.72rem;background:#fff7ed;color:#c2410c;border:1px solid #fed7aa;border-radius:999px;padding:2px 8px;margin-left:6px;font-weight:700}
"""
(OUT / "tema.css").write_text(css, encoding="utf-8")


def tel_txt(pk):
    return wa_vis(pk)


def encabezado(pk=None):
    wa = wa_link(pk or "colombia", "Hola, necesito servicio técnico para mi electrodoméstico Samsung")
    pais_pop = "".join(f'<div><h5><a href="{R_PAIS(k)}">{P["bandera"]} {esc(P["nombre"])}</a></h5><div class="aq-chips">' + "".join(f'<a href="{R_CIU(c)}">{esc(c["n"])}</a>' for c in CIU_PAIS[k]) + "</div></div>" for k, P in PAISES.items())
    serv_pop = "".join(f'<a href="{R_SERV(sv)}">{ilus(sv, 48)}<span><b>{esc(SERVICIOS[sv]["tit"])}</b><small>Servicio técnico</small></span></a>' for sv in ORDEN_SERV + ["tv"])
    return ('<div class="aq-h"><div class="aq-bar"><span>🛠️ Servicio técnico Samsung · línea blanca en 8 países</span><span>🗓️ Visita a domicilio · diagnóstico primero</span><a href="' + wa + '" target="_blank" rel="noopener">WhatsApp ' + esc(wa_vis(pk or "colombia")) + '</a></div>'
            '<div class="aq-ticker" role="marquee" aria-label="Ciudades donde damos servicio"><span class="aq-tk-tag">🌎 Servicio en toda la región</span><div class="aq-tk-view"><div class="aq-tk-track" data-tk></div></div></div>'
            '<div class="aq-row aq-wrap"><a class="aq-brand" href="index.html"><img class="st-brand-logo" src="img/samsung-logo.png" alt="Samsung" width="126" height="20"><span><b>Centro de Servicio Técnico</b><small>Línea blanca · 8 países</small></span></a>'
            '<form class="aq-search" role="search" onsubmit="return false">' + ICO["lupa"].replace("<svg", '<svg aria-hidden="true"') + '<input type="search" data-aq-q placeholder="Tu ciudad, país o electrodoméstico…" autocomplete="off" aria-label="Buscar"><div class="aq-res" hidden></div></form>'
            '<a class="aq-cta" href="solicitar-visita.html">Solicitar visita</a></div>'
            '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap"><a href="index.html">Inicio</a>'
            f'<details class="aq-dd"><summary>Países y ciudades</summary><div class="aq-pop ciu"><div class="aq-wrap">{pais_pop}</div></div></details>'
            f'<details class="aq-dd"><summary>Servicios</summary><div class="aq-pop prod"><div class="aq-wrap">{serv_pop}</div></div></details>'
            '<a href="guias-servicio-tecnico-samsung.html">Guías de fallas</a><a href="cobertura-servicio-tecnico-samsung.html">Cobertura</a><a href="preguntas-frecuentes-servicio-tecnico-samsung.html">Preguntas</a><a href="solicitar-visita.html"><b>Solicitar visita</b></a></div></nav></div>')


def pie():
    pa = "".join(f'<li><a href="{R_PAIS(k)}">{P["bandera"]} {esc(P["nombre"])}</a></li>' for k, P in PAISES.items())
    sv = "".join(f'<li><a href="{R_SERV(s)}">{esc(SERVICIOS[s]["tit"])}</a></li>' for s in ORDEN_SERV + ["tv"])
    top = "".join(f'<li><a href="{R_CIU(c)}">{esc(c["n"])}</a></li>' for c in CIU[:9])
    return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/samsung-oval.png" alt="Samsung" width="90" height="30" loading="lazy"></span>'
            '<p>Servicio técnico especializado en electrodomésticos Samsung: línea blanca en 8 países y televisores en Costa Rica. Samsung y su logotipo son marcas de Samsung Electronics Co., Ltd., y se usan solo para identificar la marca del equipo que reparamos. '
            'Este sitio es un servicio técnico independiente y no pertenece a Samsung Electronics ni es su canal oficial de soporte.</p></div>'
            f'<div><h5>Países</h5><ul>{pa}</ul></div><div><h5>Servicios</h5><ul>{sv}</ul></div><div><h5>Ciudades</h5><ul>{top}<li><a href="cobertura-servicio-tecnico-samsung.html"><b>Ver todas →</b></a></li></ul></div>'
            '<div><h5>Ayuda</h5><ul><li><a href="solicitar-visita.html">Solicitar visita</a></li><li><a href="guias-servicio-tecnico-samsung.html">Guías de fallas</a></li><li><a href="preguntas-frecuentes-servicio-tecnico-samsung.html">Preguntas frecuentes</a></li>'
            '<li><a href="respuestas-para-ia-servicio-tecnico-samsung.html">Respuestas rápidas</a></li><li><a href="quienes-somos.html">Quiénes somos</a></li><li><a href="contacto.html">Contacto</a></li><li><a href="mapa-del-sitio.html">Mapa del sitio</a></li></ul></div></div>'
            f'<div class="aq-wrap aq-f-pay"><div>© {_d.year} Centro de Servicio Técnico Samsung</div></div></footer>'
            f'<div class="st-barra"><a class="st-btn wa" href="{wa_link("colombia", "Hola, necesito servicio técnico para mi electrodoméstico Samsung")}" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a class="st-btn sol" href="solicitar-visita.html">Solicitar visita</a></div>')


def qa(titulo, respuesta, datos=None):
    d = ""
    if datos:
        d = '<ul class="qa-datos">' + "".join(f"<li><b>{esc(k)}</b>{esc(v)}</li>" for k, v in datos) + "</ul>"
    return (f'<section class="aq-qa-sec"><div class="wrap"><div class="qa" data-ia="respuesta"><p class="tag">⚡ Respuesta rápida</p><h2>{esc(titulo)}</h2><p>{respuesta}</p>{d}'
            f'<p class="qa-meta">Información revisada · actualizada el {FECHA_LARGA} · Servicio técnico especializado en Samsung</p></div></div></section>')


def seccion(h2, cuerpo, alt=False, sub=""):
    return f'<section class="aq-sec{" alt" if alt else ""}"><div class="wrap"><h2>{h2}</h2>' + (f'<p class="sub2">{sub}</p>' if sub else "") + cuerpo + "</div></section>"


def faq_html(preg, h2="Preguntas frecuentes"):
    return ('<section class="aq-sec alt"><div class="wrap"><h2>' + esc(h2) + '</h2><div class="faq-num">'
            + "".join(f'<details{" open" if i == 0 else ""}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for i, (q, a) in enumerate(preg)) + "</div></div></section>")


def hero_simple(kicker, h1, sub, extra=""):
    return f'<section class="hero"><div class="wrap"><span class="kicker">{esc(kicker)}</span><h1>{esc(h1)}</h1><p class="sub" style="margin-top:16px;">{esc(sub)}</p>{extra}</div></section>'


def acciones(pk, msg):
    return f'<div class="st-acc"><a class="st-btn wa" href="{wa_link(pk, msg)}" target="_blank" rel="noopener">{ICO["wa"]} Escribir por WhatsApp</a><a class="st-btn sol" href="solicitar-visita.html">Solicitar visita</a></div>'


def tiles_serv(pk, c=None):
    out = ""
    for sv in SERV_PAIS[pk]:
        s1, s2 = pal(pk, sv)
        href = R_CS(c, sv) if c else R_SERV(sv)
        out += f'<a class="st-serv" href="{href}">{ilus(sv, 84)}<b>{esc(SERVICIOS[sv]["tit"] if not c else s2.capitalize())}</b><small>{("Disponible en Costa Rica" if sv == "tv" else "Reparación y mantenimiento") if not c else "Ver servicio en " + esc(c["n"])}</small></a>'
    return f'<div class="st-servs">{out}</div>'


def panel_equipos(pk=None, c=None, titulo=None, compacto=False):
    """Todos los electrodomésticos que reparamos, con imagen, líneas Samsung y fallas típicas. pk/c dan el idioma local y el destino."""
    base = pk or "colombia"
    sv_lista = SERV_PAIS[pk] if pk else ORDEN_SERV + ["tv"]
    out = ""
    for sv in sv_lista:
        S = SERVICIOS[sv]
        s1, s2 = pal(base, sv) if (pk or sv != "tv") else pal("costa-rica", "tv")
        nom = c["n"] if c else None
        href = R_CS(c, sv) if c else R_SERV(sv)
        msg = f"Hola, necesito servicio técnico para mi {s1} Samsung" + (f" en {nom}" if nom else "")
        badge = '<span class="st-eq-badge">Solo Costa Rica</span>' if (sv == "tv" and not pk) else ""
        chips = "".join(f"<li>{esc(x)}</li>" for x in S["sintomas"][:3])
        if compacto:
            out += (f'<a class="st-serv" href="{href}">{ilus(sv, 64)}<b>{esc(cap(s2))}</b><small>{"Ver servicio en " + esc(nom) if nom else "Ver servicio"}</small></a>')
            continue
        out += (f'<article class="st-eq-c"><div class="st-eq-top"><a class="st-eq-img" href="{href}" aria-label="{esc(S["tit"])}">{ilus(sv, 72)}</a><div><h3>{esc(cap(s2) if c or pk else S["tit"])}{badge}</h3><img src="img/samsung-logo.png" alt="Samsung" width="80" height="13" loading="lazy"></div></div>'
                f'<p class="st-eq-lin">{esc(cap(S["lineas"]))}</p><ul class="st-eq-chips">{chips}</ul>'
                f'<div class="st-eq-btn"><a class="st-btn sol" href="{href}">{"Ver servicio" + (" en " + esc(nom) if nom else "")}</a><a class="st-btn wa" href="{wa_link(base, msg)}" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a></div></article>')
    ttl = titulo or ("Todos los electrodomésticos Samsung que reparamos" + (f" en {esc(c['n'])}" if c else ""))
    if compacto:
        return f'<section class="aq-sec estante-top st-equipos"><div class="wrap"><h2>{ttl}</h2><div class="st-servs">{out}</div></div></section>'
    return f'<section class="aq-sec estante-top st-equipos"><div class="wrap"><h2>{ttl}</h2><div class="st-eq">{out}</div></div></section>'


def ld_base(nombre, titulo, desc, miga, pk=None):
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    return [{"@type": "WebPage", "@id": url, "name": titulo, "url": url, "inLanguage": PAISES[pk]["cod"] if pk else "es", "description": desc, "dateModified": HOY, "isPartOf": {"@id": f"{DOMINIO}/#negocio"},
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa h2", ".qa p"]}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"{DOMINIO}/{u}"} if u else {})} for i, (n, u) in enumerate(miga)]}]


def ld_faq(preg):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}


NEGOCIO_LD = {"@type": ["ProfessionalService", "LocalBusiness"], "@id": f"{DOMINIO}/#negocio", "name": NOMBRE, "url": f"{DOMINIO}/", "logo": f"{DOMINIO}/img/samsung-oval.png", "image": f"{DOMINIO}/img/samsung-oval.png",
              "description": "Servicio técnico especializado en electrodomésticos Samsung: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas en 8 países; televisores en Costa Rica.",
              "telephone": "+" + WA_DEF, "priceRange": "$$", "areaServed": [{"@type": "Country", "name": P["nombre"]} for P in PAISES.values()] + [{"@type": "City", "name": c["n"]} for c in CIU],
              "knowsAbout": [SERVICIOS[s]["tit"] for s in SERVICIOS], "contactPoint": {"@type": "ContactPoint", "telephone": "+" + WA_DEF, "contactType": "customer service", "availableLanguage": "es"}}


def pagina(nombre, titulo, desc, kw, miga, cuerpo, preguntas=(), ld_extra=(), prio="0.6", pk=None, tipo="guias", ctx=None, compacto=False):
    titulo = titulo.strip()
    if len(titulo) > 66:
        titulo = titulo[:66].rsplit(" ", 1)[0].rstrip(" ,:;·|-")
    if len(desc) > 160:
        c = desc[:160]
        k = max(c.rfind(". "), c.rfind(": "), c.rfind("; "), c.rfind(", "))
        desc = (c[:k] if k > 90 else c[:c.rfind(" ")]).rstrip(" ,;:.") + "."
    url = f"{DOMINIO}/{nombre}" if nombre != "index.html" else f"{DOMINIO}/"
    graf = ld_base(nombre, titulo, desc, miga, pk) + ([ld_faq(list(preguntas))] if preguntas else []) + list(ld_extra)
    if nombre == "index.html":
        graf.append(NEGOCIO_LD)
    bc = '<div class="breadcrumb wrap" style="font:500 13px Inter,sans-serif;padding:16px 22px 0;">' + " / ".join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in miga) + "</div>" if len(miga) > 1 else ""
    hl = PAISES[pk]["cod"] if pk else "es"
    head = ('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><meta name="keywords" content="{esc(kw)}"><link rel="canonical" href="{url}">'
            '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#1428a0"><meta name="author" content="Centro de Servicio Técnico Samsung">'
            f'<link rel="alternate" hreflang="{hl}" href="{url}">' + (f'<link rel="alternate" hreflang="x-default" href="{url}">' if nombre == "index.html" else "") + f'<link rel="alternate" type="text/plain" href="{DOMINIO}/llms.txt" title="llms.txt"><link rel="alternate" type="application/json" href="{DOMINIO}/datos-servicio-tecnico.json" title="Datos estructurados">'
            + "".join(f'<meta name="google-site-verification" content="{t}">' for t in TOKENS)
            + (("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','" + GTM + "');</script>") if GTM else "")
            + f'<meta property="og:type" content="website"><meta property="og:locale" content="{hl.replace("-", "_")}"><meta property="og:site_name" content="{NOMBRE}"><meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMINIO}/img/samsung-oval.png">'
            f'<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{esc(titulo)}"><meta name="twitter:description" content="{esc(desc)}">'
            '<link rel="icon" href="img/icono-samsung.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="tema.css?v=st1">'
            f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body>'
            + (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' if GTM else ""))
    if cuerpo.startswith('<section class="hero">') and "st-equipos" not in cuerpo:
        k = cuerpo.index("</section>") + len("</section>")
        cuerpo = cuerpo[:k] + panel_equipos(pk, ctx, None, compacto) + cuerpo[k:]
    t = head + encabezado(pk) + bc + cuerpo + pie() + '<script src="buscar.js" defer></script></body></html>'
    (OUT / nombre).write_text(t, encoding="utf-8")
    PAGINAS.append((nombre, prio, titulo, desc, tipo))
    return t
