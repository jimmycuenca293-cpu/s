#!/usr/bin/env python3
"""Política de privacidad, términos y condiciones, ampliación de «Quiénes somos» y un blog más grande para samsungpanamaserviciotecnico.com.
Uso: python3 pa_contenido.py <carpeta_del_sitio>   (ejecutar ANTES de pa_diseno.py)"""
import datetime, html, json, pathlib, re, sys
from pa_cfg import CFG
R = pathlib.Path(sys.argv[1])
DOM = CFG["dom"]
HOY = datetime.date.today().isoformat()
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
FECHA = f"{datetime.date.today().day} de {MESES[datetime.date.today().month - 1]} de {datetime.date.today().year}"
TEL, WAN, DIR, NOMBRE = CFG["tel"], CFG["wa"], CFG["dir"], CFG["nombre"]
CIU, CORTO = CFG["ciudad"], CFG["corto"]
def loc(x):
    if CORTO == "Panamá" or not isinstance(x, str): return x.replace("110-120 V a 60 Hz", CFG["voltaje"]) if isinstance(x, str) else x
    return x.replace("110-120 V a 60 Hz", CFG["voltaje"]).replace("Ciudad de Panamá", CIU).replace("República de Panamá", "República de Colombia").replace("Panamá", CORTO)
esc = lambda s: html.escape(s, quote=True)
txt = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()
P = lambda *x: "".join(f"<p>{a}</p>" for a in x)
UL = lambda items: "<ul>" + "".join(f"<li>{a}</li>" for a in items) + "</ul>"
OL = lambda items: "<ol>" + "".join(f"<li>{a}</li>" for a in items) + "</ol>"
TB = lambda cab, filas: "<div class='tbl-wrap'><table class='spec-table'><tr>" + "".join(f"<th>{c}</th>" for c in cab) + "</tr>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in f) + "</tr>" for f in filas) + "</table></div>"
T1 = (R / "quienes-somos" / "index.html").read_text(encoding="utf-8")          # plantilla a 1 nivel
T2 = (R / "blog" / "vida-util" / "index.html").read_text(encoding="utf-8")     # plantilla a 2 niveles
def shell(tpl, nivel, ruta, titulo, desc, ld, cuerpo):
    h = tpl[: tpl.find("</head>")]; resto = tpl[tpl.find("</head>"):]
    url = f"{DOM}/{ruta}"
    h = re.sub(r"<title>.*?</title>", f"<title>{esc(titulo)}</title>", h, count=1, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + esc(desc) + m.group(2), h, count=1)
    h = re.sub(r'<meta name="keywords"[^>]*>', "", h)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="alternate" hreflang="es-PA" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    for k in ("og:title", "twitter:title"):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*(")', lambda m: m.group(1) + esc(titulo) + m.group(2), h, count=1)
    for k in ("og:description", "twitter:description"):
        h = re.sub(rf'(<meta (?:property|name)="{k}" content=")[^"]*(")', lambda m: m.group(1) + esc(desc) + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'<script type="application/ld\\+json">.*?</script>', "", h, flags=re.S)
    h += f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False)}</script>'
    a = resto.find('<div class="breadcrumb'); z = resto.find("<footer")
    return h + resto[:a] + cuerpo + resto[z:]
def miga(nivel, items):
    p = "../" * nivel
    return '<div class="breadcrumb wrap" style="font:500 13px Inter,sans-serif;padding:16px 22px 0;">' + " / ".join(f'<a href="{p}{u}">{esc(n)}</a>' if u is not None else esc(n) for n, u in items) + "</div>"
def ld_base(ruta, titulo, desc, items):
    return [{"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": f"{DOM}/{u}"} if u is not None else {})} for i, (n, u) in enumerate(items)]},
            {"@type": "WebPage", "@id": f"{DOM}/{ruta}", "name": titulo, "url": f"{DOM}/{ruta}", "inLanguage": "es-PA", "description": desc, "dateModified": HOY}]
ORG = {"@type": "Organization", "name": NOMBRE, "url": DOM + "/", "telephone": CFG["tel_link"], "logo": {"@type": "ImageObject", "url": DOM + "/img/samsung-oval.png"}}
HERO = lambda kick, h1, sub, extra="": f'<section class="pa-hero pa-hero-s"><div class="pa-w"><span class="pa-kick">{esc(kick)}</span><h1>{esc(h1)}</h1><p>{esc(sub)}</p>{extra}</div></section>'
# ======================================================================= LEGALES
def pagina_legal(ruta, titulo, h1, desc, secciones):
    toc = "".join(f'<li><a href="#s{i}">{esc(t)}</a></li>' for i, (t, _) in enumerate(secciones))
    cuerpo = "".join(f'<h2 id="s{i}">{esc(t)}</h2>{c}' for i, (t, c) in enumerate(secciones))
    body = (miga(1, [("Inicio", ""), (h1, None)]) + HERO("Información legal", h1, f"Última actualización: {FECHA}.")
            + f'<main class="pa-art"><div class="pa-w pa-cols"><article class="pa-prose"><nav class="pa-toc"><b>En esta página</b><ol>{toc}</ol></nav>{cuerpo}</article><aside class="pa-aside"><div class="pa-card"><h3>¿Dudas?</h3><p>Escríbenos y te respondemos.</p><a class="pa-b wa" style="width:100%" href="https://wa.me/{WAN}" target="_blank" rel="noopener">WhatsApp {TEL}</a></div></aside></div></main>')
    d = shell(T1, 1, ruta, titulo, desc, ld_base(ruta, titulo, desc, [("Inicio", ""), (h1, ruta)]), body)
    (R / ruta.rstrip("/")).mkdir(parents=True, exist_ok=True); (R / ruta.rstrip("/") / "index.html").write_text(d, encoding="utf-8")
DATOS = f"<b>{NOMBRE}</b>, con dirección de atención en {DIR}, teléfono y WhatsApp {TEL}"
pagina_legal("politica-de-privacidad/", f"Política de privacidad | {NOMBRE}", "Política de privacidad", f"Cómo {NOMBRE} recoge, usa y protege tus datos personales cuando pides una visita o nos escribes por WhatsApp. Derechos y contacto.", [
    ("Quién es el responsable", P(f"El responsable del tratamiento de tus datos es {DATOS}. Este sitio es un servicio técnico independiente de electrodomésticos Samsung en " + CIU + " y no es el canal oficial de Samsung Electronics.", "Esta política se redacta teniendo en cuenta " + CFG["ley_datos"] + ".")),
    ("Qué datos recogemos", P("Solo pedimos lo necesario para coordinar tu servicio:") + UL(["Nombre y teléfono o WhatsApp.", "Barrio o dirección donde se hará la visita.", "Equipo, modelo, descripción de la falla y, si las envías, fotos del equipo o de su etiqueta.", "Los datos que escribas por voluntad propia en el formulario de solicitud de visita o en el chat de WhatsApp."]) + P("No pedimos datos bancarios en este sitio ni datos sensibles.")),
    ("Para qué usamos tus datos", UL(["Responder tu consulta y coordinar el día y la franja de la visita.", "Diagnosticar el equipo y confirmarte el valor antes de reparar.", "Dar seguimiento al servicio y atender reclamos o garantías del trabajo realizado.", "Mejorar la información de este sitio, sin identificarte personalmente."]) + P("No vendemos ni alquilamos tus datos, y no los usamos para publicidad de terceros.")),
    ("Base para tratar tus datos", P("Tratamos tus datos porque nos los entregas voluntariamente para solicitar un servicio, es decir, con tu consentimiento y para atender tu solicitud. Puedes retirarlo cuando quieras escribiéndonos.")),
    ("Con quién los compartimos", P("Solo con las personas que necesitan conocerlos para prestarte el servicio, como el técnico que hará la visita. Además, usamos proveedores que procesan datos por nuestra cuenta:") + UL(["WhatsApp (Meta Platforms), cuando nos escribes por ese canal. Se rige por sus propias condiciones.", "El proveedor de alojamiento del sitio web y del correo, donde se guardan las solicitudes del formulario.", "Google Maps, que se muestra incrustado en algunas páginas y puede instalar cookies propias."]) + P("También podemos entregar datos si una autoridad competente lo exige conforme a la ley.")),
    ("Cookies y medición", P("Este sitio no usa cookies de publicidad. Los mapas de Google incrustados pueden instalar cookies de Google al cargarse. Si en el futuro activamos una herramienta de analítica, actualizaremos esta política y lo informaremos.")),
    ("Cuánto tiempo los conservamos", P("Guardamos tus datos mientras sean necesarios para atender tu solicitud, el seguimiento del servicio y las obligaciones legales o de garantía. Luego los eliminamos o los dejamos anónimos.")),
    ("Tus derechos", P("Tienes derecho a " + CFG["derechos"] + ". Para ejercerlos, escríbenos por WhatsApp al " + TEL + " indicando qué quieres hacer y con qué nombre y teléfono nos contactaste. Respondemos en un plazo razonable.", "Si crees que tus derechos no fueron atendidos, puedes acudir a " + CFG["autoridad_datos"] + ".")),
    ("Seguridad", P("Aplicamos medidas razonables para proteger tus datos, como limitar quién accede a ellos. Ninguna transmisión por internet es completamente segura, por lo que te recomendamos no enviar datos que no sean necesarios.")),
    ("Menores de edad", P("Nuestros servicios son para personas adultas que son dueñas o responsables del equipo. No recogemos datos de menores de forma intencional.")),
    ("Cambios a esta política", P(f"Podemos actualizar esta política. La fecha de la última actualización aparece arriba ({FECHA}). Te recomendamos revisarla de vez en cuando.")),
    ("Contacto", P(f"Para cualquier tema sobre tus datos: WhatsApp y teléfono {TEL}. Dirección de atención: {DIR}. Horario: abierto las 24 horas."))])
pagina_legal("terminos-y-condiciones/", f"Términos y condiciones | {NOMBRE}", "Términos y condiciones", f"Condiciones de uso del sitio y del servicio técnico a domicilio de {NOMBRE}: solicitud, diagnóstico, cotización, garantía y derechos del consumidor.", [
    ("Quiénes somos y aceptación", P(f"Estos términos regulan el uso de este sitio web y la contratación del servicio técnico de {DATOS}. Al usar el sitio o solicitar un servicio, aceptas estas condiciones.")),
    ("Servicio independiente y marcas", P("Somos un servicio técnico independiente que repara electrodomésticos Samsung. No pertenecemos a Samsung Electronics Co., Ltd., ni somos su canal oficial de soporte. Samsung y su logotipo son marcas de sus propietarios y se usan solo para indicar la marca del equipo que reparamos.")),
    ("Qué servicio ofrecemos", P("Visita técnica a domicilio en " + CIU + " y alrededores para diagnóstico, reparación y mantenimiento de refrigeradoras, lavadoras, secadoras, lavavajillas, estufas y hornos, y microondas. La disponibilidad depende del barrio, del equipo y del repuesto.")),
    ("Cómo se solicita", OL(["Escríbenos por WhatsApp o llena el formulario con el equipo, el modelo, la falla y tu barrio.", "Coordinamos el día y una franja para la visita.", "El técnico revisa el equipo en tu domicilio y te explica la falla y las opciones.", "Antes de empezar, te confirma el valor de la reparación. Solo se repara si tú lo aceptas."])),
    ("Diagnóstico, cotización y aprobación", P("El valor del servicio depende del equipo, la falla, el repuesto y la zona, y se te informa antes de iniciar el trabajo. No se cambia ninguna pieza sin tu aprobación. Si decides no reparar, se te informa el costo del diagnóstico antes de la visita cuando corresponda.")),
    ("Repuestos, tiempos y garantía del trabajo", P("Los tiempos de reparación dependen de la disponibilidad del repuesto y se informan cuando se conocen. La garantía del trabajo y de las piezas instaladas se indica al momento de la cotización y se aplica a la falla reparada. No cubre daños por mal uso, golpes, líquidos, variaciones eléctricas ni manipulación posterior por terceros.")),
    ("Garantía de fábrica", P("La garantía de fábrica de tu equipo la gestiona Samsung o la tienda donde lo compraste. Si tu equipo está en garantía, revisa sus condiciones en el manual antes de que alguien lo intervenga: abrir o reparar un equipo por fuera del servicio de fábrica puede afectar esa garantía.")),
    ("Tus responsabilidades", UL(["Darnos información real sobre el equipo y la falla.", "Permitir el acceso seguro al equipo, desconectado y con espacio para trabajar.", "Respaldar o retirar lo que tengas dentro del equipo si corresponde (por ejemplo, alimentos o ropa).", "Estar presente o dejar a un adulto responsable durante la visita."])),
    ("Pagos", P("Las formas y el momento de pago se acuerdan al confirmar la cotización y antes de iniciar el trabajo. Te entregaremos constancia del servicio realizado.")),
    ("Derechos del consumidor", P("Esto no limita los derechos que te reconoce " + CFG["ley_consumo"] + ". Puedes presentar quejas ante " + CFG["autoridad_consumo"] + ".")),
    ("Contenido del sitio", P("La información de este sitio es de orientación general y puede actualizarse. Las guías de fallas no sustituyen la revisión de un técnico, y no debes abrir equipos conectados a la corriente ni manipular instalaciones de gas por tu cuenta.")),
    ("Propiedad intelectual y enlaces", P("Los textos, imágenes y el diseño de este sitio son de sus autores y no pueden copiarse sin permiso. Si enlazamos a páginas de terceros, no controlamos su contenido.")),
    ("Ley aplicable", P("Estos términos se rigen por " + CFG["ley_aplicable"] + ".")),
    ("Cambios y contacto", P(f"Podemos actualizar estos términos; la fecha de la última actualización es {FECHA}. Contacto: WhatsApp y teléfono {TEL}, {DIR}."))])
# Quiénes somos: bloque de transparencia al final
q = R / "quienes-somos" / "index.html"; tq = q.read_text(encoding="utf-8")
if "Datos del negocio" not in tq:
    bloque = ('<section class="aq-sec chap"><div class="wrap"><h2>Datos del negocio y transparencia</h2>'
              f'<div class="tbl-wrap"><table class="spec-table"><tr><td><b>Nombre</b></td><td>{NOMBRE}</td></tr><tr><td><b>Dirección de atención</b></td><td>{DIR}</td></tr><tr><td><b>Horario</b></td><td>{CFG["horario"]}</td></tr><tr><td><b>Teléfono y WhatsApp</b></td><td>{TEL}</td></tr><tr><td><b>Cobertura</b></td><td>{CFG["cobertura"]}</td></tr><tr><td><b>Tipo de servicio</b></td><td>Servicio técnico independiente de electrodomésticos Samsung, a domicilio</td></tr></table></div>'
              '<p>Somos un servicio técnico independiente: no pertenecemos a Samsung ni somos su canal oficial. Reparamos equipos Samsung y te decimos el valor antes de empezar. Lee nuestros <a href="../terminos-y-condiciones/">términos y condiciones</a> y nuestra <a href="../politica-de-privacidad/">política de privacidad</a>.</p></div></section>')
    z = tq.find("<footer"); q.write_text(tq[:z] + bloque + tq[z:], encoding="utf-8")
# ======================================================================= BLOG
CATS = {"refri": "Refrigeradoras" if CORTO == "Panamá" else "Neveras", "lava": "Lavadoras y secadoras", "cocina": "Cocina y seguridad", "clima": CFG["cats_clima"], "decide": "Decisiones y garantía"}
ART = {}   # slug -> dict
TT = {'codigos-de-error-lavadora-samsung': 'Códigos de error de lavadoras Samsung: 5E, 4E, UE, dE, LE', 'refrigeradora-samsung-con-escarcha-causas': 'Refrigeradora Samsung con escarcha: causas y qué revisar', 'modelo-samsung-donde-esta-y-que-significa': 'Dónde está el modelo de tu Samsung y qué significa', 'voltaje-y-proteccion-refrigeradora-panama': 'Voltaje en Panamá: cómo proteger tu refrigeradora', 'humedad-y-salitre-en-electrodomesticos-panama': 'Humedad y salitre en Panamá: cómo afectan tus equipos', 'como-se-cobra-una-reparacion-de-electrodomesticos': 'Cómo se cobra una reparación de electrodomésticos', 'garantia-de-fabrica-o-tecnico-independiente': 'Garantía de fábrica o técnico independiente: cuál elegir', 'lavadora-samsung-huele-mal-como-limpiarla': 'Lavadora Samsung con mal olor: causas y cómo limpiarla', 'lavavajillas-samsung-mantenimiento-y-fallas': 'Lavavajillas Samsung: mantenimiento y fallas comunes', 'estufa-y-horno-olor-a-gas-seguridad': 'Estufa y horno: qué hacer si hueles gas', 'microondas-samsung-no-calienta-que-hacer': 'Microondas Samsung que no calienta: causas y precauciones', 'senales-de-que-tu-refrigeradora-necesita-revision': '7 señales de que tu refrigeradora Samsung necesita revisión'}
def art(slug, cat, titulo, desc, intro, secciones, faq, kw=""):
    if slug == "humedad-y-salitre-en-electrodomesticos-panama" and not CFG["humedad"]:
        return
    if CORTO != "Panamá": slug = slug.replace("-panama", "-" + CORTO.lower())
    ART[slug] = dict(slug=slug, cat=cat, titulo=loc(titulo), desc=loc(desc), intro=loc(intro), secciones=[(loc(a), loc(b)) for a, b in secciones], faq=[(loc(a), loc(b)) for a, b in faq], kw=kw)
art("codigos-de-error-lavadora-samsung", "lava", "Códigos de error de lavadoras Samsung: 5E, 4E, UE, dE, LE y más",
    "Qué significan los códigos 5E, 4E, UE, dE, LE y 3E en lavadoras Samsung, qué puedes revisar tú con seguridad y cuándo llamar a un técnico en Panamá.",
    "Cuando la lavadora Samsung muestra un código, te está diciendo qué sistema revisar. Esta guía traduce los más comunes y te dice qué puedes comprobar sin riesgo.",
    [("Tabla rápida de códigos", P("El significado exacto puede variar según el modelo; confirma siempre en el manual de tu lavadora.") + TB(["Código", "Qué suele indicar", "Qué revisar primero"], [["5E o SE", "No desagua", "Filtro de la bomba, manguera de desagüe doblada o tapada"], ["4E o 4C", "No entra agua", "Llave de paso abierta, mangueras sin dobleces, filtros de entrada"], ["UE o UB", "Carga desbalanceada", "Redistribuir la ropa; no lavar piezas muy pesadas solas"], ["dE o dC", "Puerta mal cerrada", "Cerrar bien, sin ropa atrapada en el sello"], ["LE o LC", "Fuga o exceso de agua", "Revisar mangueras y piso; desconectar y llamar si hay agua"], ["1E o 1C", "Sensor de nivel de agua", "Suele requerir revisión técnica (presostato)"], ["3E o 3C", "Motor o su control", "Apagar y reiniciar; si vuelve, requiere técnico"]])),
     ("Qué puedes hacer con seguridad", UL(["Apaga la lavadora y desconéctala de la corriente unos minutos antes de volver a probar.", "Revisa que las mangueras no estén dobladas ni aplastadas contra la pared.", "Limpia el filtro de la bomba con la lavadora desconectada y con una toalla debajo, porque sale agua.", "Reparte la ropa y no sobrecargues el tambor."])),
     ("Qué NO debes hacer", UL(["No abras la lavadora ni toques el motor o la tarjeta estando conectada.", "No fuerces la puerta si el seguro no suelta: espera a que se desbloquee.", "No ignores una fuga: puede dañar el piso y causar un riesgo eléctrico."])),
     ("Cuándo llamar a un técnico", P("Si el código vuelve después de revisar lo anterior, si ves agua fuera de la lavadora, si huele a quemado o si salta el breaker, deja de usarla y pide una visita. Dinos el modelo, el código y desde cuándo ocurre."))],
    [("¿Cómo borro un código de error?", "Muchas veces desaparece al apagar y desconectar la lavadora unos minutos. Si regresa, la causa sigue ahí y conviene revisarla."), ("¿El código 5E siempre es la bomba?", "No. Primero suele ser el filtro o la manguera de desagüe obstruidos; la bomba es una posibilidad cuando eso está limpio."), ("¿Cuánto cuesta reparar un código de error?", "Depende de la causa y del repuesto. El valor se confirma después del diagnóstico y antes de reparar.")])
art("refrigeradora-samsung-con-escarcha-causas", "refri", "Refrigeradora Samsung con escarcha: causas y qué revisar",
    "Por qué se forma escarcha en una refrigeradora Samsung No Frost: sello de puerta, deshielo, sensores y ventilador. Qué revisar y cuándo llamar a un técnico.",
    "En una refrigeradora No Frost la escarcha no debería acumularse. Si aparece, algo en el sistema de aire o de deshielo no está funcionando como debe.",
    [("Por qué no debería haber escarcha", P("Las refrigeradoras No Frost enfrían con un evaporador y un ventilador que reparten el aire frío. Cada cierto tiempo un ciclo de deshielo derrite la escarcha del evaporador. Si ese ciclo falla, el hielo se acumula y bloquea el paso del aire.")),
     ("Causas más frecuentes", UL(["<b>Sello de la puerta dañado o sucio:</b> entra aire húmedo y se congela. En Panamá la humedad lo agrava.", "<b>Puerta mal cerrada</b> por alimentos que sobresalen o por una puerta desnivelada.", "<b>Falla del sistema de deshielo:</b> resistencia, sensor de temperatura o su control.", "<b>Ventilador del evaporador</b> que no gira bien: el aire no circula y se forma hielo.", "<b>Ventilación bloqueada</b> por comida pegada a las salidas de aire."])),
     ("Qué puedes revisar tú", OL(["Comprueba que la puerta cierre bien y que el sello no tenga grietas ni suciedad.", "No tapes las rejillas de aire con alimentos.", "Evita abrir la puerta por periodos largos y no guardes comida caliente.", "Si hay mucho hielo, desconecta la refrigeradora y déjala descongelar bien, con toallas para el agua."])),
     ("Lo que no conviene hacer", UL(["No uses cuchillos, picahielos ni secadores de pelo cerca del evaporador.", "No dejes la refrigeradora desenchufada con comida adentro sin plan para conservarla."])),
     ("Cuándo llamar a un técnico", P("Si la escarcha regresa después de descongelar, el problema probablemente está en el deshielo, el sensor o el ventilador, y requiere medición con instrumentos. Un diagnóstico a tiempo evita que se dañe la comida y que el compresor trabaje de más."))],
    [("¿La escarcha en el congelador es normal?", "Una capa fina en las paredes puede aparecer, pero en un equipo No Frost no debería formarse hielo grueso ni cubrir las rejillas."), ("¿Descongelar la soluciona?", "Solo temporalmente si la causa no se corrige: el hielo vuelve."), ("¿Puede dañar el compresor?", "Un evaporador bloqueado hace que el equipo trabaje más y enfríe peor. Conviene revisarlo pronto.")])
art("modelo-samsung-donde-esta-y-que-significa", "decide", "Dónde está el modelo de tu electrodoméstico Samsung y qué significa",
    "Dónde encontrar la etiqueta con el modelo de tu refrigeradora, lavadora, secadora o microondas Samsung, y qué indican las letras iniciales (RS, RT, WA, WW, DV).",
    "Con el modelo exacto, el técnico sabe qué repuesto y qué procedimiento corresponde. Encontrarlo toma un minuto.",
    [("Dónde buscar la etiqueta", TB(["Equipo", "Dónde suele estar la etiqueta"], [["Refrigeradora", "Dentro del refrigerador, en una pared lateral o cerca del techo; a veces en la parte trasera"], ["Lavadora", "Marco de la puerta, parte trasera o bajo la tapa"], ["Secadora", "Marco de la puerta o detrás de la puerta"], ["Lavavajillas", "Borde interior de la puerta o lateral"], ["Microondas", "Parte trasera o dentro, junto a la puerta"], ["Estufa u horno", "Marco del horno o interior del cajón inferior"]])),
     ("Qué indican las letras del inicio", P("Como orientación general, Samsung usa letras iniciales por tipo de equipo. Confirma siempre con el manual.") + TB(["Inicio del modelo", "Suele corresponder a"], [["RS", "Refrigeradora Side by Side"], ["RT", "Refrigeradora con congelador arriba"], ["RB", "Refrigeradora con congelador abajo"], ["RF", "Refrigeradora French Door"], ["WA", "Lavadora de carga superior"], ["WW o WF", "Lavadora de carga frontal"], ["DV", "Secadora"], ["DW", "Lavavajillas"], ["MS o ME", "Microondas"]])),
     ("Qué anotar y qué fotografiar", UL(["El modelo completo, con todas las letras y números.", "El número de serie si aparece.", "Una foto nítida de la etiqueta, sin reflejos.", "El código de error, si el equipo lo muestra."])),
     ("Por qué ayuda tanto", P("Equipos que parecen iguales pueden usar repuestos distintos. Con el modelo se confirma si una pieza es compatible antes de hacer la visita, y se evita perder tiempo."))],
    [("¿El modelo y el número de serie son lo mismo?", "No. El modelo identifica el tipo de equipo; el número de serie identifica tu unidad."), ("¿Y si la etiqueta se borró?", "Envía una foto del equipo completo y de las piezas, y confirmamos el modelo en la visita."), ("¿Puedo enviar la foto por WhatsApp?", "Sí, es la forma más rápida de preparar la visita.")])
art("voltaje-y-proteccion-refrigeradora-panama", "clima", "Voltaje en Panamá: cómo proteger tu refrigeradora y tu lavadora",
    "Qué hacer ante bajones y picos de voltaje en Panamá para proteger refrigeradoras y lavadoras Samsung: protectores, tomas, tormentas y cortes de luz.",
    "En Panamá la red eléctrica es de 110-120 V a 60 Hz. Las variaciones, los picos y los cortes pueden dañar tarjetas y compresores.",
    [("Qué daña a los electrodomésticos", UL(["Picos de voltaje por tormentas o maniobras en la red.", "Bajones que hacen trabajar de más al compresor.", "Regresos bruscos de la corriente después de un corte.", "Tomas flojas, extensiones largas o regletas sobrecargadas."])),
     ("Cómo protegerlos", UL(["Usa un protector de voltaje con retardo para la refrigeradora, que espera unos minutos antes de reconectar.", "Conecta el equipo directo a una toma firme y con tierra, sin multitomas sobrecargadas.", "Durante tormentas eléctricas fuertes, desconecta los equipos que no necesites.", "Después de un corte, espera unos minutos antes de que el compresor vuelva a arrancar."])),
     ("Señales de que hubo un daño eléctrico", UL(["El equipo no enciende después de una tormenta o un corte.", "El panel muestra códigos o se reinicia solo.", "Huele a quemado o salta el breaker.", "El compresor hace clic y se apaga."])),
     ("Cuándo pedir una revisión", P("Si notas cualquiera de esas señales, desconecta el equipo y pide una visita. Con la tarjeta electrónica y el compresor, una revisión temprana evita daños mayores."))],
    [("¿Necesito un protector para cada electrodoméstico?", "Es especialmente recomendable para la refrigeradora y la lavadora con tarjeta electrónica. Elige uno con la capacidad que indica la etiqueta del equipo."), ("¿Un regulador es igual que un protector?", "No. Un protector corta la energía ante un problema; un regulador estabiliza el voltaje. Cada uno sirve para un caso distinto."), ("¿La garantía cubre los daños por voltaje?", "Suele excluirlos. Revisa las condiciones en el manual de tu equipo.")])
art("humedad-y-salitre-en-electrodomesticos-panama", "clima", "Humedad y salitre en Panamá: cómo afectan a tus electrodomésticos",
    "Cómo el clima tropical, la lluvia y el salitre de zonas costeras de Panamá dañan contactos, sellos y tarjetas, y qué hábitos alargan la vida de tus equipos.",
    "El clima tropical de Panamá, con humedad alta y meses de lluvia de mayo a diciembre, exige cuidados distintos a los de otros lugares.",
    [("Qué pasa con la humedad", UL(["Se forma condensación en sellos y contactos.", "Los sellos de las puertas se ensucian y pierden ajuste.", "Las tarjetas electrónicas pueden oxidarse con el tiempo.", "Aparece moho en tambores, gomas y filtros."])),
     ("Zonas costeras y salitre", P("En barrios cercanos al mar, como Costa del Este, Punta Pacífica o Paitilla, el salitre acelera la corrosión de contactos y partes metálicas. Conviene limpiar y revisar con más frecuencia.")),
     ("Hábitos que ayudan", UL(["Deja espacio detrás y a los lados de la refrigeradora para que respire.", "Limpia los sellos de las puertas con un paño húmedo y sécalos.", "Deja la puerta o la tapa de la lavadora abiertas al terminar para que se seque.", "Usa deshumidificación o ventilación donde estén las secadoras y lavadoras."])),
     ("Mantenimiento preventivo", P("Una revisión anual permite limpiar contactos, comprobar sellos y detectar piezas gastadas antes de que fallen. En el clima de Panamá suele ser más útil que en otros lugares."))],
    [("¿Cada cuánto debo limpiar los sellos?", "Una vez al mes alcanza para la mayoría de los hogares; más seguido si hay mucha humedad."), ("¿La humedad daña la garantía?", "Los daños por humedad o corrosión suelen quedar fuera de la garantía. Revisa el manual."), ("¿Sirve cubrir los equipos?", "No los tapes con plástico: atrapa humedad. Mejor mantenerlos secos y ventilados.")])
art("como-se-cobra-una-reparacion-de-electrodomesticos", "decide", "Cómo se cobra una reparación de electrodomésticos y qué pedir por escrito",
    "De qué se compone el costo de una reparación de línea blanca (visita, repuesto, mano de obra), qué debe quedar acordado antes y cómo evitar sorpresas.",
    "El valor de una reparación no es un número fijo: depende de varios factores. Saber cuáles son te ayuda a comparar y a evitar sorpresas.",
    [("De qué se compone el costo", UL(["<b>Visita o diagnóstico:</b> el trabajo de revisar el equipo y encontrar la falla.", "<b>Repuesto:</b> depende del modelo y de su disponibilidad.", "<b>Mano de obra:</b> el tiempo y la dificultad de la reparación.", "<b>Traslado:</b> según el barrio, en algunos casos."])),
     ("Qué debe quedar claro antes de empezar", UL(["El valor del diagnóstico y si se descuenta cuando apruebas la reparación.", "El valor de la reparación completa, con repuesto y mano de obra.", "El tiempo estimado y si hay que esperar un repuesto.", "La garantía del trabajo y de la pieza, por escrito."])),
     ("Señales de alerta", UL(["Cambian piezas sin explicarte por qué.", "No quieren dar el valor antes de empezar.", "Piden pagar todo por adelantado sin comprobante.", "No te dejan ver la pieza dañada."])),
     ("Cómo trabajamos nosotros", P("Primero se diagnostica, luego se te explica la falla y se te confirma el valor antes de reparar. No se cambia ninguna pieza sin tu aprobación."))],
    [("¿Por qué no hay una tarifa fija?", "Porque dos equipos con la misma falla aparente pueden necesitar repuestos y tiempos distintos."), ("¿Conviene pedir otra opinión?", "Sí, si el valor te parece alto. Pide también el diagnóstico por escrito."), ("¿Puedo pedir factura o comprobante?", "Sí, y conviene guardarlo para la garantía del trabajo.")])
art("garantia-de-fabrica-o-tecnico-independiente", "decide", "Garantía de fábrica o técnico independiente: qué conviene según tu caso",
    "Cuándo conviene usar la garantía de fábrica de tu Samsung y cuándo un técnico independiente, qué papeles guardar y cómo no perder tu garantía.",
    "Esta es una de las dudas más comunes: ¿llamo al servicio de fábrica o a un técnico independiente? Depende de si tu equipo sigue en garantía.",
    [("Si tu equipo está en garantía", UL(["Revisa el manual y la factura: cuánto dura y qué cubre.", "Antes de que alguien lo abra, consulta con Samsung o con la tienda donde lo compraste.", "Intervenciones de terceros pueden afectar la garantía de fábrica."])),
     ("Si ya salió de garantía", P("Un técnico independiente puede ser una buena opción: suele coordinar más rápido y a domicilio. Pide siempre el valor antes de empezar y una garantía por escrito del trabajo.")),
     ("Qué papeles guardar", UL(["Factura de compra del equipo.", "Manual y tarjeta de garantía.", "Comprobante de cada reparación, con fecha y descripción.", "Fotos de la etiqueta del modelo."])),
     ("Cómo decidir", TB(["Situación", "Qué conviene"], [["Equipo con menos de un año", "Consultar primero la garantía de fábrica"], ["Garantía vencida", "Técnico independiente con valor confirmado antes"], ["Falla por golpe, líquido o voltaje", "Suele estar excluida de la garantía; pedir diagnóstico"], ["Duda sobre si está cubierto", "Preguntar a Samsung o a la tienda por escrito"]]))],
    [("¿Un técnico independiente puede reparar mi equipo en garantía?", "Puede, pero si lo hace sin autorización de fábrica, la garantía podría perderse. Consulta antes."), ("¿Dónde veo cuánto dura mi garantía?", "En la tarjeta de garantía, la factura o el manual del equipo."), ("¿Qué garantía da el técnico independiente?", "La del trabajo y las piezas que instala, que debe quedar por escrito.")])
art("lavadora-samsung-huele-mal-como-limpiarla", "lava", "Lavadora Samsung con mal olor: causas y cómo limpiarla",
    "Por qué huele mal una lavadora Samsung, dónde se acumula el moho (sello, gaveta, filtro, tambor) y cómo limpiarla y prevenirlo en el clima de Panamá.",
    "El mal olor casi siempre viene de moho y residuos de detergente atrapados en sitios húmedos. Se puede corregir y prevenir.",
    [("De dónde viene el olor", UL(["El sello de goma de la puerta, donde queda agua.", "La gaveta del detergente, con residuos.", "El filtro de la bomba, con pelusa y agua estancada.", "El tambor y la tina, por el uso de agua fría o demasiado detergente."])),
     ("Cómo limpiarla paso a paso", OL(["Limpia el sello de goma con un paño y un limpiador suave; no olvides los pliegues.", "Saca la gaveta, límpiala y enjuágala.", "Limpia el filtro de la bomba con la lavadora desconectada.", "Corre un ciclo de limpieza de la tina si tu modelo lo trae, o usa un limpiador especial para lavadoras.", "Deja la puerta abierta al terminar para que seque."])),
     ("Cómo prevenirlo", UL(["Usa la cantidad de detergente recomendada; el exceso deja residuo.", "Evita dejar ropa mojada dentro por horas.", "Limpia el sello y el filtro cada mes o dos, según el uso."])),
     ("Cuándo llamar a un técnico", P("Si el olor persiste tras la limpieza, si huele a quemado o si hay agua que no desagua del todo, puede haber una falla de bomba o manguera que requiere revisión."))],
    [("¿Puedo usar cloro?", "Revisa el manual: algunos fabricantes no lo recomiendan. Prefiere limpiadores diseñados para lavadoras."), ("¿Por qué huele aunque lave con agua caliente?", "Por el moho acumulado en el sello o el filtro. Hay que limpiar esos puntos."), ("¿Cada cuánto debo limpiar el filtro?", "Cada uno o dos meses, o antes si lavas mucha ropa con pelusa.")])
art("lavavajillas-samsung-mantenimiento-y-fallas", "cocina", "Lavavajillas Samsung: mantenimiento, olores y fallas comunes",
    "Cómo mantener un lavavajillas Samsung: filtro, brazos rociadores, desagüe y carga correcta. Fallas comunes y cuándo llamar a un técnico en Panamá.",
    "Un lavavajillas bien cuidado lava mejor y dura más. Casi todos los problemas empiezan en el filtro, los rociadores o el desagüe.",
    [("Mantenimiento básico", UL(["Limpia el filtro del fondo cada pocas semanas.", "Revisa que los orificios de los brazos rociadores no estén tapados.", "Limpia el sello de la puerta.", "Corre un ciclo de limpieza o con un limpiador específico de vez en cuando."])),
     ("Fallas comunes", TB(["Síntoma", "Causa frecuente"], [["Deja residuos en la vajilla", "Filtro o rociadores tapados, carga mal acomodada"], ["No desagua", "Filtro o manguera de desagüe obstruidos"], ["Huele mal", "Restos de comida y humedad en filtro y sello"], ["No seca bien", "Falta de abrillantador o resistencia con falla"], ["Gotea por la puerta", "Sello dañado o puerta mal alineada"]])),
     ("Cómo cargarlo bien", UL(["No tapes los rociadores con platos grandes.", "Quita los restos grandes de comida antes.", "Carga con las superficies sucias hacia el centro."])),
     ("Cuándo llamar a un técnico", P("Si no desagua después de limpiar el filtro, si se filtra agua por abajo o si el panel muestra un error que no desaparece, pide una visita."))],
    [("¿Debo prelavar la vajilla?", "Solo quitar los restos grandes; el lavavajillas necesita algo de suciedad para que los detergentes actúen bien."), ("¿Por qué queda blanco el vidrio?", "Puede ser agua dura o exceso de detergente; revisa las indicaciones del manual."), ("¿Cada cuánto limpio el filtro?", "Cada dos a cuatro semanas, según el uso.")])
art("estufa-y-horno-olor-a-gas-seguridad", "cocina", "Estufa y horno: qué hacer si hueles gas y cuándo llamar a un técnico",
    "Pasos de seguridad si sientes olor a gas en tu estufa u horno, señales de que un quemador necesita revisión y por qué no debes manipular el gas tú mismo.",
    "El gas exige respeto. Esta guía resume qué hacer ante un olor a gas y qué fallas de estufas y hornos sí requieren a un técnico.",
    [("Si hueles gas", OL(["Cierra la llave de paso o del cilindro.", "Abre puertas y ventanas para ventilar.", "No enciendas luces, interruptores, llamas ni celulares cerca.", "Sal del lugar y pide ayuda desde afuera.", "No vuelvas a usar la estufa hasta que alguien la revise."])),
     ("Señales de que hay que revisar el equipo", UL(["Un quemador no enciende o enciende con dificultad.", "La llama es amarilla o irregular, en lugar de azul.", "La chispa no deja de sonar.", "Perillas flojas o que no cierran del todo.", "El horno no calienta o no mantiene la temperatura."])),
     ("Qué puedes hacer tú", UL(["Limpiar los quemadores cuando están fríos y secarlos bien.", "Revisar que la manguera del gas no esté vencida, doblada o rozando partes calientes.", "Mantener la cocina ventilada."])),
     ("Qué no debes hacer", P("No desarmes válvulas ni conexiones de gas ni uses sustancias para detectar fugas que no sean las indicadas. Esa parte la revisa un técnico."))],
    [("¿La llama amarilla es peligrosa?", "Puede indicar mala mezcla de aire o quemador sucio. Conviene limpiarlo y, si sigue, que lo revise un técnico."), ("¿Cada cuánto cambio la manguera del gas?", "Revisa la fecha impresa y cámbiala cuando esté vencida o con grietas."), ("¿El horno eléctrico también necesita revisión?", "Si no calienta o no mantiene la temperatura, suele ser resistencia, sensor o termostato.")])
art("microondas-samsung-no-calienta-que-hacer", "cocina", "Microondas Samsung que no calienta: causas y precauciones",
    "Qué puede fallar cuando un microondas Samsung gira pero no calienta, por qué no debes abrirlo y qué señales indican que debes dejar de usarlo.",
    "Un microondas que gira pero no calienta tiene una falla interna, y por seguridad no es un equipo para abrir en casa.",
    [("Causas frecuentes", UL(["Magnetrón, que es la pieza que genera el calor.", "Diodo o transformador de alto voltaje.", "Fusible o termofusible.", "Seguros de la puerta que no detectan el cierre."])),
     ("Por qué no debes abrirlo", P("Aunque esté desconectado, el microondas puede guardar una carga de alto voltaje en su interior. Abrirlo es peligroso, y solo debe hacerlo un técnico con las herramientas y el procedimiento correctos.")),
     ("Qué puedes revisar", UL(["Que la puerta cierre bien.", "Que no haya restos de comida en el sello.", "Que el enchufe y el breaker estén bien.", "Que no uses recipientes de metal."])),
     ("Deja de usarlo si", UL(["Hace chispas dentro.", "Huele a quemado.", "La puerta está golpeada o no cierra.", "Se apaga o salta el breaker al encenderlo."]))],
    [("¿Vale la pena reparar un microondas?", "Depende del modelo y de la falla. El técnico te confirma el valor antes de empezar para que decidas."), ("¿Por qué gira el plato pero no calienta?", "El motor del plato es independiente del sistema de calentamiento."), ("¿Puedo usar un microondas con la puerta algo dañada?", "No. Un sello o una puerta dañada puede ser un riesgo y debe revisarse.")])
art("senales-de-que-tu-refrigeradora-necesita-revision", "refri", "7 señales de que tu refrigeradora Samsung necesita revisión",
    "Ruidos, hielo, agua, olores y consumo: las 7 señales de que tu refrigeradora Samsung necesita un técnico y qué hacer mientras tanto para no perder alimentos.",
    "Una refrigeradora avisa antes de fallar del todo. Conocer las señales te permite actuar a tiempo y salvar los alimentos.",
    [("Las 7 señales", OL(["Enfría poco o de forma despareja: arriba frío y abajo tibio, o al revés.", "Escarcha o hielo en las paredes o en las rejillas.", "Ruidos nuevos: zumbidos fuertes, golpeteos o chirridos.", "Agua debajo o dentro de la refrigeradora.", "El compresor trabaja sin parar o se apaga y enciende muy seguido.", "Olores raros o alimentos que se dañan antes.", "Aumento notable del consumo de luz sin razón."])),
     ("Qué hacer mientras llega el técnico", UL(["No abras la puerta más de lo necesario.", "Pasa los alimentos más delicados a otra nevera o a una hielera.", "Si hay fuga de agua, desconecta el equipo y seca el piso.", "Anota el modelo y desde cuándo ocurre."])),
     ("Cuándo es una urgencia", P("Si la refrigeradora dejó de enfriar por completo, si huele a quemado o si hay agua cerca del enchufe, desconéctala y pide una visita cuanto antes.")),
     ("Cómo evitar que se repita", P("Limpia el condensador, revisa los sellos, deja espacio para que respire y protege el equipo de bajones de voltaje. Una revisión anual ayuda a detectar piezas gastadas."))],
    [("¿Cuánto aguanta la comida sin enfriar?", "Depende del equipo y del calor, pero no conviene arriesgar más de unas pocas horas. Pasa lo delicado a otro lugar."), ("¿Puedo mover la refrigeradora para limpiarla?", "Con cuidado y desconectada. Limpia el condensador y deja espacio para que respire."), ("¿Es normal que haga ruido?", "Un zumbido suave sí. Un ruido nuevo o fuerte conviene revisarlo.")])
# ---- páginas de artículo
def tarjeta_rel(a, p=""):
    return f'<a class="pa-rc" href="{p}{a["slug"]}/"><span class="pa-cat">{esc(CATS[a["cat"]])}</span><b>{esc(a["titulo"])}</b><small>{max(3, round(len(txt(a["intro"] + "".join(c for _, c in a["secciones"])).split()) / 190))} min de lectura</small></a>'
for a in ART.values():
    palabras = len(txt(a["intro"] + "".join(c for _, c in a["secciones"]) + "".join(q + r for q, r in a["faq"])).split()); mins = max(3, round(palabras / 190))
    toc = "".join(f'<li><a href="#s{i}">{esc(t)}</a></li>' for i, (t, _) in enumerate(a["secciones"]))
    cuerpo_a = "".join(f'<h2 id="s{i}">{esc(t)}</h2>{c}' for i, (t, c) in enumerate(a["secciones"]))
    faq = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(r)}</p></details>" for q, r in a["faq"])
    rel = [x for x in ART.values() if x["slug"] != a["slug"] and x["cat"] == a["cat"]][:2] + [x for x in ART.values() if x["slug"] != a["slug"] and x["cat"] != a["cat"]][:3]
    rel = rel[:3]
    ruta = f"blog/{a['slug']}/"
    body = (miga(2, [("Inicio", ""), ("Blog", "blog/"), (a["titulo"], None)])
            + HERO(f"Blog · {CATS[a['cat']]}", a["titulo"], a["desc"], f'<p class="pa-meta">{mins} min de lectura · Actualizado el {FECHA} · Por el equipo técnico de {esc(NOMBRE)}</p>')
            + f'<main class="pa-art"><div class="pa-w pa-cols"><article class="pa-prose"><p class="pa-lead">{esc(a["intro"])}</p><nav class="pa-toc"><b>En este artículo</b><ol>{toc}</ol></nav>{cuerpo_a}<h2 id="faq">Preguntas frecuentes</h2><div class="pa-faq">{faq}</div>'
              f'<div class="pa-cta2"><h3>¿Tu Samsung presenta esta falla?</h3><p>Escríbenos con el modelo y lo que ves: coordinamos la visita en tu barrio.</p><a class="pa-b wa" href="https://wa.me/{WAN}?text={esc("Hola, leí el artículo «" + a["titulo"] + "» y necesito un técnico Samsung").replace(" ", "%20")}" target="_blank" rel="noopener">Escribir por WhatsApp</a></div></article>'
              f'<aside class="pa-aside"><div class="pa-card"><h3>Pide tu visita</h3><p>Diagnóstico primero y valor confirmado antes de reparar.</p><a class="pa-b wa" style="width:100%" href="https://wa.me/{WAN}" target="_blank" rel="noopener">WhatsApp {TEL}</a><p style="margin:12px 0 0;font-size:.85rem;color:#5b6478">Abierto las 24 horas · {esc(DIR)}</p></div>'
              f'<div class="pa-card"><h3>Sigue leyendo</h3>{"".join(tarjeta_rel(x, "../") for x in rel)}</div></aside></div></main>')
    art_ld = {"@type": "Article", "headline": a["titulo"], "description": a["desc"], "inLanguage": "es-PA", "datePublished": HOY, "dateModified": HOY, "wordCount": palabras, "author": ORG, "publisher": ORG, "mainEntityOfPage": f"{DOM}/{ruta}", "image": f"{DOM}/img/tecnico-samsung-saluda-en-la-puerta.webp", "articleSection": CATS[a["cat"]]}
    faq_ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in a["faq"]]}
    d = shell(T2, 2, ruta, loc(TT.get(a["slug"].replace("-" + CORTO.lower(), "-panama"), a["titulo"])), a["desc"], ld_base(ruta, a["titulo"], a["desc"], [("Inicio", ""), ("Blog", "blog/"), (a["titulo"], ruta)]) + [art_ld, faq_ld], body)
    (R / "blog" / a["slug"]).mkdir(parents=True, exist_ok=True); (R / "blog" / a["slug"] / "index.html").write_text(d, encoding="utf-8")
# ---- hub del blog con todos los artículos (los nuevos y los que ya existían)
VIEJOS = {"vida-util": "refri", "cuidado-clima": "clima", "corte-de-luz": "clima", "ahorro-energia": "clima", "errores-lavadora": "lava", "secadora-lluvias": "lava", "mantenimiento-anual": "decide", "mitos": "decide", "elegir-tecnico": "decide", "checklist-visita": "decide"}
todos = []
for s_, c_ in VIEJOS.items():
    f = R / "blog" / s_ / "index.html"
    if f.exists():
        tt = f.read_text(encoding="utf-8"); h1 = txt(re.search(r"<h1[^>]*>(.*?)</h1>", tt, re.S).group(1)); ds = re.search(r'name="description" content="([^"]*)"', tt).group(1)
        todos.append(dict(slug=s_, cat=c_, titulo=h1, desc=html.unescape(ds), mins=max(4, round(len(txt(tt).split()) / 190))))
for a in ART.values():
    todos.append(dict(slug=a["slug"], cat=a["cat"], titulo=a["titulo"], desc=a["desc"], mins=max(3, round(len(txt(a["intro"] + "".join(c for _, c in a["secciones"])).split()) / 190))))
card = lambda x: f'<a class="pa-bc" href="{x["slug"]}/"><span class="pa-cat">{esc(CATS[x["cat"]])}</span><b>{esc(x["titulo"])}</b><p>{esc(x["desc"])}</p><small>{x["mins"]} min de lectura</small></a>'
dest = [t for t in todos if t["slug"] in ("codigos-de-error-lavadora-samsung", "refrigeradora-samsung-con-escarcha-causas", "garantia-de-fabrica-o-tecnico-independiente")]
sec = "".join(f'<h2 class="pa-h2" style="margin-top:34px">{esc(n)}</h2><div class="pa-bg">{"".join(card(t) for t in todos if t["cat"] == k)}</div>' for k, n in CATS.items() if any(t["cat"] == k for t in todos))
hub = (miga(1, [("Inicio", ""), ("Blog", None)]) + HERO("Blog técnico", f"Blog de electrodomésticos Samsung en {CORTO}", f"{len(todos)} guías claras sobre fallas, mantenimiento, voltaje, clima y garantía, escritas por el equipo técnico.")
       + f'<main class="pa-art"><div class="pa-w"><h2 class="pa-h2">Lo más leído</h2><div class="pa-bg">{"".join(card(t) for t in dest)}</div>{sec}</div></main>')
ldh = ld_base("blog/", f"Blog de electrodomésticos Samsung en {CORTO}", f"Guías sobre fallas, mantenimiento, voltaje, clima y garantía de electrodomésticos Samsung en {CORTO}.", [("Inicio", ""), ("Blog", "blog/")]) + [{"@type": "Blog", "name": f"Blog de {NOMBRE}", "url": f"{DOM}/blog/", "inLanguage": "es-PA", "publisher": ORG, "blogPost": [{"@type": "BlogPosting", "headline": t["titulo"], "url": f"{DOM}/blog/{t['slug']}/"} for t in todos]}]
(R / "blog" / "index.html").write_text(shell(T1, 1, "blog/", f"Blog de electrodomésticos Samsung en {CORTO} | Guías y consejos", f"{len(todos)} guías sobre fallas, mantenimiento, voltaje, clima y garantía de {CATS['refri'].lower()}, lavadoras, secadoras y más Samsung en {CORTO}.", ldh, hub.replace('href="', 'href="', 1)), encoding="utf-8")
# ---- sitemap
sm = next((x for x in sorted(R.glob("sitemap-*.xml")) if "imagenes" not in x.name), R / "sitemap.xml")
if sm.exists():
    s = sm.read_text(encoding="utf-8")
    nuevas = ["politica-de-privacidad/", "terminos-y-condiciones/"] + [f"blog/{a['slug']}/" for a in ART.values()]
    add = "".join(f"<url><loc>{DOM}/{u}</loc><lastmod>{HOY}</lastmod><changefreq>monthly</changefreq><priority>{'0.7' if u.startswith('blog') else '0.3'}</priority></url>" for u in nuevas if f"/{u}</loc>" not in s)
    sm.write_text(s.replace("</urlset>", add + "</urlset>"), encoding="utf-8")
print("artículos nuevos:", len(ART), "· blog total:", len(todos), "· legales: 2")
