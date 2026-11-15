# Subpáginas por zona, guías de mantenimiento por ciudad y guías de voltaje por país (se ejecuta dentro de st_paginas.py antes de la salida).
TIT_Z = ["Servicio técnico Samsung en {z}, {c}", "Técnico Samsung a domicilio en {z} ({c})", "Reparación de electrodomésticos Samsung en {z}, {c}", "{z}: servicio técnico Samsung en {c}",
         "Servicio técnico de línea blanca Samsung en {z} ({c})", "Arreglo de {nev} y {lav} Samsung en {z}, {c}", "Técnico de {nev} Samsung en {z} | {c}", "Servicio Samsung a domicilio en {z}, {c}", "Centro de servicio técnico Samsung en {z}, {c}", "Centro de servicio Samsung en {z} ({c})"]
DESC_Z = ["Servicio técnico Samsung a domicilio en {z}, {c}: {nev}, {lav}, secadoras y más. Escríbenos y coordinamos la visita; el valor se confirma antes de reparar.",
          "¿Falló tu Samsung en {z} ({c})? Revisamos y reparamos línea blanca en tu casa. Diagnóstico primero y valor confirmado antes de reparar.",
          "Técnicos para electrodomésticos Samsung en {z}, {c}: {nev}, {lav}, lavavajillas, estufas y microondas, con visita a domicilio.",
          "Atendemos {z}, en {c}: reparación y mantenimiento de línea blanca Samsung sin llevar el equipo a un taller. Pide tu visita por WhatsApp."]
QA_Z = ["¿Hay técnico Samsung a domicilio en {z}?", "¿Reparan electrodomésticos Samsung en {z}, {c}?", "¿Quién repara una Samsung en {z} ({c})?", "¿Atienden en {z} para neveras y lavadoras Samsung?"]
R_Z = lambda c, z: f"{c['pk']}/{c['d']}/{slug(z)}/index.html"
R_MANT = lambda c: f"{c['pk']}/{c['d']}/mantenimiento/index.html"
R_VOLT = lambda pk: f"{pk}/voltaje/index.html"
ZONAS_P = []  # (c, z)

for c in CIU:
    pk = c["pk"]; P = PAISES[pk]; cl = CLIMA[c["s"]]; nev = pal(pk, "nevera")[1]; lav = pal(pk, "lava")[1]
    zs = c["zonas"]
    for i, z in enumerate(zs if c["zp"] else []):
        key = f"z|{c['s']}|{z}"
        svs = SERV_PAIS[pk]
        spot = mix(key + "|sp", svs, 2)
        vec = [zs[(i + 1) % len(zs)], zs[(i - 1) % len(zs)]] + [x for x in mix(key + "|v", [y for y in zs if y != z], 2)]
        vec = [v for k, v in enumerate(vec) if v != z and v not in vec[:k]][:4]
        equipos = ", ".join(pal(pk, s)[1] for s in svs)
        f = dict(z=z, c=c["n"], nev=nev, lav=lav, equipos=cap(equipos))
        intro = uno(key + "|in", INTRO_Z).format(**f)
        climat = parrafo_clima(c, z, spot[0], key + "|cl")
        secs = ""
        for n, sv in enumerate(spot):
            s1, s2 = pal(pk, sv)
            extra = f"{cap(efecto_de(c, sv))}. " if n == 1 else ""
            secs += seccion(f"{esc(cap(s2))} Samsung en {esc(z)}", f"<p>{esc(extra)}{esc(uno(key + '|tp' + sv, TIPS[sv]))}</p><p>Fallas por las que nos llaman: " + esc(", ".join(mix(key + "|sy" + sv, SERVICIOS[sv]["sintomas"], 3))) + ".</p>"
                            f'<p><a href="{R_CS(c, sv)}">Ver el servicio de {esc(s2)} Samsung en {esc(c["n"])}</a></p>', alt=(n == 1))
        sig = []
        for sv in mix(key + "|sg", svs, 4):
            s1, _ = pal(pk, sv)
            sig.append(f"Tu {s1} Samsung {uno(key + '|sg' + sv, SERVICIOS[sv]['sintomas'])}.")
        pasos = [x.format(**f) for x in uno(key + "|vs", VISITA)]
        preg = [(q.format(**f), a.format(**f)) for q, a in mix(key + "|fq", FAQ_Z, 4)] + preguntas_ia(c, key, 2)
        msg = f"Hola, necesito servicio técnico Samsung en {z}, {c['n']}"
        cuerpo = (hero_simple(f"{z} · {c['n']}", f"Servicio técnico Samsung en {z}, {c['n']}", f"Visita técnica a domicilio para línea blanca Samsung en {z}, {c['dep']}.", acciones(pk, msg))
                  + qa(uno(key + "|qa", QA_Z).format(**f), f"Sí. Atendemos <b>{esc(z)}</b>, en {esc(c['n'])}, con visita a domicilio para {esc(equipos)} Samsung. Escríbenos por WhatsApp: hacemos el diagnóstico y te confirmamos el valor antes de reparar.",
                       [("Zona", z), ("Ciudad", c["n"]), ("Atención", "A domicilio"), ("WhatsApp", wa_vis(pk))])
                  + seccion(f"Atención en {esc(z)}", f"<p>{esc(intro)}</p><p>{esc(climat)}</p>") + secs
                  + bloque_mitos(key, spot) + bloque_snippets(c, f"sz|{c['s']}|{z}", 1, False)
                  + seccion("Señales de que tu equipo necesita revisión", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in sig) + "</ul>", alt=True)
                  + seccion(f"Cómo coordinamos la visita en {esc(z)}", '<ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in pasos) + "</ol>")
                  + faq_html(preg, f"Preguntas sobre el servicio en {z}")
                  + seccion("Zonas cercanas y más información", '<div class="city-tags">' + "".join(f'<a href="{R_Z(c, v)}">Servicio técnico Samsung en {esc(v)}</a>' for v in vec) + f'<a href="{R_CIU(c)}">Todo {esc(c["n"])}</a><a href="{R_MANT(c)}">Mantenimiento en {esc(c["n"])}</a><a href="{R_PAIS(pk)}">{esc(P["nombre"])}</a></div>'))
        tt = uno(key + "|t", TIT_Z).format(**f)
        pagina(R_Z(c, z), tt, uno(key + "|d", DESC_Z).format(**f), f"servicio tecnico samsung {z.lower()}, tecnico samsung {z.lower()} {c['n'].lower()}, reparacion {nev} samsung {z.lower()}",
               [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (c["n"], R_CIU(c)), (z, None)], cuerpo, preg,
               [{"@type": "Service", "name": f"Servicio técnico Samsung en {z}, {c['n']}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "Place", "name": f"{z}, {c['n']}"}}], prio="0.6", pk=pk, tipo="zonas", ctx=c, compacto=True)
        ZONAS_P.append((c, z))

# ------------------------------------------------------------------ mantenimiento por ciudad (guía según el clima)
CAL = {"pre": ["Revisa los sellos de la nevera y de la lavadora y cámbialos si están resecos.", "Instala o revisa un protector de voltaje en los equipos grandes.", "Limpia el polvo del condensador de la nevera.", "Revisa las mangueras de la lavadora y del lavavajillas.", "Limpia el filtro de pelusa y el ducto de la secadora."],
       "lluvia": ["Desconecta los equipos delicados durante las tormentas eléctricas.", "Seca el sello de la lavadora después de cada lavado.", "Limpia el filtro de la secadora en cada carga.", "Evita abrir la nevera por largos periodos.", "Deja ventilado el espacio de la nevera y de la secadora."],
       "despues": ["Haz un ciclo de limpieza del tambor de la lavadora.", "Revisa si aparecieron manchas de humedad o moho en los sellos.", "Limpia el filtro del lavavajillas y los brazos rociadores.", "Comprueba que la nevera no tenga escarcha ni gotee.", "Prueba los quemadores y el horno si estuvieron sin uso."],
       "seca": ["Aprovecha para limpiar por detrás la nevera y revisar el ventilador.", "Programa la revisión preventiva de lavadora y secadora.", "Revisa el desagüe de la lavadora y del lavavajillas.", "Limpia el panel y las rejillas del microondas y del horno.", "Revisa los cables y el estado de los enchufes."]}
for c in CIU:
    pk = c["pk"]; P = PAISES[pk]; cl = CLIMA[c["s"]]; v = VOLT[pk]; key = f"m|{c['s']}"
    riesgo = tipo_riesgo(cl); svs = SERV_PAIS[pk]
    alt = alt_txt(cl)
    ctxp = uno(key + "|ctx", ([f"{c['n']} tiene un clima {cl['clima']}, a unos {alt} metros sobre el nivel del mar. Las lluvias llegan {cl['lluvia']}.", f"El clima de {c['n']} es {cl['clima']}; está a unos {alt} metros de altitud y llueve {cl['lluvia']}.",
                              f"Con unos {alt} m de altitud, {c['n']} tiene un clima {cl['clima']} y lluvias {cl['lluvia']}."] if alt else [f"{c['n']} tiene un clima {cl['clima']}. Las lluvias llegan {cl['lluvia']}.", f"El clima de {c['n']} es {cl['clima']} y llueve {cl['lluvia']}."]))
    efectos = "".join(f"<li><b>{esc(cap(pal(pk, sv)[1]))}:</b> {esc(efecto_de(c, sv))}.</li>" for sv in svs)
    tabla = ('<div class="tbl-wrap"><table class="spec-table"><tr><th>Cuándo</th><th>Qué hacer</th></tr>'
             + f"<tr><td>Antes de las lluvias ({esc(cl['lluvia'])})</td><td>{esc(' '.join(mix(key + '|pre', CAL['pre'], 2)))}</td></tr>"
             + f"<tr><td>Durante las lluvias</td><td>{esc(' '.join(mix(key + '|ll', CAL['lluvia'], 2)))}</td></tr>"
             + f"<tr><td>Después de las lluvias</td><td>{esc(' '.join(mix(key + '|des', CAL['despues'], 2)))}</td></tr>"
             + f"<tr><td>Época más seca</td><td>{esc(' '.join(mix(key + '|se', CAL['seca'], 2)))}</td></tr></table></div>")
    elec = uno(key + "|el", [f"En {P['nombre']} la red es de {v[0]} a {v[1]} con enchufes {v[2]}. En {c['n']} el riesgo eléctrico más relevante es: {cl['riesgo']}. Un protector de voltaje y un buen polo a tierra ayudan a proteger la tarjeta de tus equipos.",
                             f"La corriente en {P['nombre']} es de {v[0]} y {v[1]} (enchufes {v[2]}). Para {c['n']} conviene tener presente {cl['riesgo']}: un protector de voltaje reduce el riesgo de daños en tarjetas y compresores.",
                             f"Los equipos Samsung en {c['n']} trabajan con {v[0]} y {v[1]}. Dado el contexto local ({cl['riesgo']}), usa protector de voltaje y evita regletas sobrecargadas."])
    resp = f"En {c['n']} ({cl['clima']}), lo recomendable es limpiar el filtro de la secadora en cada carga, el condensador de la nevera cada seis meses, el tambor de la lavadora una vez al mes y vigilar {cl['riesgo']}."
    preg = [(f"¿Cada cuánto hay que dar mantenimiento a una nevera Samsung en {c['n']}?", f"Una limpieza del condensador cada seis meses y una revisión preventiva al año; en {c['n']} conviene reforzar por {cl['riesgo']}."),
            (f"¿Qué voltaje usan los electrodomésticos en {c['n']}?", f"{v[0]} a {v[1]}, con enchufes {v[2]}."), (f"¿Cuándo llamar a un técnico en {c['n']}?", "Si hay ruidos nuevos, fugas, códigos de error o el equipo no cumple su función.")]
    cuerpo = (hero_simple(f"{c['n']} · {P['nombre']}", f"Mantenimiento de electrodomésticos Samsung en {c['n']}", f"Guía según el clima de {c['n']}: calendario, riesgos por equipo y electricidad.", acciones(pk, f"Hola, quiero mantenimiento para mis electrodomésticos Samsung en {c['n']}"))
              + qa(f"¿Cómo cuidar mis electrodomésticos Samsung en {c['n']}?", esc(resp), [("Clima", cl["clima"][:40]), ("Altitud", f"{alt} m" if alt else "Costa o llanura"), ("Lluvias", cl["lluvia"][:40]), ("Red eléctrica", f"{v[0]} · {v[1]}")])
              + seccion(f"El clima de {esc(c['n'])} y tus equipos", f"<p>{esc(ctxp)}</p><ul class=\"spec-list\">{efectos}</ul>") + seccion("Calendario de mantenimiento", tabla, alt=True)
              + seccion(f"Electricidad en {esc(c['n'])}", f"<p>{esc(elec)}</p>") + faq_html(preg)
              + seccion("Más información", '<div class="city-tags">' + f'<a href="{R_CIU(c)}">Servicio técnico Samsung en {esc(c["n"])}</a><a href="{R_VOLT(pk)}">Voltaje en {esc(P["nombre"])}</a>' + "".join(zlink(c, z) for z in c["zonas"]) + "</div>"))
    pagina(R_MANT(c), f"Mantenimiento de electrodomésticos Samsung en {c['n']}", f"Guía de mantenimiento para neveras, lavadoras y secadoras Samsung en {c['n']} según su clima ({cl['clima'][:40]}), lluvias y electricidad.", f"mantenimiento electrodomesticos samsung {c['n'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (c["n"], R_CIU(c)), ("Mantenimiento", None)], cuerpo, preg, [], prio="0.6", pk=pk, tipo="guias", ctx=c, compacto=True)

# ------------------------------------------------------------------ voltaje y corriente por país
for pk, P in PAISES.items():
    v = VOLT[pk]; es220 = v[0].startswith("220")
    key = f"v|{pk}"
    tabla = f'<div class="tbl-wrap"><table class="spec-table"><tr><th>Dato</th><th>{esc(P["nombre"])}</th></tr><tr><td>Voltaje</td><td>{v[0]}</td></tr><tr><td>Frecuencia</td><td>{v[1]}</td></tr><tr><td>Enchufes</td><td>{v[2]}</td></tr></table></div>'
    sig = (f"En {P['nombre']} la red es de {v[0]}. Un electrodoméstico fabricado para otro voltaje (por ejemplo 110-120 V) necesita transformador, y en neveras, lavadoras y secadoras eso no es recomendable: revisa siempre la placa del equipo." if es220 else
           f"En {P['nombre']} la red es de {v[0]}. Los equipos pensados para 220-240 V (algunas secadoras y cocinas de gran tamaño importadas) necesitan un circuito adecuado; revisa siempre la placa del equipo antes de conectar.")
    imp = (f"Si compraste un Samsung en un país con red de 110-120 V, antes de usarlo en {P['nombre']} verifica en la etiqueta si admite 100-240 V. Si no, no lo conectes directo." if es220 else
           f"Si compraste un Samsung en un país de red de 220-240 V, antes de usarlo en {P['nombre']} verifica en la etiqueta si admite el voltaje local. Si no, no lo conectes directo.")
    ciu = ", ".join(c["n"] for c in CIU_PAIS[pk])
    preg = [(f"¿Qué voltaje tiene {P['nombre']}?", f"{v[0]} a {v[1]}, con enchufes {v[2]}."), ("¿Puedo usar un Samsung comprado en otro país?", "Solo si la placa indica que admite el voltaje y la frecuencia locales; si no, hay riesgo de daño."),
            ("¿Necesito protector de voltaje?", "Es muy recomendable para neveras, lavadoras y televisores: los picos dañan tarjetas y fuentes."), ("¿Dónde está la placa del equipo?", "En una etiqueta, normalmente atrás o dentro de la puerta; ahí figuran voltaje, frecuencia y potencia.")]
    LOC = {
        "colombia": "En Colombia la red doméstica es de 110-120 V, y los Samsung que se venden en el país vienen preparados para ese voltaje. Las secadoras y estufas eléctricas grandes pueden pedir un circuito independiente: conviene que lo revise un electricista.",
        "panama": "En Panamá el aire acondicionado funciona casi todo el año, y eso exige mucho a las instalaciones antiguas. Si en tu edificio las luces bajan cuando arranca el aire, protege la nevera con un regulador.",
        "costa-rica": "En Costa Rica las tormentas eléctricas de la época lluviosa dejan picos de voltaje; los televisores y las neveras con tarjeta inverter son los más sensibles. Desconéctalos en tormentas fuertes.",
        "paraguay": "Paraguay trabaja con 220 V y 50 Hz. Un Samsung comprado en un mercado de 110-120 V y 60 Hz no funcionará bien aunque use transformador: el motor y los relojes internos dependen de la frecuencia.",
        "guatemala": "En Guatemala las lluvias fuertes de la temporada traen cortes y picos de energía. Un protector de voltaje con retardo de reconexión evita que el compresor arranque de golpe cuando vuelve la luz.",
        "el-salvador": "En El Salvador la red es de 115-120 V. Las tormentas de la época lluviosa y los cortes breves son los principales riesgos para las tarjetas electrónicas; usa protector y no desconectes y reconectes de inmediato la nevera.",
        "ecuador": "En Ecuador la red es de 120 V. En ciudades de altura como Quito y de costa como Guayaquil las condiciones de uso cambian, pero el cuidado eléctrico es el mismo: protector de voltaje y polo a tierra.",
        "chile": "En Chile la red es de 220-230 V y 50 Hz, con enchufes tipo C y L. Un Samsung comprado en un mercado de 120 V y 60 Hz no es compatible; revisa la placa del equipo antes de comprar o conectar.",
    }
    ciu_clima = " ".join(f"{c['n']} tiene un clima {CLIMA[c['s']]['clima']} y {CLIMA[c['s']]['lluvia']} son sus meses de más lluvia." for c in CIU_PAIS[pk])
    cuerpo = (hero_simple(f"{P['bandera']} {P['nombre']}", f"Voltaje y corriente en {P['nombre']}: qué debes saber para tus electrodomésticos Samsung", f"Datos de la red eléctrica de {P['nombre']} y cómo proteger tu línea blanca.", acciones(pk, f"Hola, tengo una duda eléctrica con mi Samsung en {P['nombre']}"))
              + qa(f"¿Qué voltaje usan los electrodomésticos en {P['nombre']}?", f"En {esc(P['nombre'])} la red eléctrica es de <b>{v[0]}</b> a <b>{v[1]}</b>, con enchufes {v[2]}. Revisa siempre la placa de tu Samsung antes de conectarlo y usa protector de voltaje.", [("Voltaje", v[0]), ("Frecuencia", v[1]), ("Enchufes", v[2])])
              + seccion("Datos de la red", tabla) + seccion("Qué significa para tu Samsung", f"<p>{esc(sig)}</p><p>{esc(imp)}</p>", alt=True)
              + seccion(f"Lo que debes saber en {esc(P['nombre'])}", f"<p>{esc(LOC[pk])}</p><p>{esc(ciu_clima)}</p>")
              + seccion("Cómo proteger tus equipos", _ul(["Usa un protector de voltaje o regulador en neveras, lavadoras y televisores.", "Evita conectar varios equipos grandes en la misma regleta.", "Verifica que la instalación tenga polo a tierra.", "Desconecta los equipos delicados durante tormentas eléctricas."]))
              + faq_html(preg) + seccion("Servicio técnico en tu ciudad", '<div class="city-tags">' + "".join(f'<a href="{R_CIU(c)}">{esc(c["n"])}</a>' for c in CIU_PAIS[pk]) + f'<a href="{R_PAIS(pk)}">Servicio en {esc(P["nombre"])}</a></div>', alt=True))
    pagina(R_VOLT(pk), f"Voltaje en {P['nombre']} y electrodomésticos Samsung", f"Voltaje ({v[0]}), frecuencia ({v[1]}) y enchufes de {P['nombre']}: cómo proteger tu línea blanca Samsung y qué revisar antes de conectar un equipo importado.", f"voltaje {P['nombre'].lower()} electrodomesticos samsung",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Voltaje", None)], cuerpo, preg, [], prio="0.6", pk=pk, tipo="guias")
