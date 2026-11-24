"""Contenido esencial adicional por tipo de página (solo sitios con CFG['esencial']).
Todo se arma con los datos reales de cada marca (fallas, etiquetas, mantenimiento, técnica) y con texto
general de buen sentido: no se inventan precios, plazos, horarios, garantías ni direcciones."""
import re


def _lista(items, tag="ul"):
    return f"<{tag}>" + "".join(f"<li>{x}</li>" for x in items) + f"</{tag}>"


def _oraciones(t, n=2):
    ps = re.split(r"(?<=[.!?])\s+", (t or "").strip())
    return " ".join(ps[:n])


def _min(t):
    t = (t or "").strip()
    return t[0].lower() + t[1:] if len(t) > 1 and t[0].isupper() and t[1].islower() else t


def _eqs(d, filtro=None):
    es = list(d["equipos"])
    if filtro:
        f = [e for e in es if e in filtro]
        return f or es
    return es


SEGURIDAD_NO = [
    "Abrir paneles, tapas o la parte trasera con el equipo conectado.",
    "Puentear fusibles, protectores o sensores para que «arranque».",
    "Subir y bajar el breaker varias veces seguidas: puede dañar la placa.",
    "Seguir usando el equipo si huele a quemado, hay chispas o hay agua cerca de las conexiones.",
]
SEGURIDAD_SI = [
    "Comprobar que el equipo esté bien conectado y que el tomacorriente tenga energía (prueba con otro aparato).",
    "Revisar que el breaker no haya saltado y que la llave de agua, si el equipo usa agua, esté abierta.",
    "Anotar el código o mensaje que muestra la pantalla y cuándo empezó la falla.",
    "Tomar una foto de la etiqueta con el modelo y, si puedes, un video corto del problema.",
    "Despejar el espacio alrededor del equipo para que el técnico pueda moverlo con seguridad.",
]


def esencial(path, m, X):
    """Devuelve (html, faqs) para la página `path` de la marca `m`; ('' , []) si no corresponde."""
    sec, faq_html, cap, esc, pathb, junta = X["sec"], X["faq_html"], X["cap"], X["esc"], X["pathb"], X["junta"]
    d = X["M"][m]; N = d["nombre"]; ciu = X["ciudad"]; tel = X["tel"]; EQ = X["EQ"]
    partes = [p for p in path.split("/") if p]
    slug = partes[1] if len(partes) > 1 and partes[0] == X["base_slug"](m) else (partes[-1] if partes else "")
    eqn = lambda e: EQ[e][2]
    fallas = d.get("fallas", {}); eti = d.get("etiqueta", {}); tech = d.get("tech", {})
    out = []; faqs = []

    if slug == "diagnostico-por-sintoma":
        out.append(sec(f"Cómo usar el diagnóstico de equipos {N}", _lista([
            f"Elige el equipo ({', '.join(EQ[x][1] for x in _eqs(d)[:3])}…) en el primer campo.",
            "Elige lo que notas: un ruido, un código en pantalla, una fuga, un olor.",
            "Compara la causa más probable con lo que ves en tu equipo y revisa lo que puedes comprobar sin riesgo.",
            "Si el síntoma sigue, escríbenos con el modelo y la foto de la etiqueta para coordinar la visita.",
        ], "ol")))
        bloq = ""
        for e in _eqs(d):
            fs = (fallas.get(e) or [])[:3]
            if fs:
                bloq += f"<h3>{cap(eqn(e))} {N}</h3>" + _lista([f"<b>{esc(s)}</b>. Causa probable: {esc(_min(c))}" for s, c, _r in fs])
        if bloq: out.append(sec(f"Síntomas más consultados en equipos {N}", bloq, alt=True, lead=f"Estas son las fallas que más vemos en {junta(eqn(e) for e in d['equipos'])} {N} en {ciu}. Son causas probables: se confirman con pruebas en el equipo."))
        out.append(sec("Qué puedes revisar tú, sin riesgo", _lista(SEGURIDAD_SI) + "<h3>Qué no debes hacer</h3>" + _lista(SEGURIDAD_NO)))
        et = "".join(f"<li><b>{cap(eqn(e))} {N}:</b> {esc(eti[e])}</li>" for e in _eqs(d) if eti.get(e))
        if et: out.append(sec(f"Dónde está el modelo de tu equipo {N}", f"<p>El modelo y el número de serie están en una etiqueta. Con ese dato el técnico puede preparar la visita.</p><ul>{et}</ul>" + (f"<p>{esc(d['modelo_ej'])}</p>" if d.get("modelo_ej") else ""), alt=True))
        faqs = [
            (f"¿El diagnóstico por síntoma reemplaza la visita del técnico {N}?", "No. Es una guía para entender la causa más probable y qué revisar. La causa real se confirma con pruebas en el equipo, en la visita."),
            ("¿Qué hago si mi síntoma no aparece en la lista?", f"Escríbenos por WhatsApp o llama al {tel} y cuéntanos qué hace el equipo, el modelo y desde cuándo. Con esos datos te orientamos."),
            ("¿Puedo seguir usando el equipo mientras espero la visita?", "Si no hay olor a quemado, chispas, saltos del breaker ni agua cerca de las conexiones, puedes usarlo con cuidado. Ante cualquiera de esas señales, desconéctalo y no lo uses hasta la revisión."),
        ]

    elif slug == "cobertura":
        zx = X["zx"]; zonas = X["ZONAS"]
        bl = ""
        for z, zv in zonas.items():
            t = zx.get(z)
            if t:
                bl += f"<h3>{esc(zv[0])}</h3><p>Incluye {esc(t[2])}. Predominan {esc(t[0])}. Al coordinar la visita de equipos {N} tenemos en cuenta {esc(t[1])}.</p>"
        out.append(sec(f"Cómo es la visita de equipos {N} en cada zona", bl, lead=f"{X['intro_clima']} Por eso la visita se coordina según la zona y la franja que elijas."))
        out.append(sec(f"Equipos {N} que atendemos en {ciu} y su área metropolitana", f"<p>Atendemos {junta(eqn(e) for e in d['equipos'])} de la marca {N}." + (f" Entre las líneas más comunes están {junta(d['lineas'][:5])}." if d.get("lineas") else "") + "</p>", alt=True))
        out.append(sec("Lo que acelera la visita", _lista([
            "El modelo del equipo (foto de la etiqueta) y la marca.",
            "El código o mensaje de la pantalla, si lo hay, y desde cuándo ocurre.",
            "El barrio o conjunto y si hay portería o control de acceso, para avisar con tiempo.",
            "Una persona adulta en casa durante la visita y el espacio libre alrededor del equipo.",
        ])))
        faqs = [
            ("¿Cómo sé si mi barrio está cubierto?", f"Escríbenos tu barrio y el equipo por WhatsApp o llama al {tel}. Confirmamos si podemos atenderte y coordinamos día y franja."),
            (f"¿Atienden equipos {N} en todo el área metropolitana?", f"Sí, en el área metropolitana: {X['zlista']}. En las zonas más lejanas la franja se coordina con más anticipación."),
            ("¿Cómo agendo la visita?", "Por WhatsApp o por teléfono. Te preguntamos marca, modelo y qué hace el equipo, y acordamos el día y la franja."),
        ]

    elif slug == "guias":
        out.append(sec(f"Cuidados esenciales para equipos {N}", _lista([esc(x) for x in d.get("mantenimiento", [])[:6]]), lead=f"Hábitos simples que alargan la vida de tus equipos {N} y evitan visitas innecesarias."))
        out.append(sec(f"Qué cambia con el clima de {ciu}", f"<p>{esc(X['intro_clima'])}</p><p>{esc(X.get("clima_extra") or "Las tormentas eléctricas pueden provocar picos de voltaje que dañan placas electrónicas. Un protector de voltaje adecuado y desconectar los equipos más sensibles durante tormentas fuertes reduce ese riesgo. La humedad y las lluvias favorecen el moho en empaques de lavadoras y la condensación en aires acondicionados.")}</p>", alt=True))
        out.append(sec("Cuándo conviene dejar de probar y llamar al técnico", _lista([
            "El equipo huele a quemado, hace chispas o saltó el breaker.",
            "Hay agua cerca de la parte eléctrica o debajo del equipo y no encuentras el origen.",
            "Muestra un código de error que sigue apareciendo después de apagar y encender.",
            "El problema vuelve a las pocas horas o días de «resolverse».",
        ])))
        faqs = [
            (f"¿Cada cuánto conviene revisar mis equipos {N}?", "Depende del equipo y del uso. Una limpieza de filtros, empaques y desagües según el manual y revisar si hay ruidos o fugas nuevas es un buen hábito."),
            ("¿Estas guías reemplazan el manual del fabricante?", "No. Son consejos prácticos generales; las instrucciones y advertencias del manual de tu modelo tienen prioridad."),
        ]

    elif slug == "quienes-somos":
        bl = ""
        for e in _eqs(d):
            if tech.get(e): bl += f"<h3>{cap(eqn(e))} {N}</h3><p>{esc(_oraciones(tech[e], 2))}</p>"
        if bl: out.append(sec(f"Qué equipos {N} reparamos y cómo los revisamos", bl, lead=f"Cada marca tiene sus particularidades. Esto es lo que tenemos en cuenta en {junta(eqn(e) for e in d['equipos'])} {N}."))
        out.append(sec("Cómo trabajamos", _lista([
            "<b>Diagnóstico primero:</b> revisamos el equipo y te explicamos la causa antes de hablar de valores.",
            "<b>Tú decides:</b> no reparamos nada sin tu aprobación del valor.",
            "<b>Explicación clara:</b> te decimos qué pieza falló, por qué y qué opciones hay, incluida la de no reparar si no conviene.",
            "<b>Prueba al final:</b> dejamos el equipo funcionando y lo probamos contigo antes de irnos.",
        ]), alt=True))
        out.append(sec("Dónde trabajamos", f"<p>Atendemos a domicilio en {X['zlista']}.</p>"))
        faqs = [
            (f"¿Son el servicio técnico oficial de {N}?", f"No. Somos un servicio técnico independiente. El nombre {N} se usa solo para indicar qué equipos reparamos."),
            ("¿Cómo puedo contactarlos?", f"Por WhatsApp o llamando al {tel}."),
        ]

    elif slug == "garantia":
        out.append(sec(f"Cómo saber si tu equipo {N} aún tiene garantía de fábrica", _lista([
            "Busca la factura de compra: ahí está la fecha y la tienda.",
            "Revisa el manual o la tarjeta de garantía del equipo: indican el plazo y qué cubre.",
            "Ubica el modelo y el número de serie en la etiqueta del equipo.",
            "Si el equipo es nuevo y la falla es de un componente, empieza por la garantía del fabricante o de la tienda.",
        ]), lead=f"El plazo exacto depende del modelo y de la tienda donde lo compraste."))
        out.append(sec("Qué hacer si la garantía ya venció", f"<p>Si el equipo está fuera de garantía, podemos revisarlo a domicilio, explicarte la causa y darte el valor antes de reparar. Tú decides si apruebas la reparación.</p>", alt=True))
        faqs = [(f"¿Reparar fuera del servicio oficial de {N} afecta la garantía?", "Puede afectarla. Si tu equipo está en garantía, consulta primero las condiciones del fabricante o de la tienda antes de pedir una reparación particular.")]

    elif slug == "cuanto-cuesta-la-reparacion":
        out.append(sec("Qué factores componen el valor de una reparación", _lista([
            "<b>El diagnóstico:</b> identificar la causa real con pruebas.",
            "<b>La pieza que falló:</b> varía mucho según el equipo y el modelo.",
            "<b>La mano de obra:</b> depende de lo complejo que sea llegar a la pieza.",
            "<b>La disponibilidad del repuesto:</b> si hay que pedirlo, cambian el plazo y el valor.",
            "<b>La zona:</b> en las zonas más lejanas puede influir el desplazamiento.",
        ]), lead="Por eso no damos precios sin ver el equipo: el valor real se confirma después del diagnóstico y antes de reparar."))
        out.append(sec("¿Reparar o cambiar el equipo?", f"<p>Conviene comparar el valor de la reparación con el de un equipo nuevo. Suele valer la pena reparar cuando el equipo no es muy antiguo, la falla es puntual y el repuesto está disponible. Si el equipo tiene muchos años o ya tuvo varias fallas, cambiarlo puede ser más sensato. En la visita te damos la información para decidir.</p>", alt=True))
        faqs = [("¿Me cobran si decido no reparar?", f"Eso depende de las condiciones de la visita. Consúltalas por WhatsApp o al {tel} antes de agendar.")]

    elif slug == "reparacion-a-domicilio":
        out.append(sec("Qué esperar durante la visita", _lista([
            "El técnico revisa el equipo y hace las pruebas necesarias para confirmar la causa.",
            "Te explica qué encontró y te da el valor de la reparación antes de empezar.",
            "Si apruebas, repara y prueba el equipo contigo.",
            "Si hace falta llevarlo a taller, se coordina el retiro con cuidado.",
        ], "ol")))
        out.append(sec("Cómo prepararte para la visita", _lista(SEGURIDAD_SI[2:]), alt=True))
        faqs = [("¿Cuánto dura la visita?", "Depende del equipo y de la falla. El diagnóstico suele ser lo primero y, según la causa, el técnico te indica el tiempo de la reparación.")]

    elif slug == "centro-de-servicio-cerca-de-mi":
        out.append(sec("Servicio a domicilio o llevar el equipo al centro", f"<p>No necesitas cargar el equipo: vamos a tu casa en {ciu} y su área metropolitana, hacemos el diagnóstico y, si la reparación requiere taller, coordinamos el retiro con cuidado. Para neveras, lavadoras y secadoras grandes, ahorrarte el traslado es una ventaja importante.</p>"))
        faqs = [(f"¿Hay un local para llevar equipos {N}?", f"Atendemos a domicilio. Si necesitas coordinar algo distinto, escríbenos o llama al {tel}.")]

    elif slug.startswith("guia-"):
        filtro = None
        if "aire" in slug: filtro = ("aires",)
        elif "inverter" in slug: filtro = ("neveras", "aires", "lavadoras", "secadoras")
        es = _eqs(d, filtro)
        out.append(sec(f"Lo esencial sobre equipos {N}", _lista([esc(x) for x in d.get("mantenimiento", [])[:4]]) if d.get("mantenimiento") else "", lead="Hábitos que sí marcan la diferencia."))
        sig = ""
        for e in es:
            fs = (fallas.get(e) or [])[:2]
            if fs: sig += f"<h3>{cap(eqn(e))} {N}</h3>" + _lista([f"<b>{esc(s)}</b>. Causa probable: {esc(_min(c))}" for s, c, _r in fs])
        if sig: out.append(sec(f"Señales de que ya necesitas un técnico {N}", sig, alt=True))
        et = "".join(f"<li><b>{cap(eqn(e))}:</b> {esc(eti[e])}</li>" for e in es if eti.get(e))
        if et: out.append(sec("Antes de llamar: dónde encontrar el modelo", f"<ul>{et}</ul>"))
        faqs = [("¿Puedo seguir usando el equipo mientras espero al técnico?", "Si no hay olor a quemado, chispas, saltos del breaker ni agua cerca de las conexiones, puedes usarlo con cuidado. Si hay alguna de esas señales, desconéctalo."),
                (f"¿Qué datos necesita el técnico para atender mi equipo {N}?", "La marca, el modelo (etiqueta), el código o mensaje que muestra y desde cuándo ocurre la falla.")]

    if faqs: out.append(sec("Preguntas frecuentes", faq_html(faqs), alt=len(out) % 2 == 1))
    return "".join(out), faqs
