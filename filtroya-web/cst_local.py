# -*- coding: utf-8 -*-
"""SEO local sin marca (hubs para toda la ciudad): /zonas/, /zonas/<zona>/, /equipos/, /equipos/<equipo>/ y /marcas/.
Cada página une todas las marcas con una zona o con un equipo, y enlaza a las páginas de marca (marca x zona, marca x equipo).
Todo el texto sale de los datos reales de cada zona y de cada marca; no se inventan precios, plazos ni horarios."""
import re


def build_local(g):
    M, EQ, CFG, ZONAS, ZX, CLIMA, BO = g["M"], g["EQ"], g["CFG"], g["ZONAS"], g["ZX"], g["CLIMA"], g["BRANDS_ORDER"]
    pagina, sec, faq_html, faq_ld, cap, esc, pathb, base, junta = g["pagina"], g["sec"], g["faq_html"], g["faq_ld"], g["cap"], g["esc"], g["pathb"], g["base"], g["junta"]
    DOM, NOMBRE, TEL, nom = g["DOM"], g["NOMBRE"], g["TEL"], g["nom"]
    MI = g.get("MI_LOC", {})
    ciu = CFG["ciudad"]; sect = CFG.get("sectores", {}); sector_de = CFG.get("sector_de", {})
    ceq = set(CFG.get("comunas_eq", []))
    lista = lambda xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
    pill = lambda u, t: f'<a class="pill" href="{u}">{esc(t)}</a>'
    card = lambda u, t, s="": f'<a class="card l" href="{u}"><span class="t">{esc(t)}</span>' + (f"<br><small>{esc(s)}</small>" if s else "") + "</a>"
    crumbs0 = [(NOMBRE, "/")]
    marcas = [m for m in BO if m in M]
    # equipos presentes (sin pantallas), en el orden de EQ
    equipos = [e for e in EQ if not e.startswith("tv-") and any(e in M[m]["equipos"] for m in marcas)]
    brands_de = {e: [m for m in marcas if e in M[m]["equipos"]] for e in equipos}
    art = g["ART_EQ"]

    # ------------------------------------------------------------------ /zonas/<zona>/
    for zi, (z, zv) in enumerate(ZONAS.items()):
        zn, sectores, rasgo = zv
        viv, acc, vis = ZX[z]
        sl = sector_de.get(z); sv = [c for c in sect[sl][2] if c != z] if sl else []
        cerca = (sv[zi % len(sv):] + sv[:zi % len(sv)])[:8] if sv else []
        eq_ok = [e for e in equipos]
        faq = [(f"¿Hacen visitas a domicilio de servicio técnico en {zn}?", f"Sí. Atendemos {vis}. Escríbenos por WhatsApp con la marca, el equipo y lo que hace, y coordinamos el día y la franja teniendo en cuenta {acc}."),
               (f"¿Qué marcas de electrodomésticos reparan en {zn}?", f"Atendemos {junta(nom(m) for m in marcas)}. Elige tu marca más abajo para ver sus fallas y equipos."),
               (f"¿Qué equipos reparan en {zn}?", f"Reparamos {junta(EQ[e][2] for e in eq_ok)}, según la marca. Si tu equipo no aparece, escríbenos con el modelo y la falla."),
               (f"¿Qué hago si mi equipo falla después de una tormenta o un apagón en {zn}?", f"Desconéctalo, espera unos minutos y no lo reinicies varias veces seguidas: los picos de voltaje dañan las placas. {CLIMA[z].capitalize()} influyen en cómo envejecen los equipos de esta zona. Escríbenos y lo revisamos a domicilio."),
               (f"¿Cuánto cuesta una visita de servicio técnico en {zn}?", "El valor depende del equipo y de la falla. Se confirma por escrito después del diagnóstico y solo se repara si tú lo apruebas.")]
        marc = "".join(card(pathb(m, "servicio-tecnico-" + z), f"Servicio técnico {nom(m)} en {zn}", ", ".join([EQ[e][2] for e in M[m]["equipos"] if not e.startswith("tv-")][:4])) for m in marcas)
        eqs = "".join(card(f"/equipos/{EQ[e][0]}/", f"Reparación de {EQ[e][2]} en {zn}", f"{len(brands_de[e])} marca" + ("s" if len(brands_de[e]) != 1 else "")) for e in eq_ok)
        rs = rasgo if rasgo.endswith(".") else rasgo + "."
        cuerpo = (sec(f"Atención a domicilio en {zn}",
                      f"<p>Atendemos equipos de {junta(nom(m) for m in marcas)} a domicilio en {esc(zn)}. {esc(rs)} Entre los sectores que visitamos están {esc(vis)}.</p>"
                      f"<p>Al coordinar la visita en {esc(zn)} contamos con {esc(acc)}. {esc(CLIMA[z].capitalize())} influyen en cómo envejecen los equipos de esta zona.</p>")
                  + sec(f"Marcas que atendemos en {zn}", f'<div class="g c3">{marc}</div>', alt=True)
                  + sec(f"Equipos que reparamos en {zn}", f'<div class="g c3">{eqs}</div>')
                  + sec(f"Cómo es la visita en {zn}", lista(["<b>Escríbenos</b> por WhatsApp con la marca, el modelo y lo que hace el equipo.", f"<b>Coordinamos</b> el día y la franja en {esc(zn)}, con {esc(acc)}.",
                                                            "<b>Diagnóstico en tu casa</b>: revisamos el equipo y te explicamos la causa.", "<b>Cotización antes de reparar</b>: solo se repara si tú lo apruebas."]), alt=True)
                  + (sec(f"Zonas cercanas a {zn}", "<p>" + "".join(pill(f"/zonas/{c}/", f"Servicio técnico en {ZONAS[c][0]}") for c in cerca) + "</p>" + (f'<p><a href="{pathb(marcas[0], "servicio-tecnico-" + sl)}">Servicio técnico en {esc(sect[sl][0])}</a> · <a href="/zonas/">Todas las zonas</a></p>' if sl else '<p><a href="/zonas/">Todas las zonas</a></p>')) if cerca else "")
                  + sec(f"Preguntas frecuentes: servicio técnico en {zn}", faq_html(faq), alt=True))
        pagina(f"/zonas/{z}/", f"Servicio técnico de electrodomésticos en {zn}", f"Servicio técnico a domicilio en {zn}: {junta(nom(m) for m in marcas[:5])} y más. Fallas, equipos que reparamos y cómo coordinar la visita por WhatsApp.",
               f"Servicio técnico de electrodomésticos en {zn}", cuerpo, None, None, crumbs0 + [("Zonas", "/zonas/"), (zn, f"/zonas/{z}/")],
               [{"@type": "Service", "name": f"Servicio técnico de electrodomésticos en {zn}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": zn, "containedInPlace": {"@type": "City", "name": ciu}},
                 "serviceType": "Reparación de electrodomésticos a domicilio"}, faq_ld(faq)],
               bd=f"{ciu} · {zn}", prio="0.8", lead=f"Todas las marcas en {esc(zn)}: equipos, fallas frecuentes y visita a domicilio por WhatsApp.")

    # ------------------------------------------------------------------ /zonas/
    cuerpo = ""
    for i, (sl, (frase, desc, zs)) in enumerate(sect.items()):
        cuerpo += sec(f"Servicio técnico en {frase}", f"<p>{esc(desc)}</p>" + '<div class="g c3">' + "".join(card(f"/zonas/{z}/", f"Servicio técnico en {ZONAS[z][0]}", ZONAS[z][1]) for z in zs) + "</div>", alt=bool(i % 2))
    faq = [(f"¿En qué zonas de {ciu} atienden?", f"Atendemos {len(ZONAS)} zonas y municipios: {junta(ZONAS[z][0] for z in list(ZONAS)[:10])} y más. En cada zona puedes ver las marcas y los equipos que reparamos."),
           ("¿Cómo sé si mi zona está cubierta?", "Escríbenos por WhatsApp con tu zona o colonia y el equipo, y confirmamos si podemos atenderte y coordinamos día y franja.")]
    cuerpo += sec("Preguntas frecuentes", faq_html(faq), alt=bool(len(sect) % 2))
    pagina("/zonas/", f"Zonas donde damos servicio técnico en {ciu}", f"Todas las zonas y municipios de {ciu} donde reparamos electrodomésticos a domicilio: Samsung, LG, Whirlpool, Mabe y más marcas.", f"Zonas de servicio técnico en {ciu}", cuerpo, None, None,
           crumbs0 + [("Zonas", "/zonas/")],
           [{"@type": "Service", "name": f"Servicio técnico de electrodomésticos en {ciu}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": [{"@type": "Place", "name": zv[0]} for zv in list(ZONAS.values())[:30]]}, faq_ld(faq)],
           bd=f"{ciu} · Cobertura", prio="0.9", lead=f"Elige tu zona en {esc(ciu)} para ver las marcas y los equipos que reparamos a domicilio.")

    # ------------------------------------------------------------------ /equipos/<equipo>/
    for e in equipos:
        ms = brands_de[e]; sing, pl = EQ[e][1], EQ[e][2]; un = art.get(e, "un")
        fall, vistos = [], set()
        for k in range(6):
            for m in ms:
                fs = M[m]["fallas"].get(e, [])
                if k < len(fs) and fs[k][0].lower() not in vistos and len(fall) < 6:
                    vistos.add(fs[k][0].lower()); fall.append(fs[k])
        mi = MI.get(e, {})
        mant = (f"<p>{esc(mi['mant_intro'])}</p>" if mi.get("mant_intro") else "") + (f"<p>{esc(mi['mant_gye'])}</p>" if mi.get("mant_gye") else "")
        zds = [z for z in CFG.get("zonas_destacadas", list(ZONAS))[:12] if z in ZONAS]
        faq = [(f"¿Reparan {pl} de todas las marcas?", f"Reparamos {pl} de {junta(nom(m) for m in ms)}. Elige tu marca para ver sus fallas y cómo pedir la visita."),
               (f"¿Cuánto cuesta reparar {un} {sing}?", "El valor depende de la marca, el modelo y la falla. Se confirma por escrito después del diagnóstico y solo se repara si tú lo apruebas."),
               (f"¿Mi {sing} falló después de una tormenta o un apagón: qué hago?", "Desconéctalo, espera unos minutos y no lo reinicies varias veces seguidas. Los picos de voltaje al volver la luz dañan las placas y los compresores. Escríbenos y lo revisamos a domicilio."),
               (f"¿En qué zonas de {ciu} reparan {pl}?", f"Atendemos {len(ZONAS)} zonas y municipios, entre ellos {junta(ZONAS[z][0] for z in zds[:6])}. Escríbenos con tu zona y confirmamos.")]
        cuerpo = (sec(f"Reparación de {pl} a domicilio en {ciu}", f"<p>Reparamos {esc(pl)} de {esc(junta(nom(m) for m in ms))} en {esc(ciu)}. El técnico va a tu casa, revisa el equipo, te explica la causa y te da la cotización antes de reparar.</p>")
                  + sec(f"Marcas de {pl} que reparamos", '<div class="g c3">' + "".join(card(pathb(m, "reparacion-" + EQ[e][0]), f"Reparación de {pl} {nom(m)}", f"Servicio técnico {nom(m)} en {ciu}") for m in ms) + "</div>", alt=True)
                  + sec(f"Fallas más comunes en {pl}", lista([f"<b>{esc(f[0].rstrip('.'))}.</b> Causa probable: {esc((f[1] or '')[:1].lower() + (f[1] or '')[1:])}" for f in fall]))
                  + (sec(f"Mantenimiento de {pl} en {ciu}", mant, alt=True) if mant else "")
                  + sec(f"Zonas donde reparamos {pl}", "<p>" + "".join(pill(f"/zonas/{z}/", f"Reparación de {pl} en {ZONAS[z][0]}") for z in zds) + '</p><p><a href="/zonas/">Ver todas las zonas</a></p>')
                  + sec(f"Preguntas frecuentes: reparación de {pl}", faq_html(faq), alt=True))
        pagina(f"/equipos/{EQ[e][0]}/", f"Reparación de {pl} en {ciu}", f"Reparación de {pl} a domicilio en {ciu}: {junta(nom(m) for m in ms[:5])} y más. Fallas comunes, mantenimiento y cómo pedir la visita por WhatsApp.",
               f"Reparación de {pl} en {ciu}", cuerpo, None, None, crumbs0 + [("Equipos", "/equipos/"), (cap(pl), f"/equipos/{EQ[e][0]}/")],
               [{"@type": "Service", "name": f"Reparación de {pl} en {ciu}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "City", "name": ciu}, "serviceType": f"Reparación de {pl}"}, faq_ld(faq)],
               bd=f"{ciu} · {cap(pl)}", prio="0.8", lead=f"{cap(pl)} de {esc(junta(nom(m) for m in ms[:6]))}: fallas frecuentes y visita a domicilio.")

    # ------------------------------------------------------------------ /equipos/
    cuerpo = sec(f"Qué equipos reparamos en {ciu}", '<div class="g c3">' + "".join(card(f"/equipos/{EQ[e][0]}/", f"Reparación de {EQ[e][2]}", f"{len(brands_de[e])} marca" + ("s" if len(brands_de[e]) != 1 else "") + ": " + ", ".join(nom(m) for m in brands_de[e][:4]) + ("…" if len(brands_de[e]) > 4 else "")) for e in equipos) + "</div>")
    pagina("/equipos/", f"Equipos que reparamos en {ciu}", f"Reparación a domicilio en {ciu} de {junta(EQ[e][2] for e in equipos[:6])} y más, de las principales marcas.", f"Equipos que reparamos en {ciu}", cuerpo, None, None, crumbs0 + [("Equipos", "/equipos/")],
           None, bd=f"{ciu} · Equipos", prio="0.8", lead=f"Elige tu tipo de equipo para ver las marcas, las fallas frecuentes y cómo pedir la visita.")

    # ------------------------------------------------------------------ /marcas/
    cards = "".join(f'<a class="card l" href="{base(m)}"><img src="/img/logos/{m}.png" alt="Logo {esc(nom(m))}" width="130" height="40" style="display:block;height:30px;width:auto;max-width:130px;object-fit:contain;margin-bottom:6px"><span class="t">Servicio técnico {esc(nom(m))} en {esc(ciu)}</span><br><small>{esc(", ".join(EQ[e][2] for e in M[m]["equipos"] if not e.startswith("tv-")))}</small></a>' for m in marcas)
    cuerpo = sec(f"Marcas que reparamos en {ciu}", f'<div class="g c3">{cards}</div>')
    pagina("/marcas/", f"Marcas de electrodomésticos que reparamos en {ciu}", f"Servicio técnico a domicilio en {ciu} para {junta(nom(m) for m in marcas)}.", f"Marcas que reparamos en {ciu}", cuerpo, None, None, crumbs0 + [("Marcas", "/marcas/")],
           None, bd=f"{ciu} · Marcas", prio="0.8", lead="Elige tu marca para ver sus equipos, fallas frecuentes y zonas de cobertura.")
