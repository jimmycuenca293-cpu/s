"""Tutorial de instalación de cada filtro: dónde va, cómo se saca el viejo, cómo se pone el nuevo,
cuánta agua purgar y cómo reiniciar el aviso. Lo usan la ficha del producto, las páginas de
referencia y de modelo de nevecón, y la página /instalacion/.

Donde el lugar cambia según el modelo, el texto lo dice: es mejor guiar al cliente a revisar
su nevecón que prometerle un sitio exacto que no sea el suyo.
"""
import html

esc = lambda s: html.escape(str(s), quote=True)

import json
import pathlib
import re

_APP = (pathlib.Path(__file__).resolve().parent.parent / "filtros-app" / "index.html").read_text(encoding="utf-8")
INSTALACION = json.loads(re.search(r"\nconst INSTALACION = (\{.*?\});\n", _APP).group(1))
_EXTERNO = INSTALACION["sam-ex-o"]
_INTERNO_GIRO = INSTALACION["lg-500-o"]["pasos"][1:5]


def datos(p):
    return INSTALACION.get(p["id"]) or (dict(_EXTERNO) if "-ex-" in p["id"] else {
        "donde": "Dentro del refrigerador, arriba o en la rejilla de abajo según el modelo.", "tiempo": "2 minutos",
        "herramientas": "Ninguna, solo un trapo.", "pasos": _INTERNO_GIRO + ["Saca unos 4 litros de agua por el dispensador."],
        "reset": "Reinicia el aviso dejando presionado 3 segundos el botón «Filter» del panel."})


def tutorial_html(p, nombre=None):
    """Sección «Cómo instalar» con los pasos propios del filtro. id="instalacion" para enlazarla."""
    d = datos(p)
    nombre = nombre or p["ref"]
    return f"""<section class="caja tutorial" id="instalacion">
  <h2>Cómo instalar el filtro {esc(nombre)}: paso a paso</h2>
  <dl class="dq"><dt>Dónde va</dt><dd>{esc(d["donde"])}</dd><dt>Tiempo</dt><dd>{esc(d["tiempo"])}</dd><dt>Herramientas</dt><dd>{esc(d["herramientas"])}</dd></dl>
  <ol class="pasos">{"".join(f"<li>{esc(x)}</li>" for x in d["pasos"])}</ol>
  <p><b>Último paso:</b> {esc(d["reset"])}</p>
  <p class="m">Consejos: el agua de los primeros vasos puede salir turbia o con burbujas, es normal y se aclara en unos minutos. Bota el primer hielo que salga después del cambio. Si gotea, saca el filtro y vuelve a meterlo derecho hasta que quede firme. En Cali te lo instalamos {"por $ 30.000" if "-ex-" in p["id"] else "gratis"}.</p>
</section>"""


def tutorial_ld(p, url, nombre=None):
    """Datos estructurados HowTo para Google y los asistentes de IA."""
    d = datos(p)
    nombre = nombre or p["ref"]
    pasos = d["pasos"] + [d["reset"]]
    return {"@type": "HowTo", "name": f"Cómo instalar el filtro de agua {nombre}", "totalTime": "PT15M" if "15" in d["tiempo"] else "PT3M",
            "supply": [{"@type": "HowToSupply", "name": f"Filtro {nombre}"}], "tool": [{"@type": "HowToTool", "name": "Trapo"}],
            "step": [{"@type": "HowToStep", "position": i + 1, "text": x, "url": f"{url}#instalacion"} for i, x in enumerate(pasos)]}
