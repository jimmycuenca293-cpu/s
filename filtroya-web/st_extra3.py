# Capa de posicionamiento: páginas por línea Samsung (por país) y por falla (por ciudad). Se ejecuta antes de st_salida.py.
LINEAS = {
    "nevera": [
        ("French Door", "dos puertas arriba y un cajón de congelador abajo", ["el cajón del congelador no cierra bien o se atora", "los sellos de las puertas pierden hermeticidad", "gotea agua o se forma escarcha", "la fábrica de hielo no produce", "no enfría de manera pareja", "hace un ruido nuevo al funcionar"],
         ["sellos de las dos puertas", "guías y riel del cajón", "sistema de deshielo", "ventiladores del evaporador"]),
        ("Side by Side", "refrigerador y congelador lado a lado, con dispensador de agua y hielo en muchos modelos", ["el dispensador de agua no sirve", "la fábrica de hielo se congela o no produce", "gotea agua por la puerta", "el ventilador hace ruido", "el congelador se llena de escarcha", "no enfría el refrigerador"],
         ["válvula y mangueras del dispensador", "filtro de agua", "ventiladores", "sellos y resistencia de deshielo"]),
        ("Family Hub", "pantalla táctil integrada, cámaras interiores y conectividad Wi-Fi", ["la pantalla se queda en negro o no responde", "no se conecta al Wi-Fi ni a la aplicación", "las cámaras interiores no muestran imagen", "no enfría como antes", "la fábrica de hielo no produce", "marca un código de error en la pantalla"],
         ["pantalla y módulo de conectividad", "tarjeta principal", "sistema de enfriamiento", "sensores de temperatura"]),
        ("Bespoke", "paneles de colores intercambiables y diseño modular", ["no enfría de manera pareja", "los paneles frontales quedan flojos o desalineados", "gotea agua por dentro", "hace ruido el ventilador", "las puertas no sellan bien", "la pantalla o el panel no responde"],
         ["sellos de las puertas", "paneles y bisagras", "ventiladores", "tarjeta electrónica"]),
        ("Twin Cooling Plus", "dos circuitos de enfriamiento independientes, uno para el refrigerador y otro para el congelador", ["el congelador no congela bien", "el refrigerador enfría de más y congela las verduras", "se forma escarcha en el evaporador", "el compresor arranca y se detiene a cada rato", "hace ruido el ventilador", "gotea agua por dentro"],
         ["evaporadores y ventiladores", "sensores de temperatura", "compresor", "sistema de deshielo"]),
    ],
    "lava": [
        ("EcoBubble", "generación de burbujas de detergente para lavar con agua fría", ["no desagua o deja agua en el tambor", "no genera burbujas o deja residuos de detergente", "hace ruido al centrifugar", "bota agua por la puerta", "marca un código de error", "huele mal"],
         ["generador de burbujas", "bomba de desagüe", "válvulas de entrada de agua", "amortiguadores y rodamientos"]),
        ("AddWash", "una puerta adicional para agregar prendas durante el ciclo", ["la puerta pequeña no cierra o gotea", "el seguro de la puerta no engancha", "bota agua por la puerta de AddWash", "no entra agua", "no centrifuga", "marca error de puerta (dE)"],
         ["puerta AddWash y su sello", "seguro de la puerta", "válvulas de agua", "bomba de desagüe"]),
    ],
    "tv": [
        ("Crystal UHD", "televisores LED 4K de uso general", ["pantalla negra con sonido", "no enciende", "imagen oscura o parpadeo", "líneas verticales u horizontales"], ["fuente de poder", "retroiluminación", "tarjeta principal", "cables internos del panel"]),
        ("QLED", "pantallas con puntos cuánticos para más brillo y color", ["pantalla negra con sonido", "manchas o zonas oscuras", "no enciende", "no conecta al Wi-Fi"], ["retroiluminación", "fuente de poder", "tarjeta principal", "conectividad"]),
        ("Neo QLED", "retroiluminación Mini LED para mayor contraste", ["zonas de la pantalla se ven apagadas", "pantalla negra con sonido", "no enciende", "parpadeo de imagen"], ["módulos de retroiluminación", "fuente de poder", "tarjeta principal", "firmware y conectividad"]),
        ("OLED", "paneles que encienden cada píxel por separado", ["líneas o manchas en la pantalla", "imagen quemada o con retención", "no enciende", "pantalla negra con sonido"], ["panel y cables", "fuente de poder", "tarjeta principal", "configuración de imagen"]),
    ],
}
INTRO_L = ["{linea} es la línea de {desc}. Si tu {s1} Samsung {linea} falla en {pais}, un técnico va a tu casa, la revisa y te confirma el valor antes de reparar.",
           "Atendemos {s2} Samsung {linea} en {pais} con visita a domicilio. Esta línea se caracteriza por {desc}, y por eso las fallas suelen concentrarse en unos pocos componentes.",
           "¿Tienes una {s1} Samsung {linea}? En {pais} la revisamos en tu casa: sabemos qué suele fallar en esta línea y lo comprobamos en el diagnóstico.",
           "Reparación de {s2} Samsung {linea} en {pais}: equipos con {desc}. Coordinas por WhatsApp y el técnico revisa el equipo en tu hogar."]
FAQ_L = [("¿Reparan la {s1} Samsung {linea} en {pais}?", "Sí, con visita a domicilio en las ciudades de cobertura de {pais}."), ("¿Qué falla más en una {s1} Samsung {linea}?", "Las fallas más frecuentes: {fallas}."),
         ("¿Cómo sé si mi equipo es {linea}?", "Mira el nombre en el equipo o el modelo de la etiqueta; si tienes dudas, envíanos una foto por WhatsApp."), ("¿Cuánto cuesta reparar una {s1} Samsung {linea}?", "Depende de la falla y el repuesto; el valor se confirma tras el diagnóstico y antes de reparar."),
         ("¿Atienden equipos fuera de garantía?", "Sí, dentro y fuera de garantía; consulta las condiciones de tu garantía en el manual."), ("¿Qué datos necesito para pedir la visita?", "El modelo (etiqueta), la falla y la dirección.")]
LINEAS_P = []  # (pk, sv, linea, url)
R_LIN = lambda pk, linea: f"{pk}/{slug(linea)}/index.html"
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]
    for sv, lista in LINEAS.items():
        if sv not in SERV_PAIS[pk]:
            continue
        s1, s2 = pal(pk, sv)
        for (linea, desc, fallas, revisa) in lista:
            key = f"ln|{pk}|{linea}"
            f = dict(linea=linea, desc=desc, pais=P["nombre"], s1=s1, s2=s2, fallas=", ".join(mix(key + "|f", fallas, 3)))
            intro = uno(key + "|in", INTRO_L).format(**f)
            principales = [c for c in cs if not c["amp"]][:3] or cs[:3]
            clima = " ".join(parrafo_clima(c, c["zonas"][0], sv, key + "|" + c["s"]) for c in principales[:2])
            preg = [(q.format(**f), a.format(**f)) for q, a in mix(key + "|fq", FAQ_L, 4)]
            cuerpo = (hero_simple(f"{linea} · {P['nombre']}", f"Reparación de {s2} Samsung {linea} en {P['nombre']}", f"Servicio técnico a domicilio para {s2} Samsung {linea} en {len(cs)} ciudades de {P['nombre']}.", acciones(pk, f"Hola, necesito reparar mi {s1} Samsung {linea} en {P['nombre']}"))
                      + qa(f"¿Reparan la {s1} Samsung {linea} en {P['nombre']}?", f"Sí. Reparamos {esc(s2)} Samsung {esc(linea)} ({esc(desc)}) en {esc(P['nombre'])}, con visita a domicilio. Fallas frecuentes: {esc(f['fallas'])}. El valor se confirma tras el diagnóstico.", [("Línea", linea), ("Equipo", cap(s2) + " Samsung"), ("País", P["nombre"]), ("WhatsApp", wa_vis(pk))])
                      + seccion(f"Samsung {esc(linea)}: qué es y qué suele fallar", f"<p>{esc(intro)}</p><ul class=\"spec-list\">" + "".join(f"<li>Tu {esc(s1)} {esc(x)}.</li>" for x in mix(key + "|fl", fallas, 5)) + "</ul>")
                      + seccion("Qué revisa el técnico", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in revisa) + "</ul>", alt=True)
                      + seccion(f"El clima y tu {esc(linea)} en {esc(P['nombre'])}", f"<p>{esc(clima)}</p>")
                      + bloque_mitos(key, [sv], 1)
                      + seccion(f"Ciudades de {esc(P['nombre'])} donde reparamos {esc(linea)}", '<div class="city-tags">' + "".join(f'<a href="{R_CS(c, sv)}">{esc(cap(s2))} Samsung en {esc(c["n"])}</a>' for c in cs[:40]) + "</div>", alt=True)
                      + faq_html(preg))
            pagina(R_LIN(pk, linea), f"Reparación de {s2} Samsung {linea} en {P['nombre']}", f"Servicio técnico para {s2} Samsung {linea} en {P['nombre']}: {fallas[0]}, {fallas[1]} y más. Visita a domicilio y valor confirmado antes de reparar.",
                   f"reparacion {s2} samsung {linea.lower()} {P['nombre'].lower()}, servicio tecnico samsung {linea.lower()}", [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (cap(s2), R_SERV(pk, sv)), (linea, None)], cuerpo, preg,
                   [{"@type": "Service", "name": f"Reparación de {s2} Samsung {linea} en {P['nombre']}", "provider": {"@id": f"{DOMINIO}/#negocio"}, "areaServed": {"@type": "Country", "name": P["nombre"]}}], prio="0.7", pk=pk, tipo="paises")
            LINEAS_P.append((pk, sv, linea, R_LIN(pk, linea)))

# ------------------------------------------------------------------ falla × ciudad (búsquedas de alta intención)
PROB = [
    dict(sv="nevera", sl="no-enfria", tit="{S} Samsung no enfría en {c}", q="¿Por qué mi {s} Samsung no enfría en {c}?",
         res="Lo más común es escarcha que bloquea el ventilador, sellos de puerta dañados, un ventilador o el compresor con falla, o un sensor de temperatura descalibrado.",
         causas=["Escarcha que bloquea el flujo de aire del evaporador.", "Sellos de las puertas gastados o sucios.", "Ventilador del evaporador o del condensador sin funcionar.", "Compresor o relé de arranque con falla.", "Sensor de temperatura o tarjeta electrónica.", "Condensador cubierto de polvo."],
         pasos=["Comprueba que la puerta cierre bien y no esté desnivelada.", "Separa la {s} de la pared y limpia el polvo del condensador.", "Libera las rejillas de aire internas.", "Revisa si hay hielo en la pared del fondo del congelador.", "Deja pasar 24 horas tras ajustar la temperatura.", "Si el compresor no arranca, desconéctala y pide revisión."]),
    dict(sv="nevera", sl="con-escarcha", tit="{S} Samsung con escarcha en el congelador en {c}", q="¿Por qué mi {s} Samsung se llena de escarcha en {c}?",
         res="Suele venir de sellos que no cierran, puertas que se abren con frecuencia o una falla del sistema de deshielo (resistencia, sensor o tarjeta).",
         causas=["Sellos de la puerta rotos o sucios.", "Puerta que no cierra del todo.", "Falla de la resistencia de deshielo.", "Sensor de deshielo defectuoso.", "Alimentos calientes o sin tapar que aportan humedad.", "Desagüe de deshielo obstruido."],
         pasos=["Limpia los sellos y comprueba que cierren.", "No tapes las rejillas de aire.", "Descongela por completo con el equipo apagado.", "Observa si la escarcha vuelve en pocos días.", "Evita abrir la puerta por largos periodos.", "Si vuelve, pide revisión del deshielo."]),
    dict(sv="lava", sl="no-desagua", tit="{S} Samsung no desagua (código 5E) en {c}", q="¿Por qué mi {s} Samsung no desagua en {c}?",
         res="Casi siempre hay una obstrucción en la manguera o en el filtro de la bomba (monedas, pelusa, medias); si están limpios, la bomba de desagüe puede estar dañada.",
         causas=["Filtro de la bomba tapado.", "Manguera de desagüe doblada o muy alta.", "Bomba de desagüe dañada.", "Objetos pequeños atrapados.", "Desagüe de la casa obstruido.", "Tarjeta electrónica."],
         pasos=["Apaga y desconecta la {s}.", "Revisa la manguera de desagüe.", "Limpia el filtro de la bomba con un recipiente y trapo a mano.", "Quita monedas, botones o pelusa.", "Conecta y prueba un ciclo de desagüe.", "Si sigue, pide revisión de la bomba."]),
    dict(sv="lava", sl="huele-mal", tit="{S} Samsung huele mal en {c}", q="¿Por qué mi {s} Samsung huele mal en {c}?",
         res="Moho en el sello de la puerta, residuos de detergente y humedad atrapada en el tambor; se corrige con limpieza y dejando la puerta entreabierta.",
         causas=["Humedad atrapada tras cerrar la puerta.", "Sello con moho.", "Exceso de detergente o suavizante.", "Filtro de la bomba con restos.", "Cajón de detergente sucio.", "Agua estancada por desagüe lento."],
         pasos=["Limpia el sello con un paño y vinagre o limpiador suave.", "Ejecuta el ciclo de limpieza del tambor (Self Clean, según modelo).", "Limpia el cajón de detergente.", "Limpia el filtro de la bomba.", "Deja la puerta entreabierta tras lavar.", "Usa la cantidad correcta de detergente."]),
    dict(sv="seca", sl="no-seca", tit="{S} Samsung no seca bien en {c}", q="¿Por qué mi {s} Samsung no seca en {c}?",
         res="Casi siempre es el filtro de pelusa o el ducto tapados; si están limpios, puede fallar la resistencia (o bomba de calor), un sensor o la tarjeta.",
         causas=["Filtro de pelusa tapado.", "Ducto de salida con dobleces u obstrucción.", "Sobrecarga del tambor.", "Resistencia o bomba de calor con falla.", "Sensor de temperatura.", "Ropa muy mojada desde la lavadora."],
         pasos=["Limpia el filtro de pelusa.", "Revisa que el ducto no esté doblado ni tapado.", "No sobrecargues el tambor.", "Centrifuga bien la ropa en la lavadora.", "Deja ventilado el espacio de la {s}.", "Si tarda cada vez más, pide revisión."]),
]
PROB_P = []
R_PROB = lambda c, p: f"{c['pk']}/{c['d']}/{slug(pal(c['pk'], p['sv'])[0])}-{p['sl']}/index.html"
for c in CIU:
    if c["amp"]:
        continue
    pk = c["pk"]; P = PAISES[pk]; nom = c["n"]
    for pr in PROB:
        sv = pr["sv"]
        if sv not in SERV_PAIS[pk]:
            continue
        s1, s2 = pal(pk, sv); S1 = cap(s1)
        key = f"pb|{c['s']}|{pr['sl']}"
        f = dict(S=S1, s=s1, c=nom)
        caus = mix(key + "|c", pr["causas"], 4)
        pasos = [x.format(s=s1) for x in mix(key + "|p", pr["pasos"], 4)]
        clima = parrafo_clima(c, c["zonas"][0], sv, key + "|cl")
        preg = [(f"¿Cuánto cuesta reparar una {s1} Samsung que {pr['sl'].replace('-', ' ')} en {nom}?" if False else f"¿Cuánto cuesta el técnico para una {s1} Samsung en {nom}?", "Depende de la falla y del repuesto; se hace el diagnóstico y el valor se confirma antes de reparar."),
                (f"¿Van a domicilio en {nom}?", f"Sí, atendemos en tu casa en {zonas_txt(c)} y otras zonas de {nom}."), (f"¿Puedo seguir usando la {s1} mientras tanto?", "Si hay olor a quemado, ruidos fuertes, agua o chispas, desconéctala; si no, usa lo mínimo hasta la revisión."),
                ("¿Cómo pido la visita?", f"Por WhatsApp al {wa_vis(pk)} o con el formulario de solicitud.")] + preguntas_ia(c, key, 2)
        cuerpo = (hero_simple(f"{nom} · {P['nombre']}", pr["tit"].format(**f), f"Causas, qué revisar y técnico a domicilio en {nom}.", acciones(pk, f"Hola, mi {s1} Samsung falla ({pr['sl'].replace('-', ' ')}) en {nom}"))
                  + qa(pr["q"].format(**f), esc(pr["res"]) + f" En {esc(nom)} ({esc(CLIMA[c['s']]['clima'][:50])}), {esc(efecto_de(c, sv))}.", [("Equipo", S1 + " Samsung"), ("Ciudad", nom), ("Atención", "A domicilio"), ("WhatsApp", wa_vis(pk))])
                  + seccion("Causas más comunes", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in caus) + "</ul>")
                  + seccion("Qué revisar primero", '<ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in pasos) + "</ol>", alt=True)
                  + seccion(f"{esc(nom)}: clima y {esc(s1)}", f"<p>{esc(clima)}</p><p>{esc(uno(key + '|tip', TIPS[sv]))}</p>")
                  + bloque_mitos(key, [sv], 1)
                  + faq_html(preg, f"Preguntas sobre esta falla en {nom}")
                  + seccion("Más información", '<div class="city-tags">' + f'<a href="{R_CS(c, sv)}">{esc(cap(s2))} Samsung en {esc(nom)}</a><a href="{R_CIU(c)}">Centro de servicio técnico Samsung en {esc(nom)}</a><a href="{R_MANT(c)}">Mantenimiento en {esc(nom)}</a>'
                            + "".join(f'<a href="{R_G(g, pk)}">{esc(g["tit"])}</a>' for g in guias_de(sv)[:2]) + "".join(zlink(c, z, f"{z}") for z in c["zonas"][:4]) + "</div>"))
        tt = pr["tit"].format(**f)
        pagina(R_PROB(c, pr), tt, f"{tt}: causas, qué revisar y técnico Samsung a domicilio en {nom}, {P['nombre']}. Valor confirmado antes de reparar.", f"{s1} samsung {pr['sl'].replace('-', ' ')} {nom.lower()}, tecnico {s1} samsung {nom.lower()}",
               [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (nom, R_CIU(c)), (tt, None)], cuerpo, preg, [{"@type": "Article", "headline": tt, "inLanguage": PAISES[pk]["cod"], "datePublished": HOY, "dateModified": HOY, "author": {"@type": "Organization", "name": NOMBRE}, "publisher": {"@id": f"{DOMINIO}/#negocio"}}],
               prio="0.6", pk=pk, tipo="ciudades", ctx=c, compacto=True)
        PROB_P.append((c, pr))


# ---- enlazado desde la ciudad, el país y el hub de cada servicio
def _ins(nombre, html_, antes='<section class="aq-sec alt"><div class="wrap"><h2>Preguntas frecuentes'):
    f = OUT / nombre
    if not f.exists():
        return
    t = f.read_text(encoding="utf-8")
    i = t.find(antes)
    if i < 0:
        i = t.rfind('<footer class="aq-f">')
    f.write_text(t[:i] + html_ + t[i:], encoding="utf-8")


for c in CIU:
    ps = [(cc, pr) for cc, pr in PROB_P if cc is c]
    if ps:
        _ins(R_CIU(c), seccion(f"Fallas frecuentes en {esc(c['n'])}", '<div class="city-tags">' + "".join(f'<a href="{R_PROB(cc, pr)}">{esc(pr["tit"].format(S=cap(pal(c["pk"], pr["sv"])[0]), s=pal(c["pk"], pr["sv"])[0], c=c["n"]))}</a>' for cc, pr in ps) + "</div>", alt=True))
for pk, P in PAISES.items():
    ls = [(sv, ln, u) for k, sv, ln, u in LINEAS_P if k == pk]
    if ls:
        _ins(R_PAIS(pk), seccion(f"Líneas Samsung que reparamos en {esc(P['nombre'])}", '<div class="city-tags">' + "".join(f'<a href="{u}">{esc(cap(pal(pk, sv)[1]))} Samsung {esc(ln)}</a>' for sv, ln, u in ls) + "</div>", alt=True))
        for sv in {x[0] for x in ls}:
            _ins(R_SERV(pk, sv), seccion(f"Líneas de {esc(pal(pk, sv)[1])} Samsung", '<div class="city-tags">' + "".join(f'<a href="{u}">{esc(ln)}</a>' for s_, ln, u in ls if s_ == sv) + "</div>"))
