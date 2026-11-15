# Más contenido en cada página: cómo funciona el servicio, qué incluye y qué no, cuidados según clima, datos de la ubicación y glosario del equipo (se inserta antes de las preguntas frecuentes).
GLOS = {
    "nevera": [("Compresor", "Es el motor que comprime el gas refrigerante y hace circular el frío; si falla, la nevera no enfría."), ("Evaporador", "Es la parte que absorbe el calor del interior; si se llena de hielo, el aire frío no circula."), ("Condensador", "Libera el calor hacia afuera; con polvo acumulado el equipo trabaja de más."), ("Deshielo", "Ciclo que derrite el hielo del evaporador mediante una resistencia, un sensor y la tarjeta."), ("Inverter", "Tecnología que varía la velocidad del compresor para gastar menos energía y hacer menos ruido."), ("Sello de puerta", "Empaque de goma que mantiene el frío adentro; si está gastado se pierde temperatura."), ("Sensor de temperatura", "Mide el frío y le dice a la tarjeta cuándo encender o apagar el compresor."), ("Tarjeta electrónica", "Cerebro del equipo: coordina compresor, ventiladores, deshielo y panel.")],
    "lava": [("Bomba de desagüe", "Saca el agua del tambor; si se tapa o falla aparece el código 5E."), ("Válvula de entrada", "Deja pasar el agua a la lavadora; su filtro suele taparse con sedimento (código 4E)."), ("Amortiguadores", "Absorben el movimiento del tambor al centrifugar; gastados provocan golpes y vibración."), ("Rodamientos", "Permiten girar el tambor; dañados producen un ruido metálico fuerte."), ("Sello de la puerta", "Goma que evita fugas en lavadoras de carga frontal; el moho aparece aquí."), ("Motor inverter", "Motor de velocidad variable de las lavadoras Samsung Digital Inverter."), ("Presostato o sensor de nivel", "Detecta cuánta agua hay en el tambor."), ("Tarjeta de control", "Coordina ciclos, motor, bomba y panel de la lavadora.")],
    "seca": [("Filtro de pelusa", "Atrapa las fibras de la ropa; debe limpiarse en cada uso."), ("Ducto de salida", "Conduce el aire húmedo hacia afuera; si se dobla o se tapa, la secadora tarda más."), ("Resistencia", "Calienta el aire en secadoras de condensación o eléctricas."), ("Bomba de calor", "Sistema eficiente que seca con menos energía en modelos Heat Pump."), ("Termostato", "Corta el calentamiento si la temperatura sube demasiado."), ("Sensor de humedad", "Detecta cuándo la ropa ya está seca para terminar el ciclo."), ("Tambor", "Cilindro donde gira la ropa; lo mueven una banda o un motor y unos rodillos."), ("Condensador", "En equipos sin ducto, convierte el vapor en agua que se recoge en un depósito.")],
    "lavaplatos": [("Brazos rociadores", "Distribuyen el agua por todo el lavavajillas; si se tapan, lava mal."), ("Filtro del fondo", "Retiene restos de comida; hay que limpiarlo con frecuencia."), ("Bomba de circulación", "Impulsa el agua hacia los brazos rociadores."), ("Bomba de desagüe", "Saca el agua sucia al terminar cada fase."), ("Sal y abrillantador", "Ablandan el agua dura y ayudan a secar sin manchas."), ("Resistencia", "Calienta el agua y ayuda a secar."), ("Sello de la puerta", "Evita fugas durante el ciclo."), ("Válvula de entrada", "Controla la entrada de agua desde la llave.")],
    "cocina": [("Quemador", "Parte donde sale el gas y se forma la llama; debe estar limpio y seco."), ("Chispero o encendedor", "Genera la chispa para encender el quemador."), ("Termopar", "Sensor que corta el gas si la llama se apaga, por seguridad."), ("Resistencia del horno", "Elemento que calienta el horno eléctrico."), ("Termostato del horno", "Controla la temperatura interna del horno."), ("Ventilador de convección", "Mueve el aire caliente para cocinar de forma pareja."), ("Sello de la puerta", "Mantiene el calor dentro del horno."), ("Tarjeta de control", "Maneja relojes, temperaturas y programas en hornos con panel digital.")],
    "micro": [("Magnetrón", "Genera las microondas que calientan la comida; si falla, el equipo gira pero no calienta."), ("Diodo de alto voltaje", "Componente que alimenta al magnetrón; no se debe manipular sin técnico."), ("Condensador", "Almacena energía para el circuito de alto voltaje."), ("Guía de ondas", "Conducto que lleva las microondas a la cámara; su tapa de mica puede quemarse."), ("Plato giratorio", "Gira la comida para que se caliente de forma pareja."), ("Seguro de la puerta", "Interruptores que impiden funcionar con la puerta abierta."), ("Fusible", "Protege el circuito; se funde ante una sobrecarga."), ("Tarjeta de control", "Controla tiempo, potencia y panel.")],
    "tv": [("Retroiluminación", "Luces que iluminan la pantalla; si fallan, hay imagen muy oscura."), ("Fuente de poder", "Alimenta todas las partes del televisor; una falla impide encender."), ("Tarjeta principal (main)", "Procesa la imagen, el sonido y las entradas."), ("Tarjeta T-Con", "Envía la señal a los paneles de la pantalla."), ("Panel", "La pantalla en sí; los golpes y las líneas suelen indicar daño."), ("HDMI", "Entrada digital de video y audio."), ("Modo de espera (standby)", "Estado con luz roja o blanca cuando está apagado pero conectado."), ("Protector de voltaje", "Evita que picos de la red dañen la fuente y la tarjeta.")],
}
PASOS_FUNC = [["Escríbenos por WhatsApp al {wa} con el equipo, el modelo y la falla.", "Coordinamos el día y una franja para la visita en {c}.", "El técnico llega a tu casa, revisa el equipo y encuentra la causa.", "Te explica la falla y te confirma el valor antes de empezar.", "Si aceptas, repara y prueba el equipo contigo."],
              ["Cuéntanos por WhatsApp ({wa}) qué le pasa a tu electrodoméstico.", "Agendamos la visita a domicilio en {c} según tu disponibilidad.", "Se hace el diagnóstico en el lugar: nada de llevarlo a un taller sin necesidad.", "Recibes el valor de la reparación antes de que se cambie cualquier pieza.", "Probamos el equipo al terminar y te explicamos cómo cuidarlo."],
              ["Envíanos una foto de la etiqueta del equipo por WhatsApp al {wa}.", "Confirmamos tu dirección en {c} y el horario de la visita.", "El técnico revisa, mide y prueba el equipo en tu casa.", "Te dice qué falla tiene y cuánto costaría repararla.", "Tú decides: si apruebas el valor, se hace la reparación; si no, la visita termina ahí."]]
CUBRE = ["Diagnóstico a domicilio del equipo.", "Explicación clara de la falla y de las opciones.", "Valor de la reparación confirmado antes de empezar.", "Prueba del equipo al terminar el trabajo."]
NO_CUBRE = ["No se cambia ninguna pieza sin tu aprobación.", "La garantía de fábrica la gestiona Samsung o la tienda donde compraste; revisa su vigencia en el manual.", "Si el equipo no tiene arreglo práctico, te lo decimos con honestidad.", "No prometemos tiempos de reparación sin conocer el repuesto."]
CUIDADO_P = {
    "nevera": ["En {c} el clima es {clima}: deja unos centímetros entre la nevera y la pared para que el condensador respire.", "En los meses de lluvia ({ll}), protege la nevera con un regulador de voltaje.", "Revisa los sellos de las puertas cada tres meses; un sello gastado hace trabajar más al compresor.", "No guardes alimentos calientes: suben la humedad y forman escarcha."],
    "lava": ["Deja la puerta entreabierta después de lavar: en {c} ({clima}) la humedad favorece el moho en el sello.", "Limpia el filtro de la bomba cada uno o dos meses.", "Usa la cantidad de detergente que indica el fabricante: el exceso deja residuos.", "Revisa que la lavadora esté nivelada para que no vibre al centrifugar."],
    "seca": ["Limpia el filtro de pelusa después de cada ciclo.", "En los meses de lluvia de {c} ({ll}), la secadora se usa más: revisa el ducto con frecuencia.", "No sobrecargues el tambor: la ropa necesita espacio para girar.", "Mantén ventilado el lugar donde está la secadora."],
    "lavaplatos": ["Limpia el filtro del fondo cada semana si lo usas a diario.", "Si el agua en {c} deja manchas, revisa la sal y el abrillantador.", "Quita los restos grandes de comida antes de cargar los platos.", "Ejecuta un ciclo de limpieza una vez al mes."],
    "cocina": ["Limpia los quemadores y el chispero cuando estén fríos.", "Con la humedad de {c} ({clima}), seca bien los quemadores antes de encender.", "Revisa las mangueras de gas y su fecha de vencimiento.", "No cubras el fondo del horno con papel de aluminio: afecta el flujo de calor."],
    "micro": ["Limpia el interior con un paño húmedo y deja la puerta entreabierta para que se seque.", "No lo uses vacío ni con recipientes metálicos.", "Evita golpear la puerta: el seguro y el sello son críticos.", "Conéctalo directamente a la toma, sin regletas delgadas."],
    "tv": ["Usa un protector de voltaje: en {c} las tormentas de los meses de lluvia ({ll}) dejan picos de energía.", "Mantén ventilado el espacio detrás del televisor.", "Limpia la pantalla con un paño de microfibra seco o apenas húmedo.", "Desconéctalo en tormentas eléctricas fuertes."],
}


def _datos(c):
    pk = c["pk"]; cl = CLIMA[c["s"]]; v = VOLT[pk]
    filas = [("Ciudad", f"{c['n']}, {c['dep']}"), ("Clima", cl["clima"]), ("Meses de más lluvia", cl["lluvia"]), ("Red eléctrica", f"{v[0]} · {v[1]}"), ("WhatsApp", wa_vis(pk)), ("Atención", "A domicilio")]
    if cl.get("alt"):
        filas.insert(2, ("Altitud aproximada", f"{alt_txt(cl)} m"))
    if c["zonas"]:
        filas.append(("Zonas con subpágina" if c["zp"] else "Sectores", ", ".join(c["zonas"][:6])))
    return '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in filas) + "</table></div>"


def _como(c, key):
    wa = wa_vis(c["pk"])
    return '<ol class="vl">' + "".join(f"<li>{esc(x.format(c=c['n'], wa=wa))}</li>" for x in uno(key + "|pf", PASOS_FUNC)) + "</ol>"


def _cubre(key):
    return '<div class="tbl-wrap"><table class="spec-table"><tr><th>La visita incluye</th><th>Importante saber</th></tr><tr><td>' + "<br>".join("• " + esc(x) for x in mix(key + "|ci", CUBRE, 4)) + "</td><td>" + "<br>".join("• " + esc(x) for x in mix(key + "|nc", NO_CUBRE, 3)) + "</td></tr></table></div>"


def _glos(sv, key, n=4):
    return '<dl class="glos">' + "".join(f"<dt><b>{esc(t)}</b></dt><dd>{esc(d)}</dd>" for t, d in mix(key + "|g", GLOS[sv], n)) + "</dl>"


def _cuidado(c, sv, key, n=3):
    cl = CLIMA[c["s"]]
    return _ul2([x.format(c=c["n"], clima=cl["clima"][:60], ll=cl["lluvia"]) for x in mix(key + "|cu", CUIDADO_P[sv], n)])


for _c in CIU:
    _pk = _c["pk"]; _P = PAISES[_pk]
    k0 = f"e6|{_c['s']}"
    _ins(R_CIU(_c), seccion(f"Cómo funciona el servicio técnico Samsung en {esc(_c['n'])}", _como(_c, k0)) + seccion(f"Datos de {esc(_c['n'])} que influyen en tus electrodomésticos", _datos(_c), alt=True) + seccion("Qué incluye la visita y qué debes saber", _cubre(k0)))
    for _sv in SERV_PAIS[_pk]:
        _s1, _s2 = pal(_pk, _sv); k1 = f"{k0}|{_sv}"
        _ins(R_CS(_c, _sv), seccion(f"Cuidados para tu {esc(_s1)} Samsung en {esc(_c['n'])}", _cuidado(_c, _sv, k1)) + seccion(f"Glosario: partes de tu {esc(_s1)} Samsung", _glos(_sv, k1), alt=True) + seccion("Cómo funciona la visita", _como(_c, k1)) + seccion("Qué incluye y qué debes saber", _cubre(k1), alt=True))
    for _t, _u in (("wa", R_WA(_c)), ("tel", R_TEL(_c))):
        _ins(_u, seccion(f"Cómo pedir tu visita en {esc(_c['n'])}", _como(_c, k0 + _t)) + seccion(f"Datos de {esc(_c['n'])}", _datos(_c), alt=True))
for _c, _z in ZONAS_P:
    k = f"e6z|{_c['s']}|{_z}"
    _ins(R_Z(_c, _z), seccion(f"Cómo funciona el servicio en {esc(_z)}", _como(_c, k)) + seccion(f"Datos de {esc(_c['n'])}", _datos(_c), alt=True) + seccion("Qué incluye la visita", _cubre(k)))
for _c, _pr in PROB_P:
    k = f"e6p|{_c['s']}|{_pr['sl']}|{_pr['sv']}"
    _s1 = pal(_c["pk"], _pr["sv"])[0]
    _ins(R_PROB(_c, _pr), seccion(f"Glosario: partes que intervienen en esta falla", _glos(_pr["sv"], k)) + seccion(f"Cómo funciona la visita en {esc(_c['n'])}", _como(_c, k), alt=True) + seccion("Qué incluye y qué debes saber", _cubre(k)) + seccion(f"Cuidados para tu {esc(_s1)} en {esc(_c['n'])}", _cuidado(_c, _pr["sv"], k), alt=True))
for _pk, _P in PAISES.items():
    cs_ = CIU_PAIS[_pk]; v = VOLT[_pk]
    _ins(R_PAIS(_pk), seccion(f"Cómo funciona el servicio técnico Samsung en {esc(_P['nombre'])}", '<ol class="vl">' + "".join(f"<li>{esc(x.format(c=_P['nombre'], wa=wa_vis(_pk)))}</li>" for x in uno(f"e6|{_pk}|pf", PASOS_FUNC)) + "</ol>")
         + seccion(f"Datos de {esc(_P['nombre'])}", f'<div class="tbl-wrap"><table class="spec-table"><tr><td><b>Ciudades</b></td><td>{esc(", ".join(c["n"] for c in cs_))}</td></tr><tr><td><b>Red eléctrica</b></td><td>{esc(v[0])} · {esc(v[1])} · enchufes {esc(v[2])}</td></tr><tr><td><b>WhatsApp</b></td><td>{esc(wa_vis(_pk))}</td></tr><tr><td><b>Equipos</b></td><td>{esc(", ".join(pal(_pk, s_)[1] for s_ in SERV_PAIS[_pk]))}</td></tr></table></div>', alt=True)
         + seccion("Qué incluye la visita y qué debes saber", _cubre(f"e6|{_pk}")))
    for _sv in SERV_PAIS[_pk]:
        _s1 = pal(_pk, _sv)[0]
        _ins(R_SERV(_pk, _sv), seccion(f"Glosario: partes de tu {esc(_s1)} Samsung", _glos(_sv, f"e6h|{_pk}|{_sv}", 6)) + seccion("Qué incluye la visita y qué debes saber", _cubre(f"e6h|{_pk}|{_sv}"), alt=True))
    for _t, _u in (("wa", R_WAP(_pk)), ("tel", R_TELP(_pk))):
        _ins(_u, seccion(f"Datos de {esc(_P['nombre'])}", f'<p>{esc(_P["nombre"])}: red de {esc(v[0])} a {esc(v[1])}. Ciudades: {esc(", ".join(c["n"] for c in cs_))}.</p>') + seccion("Qué incluye la visita", _cubre(f"e6{_t}|{_pk}"), alt=True))
for _pk in PAISES:
    for _g in GUIAS_PK(_pk):
        _ins(R_G(_g, _pk), seccion("Glosario de partes", _glos(_g["serv"], f"e6g|{_pk}|{_g['slug']}", 5)) + seccion("Qué incluye la visita", _cubre(f"e6g|{_pk}|{_g['slug']}"), alt=True))
