# Secciones de contacto por ubicación: «WhatsApp del servicio técnico Samsung en…» y «Teléfono del servicio técnico Samsung en…» (ciudad y país).
CONT_P = []  # (pk, c|None, tipo, url)
INTRO_WA = ["Si buscas el WhatsApp del servicio técnico Samsung en {l}, es {n}. Escribe ahí y coordinamos la visita a domicilio.",
            "El número de WhatsApp para pedir servicio técnico Samsung en {l} es {n}. Te respondemos para agendar la visita y confirmar el valor tras el diagnóstico.",
            "Para servicio técnico Samsung en {l}, escribe al WhatsApp {n}: cuéntanos el equipo, el modelo y la falla.",
            "¿Necesitas un técnico Samsung en {l}? El WhatsApp de atención es {n}. La visita es a domicilio y el valor se confirma antes de reparar."]
INTRO_TEL = ["El teléfono de contacto del servicio técnico Samsung en {l} es {n}. La forma más rápida de atención es WhatsApp en ese mismo número.",
             "Para hablar con el servicio técnico Samsung en {l}, el número es {n}. También puedes escribirnos por WhatsApp y te respondemos para coordinar la visita.",
             "Número de servicio técnico Samsung en {l}: {n}. Atendemos a domicilio; primero el diagnóstico y el valor se confirma antes de reparar.",
             "Si prefieres llamar, el número del servicio técnico Samsung en {l} es {n}. Si no contestamos, escríbenos por WhatsApp."]
ENVIAR = ["El tipo de equipo (nevera, lavadora, secadora, lavavajillas, estufa, horno, microondas).", "El modelo, que está en una etiqueta del equipo.", "La falla o el código de error que muestra.", "Tu barrio o zona dentro de la ciudad.", "Una foto de la etiqueta o del problema, si puedes.", "El mejor horario para la visita."]


def _contacto(pk, c, tipo):
    P = PAISES[pk]; l = c["n"] if c else P["nombre"]; n = wa_vis(pk); es_wa = tipo == "wa"
    key = f"ct|{tipo}|{pk}|{c['s'] if c else ''}"
    f = dict(l=l, n=n)
    intro = uno(key + "|i", INTRO_WA if es_wa else INTRO_TEL).format(**f)
    tit = f"WhatsApp del servicio técnico Samsung en {l}" if es_wa else f"Teléfono del servicio técnico Samsung en {l}"
    h1 = f"WhatsApp servicio técnico Samsung en {l}" if es_wa else f"Teléfono de servicio técnico Samsung en {l}"
    q = f"¿Cuál es el WhatsApp del servicio técnico Samsung en {l}?" if es_wa else f"¿Cuál es el teléfono del servicio técnico Samsung en {l}?"
    msg = f"Hola, necesito servicio técnico Samsung en {l}"
    eq = ", ".join(pal(pk, s_)[1] for s_ in SERV_PAIS[pk])
    zonas = (c["zonas"][:6] if c else [])
    tel = "+" + wa_num(pk)
    botones = f'<div class="st-acc"><a class="st-btn wa" href="{wa_link(pk, msg)}" target="_blank" rel="noopener">{ICO["wa"]} Escribir por WhatsApp</a>' + ("" if es_wa else f'<a class="st-btn sol" href="tel:{tel}">Llamar {esc(n)}</a>') + f'<a class="st-btn" href="{R_SOL(pk)}">Solicitar visita</a></div>'
    preg = [(q, f"{intro}"), (f"¿Atienden por WhatsApp en {l}?", f"Sí: el número {n} recibe mensajes de WhatsApp para pedir servicio técnico Samsung en {l}."),
            (f"¿Qué equipos Samsung reparan en {l}?", eq.capitalize() + ", a domicilio."), (f"¿Cuánto cuesta la visita en {l}?", "Depende de la falla y del repuesto; el técnico hace el diagnóstico y el valor se confirma antes de reparar."),
            ("¿Qué datos debo enviar?", "Equipo, modelo, falla o código de error, zona y, si puedes, una foto de la etiqueta.")]
    if c:
        preg += preguntas_ia(c, key, 2)
    enlaces = ('<div class="city-tags">' + (f'<a href="{R_CIU(c)}">Servicio técnico Samsung en {esc(l)}</a>' + "".join(f'<a href="{R_CS(c, s_)}">{esc(cap(pal(pk, s_)[1]))} en {esc(l)}</a>' for s_ in SERV_PAIS[pk]) + "".join(zlink(c, z, z) for z in zonas)
               if c else f'<a href="{R_PAIS(pk)}">Servicio técnico Samsung en {esc(P["nombre"])}</a>' + "".join(f'<a href="{R_CIU(x)}">{esc(x["n"])}</a>' for x in CIU_PAIS[pk])) + "</div>")
    otro = (R_TEL(c) if c else R_TELP(pk)) if es_wa else (R_WA(c) if c else R_WAP(pk))
    cuerpo = (hero_simple(f"{P['bandera']} {l}", h1, f"{n} · atención a domicilio en {l}.", botones)
              + qa(q, esc(intro), [("WhatsApp" if es_wa else "Teléfono", n), ("Ubicación", f"{l}, {P['nombre']}"), ("Atención", "A domicilio")])
              + seccion(f"Qué enviar por WhatsApp para pedir tu visita en {esc(l)}", _ul2(mix(key + "|e", ENVIAR, 4)) + f"<p>Con esos datos coordinamos la visita y el técnico llega a tu casa o apartamento en {esc(l)}.</p>")
              + seccion("Servicio técnico Samsung cerca de ti", enlaces, alt=True)
              + seccion("Otro canal", f'<p><a href="{otro}">{"Teléfono" if es_wa else "WhatsApp"} del servicio técnico Samsung en {esc(l)}</a></p>')
              + faq_html(preg, f"Preguntas sobre el contacto en {l}"))
    nombre = (R_WA(c) if c else R_WAP(pk)) if es_wa else (R_TEL(c) if c else R_TELP(pk))
    miga = [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk))] + ([(l, R_CIU(c))] if c else []) + [("WhatsApp" if es_wa else "Teléfono", None)]
    pagina(nombre, f"{tit} | {n}", f"{'WhatsApp' if es_wa else 'Teléfono'} del servicio técnico Samsung en {l}, {P['nombre']}: {n}. Visita a domicilio para {eq}; valor confirmado antes de reparar.", f"{'whatsapp' if es_wa else 'telefono'} servicio tecnico samsung {l.lower()}, numero servicio tecnico samsung {l.lower()}",
           miga, cuerpo, preg, [], prio="0.8", pk=pk, tipo="ciudades" if c else "paises", ctx=c, compacto=True)
    CONT_P.append((pk, c, tipo, nombre, h1))


for _pk in PAISES:
    for _t in ("wa", "tel"):
        _contacto(_pk, None, _t)
for _c in CIU:
    for _t in ("wa", "tel"):
        _contacto(_c["pk"], _c, _t)
# enlaces desde la ciudad y el país
for _c in CIU:
    _ins(R_CIU(_c), seccion(f"Contacto del servicio técnico Samsung en {esc(_c['n'])}", f'<div class="city-tags"><a href="{R_WA(_c)}">WhatsApp en {esc(_c["n"])}: {esc(wa_vis(_c["pk"]))}</a><a href="{R_TEL(_c)}">Teléfono en {esc(_c["n"])}</a></div>'))
for _pk, _P in PAISES.items():
    _ins(R_PAIS(_pk), seccion(f"Contacto del servicio técnico Samsung en {esc(_P['nombre'])}", f'<div class="city-tags"><a href="{R_WAP(_pk)}">WhatsApp en {esc(_P["nombre"])}: {esc(wa_vis(_pk))}</a><a href="{R_TELP(_pk)}">Teléfono en {esc(_P["nombre"])}</a></div>'))
