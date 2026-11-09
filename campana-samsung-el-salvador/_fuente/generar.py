"""Campaña de Google Ads (Búsqueda) para Servicio Técnico Samsung El Salvador. Solo canal WhatsApp (+507 6933 7976).
Las páginas de destino salen del sitio generado (samsung-el-salvador/site). Sin «autorizado», «oficial», «garantía», «original» ni precios."""
import csv, json, re, sys
from pathlib import Path

QUI = Path(__file__).resolve().parent
RAIZ = QUI.parent
WEB = RAIZ.parent / "samsung-el-salvador" / "site"
DOM = "https://serviciotecnicosamsungelsalvador.click"
CAMP = "Samsung El Salvador - Búsqueda"
PROHIBIDAS = re.compile(r"autorizad|oficial|garant[ií]a|original|genuin|compatib|100 ?%|mejor |gratis|\$|\d+ ?usd|barato", re.I)


def url(ruta):
    r = ruta.strip("/")
    assert ((WEB / r / "index.html").exists() if r else (WEB / "index.html").exists()), ruta
    return f"{DOM}/{r}/" if r else f"{DOM}/"


GEN_H = ["Escríbenos por WhatsApp", "Atención por WhatsApp", "Visita a Domicilio", "Costo Antes de Reparar", "Diagnóstico Claro", "Cobertura en El Salvador",
         "Respondemos por WhatsApp", "Pide tu Visita Hoy", "Envía Modelo y Falla", "Técnico a Domicilio", "Samsung El Salvador"]
GEN_D = ["Escríbenos por WhatsApp con el modelo y la falla. Te confirmamos la visita a domicilio.",
         "Atendemos solo por WhatsApp: envía una foto de la etiqueta y un video corto de la falla.",
         "Te explicamos la falla y te damos el costo antes de reparar. Tú decides si continuamos.",
         "Visita a domicilio en San Salvador, La Libertad, occidente y oriente del país."]
G = []


def grupo(nombre, destino, p1, p2, titulos, descripciones, claves, nota=""):
    G.append(dict(nombre=nombre, url=destino, path1=p1, path2=p2, titulos=titulos, descripciones=descripciones, claves=claves, nota=nota))


def tit(esp):
    return list(dict.fromkeys(esp + GEN_H))[:15]


# ---------- grupos por equipo y por intención
grupo("Servicio técnico Samsung", url(""), "Samsung", "ServicioTecnico",
      tit(["Servicio Técnico Samsung", "Servicio Técnico Samsung SV", "Técnico Samsung a Domicilio", "Reparación Samsung El Salvador", "Samsung: Reparación en Casa", "Reparamos Equipos Samsung", "Servicio Samsung a Domicilio"]),
      ["Servicio técnico Samsung en El Salvador: lavadoras, secadoras, neveras y refrigeradoras.", GEN_D[0], GEN_D[1], GEN_D[2]],
      ["servicio tecnico samsung el salvador", "servicio técnico samsung el salvador", "servicio tecnico samsung san salvador", "tecnico samsung el salvador", "tecnico samsung a domicilio el salvador",
       "reparacion samsung el salvador", "reparación de electrodomésticos samsung el salvador", "samsung servicio tecnico el salvador", "soporte tecnico samsung el salvador", "tecnico de electrodomesticos samsung",
       "servicio tecnico samsung a domicilio", "servicio samsung el salvador", "samsung service el salvador", "reparar electrodomesticos samsung el salvador"])
grupo("Centro de servicio Samsung", url("centro-de-servicio-samsung-el-salvador"), "Samsung", "CentroServicio",
      tit(["Centro de Servicio Samsung", "Centro de Servicio El Salvador", "Servicio Samsung sin Salir", "Samsung a Domicilio", "Técnico en Tu Casa", "Sin Llevar tu Equipo", "Centro de Servicio a Domicilio"]),
      ["¿Buscas centro de servicio Samsung? El técnico va a tu casa. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["centro de servicio samsung el salvador", "centro de servicio samsung san salvador", "centro de servicio samsung", "centro servicio samsung el salvador", "donde reparar electrodomesticos samsung el salvador",
       "taller samsung el salvador", "taller de electrodomesticos samsung", "samsung centro de servicio san salvador", "dónde reparan samsung en el salvador"])
grupo("Lavadoras Samsung", url("reparacion-de-lavadoras-samsung-el-salvador"), "Lavadoras", "Samsung",
      tit(["Reparación Lavadora Samsung", "Técnico Lavadoras Samsung", "Lavadora Samsung con Falla", "Arreglo de Lavadora Samsung", "Servicio Lavadora Samsung", "Lavadora Samsung a Domicilio", "Lavadora Samsung No Funciona"]),
      ["Reparación de lavadoras Samsung a domicilio en El Salvador. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["reparacion de lavadoras samsung el salvador", "reparacion lavadora samsung el salvador", "tecnico lavadoras samsung el salvador", "servicio tecnico lavadoras samsung el salvador", "arreglo de lavadora samsung",
       "reparar lavadora samsung", "reparacion lavadora samsung", "tecnico de lavadoras samsung", "lavadora samsung no funciona el salvador", "servicio tecnico lavadora samsung a domicilio", "mantenimiento lavadora samsung el salvador"])
grupo("Secadoras Samsung", url("reparacion-de-secadoras-samsung-el-salvador"), "Secadoras", "Samsung",
      tit(["Reparación Secadora Samsung", "Técnico Secadoras Samsung", "Secadora Samsung No Seca", "Secadora Samsung No Calienta", "Arreglo de Secadora Samsung", "Servicio Secadora Samsung", "Secadora Samsung a Domicilio"]),
      ["Reparación de secadoras Samsung a domicilio en El Salvador. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["reparacion de secadoras samsung el salvador", "reparacion secadora samsung el salvador", "tecnico secadoras samsung el salvador", "servicio tecnico secadoras samsung", "secadora samsung no seca",
       "secadora samsung no calienta", "reparar secadora samsung", "arreglo de secadora samsung", "mantenimiento secadora samsung el salvador", "secadora samsung no enciende"])
grupo("Neveras Samsung", url("reparacion-de-neveras-samsung-el-salvador"), "Neveras", "Samsung",
      tit(["Reparación Nevera Samsung", "Técnico Neveras Samsung", "Nevera Samsung No Enfría", "Arreglo de Nevera Samsung", "Servicio Nevera Samsung", "Nevera Samsung a Domicilio", "Nevera Samsung con Falla"]),
      ["Reparación de neveras Samsung a domicilio en El Salvador. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["reparacion de neveras samsung el salvador", "reparacion nevera samsung el salvador", "tecnico neveras samsung el salvador", "servicio tecnico neveras samsung", "nevera samsung no enfria",
       "reparar nevera samsung", "arreglo de nevera samsung", "nevera samsung hace ruido", "nevera samsung no congela", "nevera samsung gotea agua", "mantenimiento nevera samsung el salvador"])
grupo("Refrigeradoras Samsung", url("reparacion-de-refrigeradoras-samsung-el-salvador"), "Refrigeradoras", "Samsung",
      tit(["Reparar Refrigeradora Samsung", "Técnico Refrigeradoras Samsung", "Refrigeradora Samsung Falla", "Arreglo de Refrigeradora", "Servicio Refrigeradora Samsung", "Refrigeradora a Domicilio", "Refrigeradora con Falla"]),
      ["Reparación de refrigeradoras Samsung a domicilio en El Salvador. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["reparacion de refrigeradoras samsung el salvador", "reparacion refrigeradora samsung el salvador", "tecnico refrigeradoras samsung el salvador", "servicio tecnico refrigeradoras samsung", "refrigeradora samsung no enfria",
       "reparar refrigeradora samsung", "arreglo de refrigeradora samsung", "refrigeradora samsung hace ruido", "refrigeradora samsung no congela", "refrigeradora samsung gotea agua", "refrigeradora samsung escarcha",
       "mantenimiento refrigeradora samsung el salvador"])
grupo("Fallas de refrigeración", url("refrigeradora-samsung-no-enfria-el-salvador"), "Refrigeradora", "NoEnfria",
      tit(["Refrigeradora No Enfría", "Nevera No Enfría Samsung", "Samsung No Enfría", "¿No Enfría tu Nevera?", "Falla de Frío Samsung", "Revisamos tu Refrigeradora", "Nevera Samsung Falla de Frío"]),
      ["¿Tu refrigeradora Samsung no enfría? Escríbenos por WhatsApp y coordinamos la visita.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["refrigeradora samsung no enfria el salvador", "nevera samsung no enfria el salvador", "refrigeradora no enfria samsung", "nevera no enfria samsung", "por que mi refrigeradora samsung no enfria",
       "refrigeradora samsung no enfria abajo", "nevera samsung no enfria pero congela", "refrigeradora samsung se apaga sola"])
grupo("Fallas de lavadora", url("lavadora-samsung-no-desagua-el-salvador"), "Lavadora", "NoDesagua",
      tit(["Lavadora No Desagua", "Lavadora Samsung No Desagua", "Lavadora No Centrifuga", "Lavadora Samsung Falla", "¿Tu Lavadora No Desagua?", "Revisamos tu Lavadora", "Lavadora Samsung No Centrifuga"]),
      ["¿Tu lavadora Samsung no desagua o no centrifuga? Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["lavadora samsung no desagua el salvador", "lavadora samsung no desagua", "lavadora samsung no centrifuga", "lavadora samsung no centrifuga el salvador", "lavadora samsung no llena de agua",
       "lavadora samsung gotea agua", "lavadora samsung no enciende", "lavadora samsung hace ruido", "lavadora samsung vibra mucho"])
grupo("Códigos de error lavadora", url("lavadora-samsung-codigos-de-error-el-salvador"), "Lavadora", "CodigosError",
      tit(["Código 5E Lavadora Samsung", "Código 4E Lavadora Samsung", "Códigos Error Samsung", "Lavadora Samsung Error", "Error 5E Samsung", "Error UE Lavadora Samsung", "Código de Error Lavadora"]),
      ["Tu lavadora Samsung muestra un código de error. Escríbenos por WhatsApp con el código.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["codigo 5e lavadora samsung", "codigo 4e lavadora samsung", "error 5e lavadora samsung", "error 4e lavadora samsung", "codigo ue lavadora samsung", "lavadora samsung codigo de error",
       "lavadora samsung muestra error", "codigos de error lavadora samsung", "error se lavadora samsung", "lavadora samsung codigo he", "lavadora samsung codigo le"])
grupo("San Salvador", url("servicio-tecnico-samsung-gran-san-salvador"), "SanSalvador", "Samsung",
      tit(["Técnico Samsung San Salvador", "Servicio Samsung San Salvador", "Samsung en San Salvador", "Reparación en San Salvador", "Técnico Samsung Soyapango", "Técnico Samsung Mejicanos", "Samsung Colonia Escalón"]),
      ["Servicio técnico Samsung en San Salvador y alrededores. Escríbenos por WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["servicio tecnico samsung san salvador", "tecnico samsung san salvador", "reparacion samsung san salvador", "tecnico samsung soyapango", "tecnico samsung mejicanos", "servicio tecnico samsung apopa",
       "servicio tecnico samsung escalon", "reparacion lavadora samsung san salvador", "reparacion refrigeradora samsung san salvador", "tecnico samsung ilopango"])
grupo("Santa Tecla y La Libertad", url("servicio-tecnico-samsung-la-libertad"), "LaLibertad", "Samsung",
      tit(["Técnico Samsung Santa Tecla", "Servicio Samsung Santa Tecla", "Samsung La Libertad", "Técnico Antiguo Cuscatlán", "Reparación Samsung Merliot", "Samsung en Santa Tecla", "Servicio Samsung La Libertad"]),
      ["Servicio técnico Samsung en Santa Tecla, Antiguo Cuscatlán y La Libertad. WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["servicio tecnico samsung santa tecla", "tecnico samsung santa tecla", "reparacion samsung santa tecla", "servicio tecnico samsung antiguo cuscatlan", "tecnico samsung merliot", "tecnico samsung la libertad",
       "reparacion lavadora samsung santa tecla", "reparacion refrigeradora samsung santa tecla", "tecnico samsung colon", "tecnico samsung ciudad arce"])
grupo("Santa Ana y occidente", url("servicio-tecnico-samsung-occidente"), "Occidente", "Samsung",
      tit(["Técnico Samsung Santa Ana", "Servicio Samsung Santa Ana", "Samsung en Santa Ana", "Técnico Samsung Sonsonate", "Samsung Occidente", "Reparación en Santa Ana", "Servicio Samsung Ahuachapán"]),
      ["Servicio técnico Samsung en Santa Ana, Sonsonate y el occidente del país. WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["servicio tecnico samsung santa ana", "tecnico samsung santa ana", "reparacion samsung santa ana", "tecnico samsung sonsonate", "servicio tecnico samsung sonsonate", "tecnico samsung ahuachapan",
       "tecnico samsung chalchuapa", "reparacion lavadora samsung santa ana", "reparacion refrigeradora samsung santa ana", "tecnico samsung occidente el salvador"])
grupo("San Miguel y oriente", url("servicio-tecnico-samsung-san-miguel"), "Oriente", "Samsung",
      tit(["Técnico Samsung San Miguel", "Servicio Samsung San Miguel", "Samsung en San Miguel", "Técnico Samsung Usulután", "Samsung Oriente", "Reparación en San Miguel", "Servicio Samsung La Unión"]),
      ["Servicio técnico Samsung en San Miguel, Usulután y el oriente del país. WhatsApp.", GEN_D[0], GEN_D[2], GEN_D[1]],
      ["servicio tecnico samsung san miguel", "tecnico samsung san miguel", "reparacion samsung san miguel", "tecnico samsung usulutan", "tecnico samsung la union", "tecnico samsung santa rosa de lima",
       "reparacion lavadora samsung san miguel", "reparacion refrigeradora samsung san miguel", "tecnico samsung oriente el salvador", "tecnico samsung san vicente"])

NEGATIVAS = ["usado", "usada", "segunda mano", "casero", "casera", "manual", "pdf", "descargar", "video", "youtube", "curso", "empleo", "trabajo", "vacante", "gratis", "tutorial",
             "celular", "telefono", "teléfono", "smartphone", "galaxy", "tablet", "televisor", "television", "tv", "pantalla", "monitor", "laptop", "computadora", "impresora", "audifonos", "reloj", "smartwatch",
             "aire acondicionado", "microondas", "lavavajillas", "cocina", "horno", "aspiradora", "plancha",
             "comprar", "tienda", "precio de lavadora", "precio de refrigeradora", "lavadora nueva", "refrigeradora nueva", "oferta", "ofertas", "catalogo", "catálogo", "cuotas", "credito", "crédito",
             "mercadolibre", "amazon", "alibaba", "aliexpress", "temu", "olx", "facebook", "tiktok",
             "mexico", "méxico", "colombia", "ecuador", "panama", "panamá", "costa rica", "guatemala", "honduras", "nicaragua", "peru", "perú", "chile", "argentina", "españa", "venezuela", "bolivia", "republica dominicana", "estados unidos", "usa",
             "mabe", "lg", "whirlpool", "frigidaire", "electrolux", "daewoo", "indurama", "midea", "haceb", "general electric",
             "repuestos", "pieza", "piezas", "tarjeta", "placa", "motor suelto"]
SITELINKS = [("Lavadoras Samsung", "Reparación a domicilio", "Escríbenos por WhatsApp", url("reparacion-de-lavadoras-samsung-el-salvador")),
             ("Refrigeradoras Samsung", "Reparación a domicilio", "Escríbenos por WhatsApp", url("reparacion-de-refrigeradoras-samsung-el-salvador")),
             ("Neveras Samsung", "Reparación a domicilio", "Escríbenos por WhatsApp", url("reparacion-de-neveras-samsung-el-salvador")),
             ("Secadoras Samsung", "Reparación a domicilio", "Escríbenos por WhatsApp", url("reparacion-de-secadoras-samsung-el-salvador")),
             ("Centro de servicio", "Técnico a domicilio", "Sin llevar tu equipo", url("centro-de-servicio-samsung-el-salvador")),
             ("Cobertura", "San Salvador y todo el país", "Elige tu zona", url("zonas-de-servicio-el-salvador")),
             ("Nevera no enfría", "Causas y qué revisar", "Guía paso a paso", url("refrigeradora-samsung-no-enfria-el-salvador")),
             ("Lavadora no desagua", "Causas y qué revisar", "Guía paso a paso", url("lavadora-samsung-no-desagua-el-salvador")),
             ("Códigos de error", "Lavadoras Samsung", "5E, 4E, UE y más", url("lavadora-samsung-codigos-de-error-el-salvador")),
             ("Cómo trabajamos", "Pide tu visita por WhatsApp", "Costo antes de reparar", url("como-trabajamos"))]
CALLOUTS = ["Atención por WhatsApp", "Visita a Domicilio", "Costo Antes de Reparar", "Diagnóstico Claro", "Cobertura Nacional", "Lavadoras y Neveras", "Secadoras, Refrigeradoras", "Respuesta por WhatsApp"]
SNIPPET = ("Tipos", ["Lavadoras", "Secadoras", "Neveras", "Refrigeradoras"])

err = []
for g in G:
    t, d = list(dict.fromkeys(g["titulos"]))[:15], g["descripciones"]; g["titulos"] = t
    if len(t) < 12: err.append(f"{g['nombre']}: solo {len(t)} títulos")
    for x in t:
        if len(x) > 30: err.append(f"{g['nombre']}: título largo ({len(x)}): {x}")
        if PROHIBIDAS.search(x): err.append(f"título prohibido: {x}")
    for x in d:
        if len(x) > 90: err.append(f"{g['nombre']}: descripción larga ({len(x)}): {x}")
        if PROHIBIDAS.search(x): err.append(f"descripción prohibida: {x}")
    g["claves"] = list(dict.fromkeys(g["claves"]))
    for k in g["claves"]:
        if PROHIBIDAS.search(k): err.append(f"clave prohibida: {k}")
    for p1 in (g["path1"], g["path2"]):
        if len(p1) > 15: err.append(f"ruta larga: {p1}")
for x in CALLOUTS:
    if len(x) > 25 or PROHIBIDAS.search(x): err.append(f"destacado: {x}")
for s in SITELINKS:
    if len(s[0]) > 25 or len(s[1]) > 35 or len(s[2]) > 35 or PROHIBIDAS.search(" ".join(s[:3])): err.append(f"sitelink: {s}")
if err:
    print("\n".join(err)); sys.exit(1)

out = RAIZ / "05-archivos-para-importar"; out.mkdir(exist_ok=True)
with open(out / "anuncios.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Campaign", "Ad group", "Ad type", "Final URL", "Path 1", "Path 2"] + [f"Headline {i}" for i in range(1, 16)] + [f"Description {i}" for i in range(1, 5)])
    for g in G:
        w.writerow([CAMP, g["nombre"], "Responsive search ad", g["url"], g["path1"], g["path2"]] + g["titulos"] + [""] * (15 - len(g["titulos"])) + g["descripciones"] + [""] * (4 - len(g["descripciones"])))
with open(out / "palabras-clave.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Ad group", "Keyword", "Criterion Type"])
    for g in G:
        for k in g["claves"]:
            w.writerow([CAMP, g["nombre"], k, "Phrase"]); w.writerow([CAMP, g["nombre"], k, "Exact"])
with open(out / "palabras-negativas.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Keyword", "Criterion Type"])
    for k in NEGATIVAS: w.writerow([CAMP, k, "Campaign negative phrase"])
with open(out / "enlaces-de-sitio.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(["Campaign", "Link text", "Description line 1", "Description line 2", "Final URL"])
    for s in SITELINKS: w.writerow([CAMP] + list(s))
(RAIZ / "08-palabras-clave-para-copiar.txt").write_text("\n\n".join(f"# {g['nombre']}\n" + "\n".join(g["claves"]) for g in G), encoding="utf-8")
gd = RAIZ / "02-grupos-de-anuncios"; gd.mkdir(exist_ok=True)
for f in gd.glob("*.md"): f.unlink()
for i, g in enumerate(G, 1):
    md = [f"# Grupo {i}: {g['nombre']}", "", f"**Página de destino:** {g['url']}  ", f"**Rutas visibles:** {DOM.split('//')[1]}/{g['path1']}/{g['path2']}", ""]
    md += ["## Títulos (máximo 30 caracteres)"] + [f"{j}. {t} ({len(t)})" for j, t in enumerate(g["titulos"], 1)]
    md += ["", "## Descripciones (máximo 90 caracteres)"] + [f"{j}. {d} ({len(d)})" for j, d in enumerate(g["descripciones"], 1)]
    md += ["", f"## Palabras clave ({len(g['claves'])})"] + [f"- {k}" for k in g["claves"]]
    (gd / f"{i:02d}-{re.sub('[^a-z0-9]+', '-', g['nombre'].lower()).strip('-')}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(RAIZ / "03-palabras-negativas.md").write_text("# 3. Palabras negativas (a nivel de campaña)\n\nSon búsquedas por las que NO quieres pagar: otros productos Samsung (celulares, televisores…), compra de equipos nuevos, empleo, manuales, otros países y otras marcas. Ya vienen en `05-archivos-para-importar/palabras-negativas.csv`. Revisa «Términos de búsqueda» cada semana y agrega las que no te sirvan.\n\n" + "\n".join(f"- {k}" for k in NEGATIVAS) + "\n", encoding="utf-8")
(RAIZ / "04-recursos-extensiones.md").write_text("# Recursos (extensiones) a nivel de campaña\n\n## Enlaces de sitio (título ≤25, descripciones ≤35)\n"
    + "\n".join(f"- **{s[0]}** — {s[1]} / {s[2]} → {s[3]}" for s in SITELINKS) + "\n\n## Textos destacados (≤25)\n" + "\n".join(f"- {c}" for c in CALLOUTS)
    + f"\n\n## Fragmento estructurado\n**{SNIPPET[0]}:** {', '.join(SNIPPET[1])}\n\n## Llamadas\n- **No agregues recurso de llamada**: la atención es solo por WhatsApp. Tampoco actives «llamadas desde anuncios».\n\n## Imágenes\n- Usa fotos del técnico y de los equipos Samsung del sitio (cuadradas 1:1 y 1,91:1), sin texto encima.\n", encoding="utf-8")
ng = sum(len(g["claves"]) for g in G)
(QUI / "datos.json").write_text(json.dumps(dict(grupos=G, negativas=NEGATIVAS, sitelinks=SITELINKS, destacados=CALLOUTS, fragmento=SNIPPET, dominio=DOM, campana=CAMP, total_claves=ng), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK: {len(G)} grupos, {ng} palabras clave, {len(NEGATIVAS)} negativas, {len(SITELINKS)} enlaces")
