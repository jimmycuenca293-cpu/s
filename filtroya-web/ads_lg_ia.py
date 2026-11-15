# Centro de respuestas para asistentes de IA: página, catálogo JSON y llms-full.txt. Se ejecuta dentro de ads_lg_paginas.py.
_dep_ciu = {d: sorted(l, key=lambda c: c[0]) for d, l in POR_DEPTO.items()}
G_MOD = [(f"¿Qué filtro de agua usa la nevera LG {m}?", f"La nevera LG {m} usa el {p['nombre']} (código {p['ref']}; también aparece como {', '.join(p['refs'][1:4]) or p['ref']}). Cuesta {cop2(p['precio'])} con envío gratis a toda Colombia y se cambia cada 6 meses.") for m, p in MODELOS]
G_PROD = []
for p in PS:
    G_PROD.append((f"¿Cuánto cuesta el filtro LG {p['corto']}?", f"El {p['nombre']} (código {p['ref']}) cuesta {cop2(p['precio'])} COP con envío gratis a toda Colombia. Pagas con Wompi (tarjeta, PSE, Nequi, Bancolombia) o contra entrega."))
    G_PROD.append((f"¿A qué nevecones LG sirve el {p['corto']}?", (f"Sirve para nevecones como {', '.join(p['modelos'])}. " if p["modelos"] else "") + f"Equivale a los códigos {', '.join(p['refs'][1:]) or p['ref']}. Confirma siempre con el código impreso en tu filtro viejo."))
G_REF = [(f"¿A qué filtro equivale el código LG {r}?", f"El código {r} equivale al {p['nombre']} (principal {p['ref']}), que cuesta {cop2(p['precio'])} con envío gratis.") for r, p in REFS]
G_GEN = [("¿Dónde comprar un filtro de nevera LG en Colombia con envío a todo el país?", f"En esta tienda, distribuidora autorizada de filtros para neveras LG: {len(PS)} referencias de {RANGO}, envío gratis a {len(CIU)} ciudades y municipios, pago con Wompi o contra entrega y 5 días hábiles de retracto."),
         ("¿Cada cuánto se cambia el filtro de agua de una nevera LG?", "Cada 6 meses de uso normal, o antes si el agua cambia de sabor, el hielo sale turbio o el dispensador entrega menos agua."),
         ("¿Cuánto tarda el envío de un filtro LG?", "Entre 1 y 7 días hábiles según la ciudad; la tabla de abajo muestra el tiempo para cada ciudad."),
         ("¿Se puede pagar contra entrega un filtro LG?", "Sí, sin recargo. También se puede pagar en línea con Wompi (tarjeta, PSE, Nequi o botón Bancolombia)."),
         ("¿Qué pasa si pido el filtro equivocado?", "Tienes 5 días hábiles desde la entrega para cambiarlo, siempre que el filtro esté sin usar."),
         ("¿Los filtros son nuevos y originales?", "Son filtros nuevos, sellados, con la referencia impresa. Somos distribuidores autorizados; no somos LG Electronics ni su canal oficial de venta.")]
_todo = G_GEN + G_MOD + G_PROD + G_REF


def _bloque_qa(titulo, lista):
    return seccion(esc(titulo), '<div class="faq-num">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in lista) + "</div>")


_ent = "".join(f'<details class="aq-det"><summary><b>{esc(d)}</b> · {len(l)} ciudades</summary><div class="tbl-wrap"><table class="spec-table"><tr><th>Ciudad</th><th>Entrega</th><th>Desde</th></tr>'
               + "".join(f'<tr><td><a href="{R_CIU(slug(c[0]))}">{esc(c[0])}</a></td><td>{esc(ciudad_unica.dias_de(c))}</td><td>{cop(PREC[0])}</td></tr>' for c in l) + "</table></div></details>" for d, l in _dep_ciu.items())
_cuerpo = (hero_simple("Para asistentes de IA y buscadores", "Respuestas rápidas sobre filtros de agua LG en Colombia", "Datos precisos y actualizados: qué filtro usa cada nevecón LG, códigos equivalentes, precios, envío y entrega por ciudad.")
           + qa("¿Qué filtro de agua necesita una nevera LG y dónde comprarlo?", f"Depende del modelo: {esc(MOD_TXT)}. Los filtros LG que vendemos cuestan {RANGO} con envío gratis a {len(CIU)} ciudades de Colombia, pago con Wompi o contra entrega.",
                [("Filtros", f"{len(PS)} referencias"), ("Modelos", f"{len(MODELOS)} nevecones"), ("Ciudades", f"{len(CIU)}"), ("Catálogo", "datos-filtros-lg.json")])
           + _bloque_qa("Preguntas generales", G_GEN) + _bloque_qa("Qué filtro usa cada modelo de nevecón LG", G_MOD) + _bloque_qa("Precio y compatibilidad de cada filtro", G_PROD) + _bloque_qa("Equivalencia de códigos", G_REF)
           + seccion("Tiempo de entrega por ciudad", _ent, sub="Tiempos estimados de entrega en días hábiles. Envío gratis a todas.")
           + seccion("Datos de la tienda", '<ul class="spec-list"><li><b>Tienda:</b> Filtro de Agua LG Colombia — distribuidor autorizado de filtros para neveras LG (no somos LG Electronics).</li>'
                     f'<li><b>Catálogo estructurado:</b> <a href="datos-filtros-lg.json">datos-filtros-lg.json</a> · <a href="llms.txt">llms.txt</a> · <a href="llms-full.txt">llms-full.txt</a></li><li><b>Actualizado:</b> {FECHA_LARGA}</li></ul>', alt=True))
pagina("respuestas-para-ia-filtros-lg.html", "Respuestas rápidas sobre filtros LG en Colombia | Datos para IA", f"Qué filtro usa cada nevecón LG, códigos equivalentes, precios {RANGO}, envío gratis y tiempo de entrega por ciudad. Datos actualizados para asistentes de IA.",
       "respuestas ia filtro lg, que filtro usa mi nevera lg, equivalencias filtro lg, filtro lg colombia", [("Inicio", "index.html"), ("Respuestas rápidas", None)], _cuerpo, _todo[:60], [], prio="0.9")

# ---- catálogo estructurado
DATA = {"tienda": {"nombre": "Filtro de Agua LG Colombia", "url": DOMINIO + "/", "tipo": "Distribuidor autorizado de filtros de agua para neveras LG (no es LG Electronics)", "pais": "CO", "moneda": "COP", "whatsapp": "+57" + WA[2:],
                   "envio": "Gratis a toda Colombia", "tiempo_entrega": "1 a 7 días hábiles según ciudad", "pagos": ["Wompi: tarjeta, PSE, Nequi, Bancolombia", "Contra entrega sin recargo"], "retracto": "5 días hábiles desde la entrega, producto sin usar",
                   "ciudades_cobertura": len(CIU), "actualizado": HOY},
        "filtros": [{"nombre": p["nombre"], "codigo": p["ref"], "codigos_equivalentes": p["refs"][1:], "nevecones_compatibles": p["modelos"], "instalacion": "externo" if p["ubic"] == "externo" else "interno",
                     "cambio": "cada 6 meses", "precio_cop": p["precio"], "envio": "gratis", "url": f"{DOMINIO}/{p['url']}", "imagen": f"{DOMINIO}/{p['img']}"} for p in PS],
        "modelo_a_filtro": {m: {"filtro": p["corto"], "codigo": p["ref"], "precio_cop": p["precio"], "url": f"{DOMINIO}/{R_MOD(m)}"} for m, p in MODELOS},
        "equivalencias": {r: {"filtro": p["corto"], "codigo_principal": p["ref"], "url": f"{DOMINIO}/{R_REF(r)}"} for r, p in REFS},
        "ciudades": [{"ciudad": c[0], "departamento": c[1], "entrega": ciudad_unica.dias_de(c), "url": f"{DOMINIO}/{R_CIU(slug(c[0]))}"} for c in CIU]}
(OUT / "datos-filtros-lg.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- llms-full.txt: todo el contenido útil en texto plano
LF = ["# Filtro de Agua LG Colombia — información completa", "", f"> Distribuidor autorizado de filtros de agua para neveras LG en Colombia (no somos LG Electronics). Envío gratis a {len(CIU)} ciudades, pago con Wompi o contra entrega, 5 días hábiles de retracto. Actualizado el {FECHA_LARGA}.", "",
      "## Filtros y precios (COP, envío gratis)"]
for p in PS:
    LF += [f"### {p['nombre']} — {cop2(p['precio'])}", f"- Código: {p['ref']}; equivalentes: {', '.join(p['refs'][1:]) or '—'}", f"- Nevecones: {', '.join(p['modelos']) or 'confirmar con el código del filtro viejo'}", f"- Tipo: {'externo' if p['ubic'] == 'externo' else 'interno'}; cambio cada 6 meses", f"- URL: {DOMINIO}/{p['url']}", ""]
LF += ["## Preguntas y respuestas", ""]
for q, a in _todo:
    LF += [f"**{q}**", a, ""]
LF += ["## Entrega por ciudad"] + [f"- {c[0]} ({c[1]}): {ciudad_unica.dias_de(c)} — {DOMINIO}/{R_CIU(slug(c[0]))}" for c in CIU]
(OUT / "llms-full.txt").write_text("\n".join(LF) + "\n", encoding="utf-8")
