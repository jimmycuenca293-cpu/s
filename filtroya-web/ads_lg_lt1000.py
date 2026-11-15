# Clúster del filtro más vendido: LT1000P (guía completa + páginas por ciudad). Se ejecuta después del enlazado interno.
L = PS[0]
LREFS = ", ".join(L["refs"][1:])
LMOD = ", ".join(L["modelos"])
ALIAS = "LT 1000P, LT1000, LTP1000, LTP 1000 o LT-1000P"
_orden = [s for s in TOP if s in CIUDAD] + sorted(s for s in GRANDES_S if s in CIUDAD and s not in TOP)
CIU_LT = _orden[:40]
R_LT = lambda s: f"filtro-lt1000p-{s}.html"

# ---- guía completa
preg_l = [(f"¿Qué es el filtro LG LT1000P?", f"Es el {L['nombre']}, un filtro de agua interno de reemplazo para nevecones LG. Equivale a {LREFS}."), (f"¿LTP1000, LT 1000P y LT1000 son el mismo filtro?", f"Es la misma referencia escrita de distintas formas: {ALIAS} se refieren al LT1000P. Confirma con el código impreso en tu filtro."),
          ("¿Qué nevecones usan el LT1000P?", f"Entre otros, {LMOD}. Si tu modelo no está en la lista, confirma con el código del filtro viejo."), ("¿Cuánto cuesta el LT1000P?", f"{cop2(L['precio'])} COP con envío gratis a toda Colombia."),
          ("¿Cada cuánto se cambia el LT1000P?", "Cada 6 meses de uso normal."), ("¿El LT1000PC y el LT1000PCS son iguales?", "Son códigos equivalentes del mismo filtro."), ("¿Se puede pagar contra entrega?", FPAGO),
          ("¿Cómo instalo el LT1000P?", "Retira el filtro viejo con un giro suave, instala el nuevo hasta que quede firme, saca unos 6 litros de agua y reinicia el aviso del panel."), ("¿El filtro viene sellado?", "Sí, nuevo y sellado; tienes 5 días hábiles de retracto con el filtro sin usar."),
          ("¿Enviarán a mi ciudad?", f"Sí, a {len(CIU)} ciudades y municipios de Colombia con envío gratis.")]
cuerpo = (hero_simple("Guía completa · el más vendido", "Filtro LG LT1000P: guía completa, equivalencias y precio", f"Todo sobre el LT1000P: códigos equivalentes, nevecones compatibles, cómo cambiarlo y dónde comprarlo con envío gratis.")
          + qa("¿Qué es el filtro LG LT1000P y dónde comprarlo?", f"El <b>LT1000P</b> es el filtro de agua de reemplazo para nevecones LG como {esc(LMOD)}. También se busca como {esc(ALIAS)}. Cuesta <b>{cop2(L['precio'])}</b> con envío gratis a toda Colombia, pago con Wompi o contra entrega.",
                [("Código", "LT1000P"), ("Equivale a", ", ".join(L["refs"][1:4])), ("Precio", cop2(L["precio"])), ("Cambio", "Cada 6 meses")])
          + seccion("Compra el LT1000P", '<div class="tf-grid">' + tarjeta(L, 0) + "</div>")
          + seccion("Qué es el LT1000P", f"<p>El {esc(L['nombre'])} es un filtro de agua interno que se instala dentro del refrigerador de nevecones LG compatibles. Retiene sedimentos y mejora el sabor y el olor del agua y del hielo del dispensador. Se reemplaza cada 6 meses de uso normal.</p>"
                    f"<p>Mucha gente lo busca con nombres distintos: <b>{esc(ALIAS)}</b>. Todos se refieren a la misma referencia; lo importante es que el código impreso en tu filtro viejo coincida.</p>")
          + seccion("Códigos equivalentes", '<p>Estos códigos corresponden al mismo filtro:</p><div class="city-tags">' + "".join(f'<a href="{R_REF(r)}">{esc(r)}</a>' for r in L["refs"][1:]) + "</div>", alt=True)
          + seccion("Nevecones que lo usan", '<div class="city-tags">' + "".join(f'<a href="{R_MOD(m)}">{esc(m)}</a>' for m in L["modelos"]) + '</div><p class="note" style="margin-top:12px">¿Tu modelo no aparece? Mira <a href="cual-es-mi-filtro.html">cómo identificar tu filtro</a>.</p>')
          + seccion("Cómo cambiarlo", _pasos(["Cierra la llave de paso si tu modelo lo requiere.", "Abre el refrigerador y ubica el filtro.", "Retira el viejo con un giro suave.", "Quita las tapas del nuevo e instálalo hasta que quede firme.", "Saca unos 6 litros de agua por el dispensador.", "Reinicia el aviso del filtro en el panel."])
                    + '<p>Más detalles: <a href="cambio-e-instalacion.html">guía de instalación</a> y <a href="luz-del-filtro-de-la-nevera-lg-no-se-apaga.html">luz que no se apaga</a>.</p>')
          + seccion("LT1000P por ciudad", '<div class="city-tags">' + "".join(f'<a href="{R_LT(s)}">LT1000P en {esc(CIUDAD[s][0])}</a>' for s in CIU_LT) + "</div>", alt=True)
          + faq_html(preg_l))
pagina("lt1000p-guia-completa-filtro-lg.html", "Filtro LG LT1000P: guía completa, equivalencias y precio", f"Todo sobre el filtro LG LT1000P (LTP1000, LT 1000P): códigos equivalentes, nevecones compatibles, cómo cambiarlo y precio {cop(L['precio'])} con envío gratis.",
       "lt1000p, ltp1000, lt 1000p, filtro lg lt1000p, lt1000pc, lt1000pcs, adq74793501, filtro nevera lg lt1000p precio", [("Inicio", "index.html"), ("LT1000P", "filtro-lg-lt1000p.html"), ("Guía completa", None)], cuerpo, preg_l, [ld_producto(L)], prio="0.9", og=L["img"])

# ---- una página por ciudad grande (contenido propio por ciudad)
def _vec(s):
    d = CIUDAD[s][1]
    return [x for x in CIU_LT if x != s and CIUDAD[x][1] == d][:4]


for s in CIU_LT:
    c = CIUDAD[s]; nom = c[0].split(" (")[0]; dias = ciudad_unica.dias_de(c); h = random.Random("lt|" + s)
    area = next((v[0] for k, v in AREAS.items() if any(m_[0] == c[0] for m_ in v[2])), None)
    intro = h.choice([f"Si buscas el filtro LT1000P en {nom}, lo enviamos con envío gratis y llega en {dias}. Es la referencia que más piden quienes tienen un nevecón LG {L['modelos'][0]} o similar.",
                      f"En {nom} ({c[1]}) entregamos el filtro de agua LG LT1000P en {dias}, sin costo de envío. Pagas en línea o contra entrega.",
                      f"El LT1000P es el filtro LG que más se pide en {nom}. Lo despachamos nuevo y sellado, con envío gratis y entrega en {dias}.",
                      f"Pedir el filtro LT1000P en {nom} es fácil: lo escoges, pagas en línea o contra entrega y llega en {dias} sin costo de envío."])
    p2 = h.choice([f"Antes de despachar confirmamos que el LT1000P corresponda a tu nevecón. Si tienes un {L['modelos'][1]} o un {L['modelos'][2]}, es el filtro indicado.", f"Si tu nevecón es {L['modelos'][0]}, {L['modelos'][1]} o {L['modelos'][2]}, el LT1000P es tu filtro. Si no estás seguro, escríbenos con el código del filtro viejo.",
                   f"Verificamos la referencia antes de enviarla a {nom}: los modelos {LMOD} usan el LT1000P."])
    p3 = h.choice([f"Cámbialo cada 6 meses: así el agua y el hielo de tu nevera en {nom} mantienen el sabor.", f"En {nom}, igual que en el resto del país, el cambio recomendado es cada 6 meses de uso normal.", f"No esperes a que el agua cambie de sabor: programa el cambio del LT1000P cada 6 meses."])
    vec = _vec(s)
    cuerpo = (hero_simple(f"LT1000P · {nom}", f"Filtro LG LT1000P en {nom}", f"Precio, envío y entrega del filtro LT1000P en {nom}, {c[1]}.")
              + qa(f"¿Dónde comprar el filtro LG LT1000P en {nom}?", f"Aquí: enviamos el {esc(L['nombre'])} a {esc(nom)} con envío gratis; llega en {dias}. Cuesta <b>{cop2(L['precio'])}</b> y pagas con Wompi o contra entrega.",
                    [("Ciudad", c[0]), ("Entrega", dias), ("Precio", cop2(L["precio"])), ("Envío", "Gratis")])
              + seccion(f"Compra el LT1000P en {esc(nom)}", '<div class="tf-grid">' + tarjeta(L, 0) + "</div>")
              + seccion(f"El LT1000P en {esc(nom)}", f"<p>{esc(intro)}</p><p>{esc(p2)}</p><p>{esc(p3)}</p>" + (f"<p>Atendemos {esc(nom)} y su área ({esc(area)}).</p>" if area else "")
                        + f'<p>También buscado como {esc(ALIAS)}. Equivale a {esc(LREFS)}.</p>')
              + seccion("Datos del filtro", '<div class="tbl-wrap"><table class="spec-table">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in [("Filtro", L["nombre"]), ("Código", "LT1000P"), ("Equivalentes", LREFS), ("Nevecones", LMOD), ("Precio", cop2(L["precio"]) + " COP"), ("Entrega a " + nom, dias), ("Cambio", "Cada 6 meses")]) + "</table></div>", alt=True)
              + seccion("Más información", '<div class="city-tags"><a href="' + R_CIU(s) + f'">Envío de filtros LG a {esc(nom)}</a><a href="lt1000p-guia-completa-filtro-lg.html">Guía completa del LT1000P</a><a href="{L["url"]}">Ficha del LT1000P</a>'
                        + "".join(f'<a href="{R_LT(v)}">LT1000P en {esc(CIUDAD[v][0])}</a>' for v in vec) + "</div>"))
    pr = [(f"¿Cuánto cuesta el LT1000P en {nom}?", f"{cop2(L['precio'])} con envío gratis a {nom}."), (f"¿Cuánto tarda el envío a {nom}?", f"{dias}."), (f"¿Puedo pagar contra entrega en {nom}?", FPAGO),
          ("¿LTP1000 y LT1000P son el mismo?", "Sí, es la misma referencia escrita de otra forma."), ("¿Qué nevecones usan el LT1000P?", LMOD + ".")]
    cuerpo += faq_html(pr, f"Preguntas sobre el LT1000P en {nom}")
    pagina(R_LT(s), h.choice([f"Filtro LG LT1000P en {c[0]} | Envío gratis", f"Comprar filtro LT1000P en {c[0]} | {cop(L['precio'])}", f"LT1000P en {c[0]}: filtro LG con envío gratis"]), f"Filtro de agua LG LT1000P en {c[0]}: {cop(L['precio'])}, envío gratis y entrega en {dias}. Pago en línea o contra entrega.",
           f"lt1000p {nom.lower()}, filtro lg lt1000p {nom.lower()}, ltp1000 {nom.lower()}", [("Inicio", "index.html"), ("LT1000P", "filtro-lg-lt1000p.html"), (nom, None)], cuerpo, pr,
           [{"@type": "Product", **{k: v for k, v in ld_producto(L).items() if k != "@type"}, "offers": {**ld_producto(L)["offers"], "areaServed": {"@type": "City", "name": c[0]}}}], prio="0.6")

# ---- enlazado hacia el clúster
_insertar(L["url"], _bloque("LT1000P en tu ciudad", "".join(f'<a href="{R_LT(s)}">Filtro LT1000P en {esc(CIUDAD[s][0])}</a>' for s in CIU_LT) + '<a href="lt1000p-guia-completa-filtro-lg.html">Guía completa del LT1000P</a>'))
for s in CIU_LT:
    _insertar(R_CIU(s), _bloque(f"El más vendido en {esc(CIUDAD[s][0].split(' (')[0])}", f'<a href="{R_LT(s)}">Filtro LT1000P en {esc(CIUDAD[s][0])}</a><a href="lt1000p-guia-completa-filtro-lg.html">Guía completa del LT1000P</a>'))
E_ = (OUT / L["url"]).read_text(encoding="utf-8")
(OUT / L["url"]).write_text(E_.replace('<meta name="keywords" content="', f'<meta name="keywords" content="ltp1000, lt 1000p, lt1000, lt-1000p, ', 1), encoding="utf-8")
