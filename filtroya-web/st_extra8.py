# Sitio de una sola ciudad: páginas por término de búsqueda (mantenimiento, instalación, repuestos, garantía…) y fallas principales por barrio.
if SOLO:
    _c = CIU[0]; _pk = _c["pk"]; _P = PAISES[_pk]; _nom = _c["n"]; _wa = wa_vis(_pk)
    TERMS = [
        ("mantenimiento", "Mantenimiento de {s2} Samsung en {c}", "¿Cada cuánto hacer mantenimiento a una {s1} Samsung en {c}?", "Una revisión preventiva al año y limpieza periódica de filtros y partes que acumulan polvo, grasa o sarro mantienen la {s1} Samsung funcionando bien y evitan fallas mayores."),
        ("instalacion", "Instalación de {s2} Samsung en {c}", "¿Quién instala una {s1} Samsung en {c}?", "Coordinamos la revisión de la conexión, la nivelación y la puesta en marcha de tu {s1} Samsung en {c}; las conexiones de gas o eléctricas especiales las debe hacer un instalador competente."),
        ("tecnico-a-domicilio", "Técnico de {s2} Samsung a domicilio en {c}", "¿Hay técnico de {s2} Samsung a domicilio en {c}?", "Sí: un técnico va a tu casa en {c}, diagnostica la {s1} Samsung y te confirma el valor antes de reparar."),
        ("cerca-de-mi", "Técnico de {s2} Samsung cerca de mí en {c}", "¿Dónde hay un técnico de {s2} Samsung cerca de mí en {c}?", "Atendemos {c} con visita a domicilio: escribe tu barrio por WhatsApp y coordinamos la visita para tu {s1} Samsung."),
        ("repuestos", "Repuestos para {s2} Samsung en {c}", "¿Dónde conseguir repuestos para una {s1} Samsung en {c}?", "El técnico identifica la pieza que falla en el diagnóstico y te indica su disponibilidad y valor antes de cambiarla; no se cambia nada sin tu aprobación."),
        ("garantia", "Garantía de {s2} Samsung en {c}: qué hacer", "¿Qué hacer si mi {s1} Samsung tiene garantía en {c}?", "Revisa las condiciones de la garantía en el manual y con la tienda donde compraste; somos un servicio técnico independiente y atendemos equipos dentro y fuera de garantía."),
        ("diagnostico", "Diagnóstico de {s2} Samsung en {c}", "¿Cómo es el diagnóstico de una {s1} Samsung en {c}?", "El técnico revisa el equipo en tu casa, encuentra la causa de la falla, te la explica y te confirma el valor de la reparación antes de empezar."),
        ("como-elegir-tecnico", "Cómo elegir un buen técnico de {s2} Samsung en {c}", "¿Cómo elijo un buen técnico para mi {s1} Samsung en {c}?", "Elige un técnico que haga el diagnóstico primero, confirme el valor antes de reparar, te explique la falla con claridad y te oriente con honestidad."),
    ]
    R_TERM = lambda t, sv: f"{_pk}/{_c['d']}/{t}-{slug(pal(_pk, sv)[1])}/index.html"
    TERM_BLOQUE = {
        "mantenimiento": lambda s1, s2, k: ["Limpieza de las partes que acumulan polvo, grasa o sarro.", "Revisión de sellos, mangueras y conexiones.", "Prueba de funcionamiento en un ciclo completo.", "Revisión de la nivelación y de la ventilación.", "Recomendaciones de uso según el clima de la ciudad.", "Aviso de partes con desgaste antes de que fallen."],
        "instalacion": lambda s1, s2, k: ["Revisión del lugar donde va el equipo (espacio, ventilación, nivel).", "Verificación de la toma eléctrica y del polo a tierra.", "Conexión de mangueras o ductos según el equipo.", "Nivelación y prueba de funcionamiento.", "Instrucciones básicas de uso y cuidado.", "Si requiere gas o instalaciones especiales, te orientamos para que lo haga un instalador competente."],
        "tecnico-a-domicilio": lambda s1, s2, k: ["Visita en tu casa o apartamento, sin llevar el equipo a un taller.", "Diagnóstico en el lugar con herramientas de medición.", "Valor confirmado antes de reparar.", "Reparación en la misma visita cuando el repuesto está disponible.", "Prueba del equipo contigo al terminar.", "Atención por WhatsApp para coordinar horario."],
        "cerca-de-mi": lambda s1, s2, k: ["Escríbenos tu barrio y coordinamos la visita.", "Atendemos toda la ciudad con visita a domicilio.", "Sin que tengas que mover el equipo.", "El técnico llega con herramientas de diagnóstico.", "Valor confirmado antes de reparar.", "Respuesta por WhatsApp para agendar."],
        "repuestos": lambda s1, s2, k: ["El técnico identifica la pieza que falla en el diagnóstico.", "Te informa la disponibilidad del repuesto y su valor.", "No se cambia nada sin tu aprobación.", "Si la pieza no está en el momento, se coordina su consecución.", "Se prueba el equipo después del cambio.", "Te explicamos cómo prolongar la vida de la pieza nueva."],
        "garantia": lambda s1, s2, k: ["Revisa la fecha de compra y la factura.", "Lee las condiciones de la garantía en el manual.", "La garantía de fábrica la gestiona Samsung o la tienda.", "Fuera de garantía, atendemos con diagnóstico y valor confirmado.", "Si intervienen terceros, la garantía puede cambiar: consúltalo antes.", "Guarda la factura y el modelo del equipo."],
        "diagnostico": lambda s1, s2, k: ["Lectura de códigos de error y revisión visual.", "Pruebas de funcionamiento de las partes principales.", "Medición eléctrica donde aplica.", "Explicación de la causa de la falla.", "Opciones: reparar, cambiar la pieza o reemplazar el equipo.", "Valor confirmado antes de reparar."],
        "como-elegir-tecnico": lambda s1, s2, k: ["Que haga el diagnóstico antes de reparar.", "Que te confirme el valor antes de empezar.", "Que te explique la falla con claridad.", "Que te diga con honestidad si conviene reparar o cambiar.", "Que pruebe el equipo contigo al terminar.", "Que atienda por un canal claro, como WhatsApp."],
    }
    for _sv in SERV_PAIS[_pk]:
        _s1, _s2 = pal(_pk, _sv); S = SERVICIOS[_sv]
        for (t, h1t, qq, aa) in TERMS:
            k = f"tm|{t}|{_sv}"; f_ = dict(s1=_s1, s2=_s2, c=_nom)
            tit = h1t.format(**f_)
            preg = [(qq.format(**f_), aa.format(**f_)), (f"¿Atienden toda la ciudad de {_nom}?", f"Sí, atendemos {_nom} con visita a domicilio: {', '.join(_c['zonas'][:8])} y más barrios."),
                    (f"¿Cuánto cuesta el servicio de {_s2} Samsung en {_nom}?", "Depende de la falla, del repuesto y del equipo; el técnico diagnostica y el valor se confirma antes de reparar."),
                    ("¿Cómo contacto al técnico?", f"Por WhatsApp al {_wa}: envía el modelo, la falla y tu barrio.")] + preguntas_ia(_c, k, 2)
            secs_t = [seccion(f"{esc(_nom)}: clima y {esc(_s1)}", f"<p>{esc(parrafo_clima(_c, _c['zonas'][0], _sv, k + '|cl'))}</p><p>{esc(uno(k + '|tip', TIPS[_sv]))}</p>"), bloque_mitos(k, [_sv], 1),
                      seccion(f"Fallas frecuentes de {esc(_s2)} Samsung", _ul2(mix(k + "|sn", S["sintomas"], 4)) + f"<p>{esc(efecto_de(_c, _sv))}.</p>", alt=True),
                      seccion(f"Cuidados para tu {esc(_s1)} Samsung en {esc(_nom)}", _cuidado(_c, _sv, k, 2)),
                      seccion(f"Glosario: partes de tu {esc(_s1)} Samsung", _glos(_sv, k, 3), alt=True),
                      seccion("Cómo funciona la visita", _como(_c, k)),
                      seccion(f"{esc(cap(_s2))} Samsung por barrio en {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_ZS(_c, z, _sv)}">{esc(z)}</a>' for z in mix(k + "|b", _c["zonas"], 8)) + f'<a href="{R_CS(_c, _sv)}"><b>{esc(cap(_s2))} Samsung en {esc(_nom)} →</b></a></div>', alt=True),
                      seccion(f"Más sobre {esc(_s2)} Samsung en {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_TERM(t2, _sv)}">{esc(h2.format(**f_))}</a>' for (t2, h2, *_r) in TERMS if t2 != t) + "</div>")]
            kt = sorted(mix(k + "|kt", list(range(len(secs_t))), 5))
            cuerpo = (hero_simple(f"{_nom} · {_c['dep']}", tit, f"{cap(_s2)} Samsung en {_nom}: visita a domicilio, diagnóstico primero y valor confirmado antes de reparar.", acciones(_pk, f"Hola, necesito {t.replace('-', ' ')} para mi {_s1} Samsung en {_nom}"))
                      + qa(qq.format(**f_), esc(aa.format(**f_)), [("Equipo", cap(_s2) + " Samsung"), ("Ciudad", _nom), ("WhatsApp", _wa), ("Atención", "A domicilio")])
                      + seccion(f"Qué incluye en {esc(_nom)}", _ul2(mix(k + "|tb", TERM_BLOQUE[t](_s1, _s2, k), 3)))
                      + "".join(secs_t[i_] for i_ in kt)
                      + faq_html(preg, f"Preguntas: {t.replace('-', ' ')} de {_s2} Samsung en {_nom}"))
            SOLO_EXTRA.append((tit, R_TERM(t, _sv), 'Servicio'))
            pagina(R_TERM(t, _sv), tit, f"{tit}: visita a domicilio, diagnóstico primero y valor confirmado antes de reparar. WhatsApp {_wa}.", f"{t.replace('-', ' ')} {_s1} samsung {_nom.lower()}, {_s1} samsung {_nom.lower()}",
                   [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), (cap(_s2), R_CS(_c, _sv)), (tit, None)], cuerpo, preg, [], prio="0.7", pk=_pk, tipo="ciudades", ctx=_c, compacto=True)
        _ins(R_CS(_c, _sv), seccion(f"Todo sobre {esc(_s2)} Samsung en {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_TERM(t2, _sv)}">{esc(h2.format(s1=_s1, s2=_s2, c=_nom))}</a>' for (t2, h2, *_r) in TERMS) + "</div>", alt=True))
    # fallas principales por barrio
    FB = {"nevera": ["no-enfria", "con-escarcha"], "lava": ["no-desagua", "no-centrifuga"], "seca": ["no-seca"], "lavaplatos": ["no-lava-bien"], "cocina": ["horno-no-calienta"], "micro": ["no-calienta"]}
    R_FB = lambda z, pr: f"{_pk}/{_c['d']}/{slug(z)}/{slug(pal(_pk, pr['sv'])[0])}-{pr['sl']}/index.html"
    _pr_idx = {(pr["sv"], pr["sl"]): pr for _cc, pr in PROB_P}
    for _z in _c["zonas"]:
        for sv_, sls in FB.items():
            for sl_ in sls:
                pr = _pr_idx.get((sv_, sl_))
                if not pr:
                    continue
                s1, s2 = pal(_pk, sv_); S = SERVICIOS[sv_]; k = f"fb|{_z}|{sv_}|{sl_}"; f_ = dict(S=cap(s1), s=s1, c=_nom)
                tt = pr["tit"].format(**f_).replace(f" en {_nom}", f" en {_z}, {_nom}")
                caus = mix(k + "|c", pr["causas"], 3); pasos = [x.format(s=s1) for x in mix(k + "|p", pr["pasos"], 3)]
                preg = [(f"¿Reparan {s2} Samsung en {_z}?", f"Sí, atendemos {_z} y toda {_nom} con visita a domicilio. WhatsApp {_wa}."), (f"¿Cuánto cuesta reparar esta falla en {_z}?", "Depende de la falla y del repuesto; el valor se confirma después del diagnóstico y antes de reparar.")] + preguntas_ia(_c, k, 3)
                n2_ = mix(k + "|n", [zz for zz in _c["zonas"] if zz != _z], 2)
                bp_ = uno(k + "|bp", ["Atendemos {z} con visita a domicilio; también pasamos por {a} y {b}.", "Si estás en {z}, escribe al WhatsApp y confirmamos el día de la visita para tu {s}.", "En {z} el diagnóstico se hace en tu casa y el valor se confirma antes de reparar; cubrimos además {a} y {b}.", "{z}, {a} y {b} están dentro de nuestra ruta de visitas en {c}."]).format(z=_z, a=n2_[0], b=n2_[1], s=s1, c=_nom)
                cuerpo = (hero_simple(f"{_z} · {_nom}", tt, f"Causas, qué revisar y técnico a domicilio en {_z}.", acciones(_pk, f"Hola, mi {s1} Samsung falla ({pr['sl'].replace('-', ' ')}) en {_z}, {_nom}"))
                          + qa(pr["q"].format(**f_).replace(f" en {_nom}", f" en {_z}, {_nom}"), esc(pr["res"]) + f" En {esc(_z)} ({esc(_nom)}), {esc(efecto_de(_c, sv_))}.", [("Barrio", _z), ("Equipo", cap(s1) + " Samsung"), ("WhatsApp", _wa)])
                          + seccion(f"Atención en {esc(_z)}", f"<p>{esc(bp_)}</p>") + seccion(f"{esc(_z)}: clima y {esc(s1)}", f"<p>{esc(parrafo_clima(_c, _z, sv_, k + '|cl'))}</p><p>{esc(uno(k + '|tip', TIPS[sv_]))}</p>") + bloque_mitos(k, [sv_], 1) + seccion("Causas más comunes", _ul2(caus)) + seccion("Qué revisar primero", '<ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in pasos) + "</ol>", alt=True)
                          + (seccion(f"Qué incluye la visita en {esc(_z)}", _ul2(mix(k + "|v", VISITA_E[sv_], 3))) if len(k) % 2 else "")
                          + seccion("Más información", '<div class="city-tags">' + f'<a href="{R_PROB(_c, pr)}">{esc(pr["tit"].format(**f_))}</a><a href="{R_ZS(_c, _z, sv_)}">{esc(cap(s2))} Samsung en {esc(_z)}</a><a href="{R_Z(_c, _z)}">Servicio técnico Samsung en {esc(_z)}</a><a href="{R_CS(_c, sv_)}">{esc(cap(s2))} Samsung en {esc(_nom)}</a></div>', alt=True)
                          + faq_html(preg))
                SOLO_EXTRA.append((tt, R_FB(_z, pr), 'Falla por barrio'))
                pagina(R_FB(_z, pr), tt, f"{tt}: causas, qué revisar y técnico Samsung a domicilio en {_z}. Valor confirmado antes de reparar.", f"{s1} samsung {pr['sl'].replace('-', ' ')} {_z.lower()} {_nom.lower()}",
                       [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), (_z, R_Z(_c, _z)), (tt, None)], cuerpo, preg, [], prio="0.6", pk=_pk, tipo="ciudades", ctx=_c, compacto=True)
