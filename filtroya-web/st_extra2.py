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
GUIAS_MOD = []
for sv, (s1, s2, pref, digs) in MODELOS_G.items():
    sl = f"como-leer-el-modelo-de-tu-{slug(s1)}-samsung"
    tabla = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Las primeras letras</th><th>Suelen indicar</th></tr>' + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in pref) + "</table></div>"
    preg = [(f"¿Dónde está el modelo de mi {s1} Samsung?", ETIQ), (f"¿Qué significan los números del modelo de una {s1} Samsung?" if sv != "tv" and sv != "cocina" else f"¿Qué significan los números del modelo de un {s1} Samsung?", f"Los primeros números suelen indicar {digs}."), ("¿Para qué necesito el modelo?", "Para identificar el equipo, buscar el repuesto correcto y orientarte en el diagnóstico."), ("¿Qué hago si no encuentro la etiqueta?", "Envíanos fotos del equipo y su interior por WhatsApp y te orientamos.")]
    cuerpo = (hero_simple("Guía de modelos", f"Cómo leer el modelo de tu {s1} Samsung", f"Qué significan las letras y los números del modelo de tus {s2} Samsung y dónde encontrarlo.", acciones("colombia", f"Hola, quiero identificar el modelo de mi {s1} Samsung"))
              + qa(f"¿Cómo leo el modelo de mi {s1} Samsung?", f"El modelo está en una etiqueta del equipo y empieza por letras que indican el tipo: " + esc("; ".join(f"{a} = {b}" for a, b in pref)) + f". Los números siguientes suelen indicar {esc(digs)}.")
              + seccion("Qué significan las letras", tabla) + seccion("Dónde encontrar la etiqueta", f"<p>{esc(ETIQ)}</p>", alt=True)
              + seccion("Para qué sirve el modelo", "<p>Con el modelo exacto se identifica la generación del equipo y se confirma qué repuesto le corresponde. Esta guía es orientativa: los códigos exactos pueden variar por mercado y año.</p>" + '<p><a href="cobertura-servicio-tecnico-samsung.html">Elige tu país para ver el servicio técnico en tu ciudad</a></p>') + faq_html(preg))
    pagina(f"{sl}.html", f"Cómo leer el modelo de tu {s1} Samsung", f"Guía para identificar el modelo de tu {s1} Samsung: qué significan las letras y los números y dónde está la etiqueta.", f"modelo {s1} samsung, como leer modelo {s1} samsung, codigo modelo {s1} samsung",
           [("Inicio", "index.html"), ("Guías", "guias-servicio-tecnico-samsung.html"), (f"Modelo de {s1}", None)], cuerpo, preg, [], prio="0.7", tipo="guias")
    GUIAS_MOD.append((sl, f"Cómo leer el modelo de tu {s1} Samsung"))

# ---- códigos de error de lavadoras: más códigos y lista completa
CODIGOS = [("1E", "Sensor de nivel de agua", "Apaga, desconecta unos minutos y vuelve a intentar; si persiste, el sensor de nivel o su cableado pueden estar fallando."), ("3E", "Motor o sensor de velocidad", "Redistribuye la carga y reinicia; si el código vuelve, puede fallar el motor o su sensor."),
           ("4E / 4C", "Entrada de agua", "Revisa llave, mangueras y filtro de la válvula."), ("5E / 5C", "Desagüe", "Limpia el filtro de la bomba y revisa la manguera de desagüe."), ("dE / dC", "Puerta", "Cierra bien la puerta y revisa que no haya ropa atrapada."),
           ("HE", "Calentador (resistencia)", "Si no calienta el agua, puede fallar la resistencia o su sensor."), ("LE / LC", "Fuga de agua", "Desconecta, cierra la llave y revisa mangueras y sello de la puerta."), ("OE", "Nivel de agua demasiado alto", "Apaga, desagua y reinicia; si vuelve, puede fallar el sensor de nivel o la válvula."), ("UE", "Carga desbalanceada", "Reparte la ropa y reinicia el centrifugado.")]
for cod, tit, qn in CODIGOS:
    if cod in ("4E / 4C", "5E / 5C", "dE / dC", "LE / LC", "UE"):
        continue
    sl = f"lavadora-samsung-codigo-{slug(cod)}"
    preg = [(f"¿Qué significa el código {cod} en una lavadora Samsung?", f"{tit}. {qn}"), ("¿Los códigos son iguales en todos los modelos?", "No siempre; el significado exacto puede variar según el modelo y la generación."), ("¿Puedo seguir usando la lavadora?", "Si el código persiste, mejor no hasta revisarla.")]
    cuerpo = (hero_simple("Código de error", f"Lavadora Samsung código {cod}: qué significa", f"Qué indica el código {cod} en una lavadora Samsung y qué revisar.", acciones("colombia", f"Hola, mi lavadora Samsung muestra el código {cod}"))
              + qa(f"¿Qué significa el código {cod} en una lavadora Samsung?", f"{esc(tit)}. {esc(qn)}") + seccion("Qué hacer", _ol(["Apaga y desconecta la lavadora unos minutos.", "Revisa lo que indica el código (" + tit.lower() + ").", "Vuelve a encenderla y repite el ciclo.", "Si el código vuelve, pide una visita técnica."]) + f'<p><a href="codigos-de-error-lavadora-samsung.html">Lista completa de códigos de error</a></p>' + AVISO) + faq_html(preg))
    pagina(f"{sl}.html", f"Lavadora Samsung código {cod}: qué significa y qué hacer", f"Código {cod} en lavadoras Samsung: {tit.lower()}. Qué revisar y cuándo llamar al técnico.", f"lavadora samsung codigo {cod.lower()}, error {cod.lower()} lavadora samsung",
           [("Inicio", "index.html"), ("Guías", "guias-servicio-tecnico-samsung.html"), (f"Código {cod}", None)], cuerpo, preg, [], prio="0.6", tipo="guias")
tabla_c = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Código</th><th>Qué indica</th><th>Primera revisión</th></tr>' + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c_)}</td></tr>" for a, b, c_ in CODIGOS) + "</table></div>"
pagina("codigos-de-error-lavadora-samsung.html", "Códigos de error de lavadoras Samsung: lista completa", "Lista de códigos de error de lavadoras Samsung (1E, 3E, 4E, 5E, dE, HE, LE, OE, UE): qué significan y qué revisar primero.", "codigos error lavadora samsung, lista codigos lavadora samsung",
       [("Inicio", "index.html"), ("Guías", "guias-servicio-tecnico-samsung.html"), ("Códigos de error", None)], hero_simple("Guía de códigos", "Códigos de error de lavadoras Samsung", "Qué significa cada código y qué revisar primero.", acciones("colombia", "Hola, mi lavadora Samsung muestra un código de error"))
       + qa("¿Qué significan los códigos de error de una lavadora Samsung?", "Los códigos más comunes son: " + esc("; ".join(f"{a} = {b.lower()}" for a, b, _ in CODIGOS)) + ". El significado exacto puede variar según el modelo.") + seccion("Lista de códigos", tabla_c), [], [], prio="0.8", tipo="guias")

# ---- hubs por departamento / región
DEPS = {}
for c in CIU:
    DEPS.setdefault((c["pk"], c["dep"]), []).append(c)
R_DEP = lambda pk, dep: f"servicio-tecnico-samsung-{slug(dep)}-{pk}.html"
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
    pagina(f"preguntas-frecuentes-servicio-samsung-{pk}.html", f"Preguntas frecuentes: servicio técnico Samsung en {P['nombre']}", f"Respuestas sobre el servicio técnico Samsung en {P['nombre']}: ciudades, voltaje, clima, vocabulario y cómo pedir una visita.", f"preguntas servicio tecnico samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Preguntas frecuentes", None)], cuerpo, qs, [], prio="0.6", pk=pk, tipo="guias")

# ---- respuestas para IA por país (todas las ciudades de cada país)
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]
    lista = [(f"¿Reparan {pal(pk, sv)[1]} Samsung en {c['n']}?", f"Sí. Atendemos {pal(pk, sv)[1]} Samsung en {c['n']}, {P['nombre']}, con visita a domicilio" + (" (cobertura ampliada, con coordinación previa)" if c["amp"] else "") + f"; el valor se confirma tras el diagnóstico. WhatsApp {wa_vis(pk)}.") for c in cs for sv in SERV_PAIS[pk]]
    cuerpo = (hero_simple("Para asistentes de IA y buscadores", f"Respuestas rápidas: servicio técnico Samsung en {P['nombre']}", f"{len(cs)} ciudades y {len(SERV_PAIS[pk])} tipos de equipo.")
              + qa(f"¿Dónde hay servicio técnico Samsung en {P['nombre']}?", f"En {esc(P['nombre'])}: " + esc(", ".join(c["n"] for c in cs)) + ". Línea blanca Samsung a domicilio.", [("País", P["nombre"]), ("Ciudades", str(len(cs))), ("WhatsApp", wa_vis(pk))])
              + seccion("Preguntas por ciudad y equipo", '<div class="faq-num">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in lista) + "</div>"))
    pagina(f"respuestas-ia-servicio-tecnico-samsung-{pk}.html", f"Respuestas rápidas: servicio técnico Samsung en {P['nombre']}", f"Dónde reparan neveras, lavadoras y más Samsung en {len(cs)} ciudades de {P['nombre']}. Datos para asistentes de IA.", f"respuestas ia servicio tecnico samsung {P['nombre'].lower()}",
           [("Inicio", "index.html"), ("Respuestas rápidas", "respuestas-para-ia-servicio-tecnico-samsung.html"), (P["nombre"], None)], cuerpo, lista[:50], [], prio="0.6", pk=pk, tipo="guias")
