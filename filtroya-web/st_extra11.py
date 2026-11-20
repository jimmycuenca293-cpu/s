# Cali (y cualquier sitio con mas=True): servicios por pieza, más términos de búsqueda, comunas y preguntas por equipo.
if SOLO and SOLO_CFG[SOLO].get("mas"):
    _c = CIU[0]; _pk = _c["pk"]; _P = PAISES[_pk]; _nom = _c["n"]; _wa = wa_vis(_pk)
    PIEZAS = {
        "nevera": [("compresor", "Compresor", "Es el motor que hace circular el gas refrigerante y mantiene el frío; si falla, la nevera deja de enfriar o no arranca.", ["la nevera no enfría aunque el motor suena", "se escucha un zumbido fuerte o clics repetidos", "se calienta mucho la parte trasera", "la nevera se apaga sola"]),
                   ("sello de la puerta", "Sello de la puerta", "Es el empaque de goma que cierra la puerta; si está roto o deformado se pierde frío y se forma escarcha.", ["la puerta no cierra del todo", "hay escarcha cerca de la puerta", "el consumo de energía subió", "el empaque está rígido, roto o con moho"]),
                   ("ventilador del evaporador", "Ventilador del evaporador", "Reparte el aire frío dentro de la nevera; si se detiene o hace ruido, el congelador enfría pero el refrigerador no.", ["el congelador congela y el refrigerador queda tibio", "ruido de aleteo o golpeteo", "escarcha en la pared del fondo"]),
                   ("resistencia de deshielo", "Resistencia de deshielo", "Derrite el hielo del evaporador; si falla, el hielo se acumula y bloquea el aire.", ["capa gruesa de hielo en el congelador", "la nevera enfría cada vez menos", "gotea agua por falla del deshielo"]),
                   ("tarjeta electrónica", "Tarjeta electrónica", "Coordina el compresor, los ventiladores, el deshielo y el panel; los picos de voltaje la dañan con frecuencia.", ["el panel no responde o muestra errores", "la nevera no enciende pese a tener corriente", "los componentes se activan sin orden"]),
                   ("sensor de temperatura", "Sensor de temperatura", "Mide el frío y avisa a la tarjeta cuándo encender o apagar el compresor.", ["enfría demasiado o muy poco sin explicación", "el panel marca una temperatura que no corresponde", "congela las verduras"])],
        "lava": [("bomba de desagüe", "Bomba de desagüe", "Saca el agua del tambor; si se tapa o se daña aparece el código 5E y la lavadora no desagua.", ["queda agua en el tambor al terminar el ciclo", "código 5E o 5C en el panel", "ruido fuerte al desaguar"]),
                 ("rodamientos del tambor", "Rodamientos del tambor", "Permiten girar el tambor sin fricción; desgastados producen un ruido metálico fuerte al centrifugar.", ["ruido metálico o rugido al centrifugar", "el tambor tiene juego al moverlo", "vibración fuerte"]),
                 ("amortiguadores", "Amortiguadores", "Absorben el movimiento del tambor mientras gira; gastados provocan golpes y desplazamiento de la lavadora.", ["la lavadora salta o se mueve", "golpes durante el centrifugado", "código UE repetido"]),
                 ("válvula de entrada de agua", "Válvula de entrada de agua", "Deja pasar el agua al tambor; si falla o su filtro se tapa, no entra agua o entra muy lenta.", ["código 4E o 4C", "la lavadora no llena o llena muy despacio", "se filtra agua cuando está apagada"]),
                 ("sello de la puerta", "Sello de la puerta", "Evita fugas en las lavadoras de carga frontal; con el tiempo acumula moho o se rompe.", ["bota agua por la puerta", "olor a humedad o moho", "grietas en la goma"]),
                 ("tarjeta electrónica", "Tarjeta electrónica", "Controla los ciclos, el motor, la bomba y el panel; los picos de voltaje suelen dañarla.", ["no enciende pese a tener corriente", "el panel muestra caracteres raros", "se detiene en mitad del ciclo sin código claro"])],
        "seca": [("resistencia", "Resistencia", "Calienta el aire en secadoras eléctricas o de condensación; si se quema, la ropa sale húmeda.", ["la secadora gira pero no calienta", "los ciclos tardan mucho más de lo normal", "olor a quemado"]),
                 ("correa y rodillos del tambor", "Correa y rodillos del tambor", "Hacen girar el tambor; gastados producen chirridos o el tambor deja de girar.", ["ruido de chirrido o golpeteo", "el motor suena pero el tambor no gira", "olor a goma quemada"]),
                 ("termostato y sensor de temperatura", "Termostato y sensor de temperatura", "Controlan que la secadora no se sobrecaliente y cortan el ciclo cuando la ropa está seca.", ["se apaga a mitad del ciclo", "seca de más o de menos", "se calienta demasiado la puerta"]),
                 ("filtro y ducto de pelusa", "Filtro y ducto de pelusa", "Dejan salir el aire húmedo; si se tapan, la secadora tarda más y se sobrecalienta.", ["secado muy lento", "pelusa en la puerta o en el ducto", "se calienta el exterior del equipo"]),
                 ("tarjeta electrónica", "Tarjeta electrónica", "Maneja los programas, la temperatura y el motor.", ["no responde el panel", "se detiene sin código", "no arranca el ciclo"]),
                 ("bomba de calor", "Bomba de calor", "En modelos Heat Pump, seca con menos energía; si falla, el secado se alarga.", ["secado muy lento en modelos Heat Pump", "agua en el depósito sin secar bien", "ruido inusual del compresor"])],
        "lavaplatos": [("bomba de desagüe", "Bomba de desagüe", "Saca el agua sucia del lavavajillas; si falla, queda agua en el fondo.", ["queda agua al terminar el ciclo", "olor a agua estancada", "el equipo se detiene con error"]),
                       ("brazos rociadores", "Brazos rociadores", "Reparten el agua por toda la cuba; si se tapan o se aflojan, los platos salen sucios.", ["platos con restos", "los brazos no giran", "poco agua en la parte alta"]),
                       ("sello de la puerta", "Sello de la puerta", "Evita fugas durante el ciclo.", ["gotea agua por la puerta", "humedad en el mueble", "el sello está duro o roto"]),
                       ("bomba de circulación", "Bomba de circulación", "Impulsa el agua hacia los brazos rociadores.", ["lava con poca fuerza", "ruido inusual durante el lavado", "error en el panel"]),
                       ("resistencia", "Resistencia", "Calienta el agua y ayuda a secar los platos.", ["los platos salen húmedos", "agua poco caliente", "ciclos muy largos"]),
                       ("tarjeta electrónica", "Tarjeta electrónica", "Controla los ciclos y los sensores.", ["no enciende", "no avanza de un ciclo a otro", "el panel no responde"])],
        "cocina": [("quemador", "Quemador", "Es donde sale el gas y se forma la llama; suciedad o humedad lo hacen fallar.", ["la llama es amarilla o irregular", "una hornilla no enciende", "poca potencia de llama"]),
                   ("chispero o encendedor", "Chispero o encendedor", "Genera la chispa para encender el quemador.", ["hace clic pero no enciende", "enciende solo a veces", "chispa débil"]),
                   ("perilla y válvula de gas", "Perilla y válvula de gas", "Regulan el paso del gas; si se traban, la perilla no gira o no se apaga bien.", ["la perilla no gira o está dura", "no se apaga la llama", "olor a gas: cierra la llave y ventila"]),
                   ("resistencia del horno", "Resistencia del horno", "Calienta el horno eléctrico; si se quema, no sube la temperatura.", ["el horno no calienta", "calienta solo arriba o solo abajo", "tarda mucho en llegar a temperatura"]),
                   ("termostato del horno", "Termostato del horno", "Controla la temperatura interna.", ["quema o deja crudo", "no mantiene la temperatura", "se apaga el horno"]),
                   ("sello de la puerta del horno", "Sello de la puerta del horno", "Mantiene el calor adentro.", ["se escapa el calor por la puerta", "la puerta no cierra bien", "gasto de gas mayor"])],
        "micro": [("magnetrón", "Magnetrón", "Genera las microondas que calientan la comida; si falla, el equipo gira pero no calienta.", ["gira el plato pero la comida queda fría", "zumbido fuerte sin calor", "olor a quemado"]),
                  ("diodo de alto voltaje", "Diodo de alto voltaje", "Alimenta al magnetrón; su manipulación solo la debe hacer un técnico.", ["no calienta con el panel funcionando", "se funde el fusible", "ruido de zumbido"]),
                  ("fusible", "Fusible", "Protege el circuito ante sobrecargas.", ["el microondas no enciende", "no da señal en el panel", "se apagó tras un pico de voltaje"]),
                  ("seguro de la puerta", "Seguro de la puerta", "Impide funcionar con la puerta abierta; si falla, el microondas no arranca.", ["la puerta cierra pero no arranca", "se apaga al cerrar", "la puerta no ajusta bien"]),
                  ("motor del plato giratorio", "Motor del plato giratorio", "Hace girar el plato para calentar parejo.", ["el plato no gira", "ruido al girar", "calienta de forma desigual"]),
                  ("tarjeta y panel", "Tarjeta y panel", "Controlan tiempo, potencia y teclas.", ["el panel no responde", "pantalla apagada", "teclas que no funcionan"])],
    }
    R_PZ = lambda sv, pz: f"{_pk}/{_c['d']}/cambio-de-{slug(pz)}-{slug(pal(_pk, sv)[0])}/index.html"
    for _sv, lista in PIEZAS.items():
        if _sv not in SERV_PAIS[_pk]:
            continue
        _s1, _s2 = pal(_pk, _sv); S = SERVICIOS[_sv]
        for pz, titpz, desc_pz, senales in lista:
            k = f"pz|{_sv}|{pz}"; f_ = dict(s1=_s1, s2=_s2, c=_nom)
            tit = f"Cambio de {pz} de {_s1} Samsung en {_nom}"
            preg = [(f"¿Cuándo hay que cambiar el {pz} de una {_s1} Samsung?" if False else f"¿Cuándo hay que revisar el {pz} de mi {_s1} Samsung?", f"Cuando aparecen señales como: {'; '.join(senales[:3])}. El técnico confirma en el diagnóstico si hay que cambiarlo."),
                    (f"¿Hacen el cambio de {pz} en {_nom}?", f"Sí, a domicilio en {_nom}: el técnico diagnostica, te confirma el valor y la disponibilidad de la pieza antes de repararla. WhatsApp {_wa}."),
                    (f"¿Cuánto cuesta cambiar el {pz}?", "Depende del modelo y de la disponibilidad del repuesto; no hay precio sin diagnóstico. El valor se confirma antes de reparar."),
                    ("¿Puedo cambiarlo yo mismo?", "No lo recomendamos: hay riesgo eléctrico y de dañar otras piezas; la revisión la debe hacer un técnico.")] + preguntas_ia(_c, k, 2)
            cuerpo = (hero_simple(f"{_nom} · {_c['dep']}", tit, f"Qué hace esta pieza, cuándo falla y cómo se revisa a domicilio en {_nom}.", acciones(_pk, f"Hola, creo que el {pz} de mi {_s1} Samsung falla en {_nom}"))
                      + qa(f"¿Cuándo hay que revisar el {pz} de una {_s1} Samsung?", f"{esc(desc_pz)} Señales: {esc('; '.join(senales[:3]))}. Visita a domicilio en {esc(_nom)}.", [("Equipo", cap(_s1) + " Samsung"), ("Pieza", titpz), ("Ciudad", _nom), ("WhatsApp", _wa)])
                      + seccion(f"Qué es el {esc(pz)} y para qué sirve", f"<p>{esc(desc_pz)}</p>")
                      + seccion(f"Señales de que el {esc(pz)} falla", _ul2(senales))
                      + seccion("Qué hace el técnico en la visita", '<ol class="vl"><li>Escucha tu descripción y revisa el equipo.</li><li>Comprueba la pieza y las partes relacionadas con medición.</li><li>Te explica el resultado y las opciones.</li><li>Te confirma el valor y la disponibilidad del repuesto antes de repararlo.</li><li>Si aceptas, cambia la pieza y prueba el equipo contigo.</li></ol>')
                      + seccion(f"Cuidados para tu {esc(_s1)} Samsung en {esc(_nom)}", _cuidado(_c, _sv, k, 3))
                      + seccion(f"Más sobre {esc(_s2)} Samsung en {esc(_nom)}", '<div class="city-tags">' + f'<a href="{R_CS(_c, _sv)}">{esc(cap(_s2))} Samsung en {esc(_nom)}</a>' + "".join(f'<a href="{R_PZ(_sv, p2[0])}">Cambio de {esc(p2[0])}</a>' for p2 in lista if p2[0] != pz) + f'<a href="{R_WA(_c)}">WhatsApp en {esc(_nom)}</a></div>')
                      + faq_html(preg, f"Preguntas sobre el {pz} de tu {_s1} Samsung"))
            SOLO_EXTRA.append((tit, R_PZ(_sv, pz), "Pieza"))
            pagina(R_PZ(_sv, pz), tit, f"Cambio de {pz} de {_s1} Samsung en {_nom}: qué hace la pieza, señales de falla y revisión a domicilio. Valor confirmado antes de reparar. WhatsApp {_wa}.", f"cambio de {pz} {_s1} samsung {_nom.lower()}, {pz} {_s1} samsung",
                   [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), (cap(_s2), R_CS(_c, _sv)), (tit, None)], cuerpo, preg, [{"@type": "Service", "name": tit, "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "City", "name": _nom}}], prio="0.7", pk=_pk, tipo="ciudades", ctx=_c, compacto=True)
        _ins(R_CS(_c, _sv), seccion(f"Servicio por pieza: {esc(_s2)} Samsung en {esc(_nom)}", '<div class="city-tags">' + "".join(f'<a href="{R_PZ(_sv, p2[0])}">Cambio de {esc(p2[0])}</a>' for p2 in lista) + "</div>", alt=True))
    # comunas de la ciudad (sin asignar barrios que no confirmamos)
    _com = SOLO_CFG[SOLO].get("comunas", True)
    R_CM = lambda n: f"{_pk}/{_c['d']}/comuna-{n}/index.html"
    R_CMS = f"{_pk}/{_c['d']}/comunas/index.html"
    for n in (range(1, 23) if _com else []):
        tit = f"Servicio técnico Samsung en la comuna {n} de {_nom}"
        preg = [(f"¿Atienden la comuna {n} de {_nom}?", f"Sí, atendemos la comuna {n} con visita a domicilio. Escribe al {_wa} con tu barrio y coordinamos la visita."), ("¿Qué equipos reparan?", ", ".join(pal(_pk, s_)[1] for s_ in SERV_PAIS[_pk]).capitalize() + "."), ("¿Cómo pido la visita?", f"Por WhatsApp al {_wa}: envía tu barrio, el equipo, el modelo y la falla.")] + preguntas_ia(_c, f"cm|{n}", 2)
        cuerpo = (hero_simple(f"{_nom} · Comuna {n}", tit, f"Visita a domicilio en la comuna {n}: neveras, lavadoras, secadoras, lavavajillas, estufas y microondas Samsung.", acciones(_pk, f"Hola, necesito servicio técnico Samsung en la comuna {n} de {_nom}"))
                  + qa(f"¿Hay servicio técnico Samsung a domicilio en la comuna {n} de {_nom}?", f"Sí. Atendemos la comuna {n} de {esc(_nom)}: escribe al {esc(_wa)} con tu barrio y coordinamos la visita; el valor se confirma antes de reparar.")
                  + seccion("Cómo pedir la visita en tu comuna", '<ol class="vl"><li>Escribe por WhatsApp con tu barrio y la comuna.</li><li>Cuéntanos el equipo, el modelo y la falla.</li><li>Coordinamos el día de la visita.</li><li>El técnico diagnostica y confirma el valor antes de reparar.</li></ol>')
                  + seccion(f"Equipos que reparamos en la comuna {n}", '<div class="city-tags">' + "".join(f'<a href="{R_CS(_c, s_)}">{esc(cap(pal(_pk, s_)[1]))} Samsung en {esc(_nom)}</a>' for s_ in SERV_PAIS[_pk]) + "</div>", alt=True)
                  + seccion("Barrios de la ciudad donde atendemos", '<div class="city-tags">' + "".join(f'<a href="{R_Z(_c, z)}">{esc(z)}</a>' for z in _c["zonas"][:30]) + f'<a href="{R_BARRIOS(_c)}"><b>Ver todos →</b></a></div>')
                  + seccion("Otras comunas", '<div class="city-tags">' + "".join(f'<a href="{R_CM(m)}">Comuna {m}</a>' for m in range(1, 23) if m != n) + "</div>", alt=True) + faq_html(preg))
        SOLO_EXTRA.append((tit, R_CM(n), "Comuna"))
        pagina(R_CM(n), tit, f"Servicio técnico Samsung a domicilio en la comuna {n} de {_nom}: neveras, lavadoras, secadoras, lavavajillas, estufas y microondas. WhatsApp {_wa}.", f"servicio tecnico samsung comuna {n} {_nom.lower()}, tecnico samsung comuna {n} {_nom.lower()}",
               [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("Comunas", R_CMS), (f"Comuna {n}", None)], cuerpo, preg, [], prio="0.6", pk=_pk, tipo="zonas", ctx=_c, compacto=True)
    if _com:
        pagina(R_CMS, f"Comunas de {_nom} donde damos servicio técnico Samsung", f"Servicio técnico Samsung a domicilio en las 22 comunas de {_nom}. Elige tu comuna y escribe por WhatsApp {_wa}.", f"comunas {_nom.lower()} servicio tecnico samsung",
               [("Inicio", "index.html"), (_P["nombre"], R_PAIS(_pk)), (_nom, R_CIU(_c)), ("Comunas", None)],
               hero_simple(f"{_nom} · Comunas", f"Servicio técnico Samsung en las comunas de {_nom}", "Elige tu comuna.", acciones(_pk, f"Hola, necesito servicio técnico Samsung en {_nom}"))
               + qa(f"¿En qué comunas de {_nom} atienden?", f"En las 22 comunas de {esc(_nom)}. WhatsApp {esc(_wa)}.") + seccion("Las 22 comunas", '<div class="city-tags">' + "".join(f'<a href="{R_CM(m)}">Comuna {m}</a>' for m in range(1, 23)) + "</div>"), [], [], prio="0.7", pk=_pk, tipo="zonas", ctx=_c, compacto=True)
        _ins(R_CIU(_c), seccion(f"Comunas de {esc(_nom)}", f'<p><a href="{R_CMS}">Servicio técnico Samsung en las 22 comunas de {esc(_nom)} →</a></p>', alt=True))
