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
.aq-hero.compacto{padding:14px 0 44px}.aq-hero.compacto h1{font-size:clamp(1.7rem,3.2vw,2.5rem);margin:2px 0 8px}.aq-hero.compacto .aq-stage{display:none}.st-hero-art{display:none}@media(min-width:980px){.aq-hero.compacto .wrap{grid-template-columns:1.15fr .85fr!important}.st-hero-art{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;background:rgba(255,255,255,.12);padding:16px;border-radius:22px;border:1px solid rgba(255,255,255,.25)}.st-hero-art span{background:#fff;border-radius:14px;padding:8px 4px;display:flex;justify-content:center}.st-hero-art img{width:100%;height:auto;max-height:150px;object-fit:contain}.st-hero-art{grid-template-columns:repeat(2,1fr)!important}}
.st-barra{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;gap:8px;padding:8px max(10px,env(safe-area-inset-left,0px)) calc(8px + env(safe-area-inset-bottom,0px));background:#fff;border-top:1px solid var(--line);box-shadow:0 -8px 22px rgba(20,40,160,.12)}.st-barra a{flex:1}
@media(max-width:760px){.st-barra{display:flex}body{padding-bottom:64px}.aq-wa{display:none}}
.st-form{display:grid;gap:12px;max-width:640px}.st-form label{display:grid;gap:4px;font-weight:600;font-size:.92rem}.st-form input,.st-form select,.st-form textarea{font:inherit;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink)}.st-form textarea{min-height:100px}.st-ok{background:#ecfdf5;border:1px solid #86efac;border-radius:14px;padding:16px}.st-hp{position:absolute;left:-9999px}
.st-aviso{font-size:.8rem;color:var(--mute);margin-top:10px}.st-geo{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center;background:#eef2ff;border-bottom:1px solid var(--line);padding:10px 14px;font:500 14px Inter,sans-serif;position:relative}.st-geo .st-btn{padding:8px 14px;font-size:13px}.st-x{border:0;background:none;font-size:22px;cursor:pointer;color:var(--mute);line-height:1}.st-pais-det{outline:3px solid var(--aqua);box-shadow:0 16px 34px rgba(20,40,160,.22)}.hero.st-bg{background:linear-gradient(105deg,rgba(7,26,107,.9),rgba(20,40,160,.72) 52%,rgba(20,40,160,.32)),var(--bgimg) center 30%/cover no-repeat;min-height:300px}.hero.st-bg h1,.hero.st-bg .sub{text-shadow:0 2px 14px rgba(0,0,0,.35)}.st-split{display:grid;gap:20px;grid-template-columns:minmax(220px,340px) 1fr;align-items:center}@media(max-width:720px){.st-split{grid-template-columns:1fr}}
.st-foto{display:block;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;aspect-ratio:4/3}.st-fimg{width:100%;height:100%;display:block;object-fit:contain;background:#fff}.st-fimg.cover{object-fit:cover}
.st-serv .st-fimg{height:150px;border-radius:12px}.st-servs{grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}
.aq-pop.prod .st-fimg{width:48px;height:48px;border-radius:8px}.st-eq-top{display:flex;gap:10px;justify-content:space-between;align-items:center}
.st-eq{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px}
.st-eq-c{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:16px;display:flex;flex-direction:column;gap:10px;box-shadow:0 10px 26px rgba(20,40,160,.07);transition:.2s}
.st-eq-c:hover{transform:translateY(-3px);box-shadow:0 16px 34px rgba(20,40,160,.16);border-color:var(--aqua)}
.st-eq-top{display:flex;gap:14px;align-items:center}.st-eq-img{flex:none;background:var(--aqua-soft);border-radius:16px;padding:8px;display:flex}.st-eq-top h3{margin:0;font-size:1.12rem;line-height:1.2}
.st-eq-top img{height:13px;width:auto;display:block;margin-top:6px;opacity:.9}.st-eq-lin{margin:0;font-size:.82rem;color:var(--mute)}
.st-eq-chips{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}.st-eq-chips li{background:var(--aqua-soft);color:var(--ocean);border-radius:999px;padding:4px 10px;font-size:.76rem;font-weight:600}
.st-eq-btn{display:flex;gap:8px;margin-top:auto}.st-eq-btn a{flex:1;text-align:center;padding:10px 8px;font-size:13.5px}.st-eq-badge{font-size:.72rem;background:#fff7ed;color:#c2410c;border:1px solid #fed7aa;border-radius:999px;padding:2px 8px;margin-left:6px;font-weight:700}
"""
css += "\n.glos{margin:0}.glos dt{margin-top:14px}.glos dd{margin:3px 0 0;color:#445}\n"
css += "\n.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}.gal figure{margin:0}.gal img{width:100%;height:auto;border-radius:14px;display:block;background:#fff}.gal figcaption{font-size:13px;color:#5a6873;margin-top:6px}\n.aq-sec .wrap::after{content:'';display:block;clear:both}.sec-img{float:right;width:46%;margin:4px 0 14px 26px}.sec-img.izq{float:left;margin:4px 26px 14px 0}.sec-img figcaption{font-size:12.5px;color:#5a6873;margin-top:6px;line-height:1.35}.sec-img img{width:100%;height:auto;border-radius:14px;display:block}.sec-img.prod img{background:#fff;border:1px solid #e3e8f0;padding:10px}@media(max-width:760px){.sec-img,.sec-img.izq{float:none;width:100%;margin:0 auto 16px}}\n.hero.st-split{display:block;padding:44px 0 62px}.hero.st-split .st-hgrid{width:100%;margin:0 auto}.st-hgrid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:38px;align-items:center}.st-hfig{margin:0}.st-hfig img{width:100%;height:auto;border-radius:18px;display:block;box-shadow:0 22px 50px rgba(0,0,0,.35)}@media(max-width:860px){.st-hgrid{grid-template-columns:1fr}.st-hfig{max-width:520px}}\nbody{counter-reset:cap}.aq-sec.chap>.wrap>h2::before{counter-increment:cap;content:counter(cap);display:inline-flex;align-items:center;justify-content:center;min-width:1.55em;height:1.55em;margin-right:.55em;border-radius:50%;background:#1428a0;color:#fff;font:800 .55em Inter,sans-serif;vertical-align:.22em}.toc-sec{padding:6px 0 0}.toc{background:#fff;border:1px solid #dfe5f5;border-radius:16px;padding:16px 20px;font:600 14px Inter,sans-serif}.toc b{display:block;margin-bottom:6px;font-size:15px}.toc ol{margin:0;padding-left:20px;columns:2;column-gap:32px}.toc li{margin:3px 0;break-inside:avoid}.toc a{color:#1428a0;text-decoration:none}.toc a:hover{text-decoration:underline}@media(max-width:700px){.toc ol{columns:1}}\n"
(OUT / "tema.css").write_text(css, encoding="utf-8")


def tel_txt(pk):
    return wa_vis(pk)


def encabezado(pk=None):
    if pk:
        P = PAISES[pk]; cs = CIU_PAIS[pk]
        wa = wa_link(pk, f"Hola, necesito servicio técnico para mi electrodoméstico Samsung en {P['nombre']}")
        ciu_pop = "".join(f'<a href="{R_CIU(c)}">{esc(c["n"])}</a>' for c in cs[:14]) + (f'<a href="{R_PAIS(pk)}"><b>Ver las {len(cs)} ciudades →</b></a>' if len(cs) > 14 else "")
        _lbl = f"Ciudades de {P['nombre']}"
        if SOLO:
            _c0 = cs[0]; _lbl = f"Barrios de {_c0['n']}"
            ciu_pop = "".join(f'<a href="{R_Z(_c0, z)}">{esc(z)}</a>' for z in _c0["zonas"]) + f'<a href="{R_BARRIOS(_c0)}"><b>Ver todos los barrios →</b></a>'
        pop_c = f'<div class="aq-pop ciu"><div class="aq-wrap"><div><h5>{esc(_lbl)}</h5><div class="aq-chips">{ciu_pop}</div></div></div></div>'
        serv_pop = "".join(f'<a href="{R_SERV(pk, sv)}">{foto_serv(sv, 48, True)}<span><b>{esc(cap(pal(pk, sv)[1]))}</b><small>Servicio técnico</small></span></a>' for sv in SERV_PAIS[pk])
        bar1 = f"Servicio técnico Samsung en {cs[0]['n'] if SOLO else P['nombre']}"; bar2 = ("Abierto las 24 horas · visita a domicilio" if SOLO and SOLO_CFG[SOLO].get("horas24") else "Visita a domicilio · diagnóstico primero"); sub = f"Línea blanca · {cs[0]['n'] if SOLO else P['nombre']}"
        nav = (f'<a href="{R_PAIS(pk)}">Inicio</a>' f'<details class="aq-dd"><summary>{esc(_lbl)}</summary>{pop_c}</details>'
               f'<details class="aq-dd"><summary>Servicios</summary><div class="aq-pop prod"><div class="aq-wrap">{serv_pop}</div></div></details>'
               f'<a href="{R_GUIAS(pk)}">Guías de fallas</a>' + (f'<a href="{R_GAL(cs[0])}">Galería</a>' if SOLO else "") + f'<a href="{pk}/blog/index.html">Blog</a><a href="{R_FAQ(pk)}">Preguntas</a><a href="{R_SOL(pk)}"><b>Solicitar visita</b></a>')
        tk = f'<span class="aq-tk-tag">Servicio en {esc(P["nombre"])}</span><div class="aq-tk-view"><div class="aq-tk-track" data-tk="{pk}"></div></div>'
        ph = (f"Tu barrio de {cs[0]['n']} o electrodoméstico…" if SOLO else f"Tu ciudad en {P['nombre']} o electrodoméstico…")
    else:
        wa = "index.html#paises"
        pais_pop = '<div><h5>Elige tu país</h5><div class="aq-chips">' + "".join(f'<a href="{R_PAIS(k)}">{esc(P["nombre"])}</a>' for k, P in PAISES.items()) + "</div></div>"
        bar1 = "Servicio técnico Samsung a domicilio"; bar2 = "Elige tu país para ver tu ciudad"; sub = "Línea blanca"
        nav = ('<a href="index.html">Inicio</a>' f'<details class="aq-dd"><summary>Países</summary><div class="aq-pop ciu"><div class="aq-wrap">{pais_pop}</div></div></details>'
               '<a href="index.html#paises"><b>Elegir mi país</b></a>')
        tk = '<span class="aq-tk-tag">Elige tu país</span><div class="aq-tk-view"><div class="aq-tk-track" data-tk="paises"></div></div>'
        ph = "Tu país, tu ciudad o electrodoméstico…"
    num = wa_vis(pk) if pk else None
    return ('<div class="aq-h"><div class="aq-bar"><span>' + esc(bar1) + '</span><span>' + esc(bar2) + '</span><a href="' + wa + '"' + (' target="_blank" rel="noopener">WhatsApp ' + esc(num) if pk else '>Elegir mi país') + '</a></div>'
            f'<div class="aq-ticker" role="marquee" aria-label="Ciudades">{tk}</div>'
            '<div class="aq-row aq-wrap"><a class="aq-brand" href="' + (R_PAIS(pk) if pk else "index.html") + '"><img class="st-brand-logo" src="img/samsung-logo.png" alt="Samsung" width="126" height="20"><span><b>Soporte Técnico</b><small>' + esc(sub) + '</small></span></a>'
            '<form class="aq-search" role="search" onsubmit="return false">' + ICO["lupa"].replace("<svg", '<svg aria-hidden="true"') + f'<input type="search" data-aq-q data-aq-pais="{pk or ""}" placeholder="{esc(ph)}" autocomplete="off" aria-label="Buscar"><div class="aq-res" hidden></div></form>'
            '<a class="aq-cta" href="' + (R_SOL(pk) if pk else "index.html#paises") + '">Solicitar visita</a></div>'
            '<nav class="aq-nav" aria-label="Principal"><div class="aq-wrap">' + nav + '</div></nav></div>')


def pie(pk=None):
    if pk:
        P = PAISES[pk]; cs = CIU_PAIS[pk]
        sv = "".join(f'<li><a href="{R_SERV(pk, s)}">{esc(cap(pal(pk, s)[1]))}</a></li>' for s in SERV_PAIS[pk])
        top = "".join(f'<li><a href="{R_CIU(c)}">{esc(c["n"])}</a></li>' for c in cs[:9]) + f'<li><a href="{R_PAIS(pk)}"><b>Ver todas →</b></a></li>'
        blurb = (f"Servicio técnico especializado en electrodomésticos Samsung en {P['nombre']}: " + ", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk]) + ". ")
        ayuda = (f'<li><a href="{R_SOL(pk)}">Solicitar visita</a></li><li><a href="{R_GUIAS(pk)}">Guías de fallas</a></li><li><a href="{pk}/blog/index.html">Blog</a></li><li><a href="{R_FAQ(pk)}">Preguntas frecuentes</a></li>'
                 f'<li><a href="{R_IA(pk)}">Respuestas rápidas</a></li><li><a href="{R_VOLT(pk)}">Voltaje en {esc(P["nombre"])}</a></li><li><a href="{R_INST(pk, "quienes-somos")}">Quiénes somos</a></li><li><a href="{R_INST(pk, "contacto")}">Contacto</a></li><li><a href="{R_MAPA(pk)}">Mapa del sitio</a></li>')
        if SOLO:
            top = "".join(f'<li><a href="{R_Z(cs[0], z)}">{esc(z)}</a></li>' for z in cs[0]["zonas"][:9]) + f'<li><a href="{R_BARRIOS(cs[0])}"><b>Ver todos →</b></a></li>'
        col2 = f'<div><h5>Servicios</h5><ul>{sv}</ul></div><div><h5>{"Barrios" if SOLO else "Ciudades"}</h5><ul>{top}</ul></div>'
        if SOLO and SOLO_CFG[SOLO].get("direccion"):
            col2 += f'<div><h5>Ubicación y horario</h5><ul><li>{esc(SOLO_CFG[SOLO]["direccion"])}</li><li>Abierto las 24 horas</li><li><a href="tel:+{wa_num(pk)}">{esc(wa_vis(pk))}</a></li><li><a href="{R_UBIC(cs[0])}">Cómo contactarnos →</a></li><li><a href="{R_24H(cs[0])}">Servicio las 24 horas</a></li></ul></div>'
    else:
        blurb = "Servicio técnico especializado en electrodomésticos Samsung. "
        paises = "".join(f'<li><a href="{R_PAIS(k)}">{esc(P["nombre"])}</a></li>' for k, P in PAISES.items())
        col2 = f'<div><h5>Países</h5><ul>{paises}</ul></div>'
        ayuda = '<li><a href="index.html#paises">Elegir mi país</a></li>'
    return ('<footer class="aq-f"><div class="aq-wrap"><div class="brandcol"><span class="logo-w"><img src="img/samsung-oval.png" alt="Samsung" width="90" height="30" loading="lazy"></span>'
            f'<p>{esc(blurb)}Samsung y su logotipo son marcas de Samsung Electronics Co., Ltd., y se usan solo para identificar la marca del equipo que reparamos. Este sitio es un servicio técnico independiente y no pertenece a Samsung Electronics ni es su canal oficial de soporte.</p></div>'
            f'{col2}<div><h5>Ayuda</h5><ul>{ayuda}</ul></div></div>'
            f'<div class="aq-wrap aq-f-pay"><div>© {_d.year} Soporte Técnico Samsung</div></div></footer>'
            + (f'<div class="st-barra"><a class="st-btn wa" href="{wa_link(pk, "Hola, necesito servicio técnico para mi electrodoméstico Samsung")}" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a><a class="st-btn sol" href="{R_SOL(pk)}">Solicitar visita</a></div>' if pk else '<div class="st-barra"><a class="st-btn wa" href="index.html#paises">Elegir mi país</a></div>'))


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
    if not pk:
        return '<div class="st-acc"><a class="st-btn sol" href="index.html#paises">Elegir mi país</a></div>'
    return f'<div class="st-acc"><a class="st-btn wa" href="{wa_link(pk, msg)}" target="_blank" rel="noopener">{ICO["wa"]} Escribir por WhatsApp</a><a class="st-btn sol" href="{R_SOL(pk)}">Solicitar visita</a></div>'


def tiles_serv(pk, c=None):
    out = ""
    for sv in SERV_PAIS[pk]:
        s1, s2 = pal(pk, sv)
        href = R_CS(c, sv) if c else R_SERV(pk, sv)
        out += f'<a class="st-serv" href="{href}">{foto_serv(sv, 150, False, c["n"] if c else (PAISES[pk]["nombre"] if pk else None))}<b>{esc(cap(s2))}</b><small>{"Ver servicio en " + esc(c["n"]) if c else "Reparación y mantenimiento"}</small></a>'
    return f'<div class="st-servs">{out}</div>'


def panel_equipos(pk=None, c=None, titulo=None, compacto=False):
    """Todos los electrodomésticos que reparamos, con su foto. pk/c dan el vocabulario local y el destino."""
    base = pk or SOLO_PK or "colombia"  # solo para el vocabulario; sin país, los botones llevan a elegir país
    sv_lista = SERV_PAIS[pk] if pk else ORDEN_SERV
    out = ""
    for sv in sv_lista:
        S = SERVICIOS[sv]
        s1, s2 = pal(base, sv)
        nom = c["n"] if c else None
        href = R_CS(c, sv) if c else (R_SERV(pk, sv) if pk else "index.html#paises")
        msg = f"Hola, necesito servicio técnico para mi {s1} Samsung" + (f" en {nom}" if nom else "")
        if compacto:
            out += f'<a class="st-serv" href="{href}">{foto_serv(sv, 130, False, nom or (PAISES[pk]["nombre"] if pk else None))}<b>{esc(cap(s2))}</b><small>{"Ver servicio en " + esc(nom) if nom else "Ver servicio"}</small></a>'
            continue
        chips = "".join(f"<li>{esc(x)}</li>" for x in S["sintomas"][:3])
        out += (f'<article class="st-eq-c"><a class="st-foto" href="{href}" aria-label="{esc(cap(s2))}">{foto_serv(sv, 220, False, nom or (PAISES[pk]["nombre"] if pk else None))}</a><div class="st-eq-top"><h3>{esc(cap(s2) if (c or pk) else S["tit"])}</h3><img src="img/samsung-logo.png" alt="Samsung" width="80" height="13" loading="lazy"></div>'
                f'<p class="st-eq-lin">{esc(cap(S["lineas"]))}</p><ul class="st-eq-chips">{chips}</ul>'
                f'<div class="st-eq-btn"><a class="st-btn sol" href="{href}">{"Ver servicio" + (" en " + esc(nom) if nom else "")}</a>{(f'<a class="st-btn wa" href="{wa_link(pk, msg)}" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a>' if pk else '<a class="st-btn" href="index.html#paises">Elegir país</a>')}</div></article>')
    ttl = titulo or ("Todos los electrodomésticos Samsung que reparamos" + (f" en {esc(c['n'])}" if c else (f" en {esc(PAISES[pk]['nombre'])}" if pk else "")))
    if compacto:
        return f'<section class="aq-sec estante-top st-equipos"><div class="wrap"><h2>{ttl}</h2><div class="st-servs">{out}</div></div></section>'
    return f'<section class="aq-sec estante-top st-equipos"><div class="wrap"><h2>{ttl}</h2><div class="st-eq">{out}</div></div></section>'


def ld_base(nombre, titulo, desc, miga, pk=None):
    url = U(nombre)
    return [{"@type": "WebPage", "@id": url, "name": titulo, "url": url, "inLanguage": PAISES[pk]["cod"] if pk else "es", "description": desc, "dateModified": HOY, "isPartOf": {"@id": f"{DOMINIO}/#negocio"},
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".qa h2", ".qa p"]}},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": U(u)} if u else {})} for i, (n, u) in enumerate(miga)]}]


def ld_faq(preg):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in preg]}


NEGOCIO_LD = {"@type": ["ProfessionalService", "LocalBusiness"], "@id": f"{DOMINIO}/#negocio", "name": NOMBRE, "url": f"{DOMINIO}/", "logo": f"{DOMINIO}/img/samsung-oval.png", "image": f"{DOMINIO}/img/samsung-oval.png",
              "description": "Servicio técnico especializado en electrodomésticos Samsung: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas en 8 países; televisores en Costa Rica.",
              "priceRange": "$$", "areaServed": [{"@type": "Country", "name": P["nombre"]} for P in PAISES.values()] + [{"@type": "City", "name": c["n"]} for c in CIU],
              "knowsAbout": [SERVICIOS[s]["tit"] for s in SERVICIOS], "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + wa_num(k), "contactType": "customer service", "areaServed": P["nombre"], "availableLanguage": "es"} for k, P in PAISES.items()]}


GEO_META = (lambda g: f'<meta name="geo.region" content="{g["region"]}"><meta name="geo.placename" content="{g["nombre"]}"><meta name="geo.position" content="{g["lat"]};{g["lon"]}"><meta name="ICBM" content="{g["lat"]}, {g["lon"]}">')(SOLO_CFG[SOLO]) if SOLO else ""


def negocio_solo():
    c = CIU[0]; P = PAISES[c["pk"]]
    return {"@type": ["ProfessionalService", "LocalBusiness"], "@id": f"{DOMINIO}/#negocio", "name": NOMBRE, "url": U(R_CIU(c)), "telephone": "+" + wa_num(c["pk"]), "image": f"{DOMINIO}/img/samsung-oval.png", "logo": f"{DOMINIO}/img/samsung-oval.png",
            "description": f"Servicio técnico independiente de electrodomésticos Samsung a domicilio en {c['n']}, {c['dep']}: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas.", "priceRange": "$$",
            "address": ({"@type": "PostalAddress", "streetAddress": SOLO_CFG[SOLO]["calle"] + ", " + SOLO_CFG[SOLO]["barrio_dir"], "addressLocality": c["n"], "addressRegion": c["dep"], "addressCountry": "CO"} if SOLO_CFG[SOLO].get("calle") else {"@type": "PostalAddress", "addressLocality": c["n"], "addressRegion": c["dep"], "addressCountry": "CO"}),
            **({"openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"}], "hasMap": "https://www.google.com/maps?q=" + __import__("urllib.parse").parse.quote_plus(SOLO_CFG[SOLO]["direccion"])} if SOLO_CFG[SOLO].get("horas24") else {}), "geo": {"@type": "GeoCoordinates", "latitude": SOLO_CFG[SOLO]["lat"], "longitude": SOLO_CFG[SOLO]["lon"]},
            "areaServed": [{"@type": "City", "name": c["n"]}] + [{"@type": "Place", "name": z + ", " + c["n"]} for z in c["zonas"]], "knowsAbout": [SERVICIOS[s_]["tit"] for s_ in SERV_PAIS[c["pk"]]],
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": f"Servicio técnico Samsung en {c['n']}", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Reparación y mantenimiento de {pal(c['pk'], s_)[1]} Samsung en {c['n']}", "url": U(R_CS(c, s_))}} for s_ in SERV_PAIS[c["pk"]]]},
            "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + wa_num(c["pk"]), "contactType": "customer service", "areaServed": "CO", "availableLanguage": "es"}]}


def faq_base(pk):
    ap = f" en {PAISES[pk]['nombre']}" if pk else ""
    wa = f"Escríbenos por WhatsApp al {wa_vis(pk)}" if pk else "Elige tu país y escríbenos por WhatsApp"
    return [(f"¿Qué electrodomésticos Samsung reparan{ap}?", "Línea blanca: neveras, lavadoras, secadoras, lavavajillas, estufas y hornos, y microondas" + ("; en Costa Rica también televisores." if (not pk or pk == "costa-rica") else ".")),
            ("¿Cómo pido una visita técnica?", f"{wa} o usa el formulario de solicitud de visita; coordinamos el día y el técnico va a tu domicilio."), ("¿El diagnóstico va antes de la reparación?", "Sí: el técnico revisa el equipo, te explica la falla y el valor se confirma antes de reparar."),
            ("¿Atienden equipos fuera de garantía?", "Sí. Si tu equipo aún tiene garantía, revisa sus condiciones en el manual antes de intervenirlo."), ("¿Son el servicio oficial de Samsung?", "No: somos un servicio técnico especializado independiente; Samsung es una marca de Samsung Electronics Co., Ltd.")]


def pagina(nombre, titulo, desc, kw, miga, cuerpo, preguntas=(), ld_extra=(), prio="0.6", pk=None, tipo="guias", ctx=None, compacto=False):
    titulo = titulo.strip()
    if SOLO and SOLO_CFG[SOLO].get("titulo_home") and nombre == R_CIU(CIU[0]):
        titulo = SOLO_CFG[SOLO]["titulo_home"]; desc = SOLO_CFG[SOLO]["desc_home"]
    if SOLO:
        _p = nombre.split("/")
        if nombre in ("index.html", f"{SOLO_PK}/index.html") or (_p[0] == SOLO_PK and len(_p) == 3 and _p[2] == "index.html" and _p[1] not in ("guias", "blog", "preguntas-frecuentes", "respuestas-rapidas", "solicitar-visita", "contacto", "quienes-somos", "mapa-del-sitio", "voltaje", SOLO_D)):
            return ""
    if not preguntas and nombre != "404.html":
        preguntas = faq_base(pk)
        cuerpo = cuerpo + faq_html(preguntas)
    if SOLO and pk:
        _pn = PAISES[pk]["nombre"]; _cn_ = CIU[0]["n"]
        if titulo.endswith("| " + _pn):
            titulo = titulo[:-len(_pn)] + _cn_
        elif _cn_ not in titulo and "Samsung" in titulo and len(titulo) < 56:
            titulo = titulo + " en " + _cn_
    if len(titulo) > 66:
        titulo = titulo[:66].rsplit(" ", 1)[0].rstrip(" ,:;·|-")
    if len(desc) > 160:
        c = desc[:160]
        k = max(c.rfind(". "), c.rfind(": "), c.rfind("; "), c.rfind(", "))
        desc = (c[:k] if k > 90 else c[:c.rfind(" ")]).rstrip(" ,;:.") + "."
    url = U(nombre)
    if pk:  # el "Inicio" de un país es el propio país: nada lleva fuera de él
        miga = [(n, u) for n, u in miga if u != "index.html"]
        miga = [(n, u) for n, u in miga if u != R_PAIS(pk)]
        if nombre != R_PAIS(pk):
            miga = [("Inicio", R_PAIS(pk))] + miga
    _wa_bloque = ""
    if pk and tipo in ("ciudades", "zonas", "paises") and cuerpo.startswith('<section class="hero') and not re.search(r"/(whatsapp|telefono)/index\.html$", nombre):
        _lugar = ctx["n"] if ctx else PAISES[pk]["nombre"]
        _q = f"¿Cuál es el WhatsApp del servicio técnico Samsung en {_lugar}?"
        _a = f"El WhatsApp y teléfono del servicio técnico Samsung en {_lugar} es {wa_vis(pk)}. Escribe con el equipo, el modelo y la falla y coordinamos la visita a domicilio; el valor se confirma antes de reparar."
        _lk = (f'<p class="qa-meta"><a href="{R_WA(ctx)}">WhatsApp en {esc(_lugar)}</a> · <a href="{R_TEL(ctx)}">Teléfono en {esc(_lugar)}</a></p>' if ctx and nombre not in (R_WA(ctx), R_TEL(ctx)) else (f'<p class="qa-meta"><a href="{R_WAP(pk)}">WhatsApp en {esc(_lugar)}</a> · <a href="{R_TELP(pk)}">Teléfono en {esc(_lugar)}</a></p>' if not ctx and nombre == R_PAIS(pk) else ""))
        _wa_bloque = qa(_q, esc(_a), [("WhatsApp", wa_vis(pk)), ("Atención", "A domicilio")]).replace('<p class="qa-meta">Información', _lk + '<p class="qa-meta">Información', 1)
        preguntas = list(preguntas) + [(_q, _a)]
    graf = ld_base(nombre, titulo, desc, miga, pk) + ([ld_faq(list(preguntas))] if preguntas else []) + list(ld_extra)
    if nombre == "index.html":
        graf.append(NEGOCIO_LD)
    if SOLO and nombre == R_CIU(CIU[0]):
        graf.append(negocio_solo())
    bc = '<div class="breadcrumb wrap" style="font:500 13px Inter,sans-serif;padding:16px 22px 0;">' + " / ".join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in miga) + "</div>" if len(miga) > 1 else ""
    hl = PAISES[pk]["cod"] if pk else "es"
    head = ('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
            f'<title>{esc(titulo)}</title><meta name="description" content="{esc(desc)}"><meta name="keywords" content="{esc(kw)}"><link rel="canonical" href="{url}">'
            + (f'<meta name="st-pais" content="{pk}">' if pk else '') + '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"><meta name="theme-color" content="#1428a0"><meta name="author" content="Soporte Técnico Samsung">'
            + ('<link rel="alternate" type="application/rss+xml" title="Blog" href="feed.xml">' if SOLO else "") +
            f'<link rel="alternate" hreflang="{hl}" href="{url}">' + (f'<link rel="alternate" hreflang="x-default" href="{url}">' if nombre == "index.html" else "") + f'<link rel="alternate" type="text/plain" href="{DOMINIO}/{(pk + "/llms.txt") if pk else "llms.txt"}" title="llms.txt"><link rel="alternate" type="application/json" href="{DOMINIO}/datos-servicio-tecnico.json" title="Datos estructurados">'
            + "".join(f'<meta name="google-site-verification" content="{t}">' for t in TOKENS)
            + (("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','" + GTM + "');</script>") if GTM else "")
            + f'<meta property="og:type" content="website"><meta property="og:locale" content="{hl.replace("-", "_")}"><meta property="og:site_name" content="{NOMBRE}"><meta property="og:title" content="{esc(titulo)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMINIO}/img/{hero_img(nombre) if SOLO else "samsung-oval"}.{"webp" if SOLO else "png"}">'
            f'<meta name="twitter:card" content="{"summary_large_image" if SOLO else "summary"}">{GEO_META if SOLO else ""}<meta name="twitter:title" content="{esc(titulo)}"><meta name="twitter:description" content="{esc(desc)}">'
            '<link rel="icon" href="img/icono-samsung.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="tema.css?v=st1">'
            f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graf}, ensure_ascii=False)}</script></head><body>'
            + (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM}" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>' if GTM else ""))
    if cuerpo.startswith('<section class="hero">') and tipo in ("ciudades", "zonas") and not SOLO:
        cuerpo = mezclar_secciones(cuerpo, nombre)
    if cuerpo.startswith('<section class="hero">'):
        cuerpo = cuerpo.replace('<section class="hero">', f'<section class="hero st-bg" style="--bgimg:url(img/{hero_img(nombre)}.webp)">', 1)
    if cuerpo.startswith('<section class="hero st-bg"') and "st-equipos" not in cuerpo:
        k = cuerpo.index("</section>") + len("</section>")
        cuerpo = cuerpo[:k] + panel_equipos(pk, ctx, None, compacto) + cuerpo[k:]
    if _wa_bloque and cuerpo.startswith('<section class="hero st-bg"'):
        _k = cuerpo.index("</section>") + len("</section>")
        cuerpo = cuerpo[:_k] + _wa_bloque + cuerpo[_k:]
    t = head + encabezado(pk) + bc + cuerpo + pie(pk) + '<script>window.ST_ROOT="__ROOT__"</script><script src="' + (f"{pk}/buscar.js" if pk else "buscar.js") + '" defer></script>' + ('<script src="geo.js" defer></script>' if not pk else (f'<script src="{pk}/geo.js" defer></script>' if nombre == R_PAIS(pk) else "")) + '</body></html>'
    assert nombre not in {x[0] for x in PAGINAS}, f"URL repetida: {nombre}"
    if SOLO:
        for _a, _b in (("Soporte Técnico Samsung", "Servicio Técnico Samsung"), ("Soporte técnico Samsung", "Servicio técnico Samsung"), ("Soporte Samsung", "Servicio Samsung"), ("| Soporte técnico", "| A domicilio"), ("Soporte Técnico</b>", "Servicio Técnico</b>")):
            t = t.replace(_a, _b)
    if SOLO:
        t = t.replace("1 ciudades", "1 ciudad").replace(f"Servicio en {PAISES[SOLO_PK]['nombre']}", f"Servicio en {CIU[0]['n']}").replace(f" Samsung en {PAISES[SOLO_PK]['nombre']}:", f" Samsung en {CIU[0]['n']}:")
        if (nombre.split("/")[2:3] or [""])[0].endswith("-samsung") or (nombre.split("/")[2:3] or [""])[0].endswith(("-samsung",)):
            t = t.replace(f" en {PAISES[SOLO_PK]['nombre']}", f" en {CIU[0]['n']}")
        if nombre.split("/")[1:2] and nombre.split("/")[1] in ("guias", "blog", "preguntas-frecuentes", "respuestas-rapidas", "solicitar-visita", "contacto", "quienes-somos", "mapa-del-sitio"):
            t = t.replace(f" en {PAISES[SOLO_PK]['nombre']}", f" en {CIU[0]['n']}")
    (OUT / nombre).parent.mkdir(parents=True, exist_ok=True)
    (OUT / nombre).write_text(t, encoding="utf-8")
    PAGINAS.append((nombre, prio, titulo, desc, tipo))
    return t
