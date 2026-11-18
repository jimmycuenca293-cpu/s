# Ubicación, horario y servicio 24 horas (solo sitios con datos de la ficha de Google: direccion/horas24).
if SOLO and SOLO_CFG[SOLO].get("direccion"):
    _cfg = SOLO_CFG[SOLO]; _c = CIU[0]; _pk = _c["pk"]; _P = PAISES[_pk]; _nom = _c["n"]; _wa = wa_vis(_pk); _dir = _cfg["direccion"]
    _tel = _cfg.get("telefono_vis", _wa)
    _mapa = '<div class="st-map"><iframe title="Mapa de ' + esc(_dir) + '" src="https://www.google.com/maps?q=' + __import__("urllib.parse").parse.quote_plus(_dir) + '&amp;output=embed" width="100%" height="340" style="border:0;border-radius:14px" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>'
    _eq = "".join(f'<a href="{R_CS(_c, s_)}">{esc(cap(pal(_pk, s_)[1]))} Samsung en {esc(_nom)}</a>' for s_ in SERV_PAIS[_pk])
    # ---- Ubicación y horario ----
    tit = f"Ubicación, horario y contacto del servicio técnico Samsung en {_nom}"
    preg = [(f"¿Dónde queda el servicio técnico Samsung en {_nom}?", f"Nuestra ubicación en Google es {_dir}. El servicio se presta a domicilio en toda la ciudad: escribe por WhatsApp al {_tel} y coordinamos la visita."),
            ("¿Cuál es el horario de atención?", "La línea de atención figura abierta las 24 horas. Escríbenos cuando lo necesites; el día y la hora de la visita se confirman por WhatsApp según la disponibilidad del técnico."),
            ("¿Cuál es el teléfono y WhatsApp?", f"El teléfono y WhatsApp es {_tel}. Puedes llamar o escribir con el equipo, el modelo y la falla."),
            ("¿Atienden domingos y festivos?", "Puedes escribir cualquier día, a cualquier hora. La disponibilidad de la visita en domingos y festivos se confirma por WhatsApp."),
            ("¿Debo llevar el equipo a la dirección?", "No es necesario: el técnico va a tu casa o negocio. Si el equipo requiere taller, te lo informamos antes de retirarlo.")]
    cuerpo = (hero_simple(f"{_nom} · Contacto", tit, f"Dirección, horario 24 horas y WhatsApp {_tel}.", acciones(_pk, f"Hola, necesito servicio técnico Samsung en {_nom}"))
              + qa(f"¿Cómo contactar al servicio técnico Samsung en {_nom}?", f"Escribe o llama al {esc(_tel)}. La línea está abierta las 24 horas y el técnico va a domicilio.")
              + seccion("Datos del negocio", f'<ul class="vl2"><li><b>Nombre:</b> {esc(NOMBRE)}</li><li><b>Dirección:</b> {esc(_dir)}</li><li><b>Horario:</b> abierto las 24 horas</li><li><b>Teléfono y WhatsApp:</b> <a href="tel:+{wa_num(_pk)}">{esc(_tel)}</a></li><li><b>Servicio:</b> reparación de neveras, lavadoras, secadoras, lavavajillas, estufas y microondas Samsung a domicilio</li></ul>')
              + seccion("Mapa", _mapa, alt=True)
              + seccion("Cómo pedir la visita", '<ol class="vl"><li>Escríbenos por WhatsApp con tu barrio.</li><li>Cuéntanos el equipo, el modelo y la falla.</li><li>Coordinamos el día y la hora de la visita.</li><li>El técnico diagnostica y te confirma el valor antes de reparar.</li></ol>')
              + seccion("Equipos que reparamos", '<div class="city-tags">' + _eq + "</div>", alt=True)
              + seccion("Más información", f'<div class="city-tags"><a href="{R_24H(_c)}">Servicio técnico Samsung 24 horas</a><a href="{R_BARRIOS(_c)}">Barrios donde atendemos</a><a href="{R_CIU(_c)}">Servicio técnico Samsung en {esc(_nom)}</a></div>')
              + faq_html(preg))
    SOLO_EXTRA.append((tit, R_UBIC(_c), "Contacto"))
    pagina(R_UBIC(_c), tit, f"Servicio técnico Samsung en {_nom}: {_dir}. Abierto las 24 horas, visita a domicilio. WhatsApp {_tel}.", f"servicio tecnico samsung {_nom.lower()} direccion, telefono servicio tecnico samsung {_nom.lower()}, horario servicio tecnico samsung {_nom.lower()}, {_cfg.get('barrio_dir','').lower()} {_nom.lower()}",
           [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("Ubicación y horario", None)], cuerpo, preg, [], prio="0.8", pk=_pk, tipo="guias", ctx=_c, compacto=True)
    # ---- 24 horas ----
    tit = f"Servicio técnico Samsung {_nom} 24 horas"
    preg = [(f"¿Hay servicio técnico Samsung 24 horas en {_nom}?", f"La línea de atención está abierta las 24 horas: escribe al {_tel} y recibes respuesta para coordinar la visita. La hora exacta de llegada se confirma según la disponibilidad."),
            ("¿Qué hago si mi nevera deja de enfriar de noche?", "Escríbenos de inmediato con el modelo y la falla. Mientras tanto, no abras la puerta para conservar el frío y pasa lo más delicado a otra nevera si puedes."),
            ("¿La visita tiene costo?", "El valor se confirma antes de reparar. Escríbenos por WhatsApp y te explicamos cómo funciona el diagnóstico."),
            ("¿Atienden urgencias?", "Sí, puedes reportar urgencias como nevera que no enfría, fugas de agua o equipos que no encienden; la visita se agenda según disponibilidad.")]
    cuerpo = (hero_simple(f"{_nom} · 24 horas", tit, f"Línea abierta las 24 horas. WhatsApp {_tel}.", acciones(_pk, f"Hola, necesito servicio técnico Samsung urgente en {_nom}"))
              + qa(f"¿Puedo escribir a cualquier hora?", f"Sí. La línea {esc(_tel)} figura abierta las 24 horas; la visita se coordina por WhatsApp.")
              + seccion("Urgencias frecuentes", '<ul class="vl2"><li>Nevera que no enfría o con el congelador descongelado.</li><li>Lavadora que no desagua o inunda.</li><li>Equipo que no enciende tras un corte o pico de voltaje.</li><li>Estufa o microondas con falla de encendido.</li></ul>')
              + seccion("Qué decirnos al escribir", '<ol class="vl"><li>El equipo y la marca (Samsung).</li><li>El modelo, si lo tienes a la vista.</li><li>Qué falla presenta y desde cuándo.</li><li>Tu barrio en ' + esc(_nom) + '.</li></ol>', alt=True)
              + seccion("Equipos que atendemos", '<div class="city-tags">' + _eq + "</div>")
              + seccion("Más información", f'<div class="city-tags"><a href="{R_UBIC(_c)}">Ubicación y horario</a><a href="{R_BARRIOS(_c)}">Barrios</a><a href="{R_CIU(_c)}">Servicio técnico Samsung en {esc(_nom)}</a></div>', alt=True)
              + faq_html(preg))
    SOLO_EXTRA.append((tit, R_24H(_c), "24 horas"))
    pagina(R_24H(_c), tit, f"Servicio técnico Samsung en {_nom} 24 horas: neveras, lavadoras, secadoras y más a domicilio. Línea abierta las 24 horas. WhatsApp {_tel}.", f"servicio tecnico samsung {_nom.lower()} 24 horas, tecnico samsung urgente {_nom.lower()}, reparacion nevera samsung {_nom.lower()} urgente",
           [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("24 horas", None)], cuerpo, preg, [], prio="0.8", pk=_pk, tipo="guias", ctx=_c, compacto=True)
    _ins(R_CIU(_c), seccion(f"Ubicación y horario en {esc(_nom)}", f'<p>{esc(_dir)} · abierto las 24 horas · {esc(_tel)}</p><div class="city-tags"><a href="{R_UBIC(_c)}">Ubicación, horario y contacto</a><a href="{R_24H(_c)}">Servicio técnico Samsung 24 horas</a></div>', alt=True))
