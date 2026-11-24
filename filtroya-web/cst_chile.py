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
    comunas = [z for z in CFG.get("zonas_destacadas", []) if z in ZONAS]
    for ei, e in enumerate(E):
        sing, pl = EQ[e][1], EQ[e][2]
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
            bloques += sec(f"Cómo funciona un {sing} {N}", f"<p>{esc(oracion(d['tech'][e], zi + ei))}</p>")
            if cod: bloques += sec(f"Códigos de error de {pl} {N}", g["tabla"](["Código", "Qué suele indicar"], [(f"<b>{esc(c)}</b>", esc(t)) for c, t in cod[:5]]), alt=True)
            et = d.get("etiqueta", {}).get(e)
            bloques += sec(f"Antes de la visita en {zn}", lista([f"Ten a mano el modelo del {sing} {N}: {esc(minus(et))}" if et else f"Ten a mano el modelo de tu {sing} {N}.", "Anota el código o mensaje que muestra y desde cuándo ocurre la falla.", "Despeja el espacio alrededor del equipo y avisa en conserjería o portería si hay control de acceso."]))
            otras = [zz for zz in comunas if zz != z]
            r = [otras[(zi * 3 + i) % len(otras)] for i in range(6)]
            pills = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[e][0] + "-" + zz)}">{esc(cap(pl))} {N} en {esc(ZONAS[zz][0])}</a>' for zz in dict.fromkeys(r))
            oe = "".join(f'<a class="pill" href="{pathb(m, "reparacion-" + EQ[x][0] + "-" + z)}">{esc(cap(EQ[x][2]))} {N} en {esc(zn)}</a>' for x in E if x != e)
            enlaces = f'<p><a href="{pathb(m, "servicio-tecnico-" + z)}">Servicio técnico {N} en {esc(zn)}</a> · <a href="{pathb(m, "reparacion-" + EQ[e][0])}">Reparación de {pl} {N}</a> · <a href="{pathb(m, "cobertura")}">Todas las comunas</a></p>'
            bloques += sec(f"Reparación de {pl} {N} en otras comunas", f"<p>{pills}</p>" + (f"<h3>Otros equipos {N} en {esc(zn)}</h3><p>{oe}</p>" if oe else "") + enlaces, alt=True)
            faq = [(f"¿Reparan {pl} {N} a domicilio en {zn}?", f"Sí. Atendemos sectores como {sect}. Escríbenos con el modelo y lo que hace el equipo y coordinamos día y franja."),
                   (f"¿Qué fallas son frecuentes en un {sing} {N}?", f"Entre las que más vemos: {'; '.join(esc(minus(f[0].rstrip('.'))) for f in sel[:3])}."),
                   (f"¿Cuánto cuesta reparar un {sing} {N} en {zn}?", "El valor depende de la falla y de la pieza. Se confirma después del diagnóstico y solo se repara si tú lo apruebas.")]
            bloques += sec(f"Preguntas frecuentes: {pl} {N} en {zn}", faq_html(faq))
            title = next((t_ for t_ in (f"Reparación de {pl} {N} en {zn}", f"Reparar {pl} {N} en {zn}", f"{cap(pl)} {N} en {zn}") if len(t_) <= 62), f"{cap(pl)} {N} en {zn}"[:62])
            pagina(pathb(m, f"reparacion-{EQ[e][0]}-{z}"), title, f"Reparación de {pl} {N} a domicilio en {zn}, {ciu}: fallas frecuentes, códigos de error, sectores que visitamos y cómo coordinar la visita.",
                   f"Reparación de {pl} {N} en {zn}", bloques, m, g["_hz"]((elegir(m, m + e + z, 1, e) or [None])[0], zn),
                   crumbs0 + [("Cobertura", pathb(m, "cobertura")), (f"Reparación de {pl} en {zn}", pathb(m, f"reparacion-{EQ[e][0]}-{z}"))],
                   [{"@type": "Service", "name": f"Reparación de {pl} {N} en {zn}", "provider": {"@id": DOM + "/#negocio"}, "areaServed": {"@type": "Place", "name": zn}, "brand": {"@type": "Brand", "name": N}}, faq_ld(faq)],
                   bd=f"{N} · {zn}", prio="0.6", lead=f"{cap(pl)} {N} en {zn}: fallas frecuentes y visita a domicilio.")

    # ------------------------------------------------------------------ B) intenciones de búsqueda
    nombre_ext, url_ext = EXT[m]
    ext = f'<ul><li><a href="{url_ext}" target="_blank" rel="noopener">{nombre_ext}</a> <small>(abre en otra pestaña; sitio del fabricante, no es nuestro)</small></li></ul>'
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
              + sec(f"Dónde consultar a la marca {N}", ext)
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
