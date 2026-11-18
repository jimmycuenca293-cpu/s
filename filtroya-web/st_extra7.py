# Sitio de una sola ciudad: páginas de barrio por equipo, portada de barrios y guía local (solo con ST_SOLO).
if SOLO:
    LINEAS_P.clear()
    _c = CIU[0]; _pk = _c["pk"]; _P = PAISES[_pk]; _nom = _c["n"]; _cl = CLIMA[_c["s"]]
    TIT_ZS = ["Técnico de {s2} Samsung en {z}, {c} | A domicilio", "Reparación de {s2} Samsung en {z} ({c})", "{z}: servicio técnico de {s2} Samsung en {c}", "Arreglo de {s2} Samsung en {z}, {c}", "Técnico de {s1} Samsung a domicilio en {z} ({c})"]
    INTRO_ZS = ["Si vives en {z} y tu {s1} Samsung falló, el técnico llega a tu casa o apartamento en {c}: coordinas por WhatsApp y el diagnóstico se hace en el lugar.",
                "Atendemos {s2} Samsung en {z}, {c}, sin que tengas que mover el equipo. Primero se diagnostica y el valor se confirma antes de reparar.",
                "¿Tu {s1} Samsung en {z} no funciona como antes? Un técnico va a {z}, revisa el equipo y te explica qué falla y qué opciones tienes.",
                "En {z} ({c}) reparamos y damos mantenimiento a {s2} Samsung a domicilio. Escribe al WhatsApp con el modelo y la falla y coordinamos la visita."]
    for _z in _c["zonas"]:
        for _sv in SERV_PAIS[_pk]:
            _s1, _s2 = pal(_pk, _sv); S = SERVICIOS[_sv]; k = f"zs|{_z}|{_sv}"
            f_ = dict(s1=_s1, s2=_s2, z=_z, c=_nom)
            tit = uno(k + "|t", TIT_ZS).format(**f_)
            wa = wa_vis(_pk)
            otros = [zz for zz in _c["zonas"] if zz != _z]
            preg = [(f"¿Hay técnico de {_s2} Samsung en {_z}?", f"Sí, atendemos {_s2} Samsung a domicilio en {_z}, {_nom}. Escribe al {wa} y coordinamos la visita."),
                    (f"¿Cuánto cuesta reparar una {_s1} Samsung en {_z}?", "Depende de la falla y del repuesto; el técnico hace el diagnóstico y el valor se confirma antes de reparar."),
                    (f"¿Cuánto demora llegar a {_z}?", "La visita se coordina por WhatsApp según tu disponibilidad y la agenda del día."),
                    ] + preguntas_ia(_c, k, 3)
            cuerpo = (hero_simple(f"{_z} · {_nom}", tit.split(" | ")[0], f"Servicio técnico de {_s2} Samsung a domicilio en {_z}, {_nom}, {_c['dep']}.", acciones(_pk, f"Hola, necesito técnico para mi {_s1} Samsung en {_z}, {_nom}"))
                      + qa(f"¿Hay técnico de {_s2} Samsung en {_z}, {_nom}?", f"Sí. {esc(uno(k + '|i', INTRO_ZS).format(**f_))} WhatsApp {esc(wa)}.", [("Barrio", _z), ("Ciudad", _nom), ("Equipo", cap(_s2) + " Samsung"), ("WhatsApp", wa)])
                      + seccion(f"Fallas que atendemos en {esc(_z)}", _ul2(S["sintomas"][:6]) + f"<p>{esc(parrafo_clima(_c, _z, _sv, k + '|cl'))}</p>")
                      + seccion(f"Qué incluye la visita en {esc(_z)}", _ul2(mix(k + "|v", VISITA_E[_sv], 5)), alt=True)
                      + seccion(f"Cuidados para tu {esc(_s1)} Samsung en {esc(_nom)}", _cuidado(_c, _sv, k))
                      + seccion(f"Glosario: partes de tu {esc(_s1)} Samsung", _glos(_sv, k), alt=True)
                      + seccion(f"{esc(cap(_s2))} Samsung en otros barrios de {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_ZS(_c, zz, _sv)}">{esc(zz)}</a>' for zz in mix(k + "|o", otros, 10)) + f'<a href="{R_CS(_c, _sv)}"><b>{esc(cap(_s2))} Samsung en {esc(_nom)} →</b></a></div>')
                      + seccion(f"Otros equipos Samsung en {esc(_z)}", '<div class="city-tags">' + "".join(f'<a href="{R_ZS(_c, _z, s_)}">{esc(cap(pal(_pk, s_)[1]))}</a>' for s_ in SERV_PAIS[_pk] if s_ != _sv) + f'<a href="{R_Z(_c, _z)}">Servicio técnico Samsung en {esc(_z)}</a></div>', alt=True)
                      + faq_html(preg, f"Preguntas sobre {_s2} Samsung en {_z}"))
            pagina(R_ZS(_c, _z, _sv), tit, f"{cap(_s2)} Samsung en {_z}, {_nom}: técnico a domicilio, diagnóstico primero y valor confirmado antes de reparar. WhatsApp {wa}.", f"tecnico {_s1} samsung {_z.lower()} {_nom.lower()}, reparacion {_s2} samsung {_z.lower()}",
                   [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), (_z, R_Z(_c, _z)), (cap(_s2), None)], cuerpo, preg, [{"@type": "Service", "name": f"Reparación de {_s2} Samsung en {_z}, {_nom}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "Place", "name": f"{_z}, {_nom}"}}],
                   prio="0.7", pk=_pk, tipo="zonas", ctx=_c, compacto=True)
    # portada de barrios
    _tags = '<div class="city-tags">' + "".join(f'<a href="{R_Z(_c, z)}">{esc(z)}</a>' for z in _c["zonas"]) + "</div>"
    _tabla = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Barrio</th>' + "".join(f"<th>{esc(cap(pal(_pk, s_)[1]))}</th>" for s_ in SERV_PAIS[_pk]) + "</tr>" + "".join(f'<tr><td><a href="{R_Z(_c, z)}"><b>{esc(z)}</b></a></td>' + "".join(f'<td><a href="{R_ZS(_c, z, s_)}">Ver</a></td>' for s_ in SERV_PAIS[_pk]) + "</tr>" for z in _c["zonas"]) + "</table></div>"
    _pq = [(f"¿En qué barrios de {_nom} dan servicio técnico Samsung?", "En " + ", ".join(_c["zonas"][:14]) + f" y otros sectores de {_nom}."), ("¿Cómo pido la visita?", f"Escribe al WhatsApp {wa_vis(_pk)} con tu barrio, el equipo y la falla."), ("¿Atienden en toda la ciudad?", f"Sí, atendemos {_nom} con visita a domicilio; si tu barrio no aparece, escríbenos y lo confirmamos.")]
    pagina(R_BARRIOS(_c), f"Barrios de {_nom} donde damos servicio técnico Samsung", f"Servicio técnico Samsung a domicilio en {len(_c['zonas'])} barrios de {_nom}: {', '.join(_c['zonas'][:8])} y más.", f"barrios {_nom.lower()} servicio tecnico samsung",
           [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("Barrios", None)],
           hero_simple(f"{_nom} · {_c['dep']}", f"Servicio técnico Samsung por barrios en {_nom}", "Elige tu barrio y el equipo.", acciones(_pk, f"Hola, necesito servicio técnico Samsung en {_nom}"))
           + qa(f"¿En qué barrios de {_nom} atienden?", "Atendemos " + esc(", ".join(_c["zonas"])) + f". WhatsApp {esc(wa_vis(_pk))}.") + seccion("Barrios", _tags) + seccion("Equipo por barrio", _tabla, alt=True) + faq_html(_pq), _pq, [], prio="0.8", pk=_pk, tipo="zonas", ctx=_c, compacto=True)
    # guía local
    R_IG = f"{_pk}/{_c['d']}/clima-y-electrodomesticos-en-ibague/index.html"
    v = VOLT[_pk]
    _ig_q = [(f"¿Cómo afecta el clima de {_nom} a mis electrodomésticos Samsung?", f"{_nom} tiene clima {_cl['clima']}. Los meses de más lluvia son {_cl['lluvia']}."), (f"¿Qué voltaje hay en {_nom}?", f"{v[0]} a {v[1]}, con enchufes {v[2]}."),
             ("¿Conviene usar protector de voltaje?", "Sí, para neveras, lavadoras y televisores: los picos de tensión dañan tarjetas y fuentes."), ("¿Cada cuánto hacer mantenimiento?", "Una revisión preventiva al año y limpieza periódica de filtros y condensadores.")]
    _ig_body = "".join(f"<h3>{esc(cap(pal(_pk, s_)[1]))} Samsung en {esc(_nom)}</h3><p>{esc(efecto_de(_c, s_))}.</p><p>{esc(uno('ig|' + s_, TIPS[s_]))}</p>" for s_ in SERV_PAIS[_pk])
    pagina(R_IG, f"Clima y electrodomésticos Samsung en {_nom}: cuidados", f"Cómo afectan el clima, la altitud y la electricidad de {_nom} a tus neveras, lavadoras y secadoras Samsung, y cómo cuidarlas.", f"clima {_nom.lower()} electrodomesticos samsung, cuidar nevera samsung {_nom.lower()}",
           [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("Clima y electrodomésticos", None)],
           hero_simple(f"{_nom} · {_c['dep']}", f"Clima y electrodomésticos Samsung en {_nom}", f"Altitud, calor, lluvias y voltaje: lo que debes saber para cuidar tu línea blanca.", acciones(_pk, f"Hola, quiero una revisión de mis electrodomésticos Samsung en {_nom}"))
           + qa(f"¿Cómo cuidar mis electrodomésticos Samsung en {_nom}?", f"En {esc(_nom)} el clima es {esc(_cl['clima'])}; los meses de más lluvia son {esc(_cl['lluvia'])}. Usa protector de voltaje (red de {esc(v[0])}), deja ventilados los equipos y haz una revisión preventiva al año.", [("Altitud", f"{_cl['alt']} m"), ("Clima", _cl["clima"]), ("Red eléctrica", f"{v[0]} · {v[1]}")])
           + seccion("Datos de la ciudad", _datos(_c)) + seccion(f"Cuidado por equipo en {esc(_nom)}", '<div class="prose">' + _ig_body + "</div>", alt=True) + faq_html(_ig_q), _ig_q, [], prio="0.7", pk=_pk, tipo="guias", ctx=_c, compacto=True)
    # enlaces desde la ciudad, los barrios y los servicios
    _ins(R_CIU(_c), seccion(f"Servicio técnico por barrio en {esc(_nom)}", _tags + f'<p><a href="{R_BARRIOS(_c)}">Ver todos los barrios y equipos →</a> · <a href="{R_IG}">Clima y cuidados en {esc(_nom)}</a></p>', alt=True))
    for _z in _c["zonas"]:
        _ins(R_Z(_c, _z), seccion(f"Equipos que reparamos en {esc(_z)}", '<div class="city-tags">' + "".join(f'<a href="{R_ZS(_c, _z, s_)}">{esc(cap(pal(_pk, s_)[1]))} Samsung en {esc(_z)}</a>' for s_ in SERV_PAIS[_pk]) + "</div>", alt=True))
    for _sv in SERV_PAIS[_pk]:
        _ins(R_CS(_c, _sv), seccion(f"{esc(cap(pal(_pk, _sv)[1]))} Samsung por barrio en {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_ZS(_c, z, _sv)}">{esc(z)}</a>' for z in _c["zonas"]) + "</div>"))
