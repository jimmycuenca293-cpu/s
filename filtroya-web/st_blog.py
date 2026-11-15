# Blog por país (10 artículos por país, con datos propios de cada país y ciudad) + bloques «respuesta para fragmento destacado». Se ejecuta antes de st_salida.py.
import csv as _csv


def _prin(pk):
    cs = [c for c in CIU_PAIS[pk] if not c["amp"]]
    return cs[0], cs[:3]


def _ciu_txt(pk, n=8):
    cs = CIU_PAIS[pk]
    return ", ".join(c["n"] for c in cs[:n]) + (f" y {len(cs) - n} ciudades más" if len(cs) > n else "")


AHORRO = ["Mantén la puerta de la {nev} cerrada el mayor tiempo posible y no guardes comida caliente.", "Llena la lavadora según su capacidad: lavar con poca carga gasta más agua y energía por prenda.", "Usa ciclos con agua fría cuando la ropa no lo requiera; consumen menos energía.",
          "Limpia el filtro de la secadora en cada carga: un filtro tapado alarga el ciclo y gasta más.", "Centrifuga bien la ropa antes de pasarla a la secadora.", "Separa la {nev} de la pared unos centímetros para que ventile el condensador.",
          "Carga el lavavajillas por completo antes de encenderlo.", "Tapa las ollas al cocinar y apaga el horno unos minutos antes de terminar.", "No uses el microondas vacío ni con recipientes inadecuados.", "Desconecta de la corriente los equipos que no uses por temporadas largas, usando un protector de voltaje."]
CRITERIOS = ["Hace el diagnóstico antes de reparar y te explica la falla en palabras simples.", "Te confirma el valor antes de empezar la reparación.", "Pregunta por el modelo y por el código de error antes de ir.", "Va a tu domicilio y trabaja con herramientas propias.", "Responde rápido por WhatsApp y coordina un día y una franja concretos.",
             "Cambia solo lo necesario y te muestra la pieza reemplazada.", "Prueba el equipo contigo antes de irse.", "Te orienta con honestidad si conviene reparar o cambiar el equipo.", "Tiene experiencia con la marca de tu equipo.", "Te explica cómo evitar que la falla se repita."]
VIDA = [("Ruido nuevo o vibración fuerte", "Normalmente se repara", "Se evalúa si hay daño en el compresor o el motor"), ("El equipo no enciende", "Muchas veces es fuente o tarjeta: se repara", "Si la tarjeta ya no se consigue, el técnico lo dice"),
        ("Fuga o humedad", "Se repara si es manguera, sello o desagüe", "Se evalúa si el tanque o el evaporador están dañados"), ("Falla repetida tras varias reparaciones", "Conviene un diagnóstico completo", "Puede convenir cambiar el equipo si la causa es estructural"),
        ("Consumo de energía muy alto", "Se revisan sellos, ventiladores y sensores", "Si el compresor está agotado, se compara costo de reparación y de un equipo nuevo")]
BLOG = []
_G4, _G5, _GU = [next(g for g in GUIAS if g['slug'].endswith(x)) for x in ('codigo-4e', 'codigo-5e', 'codigo-ue')]  # (pk, slug, titulo, url)
R_BLOG = lambda pk, sl: f"{pk}/blog/{sl}/index.html"
CAT = {"cuidado-clima": "Cuidado del equipo", "vida-util": "Reparar o cambiar", "checklist-visita": "Antes de la visita", "corte-de-luz": "Electricidad", "errores-lavadora": "Lavadoras", "secadora-lluvias": "Secadoras", "ahorro-energia": "Ahorro de energía",
       "mitos": "Mitos y verdades", "mantenimiento-anual": "Mantenimiento", "elegir-tecnico": "Cómo elegir técnico"}
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; c0, top = _prin(pk); v = VOLT[pk]
    nev1, nev2 = pal(pk, "nevera"); lav1, lav2 = pal(pk, "lava"); sec1, sec2 = pal(pk, "seca")
    cl0 = CLIMA[c0["s"]]; wa = wa_vis(pk)
    posts = []
    # 1
    secc = "".join(seccion(f"{esc(c['n'])}: qué le pasa a tu {esc(nev1)}", f"<p>{esc(parrafo_clima(c, c['zonas'][0], 'nevera', f'b1|{pk}|{c['s']}'))}</p><p>{esc(uno(f'b1t|{pk}|{c['s']}', TIPS['nevera']))}</p>", alt=(i % 2 == 1)) for i, c in enumerate(top[:2]))
    posts.append(("cuidado-clima", f"Cuidar tu {nev1} Samsung en {P['nombre']}: clima y hábitos", f"Consejos para que tu {nev1} Samsung rinda más en el clima de {c0['n']} y otras ciudades de {P['nombre']}: ventilación, sellos, voltaje y mantenimiento.",
                  f"Para cuidar tu {nev1} Samsung en {P['nombre']}, déjala ventilada, limpia el condensador cada seis meses, revisa los sellos de las puertas y protégela con un regulador de voltaje ({v[0]}). En {c0['n']}, con un clima {cl0['clima']}, vigila especialmente {cl0['riesgo']}.",
                  secc + seccion(f"Cinco hábitos para cualquier ciudad de {esc(P['nombre'])}", "<ol class=\"vl\">" + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b1h|{pk}", TIPS["nevera"], 5)) + "</ol>", alt=True)
                  + seccion("Electricidad", f"<p>La red de {esc(P['nombre'])} es de {v[0]} a {v[1]}. Un protector de voltaje reduce el riesgo de daños en la tarjeta y el compresor de tu {esc(nev1)}.</p>"),
                  [(f"¿Cada cuánto limpiar el condensador de la {nev1}?", "Cada seis meses es una referencia razonable; antes si hay mucho polvo."), (f"¿Cómo afecta el clima de {c0['n']} a mi {nev1} Samsung?", f"{cap(efecto_de(c0, 'nevera'))}."), ("¿Dónde pido un técnico?", f"Por WhatsApp al {wa}; hacemos el diagnóstico en tu casa.")]))
    # 2
    tabla = '<div class="tbl-wrap"><table class="spec-table"><tr><th>Síntoma</th><th>Lo habitual</th><th>Cuándo pensar en cambiar</th></tr>' + "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c_)}</td></tr>" for a, b, c_ in VIDA) + "</table></div>"
    posts.append(("vida-util", f"¿Cuánto dura tu {nev1} Samsung en {P['nombre']}?", f"Qué influye en la vida útil de una {nev1} Samsung en {P['nombre']} y cómo decidir entre reparar o cambiar el equipo según la falla.",
                  f"La vida útil de una {nev1} Samsung depende del uso, del mantenimiento y de la electricidad (en {P['nombre']}: {v[0]}, {v[1]}). Casi todas las fallas se reparan; conviene cambiar el equipo solo si el daño es estructural y el costo se acerca al de uno nuevo.",
                  seccion("Qué hace que dure más", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b2|{pk}", TIPS["nevera"], 4)) + f"<li>Protector de voltaje ({esc(v[0])}).</li><li>Ventilación detrás y a los lados.</li></ul>")
                  + seccion("¿Reparar o cambiar?", tabla, alt=True) + seccion(f"En {esc(c0['n'])}", f"<p>{esc(parrafo_clima(c0, c0['zonas'][0], 'nevera', f'b2c|{pk}'))}</p>"),
                  [(f"¿Se puede reparar una {nev1} Samsung vieja?", "Casi siempre; depende de la falla y de si el repuesto se consigue."), ("¿Cómo sé si conviene cambiarla?", "Cuando el costo de reparar se acerca al de un equipo nuevo o la falla es estructural; el técnico te orienta en el diagnóstico."), (f"¿Reparan {nev2} Samsung en {P['nombre']}?", f"Sí, en {_ciu_txt(pk, 6)}.")]))
    # 3
    posts.append(("checklist-visita", f"Checklist antes de pedir un técnico Samsung en {P['nombre']}", f"Qué tener listo antes de la visita de un técnico Samsung en {P['nombre']}: modelo, código de error, fotos y dirección.",
                  f"Antes de pedir un técnico Samsung en {P['nombre']}, anota el modelo de la etiqueta, el código de error del panel y desde cuándo falla; toma una foto o video corto y escribe por WhatsApp al {wa}.",
                  seccion("Lo que debes tener listo", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b3|{pk}", ANTES, 6)) + "</ul>")
                  + seccion("Cómo es la visita", '<ol class="vl">' + "".join(f"<li>{esc(x.format(z=c0['zonas'][0], c=c0['n']))}</li>" for x in VISITA[H(pk) % len(VISITA)]) + "</ol>", alt=True)
                  + seccion("Ciudades donde atendemos", f"<p>{esc(_ciu_txt(pk, 14))}.</p>"),
                  [("¿Qué es lo más importante que debo decir?", "El modelo, la falla y la dirección."), ("¿Puedo mandar fotos?", "Sí, por WhatsApp."), ("¿El valor se confirma antes?", "Sí, siempre antes de reparar.")]))
    # 4
    posts.append(("corte-de-luz", f"{cap(nev1)} Samsung en un corte de luz en {P['nombre']}", f"Pasos para proteger tus alimentos y tu {nev1} Samsung durante un corte de luz y cuando vuelve la energía en {P['nombre']}.",
                  f"Durante un corte de luz, mantén cerrada la puerta de la {nev1}: así conserva el frío por varias horas. Cuando vuelva la energía, espera unos minutos antes de volver a conectarla si se desconectó, y usa un protector de voltaje.",
                  seccion("Durante el corte", '<ol class="vl"><li>No abras la puerta sin necesidad.</li><li>Agrupa los alimentos en el congelador para que se mantengan fríos entre sí.</li><li>Si el corte es largo, usa una nevera portátil con hielo para lo esencial.</li><li>Evita volver a llenar la nevera con comida caliente.</li></ol>')
                  + seccion("Cuando vuelve la luz", f"<p>Si la {esc(nev1)} se desconectó, espera unos minutos antes de volver a conectarla. Un protector de voltaje evita daños por picos al regresar la energía. En {esc(c0['n'])}, el riesgo principal es: {esc(cl0['riesgo'])}.</p>", alt=True),
                  [(f"¿Cuánto frío conserva una {nev1} sin energía?", "Con la puerta cerrada, varias horas; depende del llenado y de la temperatura ambiente."), ("¿Debo desconectarla en tormentas?", "Si no tienes protector de voltaje, es recomendable."), ("¿Y si no vuelve a enfriar?", f"Escríbenos por WhatsApp al {wa}.")]))
    # 5
    posts.append(("errores-lavadora", f"Errores comunes con la {lav1} Samsung en {P['nombre']}", f"Los errores más frecuentes al usar una {lav1} Samsung en {P['nombre']}: exceso de detergente, sobrecarga, puerta cerrada y códigos ignorados.",
                  f"Los errores más comunes con una {lav1} Samsung son usar demasiado detergente, sobrecargar el tambor, cerrar la puerta al terminar y ignorar los códigos de error (4E, 5E, UE, dE, LE). Evitarlos prolonga su vida y evita malos olores.",
                  seccion("Los errores", '<ol class="vl">' + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b5|{pk}", TIPS["lava"], 6)) + "</ol>")
                  + seccion("Códigos que no debes ignorar", f"<p>Consulta la <a href=\"{R_COD_LISTA(pk)}\">lista de códigos de error</a> y las guías de <a href=\"{R_G(_G4, pk)}\">4E</a>, <a href=\"{R_G(_G5, pk)}\">5E</a> y <a href=\"{R_G(_GU, pk)}\">UE</a>.</p>", alt=True)
                  + seccion(f"En {esc(c0['n'])}", f"<p>{esc(parrafo_clima(c0, c0['zonas'][0], 'lava', f'b5c|{pk}'))}</p>"),
                  [("¿Cuánto detergente usar?", "El indicado por el fabricante según la dureza del agua y la carga; el exceso deja residuos."), (f"¿Debo dejar la puerta abierta?", "Sí, entreabierta, para que el sello se seque."), ("¿Qué hago si aparece un código?", f"Anótalo y escríbenos al {wa}.")]))
    # 6
    lluvia = cl0["lluvia"]
    posts.append(("secadora-lluvias", f"{cap(sec1)} Samsung en lluvias: cuidados en {P['nombre']}", f"Cómo cuidar tu {sec1} Samsung en la época de lluvias de {P['nombre']} ({lluvia}): filtro, ducto, ventilación y carga.",
                  f"En la época de lluvias ({lluvia} en {c0['n']}) la {sec1} trabaja más: limpia el filtro de pelusa en cada carga, revisa que el ducto no esté tapado, no la sobrecargues y deja ventilado el espacio.",
                  seccion("Qué cambia con las lluvias", f"<p>{esc(parrafo_clima(c0, c0['zonas'][0], 'seca', f'b6|{pk}'))}</p>") + seccion("Cuidados", "<ol class=\"vl\">" + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b6t|{pk}", TIPS["seca"], 5)) + "</ol>", alt=True),
                  [(f"¿Cada cuánto limpiar el filtro de la {sec1}?", "En cada carga."), ("¿Por qué tarda más en secar?", "Filtro o ducto tapados, sobrecarga o falla de calentamiento."), (f"¿Reparan {sec2} Samsung en {P['nombre']}?", f"Sí, en {_ciu_txt(pk, 6)}.")]))
    # 7
    posts.append(("ahorro-energia", f"Cómo ahorrar energía con tus electrodomésticos Samsung en {P['nombre']}", f"Hábitos sencillos para gastar menos energía con tu {nev1}, {lav1} y {sec1} Samsung en {P['nombre']}.",
                  f"Para ahorrar energía con tus electrodomésticos Samsung: mantén la {nev1} ventilada y bien cerrada, llena la {lav1} según su capacidad, limpia el filtro de la {sec1} en cada carga y usa un protector de voltaje ({v[0]}).",
                  seccion("Hábitos que ahorran", "<ul class=\"spec-list\">" + "".join(f"<li>{esc(x.format(nev=nev1))}</li>" for x in mix(f"b7|{pk}", AHORRO, 7)) + "</ul>")
                  + seccion("Electricidad en tu país", f"<p>En {esc(P['nombre'])} la red es de {v[0]} y {v[1]} (enchufes {v[2]}). Revisa la placa del equipo para confirmar que corresponde.</p>", alt=True),
                  [("¿Un equipo viejo gasta más?", "Puede gastar más si tiene sellos o ventiladores en mal estado; una revisión lo detecta."), ("¿Sirve desconectar equipos que no uso?", "Sí, con un protector de voltaje."), ("¿Dónde reviso mi equipo?", f"Escríbenos al {wa}.")]))
    # 8
    pares = [(sv, m) for sv in SERV_PAIS[pk] for m in MITOS.get(sv, [])]
    posts.append(("mitos", f"Mitos y verdades sobre los electrodomésticos Samsung en {P['nombre']}", f"Seis mitos frecuentes sobre {nev2}, {lav2} y {sec2} Samsung en {P['nombre']} y lo que realmente conviene hacer.",
                  f"Algunos mitos comunes: poner la {nev1} al máximo frío no la enfría más rápido, más detergente no lava mejor y un ciclo más largo no seca mejor si el filtro está tapado. La verdad casi siempre es mantenimiento y buenos hábitos.",
                  seccion("Seis mitos", "<ul class=\"spec-list\">" + "".join(f"<li><b>Mito:</b> {esc(m[0])}<br><b>Verdad:</b> {esc(m[1])}</li>" for sv, m in mix(f"b8|{pk}", pares, 6)) + "</ul>"),
                  [("¿De dónde salen los mitos?", "De costumbres que funcionaban en equipos antiguos."), ("¿Cómo salgo de dudas?", f"Pregúntanos por WhatsApp al {wa}."), ("¿Reparan en mi ciudad?", f"Atendemos {_ciu_txt(pk, 6)}.")]))
    # 9
    tab9 = (f'<div class="tbl-wrap"><table class="spec-table"><tr><th>Época</th><th>Qué hacer</th></tr><tr><td>Antes de las lluvias ({esc(lluvia)})</td><td>{esc(" ".join(mix(f"b9a|{pk}", CAL["pre"], 2)))}</td></tr>'
            f'<tr><td>Durante las lluvias</td><td>{esc(" ".join(mix(f"b9b|{pk}", CAL["lluvia"], 2)))}</td></tr><tr><td>Después</td><td>{esc(" ".join(mix(f"b9c|{pk}", CAL["despues"], 2)))}</td></tr><tr><td>Época seca</td><td>{esc(" ".join(mix(f"b9d|{pk}", CAL["seca"], 2)))}</td></tr></table></div>')
    posts.append(("mantenimiento-anual", f"Mantenimiento anual de tus Samsung en {P['nombre']}", f"Qué hacer antes, durante y después de las lluvias ({lluvia}) para mantener tu línea blanca Samsung en {P['nombre']}.",
                  f"El mantenimiento anual de tu línea blanca Samsung en {P['nombre']} se organiza por épocas: revisión de sellos y mangueras antes de las lluvias ({lluvia}), cuidados durante la temporada y limpieza profunda cuando termina.",
                  seccion("Calendario", tab9) + seccion("Guías por ciudad", '<div class="city-tags">' + "".join(f'<a href="{R_MANT(c)}">Mantenimiento en {esc(c["n"])}</a>' for c in cs[:12]) + "</div>", alt=True),
                  [("¿Cada cuánto debo hacer mantenimiento?", "Una revisión preventiva al año y limpieza periódica de filtros y condensadores."), ("¿Cuándo es mejor revisar?", f"Antes de las lluvias ({lluvia})."), ("¿Hacen mantenimiento a domicilio?", f"Sí, escribe al {wa}.")]))
    # 10
    posts.append(("elegir-tecnico", f"Elegir técnico de electrodomésticos en {c0['n']}, {P['nombre']}", f"Diez criterios para elegir un técnico de electrodomésticos Samsung en {c0['n']}: diagnóstico previo, valor confirmado, honestidad y respuesta rápida.",
                  f"Un buen técnico de electrodomésticos hace el diagnóstico antes de reparar, te confirma el valor antes de empezar, te explica la falla con claridad y te orienta con honestidad si conviene reparar o cambiar el equipo.",
                  seccion("Criterios para elegir", "<ol class=\"vl\">" + "".join(f"<li>{esc(x)}</li>" for x in mix(f"b10|{pk}", CRITERIOS, 7)) + "</ol>") + seccion(f"Dónde pedirlo en {esc(P['nombre'])}", f"<p>{esc(_ciu_txt(pk, 14))}.</p><p><a href=\"{R_CIU(c0)}\">Soporte técnico Samsung en {esc(c0['n'])}</a></p>", alt=True),
                  [("¿Debo pagar antes de que repare?", "Pide siempre el valor confirmado antes de reparar y acuerda la forma de pago."), ("¿Y si no quiero reparar?", "Puedes decidir tras el diagnóstico."), ("¿Cómo contacto?", f"Por WhatsApp al {wa}.")]))
    for sl, tit, desc, res, cuerpo_p, preg in posts:
        otros = [x for x in posts if x[0] != sl]
        rel = '<div class="link-grid">' + "".join(f'<a href="{R_BLOG(pk, o[0])}">{esc(o[1])}</a>' for o in mix(f"rel|{pk}|{sl}", otros, 4)) + "</div>"
        cuerpo = (hero_simple(f"Blog · {P['nombre']} · {CAT[sl]}", tit, desc, acciones(pk, f"Hola, leí su artículo «{tit}» y necesito un técnico Samsung"))
                  + qa(tit if tit.endswith("?") else f"{tit.split(':')[0].split(' en ')[0]}: la respuesta rápida", esc(res), [("Categoría", CAT[sl]), ("País", P["nombre"]), ("Lectura", "4 min"), ("Actualizado", FECHA_LARGA)])
                  + cuerpo_p + faq_html(preg) + seccion("Sigue leyendo", rel, alt=True)
                  + seccion("¿Necesitas un técnico?", f'<div class="city-tags"><a href="{R_PAIS(pk)}">Soporte técnico Samsung en {esc(P["nombre"])}</a>' + "".join(f'<a href="{R_CIU(c)}">{esc(c["n"])}</a>' for c in cs[:8]) + "</div>"))
        art = {"@type": "BlogPosting", "headline": tit, "description": desc, "inLanguage": P["cod"], "datePublished": HOY, "dateModified": HOY, "articleSection": CAT[sl], "author": {"@type": "Organization", "name": NOMBRE},
               "publisher": {"@id": f"{DOMINIO}/#negocio"}, "mainEntityOfPage": U(R_BLOG(pk, sl))}
        pagina(R_BLOG(pk, sl), tit, desc, f"{tit.lower()}, blog servicio tecnico samsung {P['nombre'].lower()}", [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Blog", f"{pk}/blog/index.html"), (CAT[sl], None)], cuerpo, preg, [art], prio="0.6", pk=pk, tipo="blog")
        BLOG.append((pk, sl, tit, R_BLOG(pk, sl), desc))
    lista = "".join(f'<a href="{u}" style="display:block;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:#fff;margin-bottom:10px;text-decoration:none;color:var(--ink)"><b>{esc(t)}</b><br><small style="color:var(--mute)">{esc(d)}</small></a>' for k, sl, t, u, d in BLOG if k == pk)
    pagina(f"{pk}/blog/index.html", f"Blog de servicio técnico Samsung en {P['nombre']}", f"Artículos sobre cuidado, fallas, mantenimiento y electricidad de tus electrodomésticos Samsung en {P['nombre']}: guías prácticas del centro de servicio técnico.", f"blog servicio tecnico samsung {P['nombre'].lower()}, consejos electrodomesticos samsung",
           [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Blog", None)], hero_simple(f"Blog · {P['nombre']}", f"Blog de soporte técnico Samsung en {P['nombre']}", "Guías prácticas para cuidar y reparar tus electrodomésticos.")
           + qa(f"¿Dónde encuentro consejos para mis electrodomésticos Samsung en {P['nombre']}?", f"En este blog: cuidado según el clima de {esc(P['nombre'])}, qué hacer en un corte de luz, mantenimiento anual, mitos y cómo elegir un buen técnico.") + seccion("Artículos", lista), [], [], prio="0.7", pk=pk, tipo="blog")

# ------------------------------------------------------------------ enlazar el blog desde cada país, ciudad y guía
for pk, P in PAISES.items():
    _ins(R_PAIS(pk), seccion(f"Blog del servicio técnico Samsung en {esc(P['nombre'])}", '<div class="city-tags">' + "".join(f'<a href="{u}">{esc(t)}</a>' for k, sl, t, u, d in BLOG if k == pk) + "</div>"))
    for c in CIU_PAIS[pk]:
        if c["amp"]:
            continue
        _ins(R_CIU(c), seccion(f"Artículos del blog para {esc(c['n'])}", '<div class="city-tags">' + "".join(f'<a href="{u}">{esc(t)}</a>' for k, sl, t, u, d in mix(f"bl|{c['s']}", [b for b in BLOG if b[0] == pk], 4)) + f'<a href="{pk}/blog/index.html"><b>Ver todo el blog →</b></a></div>', alt=True))

