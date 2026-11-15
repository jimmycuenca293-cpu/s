# Más autoridad temática: cómo leer el modelo, códigos de error, hubs por departamento, preguntas por país y respuestas para IA por país (se ejecuta antes de st_salida.py).
# ---- cómo leer el modelo de cada equipo Samsung
ETIQ = "La etiqueta del modelo suele estar dentro del equipo (puerta, pared lateral o techo en neveras; marco de la puerta en lavadoras y secadoras) o en la parte trasera. Tómale una foto: con ella te orientamos más rápido."
MODELOS_G = {
    "nevera": ("nevera", "neveras", [("RT", "congelador arriba (top mount)"), ("RB", "congelador abajo (bottom mount)"), ("RS", "dos puertas lado a lado (side by side)"), ("RF", "French door: dos puertas arriba y cajón de congelador abajo")], "capacidad aproximada (en litros o en pies cúbicos, según el mercado)"),
    "lava": ("lavadora", "lavadoras", [("WW", "carga frontal"), ("WF", "carga frontal"), ("WA", "carga superior"), ("WD", "lavasecadora")], "capacidad de lavado aproximada en kilos (por ejemplo, 90 suele indicar 9 kg)"),
    "seca": ("secadora", "secadoras", [("DV", "secadora de ropa")], "capacidad aproximada en kilos (por ejemplo, 90 suele indicar 9 kg)"),
    "lavaplatos": ("lavavajillas", "lavavajillas", [("DW", "lavavajillas")], "el ancho o la capacidad del equipo (por ejemplo, 60 suele indicar 60 cm)"),
    "cocina": ("cocina", "cocinas, estufas y hornos", [("NE / NX", "cocinas y estufas"), ("NV / NQ", "hornos empotrados"), ("NA / NZ", "placas (cooktops)")], "el tamaño y la configuración del equipo"),
    "micro": ("microondas", "microondas", [("MS / ME", "microondas solo"), ("MG", "microondas con grill"), ("MC", "microondas con convección")], "la capacidad aproximada en litros"),
    "tv": ("televisor", "televisores", [("UN / QN", "modelos de Estados Unidos y gran parte de Latinoamérica (LED y QLED)"), ("UE / QE", "modelos de Europa (LED y QLED)")], "el tamaño de pantalla en pulgadas (por ejemplo, 55 o 65)"),
}

def _cod_tab():
    return '<div class="tbl-wrap"><table class="spec-table"><tr><th>Código</th><th>Qué indica</th><th>Primera revisión</th></tr>' + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c_)}</td></tr>" for a, b, c_ in CODIGOS) + "</table></div>"


CODIGOS = [("1E", "Sensor de nivel de agua", "Apaga, desconecta unos minutos y vuelve a intentar; si persiste, el sensor de nivel o su cableado pueden estar fallando."), ("3E", "Motor o sensor de velocidad", "Redistribuye la carga y reinicia; si el código vuelve, puede fallar el motor o su sensor."),
           ("4E / 4C", "Entrada de agua", "Revisa llave, mangueras y filtro de la válvula."), ("5E / 5C", "Desagüe", "Limpia el filtro de la bomba y revisa la manguera de desagüe."), ("dE / dC", "Puerta", "Cierra bien la puerta y revisa que no haya ropa atrapada."),
           ("HE", "Calentador (resistencia)", "Si no calienta el agua, puede fallar la resistencia o su sensor."), ("LE / LC", "Fuga de agua", "Desconecta, cierra la llave y revisa mangueras y sello de la puerta."), ("OE", "Nivel de agua demasiado alto", "Apaga, desagua y reinicia; si vuelve, puede fallar el sensor de nivel o la válvula."), ("UE", "Carga desbalanceada", "Reparte la ropa y reinicia el centrifugado.")]
INTRO_L = ["En {pais} atendemos esta consulta en {ciu}: escribe al {wa} con una foto de la etiqueta o de la pantalla.",
           "Si estás en {ciu} u otra ciudad de {pais}, el técnico llega a tu casa; coordina por WhatsApp ({wa}).",
           "En {pais} la red es de {v0}: si el equipo muestra fallas sin patrón, revisa también el voltaje de tu tomacorriente antes de la visita.",
           "Atendemos {pais} con visita a domicilio ({ciu}, entre otras). El valor se confirma después del diagnóstico."]
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; v = VOLT[pk]; lav1, lav2 = pal(pk, "lava")
    f_ = dict(pais=P["nombre"], v0=v[0], ciu=", ".join(c["n"] for c in cs[:3]), wa=wa_vis(pk))
    ciu_tags = '<div class="city-tags">' + "".join(f'<a href="{R_CIU(c)}">{esc(c["n"])}</a>' for c in cs) + "</div>"
    # ---- cómo leer el modelo
    for sv in SERV_PAIS[pk]:
        _, _, pref, digs = MODELOS_G[sv]; s1, s2 = pal(pk, sv)
        tabla = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Las primeras letras</th><th>Suelen indicar</th></tr>' + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in pref) + "</table></div>"
        art = "una" if s1.endswith("a") else "un"
        preg = [(f"¿Dónde está el modelo de mi {s1} Samsung?", loc(ETIQ, pk)), (f"¿Qué significan los números del modelo de {art} {s1} Samsung?", f"Los primeros números suelen indicar {digs}."), ("¿Para qué necesito el modelo?", "Para identificar el equipo, buscar el repuesto correcto y orientarte en el diagnóstico."), ("¿Qué hago si no encuentro la etiqueta?", f"Envíanos fotos del equipo y su interior por WhatsApp al {wa_vis(pk)} y te orientamos.")]
        cuerpo = (hero_simple(f"{P['bandera']} Guía de modelos · {P['nombre']}", f"Cómo leer el modelo de tu {s1} Samsung", f"Qué significan las letras y los números del modelo de tus {s2} Samsung y dónde encontrarlo.", acciones(pk, f"Hola, quiero identificar el modelo de mi {s1} Samsung"))
                  + qa(f"¿Cómo leo el modelo de mi {s1} Samsung?", f"El modelo está en una etiqueta del equipo y empieza por letras que indican el tipo: " + esc("; ".join(f"{a} = {b}" for a, b in pref)) + f". Los números siguientes suelen indicar {esc(digs)}.")
                  + seccion("Qué significan las letras", tabla) + seccion("Dónde encontrar la etiqueta", f"<p>{esc(loc(ETIQ, pk))}</p>", alt=True)
                  + seccion("Para qué sirve el modelo", "<p>Con el modelo exacto se identifica la generación del equipo y se confirma qué repuesto le corresponde. Esta guía es orientativa: los códigos exactos pueden variar por mercado y año.</p><p>" + esc(uno(f"il|{pk}|{sv}", INTRO_L).format(**f_)) + "</p>")
                  + seccion(f"Servicio técnico de {esc(s2)} Samsung en {esc(P['nombre'])}", f'<p><a href="{R_SERV(pk, sv)}">Ver el servicio de {esc(s2)} Samsung en {esc(P["nombre"])}</a></p>' + ciu_tags, alt=True) + faq_html(preg))
        pagina(R_MOD(pk, sv), f"Cómo leer el modelo de tu {s1} Samsung | {P['nombre']}", f"Guía para identificar el modelo de tu {s1} Samsung en {P['nombre']}: qué significan las letras y los números y dónde está la etiqueta.", f"modelo {s1} samsung, como leer modelo {s1} samsung, codigo modelo {s1} samsung {P['nombre'].lower()}",
               [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Guías", R_GUIAS(pk)), (f"Modelo de {s1}", None)], cuerpo, preg, [], prio="0.7", pk=pk, tipo="guias")
    # ---- códigos de error de lavadoras
    for cod, tit, qn in CODIGOS:
        if cod in ("4E / 4C", "5E / 5C", "dE / dC", "LE / LC", "UE"):
            continue
        preg = [(f"¿Qué significa el código {cod} en una {lav1} Samsung?", f"{tit}. {qn}"), ("¿Los códigos son iguales en todos los modelos?", "No siempre; el significado exacto puede variar según el modelo y la generación."), (f"¿Puedo seguir usando la {lav1}?", "Si el código persiste, mejor no hasta revisarla.")]
        cuerpo = (hero_simple(f"{P['bandera']} Código de error · {P['nombre']}", f"{cap(lav1)} Samsung código {cod}: qué significa", f"Qué indica el código {cod} en una {lav1} Samsung y qué revisar.", acciones(pk, f"Hola, mi {lav1} Samsung muestra el código {cod}"))
                  + qa(f"¿Qué significa el código {cod} en una {lav1} Samsung?", f"{esc(tit)}. {esc(qn)}") + seccion("Qué hacer", _ol([f"Apaga y desconecta la {lav1} unos minutos.", "Revisa lo que indica el código (" + tit.lower() + ").", "Vuelve a encenderla y repite el ciclo.", "Si el código vuelve, pide una visita técnica."]) + f'<p><a href="{R_COD_LISTA(pk)}">Lista completa de códigos de error</a></p>' + AVISO)
                  + seccion(f"Si estás en {esc(P['nombre'])}", "<p>" + esc(uno(f"ic|{pk}|{cod}", INTRO_L).format(**f_)) + "</p>" + ciu_tags, alt=True) + faq_html(preg))
        pagina(R_COD(pk, cod), f"{cap(lav1)} Samsung código {cod}: qué significa y qué hacer en {P['nombre']}", f"Código {cod} en {lav2} Samsung: {tit.lower()}. Qué revisar y cuándo llamar al técnico en {P['nombre']}.", f"{lav1} samsung codigo {cod.lower()}, error {cod.lower()} {lav1} samsung {P['nombre'].lower()}",
               [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Guías", R_GUIAS(pk)), (f"Código {cod}", None)], cuerpo, preg, [], prio="0.6", pk=pk, tipo="guias")
    pagina(R_COD_LISTA(pk), f"Códigos de error de {lav2} Samsung en {P['nombre']}: lista", f"Lista de códigos de error de {lav2} Samsung (1E, 3E, 4E, 5E, dE, HE, LE, OE, UE): qué significan y qué revisar primero. Servicio en {P['nombre']}.", f"codigos error {lav1} samsung, lista codigos {lav1} samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Guías", R_GUIAS(pk)), ("Códigos de error", None)], hero_simple(f"{P['bandera']} Guía de códigos · {P['nombre']}", f"Códigos de error de {lav2} Samsung", "Qué significa cada código y qué revisar primero.", acciones(pk, f"Hola, mi {lav1} Samsung muestra un código de error"))
           + qa(f"¿Qué significan los códigos de error de una {lav1} Samsung?", "Los códigos más comunes son: " + esc("; ".join(f"{a} = {b.lower()}" for a, b, _ in CODIGOS)) + ". El significado exacto puede variar según el modelo.") + seccion("Lista de códigos", _cod_tab()) + seccion(f"Servicio en {esc(P['nombre'])}", ciu_tags, alt=True), [], [], prio="0.8", pk=pk, tipo="guias")

# ---- hubs por departamento / región
DEPS = {}
for c in CIU:
    DEPS.setdefault((c["pk"], c["dep"]), []).append(c)
R_DEP = lambda pk, dep: f"{pk}/region-{slug(dep)}/index.html"
DEP_HUBS = []
for (pk, dep), cs in DEPS.items():
    if len(cs) < 2:
        continue
    P = PAISES[pk]; key = f"d|{pk}|{dep}"
    filas = "".join(f'<tr><td><a href="{R_CIU(c)}">{esc(c["n"])}</a></td><td>{esc(CLIMA[c["s"]]["clima"][:60])}</td><td>{esc(alt_txt(CLIMA[c["s"]]) + " m" if CLIMA[c["s"]].get("alt") else "—")}</td><td>{"Ampliada" if c["amp"] else "Directa"}</td></tr>' for c in cs)
    zs = [(c, z) for c in cs if c["zp"] for z in c["zonas"]]
    preg = [(f"¿Hay servicio técnico Samsung en {dep}?", f"Sí: atendemos " + ", ".join(c["n"] for c in cs) + f" (en {P['nombre']})."), (f"¿Qué equipos reparan en {dep}?", ", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk]).capitalize() + "."), ("¿Cómo pido la visita?", f"Por WhatsApp al {wa_vis(pk)} o con el formulario.")]
    cuerpo = (hero_simple(f"{dep} · {P['nombre']}", f"Servicio técnico Samsung en {dep}", f"Línea blanca Samsung a domicilio en {len(cs)} ciudades de {dep}, {P['nombre']}.", acciones(pk, f"Hola, necesito servicio técnico Samsung en {dep}"))
              + qa(f"¿Hay servicio técnico Samsung en {dep}?", f"Sí. En {esc(dep)} ({esc(P['nombre'])}) atendemos {esc(', '.join(c['n'] for c in cs))}: " + esc(", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk])) + " Samsung a domicilio.", [("Departamento", dep), ("Ciudades", str(len(cs))), ("WhatsApp", wa_vis(pk))])
              + seccion(f"Ciudades de {esc(dep)}", '<div class="tbl-wrap"><table class="spec-table"><tr><th>Ciudad</th><th>Clima</th><th>Altitud</th><th>Cobertura</th></tr>' + filas + "</table></div>")
              + (seccion("Zonas con subpágina", '<div class="city-tags">' + "".join(f'<a href="{R_Z(c, z)}">{esc(z)} · {esc(c["n"])}</a>' for c, z in zs[:40]) + "</div>", alt=True) if zs else "") + faq_html(preg))
    pagina(R_DEP(pk, dep), f"Servicio técnico Samsung en {dep} ({P['nombre']})", f"Servicio técnico Samsung a domicilio en {dep}: " + ", ".join(c["n"] for c in cs[:6]) + f". Línea blanca Samsung en {P['nombre']}.", f"servicio tecnico samsung {dep.lower()}, reparacion samsung {dep.lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), (dep, None)], cuerpo, preg, [], prio="0.7", pk=pk, tipo="paises", ctx=cs[0] if len(cs) == 1 else None)
    DEP_HUBS.append((pk, dep))
# enlazar los hubs desde la página de cada país
for pk, P in PAISES.items():
    hubs = [dep for (k, dep) in DEP_HUBS if k == pk]
    if not hubs:
        continue
    f = OUT / R_PAIS(pk)
    t = f.read_text(encoding="utf-8")
    bloque = seccion(f"Servicio técnico por departamento en {esc(P['nombre'])}", '<div class="city-tags">' + "".join(f'<a href="{R_DEP(pk, d)}">{esc(d)}</a>' for d in hubs) + "</div>", alt=True)
    i = t.find('<section class="aq-sec alt"><div class="wrap"><h2>Preguntas frecuentes')
    f.write_text(t[:i] + bloque + t[i:] if i > 0 else t, encoding="utf-8")

# ---- preguntas frecuentes por país
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; v = VOLT[pk]; cap_c = cs[0]; cl = CLIMA[cap_c["s"]]
    qs = [(f"¿Hay servicio técnico Samsung en {P['nombre']}?", f"Sí, en " + ", ".join(c["n"] for c in cs[:12]) + (f" y {len(cs) - 12} ciudades más" if len(cs) > 12 else "") + "."), (f"¿Cómo se dice «refrigerador» en {P['nombre']}?", f"Se dice «{pal(pk, 'nevera')[0]}»."),
          (f"¿Cómo se dice «lavadora» en {P['nombre']}?", f"Se dice «{pal(pk, 'lava')[0]}»."), (f"¿Qué voltaje tiene {P['nombre']}?", f"{v[0]} a {v[1]}, con enchufes {v[2]}."),
          (f"¿Cómo es el clima en {cap_c['n']} y cómo afecta a los electrodomésticos?", f"{cap_c['n']} tiene un clima {cl['clima']}; {efecto_de(cap_c, 'nevera')}."), (f"¿Qué equipos Samsung reparan en {P['nombre']}?", ", ".join(pal(pk, s)[1] for s in SERV_PAIS[pk]).capitalize() + "."),
          (f"¿Reparan televisores Samsung en {P['nombre']}?", "Sí, a domicilio." if PAISES[pk]["tv"] else f"En {P['nombre']} nos enfocamos en línea blanca; los televisores no forman parte del servicio."), (f"¿Cuánto cuesta una reparación en {P['nombre']}?", "Depende de la falla y del repuesto; el valor se confirma después del diagnóstico y antes de reparar."),
          ("¿La visita es a domicilio?", "Sí, el técnico va a tu casa o apartamento."), (f"¿Cómo pido una visita en {P['nombre']}?", f"Por WhatsApp al {wa_vis(pk)} o con el formulario de solicitud."),
          (f"¿Reparan equipos comprados en otro país?", f"Los revisamos; antes verifica la placa del equipo, porque en {P['nombre']} la red es de {v[0]} y {v[1]}."), (f"¿Atienden fuera de {cap_c['n']}?", "Sí, en las ciudades de cobertura directa y, con coordinación previa, en las de cobertura ampliada.")]
    cuerpo = (hero_simple(f"{P['bandera']} {P['nombre']}", f"Preguntas frecuentes del servicio técnico Samsung en {P['nombre']}", "Vocabulario local, electricidad, clima y cobertura.", acciones(pk, f"Hola, tengo una pregunta sobre servicio Samsung en {P['nombre']}"))
              + qa(f"¿Qué debo saber del servicio técnico Samsung en {P['nombre']}?", f"En {esc(P['nombre'])} atendemos {esc(', '.join(c['n'] for c in cs[:8]))}. Usamos el vocabulario local ({esc(pal(pk, 'nevera')[0])}, {esc(pal(pk, 'lava')[0])}) y la red es de {v[0]} a {v[1]}.") + faq_html(qs))
    pagina(R_FAQ(pk), f"Preguntas frecuentes: servicio técnico Samsung en {P['nombre']}", f"Respuestas sobre el servicio técnico Samsung en {P['nombre']}: ciudades, voltaje, clima, vocabulario y cómo pedir una visita.", f"preguntas servicio tecnico samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Preguntas frecuentes", None)], cuerpo, qs, [], prio="0.6", pk=pk, tipo="guias")

# ---- respuestas para IA por país (todas las ciudades de cada país)
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]
    lista = [(f"¿Reparan {pal(pk, sv)[1]} Samsung en {c['n']}?", f"Sí. Atendemos {pal(pk, sv)[1]} Samsung en {c['n']}, {P['nombre']}, con visita a domicilio" + (" (cobertura ampliada, con coordinación previa)" if c["amp"] else "") + f"; el valor se confirma tras el diagnóstico. WhatsApp {wa_vis(pk)}.") for c in cs for sv in SERV_PAIS[pk]]
    cuerpo = (hero_simple("Para asistentes de IA y buscadores", f"Respuestas rápidas: servicio técnico Samsung en {P['nombre']}", f"{len(cs)} ciudades y {len(SERV_PAIS[pk])} tipos de equipo.")
              + qa(f"¿Dónde hay servicio técnico Samsung en {P['nombre']}?", f"En {esc(P['nombre'])}: " + esc(", ".join(c["n"] for c in cs)) + ". Línea blanca Samsung a domicilio.", [("País", P["nombre"]), ("Ciudades", str(len(cs))), ("WhatsApp", wa_vis(pk))])
              + seccion("Preguntas por ciudad y equipo", '<div class="faq-num">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in lista) + "</div>"))
    pagina(R_IA(pk), f"Respuestas rápidas: servicio técnico Samsung en {P['nombre']}", f"Dónde reparan neveras, lavadoras y más Samsung en {len(cs)} ciudades de {P['nombre']}. Datos para asistentes de IA.", f"respuestas ia servicio tecnico samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Respuestas rápidas", None)], cuerpo, lista[:50], [], prio="0.6", pk=pk, tipo="guias")
