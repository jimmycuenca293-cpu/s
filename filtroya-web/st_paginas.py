# Páginas del proyecto de servicio técnico (se ejecuta dentro de st_samsung.py, después de st_base.py).
def cap(t):
    return t[:1].upper() + t[1:]


def H(clave):
    return int(hashlib.md5(clave.encode()).hexdigest()[:8], 16)


def pick(clave, lista):
    return lista[H(clave) % len(lista)]


def zonas_txt(c, n=3):
    return ", ".join(c["zonas"][:n])


def guias_de(sv):
    return [g for g in GUIAS if g["serv"] == sv]


# ------------------------------------------------------------------ ciudad × servicio (una página con contenido propio por ciudad y equipo)
for c in CIU:
    pk = c["pk"]; P = PAISES[pk]
    for sv in SERV_PAIS[pk]:
        S = SERVICIOS[sv]; s1, s2 = pal(pk, sv)
        nom = c["n"]; z3 = zonas_txt(c)
        tit = pick(f"t|{c['s']}|{sv}", [f"Reparación de {s2} Samsung en {nom} | A domicilio", f"Servicio técnico de {s2} Samsung en {nom}", f"Técnico de {s2} Samsung en {nom} | Visita a domicilio", f"{cap(s2)} Samsung en {nom}: reparación y mantenimiento", f"Arreglo de {s2} Samsung en {nom} | Servicio técnico"])
        intro = pick(f"i|{c['s']}|{sv}", [
            f"Si tu {s1} Samsung falla en {nom}, vamos a tu casa: revisamos el equipo, te decimos qué tiene y te confirmamos el valor antes de reparar.",
            f"En {nom} ({c['dep']}) atendemos {s2} Samsung a domicilio. Coordinas por WhatsApp y un técnico revisa tu equipo en tu hogar.",
            f"¿Tu {s1} Samsung dejó de funcionar en {nom}? Te ayudamos con el diagnóstico y la reparación, sin que tengas que mover el equipo.",
            f"Reparamos y damos mantenimiento a {s2} Samsung en {nom}, en zonas como {z3} y alrededores."])
        nota = pick(f"n|{c['s']}|{sv}", [
            f"Atendemos {nom} y sus zonas: {', '.join(c['zonas'])}.", f"Hacemos visitas en {', '.join(c['zonas'][:5])} y otros sectores de {nom}.", f"Si estás en {z3} u otro sector de {nom}, escríbenos y coordinamos la visita."])
        msg = f"Hola, necesito servicio técnico para mi {s1} Samsung en {nom}"
        preg = [(f"¿Reparan {s2} Samsung en {nom}?", f"Sí. Atendemos {s2} Samsung en {nom} con visita a domicilio; escríbenos por WhatsApp para coordinar."),
                (f"¿Cuánto cuesta reparar una {s1} Samsung en {nom}?" if sv != "tv" else f"¿Cuánto cuesta reparar un {s1} Samsung en {nom}?", "Depende de la falla y del repuesto. Primero se hace el diagnóstico y te confirmamos el valor antes de reparar."),
                (f"¿Van a domicilio en {nom}?", f"Sí, atendemos en tu casa en {z3} y otras zonas de {nom}."),
                (f"¿Qué líneas Samsung atienden?", f"{S['lineas'].capitalize()}."),
                ("¿Cómo agendo la visita?", f"Escríbenos por WhatsApp al {wa_vis(pk)} o usa el formulario de solicitud de visita.")] + faq_cs(c, sv)
        otros = [x for x in SERV_PAIS[pk] if x != sv]
        veci = [x for x in CIU_PAIS[pk] if x is not c][:6]
        cuerpo = (hero_simple(f"{nom} · {P['nombre']}", f"Reparación de {s2} Samsung en {nom}", f"Servicio técnico a domicilio para {s2} Samsung en {nom}, {c['dep']}.", acciones(pk, msg))
                  + qa(f"¿Reparan {s2} Samsung en {nom}?", f"Sí. Reparamos y damos mantenimiento a {esc(s2)} Samsung en <b>{esc(nom)}</b> ({esc(z3)} y más) con visita a domicilio. Escríbenos, hacemos el diagnóstico y te confirmamos el valor antes de reparar.",
                       [("Ciudad", f"{nom}, {P['nombre']}"), ("Equipo", cap(s2) + " Samsung"), ("Atención", "A domicilio" + (" (cobertura ampliada)" if c["amp"] else "")), ("WhatsApp", wa_vis(pk))])
                  + seccion(f"{esc(cap(s2))} Samsung en {esc(nom)}", f"<p>{esc(intro)}</p><p>{esc(nota + nota_amp(c))}</p><p>Líneas Samsung que atendemos: {esc(S['lineas'])}.</p>")
                  + seccion(f"Fallas que reparamos en {esc(s2)} Samsung", "<ul class=\"spec-list\">" + "".join(f"<li>Tu {esc(s1)} {esc(x)}.</li>" for x in S["sintomas"]) + "</ul>", alt=True)
                  + bloque_local(c, sv, f"bl|{c['s']}|{sv}")
                  + seccion("Qué revisa el técnico", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in S["revisa"]) + "</ul>" + (f'<p style="margin-top:14px">Si quieres adelantar algo: <a href="{R_G(guias_de(sv)[0])}">guía de fallas de {esc(s2)} Samsung</a>.</p>' if guias_de(sv) else ""))
                  + seccion(f"Sectores de {esc(nom)} donde damos servicio", '<div class="city-tags">' + "".join(zlink(c, z) for z in c["zonas"]) + "</div>")
                  + faq_html(preg, f"Preguntas sobre {s2} Samsung en {nom}")
                  
                  + seccion("Más información", '<div class="city-tags">' + f'<a href="{R_CIU(c)}">Servicio técnico Samsung en {esc(nom)}</a><a href="{R_PAIS(pk)}">Servicio en {esc(P["nombre"])}</a><a href="{R_SERV(pk, sv)}">{esc(cap(s2))} Samsung en {esc(P["nombre"])}</a>'
                            + "".join(f'<a href="{R_G(g)}">{esc(g["tit"])}</a>' for g in guias_de(sv)[:3]) + "".join(f'<a href="{R_CS(v, sv)}">{esc(cap(s2))} Samsung en {esc(v["n"])}</a>' for v in veci) + "</div>"))
        pagina(R_CS(c, sv), tit, f"Reparación de {s2} Samsung en {nom}, {P['nombre']}: servicio técnico a domicilio, diagnóstico primero y valor confirmado antes de reparar.",
               f"reparacion {s2} samsung {nom.lower()}, servicio tecnico {s2} samsung {nom.lower()}, tecnico {s1} samsung {nom.lower()}", [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (nom, R_CIU(c)), (cap(s2), None)], cuerpo, preg,
               [{"@type": "Service", "name": f"Reparación de {s2} Samsung en {nom}", "serviceType": f"Reparación de {s2}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "City", "name": nom}}], prio="0.6", pk=pk, tipo="ciudades", ctx=c, compacto=True)

# ------------------------------------------------------------------ página de cada ciudad
for c in CIU:
    pk = c["pk"]; P = PAISES[pk]; nom = c["n"]
    tit = pick(f"c|{c['s']}", [f"Servicio técnico Samsung en {nom} | Línea blanca", f"Servicio técnico de electrodomésticos Samsung en {nom}", f"Técnico Samsung en {nom} | Reparación a domicilio", f"Reparación de electrodomésticos Samsung en {nom}"])
    nombres = ", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk])
    preg = [(f"¿Hay servicio técnico Samsung en {nom}?", f"Sí. Atendemos {nombres} Samsung en {nom} con visita a domicilio."),
            (f"¿Qué electrodomésticos Samsung reparan en {nom}?", f"{cap(nombres)}."),
            ("¿Cómo pido una visita?", f"Por WhatsApp al {wa_vis(pk)} o desde el formulario de solicitud de visita."), ("¿Cuánto cuesta?", "Se cotiza después del diagnóstico; te confirmamos el valor antes de reparar.")]
    msg = f"Hola, necesito servicio técnico Samsung en {nom}"
    cuerpo = (hero_simple(f"{nom} · {P['nombre']}", f"Servicio técnico Samsung en {nom}", f"Reparación y mantenimiento de línea blanca Samsung a domicilio en {nom}, {c['dep']}.", acciones(pk, msg))
              + qa(f"¿Hay servicio técnico Samsung en {nom}?", f"Sí. En <b>{esc(nom)}</b> reparamos {esc(nombres)} Samsung a domicilio, en zonas como {esc(zonas_txt(c, 4))}. Escríbenos por WhatsApp, hacemos el diagnóstico y te confirmamos el valor antes de reparar.",
                   [("Ciudad", f"{nom}, {P['nombre']}"), ("Equipos", f"{len(SERV_PAIS[pk])} tipos"), ("Atención", "A domicilio"), ("WhatsApp", wa_vis(pk))])
              + seccion(f"Sectores de {esc(nom)} que atendemos", '<div class="city-tags">' + "".join(zlink(c, z, f"Servicio técnico Samsung en {z}") for z in c["zonas"]) + f'<a href="{R_MANT(c)}">Mantenimiento según el clima de {esc(nom)}</a></div>')
              + seccion(f"{esc(nom)}: clima, electricidad y electrodomésticos", f"<p>{esc(parrafo_clima(c, c['zonas'][0], uno('cs|' + c['s'], SERV_PAIS[pk]), 'cp|' + c['s']))}</p><p>{esc('En ' + nom + ' la red eléctrica es de ' + VOLT[pk][0] + ' a ' + VOLT[pk][1] + '. ' + cap(CLIMA[c['s']]['riesgo']) + ': por eso recomendamos protector de voltaje y mantenimiento preventivo.')}</p>"
                        + f'<p><a href="{R_MANT(c)}">Guía de mantenimiento para {esc(nom)}</a> · <a href="{R_VOLT(pk)}">Voltaje en {esc(P["nombre"])}</a></p>')
              + seccion("Fallas más comunes", "<ul class=\"spec-list\">" + "".join(f'<li><a href="{R_G(g)}">{esc(g["tit"])}</a></li>' for g in mix("fm|" + c["s"], GUIAS, 8)) + "</ul>", alt=True)
              + faq_html(preg) + seccion("Otras ciudades", '<div class="city-tags">' + "".join(f'<a href="{R_CIU(v)}">{esc(v["n"])}</a>' for v in CIU if v is not c) + f'</div><p style="margin-top:12px"><a href="{R_PAIS(pk)}">Servicio técnico Samsung en {esc(P["nombre"])}</a></p>'))
    pagina(R_CIU(c), tit, f"Servicio técnico Samsung en {nom}, {P['nombre']}: {nombres}. Visita a domicilio, diagnóstico primero y valor confirmado antes de reparar.", f"servicio tecnico samsung {nom.lower()}, tecnico samsung {nom.lower()}, reparacion electrodomesticos samsung {nom.lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (nom, None)], cuerpo, preg,
           [{"@type": "Service", "name": f"Servicio técnico Samsung en {nom}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "City", "name": nom, "containedInPlace": {"@type": "Country", "name": P["nombre"]}}}], prio="0.8", pk=pk, tipo="ciudades", ctx=c)

# ------------------------------------------------------------------ países
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; nombres = ", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk]); ciudades_txt = ", ".join(c["n"] for c in cs)
    preg = [(f"¿Hay servicio técnico Samsung en {P['nombre']}?", f"Sí, atendemos en {ciudades_txt}: {nombres} Samsung a domicilio."), (f"¿Cómo se dice «refrigerador» en {P['nombre']}?", f"En {P['nombre']} se usa «{pal(pk, 'nevera')[0]}»; por eso nuestras páginas usan ese término."),
            ("¿Cómo pido una visita?", f"Por WhatsApp al {wa_vis(pk)} o con el formulario de solicitud."), ("¿Cuánto cuesta?", "Se cotiza tras el diagnóstico; te confirmamos el valor antes de reparar.")]
    cuerpo = (hero_simple(f"{P['bandera']} {P['nombre']}", f"Servicio técnico Samsung en {P['nombre']}", f"Reparación de {nombres} Samsung a domicilio en {ciudades_txt}.", acciones(pk, f"Hola, necesito servicio técnico Samsung en {P['nombre']}"))
              + seccion(f"Ciudades de {esc(P['nombre'])} donde damos servicio", '<div class="st-paises">' + "".join(f'<a class="st-pais" href="{R_CIU(c)}"><h3><span class="st-flag">{P["bandera"]}</span>{esc(c["n"])}</h3><div class="city-tags">' + "".join(f"<span>{esc(z)}</span>" for z in c["zonas"][:4]) + '</div><span class="st-btn st-go">Ver servicio técnico →</span></a>' for c in cs) + "</div>")
              + qa(f"¿Hay servicio técnico Samsung en {P['nombre']}?", f"Sí. En {esc(P['nombre'])} atendemos {esc(ciudades_txt)}: reparamos {esc(nombres)} Samsung a domicilio. Escríbenos por WhatsApp para coordinar la visita.", [("País", P["nombre"]), ("Ciudades", str(len(cs))), ("WhatsApp", wa_vis(pk))])
              + faq_html(preg))
    pagina(R_PAIS(pk), f"Servicio técnico Samsung en {P['nombre']} | Línea blanca", f"Servicio técnico Samsung en {P['nombre']}: {nombres} en {ciudades_txt}. Visita a domicilio y valor confirmado antes de reparar.", f"servicio tecnico samsung {P['nombre'].lower()}, reparacion electrodomesticos samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], None)], cuerpo, preg, [], prio="0.9", pk=pk, tipo="paises", ctx=cs[0] if len(cs) == 1 else None)

# ------------------------------------------------------------------ servicios, uno por país (cada país con sus ciudades y su vocabulario)
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]
    for sv in SERV_PAIS[pk]:
        S = SERVICIOS[sv]; s1, s2 = pal(pk, sv)
        ciu_clima = [c for c in cs if not c["amp"]][:3] or cs[:3]
        efectos = " ".join(f"En {c['n']}, {efecto_de(c, sv)}." for c in ciu_clima[:2])
        preg = [(f"¿Reparan {s2} Samsung en {P['nombre']}?", f"Sí: {S['lineas']}. Visita a domicilio en " + ", ".join(c["n"] for c in cs[:8]) + (" y más ciudades." if len(cs) > 8 else ".")),
                (f"¿Cuánto cuesta reparar una {s1} Samsung en {P['nombre']}?" if sv != "tv" else f"¿Cuánto cuesta reparar un {s1} Samsung en {P['nombre']}?", "Depende de la falla y el repuesto; primero el diagnóstico y te confirmamos el valor antes de reparar."),
                ("¿Cómo agendo?", f"Por WhatsApp al {wa_vis(pk)} o con el formulario de solicitud de visita.")]
        cuerpo = (hero_simple(f"{P['nombre']}", f"Servicio técnico de {s2} Samsung en {P['nombre']}", f"Diagnóstico y reparación a domicilio de {s2} Samsung en {len(cs)} ciudades de {P['nombre']}.", acciones(pk, f"Hola, necesito servicio técnico para mi {s1} Samsung en {P['nombre']}"))
                  + qa(f"¿Reparan {s2} Samsung en {P['nombre']}?", f"Sí. Reparamos {esc(s2)} Samsung ({esc(S['lineas'])}) a domicilio en {esc(P['nombre'])}. Escríbenos por WhatsApp: hacemos el diagnóstico y te confirmamos el valor antes de reparar.", [("Equipo", cap(s2) + " Samsung"), ("País", P["nombre"]), ("Atención", "A domicilio"), ("WhatsApp", wa_vis(pk))])
                  + seccion(f"{esc(cap(s2))} Samsung: ciudades de {esc(P['nombre'])}", '<div class="city-tags">' + "".join(f'<a href="{R_CS(c, sv)}">{esc(cap(s2))} Samsung en {esc(c["n"])}</a>' for c in cs) + "</div>")
                  + seccion("Fallas que reparamos", f'<div class="st-split"><div class="st-foto">{foto_serv(sv, 320)}</div><ul class="spec-list" style="margin:0">' + "".join(f"<li>Tu {esc(s1)} {esc(x)}.</li>" for x in S["sintomas"]) + "</ul></div>", alt=True)
                  + seccion("Qué revisa el técnico", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in S["revisa"]) + "</ul>" + f"<p>{esc(efectos)}</p>")
                  + (seccion("Guías de fallas", '<div class="city-tags">' + "".join(f'<a href="{R_G(g)}">{esc(g["tit"])}</a>' for g in guias_de(sv)) + "</div>", alt=True) if guias_de(sv) else "") + faq_html(preg))
        pagina(R_SERV(pk, sv), f"Servicio técnico de {s2} Samsung en {P['nombre']}", f"Reparación de {s2} Samsung a domicilio en {P['nombre']} ({S['lineas']}). Diagnóstico primero y valor confirmado antes de reparar.", f"servicio tecnico {s2} samsung {P['nombre'].lower()}, reparacion {s2} samsung {P['nombre'].lower()}",
               [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (cap(s2), None)], cuerpo, preg, [{"@type": "Service", "name": f"Servicio técnico de {s2} Samsung en {P['nombre']}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "Country", "name": P["nombre"]}}], prio="0.8", pk=pk, tipo="paises")

# ------------------------------------------------------------------ guías
for g in GUIAS:
    sv = g["serv"]; pks = [pk for pk in PAISES if sv in SERV_PAIS[pk]]
    otros = [x for x in GUIAS if x is not g][:4]
    cuerpo = (hero_simple("Guía de fallas", g["tit"], g["desc"], acciones("colombia", f"Hola, mi equipo Samsung tiene este problema: {g['tit']}"))
              + qa(g["tit"], esc(g["res"])) + seccion(esc(g["tit"]), '<div class="prose">' + g["cuerpo"] + "</div>")
              + seccion("¿Prefieres que lo revise un técnico?", f'<p>Pide una visita a domicilio: hacemos el diagnóstico y te confirmamos el valor antes de reparar.</p>' + acciones("colombia", f"Hola, necesito revisar mi equipo Samsung: {g['tit']}") + '<h3 style="margin:22px 0 10px">Elige tu país</h3><div class="city-tags">' + "".join(f'<a href="{R_SERV(k, sv)}">{esc(PAISES[k]["nombre"])}</a>' for k in pks) + "</div>", alt=True)
              + faq_html(g["preg"]) + seccion("Sigue leyendo", '<div class="city-tags">' + "".join(f'<a href="{R_G(o)}">{esc(o["tit"])}</a>' for o in otros) + "</div>"))
    art = {"@type": "Article", "headline": g["tit"], "description": g["desc"], "inLanguage": "es", "datePublished": HOY, "dateModified": HOY, "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@id": f"{DOMINIO}/#negocio"}}
    pagina(R_G(g), g["tit"], g["desc"], g["tit"].lower() + ", samsung", [("Inicio", "index.html"), ("Guías", "guias-servicio-tecnico-samsung.html"), (g["tit"], None)], cuerpo, g["preg"], [art], prio="0.7", tipo="guias")

pagina("guias-servicio-tecnico-samsung.html", "Guías de fallas de electrodomésticos Samsung", "Guías prácticas de fallas en neveras, lavadoras, secadoras, lavavajillas, hornos y microondas Samsung: códigos de error, causas y qué hacer.", "guias fallas samsung, codigos error lavadora samsung",
       [("Inicio", "index.html"), ("Guías", None)], hero_simple("Guías", "Guías de fallas de electrodomésticos Samsung", "Códigos de error, causas y qué hacer antes de llamar al técnico.") + qa("¿Qué hago si mi electrodoméstico Samsung falla?", "Revisa la guía de tu falla: muchos problemas (códigos 4E, 5E, UE, dE, LE en lavadoras; escarcha o falta de frío en neveras) tienen pasos de revisión. Si persiste, pide una visita técnica.")
       + seccion("Todas las guías", '<div class="city-tags">' + "".join(f'<a href="{R_G(g)}">{esc(g["tit"])}</a>' for g in GUIAS) + "</div>"), [], [], prio="0.7", tipo="guias")

# ------------------------------------------------------------------ cobertura y preguntas generales (solo para elegir país)
def selector_paises(sufijo=None):
    return '<div class="st-paises">' + "".join(
        f'<a class="st-pais" href="{(sufijo.format(pk=pk) if sufijo else R_PAIS(pk))}"><h3><span class="st-flag">{P["bandera"]}</span>{esc(P["nombre"])}</h3><div class="city-tags">' + "".join(f"<span>{esc(c['n'])}</span>" for c in CIU_PAIS[pk][:3]) + f'</div><span class="st-btn st-go">Ver {esc(P["nombre"])} →</span></a>' for pk, P in PAISES.items()) + "</div>"


pagina("cobertura-servicio-tecnico-samsung.html", "Cobertura del servicio técnico Samsung", "Elige tu país para ver las ciudades y los electrodomésticos Samsung que reparamos a domicilio.", "cobertura servicio tecnico samsung, ciudades servicio samsung",
       [("Inicio", "index.html"), ("Cobertura", None)], hero_simple("Cobertura", "Elige tu país", "Cada país tiene su propia página con sus ciudades, sus equipos y su WhatsApp.")
       + qa("¿Dónde dan servicio técnico Samsung?", "Elige tu país: cada uno tiene su propia página con las ciudades donde atendemos y los equipos que reparamos.") + seccion("Tu país", selector_paises()), [], [], prio="0.8", tipo="paises")

faqs = [("¿Reparan electrodomésticos Samsung a domicilio?", "Sí, hacemos visita a domicilio en las ciudades de cobertura de cada país."), ("¿Cómo encuentro mi ciudad?", "Elige tu país en la portada y entra a la página de tu ciudad."),
        ("¿Qué equipos Samsung reparan?", "Línea blanca: neveras, lavadoras, secadoras, lavavajillas, estufas y hornos y microondas; en Costa Rica también televisores."), ("¿Cuánto cuesta la reparación?", "Depende de la falla y el repuesto. Primero se hace el diagnóstico y se confirma el valor antes de reparar."),
        ("¿Cómo pido una visita?", "Por WhatsApp o con el formulario de solicitud de visita."), ("¿Son el servicio oficial de Samsung?", "Somos un servicio técnico especializado independiente; no somos Samsung Electronics ni su canal oficial de soporte.")]
faqs += [(q, a) for g in GUIAS[:8] for q, a in g["preg"][:1]]
pagina("preguntas-frecuentes-servicio-tecnico-samsung.html", "Preguntas frecuentes del servicio técnico Samsung", "Respuestas sobre reparación a domicilio de línea blanca Samsung: equipos, costos y cómo agendar. Elige tu país para ver las preguntas de tu ciudad.", "preguntas frecuentes servicio tecnico samsung",
       [("Inicio", "index.html"), ("Preguntas frecuentes", None)], hero_simple("Respuestas", "Preguntas frecuentes", "Lo que más nos preguntan sobre el servicio técnico Samsung.") + qa("¿Cómo funciona el servicio técnico Samsung a domicilio?", "Escribes por WhatsApp, coordinamos la visita, el técnico hace el diagnóstico en tu casa y te confirma el valor antes de reparar.") + faq_html(faqs)
       + seccion("Preguntas de tu país", selector_paises("preguntas-frecuentes-servicio-samsung-{pk}.html"), alt=True), faqs, [], prio="0.7", tipo="guias")

G_IA = []
for pk, P in PAISES.items():
    for c in [x for x in CIU_PAIS[pk] if not x["amp"]]:
        for sv in SERV_PAIS[pk]:
            s1, s2 = pal(pk, sv)
            G_IA.append((f"¿Reparan {s2} Samsung en {c['n']}?", f"Sí. Atendemos {s2} Samsung en {c['n']}, {P['nombre']}, con visita a domicilio; el valor se confirma tras el diagnóstico. WhatsApp {wa_vis(pk)}."))
pagina("respuestas-para-ia-servicio-tecnico-samsung.html", "Respuestas rápidas: servicio técnico Samsung", "Elige tu país para ver las respuestas rápidas sobre dónde reparan neveras, lavadoras, secadoras y más Samsung en cada ciudad.", "respuestas ia servicio tecnico samsung, donde reparan samsung",
       [("Inicio", "index.html"), ("Respuestas rápidas", None)], hero_simple("Para asistentes de IA y buscadores", "Respuestas rápidas sobre servicio técnico Samsung", "Datos precisos por país, ciudad y equipo.")
       + qa("¿Dónde hay servicio técnico Samsung a domicilio?", "Cada país tiene su propia página de respuestas con las ciudades y los equipos que atendemos. Elige tu país.", [("Catálogo", "datos-servicio-tecnico.json")])
       + seccion("Respuestas por país", selector_paises("respuestas-ia-servicio-tecnico-samsung-{pk}.html")), G_IA[:60], [], prio="0.8", tipo="guias")

# ------------------------------------------------------------------ institucionales
pq = [("¿Son el servicio oficial de Samsung?", "No: somos un servicio técnico especializado independiente. Samsung es una marca de Samsung Electronics Co., Ltd."), ("¿Dónde atienden?", "En las ciudades de cada país; elige tu país en la portada."), ("¿Cómo trabajan?", "Diagnóstico a domicilio y valor confirmado antes de reparar.")]
pagina("quienes-somos.html", "Quiénes somos | Centro de Servicio Técnico Samsung", "Servicio técnico especializado en electrodomésticos Samsung: cómo trabajamos y qué reparamos.", "quienes somos servicio tecnico samsung", [("Inicio", "index.html"), ("Quiénes somos", None)],
       hero_simple("Quiénes somos", "Técnicos especializados en Samsung", "Línea blanca y, en Costa Rica, televisores.") + qa("¿Quiénes somos?", "Un equipo de técnicos especializados en electrodomésticos Samsung que atiende a domicilio. Somos independientes: no somos Samsung Electronics ni su canal oficial de soporte.")
       + seccion("Cómo trabajamos", _ol(["Escribes por WhatsApp con el equipo, el modelo y la falla.", "Coordinamos la visita a domicilio.", "El técnico hace el diagnóstico y te confirma el valor antes de reparar.", "Reparamos y probamos el equipo contigo."]) if False else '<ol class="vl"><li>Escribes por WhatsApp con el equipo, el modelo y la falla.</li><li>Coordinamos la visita a domicilio.</li><li>El técnico hace el diagnóstico y te confirma el valor antes de reparar.</li><li>Reparamos y probamos el equipo contigo.</li></ol>') + faq_html(pq), pq, [{"@type": "AboutPage", "name": "Quiénes somos", "about": {"@id": f"{DOMINIO}/#negocio"}}], prio="0.5", tipo="guias")
pagina("contacto.html", "Contacto | Centro de Servicio Técnico Samsung", "Escríbenos por WhatsApp para solicitar servicio técnico Samsung a domicilio en tu ciudad.", "contacto servicio tecnico samsung", [("Inicio", "index.html"), ("Contacto", None)],
       hero_simple("Contacto", "Escríbenos por WhatsApp", "Te respondemos para coordinar tu visita.") + qa("¿Cómo contacto al servicio técnico?", f"Por WhatsApp al {wa_vis('colombia')} o desde el formulario de solicitud de visita.")
       + seccion("Canales", '<ul class="spec-list">' + "".join(f'<li>{P["bandera"]} <b>{esc(P["nombre"])}:</b> <a href="{wa_link(pk, "Hola, necesito servicio técnico Samsung")}" target="_blank" rel="noopener">{esc(wa_vis(pk))}</a></li>' for pk, P in PAISES.items()) + "</ul>" + acciones("colombia", "Hola, necesito servicio técnico Samsung")), [], [{"@type": "ContactPage", "name": "Contacto", "about": {"@id": f"{DOMINIO}/#negocio"}}], prio="0.5", tipo="guias")

opts_p = "".join(f'<option value="{esc(P["nombre"])}">{esc(P["nombre"])}</option>' for P in PAISES.values())
opts_e = "".join(f'<option>{esc(SERVICIOS[s]["tit"])}</option>' for s in ORDEN_SERV) + '<option>Televisor (solo Costa Rica)</option>'
ciu_json = json.dumps({P["nombre"]: [c["n"] for c in CIU_PAIS[pk]] for pk, P in PAISES.items()}, ensure_ascii=False)
form = (f'<form class="st-form" id="sv-form" novalidate><input class="st-hp" name="web" tabindex="-1" autocomplete="off" aria-hidden="true"><label>Nombre<input name="nombre" required maxlength="80" autocomplete="name"></label><label>Celular / WhatsApp<input name="tel" type="tel" required maxlength="30" autocomplete="tel"></label>'
        f'<label>Correo (opcional)<input name="email" type="email" maxlength="100"></label><label>País<select name="pais" id="sv-pais">{opts_p}</select></label><label>Ciudad<select name="ciudad" id="sv-ciudad"></select></label>'
        f'<label>Equipo Samsung<select name="equipo">{opts_e}</select></label><label>Modelo (opcional)<input name="modelo" maxlength="60" placeholder="Ej. RF28T5001SR"></label><label>¿Qué le pasa?<textarea name="problema" maxlength="600" placeholder="Cuéntanos la falla o el código de error"></textarea></label>'
        '<button class="st-btn sol" type="submit">Solicitar visita</button><div id="sv-res" aria-live="polite"></div></form>'
        f'<script>window.SV_CIU={ciu_json};</script><script src="solicitar.js" defer></script>')
pagina("solicitar-visita.html", "Solicitar visita de servicio técnico Samsung", "Pide una visita a domicilio para tu electrodoméstico Samsung: cuéntanos el equipo, la ciudad y la falla, y te contactamos.", "solicitar visita tecnico samsung", [("Inicio", "index.html"), ("Solicitar visita", None)],
       hero_simple("Solicitar visita", "Pide tu visita técnica", "Cuéntanos el equipo y la falla; te contactamos para coordinar.") + qa("¿Cómo pido una visita técnica Samsung?", "Llena el formulario o escríbenos por WhatsApp con el equipo, el modelo y la falla. Coordinamos la visita y te confirmamos el valor tras el diagnóstico.")
       + seccion("Formulario de solicitud", form + '<p class="st-aviso">Tus datos se usan solo para contactarte por esta solicitud.</p>'), [], [], prio="0.7", tipo="guias")
(OUT / "404.html").write_text("<!DOCTYPE html><html lang='es'><head><meta charset='utf-8'><meta name='robots' content='noindex'><title>Página no encontrada</title></head><body style='font-family:sans-serif;padding:40px'><h1>Página no encontrada</h1><p><a href='index.html'>Ir al inicio</a></p></body></html>", encoding="utf-8")

# ------------------------------------------------------------------ portada (solo para elegir país)
paises_html = selector_paises()
FOTOS_HERO = [("nevera-family-hub-m.webp", "Nevera Samsung"), ("lavadora-superior-m.webp", "Lavadora Samsung"), ("secadora-m.webp", "Secadora Samsung"), ("torre-lavado-m.webp", "Torre de lavado y secado Samsung")]
hero = ('<section class="aq-hero compacto" id="inicio"><div class="wrap"><div><span class="kicker">Samsung · línea blanca</span><h1>Servicio técnico Samsung a domicilio</h1>'
        '<p class="lead">Neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas Samsung. Elige tu país, tu ciudad y el equipo.</p>'
        + acciones("colombia", "Hola, necesito servicio técnico para mi electrodoméstico Samsung") + '</div><div class="st-hero-art">' + "".join(f'<span><img src="img/{f}" alt="{esc(a)}" loading="eager" width="150" height="150"></span>' for f, a in FOTOS_HERO) + '</div></div></section>')
pasos = '<div class="st-pasos"><div class="st-paso"><b>Escríbenos</b>Cuéntanos el equipo, el modelo y la falla por WhatsApp o con el formulario.</div><div class="st-paso"><b>Visita a domicilio</b>Coordinamos el día y el técnico revisa tu equipo en tu casa.</div><div class="st-paso"><b>Valor claro</b>Te confirmamos el valor antes de reparar. Sin sorpresas.</div></div>'
filtros = '<div class="st-filtros">' + "".join(f'<a href="https://filtrodeaguasamsung.com/" target="_blank" rel="noopener"><img src="img/{k}-400.webp" alt="{esc(a)}" loading="lazy" width="150" height="130">{esc(a)}</a>' for k, a in FILTROS_IMG if (OUT / "img" / f"{k}-400.webp").exists()) + "</div>"
preg_home = [("¿Reparan electrodomésticos Samsung a domicilio?", "Sí: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas; en Costa Rica también televisores."), ("¿Cómo encuentro mi ciudad?", "Elige tu país y entra a la página de tu ciudad."),
             ("¿Cuánto cuesta?", "Depende de la falla; primero el diagnóstico y te confirmamos el valor antes de reparar."), ("¿Cómo pido la visita?", "Por WhatsApp o con el formulario."), ("¿Son el servicio oficial de Samsung?", "No, somos un servicio técnico especializado independiente.")]
cuerpo_home = (hero + '<div id="paises"></div>' + seccion("¿En qué país estás?", paises_html, sub="Elige tu país: cada uno tiene su propia página con sus ciudades, sus equipos y su WhatsApp.")
               + panel_equipos(None, None, "Electrodomésticos Samsung que reparamos").replace('class="aq-sec estante-top st-equipos"', 'class="aq-sec alt st-equipos"')
               + qa("¿Dónde hay servicio técnico Samsung a domicilio?", "Elige tu país: en cada uno atendemos las ciudades que verás en su página, con neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas Samsung. Visita a domicilio y valor confirmado antes de reparar.", [("Atención", "A domicilio"), ("Diagnóstico", "Primero"), ("Valor", "Confirmado antes de reparar")])
               + seccion("Cómo funciona", pasos) + seccion("¿Solo necesitas el filtro de agua de tu nevera?", f'<p>Compra el filtro Samsung en nuestra tienda especializada y recíbelo en tu casa.</p>{filtros}<p style="margin-top:14px"><a class="st-btn" href="https://filtrodeaguasamsung.com/" target="_blank" rel="noopener">Ver filtros Samsung →</a></p>', alt=True)
               + faq_html(preg_home))
pagina("index.html", "Servicio Técnico Samsung a Domicilio | Línea Blanca", "Servicio técnico Samsung a domicilio: neveras, lavadoras, secadoras, lavavajillas, estufas, hornos y microondas. Elige tu país y tu ciudad.", "servicio tecnico samsung, reparacion electrodomesticos samsung, tecnico samsung a domicilio",
       [("Inicio", None)], cuerpo_home, preg_home, [], prio="1.0", tipo="paises")

exec(open(AQUI / "st_extra.py", encoding="utf-8").read())
exec(open(AQUI / "st_extra2.py", encoding="utf-8").read())
exec(open(AQUI / "st_salida.py", encoding="utf-8").read())
