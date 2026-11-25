# -*- coding: utf-8 -*-
"""Subpáginas por términos de búsqueda para cada marca (Santiago de Chile):
  A) reparación de cada equipo de la marca en las comunas principales (equipo x comuna)
  B) intenciones de búsqueda propias: autorizado o independiente, técnico urgente, mantenimiento, garantía vencida.
Todo el texto se arma con los datos reales de cada marca; no se inventan precios, plazos, horarios ni garantías."""
import re

_CODIGO_RX = {"neveras": r"nevera|refrigerad", "lavadoras": r"^lavadora", "secadoras": r"secad", "aires": r"aire", "lavavajillas": r"lavavaj", "cocinas": r"cocina|horno|estufa", "centro-lavado": r"centro|torre|washtower"}


def build_busquedas(g, m):
    M, EQ, CFG, ZONAS, ZD, ZX, CLIMA = g["M"], g["EQ"], g["CFG"], g["ZONAS"], g["ZD"], g["ZX"], g["CLIMA"]
    pagina, sec, faq_html, faq_ld, cap, esc, pathb, base, junta = g["pagina"], g["sec"], g["faq_html"], g["faq_ld"], g["cap"], g["esc"], g["pathb"], g["base"], g["junta"]
    elegir, bajar, oracion, nom, EXT, wa, DOM = g["elegir"], g["bajar"], g["oracion"], g["nom"], g["EXT"], g["wa"], g["DOM"]
    d = M[m]; N = nom(m); ciu = CFG["ciudad"]; tel = CFG["tel"]
    E = [e for e in d["equipos"] if not e.startswith("tv-")]
    bi = g["BRANDS_ORDER"].index(m)
    crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    lista = lambda xs, tag="ul": f"<{tag}>" + "".join(f"<li>{x}</li>" for x in xs) + f"</{tag}>"
    minus = lambda t: (t or "").strip()[:1].lower() + (t or "").strip()[1:] if len((t or "").strip()) > 1 and (t or "").strip()[1].islower() else (t or "").strip()
    def codigos_de(e):
        rx = re.compile(_CODIGO_RX.get(e, "$^"), re.I)
        for k, v in (d.get("codigos") or {}).items():
            if rx.search(k): return v
        return []
    # ------------------------------------------------------------------ A) equipo x comuna
    comunas = [z for z in CFG.get("comunas_eq", CFG.get("zonas_destacadas", [])) if z in ZONAS]
    for ei, e in enumerate(E):
        sing, pl = EQ[e][1], EQ[e][2]
        art = g["ART_EQ"].get(e, "un"); del_ = "del" if art == "un" else "de la"   # género del equipo (una lavadora, un refrigerador)
        fl = d["fallas"].get(e) or []
        if not fl: continue
        for zi, z in enumerate(comunas):
            zn, barrios, rasgo = ZONAS[z]; viv, acc, sect = ZX[z]
            k = bi + ei * 2 + zi
            sel = [fl[(k + i) % len(fl)] for i in range(min(4, len(fl)))]
            det = lista([f"<b>{esc(f[0].rstrip('.'))}.</b> Causa probable: {esc(minus(f[1]))} En la visita: {esc(minus(f[2]))}" for f in sel])
            var = (bi + zi + ei) % 3
            if var == 0: intro = f"En {zn} atendemos {pl} {N} a domicilio. Predominan {viv}; al coordinar la visita contamos con {acc}. Entre los sectores que visitamos están {sect}."
            elif var == 1: intro = f"¿Tu {sing} {N} falla en {zn}? El técnico llega a tu casa ({sect}). La zona se caracteriza por {viv}, así que coordinamos la franja pensando en {acc}."
            else: intro = f"Reparación de {pl} {N} en {zn}: {rasgo} Visitamos {sect}, teniendo en cuenta {acc}."
            cod = codigos_de(e)
            bloques = sec(f"Reparación de {pl} {N} en {zn}", f"<p>{esc(intro)}</p><p>{esc(CLIMA[z].capitalize())} influyen en cómo envejecen los equipos de esta comuna.</p>")
            bloques += sec(f"Fallas de {pl} {N} que más vemos", det, alt=True)
            bloques += sec(f"Cómo funciona {art} {sing} {N}", f"<p>{esc(oracion(d['tech'][e], zi + ei))}</p>")
            if cod: bloques += sec(f"Códigos de error de {pl} {N}", g["tabla"](["Código", "Qué suele indicar"], [(f"<b>{esc(c)}</b>", esc(t)) for c, t in cod[:5]]), alt=True)
            et = d.get("etiqueta", {}).get(e)
            bloques += sec(f"Antes de la visita en {zn}", lista([f"Ten a mano el modelo {del_} {sing} {N}: {esc(minus(et))}" if et else f"Ten a mano el modelo de tu {sing} {N}.", "Anota el código o mensaje que muestra y desde cuándo ocurre la falla.", "Despeja el espacio alrededor del equipo y avisa en conserjería o portería si hay control de acceso."]))
            sd = CFG.get("sector_de", {}); sv = [zz for zz in CFG.get("sectores", {}).get(sd.get(z), ("", "", []))[2] if zz in comunas and zz != z]
            otras = [zz for zz in comunas if zz != z and zz not in sv]
            r = sv[:4] + [otras[(zi * 3 + i) % len(otras)] for i in range(6 - len(sv[:4]))]
            pills = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[e][0] + "-" + zz)}">{esc(cap(pl))} {N} en {esc(ZONAS[zz][0])}</a>' for zz in dict.fromkeys(r))
            oe = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[x][0] + "-" + z)}">{esc(cap(EQ[x][2]))} {N} en {esc(zn)}</a>' for x in E if x != e)
            enlaces = f'<p><a href="{pathb(m, "servicio-tecnico-" + z)}">Servicio técnico {N} en {esc(zn)}</a> · <a href="{pathb(m, "reparacion-" + EQ[e][0])}">Reparación de {pl} {N}</a> · <a href="{pathb(m, "cobertura")}">Todas las comunas</a></p>'
            bloques += sec(f"Reparación de {pl} {N} en otras comunas", f"<p>{pills}</p>" + (f"<h3>Otros equipos {N} en {esc(zn)}</h3><p>{oe}</p>" if oe else "") + enlaces, alt=True)
            faq = [(f"¿Reparan {pl} {N} a domicilio en {zn}?", f"Sí. Atendemos sectores como {sect}. Escríbenos con el modelo y lo que hace el equipo y coordinamos día y franja."),
                   (f"¿Qué fallas son frecuentes en {art} {sing} {N}?", f"Entre las que más vemos: {'; '.join(esc(minus(f[0].rstrip('.'))) for f in sel[:3])}."),
                   (f"¿Cuánto cuesta reparar {art} {sing} {N} en {zn}?", "El valor depende de la falla y de la pieza. Se confirma después del diagnóstico y solo se repara si tú lo apruebas.")]
            bloques += sec(f"Preguntas frecuentes: {pl} {N} en {zn}", faq_html(faq))
            title = next((t_ for t_ in (f"Reparación de {pl} {N} en {zn}", f"Reparar {pl} {N} en {zn}", f"{cap(pl)} {N} en {zn}") if len(t_) <= 62), f"{cap(pl)} {N} en {zn}"[:62])
            pagina(pathb(m, f"reparacion-{EQ[e][0]}-{z}"), title, f"Reparación de {pl} {N} a domicilio en {zn}, {ciu}: fallas frecuentes, códigos de error, sectores que visitamos y cómo coordinar la visita.",
                   f"Reparación de {pl} {N} en {zn}", bloques, m, g["_hz"]((elegir(m, m + e + z, 1, e) or [None])[0], zn),
                   crumbs0 + [("Cobertura", pathb(m, "cobertura")), (f"Reparación de {pl} en {zn}", pathb(m, f"reparacion-{EQ[e][0]}-{z}"))],
                   [{"@type": "Service", "name": f"Reparación de {pl} {N} en {zn}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": zn}, "brand": {"@type": "Brand", "name": N}}, faq_ld(faq)],
                   bd=f"{N} · {zn}", prio="0.6", lead=f"{cap(pl)} {N} en {zn}: fallas frecuentes y visita a domicilio.")

    # ------------------------------------------------------------------ B) intenciones de búsqueda
    nombre_ext, url_ext = EXT.get(m, (None, None))
    ext = f'<ul><li><a href="{url_ext}" target="_blank" rel="noopener">{nombre_ext}</a> <small>(abre en otra pestaña; sitio del fabricante, no es nuestro)</small></li></ul>' if nombre_ext else ""
    # B1 autorizado o independiente
    faq1 = [(f"¿Son el servicio técnico autorizado de {N}?", f"No. Somos un servicio técnico independiente: no pertenecemos a {N} ni estamos designados por la marca. Reparamos equipos {N} de forma particular."),
            ("¿Qué hago si mi equipo está en garantía de fábrica?", "Contacta primero a la marca o a la tienda donde lo compraste: ellos indican dónde se atiende la garantía. Si tienes dudas sobre si una reparación particular puede afectarla, consúltalo antes."),
            ("¿Cuándo conviene un servicio independiente?", "Cuando el equipo ya no tiene garantía de fábrica, cuando quieres una visita a domicilio coordinada por tu comuna y franja, o cuando buscas una segunda opinión sobre la falla.")]
    cuerpo = (sec(f"Servicio técnico autorizado o independiente para tu {N}", f"<p>Cuando falla un equipo {N} en {ciu}, aparecen dos opciones. Un <b>servicio técnico autorizado</b> es el que la marca (o su representante en Chile) designa para atender garantías. Un <b>servicio técnico independiente</b>, como el nuestro, no pertenece a la marca ni está designado por ella: repara equipos {N} de forma particular.</p><p>Ninguna opción es mejor en todos los casos. Lo que importa es la situación de tu equipo.</p>")
              + sec("Cuál elegir según tu caso", g["tabla"](["Tu situación", "Qué conviene"], [
                  ("Equipo nuevo con garantía de fábrica vigente", "Empieza por la marca o la tienda: la garantía suele depender de que la atienda quien ellos designen."),
                  ("Garantía vencida", f"Un servicio independiente puede revisar el equipo a domicilio, explicarte la causa y darte el valor antes de reparar."),
                  ("Quieres una segunda opinión", "Un diagnóstico independiente te ayuda a comparar antes de decidir si reparar o cambiar."),
                  ("No recuerdas si hay garantía", "Busca la factura y la tarjeta de garantía: ahí están la fecha de compra y las condiciones.")]), alt=True)
              + sec("Cómo saber si tu equipo aún tiene garantía", lista(["Busca la factura o boleta de compra: indica la fecha y la tienda.", "Revisa la tarjeta de garantía o el manual: señalan el plazo y qué cubre.", "Ubica el modelo y la serie en la etiqueta del equipo.", f"{esc(d['garantia'])}", "En Chile, la Ley N° 19.496 sobre protección de los derechos de los consumidores contempla una garantía legal para productos nuevos; consulta en el SERNAC los plazos y condiciones vigentes."]))
              + sec("Qué preguntar antes de contratar a cualquier técnico", lista(["¿Hace un diagnóstico antes de dar un valor?", "¿Entrega el valor de la pieza y de la mano de obra por escrito?", "¿Te explica la causa en palabras simples?", "¿Qué pasa si decides no reparar?"]), alt=True)
              + (sec(f"Dónde consultar a la marca {N}", ext) if ext else "")
              + sec("Preguntas frecuentes", faq_html(faq1), alt=True))
    pagina(pathb(m, "servicio-tecnico-autorizado-o-independiente"), f"Servicio técnico autorizado o independiente: {N}", f"Diferencias entre un servicio técnico autorizado y uno independiente para equipos {N} en {ciu}: garantía, cuándo conviene cada uno y qué preguntar.",
           f"Servicio técnico autorizado o independiente para tu {N}", cuerpo, m, (elegir(m, m + "aut", 1) or [None])[0], crumbs0 + [("Autorizado o independiente", pathb(m, "servicio-tecnico-autorizado-o-independiente"))], [faq_ld(faq1)],
           bd=f"{N} · Guía", prio="0.7", lead=f"Qué cambia entre un servicio autorizado y uno independiente, y cuál conviene para tu equipo {N}.")
    # B2 técnico urgente
    urg = {"neveras": "Dejó de enfriar y tienes alimentos: no abras la puerta, y si pasan horas, pasa lo más delicado a una hielera.", "lavadoras": "Hay una fuga de agua: cierra la llave de paso, desconecta el equipo y seca el piso.",
           "secadoras": "Huele a quemado o se calienta de más: desconéctala y no la uses hasta la revisión.", "aires": "Gotea agua dentro de la casa o la unidad exterior hace ruidos fuertes: apágalo y desconéctalo.",
           "lavavajillas": "Gotea por la puerta o por abajo: cierra la llave de paso y desconéctalo.", "centro-lavado": "Hay una fuga de agua o huele a quemado: cierra la llave de paso y desconecta el equipo.",
           "cocinas": "Si hueles a gas: cierra la llave de gas, ventila, no uses interruptores ni llamas y llama a la empresa de gas o a Bomberos (132). Eso no espera a un técnico.", "microondas": "Hace chispas o huele a quemado: desconéctalo de inmediato.", "batidoras": "Huele a quemado o suelta grasa por la cabeza: desconéctala y no la uses."}
    uc = "".join(f"<li><b>{esc(cap(EQ[e][2]))} {N}:</b> {esc(urg[e])}</li>" for e in E if e in urg)
    faq2 = [(f"¿Pueden atender hoy mi equipo {N}?", f"Depende de la agenda del día y de tu comuna. Escríbenos por WhatsApp o llama al {tel} con el modelo y la falla, y te indicamos la disponibilidad más cercana."),
            ("¿Qué datos necesito dar?", "Marca, modelo (etiqueta), lo que hace el equipo, el código si lo muestra, tu comuna y tu dirección o sector."),
            ("¿Qué hago mientras llega el técnico?", "Si hay riesgo (olor a quemado, chispas, fuga de agua, olor a gas), desconecta y cierra las llaves. Si no, no insistas en encender y apagar el equipo.")]
    cuerpo = (sec(f"Técnico {N} a domicilio urgente en {ciu}", f"<p>Cuando un equipo {N} falla de golpe, lo primero es la seguridad y lo segundo es no empeorar el daño. Aquí te decimos qué hacer mientras coordinamos la visita en tu comuna.</p>")
              + sec("Cuándo es urgente y qué hacer primero", f"<ul>{uc}</ul>", alt=True)
              + sec("Cómo coordinamos una visita urgente", lista(["Escríbenos por WhatsApp con marca, modelo y lo que hace el equipo.", "Indícanos tu comuna y si hay control de acceso o conserjería.", "Te confirmamos la disponibilidad más cercana según la agenda del día.", "En la visita se hace el diagnóstico y recién entonces se da el valor."], "ol"))
              + sec("Preguntas frecuentes", faq_html(faq2), alt=True))
    pagina(pathb(m, "tecnico-a-domicilio-urgente"), f"Técnico {N} a domicilio urgente en {ciu}", f"Técnico {N} a domicilio con visita urgente en {ciu}: qué hacer primero según el equipo, qué datos dar y cómo coordinar la visita.",
           f"Técnico {N} a domicilio urgente en {ciu}", cuerpo, m, (elegir(m, m + "urg", 1) or [None])[0], crumbs0 + [("Técnico urgente", pathb(m, "tecnico-a-domicilio-urgente"))], [faq_ld(faq2)],
           bd=f"{N} · Urgente", prio="0.7", lead=f"Qué hacer cuando tu equipo {N} falla de golpe y cómo pedir la visita.")
    # B3 mantenimiento preventivo
    mant = d.get("mantenimiento", [])
    por_eq = ""
    for e in E:
        raiz = EQ[e][1].split()[0][:5].lower()
        propios = [x for x in mant if raiz in x.lower()][:2]
        et = d.get("etiqueta", {}).get(e)
        por_eq += f"<h3>{esc(cap(EQ[e][2]))} {N}</h3><p>{esc(oracion(d['tech'][e], bi + 1))}</p>" + (lista([esc(x) for x in propios]) if propios else "") + (f"<p><b>Modelo:</b> {esc(minus(et))}</p>" if et else "")
    faq3 = [(f"¿Cada cuánto conviene hacer mantenimiento a un equipo {N}?", "Depende del equipo y del uso; sigue las indicaciones del manual de tu modelo. Como regla práctica, limpia filtros y desagües con regularidad y revisa el equipo antes del verano y antes del invierno."),
            ("¿Qué incluye una revisión preventiva?", "Limpieza de filtros y desagües, revisión de ruidos, fugas y conexiones, y comprobación del funcionamiento general. En la visita se detalla qué se revisó."),
            ("¿El mantenimiento evita todas las fallas?", "No. Reduce las fallas por polvo, suciedad y desgaste, pero no evita las de componentes electrónicos o eléctricos.")]
    cuerpo = (sec(f"Mantenimiento preventivo de equipos {N} en {ciu}", f"<p>{esc(CFG['intro_clima'])} Por eso conviene revisar los equipos {N} dos veces al año: antes de que llegue el calor y antes del invierno.</p>")
              + sec("Por equipo", por_eq, alt=True)
              + sec("Calendario sugerido para Santiago", lista(["<b>Antes del verano:</b> limpia filtros y condensadores y revisa los aires acondicionados y refrigeradores.", "<b>Antes del invierno:</b> revisa la protección de voltaje y las conexiones, y confirma que los desagües estén despejados.", "<b>Cada mes:</b> limpia filtros de secadora y de lavadora si la ropa suelta mucha pelusa."]))
              + sec("Preguntas frecuentes", faq_html(faq3), alt=True))
    pagina(pathb(m, "mantenimiento-preventivo"), f"Mantenimiento preventivo de equipos {N} en {ciu}", f"Mantenimiento preventivo de equipos {N} en {ciu}: qué revisar en cada equipo, calendario sugerido para el verano y el invierno y preguntas frecuentes.",
           f"Mantenimiento preventivo de equipos {N}", cuerpo, m, (elegir(m, m + "mant", 1) or [None])[0], crumbs0 + [("Mantenimiento", pathb(m, "mantenimiento-preventivo"))], [faq_ld(faq3)],
           bd=f"{N} · Mantenimiento", prio="0.6", lead=f"Qué revisar en tus equipos {N} y cuándo.")
    # B4 reparación fuera de garantía
    faq4 = [(f"¿Reparan equipos {N} con la garantía vencida?", f"Sí. Revisamos el equipo a domicilio, te explicamos la causa y te damos el valor antes de reparar. Escríbenos o llama al {tel}."),
            ("¿Cómo decido entre reparar o cambiar?", "Compara el valor de la reparación con el de un equipo nuevo parecido. Suele valer la pena reparar cuando la falla es puntual, el equipo no es muy antiguo y el repuesto está disponible."),
            ("¿Y si el repuesto demora?", "Si hay que pedir la pieza, cambian el plazo y el valor. Te lo informamos antes de que apruebes la reparación.")]
    cuerpo = (sec(f"Reparación de equipos {N} con garantía vencida en {ciu}", f"<p>Cuando termina la garantía de fábrica, reparar suele ser una alternativa razonable. {esc(d['garantia'])}</p>")
              + sec("Cómo lo hacemos", lista(["Escríbenos con marca, modelo y qué hace el equipo.", "Coordinamos la visita en tu comuna.", "Diagnóstico en casa y explicación de la causa.", "Valor de la pieza y de la mano de obra antes de reparar.", "Reparación y prueba solo si tú aprobas el valor."], "ol"), alt=True)
              + sec("Fallas que suelen convenir reparar", lista([esc(f"{cap(EQ[e][1])}: {minus(x[0]).rstrip('.')}") for e in E for x in d["fallas"][e][:1]][:6]))
              + sec("Preguntas frecuentes", faq_html(faq4), alt=True))
    cuerpo = cuerpo.replace("si tú aprobas", "si tú apruebas")
    pagina(pathb(m, "reparacion-fuera-de-garantia"), f"Reparación de equipos {N} con garantía vencida", f"Reparación de equipos {N} con la garantía vencida en {ciu}: cómo lo hacemos, cuándo conviene reparar o cambiar y preguntas frecuentes.",
           f"Reparación de equipos {N} fuera de garantía", cuerpo, m, (elegir(m, m + "fg", 1) or [None])[0], crumbs0 + [("Fuera de garantía", pathb(m, "reparacion-fuera-de-garantia"))], [faq_ld(faq4)],
           bd=f"{N} · Garantía vencida", prio="0.6", lead=f"Qué hacer cuando la garantía de tu equipo {N} ya terminó.")


def build_extra(g, m):
    """Páginas de sector (resumen por zona de Santiago) y más intenciones de búsqueda por marca."""
    M, EQ, CFG, ZONAS, ZX, CLIMA = g["M"], g["EQ"], g["CFG"], g["ZONAS"], g["ZX"], g["CLIMA"]
    pagina, sec, faq_html, faq_ld, cap, esc, pathb, base, junta = g["pagina"], g["sec"], g["faq_html"], g["faq_ld"], g["cap"], g["esc"], g["pathb"], g["base"], g["junta"]
    elegir, oracion, nom, DOM, tabla = g["elegir"], g["oracion"], g["nom"], g["DOM"], g["tabla"]
    d = M[m]; N = nom(m); ciu = CFG["ciudad"]; tel = CFG["tel"]
    E = [e for e in d["equipos"] if not e.startswith("tv-")]
    bi = g["BRANDS_ORDER"].index(m)
    crumbs0 = [(f"Centro de Servicio Técnico {N} Panamá", base(m))]
    lista = lambda xs, tag="ul": f"<{tag}>" + "".join(f"<li>{x}</li>" for x in xs) + f"</{tag}>"
    minus = lambda t: (t or "").strip()[:1].lower() + (t or "").strip()[1:] if len((t or "").strip()) > 1 and (t or "").strip()[1].islower() else (t or "").strip()
    ceq = set(CFG.get("comunas_eq", []))
    # ------------------------------------------------------------ sectores
    todas = [(e, f) for e in E for f in d["fallas"].get(e, [])]
    for si, (sl, (frase, desc, zs)) in enumerate(CFG["sectores"].items()):
        cards = "".join(f'<a class="card l" href="{pathb(m, "servicio-tecnico-" + z)}"><span class="t">Servicio técnico {N} en {esc(ZONAS[z][0])}</span><br><small>{esc(ZX[z][2])}</small></a>' for z in zs)
        eqp = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[e][0])}">Reparación de {esc(EQ[e][2])} {N}</a>' for e in E)
        loc = [z for z in zs if z in ceq][:3]
        eqc = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[e][0] + "-" + z)}">{esc(cap(EQ[e][2]))} {N} en {esc(ZONAS[z][0])}</a>' for z in loc for e in E[:3])
        fl = [todas[(bi * 5 + si * 7 + i * 11) % len(todas)] for i in range(3)]
        det = lista([f"<b>{esc(cap(EQ[e][1]))} {N}:</b> {esc(f[0].rstrip('.'))}. Causa probable: {esc(minus(f[1]))}" for e, f in fl])
        otros = "".join(f'<a class="pill" href="{pathb(m, "servicio-tecnico-" + o)}">Servicio técnico {N} en {esc(CFG["sectores"][o][0])}</a>' for o in CFG["sectores"] if o != sl)
        climas = sorted({CLIMA[z] for z in zs}, key=len)[0]
        faq = [(f"¿Atienden equipos {N} en {frase}?", f"Sí. Atendemos a domicilio las comunas de {frase}: {junta(ZONAS[z][0] for z in zs[:8])}{' y más' if len(zs) > 8 else ''}. Escríbenos con el modelo, la falla y tu comuna."),
               (f"¿Qué equipos {N} reparan en {frase}?", f"Atendemos {junta(EQ[e][2] for e in E)} de la marca {N}."),
               ("¿Cómo coordino la visita?", f"Por WhatsApp o llamando al {tel}: indícanos la comuna, el equipo y lo que hace. Acordamos día y franja teniendo en cuenta el acceso del edificio o condominio.")]
        cuerpo = (sec(f"Servicio técnico {N} en {frase}", f"<p>Atendemos equipos {N} a domicilio en {esc(frase)}. {esc(desc)}</p><p>{esc(climas.capitalize())} influyen en cómo envejecen los equipos de este sector.</p>")
                  + sec(f"Comunas {frase.replace('el ', 'del ', 1)} donde atendemos {N}", f'<div class="g c3">{cards}</div>', alt=True)
                  + sec(f"Equipos {N} que reparamos en {frase}", f"<p>{eqp}</p>" + (f"<h3>Reparación por comuna</h3><p>{eqc}</p>" if eqc else ""))
                  + sec(f"Fallas de {N} que más se reportan en {frase}", det, alt=True)
                  + sec("Otros sectores de Santiago", f"<p>{otros}</p><p><a href=\"{pathb(m, 'cobertura')}\">Ver todas las comunas</a></p>")
                  + sec(f"Preguntas frecuentes: servicio técnico {N} en {frase}", faq_html(faq), alt=True))
        pagina(pathb(m, "servicio-tecnico-" + sl), f"Servicio técnico {N} en {frase}", f"Servicio técnico {N} a domicilio en {frase}: comunas que atendemos, fallas frecuentes de equipos {N} y cómo coordinar la visita.",
               f"Servicio técnico {N} en {frase}", cuerpo, m, g["_hz"]((elegir(m, m + sl, 1) or [None])[0], cap(frase)),
               crumbs0 + [("Cobertura", pathb(m, "cobertura")), (cap(frase), pathb(m, "servicio-tecnico-" + sl))],
               [{"@type": "Service", "name": f"Servicio técnico {N} en {frase}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": [{"@type": "Place", "name": ZONAS[z][0]} for z in zs[:12]], "brand": {"@type": "Brand", "name": N}}, faq_ld(faq)],
               bd=f"{N} · {cap(frase)}", prio="0.8", lead=f"Equipos {N} en {frase}: comunas, fallas frecuentes y visita a domicilio.")
    # ------------------------------------------------------------ más intenciones
    def intent(slug, titulo, desc, h1, lead, cuerpo, faq, bd, clave):
        pagina(pathb(m, slug), titulo, desc, h1, cuerpo + sec("Preguntas frecuentes", faq_html(faq), alt=True), m, (elegir(m, m + clave, 1) or [None])[0],
               crumbs0 + [((titulo if len(titulo) <= 40 else titulo[:40].rsplit(" ", 1)[0]), pathb(m, slug))], [faq_ld(faq)], bd=bd, prio="0.6", lead=lead)
    rev = lista([f"<b>{esc(cap(EQ[e][2]))} {N}:</b> {esc(d['fallas'][e][0][2])}" for e in E if d["fallas"].get(e)])
    intent("que-incluye-la-visita-tecnica", f"Qué incluye la visita técnica de {N}", f"Qué incluye la visita técnica a domicilio para equipos {N} en {ciu}: qué se revisa en cada equipo, qué pasa después y cómo se aprueba el valor.",
           f"Qué incluye la visita técnica de equipos {N}", f"Qué hace el técnico en tu casa cuando va a revisar un equipo {N}.",
           sec(f"La visita técnica de {N}, paso a paso", lista(["Coordinamos día y franja en tu comuna.", "El técnico revisa el equipo y hace las pruebas necesarias.", "Te explica la causa y las opciones.", "Te da el valor de la pieza y de la mano de obra antes de reparar.", "Si apruebas, repara y prueba el equipo contigo."], "ol"))
           + sec("Qué se revisa en cada equipo", rev, alt=True) + sec("Qué conviene tener listo", lista(["El modelo del equipo (foto de la etiqueta).", "El código o mensaje de la pantalla y desde cuándo ocurre.", "El espacio libre alrededor del equipo y el acceso por conserjería o portería."])),
           [("¿Hay que pagar la visita aunque no repare?", f"Consulta las condiciones al coordinar por WhatsApp o al {tel}, antes de agendar."), ("¿Reparan sin aviso?", "No. Primero el diagnóstico y el valor; solo se repara si tú lo apruebas.")], f"{N} · Visita", "vis")
    intent("cuanto-demora-una-reparacion", f"Cuánto demora una reparación de {N}", f"Qué influye en el tiempo de una reparación de equipos {N} en {ciu}: tipo de falla, disponibilidad del repuesto y acceso al equipo.",
           f"Cuánto demora la reparación de un equipo {N}", f"De qué depende el tiempo de reparación de tu equipo {N}.",
           sec("De qué depende el tiempo", lista(["<b>El tipo de falla:</b> limpiezas, filtros o ajustes suelen resolverse en la misma visita si el técnico tiene lo necesario.", "<b>El repuesto:</b> si hay que pedir una pieza, el plazo depende de su disponibilidad.", "<b>El acceso:</b> equipos empotrados o en espacios reducidos requieren más trabajo.", "<b>La confirmación del valor:</b> la reparación empieza cuando tú apruebas."]))
           + sec(f"Fallas de {N} según su complejidad", lista([f"<b>{esc(cap(EQ[e][1]))}:</b> {esc(d['fallas'][e][0][0].rstrip('.'))}" for e in E if d["fallas"].get(e)]), alt=True),
           [("¿Me dan un plazo exacto?", "Sin ver el equipo no podemos prometer un tiempo. Después del diagnóstico te informamos cuánto se estima, según la pieza y su disponibilidad.")], f"{N} · Plazos", "dem")
    piezas = lista([f"<b>{esc(cap(EQ[e][1]))}:</b> {esc(minus(d['fallas'][e][0][1]))}" for e in E if d["fallas"].get(e)])
    intent("repuestos-originales-o-alternativos", f"Repuestos originales o alternativos: {N}", f"Repuestos originales o alternativos para equipos {N} en {ciu}: diferencias, cómo reconocer el número de parte y qué preguntar antes de aprobar una reparación.",
           f"Repuestos originales o alternativos para tu equipo {N}", f"Cómo decidir entre un repuesto original y uno alternativo para tu {N}.",
           sec("Diferencias a tener en cuenta", lista(["<b>Original:</b> lo fabrica o respalda la marca, y suele coincidir con el número de parte del equipo.", "<b>Alternativo o compatible:</b> lo fabrica un tercero para el mismo uso; la calidad varía según el fabricante.", "<b>Reacondicionado:</b> una pieza usada que se reparó; conviene saberlo antes de aprobar."]))
           + sec("Piezas que más se revisan en equipos " + N, piezas, alt=True)
           + sec("Qué preguntar antes de aprobar", lista(["¿La pieza es original, alternativa o reacondicionada?", "¿Cuál es el valor de la pieza y de la mano de obra por separado?", "¿Tiene garantía la reparación y qué cubre?"]))
           + sec(f"Dónde está el número de parte y el modelo", lista([f"<b>{esc(cap(EQ[e][1]))}:</b> {esc(minus(d['etiqueta'][e]))}" for e in E if d.get("etiqueta", {}).get(e)]), alt=True),
           [("¿Siempre usan repuestos originales?", "Depende de la pieza y de su disponibilidad. Antes de que apruebes, te informamos qué pieza se cambia y su valor."), ("¿Afecta la garantía usar un repuesto alternativo?", "Puede afectar la garantía de fábrica. Si tu equipo aún la tiene, consulta primero a la marca o a la tienda.")], f"{N} · Repuestos", "rep")
    inst = []
    for e in E:
        ov = g["CHILE_MI"].get(e, {}).get("inst_gye")
        if ov: inst.append(f"<h3>{esc(cap(EQ[e][2]))} {N}</h3><p>{esc(oracion(d['tech'][e], bi))}</p><p>{esc(ov)}</p>" + (f"<p><b>Modelo:</b> {esc(minus(d['etiqueta'][e]))}</p>" if d.get('etiqueta', {}).get(e) else ""))
    if not inst: inst = [f"<h3>{esc(cap(EQ[e][2]))} {N}</h3><p>{esc(oracion(d['tech'][e], bi))}</p>" for e in E[:3]]
    if inst:
        intent("instalacion-de-equipos", f"Instalación de equipos {N} en {ciu}", f"Qué revisar al instalar un equipo {N} en {ciu}: nivelación, voltaje, desagües, ventilación y seguridad según el equipo.",
               f"Instalación de equipos {N}", f"Qué conviene revisar antes y durante la instalación de tu equipo {N}.",
               sec(f"Instalar equipos {N} en {ciu}", "<p>Una buena instalación evita fallas en el primer año. Confirma el voltaje, nivela el equipo y deja ventilación.</p>" + "".join(inst)),
               [("¿Instalan equipos nuevos?", f"Escríbenos con la marca, el modelo y el lugar de instalación, o llama al {tel}, y te indicamos si podemos hacerlo."), ("¿Qué voltaje se usa en Chile?", "En Chile las viviendas usan 220 V. Confirma en la etiqueta del equipo que su voltaje sea compatible.")], f"{N} · Instalación", "ins")
    def temporada(slug, titulo, h1, desc, rx, intro, clave, consejos, eq_ok):
        eqs = [e for e in E if e in eq_ok and any(re.search(rx, f[0] + " " + f[1], re.I) for f in d["fallas"].get(e, []))]
        bl = ""
        for e in eqs[:5]:
            fs = [f for f in d["fallas"][e] if re.search(rx, f[0] + " " + f[1], re.I)][:2]
            bl += f"<h3>{esc(cap(EQ[e][2]))} {N}</h3>" + lista([f"<b>{esc(f[0].rstrip('.'))}.</b> Causa probable: {esc(minus(f[1]))}" for f in fs])
        if not bl:
            for e in E[:4]:
                fs = d["fallas"].get(e, [])[:2]
                if fs: bl += f"<h3>{esc(cap(EQ[e][2]))} {N}</h3>" + lista([f"<b>{esc(f[0].rstrip('.'))}.</b> Causa probable: {esc(minus(f[1]))}" for f in fs])
        intent(slug, titulo, desc, h1, intro, sec(h1, f"<p>{esc(intro)}</p>") + sec(f"Fallas de {N} más frecuentes en esta época", bl, alt=True) + sec("Qué puedes hacer", lista(consejos)),
               [(f"¿Conviene revisar mis equipos {N} antes de esta época?", "Sí: una revisión preventiva de filtros, desagües y conexiones reduce las fallas por uso intensivo."), ("¿Cuándo llamar al técnico?", "Si hay olor a quemado, chispas, fugas o un código que se repite, desconecta el equipo y pide la visita.")], f"{N} · Temporada", clave)
    temporada("fallas-en-verano", f"Fallas de equipos {N} en verano en {ciu}", f"Fallas de equipos {N} en el verano de Santiago", f"Fallas más comunes de equipos {N} en el verano de {ciu}: aire acondicionado, refrigeradores y otros equipos que trabajan más con el calor.", r"enfr|compresor|condensador|ventilador|filtro|gas|gotea|hielo|congel",
              f"Los veranos de Santiago son secos y calurosos, y los equipos de frío trabajan más. Estas son las fallas de equipos {N} que más se reportan cuando sube la temperatura.", "ver", ["Limpia filtros y condensadores antes de que empiece el calor.", "Deja espacio de ventilación detrás y a los lados del equipo.", "No sobrecargues el refrigerador ni lo pegues a la pared."], ("neveras", "aires"))
    temporada("fallas-en-invierno", f"Fallas de equipos {N} en invierno en {ciu}", f"Fallas de equipos {N} en el invierno de Santiago", f"Fallas más comunes de equipos {N} en el invierno de {ciu}: cortes de luz, variaciones de voltaje y equipos que se usan más, como las secadoras.", r"placa|no enciende|se apaga|pantalla|código|secad|ropa|voltaje|electr",
              f"En invierno hay temporales, cortes de luz y variaciones de voltaje al volver el suministro, y se usa más la secadora. Estas son las fallas de equipos {N} que más se reportan en esa época.", "inv", ["Usa un protector de voltaje en equipos con placa electrónica.", "Espera unos minutos antes de volver a conectar tras un corte de luz.", "Limpia el filtro de la secadora después de cada uso."], ("secadoras", "lavadoras", "centro-lavado", "cocinas", "neveras", "lavavajillas"))
