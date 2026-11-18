# Archivos de salida: buscador y banner, formulario de solicitud, API, mapa del sitio, sitemaps, robots, llms y datos (se ejecuta al final de st_paginas.py).
mapa = lambda t, its: f'<h2 style="font-size:22px;margin:22px 0 10px">{esc(t)}</h2><ul class="spec-list">' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>' for n, u in its) + "</ul>"
for pk, P in PAISES.items():
    cs_ = CIU_PAIS[pk]
    cuerpo = (mapa("Ciudades", [(f"Servicio técnico Samsung en {c['n']}", R_CIU(c)) for c in cs_])
              + mapa("Zonas", [(f"Servicio técnico Samsung en {z}, {c['n']}", R_Z(c, z)) for c, z in ZONAS_P if c["pk"] == pk]) + mapa("Mantenimiento por ciudad", [(f"Mantenimiento en {c['n']}", R_MANT(c)) for c in cs_]) + mapa("Voltaje", [(f"Voltaje en {P['nombre']}", R_VOLT(pk))])
              + mapa("Equipos", [(f"Servicio técnico de {pal(pk, s_)[1]} Samsung en {P['nombre']}", R_SERV(pk, s_)) for s_ in SERV_PAIS[pk]]) + mapa("Guías de fallas", [(loc(g["tit"], pk), R_G(g, pk)) for g in GUIAS_PK(pk)] + [("Códigos de error de lavadoras Samsung", R_COD_LISTA(pk))] + [(f"Cómo leer el modelo de tu {pal(pk, sv)[0]} Samsung", R_MOD(pk, sv)) for sv in SERV_PAIS[pk]])
              + mapa("Blog", [("Blog de soporte técnico Samsung", f"{pk}/blog/index.html")] + [(t, u) for k, sl, t, u, d in BLOG if k == pk]) + mapa("Líneas Samsung", [(f"{cap(pal(k, sv)[1])} Samsung {ln} en {P['nombre']}", u) for k, sv, ln, u in LINEAS_P if k == pk]) + mapa("Fallas frecuentes por ciudad", [(pr["tit"].format(S=cap(pal(c["pk"], pr["sv"])[0]), s=pal(c["pk"], pr["sv"])[0], c=c["n"]), R_PROB(c, pr)) for c, pr in PROB_P if c["pk"] == pk])
              + mapa("Por departamento", [(f"Servicio técnico Samsung en {d} ({P['nombre']})", R_DEP(k, d)) for k, d in DEP_HUBS if k == pk]) + (mapa("Más páginas por barrio, equipo y falla", [(t_, u_) for t_, u_, tp_ in SOLO_EXTRA]) if SOLO else "") + mapa("Contacto por ciudad", [(h, u) for k, c_, t_, u, h in CONT_P if k == pk]) + mapa("Ayuda", [("Solicitar visita", R_SOL(pk)), ("Preguntas frecuentes", R_FAQ(pk)), ("Respuestas rápidas", R_IA(pk)), ("Quiénes somos", R_INST(pk, "quienes-somos")), ("Contacto", R_INST(pk, "contacto"))]))
    pagina(R_MAPA(pk), f"Mapa del sitio | Servicio técnico Samsung en {P['nombre']}", f"Todas las páginas del servicio técnico Samsung en {P['nombre']}: ciudades, zonas, equipos y guías de fallas.", f"mapa del sitio servicio tecnico samsung {P['nombre'].lower()}", [("Inicio", "index.html"), (P["nombre"], R_PAIS(pk)), ("Mapa del sitio", None)],
           hero_simple(f"{P['bandera']} Mapa del sitio", f"Todas las páginas de {P['nombre']}", "Ciudades, equipos y guías.") + qa(f"¿Qué hay en la sección de {P['nombre']}?", f"Servicio técnico Samsung en {len(cs_)} ciudades de {esc(P['nombre'])}, páginas por equipo, guías de fallas y respuestas rápidas.") + seccion("Páginas", cuerpo), [], [], prio="0.4", pk=pk, tipo="guias")

if SOLO:
    _nom = CIU[0]['n']
    _items = "".join(f"<item><title>{esc(t)}</title><link>{U(u)}</link><guid>{U(u)}</guid><description>{esc(d)}</description></item>" for k_, sl, t, u, d in BLOG)
    (OUT / "feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Blog · {NOMBRE}</title><link>{DOMINIO}/</link><description>Consejos para cuidar y reparar electrodomésticos Samsung en {_nom}</description>{_items}</channel></rss>\n', encoding="utf-8")

# buscador + banner de ciudades
CL = lambda u: (lambda v: v[:-10] if v.endswith("index.html") else v)(solo_ruta(u))
items = []
for _pk, _P in PAISES.items():
    _it = [[_P["nombre"], R_PAIS(_pk), "País", f"{len(CIU_PAIS[_pk])} ciudades", _pk]] + [[c["n"], R_CIU(c), "Ciudad", c["pais"], _pk] for c in CIU_PAIS[_pk]]
    _it += [[cap(pal(_pk, s_)[1]), R_SERV(_pk, s_), "Servicio", _P["nombre"], _pk] for s_ in SERV_PAIS[_pk]] + [[loc(g["tit"], _pk), R_G(g, _pk), "Guía de fallas", "", _pk] for g in GUIAS_PK(_pk)]
    _it += [[f"{cap(pal(_pk, sv)[1])} en {c['n']}", R_CS(c, sv), "Reparación", c["pais"], _pk] for c in CIU_PAIS[_pk] for sv in SERV_PAIS[_pk]]
    _it += [[f"{z} · {c['n']}", R_Z(c, z), "Zona", c["pais"], _pk] for c, z in ZONAS_P if c["pk"] == _pk]
    _it += [[f"{cap(pal(k, sv)[1])} Samsung {ln}", u, "Línea", _P["nombre"], _pk] for k, sv, ln, u in LINEAS_P if k == _pk]
    _it += [[t, u, "Blog", _P["nombre"], _pk] for k, sl, t, u, d in BLOG if k == _pk]
    _it += [[h, u, "Contacto", _P["nombre"], _pk] for k, c_, t_, u, h in CONT_P if k == _pk]
    _it += [[pr["tit"].format(S=cap(pal(c["pk"], pr["sv"])[0]), s=pal(c["pk"], pr["sv"])[0], c=c["n"]), R_PROB(c, pr), "Falla", c["pais"], _pk] for c, pr in PROB_P if c["pk"] == _pk]
    if SOLO:
        _it += [[t_, u_, tp_, _P["nombre"], _pk] for t_, u_, tp_ in SOLO_EXTRA]
    items.append((_pk, [[a, CL(b), c_, d_, e_] for a, b, c_, d_, e_ in _it]))
home_items = [[P["nombre"], CL(R_PAIS(pk)), "País", f"{len(CIU_PAIS[pk])} ciudades", ""] for pk, P in PAISES.items()]


def mk_js(its):
    return _mk_js(its).replace("r[2]==='Ciudad'&&r[4]===K", "r[2]==='Zona'&&r[4]===K") if SOLO else _mk_js(its)


def _mk_js(its):
    return ("(function(){var D=" + json.dumps(its, ensure_ascii=False, separators=(",", ":")) + ";"
          "function n(s){return s.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/[^a-z0-9 ]+/g,' ').trim()}var X=D.map(function(r){return n(r[0]+' '+r[2]+' '+r[3])});"
          "function buscar(q,P){q=n(q);if(!q)return[];var t=q.split(/ +/),o=[];for(var i=0;i<D.length;i++){if(P&&D[i][4]&&D[i][4]!==P)continue;var ok=true,sc=0;for(var j=0;j<t.length;j++){var p=X[i].indexOf(t[j]);if(p<0){ok=false;break}sc+=p===0?0:1}if(ok){var e=n(D[i][0]);o.push([sc+(e.indexOf(q)===0?-2:0)+(D[i][2]==='Ciudad'||D[i][2]==='País'?0:.5),i])}}o.sort(function(a,b){return a[0]-b[0]});return o.slice(0,14).map(function(x){return D[x[1]]})}"
          "function pintar(caja,r,q){if(!q.trim()){caja.hidden=true;return}var g={},h='';r.forEach(function(x){(g[x[2]]=g[x[2]]||[]).push(x)});Object.keys(g).forEach(function(k){h+='<h6>'+k+'</h6>'+g[k].map(function(x){return '<a href=\"'+(window.ST_ROOT||'')+x[1]+'\"><span>'+x[0]+'</span><small>'+x[3]+'</small></a>'}).join('')});caja.innerHTML=h||'<p>No encontramos «'+q.replace(/</g,'')+'». Prueba con tu ciudad, tu país o el equipo.</p>';caja.hidden=false}"
          "document.querySelectorAll('[data-aq-q]').forEach(function(i){var c=i.parentNode.querySelector('.aq-res');var P=i.getAttribute('data-aq-pais')||'';i.addEventListener('input',function(){pintar(c,buscar(i.value,P),i.value)});i.addEventListener('focus',function(){if(i.value)pintar(c,buscar(i.value,P),i.value)});i.addEventListener('keydown',function(e){if(e.key==='Enter'){var a=c.querySelector('a');if(a)location.href=a.getAttribute('href')}if(e.key==='Escape')c.hidden=true})});"
          "(function(){var t=document.querySelector('[data-tk]');if(!t)return;var K=t.getAttribute('data-tk');var c=D.filter(function(r){return K==='paises'?r[2]==='País':(r[2]==='Ciudad'&&r[4]===K)}).map(function(r){return r[0]});if(!c.length)return;var h=c.map(function(n){return '<span>'+n+'</span>'}).join('');t.innerHTML=h+h;t.style.setProperty('--d',Math.max(25,Math.round(c.length*3))+'s')})();"
          "document.addEventListener('click',function(e){document.querySelectorAll('.aq-res').forEach(function(c){if(!c.parentNode.contains(e.target))c.hidden=true});document.querySelectorAll('.aq-nav details[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open')})});})();")



(OUT / "buscar.js").write_text(mk_js(home_items), encoding="utf-8")
for _pk, _it in items:
    (OUT / _pk).mkdir(parents=True, exist_ok=True)
    (OUT / _pk / "buscar.js").write_text(mk_js(_it), encoding="utf-8")


(OUT / "solicitar.js").write_text("""(function(){var f=document.getElementById('sv-form');if(!f)return;var P=document.getElementById('sv-pais'),C=document.getElementById('sv-ciudad'),R=document.getElementById('sv-res');
function ciu(){C.innerHTML=(window.SV_CIU[P.value]||[]).map(function(c){return '<option>'+c+'</option>'}).join('')}P.addEventListener('change',ciu);ciu();
function FY(f){if(Array.isArray(f)){f.forEach(FY);return}if(!f||!f.url||!f.datos)return;try{fetch(f.url,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(f.datos),keepalive:true}).catch(function(){})}catch(e){}}
f.addEventListener('submit',function(e){e.preventDefault();var d={};new FormData(f).forEach(function(v,k){d[k]=v});if(!d.nombre||!d.tel||String(d.tel).replace(/\\D/g,'').length<7){R.innerHTML='<p style="color:#b91c1c">Escribe tu nombre y un celular válido.</p>';return}
R.textContent='Enviando…';fetch('/api/solicitud.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)}).then(function(r){return r.json()}).then(function(j){if(!j.ok)throw new Error(j.mensaje||'Error');FY(j.form);
var m=encodeURIComponent('Hola, acabo de solicitar una visita ('+j.ref+') para mi '+d.equipo+' Samsung en '+d.ciudad);R.innerHTML='<div class="st-ok"><b>¡Solicitud recibida!</b><br>Tu referencia es '+j.ref+'. Te contactaremos pronto. Si es urgente, escríbenos por WhatsApp.<br><a class="st-btn wa" style="margin-top:10px" target="_blank" rel="noopener" href="https://wa.me/'+(window.SV_WA||'')+'?text='+m+'">Escribir por WhatsApp</a></div>';f.reset();ciu()}).catch(function(){R.innerHTML='<p style="color:#b91c1c">No pudimos enviar el formulario. Escríbenos por WhatsApp y te atendemos.</p>'})})})();
""".replace("window.SV_WA||''", "(window.SV_WA||{})[d.pais]||''"), encoding="utf-8")

# API: solicitud de visita (correo por SMTP a todos los destinatarios + formulario desde el navegador)
api = OUT / "api"; api.mkdir(exist_ok=True); (OUT / "data").mkdir(exist_ok=True)
shutil.copy(AQUI / "src" / "api" / "lib.php", api / "lib.php")
(api / ".htaccess").write_text('<FilesMatch ".*">\n  Require all denied\n</FilesMatch>\n<FilesMatch "^solicitud\\.php$">\n  Require all granted\n</FilesMatch>\nOptions -Indexes\n', encoding="utf-8")
(OUT / "data" / ".htaccess").write_text("Require all denied\n", encoding="utf-8")
(api / "solicitud.php").write_text(r"""<?php
declare(strict_types=1);
require __DIR__ . '/lib.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') { http_response_code(405); echo '{"ok":false}'; exit; }
$j = json_decode((string) file_get_contents('php://input'), true);
if (!is_array($j)) { http_response_code(400); echo '{"ok":false,"mensaje":"Datos inválidos"}'; exit; }
if (!empty($j['web'])) { echo '{"ok":true,"ref":"OK","form":[]}'; exit; }
$lim = fn(string $k, int $n): string => mb_substr(trim(strip_tags((string) ($j[$k] ?? ''))), 0, $n);
$d = ['Nombre' => $lim('nombre', 80), 'Celular' => $lim('tel', 30), 'Correo del cliente' => $lim('email', 100), 'País' => $lim('pais', 40), 'Ciudad' => $lim('ciudad', 60), 'Equipo' => $lim('equipo', 60), 'Modelo' => $lim('modelo', 60), 'Problema' => $lim('problema', 600)];
if (mb_strlen($d['Nombre']) < 2 || strlen(preg_replace('/\D/', '', $d['Celular'])) < 7 || $d['Ciudad'] === '' || $d['Equipo'] === '') { http_response_code(422); echo '{"ok":false,"mensaje":"Faltan datos"}'; exit; }
if ($d['Correo del cliente'] !== '' && !filter_var($d['Correo del cliente'], FILTER_VALIDATE_EMAIL)) $d['Correo del cliente'] = '';
// Límite sencillo: máximo 8 solicitudes por hora desde la misma IP
$dir = __DIR__ . '/../data'; if (!is_dir($dir)) @mkdir($dir, 0755, true);
$lf = $dir . '/limite-' . md5((string) ($_SERVER['REMOTE_ADDR'] ?? '')) . '.txt';
$t = is_file($lf) ? array_filter(array_map('intval', explode(',', (string) file_get_contents($lf))), fn($x) => $x > time() - 3600) : [];
if (count($t) >= 8) { http_response_code(429); echo '{"ok":false,"mensaje":"Demasiadas solicitudes"}'; exit; }
$t[] = time(); @file_put_contents($lf, implode(',', $t));
$ref = 'SV-' . date('ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
$asunto = "Nueva solicitud de visita $ref — {$d['Equipo']} — {$d['Ciudad']}, {$d['País']}";
$filas = '';
foreach (['Nombre', 'Celular', 'Correo del cliente', 'País', 'Ciudad', 'Equipo', 'Modelo', 'Problema'] as $k) if ($d[$k] !== '') $filas .= '<tr><td style="padding:6px 10px;color:#5a6873">' . h($k) . '</td><td style="padding:6px 10px"><b>' . h($d[$k]) . '</b></td></tr>';
$html = '<h2 style="margin:0 0 8px">Nueva solicitud de visita</h2><p>Referencia <b>' . h($ref) . '</b>. Contacta al cliente para coordinar.</p><table style="border-collapse:collapse">' . $filas . '</table>';
$ok = false; $m = '';
foreach (correos_destino() as $dest) { if (enviar_correo($dest, $asunto, $html, $m)) $ok = true; }
if ($d['Correo del cliente'] !== '') enviar_correo($d['Correo del cliente'], "Recibimos tu solicitud $ref", '<h2 style="margin:0 0 8px">Recibimos tu solicitud</h2><p>Hola ' . h($d['Nombre']) . ', recibimos tu solicitud de visita (' . h($ref) . ') para tu ' . h($d['Equipo']) . ' Samsung en ' . h($d['Ciudad']) . '. Te contactaremos pronto para coordinar.</p>', $m2);
$forms = [];
foreach (correos_destino() as $dest) {
    $pl = form_payload($asunto, ['Solicitud' => $ref] + $d);
    $pl['url'] = preg_replace('~/ajax/.*$~', '/ajax/', $pl['url']) . rawurlencode($dest);
    unset($pl['datos']['_cc']);
    $forms[] = $pl;
}
@file_put_contents($dir . '/solicitudes.log', date('c') . " $ref " . json_encode($d, JSON_UNESCAPED_UNICODE) . ($ok ? '' : ' [correo no enviado]') . "\n", FILE_APPEND);
echo json_encode(['ok' => true, 'ref' => $ref, 'correo' => $ok, 'form' => $forms], JSON_UNESCAPED_UNICODE);
""", encoding="utf-8")
cfg = (AQUI / "src" / "api" / "config.sample.php").read_text(encoding="utf-8")
cfg = (cfg.replace("'dominio' => 'https://filtrosnevecones.com'", f"'dominio' => '{DOMINIO}'").replace("'nombre'    => 'Filtros Nevecones Colombia'", f"'nombre'    => '{NOMBRE}'").replace("'telefono'  => '310 714 7299'", f"'telefono'  => '{wa_vis('colombia')}'")
       .replace("'whatsapp' => '3107147299'", f"'whatsapp' => '{WA_DEF}'").replace("'gtm' => 'GTM-5WSNHV66'", f"'gtm' => '{GTM}'").replace("w-s2eiVewLzOHFjK7HAR9UUeqFoNMS14k_Gfrqt_ND4", TOKENS[0] if TOKENS else ""))
if os.environ.get("CORREO_AVISOS"):
    cfg = cfg.replace("'correo_avisos'    => 'serviciotecnicoyrepuestoscali@gmail.com'", f"'correo_avisos'    => '{os.environ['CORREO_AVISOS']}'", 1)
if os.environ.get("SMTP_CLAVE"):
    cfg = cfg.replace("'clave'   => '',", f"'clave'   => '{os.environ['SMTP_CLAVE']}',", 1)
(api / "config.sample.php").write_text(cfg, encoding="utf-8")
if os.environ.get("SMTP_CLAVE"):
    (api / "config.php").write_text(cfg, encoding="utf-8")

# datos estructurados, llms, robots y sitemaps: cada país tiene los suyos dentro de su carpeta; la raíz solo apunta a ellos
for pk, P in PAISES.items():
    cs = CIU_PAIS[pk]; v = VOLT[pk]
    DATA = {"negocio": {"nombre": NOMBRE, "tipo": "Servicio técnico independiente especializado en electrodomésticos Samsung (no es Samsung Electronics)", "pais": P["nombre"], "url": U(R_PAIS(pk)), "whatsapp": "+" + wa_num(pk), "atencion": "A domicilio", "diagnostico": "Primero el diagnóstico; el valor se confirma antes de reparar", "actualizado": HOY},
            "ciudades": [{"ciudad": c["n"], "zonas": {z: U(R_Z(c, z)) for z in c["zonas"]}, "mantenimiento": U(R_MANT(c)), "clima": CLIMA[c["s"]]["clima"], "altitud_m": CLIMA[c["s"]]["alt"], "url": U(R_CIU(c)), "servicios": {pal(pk, sv)[1]: U(R_CS(c, sv)) for sv in SERV_PAIS[pk]}} for c in cs],
            "servicios": {SERVICIOS[s_]["tit"]: {"lineas": SERVICIOS[s_]["lineas"], "fallas": SERVICIOS[s_]["sintomas"], "pagina": U(R_SERV(pk, s_))} for s_ in SERV_PAIS[pk]}}
    (OUT / pk / "datos-servicio-tecnico.json").write_text(json.dumps(DATA, ensure_ascii=False, indent=1), encoding="utf-8")
    L = [f"# Servicio técnico Samsung en {P['nombre']}", "", f"> Servicio técnico independiente especializado en electrodomésticos Samsung en {P['nombre']} (no somos Samsung Electronics). Visita a domicilio en {len(cs)} ciudades; primero el diagnóstico y el valor se confirma antes de reparar. WhatsApp +{wa_num(pk)}. Actualizado el {FECHA_LARGA}.", "",
         "## Equipos que reparamos"] + [f"- [{cap(pal(pk, s_)[1])}]({U(R_SERV(pk, s_))}): {SERVICIOS[s_]['lineas']}." for s_ in SERV_PAIS[pk]]
    L += ["", "## Ciudades"] + [f"- [{c['n']}]({U(R_CIU(c))})" + (" (cobertura ampliada, con coordinación previa)" if c["amp"] else "") for c in cs]
    L += ["", "## Guías de fallas"] + [f"- [{loc(g['tit'], pk)}]({U(R_G(g, pk))}): {loc(g['res'], pk)}" for g in GUIAS_PK(pk)]
    L += ["", "## Datos útiles", f"- Red eléctrica: {v[0]} a {v[1]}, enchufes {v[2]}.", f"- [Voltaje y electrodomésticos Samsung en {P['nombre']}]({U(R_VOLT(pk))})", f"- [Preguntas frecuentes]({U(R_FAQ(pk))})", f"- [Respuestas rápidas]({U(R_IA(pk))})", f"- [Datos estructurados]({DOMINIO}/{pk}/datos-servicio-tecnico.json)", f"- [llms-full.txt]({DOMINIO}/{pk}/llms-full.txt)", "", "## Preguntas y respuestas"]
    QA_ = []
    for c in cs:
        for sv in SERV_PAIS[pk]:
            QA_ += [f"**¿Reparan {pal(pk, sv)[1]} Samsung en {c['n']}?** Sí, con visita a domicilio" + (" (cobertura ampliada)" if c["amp"] else "") + f"; el valor se confirma tras el diagnóstico. WhatsApp +{wa_num(pk)}.", ""]
    (OUT / pk / "llms.txt").write_text("\n".join(L + QA_) + "\n", encoding="utf-8")
    LF = L[:3] + ["", "## Preguntas y respuestas", ""] + QA_ + ["## Guías (texto completo)", ""] + [x for g in GUIAS_PK(pk) for x in (f"### {loc(g['tit'], pk)}", loc(g["res"], pk), loc(re.sub(r"<[^>]+>", " ", g["cuerpo"]), pk), "")]
    (OUT / pk / "llms-full.txt").write_text("\n".join(LF) + "\n", encoding="utf-8")
ll = [f"# {NOMBRE}", "", f"> Servicio técnico independiente especializado en electrodomésticos Samsung (no somos Samsung Electronics). Cada país tiene su propia sección con sus ciudades y su WhatsApp. Actualizado el {FECHA_LARGA}.", "", "## Información por país"]
ll += [f"- [{P['nombre']}]({DOMINIO}/{pk}/llms.txt)" for pk, P in PAISES.items()]
(OUT / "llms.txt").write_text("\n".join(ll) + "\n", encoding="utf-8")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /api/\nDisallow: /data/\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ("GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-Web", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "Bingbot", "Googlebot", "Amazonbot", "meta-externalagent", "cohere-ai", "DuckAssistBot", "MistralAI-User", "YouBot", "Applebot"))
                                + f"Sitemap: {DOMINIO}/sitemap.xml\n" + "".join(f"Sitemap: {DOMINIO}/sitemap-{pk}.xml\n" for pk in PAISES), encoding="utf-8")
grupos = {pk: [] for pk in PAISES}
grupos["inicio"] = []
for n, pr, _t, _d, tp in PAGINAS:
    grupos[n.split("/")[0] if n.split("/")[0] in PAISES else "inicio"].append((n, pr))
for g, l in grupos.items():
    (OUT / (f"sitemap-{g}.xml")).write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f"  <url><loc>{U(n)}</loc><lastmod>{HOY}</lastmod><changefreq>weekly</changefreq><priority>{pr}</priority></url>\n" for n, pr in l) + "</urlset>\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <sitemap><loc>{DOMINIO}/sitemap-{g}.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n" for g in grupos) + "</sitemapindex>\n", encoding="utf-8")
(OUT / ".htaccess").write_text("""DirectoryIndex index.html index.php
ErrorDocument 404 /404.html
Options -Indexes
RewriteEngine On
RewriteCond %{THE_REQUEST} \\s/+(.*?/)?index\\.html[\\s?]
RewriteRule ^(.*?/)?index\\.html$ /$1 [R=301,L]
RewriteCond %{HTTPS} off
RewriteCond %{HTTP:X-Forwarded-Proto} !https
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
<FilesMatch "\\.(sqlite|sqlite-wal|sqlite-shm|log)$">
  Require all denied
</FilesMatch>
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript application/json application/xml text/plain image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 week"
  ExpiresByType application/javascript "access plus 1 week"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>
<IfModule mod_headers.c>
  Header set X-Content-Type-Options "nosniff"
  Header set Referrer-Policy "strict-origin-when-cross-origin"
  Header set X-Frame-Options "SAMEORIGIN"
  Header set Strict-Transport-Security "max-age=31536000" env=HTTPS
</IfModule>
""", encoding="utf-8")
# ---- detección de país y ciudad (zona horaria sin permiso; ubicación exacta solo si el cliente la permite)
import csv as _c
_COD = {"colombia": "co", "panama": "pa", "costa-rica": "cr", "paraguay": "py", "guatemala": "gt", "el-salvador": "sv", "ecuador": "ec", "chile": "cl"}
_NORM = lambda x: slug(x)
_coord = {}
_csv = AQUI.parent / "app-servicio-tecnico-latam" / "tecnicos.csv"
if _csv.exists():
    for _r in _c.DictReader(open(_csv, encoding="utf-8")):
        if _r["marca"] == "samsung":
            try:
                _coord.setdefault((_r["pais"], _NORM(_r["ciudad"])), (float(_r["lat"]), float(_r["lon"])))
            except ValueError:
                pass
_extra = {("co", "giron"): (7.07, -73.17), ("co", "piedecuesta"): (6.99, -73.05), ("co", "rionegro"): (6.155, -75.374), ("co", "la-estrella"): (6.158, -75.643), ("co", "sabaneta"): (6.151, -75.616), ("co", "dosquebradas"): (4.84, -75.67),
          ("co", "santa-rosa-de-cabal"): (4.868, -75.62), ("co", "jamundi"): (3.26, -76.54), ("co", "buga"): (3.9, -76.3), ("co", "duitama"): (5.82, -73.03), ("co", "ipiales"): (0.83, -77.64), ("co", "san-andres"): (12.58, -81.7),
          ("co", "fusagasuga"): (4.34, -74.36), ("co", "facatativa"): (4.81, -74.36), ("co", "bogota"): (4.711, -74.072), ("pa", "ciudad-de-panama"): (8.983, -79.517), ("cr", "san-jose"): (9.928, -84.091), ("py", "asuncion"): (-25.264, -57.576),
          ("gt", "ciudad-de-guatemala"): (14.635, -90.507), ("sv", "san-salvador"): (13.693, -89.218), ("ec", "quito"): (-0.18, -78.468), ("ec", "guayaquil"): (-2.17, -79.92), ("cl", "santiago-de-chile"): (-33.449, -70.669)}
_geo = []
for _c_ in CIU:
    _k = (_COD[_c_["pk"]], _NORM(_c_["n"]))
    _ll = _coord.get(_k) or _extra.get(_k) or _coord.get((_k[0], _NORM(_c_["n"].replace("de Chile", "").strip())))
    if _ll:
        _geo.append([_c_["pk"], _c_["n"], CL(R_CIU(_c_)), round(_ll[0], 3), round(_ll[1], 3), 1 if _c_["amp"] else 0])
_pp = {pk: [P["nombre"], CL(R_PAIS(pk))] for pk, P in PAISES.items()}
(OUT / "geo.js").write_text("""(function(){var C=""" + json.dumps(_geo, ensure_ascii=False, separators=(",", ":")) + """,P=""" + json.dumps(_pp, ensure_ascii=False, separators=(",", ":")) + """;
var TZ={'America/Bogota':'colombia','America/Panama':'panama','America/Costa_Rica':'costa-rica','America/Asuncion':'paraguay','America/Guatemala':'guatemala','America/El_Salvador':'el-salvador','America/Guayaquil':'ecuador','Pacific/Galapagos':'ecuador','America/Santiago':'chile','America/Punta_Arenas':'chile'};
var LG={'es-co':'colombia','es-pa':'panama','es-cr':'costa-rica','es-py':'paraguay','es-gt':'guatemala','es-sv':'el-salvador','es-ec':'ecuador','es-cl':'chile'};
function K(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
var m=document.querySelector('meta[name="st-pais"]'),aqui=m?m.content:'';
var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
var det=K('st_pais')||TZ[tz]||LG[(navigator.language||'').toLowerCase()]||'';
function dist(a,b,c,d){var R=6371,r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h))}
function cerca(lat,lon){var b=null,bd=1e9,dd=null,dm=1e9;C.forEach(function(c){var d=dist(lat,lon,c[3],c[4]);if(d<bd){bd=d;b=c}if(!c[5]&&d<dm){dm=d;dd=c}});if(b&&b[5]&&dd&&dm-bd<25){b=dd;bd=dm}return b?{c:b,d:bd}:null}
function barra(html){var d=document.createElement('div');d.className='st-geo';d.setAttribute('role','region');d.setAttribute('aria-label','Tu ubicación');d.innerHTML=html;document.body.insertBefore(d,document.body.firstChild);return d}
function usar(btn,msg){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación.';return}btn.disabled=true;msg.textContent='Buscando tu ubicación…';
navigator.geolocation.getCurrentPosition(function(p){var r=cerca(p.coords.latitude,p.coords.longitude);if(!r){msg.textContent='No pudimos ubicarte.';btn.disabled=false;return}K('st_pais',r.c[0]);
if(r.d>800){msg.innerHTML='Estás lejos de nuestras ciudades. La más cercana es '+r.c[1]+' ('+Math.round(r.d)+' km). <a href="'+r.c[2]+'">Ver '+r.c[1]+'</a>';btn.disabled=false;return}
msg.textContent='Estás cerca de '+r.c[1]+'. Te llevamos a su página…';location.href=r.c[2]},function(){msg.textContent='No se pudo obtener la ubicación. Elige tu país abajo.';btn.disabled=false},{enableHighAccuracy:true,timeout:12000,maximumAge:300000})}
window.STUbicacion=usar;
document.addEventListener('DOMContentLoaded',function(){
 document.querySelectorAll('[data-geo]').forEach(function(b){var msg=b.parentNode.querySelector('[data-geo-msg]')||document.createElement('span');b.addEventListener('click',function(){usar(b,msg)})});
 if(K('st_geo_x')==='1')return;
 if(det&&P[det]&&det!==aqui){var b=barra('<span>Parece que estás en <b>'+P[det][0]+'</b>.</span> <a class="st-btn sol" href="'+P[det][1]+'">Ver servicio técnico Samsung en '+P[det][0]+'</a> <button type="button" class="st-btn" data-ub>Usar mi ubicación exacta</button> <span data-um></span> <button type="button" class="st-x" aria-label="Cerrar">×</button>');
  b.querySelector('[data-ub]').addEventListener('click',function(){usar(this,b.querySelector('[data-um]'))});b.querySelector('.st-x').addEventListener('click',function(){K('st_geo_x','1');b.remove()});
  var cards=document.querySelectorAll('.st-pais');cards.forEach(function(a){if(a.getAttribute('href')===P[det][1]){a.classList.add('st-pais-det');var g=a.parentNode;g.insertBefore(a,g.firstChild)}})}
 else if(!aqui&&!det){}
 try{if(navigator.permissions&&!aqui){navigator.permissions.query({name:'geolocation'}).then(function(r){if(r.state==='granted'){var b=document.querySelector('[data-geo]');if(b)usar(b,b.parentNode.querySelector('[data-geo-msg]')||document.createElement('span'))}})}}catch(e){}
});})();
""", encoding="utf-8")
for _pk in PAISES:
    _cg = [g for g in _geo if g[0] == _pk]
    (OUT / _pk / "geo.js").write_text("""(function(){var C=""" + json.dumps(_cg, ensure_ascii=False, separators=(",", ":")) + """,R=window.ST_ROOT||'';
function dist(a,b,c,d){var r=Math.PI/180,x=(c-a)*r,y=(d-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 12742*Math.asin(Math.sqrt(h))}
function cerca(lat,lon){var b=null,bd=1e9,dd=null,dm=1e9;C.forEach(function(c){var d=dist(lat,lon,c[3],c[4]);if(d<bd){bd=d;b=c}if(!c[5]&&d<dm){dm=d;dd=c}});if(b&&b[5]&&dd&&dm-bd<25){b=dd;bd=dm}return b?{c:b,d:bd}:null}
function usar(btn,msg){if(!navigator.geolocation){msg.textContent='Tu navegador no permite ubicación.';return}btn.disabled=true;msg.textContent='Buscando tu ubicación…';
navigator.geolocation.getCurrentPosition(function(p){var r=cerca(p.coords.latitude,p.coords.longitude);btn.disabled=false;if(!r){msg.textContent='No pudimos ubicarte.';return}
if(r.d>150){msg.innerHTML='Tu ubicación está lejos de nuestras ciudades. La más cercana es '+r.c[1]+' ('+Math.round(r.d)+' km). <a href="'+R+r.c[2]+'">Ver '+r.c[1]+'</a>';return}
msg.textContent='Estás en '+r.c[1]+'. Abriendo su página…';location.href=R+r.c[2]},function(){btn.disabled=false;msg.textContent='No se pudo obtener la ubicación. Elige tu ciudad en el menú.'},{enableHighAccuracy:true,timeout:12000,maximumAge:300000})}
document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('[data-geo]').forEach(function(b){var m=b.parentNode.querySelector('[data-geo-msg]')||(function(){var s=document.createElement('p');s.className='st-aviso';s.setAttribute('data-geo-msg','');b.parentNode.parentNode.insertBefore(s,b.parentNode.nextSibling);return s})();b.addEventListener('click',function(){usar(b,m)})})});})();
""", encoding="utf-8")
# ---- imágenes con nombre descriptivo (SEO de imágenes) y sitemap de imágenes
RN = {"nevera-family-hub": "nevera-samsung-side-by-side-family-hub", "nevera-superior-inox": "nevera-samsung-superior-inox", "lavadora-superior": "lavadora-samsung-carga-superior", "secadora-torre": "torre-lavado-secado-samsung-apilada", "secadora": "secadora-samsung-carga-frontal",
      "torre-lavado": "torre-de-lavado-samsung", "microondas": "microondas-samsung-ceramic-inside", "portada-tecnico": "tecnico-samsung-a-domicilio-portada", "tecnico-neveras": "tecnico-reparando-nevera-samsung", "tecnico-lavadora": "tecnico-reparando-lavadora-samsung",
      "c-revision": "tecnico-samsung-revision-en-casa", "c-compresor": "tecnico-samsung-revisando-compresor", "sam-cin-o": "filtro-agua-samsung-haf-cin", "sam-qin-o": "filtro-agua-samsung-haf-qin", "sam-cu1-o": "filtro-agua-samsung-aqua-pure-plus", "sam-ex-o": "filtro-agua-externo-samsung"}
for _i in range(1, 8):
    RN[f"stp{_i}"] = f"tecnico-samsung-visita-a-domicilio-{_i}"
for _o, _n in sorted(RN.items(), key=lambda x: -len(x[0])):
    for _suf in ("", "-m", "-s", "-400"):
        _f = OUT / "img" / f"{_o}{_suf}.webp"
        if _f.exists():
            _f.rename(OUT / "img" / f"{_n}{_suf}.webp")
_pat = re.compile(r"img/(" + "|".join(re.escape(o) for o in sorted(RN, key=lambda x: -len(x))) + r")((?:-m|-s|-400)?)\.webp")
for _h in list(OUT.rglob("*.html")) + [OUT / "tema.css"]:
    _t = _h.read_text(encoding="utf-8")
    _t2 = _pat.sub(lambda m: f"img/{RN[m.group(1)]}{m.group(2)}.webp", _t)
    if _t2 != _t:
        _h.write_text(_t2, encoding="utf-8")
for _pk in list(PAISES) + ["inicio"]:
    _img = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    for _n, _pr, _t, _d, _tp in PAGINAS:
        if (_n.split("/")[0] if _n.split("/")[0] in PAISES else "inicio") != _pk:
            continue
        _imgs = []
        for _m in re.finditer(r'<img[^>]+src="img/([^"]+\.webp)"[^>]*alt="([^"]*)"', (OUT / _n).read_text(encoding="utf-8")):
            if _m.group(1) not in [x[0] for x in _imgs]:
                _imgs.append((_m.group(1), _m.group(2)))
        if _imgs:
            _img += f"  <url><loc>{U(_n)}</loc>" + "".join(f"<image:image><image:loc>{DOMINIO}/img/{a}</image:loc><image:caption>{esc(b)}</image:caption></image:image>" for a, b in _imgs[:8]) + "</url>\n"
    (OUT / f"sitemap-imagenes-{_pk}.xml").write_text(_img + "</urlset>\n", encoding="utf-8")
_sm = (OUT / "sitemap.xml").read_text(encoding="utf-8")
(OUT / "sitemap.xml").write_text(_sm.replace("</sitemapindex>", "".join(f"  <sitemap><loc>{DOMINIO}/sitemap-imagenes-{_pk}.xml</loc><lastmod>{HOY}</lastmod></sitemap>\n" for _pk in list(PAISES) + ["inicio"]) + "</sitemapindex>"), encoding="utf-8")
_rb = (OUT / "robots.txt").read_text(encoding="utf-8")
(OUT / "robots.txt").write_text(_rb + "".join(f"Sitemap: {DOMINIO}/sitemap-imagenes-{_pk}.xml\n" for _pk in list(PAISES) + ["inicio"]), encoding="utf-8")
# IndexNow (Bing y buscadores que lo usan): archivo de clave + lista de URLs para enviar después de publicar
_key = hashlib.md5(("indexnow|" + DOMINIO).encode()).hexdigest()
(OUT / f"{_key}.txt").write_text(_key, encoding="utf-8")
(OUT.parent / (OUT.name + "-indexnow-urls.txt")).write_text("\n".join(U(n) for n, *_ in PAGINAS), encoding="utf-8")

# ---- pasada final: enlaces relativos según la profundidad de cada página (cada país es un directorio) y URLs limpias terminadas en «/»
_PREV = os.environ.get("ST_PREVIEW") == "1"
_attr = re.compile(r'(href|src)="(?!https?:|//|mailto:|tel:|data:|javascript:)([^"#]*)(#[^"]*)?"')


def _rel(nombre, t):
    pre = "../" * nombre.count("/")

    def f(m):
        ruta, frag = m.group(2), m.group(3) or ""
        if not _PREV and ruta.endswith("index.html"):
            ruta = ruta[:-10]
        if ruta == "" and not frag:
            return f'{m.group(1)}="{pre or "./"}"'
        if ruta == "" and frag and not pre:
            return f'{m.group(1)}="{frag}"'
        return f'{m.group(1)}="{pre}{ruta}{frag}"'
    t = _attr.sub(f, t)
    t = t.replace("url(img/", f"url({pre}img/").replace('window.ST_ROOT="__ROOT__"', f'window.ST_ROOT="{pre}"')
    return t


def _rel_solo(nombre, t):
    """Modo de una ciudad: quita el prefijo colombia/ibague/ de los enlaces antes de hacerlos relativos."""
    def f(m):
        ruta = m.group(2)
        for pre in (f"{SOLO_PK}/{SOLO_D}/", f"{SOLO_PK}/"):
            if ruta.startswith(pre):
                ruta = ruta[len(pre):] or "index.html"
                break
        if ruta in (SOLO_PK, f"{SOLO_PK}/{SOLO_D}"):
            ruta = "index.html"
        return f'{m.group(1)}="{ruta}{m.group(3) or ""}"'
    return _attr.sub(f, t)


import urllib.parse
import hashlib
if SOLO:
    # ---- enriquecimiento final de cada página: imágenes por sección, índice «En esta página», búsquedas relacionadas, precarga de la imagen principal
    _cc = CIU[0]; _cn = _cc["n"]; _wa_ = wa_vis(_cc["pk"])
    # Fotos por papel dentro de la página (lo que se ve coincide con lo que dice la sección)
    IMG_ROL = {
        "reparar": {"nevera": ["tecnico-reparando-refrigeradora-samsung-en-cocina", "tecnico-samsung-revisando-nevera-con-la-clienta", "tecnico-samsung-visita-a-domicilio-1", "tecnico-samsung-visita-a-domicilio-3", "tecnico-samsung-revisando-compresor", "tecnico-samsung-visita-a-domicilio-2", "tecnico-samsung-visita-a-domicilio-4", "tecnico-samsung-visita-a-domicilio-5", "tecnico-reparando-nevera-samsung", "tecnico-samsung-revision-en-casa"],
                    "lava": ["tecnico-samsung-visita-a-domicilio-6", "tecnico-samsung-reparando-lavadora-a-domicilio", "tecnico-samsung-midiendo-circuito-de-lavadora"],
                    "seca": ["tecnico-samsung-revision-en-casa", "tecnico-samsung-visita-a-domicilio-6"], "lavaplatos": ["tecnico-samsung-revision-en-casa"], "cocina": ["tecnico-samsung-revision-en-casa"], "micro": ["tecnico-samsung-revision-en-casa"],
                    "tv": ["taller-reparacion-televisores-samsung"], None: ["tecnico-samsung-revision-en-casa", "tecnico-samsung-visita-a-domicilio-6", "tecnico-samsung-visita-a-domicilio-1"]},
        "visita": ["tecnico-samsung-saluda-en-la-puerta", "tecnico-samsung-llegando-a-la-puerta-del-cliente", "tecnico-samsung-visita-a-domicilio-7", "tecnico-samsung-a-domicilio-portada", "tecnico-samsung-con-bolso-de-herramientas"],
        "atencion": ["atencion-al-cliente-servicio-samsung", "tecnico-samsung-atendiendo-en-recepcion", "atencion-telefonica-recepcion-servicio-samsung", "asesora-servicio-tecnico-samsung-por-telefono", "cliente-en-recepcion-servicio-tecnico-samsung", "tecnico-samsung-entrega-orden-de-servicio"],
        "producto": {"nevera": ["nevera-samsung-side-by-side-family-hub", "nevera-samsung-superior-inox", "cliente-con-nevera-samsung-family-hub", "familia-en-cocina-con-nevera-samsung"], "lava": ["lavadora-samsung-carga-superior", "torre-de-lavado-samsung"], "seca": ["secadora-samsung-carga-frontal", "torre-lavado-secado-samsung-apilada"],
                     "lavaplatos": ["lavavajillas-samsung-acero-inoxidable", "cocina-con-electrodomesticos-samsung"], "cocina": ["estufa-samsung-4-hornillas-horno", "horno-empotrado-samsung-acero", "cocina-con-electrodomesticos-samsung"], "micro": ["microondas-samsung-ceramic-inside", "cocina-con-electrodomesticos-samsung"],
                     "tv": ["taller-reparacion-televisores-samsung"], None: ["cocina-con-electrodomesticos-samsung", "familia-en-cocina-con-nevera-samsung", "cliente-con-nevera-samsung-family-hub", "nevera-samsung-side-by-side-family-hub", "lavadora-samsung-carga-superior", "secadora-samsung-carga-frontal"]},
    }
    IMG_DESC = {"nevera-samsung-side-by-side-family-hub": "Nevera Samsung Family Hub", "nevera-samsung-superior-inox": "Nevera Samsung de acero inoxidable", "tecnico-reparando-nevera-samsung": "Técnico revisando una nevera Samsung por la parte trasera", "lavadora-samsung-carga-superior": "Lavadora Samsung de carga superior", "tecnico-samsung-reparando-lavadora-a-domicilio": "Técnico Samsung reparando una lavadora de carga frontal a domicilio",
                "torre-de-lavado-samsung": "Torre de lavado Samsung", "secadora-samsung-carga-frontal": "Secadora Samsung de carga frontal", "torre-lavado-secado-samsung-apilada": "Torre de lavado y secado Samsung", "lavavajillas-samsung-acero-inoxidable": "Lavavajillas Samsung de acero inoxidable", "estufa-samsung-4-hornillas-horno": "Estufa Samsung de cuatro hornillas con horno",
                "horno-empotrado-samsung-acero": "Horno empotrado Samsung de acero", "microondas-samsung-ceramic-inside": "Microondas Samsung", "taller-reparacion-televisores-samsung": "Técnico reparando la tarjeta de un televisor Samsung en el taller", "tecnico-samsung-saluda-en-la-puerta": "Técnico Samsung saludando al cliente en la puerta al llegar a la visita",
                "atencion-al-cliente-servicio-samsung": "Asesora atendiendo a un cliente en el mostrador del servicio técnico Samsung", "tecnico-samsung-entrega-orden-de-servicio": "Técnico entregando la orden de servicio en el mostrador del servicio Samsung", "tecnico-samsung-a-domicilio-portada": "Técnico Samsung saludando en la puerta de una casa",
                "atencion-telefonica-recepcion-servicio-samsung": "Asesora del servicio técnico Samsung atendiendo una llamada en recepción", "tecnico-samsung-atendiendo-en-recepcion": "Técnico Samsung conversando con la asesora en la recepción", "tecnico-samsung-llegando-a-la-puerta-del-cliente": "Técnico Samsung saludando a una clienta en la puerta de su casa",
                "tecnico-samsung-revisando-nevera-con-la-clienta": "Técnico Samsung explicando la revisión de una nevera a la clienta", "cliente-en-recepcion-servicio-tecnico-samsung": "Cliente consultando con la asesora en la recepción del servicio técnico Samsung", "asesora-servicio-tecnico-samsung-por-telefono": "Asesora del servicio técnico Samsung al teléfono",
                "tecnico-samsung-midiendo-circuito-de-lavadora": "Técnico Samsung midiendo el circuito eléctrico de una lavadora con un multímetro", "tecnico-reparando-refrigeradora-samsung-en-cocina": "Técnico reparando el compresor de una refrigeradora Samsung en la cocina", "familia-en-cocina-con-nevera-samsung": "Familia en la cocina junto a una nevera Samsung",
                "cliente-con-nevera-samsung-family-hub": "Cliente junto a una nevera Samsung Family Hub", "cocina-con-electrodomesticos-samsung": "Cocina con nevera, lavavajillas, horno y microondas Samsung", "tecnico-samsung-con-bolso-de-herramientas": "Técnico Samsung con su bolso de herramientas", "nevera-samsung-family-hub-pantallas": "Nevera Samsung Family Hub con pantallas",
                "tecnico-samsung-revisando-compresor": "Técnico Samsung con herramientas revisando el compresor de una nevera", "tecnico-samsung-revision-en-casa": "Técnico Samsung concentrado en una revisión dentro de la cocina del cliente",
                "tecnico-samsung-visita-a-domicilio-1": "Técnico Samsung revisando la parte trasera de una nevera con el cliente presente", "tecnico-samsung-visita-a-domicilio-2": "Técnico Samsung arrodillado junto a su caja de herramientas revisando una nevera",
                "tecnico-samsung-visita-a-domicilio-3": "Técnico Samsung inspeccionando una nevera con una linterna", "tecnico-samsung-visita-a-domicilio-4": "Técnico Samsung revisando el interior de una nevera mientras el cliente observa",
                "tecnico-samsung-visita-a-domicilio-5": "Técnico Samsung diagnosticando una nevera en la cocina", "tecnico-samsung-visita-a-domicilio-6": "Técnico Samsung midiendo el circuito de una lavadora de carga frontal", "tecnico-samsung-visita-a-domicilio-7": "Técnico Samsung saludando al cliente en la puerta"}
    def _dim(nombre_img):
        try:
            from PIL import Image as _PI
            return _PI.open(OUT / "img" / f"{nombre_img}.webp").size
        except Exception:
            return (1024, 572)
    PROD = {"nevera-samsung-side-by-side-family-hub", "nevera-samsung-superior-inox", "lavadora-samsung-carga-superior", "torre-de-lavado-samsung", "secadora-samsung-carga-frontal", "torre-lavado-secado-samsung-apilada", "lavavajillas-samsung-acero-inoxidable", "estufa-samsung-4-hornillas-horno", "horno-empotrado-samsung-acero", "microondas-samsung-ceramic-inside"}
    _PAL = {sv_: (pal(_cc["pk"], sv_)[0], pal(_cc["pk"], sv_)[1]) for sv_ in SERV_PAIS[_cc["pk"]]}
    _WORDS = sorted([(slug(w), sv_) for sv_, (a_, b_) in _PAL.items() for w in {a_, b_}] + [("estufa", "cocina"), ("horno", "cocina"), ("televisor", "tv"), ("lavavajillas", "lavaplatos"), ("lavaplatos", "lavaplatos")], key=lambda x: -len(x[0]))
    _ZSLUG = {slug(z): z for z in _cc["zonas"]}
    _sv_de = lambda n: next((sv_ for w, sv_ in _WORDS if w in n and sv_ in _PAL), None)
    _TOC_N = 9

    _FALLAS_RE = r"(no-|con-|hace-|huele|gotea|se-|puerta|vibra|espuma|llama|olor|perilla|horno-|hornillas|display|deja|tiene|consume|cuanto-cuesta|pantalla|lineas|manchas|sin-sonido|parpadea|hdmi|control-remoto|smart-tv)"
    _TERM_RE = r"^(mantenimiento-|instalacion-|tecnico-a-domicilio-|cerca-de-mi-|repuestos-|garantia-|diagnostico-|como-elegir-tecnico-|centro-de-servicio-|falla-urgente-)"
    _EQ_SLUGS = {slug(b_) for a_, b_ in _PAL.values()}
    _PLUR_RE = "|".join(re.escape(cap(b_)) for a_, b_ in _PAL.values())

    def _kind(seg):
        if not seg:
            return "home"
        if seg[-1] in ("whatsapp", "telefono"):
            return "contacto"
        if seg[-1] == "galeria":
            return "galeria"
        if len(seg) == 1:
            if seg[0] in _ZSLUG:
                return "zona"
            if re.match(_TERM_RE, seg[0]):
                return "termino"
            if seg[0] in _EQ_SLUGS:
                return "equipo"
            if re.search(_FALLAS_RE, seg[0]):
                return "falla"
            return "otro"
        if len(seg) == 2 and seg[0] in _ZSLUG:
            return "zona_equipo" if seg[1] in _EQ_SLUGS else "zona_falla"
        return "otro"

    def _rank(kind, h, ciudad_re):
        """Posición de cada sección en el recorrido de la página (menor = más arriba). None = se elimina."""
        if re.search(r"Búsquedas relacionadas", h):
            return 95
        if re.search(r"^Preguntas rápidas", h):
            return 78
        if re.search(r"^(Preguntas|¿.*\?$)", h) and not re.search(r"Prefieres", h):
            return 80
        if re.search(r"^Contacto del servicio|^Otro canal", h):
            return 85
        if re.search(r"^Qué enviar por WhatsApp", h):
            return 10
        if re.search(r"^Mapa:", h):
            return 35 if kind in ("home", "zona") else 88
        if re.search(r"^Todos los electrodomésticos", h):
            return {"home": 10, "zona": 12, "equipo": 62}.get(kind)
        if re.search(r"^Atención en", h):
            return 5
        if re.search(r"^(Qué es|Para qué sirve)", h):
            return 5
        if re.search(r"^Cuándo (conviene|hay que)", h):
            return 18
        if re.search(r"^Qué hace el técnico", h):
            return 30
        if kind == "equipo" and re.search(rf"^({_PLUR_RE}) Samsung en {ciudad_re}$", h):
            return 5
        if kind == "termino" and re.search(r"^Qué incluye en ", h):
            return 6
        if kind == "otro" and re.search(r"^¿Prefieres que lo revise", h):
            return 58
        if kind == "otro" and re.search(r"^Glosario de partes", h):
            return 57
        if kind == "otro" and re.search(r"^Qué incluye la visita", h):
            return 59
        if kind == "otro" and h == "Barrios":
            return 10
        if kind == "otro" and h == "Equipo por barrio":
            return 20
        if re.search(r"^Fallas de .* que sí", h):
            return 23
        if re.search(r"^Conviene reparar", h):
            return 20
        if re.search(r"^Conviene cambiar", h):
            return 21
        if re.search(r"^Fallas más comunes", h):
            return None if kind == "home" else 40
        if re.search(r"^Fallas frecuentes en", h):
            return 40
        if re.search(r"^(Fallas que (atendemos|reparamos)|Qué revisa el técnico|Causas más comunes|Fallas frecuentes de|Todas las fallas|Qué influye en el valor|Fallas de .* que sí)", h):
            return 20
        if re.search(r"^Qué revisar primero", h):
            return 22
        if re.search(r"^Señales", h):
            return 25
        if re.search(r"^Cómo funciona el servicio en ", h) and kind == "zona":
            return None
        if re.search(r"^(Cómo (funciona|coordinamos|decidir|pedir)|Cómo es la visita)", h):
            return 20 if kind == "home" else 30
        if re.search(r"^Qué incluye y qué debes saber", h) and kind in ("equipo", "zona_equipo"):
            return None
        if re.search(r"^(Qué incluye|Prepara|Seguridad con)", h):
            return 25 if kind == "home" else 35
        if kind == "equipo" and re.search(r"^(Todo sobre|Guías y fallas de|Sectores)", h):
            return None
        if re.search(r"^Sectores", h):
            return 30 if kind == "home" else 41
        if kind == "zona" and re.search(r"^Equipos que reparamos en", h):
            return 13
        if re.search(r"^Servicio técnico por barrio", h):
            return 31
        if re.search(r"^Datos de", h):
            return 32 if kind == "home" else 42
        if re.search(r"por barrio|otros barrios|^Zonas cercanas|cerca de ti|^Equipos que reparamos en|^Otros equipos", h):
            return 41 if kind != "zona" else 45
        if kind == "zona" and re.search(r" Samsung en [^:]+$", h) and not re.search(r"^(Guías|Todo sobre|Más sobre|Mantenimiento)", h):
            return 14
        if re.search(r"clima", h):
            return 50
        if re.search(r"^Cuidados|^Hábitos", h):
            return 51
        if re.search(r"^Mitos", h):
            return 52
        if re.search(r"^Glosario", h):
            return 53
        if re.search(r"^(Guías|Galería|Artículos|Más información|Más sobre|Todo sobre|Ayuda con|Sigue leyendo|Mantenimiento de)", h):
            return 60
        return 55

    def _enriquecer(n, t):
        n2 = solo_ruta(n)
        seg = [x for x in n2.split("/") if x and x != "index.html"]
        barrio = next((_ZSLUG[x] for x in seg if x in _ZSLUG), None)
        sv_ = _sv_de(n2)
        lugar = barrio or _cn
        hero = RN.get(hero_img(n), hero_img(n))
        kind = _kind(seg)
        s1 = _PAL[sv_][0] if sv_ else "electrodoméstico"; s2 = _PAL[sv_][1] if sv_ else "electrodomésticos"
        # --- secciones extra: mapa (portada y barrios) y búsquedas relacionadas
        extra = []
        if kind in ("home", "zona") and n2 != "404.html":
            q_ = urllib.parse.quote_plus(f"{lugar}, {_cn}, {PAISES[_cc['pk']]['nombre']}")
            extra.append(f'<section class="aq-sec"><div class="wrap"><h2>Mapa: atendemos {html.escape(lugar)}</h2><iframe title="Mapa de {html.escape(lugar)}" src="https://www.google.com/maps?q={q_}&amp;output=embed" width="100%" height="320" style="border:0;border-radius:16px" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><p class="sub2">Visita a domicilio en esta zona; escribe al {html.escape(_wa_)}.</p></div></section>')
        fr = [f"servicio técnico Samsung {lugar}", f"técnico de {s2} Samsung {lugar}", f"reparación de {s2} Samsung a domicilio {lugar}", f"{s1} Samsung no funciona {lugar}", f"mantenimiento de {s2} Samsung {lugar}", f"cuánto cuesta reparar {s1} Samsung {lugar}",
              f"técnico Samsung cerca de mí {lugar}", f"WhatsApp servicio técnico Samsung {_cn}", f"teléfono servicio técnico Samsung {_cn}", f"repuestos para {s2} Samsung {_cn}", f"garantía de {s1} Samsung {_cn}", f"{s2} Samsung {_cn} a domicilio"]
        extra.append('<section class="aq-sec"><div class="wrap"><h2>Búsquedas relacionadas en ' + html.escape(lugar) + '</h2><div class="city-tags">' + "".join(f"<span>{html.escape(f_)}</span>" for f_ in fr) + f'<a href="{R_WA(_cc)}">WhatsApp {html.escape(_wa_)}</a></div></div></section>')
        # --- orden consecutivo de las secciones
        mh0 = re.search(r'<section class="hero[^"]*"[^>]*>.*?</section>', t, re.S)
        ft = t.find('<footer class="aq-f">')
        if mh0 and ft > mh0.end():
            region = t[mh0.end():ft]
            blocks = list(re.finditer(r'<section class="([^"]*)"[^>]*>.*?</section>', region, re.S))
            if "".join(b.group(0) for b in blocks).strip() == region.strip() or True:
                tops, body = [], []
                ciudad_re = re.escape(_cn)
                for b in blocks:
                    cls = b.group(1)
                    h2m = re.search(r"<h2>(.*?)</h2>", b.group(0), re.S)
                    if "aq-qa-sec" in cls:
                        tops.append(b.group(0)); continue
                    h = re.sub(r"<[^>]+>", "", h2m.group(1)).strip() if h2m else ""
                    body.append((h, b.group(0), "st-equipos" in cls))
                for ex in extra:
                    h2m = re.search(r"<h2>(.*?)</h2>", ex, re.S)
                    body.append((re.sub(r"<[^>]+>", "", h2m.group(1)), ex, False))
                vistos = set(); ordenadas = []
                for k_, (h, blk, _p) in enumerate(body):
                    r = _rank(kind, h, ciudad_re)
                    if r is None or h in vistos:
                        continue
                    vistos.add(h)
                    ordenadas.append((r, k_, blk))
                ordenadas.sort(key=lambda x: (x[0], x[1]))
                nuevo = []
                for pos, (r, k_, blk) in enumerate(ordenadas):
                    blk = re.sub(r'^<section class="[^"]*"', '<section class="aq-sec chap' + (" alt" if pos % 2 else "") + (" st-equipos" if "st-equipos" in blk[:80] else "") + '"', blk, count=1)
                    nuevo.append(blk)
                _eqs = "".join(f'<a href="{R_CS(_cc, e_)}">{html.escape(cap(_PAL[e_][1]))} Samsung en {html.escape(_cn)}</a>' for e_ in _PAL)
                _int = (f'<a href="{R_CIU(_cc)}">Servicio técnico Samsung en {html.escape(_cn)}</a>' + _eqs + f'<a href="{R_BARRIOS(_cc)}">Barrios donde atendemos</a><a href="{R_WA(_cc)}">WhatsApp del servicio técnico</a><a href="{R_GUIAS(_cc["pk"])}">Guías de reparación Samsung</a><a href="{R_FAQ(_cc["pk"])}">Preguntas frecuentes</a>'
                        + (f'<a href="{R_UBIC(_cc)}">Ubicación y horario</a><a href="{R_24H(_cc)}">Servicio 24 horas</a>' if SOLO_CFG[SOLO].get("direccion") else ""))
                _WK = {"nevera": ("Refrigerador", "Refrigerador (Wikipedia)"), "lava": ("Lavadora_(electrodoméstico)", "Lavadora (Wikipedia)"), "seca": ("Secadora_de_ropa", "Secadora de ropa (Wikipedia)"), "lavaplatos": ("Lavavajillas", "Lavavajillas (Wikipedia)"), "micro": ("Horno_de_microondas", "Horno de microondas (Wikipedia)"), "cocina": ("Cocina_(aparato)", "Cocina y horno (Wikipedia)"), "tv": ("Televisor", "Televisor (Wikipedia)")}
                _ex = []
                if sv_ in _WK:
                    _ex.append(f'<a href="https://es.wikipedia.org/wiki/{_WK[sv_][0]}" target="_blank" rel="noopener noreferrer">{_WK[sv_][1]}</a>')
                if _cc["pk"] == "colombia":
                    _ex += ['<a href="https://www.samsung.com/co/support/" target="_blank" rel="noopener noreferrer">Sitio de soporte de Samsung Colombia (marca)</a>', '<a href="https://www.sic.gov.co/" target="_blank" rel="noopener noreferrer">Superintendencia de Industria y Comercio (derechos del consumidor)</a>']
                _ex.append(f'<a href="https://www.google.com/maps/search/?api=1&amp;query={urllib.parse.quote_plus(_cn + " " + PAISES[_cc["pk"]]["nombre"])}" target="_blank" rel="noopener noreferrer">{html.escape(_cn)} en Google Maps</a>')
                nuevo.append('<section class="aq-sec chap' + (" alt" if len(nuevo) % 2 else "") + f'"><div class="wrap"><h2>Más sobre {html.escape(s2)} Samsung en {html.escape(lugar)}</h2><div class="city-tags">' + _int + '</div><h3 style="margin:18px 0 8px">Enlaces de interés</h3><div class="city-tags">' + "".join(_ex) + '</div></div></section>')
                t = t[:mh0.end()] + "".join(tops) + "".join(nuevo) + t[ft:]
        # --- ids de sección + imágenes
        cnt = [0]; usadas = []

        def _rol(plano):
            if re.search(r"(?i)atenci|contacto|whatsapp|enviar|pedir|recepci", plano):
                return "atencion"
            if re.search(r"(?i)fallas|causas|revis|señales|diagnóstico|repar|conviene|pieza|cambio", plano):
                return "reparar"
            if re.search(r"(?i)cómo funciona|coordinamos|incluye|prepara|seguridad|visita|cotizaci", plano):
                return "visita"
            return "producto"

        def _foto(rol):
            if rol == "reparar":
                cand = IMG_ROL["reparar"].get(sv_) or IMG_ROL["reparar"][None]
            elif rol == "producto":
                cand = IMG_ROL["producto"].get(sv_) or IMG_ROL["producto"][None]
            else:
                cand = IMG_ROL[rol]
            off = int(hashlib.md5(n2.encode()).hexdigest()[:6], 16)
            libres = [c for c in cand if c not in usadas]
            if libres:
                return libres[off % len(libres)]
            if rol in ("reparar", "producto"):
                libres = [c for c in IMG_ROL["visita"] if c not in usadas]
                if libres:
                    return libres[off % len(libres)]
            return None

        def sec(m):
            cnt[0] += 1
            h2 = m.group(3)
            cls = m.group(1) or ""
            tag = f'<section class="aq-sec{cls}" id="s{cnt[0]}"><div class="wrap"><h2>{h2}</h2>'
            plano = re.sub(r"<[^>]+>", "", h2)
            if "st-equipos" in cls or re.search(r"(?i)preguntas|faq|relacionadas|^mapa|^barrios|datos|sectores|por barrio|otros barrios|zonas cercanas|cerca de ti|otro canal|más información|más sobre|todo sobre|guías y|^en esta", plano) or len(usadas) >= 8 or kind == "galeria":
                return tag
            nombre_img = _foto(_rol(plano))
            if not nombre_img:
                return tag
            usadas.append(nombre_img)
            desc = IMG_DESC.get(nombre_img, "Técnico Samsung a domicilio")
            prod = nombre_img in PROD
            alt = f"{desc} en {lugar}" + (f", {_cn}" if barrio else "")
            w_, h_ = _dim(nombre_img)
            lado = " izq" if len(usadas) % 2 == 0 else ""
            return tag + f'<figure class="sec-img{" prod" if prod else ""}{lado}" style="max-width:{min(w_, 420 if prod else 560)}px"><img src="img/{nombre_img}.webp" alt="{html.escape(alt, quote=True)}" width="{w_}" height="{h_}" loading="lazy" decoding="async" onerror="this.parentNode.remove()"><figcaption>{html.escape(desc)}</figcaption></figure>'
        t = re.sub(r'<section class="aq-sec((?: [a-z-]+)*)"( id="[^"]*")?><div class="wrap"><h2>(.*?)</h2>', lambda m: sec(m), t)
        # --- encabezado dividido: texto + foto a su tamaño nativo
        mh = re.search(r'<section class="hero st-bg" style="--bgimg:url\(([^)]*)\)"><div class="wrap">(.*?)</div></section>', t, re.S)
        if mh:
            himg = hero
            hw, hh = _dim(himg)
            hdesc = IMG_DESC.get(himg, "Técnico Samsung a domicilio")
            fig = f'<figure class="st-hfig"><img src="img/{himg}.webp" alt="{html.escape(hdesc + " en " + lugar, quote=True)}" width="{hw}" height="{hh}" fetchpriority="high" decoding="async" onerror="this.parentNode.remove()"></figure>'
            t = t.replace(mh.group(0), f'<section class="hero st-split"><div class="wrap st-hgrid"><div class="st-ht">{mh.group(2)}</div>{fig}</div></section>', 1)
        # --- índice numerado «En esta página» (mismo orden y números que los capítulos)
        hs = re.findall(r'<section class="aq-sec chap[^"]*" id="(s\d+)"><div class="wrap"><h2>(.*?)</h2>', t)
        if len(hs) >= 3:
            toc = '<nav class="toc" aria-label="En esta página"><b>En esta página</b><ol>' + "".join(f'<li><a href="#{i_}">{re.sub(r"<[^>]+>", "", h_)}</a></li>' for i_, h_ in hs[:16]) + "</ol></nav>"
            t = re.sub(r'(<section class="aq-qa-sec">.*?</section>)(?!.*<section class="aq-qa-sec">)', lambda m: m.group(1) + f'<section class="aq-sec toc-sec"><div class="wrap">{toc}</div></section>', t, count=1, flags=re.S)
        # --- precarga de la imagen principal y imagen en los datos estructurados
        t = t.replace("</head>", f'<link rel="preload" as="image" href="img/{hero}.webp" fetchpriority="high"></head>', 1)
        t = t.replace('{"@type": "WebPage",', f'{{"@type": "WebPage", "primaryImageOfPage": {{"@type": "ImageObject", "url": "{DOMINIO}/img/{hero}.webp"}},', 1)
        return t
    for _n, *_r in PAGINAS:
        _f = OUT / _n
        _f.write_text(_enriquecer(_n, _f.read_text(encoding="utf-8")), encoding="utf-8")

if SOLO:
    import os as _os
    _nuevos = []
    for _n, *_r in PAGINAS:
        _f = OUT / _n
        _nn = solo_ruta(_n)
        _t = _f.read_text(encoding="utf-8")
        _t = _rel_solo(_n, _t)
        _t = _t.replace(f"{DOMINIO}/{SOLO_PK}/{SOLO_D}/", f"{DOMINIO}/").replace(f"{DOMINIO}/{SOLO_PK}/", f"{DOMINIO}/")
        _d = OUT / _nn
        _d.parent.mkdir(parents=True, exist_ok=True)
        _d.write_text(_t, encoding="utf-8")
        if _d != _f:
            _f.unlink()
        _nuevos.append((_nn, *_r))
    for _x in ("buscar.js", "llms.txt", "llms-full.txt", "datos-servicio-tecnico.json"):
        _o = OUT / SOLO_PK / _x
        if _o.exists():
            _tx = _o.read_text(encoding="utf-8").replace(f"{DOMINIO}/{SOLO_PK}/{SOLO_D}/", f"{DOMINIO}/").replace(f"{DOMINIO}/{SOLO_PK}/", f"{DOMINIO}/")
            if _x in ("llms.txt", "llms-full.txt"):
                _tx = _tx.replace("1 ciudades", "1 ciudad").replace("Servicio técnico Samsung en Colombia", f"Servicio técnico Samsung en {CIU[0]['n']}, {CIU[0]['dep']}").replace("Samsung en Colombia (no", f"Samsung en {CIU[0]['n']}, Colombia (no")
            (OUT / _x).write_text(_tx, encoding="utf-8"); _o.unlink()
    for _x in ("geo.js",):
        if (OUT / SOLO_PK / _x).exists():
            (OUT / SOLO_PK / _x).unlink()
    for _a, _b in ((f"sitemap-{SOLO_PK}.xml", f"sitemap-{SOLO}.xml"), (f"sitemap-imagenes-{SOLO_PK}.xml", f"sitemap-imagenes-{SOLO}.xml")):
        if (OUT / _a).exists():
            if _a != _b:
                (OUT / _b).write_text((OUT / _a).read_text(encoding="utf-8"), encoding="utf-8"); (OUT / _a).unlink()
    for _x in [p for p in OUT.glob("sitemap*.xml")] + [OUT / "robots.txt"]:
        _tx = _x.read_text(encoding="utf-8").replace(f"sitemap-{SOLO_PK}.xml", f"sitemap-{SOLO}.xml").replace(f"sitemap-imagenes-{SOLO_PK}.xml", f"sitemap-imagenes-{SOLO}.xml")
        _tx = _tx.replace(f"{DOMINIO}/{SOLO_PK}/{SOLO_D}/", f"{DOMINIO}/").replace(f"{DOMINIO}/{SOLO_PK}/", f"{DOMINIO}/")
        _x.write_text(_tx, encoding="utf-8")
    for _x in ("sitemap-inicio.xml", "sitemap-imagenes-inicio.xml"):
        if (OUT / _x).exists():
            (OUT / _x).unlink()
    _sm = (OUT / "sitemap.xml").read_text(encoding="utf-8")
    _sm = re.sub(r"  <sitemap><loc>[^<]*(?:sitemap-inicio|sitemap-imagenes-inicio)\.xml</loc>.*?</sitemap>\n", "", _sm)
    for _pk in PAISES:
        pass
    for _pk2 in [k_ for k_ in ("colombia", "panama", "costa-rica", "paraguay", "guatemala", "el-salvador", "ecuador", "chile") if k_ != SOLO and k_ != SOLO_PK or (k_ == SOLO_PK and SOLO_PK != SOLO)]:
        _sm = re.sub(rf"  <sitemap><loc>[^<]*sitemap(?:-imagenes)?-{_pk2}\.xml</loc>.*?</sitemap>\n", "", _sm)
    (OUT / "sitemap.xml").write_text(_sm, encoding="utf-8")
    _rb = (OUT / "robots.txt").read_text(encoding="utf-8")
    _otros = "|".join(["inicio"] + [k_ for k_ in ("colombia", "panama", "costa-rica", "paraguay", "guatemala", "el-salvador", "ecuador", "chile") if k_ != SOLO and k_ != SOLO_PK] + ([SOLO_PK] if SOLO_PK != SOLO else []))
    _rb = re.sub(rf"Sitemap: [^\n]*sitemap(?:-imagenes)?-(?:{_otros})\.xml\n", "", _rb)
    (OUT / "robots.txt").write_text(_rb, encoding="utf-8")
    _imgs = sorted(p.name for p in (OUT / "img").glob("*") if p.suffix in (".webp", ".png", ".jpg"))
    (OUT / "prueba-imagenes.html").write_text('<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prueba de imágenes</title><style>body{font:14px sans-serif;margin:16px}div{display:inline-block;width:200px;margin:6px;vertical-align:top}img{width:200px;height:120px;object-fit:contain;background:#eee;border:1px solid #ccc}</style></head><body><h1>Prueba de imágenes (' + str(len(_imgs)) + ')</h1><p>Si ves un cuadro roto o vacío, ese archivo no está en el servidor: sube de nuevo la carpeta <b>img</b> completa.</p>' + "".join(f'<div><img src="img/{n}" alt=""><br>{n}</div>' for n in _imgs) + "</body></html>", encoding="utf-8")
    PAGINAS[:] = [tuple(x) for x in _nuevos]
    for _n, *_r in PAGINAS:
        _f = OUT / _n
        _f.write_text(_rel(_n, _f.read_text(encoding="utf-8")), encoding="utf-8")
    for _d in sorted((OUT / SOLO_PK).rglob("*"), reverse=True) if (OUT / SOLO_PK).exists() else []:
        try:
            _d.rmdir() if _d.is_dir() else None
        except OSError:
            pass
    try:
        (OUT / SOLO_PK).rmdir()
    except OSError:
        pass
else:
    for _n in [n for n, *_ in PAGINAS]:
        _f = OUT / _n
        _f.write_text(_rel(_n, _f.read_text(encoding="utf-8")), encoding="utf-8")

# ---- versión por contenido en CSS y JS: si cambia un archivo, el navegador lo descarga de nuevo aunque lo tenga guardado
import hashlib as _hl2, posixpath as _pp
_attr_v = re.compile(r'(href|src)="([^"#?]*?(?:tema\.css|buscar\.js|solicitar\.js|geo\.js))(?:\?v=[\w]+)?"')
_hcache = {}


def _vh(path):
    if path not in _hcache:
        _hcache[path] = _hl2.md5(path.read_bytes()).hexdigest()[:8] if path.exists() else ""
    return _hcache[path]


for _n in [n for n, *_ in PAGINAS]:
    _f = OUT / _n
    _base = _pp.dirname(_n)
    _t = _f.read_text(encoding="utf-8")

    def _sub(m):
        _dest = OUT / _pp.normpath(_pp.join(_base, m.group(2)))
        _h = _vh(_dest)
        return f'{m.group(1)}="{m.group(2)}?v={_h}"' if _h else m.group(0)
    _t2 = _attr_v.sub(_sub, _t)
    if _t2 != _t:
        _f.write_text(_t2, encoding="utf-8")
print(f"listo: {OUT} · {len(PAGINAS)} páginas · {len(CIU)} ciudades · {len(PAISES)} países")
